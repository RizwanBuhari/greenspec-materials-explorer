"""The app's pages: product assessment, materials explorer and understanding impact."""

import os
import re
import threading
from datetime import date
from html import escape

import altair as alt
import pandas as pd
import streamlit as st

from greenspec import ai
from greenspec.data import GROUPS, Material, load_materials, load_regulations, regulations_for
from greenspec.icons import icon
from greenspec.report import COMPONENT_LABELS, build_report
from greenspec.scoring import WEIGHTS

COUNTRIES = ["United Arab Emirates", "European Union", "Other (international standards only)"]
DEFAULT_AI_DAILY_LIMIT = 100

SORTS = {
    "Default order": None,
    "Name A–Z": lambda m: m.name,
    "Highest sustainability": lambda m: -m.score.total,
    "Lowest carbon": lambda m: m.carbon,
    "Most recyclable": lambda m: -m.recyclability,
    "Lowest energy": lambda m: m.energy,
}

DIMENSIONS = (
    ("carbon", "Carbon score", "cloud", "Relative greenhouse-gas impact", True),
    ("recyclability", "Recyclability score", "recycle", "Potential for material recovery", False),
    ("energy", "Energy score", "zap", "Relative production energy demand", True),
)


def get_secret(name: str, default: str | None = None) -> str | None:
    try:
        return st.secrets.get(name, default)
    except st.errors.StreamlitSecretNotFoundError:
        return default


@st.cache_data(ttl=300, show_spinner=False)
def _materials_from_sheet(url: str) -> list[Material]:
    return load_materials(url)


def get_materials() -> list[Material]:
    url = get_secret("GOOGLE_SHEET_CSV_URL")
    if url:
        try:
            return _materials_from_sheet(url)
        except Exception:
            st.warning("Could not read the shared Google Sheet, so the app is using its saved copy of the materials.")
    return load_materials()


class _AIStore:
    """Shared across visitors: saved answers, and a daily cap to protect the API budget."""

    def __init__(self):
        self.lock = threading.Lock()
        self.answers: dict[tuple, str] = {}
        self.day = date.today()
        self.calls = 0

    def try_start_call(self, limit: int) -> bool:
        with self.lock:
            if self.day != date.today():
                self.day, self.calls = date.today(), 0
            if self.calls >= limit:
                return False
            self.calls += 1
            return True


@st.cache_resource
def _ai_store() -> _AIStore:
    return _AIStore()


# ---- Shared pieces ----


def intro(eyebrow: str, title: str, description: str, aside: str = "") -> None:
    aside_html = f'<p class="catalog-summary"><span class="dot"></span>{escape(aside)}</p>' if aside else ""
    st.html(
        f"""<div class="intro"><div>
        <p class="eyebrow">{escape(eyebrow)}</p>
        <h1 class="page-title">{escape(title)}</h1>
        <p class="page-description">{escape(description)}</p>
        </div>{aside_html}</div>"""
    )


def notice(text: str) -> None:
    st.html(f'<div class="notice" role="note">{icon("info")}<span>{escape(text)}</span></div>')


def beyond_the_score() -> None:
    items = (
        ("factory", "How it is made", "Recycled content, production methods and the energy mix matter."),
        ("truck", "How far it travels", "Weight, transport distance and local sourcing affect the footprint."),
        ("refresh", "What happens next", "Longer use, repair and a realistic recovery route can change the outcome."),
    )
    columns = "".join(
        f'<div class="beyond-item"><h3>{icon(name)} {title}</h3><p>{text}</p></div>' for name, title, text in items
    )
    st.html(
        f"""<section class="beyond"><div><p class="eyebrow">Beyond the score</p>
        <h2>A material is only part of the story.</h2></div>{columns}</section>
        <footer class="site-footer"><span>GreenSpec AI / Material intelligence, with context.</span>
        <span>Exploration, not certification. No material is sustainable in every application.</span></footer>"""
    )


def _is_favourable(key: str, value: float) -> bool:
    return value >= 5 if key == "recyclability" else value < 5


def _track(key: str, value: float, large: bool = False) -> str:
    tone = "good" if _is_favourable(key, value) else "poor"
    return (
        f'<span class="track{" track-lg" if large else ""}">'
        f'<span class="bar {tone}" style="width:{value * 10:g}%"></span></span>'
    )


# ---- Assess a product ----


def _breakdown_chart(points: dict[str, float]) -> alt.Chart:
    rows = pd.DataFrame(
        {
            "Component": [f"{COMPONENT_LABELS[key]} ({WEIGHTS[key]:.0%})" for key in COMPONENT_LABELS],
            "Points": [points[key] for key in COMPONENT_LABELS],
        }
    )
    base = alt.Chart(rows).encode(
        y=alt.Y("Component:N", sort=None, title=None, axis=alt.Axis(domain=False, ticks=False, labelLimit=180, labelFontSize=12)),
    )
    bars = base.mark_bar(color="#244D3E", size=16, cornerRadiusEnd=4).encode(
        x=alt.X("Points:Q", scale=alt.Scale(domain=[0, 10]), title="Points out of 10 (higher is better)",
                axis=alt.Axis(values=[0, 5, 10], domain=False, ticks=False, gridColor="#E5E7DF", labelFontSize=11, titleFontSize=11, titleFontWeight="normal", titleColor="#73796F")),
        tooltip=["Component", alt.Tooltip("Points:Q", title="Points out of 10")],
    )
    labels = base.mark_text(align="left", dx=6, color="#24392F", fontSize=12).encode(x="Points:Q", text=alt.Text("Points:Q", format="~g"))
    return (bars + labels).properties(height=150, background="transparent").configure_view(stroke=None)


def _assessment_key(assessment: dict) -> tuple:
    return tuple(assessment[field] for field in ("product", "material", "process", "country"))


def _generate_suggestions(assessment: dict, materials: list[Material]) -> None:
    """Fills st.session_state.ai_text, or ai_error with the reason it could not."""
    store = _ai_store()
    key = _assessment_key(assessment)
    if key in store.answers:
        st.session_state.ai_text = store.answers[key]
        return

    api_key = get_secret("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.session_state.ai_error = "AI suggestions are not connected yet: the app has no Claude API key."
        return
    if not store.try_start_call(int(get_secret("AI_DAILY_LIMIT", DEFAULT_AI_DAILY_LIMIT))):
        st.session_state.ai_error = "The app has reached its daily limit for AI suggestions. Please try again tomorrow."
        return

    prompt = ai.build_prompt(*key, materials)
    model = get_secret("ANTHROPIC_MODEL", ai.DEFAULT_MODEL)
    try:
        text = st.write_stream(ai.stream_suggestions(prompt, api_key=api_key, model=model))
    except ai.AIError as error:
        st.session_state.ai_error = str(error)
        st.session_state.ai_retryable = True
        st.rerun()
    store.answers[key] = st.session_state.ai_text = text
    st.rerun()


def _render_suggestions(assessment: dict, materials: list[Material]) -> None:
    st.html(f'<h3 class="card-title">{icon("sprout", 18)} Greener alternatives</h3>')
    if st.session_state.get("ai_text"):
        # A bold material name followed by a single newline would otherwise run into its explanation.
        st.markdown(re.sub(r"\*\*[ \t]*\n(?!\n)", "**\n\n", st.session_state.ai_text))
        st.html('<p class="muted-note">Written by Claude. An engineer should check that these are practical.</p>')
    elif not st.session_state.get("ai_error"):
        with st.spinner("Claude is reviewing your product…"):
            _generate_suggestions(assessment, materials)
    if st.session_state.get("ai_error"):
        st.warning(st.session_state.ai_error)
        if st.session_state.get("ai_retryable") and st.button("Try again", key="retry_ai"):
            st.session_state.ai_error = None
            st.session_state.ai_retryable = False
            st.rerun()


def _render_regulations(applicable: dict[str, list[str]]) -> None:
    sections = "".join(
        f'<h4 class="reg-name">{escape(name)}</h4><ul class="reg-list">'
        + "".join(f"<li>{escape(rule)}</li>" for rule in rules)
        + "</ul>"
        for name, rules in applicable.items()
    )
    st.html(
        f"""<h3 class="card-title">{icon("scanEye", 18)} Regulations to check</h3>{sections}
        <p class="muted-note">A summary for guidance, not legal advice.</p>"""
    )


def _render_results(assessment: dict, materials: list[Material]) -> None:
    with st.container(key="card_score"):
        left, right = st.columns([2, 3], gap="medium")
        left.html(
            f"""<p class="eyebrow">Sustainability score</p>
            <p class="hero-figure">{assessment["total"]}<small> / 100</small></p>
            <p class="band band-{assessment["band"].lower()}">{escape(assessment["band"])}</p>
            <p class="result-product"><strong>{escape(assessment["product"])}</strong><br>
            {escape(assessment["material"])} · {escape(assessment["country"])}</p>"""
        )
        right.altair_chart(_breakdown_chart(assessment["points"]), width="stretch")

    with st.container(key="card_ai"):
        _render_suggestions(assessment, materials)

    applicable = regulations_for(assessment["country"], load_regulations())
    with st.container(key="card_regs"):
        _render_regulations(applicable)

    with st.container(key="card_report"):
        text_col, button_col = st.columns([3, 2], vertical_alignment="center")
        text_col.html(
            '<h3 class="card-title">GreenSpec Report</h3>'
            '<p class="muted-note">A PDF of this score, the suggestions and the regulations, ready to share.</p>'
        )
        slug = re.sub(r"[^a-z0-9]+", "-", assessment["product"].lower()).strip("-") or "product"
        button_col.download_button(
            "Download PDF report",
            data=build_report(assessment, st.session_state.get("ai_text"), applicable),
            file_name=f"greenspec-report-{slug}.pdf",
            mime="application/pdf",
            type="primary",
            width="stretch",
            on_click="ignore",
        )


def assess_page() -> None:
    materials = get_materials()
    by_name = {m.name: m for m in materials}

    intro(
        "Product assessment",
        "How sustainable is your product?",
        "Tell us about it to get a sustainability score, greener alternatives and the rules that apply.",
    )
    notice("Scores are indicative ratings assigned by the project team, not verified measurements or a basis for specification.")

    form_col, results_col = st.columns([5, 8], gap="medium")

    with form_col, st.container(key="card_form"):
        st.html('<h2 class="card-heading">Your product</h2>')
        with st.form("product_form", border=False):
            product = st.text_input("Product name", max_chars=100, placeholder="e.g. Steel chair")
            material = st.selectbox("Material it is made from", list(by_name), index=None, placeholder="Choose a material")
            process = st.text_input("How it is manufactured", max_chars=200, placeholder="e.g. Cut, welded and powder coated")
            country = st.selectbox("Country it is sold in", COUNTRIES, index=None, placeholder="Choose a market")
            submitted = st.form_submit_button("Submit", type="primary", width="stretch")
        if submitted:
            fields = {"product name": product.strip(), "material": material, "manufacturing method": process.strip(), "country": country}
            blank = [name for name, value in fields.items() if not value]
            if blank:
                st.error(f"Please add the {', '.join(blank)}.")
            else:
                score = by_name[material].score
                st.session_state.assessment = {
                    "product": product.strip(),
                    "material": material,
                    "process": process.strip(),
                    "country": country,
                    "total": score.total,
                    "band": score.band,
                    "points": score.points,
                }
                st.session_state.ai_text = None
                st.session_state.ai_error = None
                st.session_state.ai_retryable = False
        st.html('<p class="muted-note">The score comes from the material. The manufacturing method and market inform the AI suggestions and regulations.</p>')

    with results_col:
        assessment = st.session_state.get("assessment")
        if assessment and assessment["material"] in by_name:
            _render_results(assessment, materials)
        else:
            st.html(
                f"""<div class="empty-state">{icon("sprout", 28)}
                <h3>Your results will appear here</h3>
                <p>Try a steel chair, a plastic bottle, a glass window, a copper wire or a concrete block.</p></div>"""
            )

    beyond_the_score()


# ---- Materials explorer ----


def _visible_materials(materials: list[Material], group: str, query: str, sort: str) -> list[Material]:
    query = query.strip().lower()
    found = [
        m
        for m in materials
        if (group == "all" or m.group == group) and (not query or query in m.name.lower() or query in m.family.lower())
    ]
    sort_key = SORTS[sort]
    return sorted(found, key=sort_key) if sort_key else found


def _material_row(m: Material, selected: bool) -> str:
    cells = "".join(
        f'<span class="score"><span class="score-value">{getattr(m, key):g}</span>{_track(key, getattr(m, key))}</span>'
        for key, *_ in DIMENSIONS
    )
    return f"""<div class="row material-row{" is-selected" if selected else ""}">
        <span class="identity"><span class="swatch" style="background:{m.texture}"></span>
        <span class="material-name">{escape(m.name)}</span></span>
        <span class="family">{escape(m.family)}</span>{cells}
        <span class="row-action">{icon("arrowRight" if selected else "chevronRight")}</span></div>"""


def _profile_html(m: Material) -> str:
    metrics = ""
    for key, label, icon_name, hint, lower_is_better in DIMENSIONS:
        value = getattr(m, key)
        direction = "Lower" if lower_is_better else "Higher"
        arrow = "arrowDown" if lower_is_better else "arrowUp"
        metrics += f"""<div class="metric">
            <div class="metric-top"><span class="metric-label">{icon(icon_name, 18)} {label}</span>
            <span class="metric-value">{value:g}<small> / 10</small></span></div>
            {_track(key, value, large=True)}
            <div class="metric-bottom"><span>{hint}</span>
            <span class="direction">{icon(arrow, 12)} {direction} is better</span></div></div>"""
    tips = "".join(f'<li>{icon("arrowUpRight", 14)}<span>{escape(tip)}</span></li>' for tip in m.tips)
    chip = f"{m.family} material" if m.family.endswith("-based") else m.family
    score = m.score
    return f"""<div class="profile-head"><span class="eyebrow">Material profile</span></div>
        <div class="hero" style="background:{m.texture}"><span class="hero-chip">{escape(chip)}</span></div>
        <div class="profile-body">
        <div class="profile-title"><h2>{escape(m.name)}</h2><span class="pill">Selected</span></div>
        <p class="profile-description">{escape(m.description)}</p>
        <div class="profile-score"><span>Sustainability score</span>
        <span class="metric-value">{score.total}<small> / 100 · {score.band}</small></span></div>
        <div class="env-head"><span>Environmental profile</span><span class="illustrative">Team scores</span></div>
        {metrics}
        <div class="tradeoff"><h3>{icon("scanEye")} Read the trade-offs</h3><p>{escape(m.tradeoff)}</p></div>
        <h3 class="section-title">Before you choose</h3><ul class="tips">{tips}</ul>
        <div class="compare"><h3 class="section-title">Compare the same function</h3>
        <p>Compare equal function and service life, not just material names. These scores have no physical units;
        they are not lifecycle assessment results.</p></div></div>"""


def _select_material(material_id: str) -> None:
    st.session_state.selected_material = material_id


def explorer_page() -> None:
    materials = get_materials()
    by_id = {m.id: m for m in materials}
    selected_id = st.session_state.get("selected_material")
    if selected_id not in by_id:
        selected_id = "wood" if "wood" in by_id else materials[0].id

    intro(
        "The material library",
        "Better choices start with materials.",
        "Explore the trade-offs. Select a material to understand its environmental profile.",
        f"{len(materials)} materials · {len(DIMENSIONS)} impact dimensions",
    )
    notice("Scores are indicative ratings assigned by the project team, not verified measurements or a basis for specification.")

    catalog_col, profile_col = st.columns([950, 482], gap="medium")

    with catalog_col, st.container(key="catalog", gap=None):
        with st.container(key="catalog_controls"):
            title_slot = st.empty()
            search_col, sort_col = st.columns([5, 1.2], gap="small")
            query = search_col.text_input("Search materials", placeholder="Search materials or families…", label_visibility="collapsed")
            sort = sort_col.selectbox("Sort materials", list(SORTS), label_visibility="collapsed")
            group = st.pills("Filter by family", list(GROUPS), format_func=GROUPS.get, default="all", required=True, label_visibility="collapsed", key="family_filter")
            st.html('<p class="score-guidance">Team scale 0–10 · Carbon &amp; energy: lower is better · Recyclability: higher is better</p>')

        visible = _visible_materials(materials, group, query, sort)
        title_slot.html(
            f"""<div class="catalog-title"><h2>All materials <span class="count">{len(visible)}</span></h2>
            <span class="view-state">Library view</span></div>"""
        )

        st.html(
            f"""<div class="row row-head"><span>Material</span><span>Family</span>
            <span class="score-col">Carbon {icon("arrowDown", 11)}</span>
            <span class="score-col">Recyclability {icon("arrowUp", 11)}</span>
            <span class="score-col">Energy {icon("arrowDown", 11)}</span><span></span></div>"""
        )
        for m in visible:
            with st.container(key=f"mrow_{m.id}", gap=None):
                st.html(_material_row(m, m.id == selected_id))
                st.button(f"Select {m.name}", key=f"select_{m.id}", on_click=_select_material, args=(m.id,))
        if not visible:
            st.html('<div class="empty">No materials match your search. Try another word or filter.</div>')

        showing = f"Showing all {len(materials)} materials" if len(visible) == len(materials) else f"Showing {len(visible)} of {len(materials)} materials"
        st.html(
            f"""<div class="catalog-footer"><span>{showing}</span>
            <span class="selected-label">{icon("circleCheck", 14)} {escape(by_id[selected_id].name)} selected</span></div>"""
        )

    with profile_col, st.container(key="profile"):
        st.html(_profile_html(by_id[selected_id]))

    beyond_the_score()


# ---- Understanding impact ----


def impact_page() -> None:
    intro(
        "Understanding impact",
        "How to read a GreenSpec score.",
        "Every material is rated on three dimensions, which combine into one number out of 100.",
    )
    notice("Scores are indicative ratings assigned by the project team, not verified measurements or a basis for specification.")

    cards = (
        ("cloud", "Carbon", "arrowDown", "Lower is better", "The relative greenhouse-gas impact of producing the material: extraction, processing and manufacturing."),
        ("recycle", "Recyclability", "arrowUp", "Higher is better", "How easily the material can be recovered and made into new material. It depends on collection, sorting and whether quality is kept."),
        ("zap", "Energy", "arrowDown", "Lower is better", "The relative energy needed to produce the material. High-temperature steps such as smelting, melting and firing push it up."),
    )
    cards_html = "".join(
        f"""<article class="impact-card"><span class="impact-icon">{icon(name, 20)}</span><h2>{title}</h2>
        <p class="direction">{icon(arrow, 12)} {direction}</p><p>{text}</p></article>"""
        for name, title, arrow, direction, text in cards
    )
    st.html(f'<div class="impact-grid">{cards_html}</div>')
    st.html(
        f"""<section class="how-to"><h2>How the score is calculated</h2>
        <p>Carbon and energy ratings are flipped so that every part reads "higher is better" (a carbon rating of 6 becomes
        4 points). The three parts are then weighted: carbon {WEIGHTS["carbon"]:.0%}, recyclability {WEIGHTS["recyclability"]:.0%},
        energy {WEIGHTS["energy"]:.0%}. The result is shown out of 100: 70 or more is Strong, 50 to 69 is Moderate, and below 50 is Low.</p>
        <h2>Compare the same function</h2>
        <p>Compare equal function and service life, not just material names. A material that lasts twice as long, or can be
        repaired, can outperform one with better scores on paper. These scores have no physical units and are not lifecycle
        assessment results.</p></section>"""
    )
    beyond_the_score()
