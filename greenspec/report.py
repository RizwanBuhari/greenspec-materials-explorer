"""Builds the downloadable GreenSpec Report as a PDF."""

import re
from datetime import date

from fpdf import FPDF

GREEN = (36, 77, 62)
INK = (36, 57, 47)
MUTED = (115, 121, 111)
TRACK = (229, 231, 223)

COMPONENT_LABELS = {"carbon": "Low carbon", "recyclability": "Recyclability", "energy": "Low energy"}

DISCLAIMER = (
    "Scores are indicative ratings assigned by the project team, not verified measurements or lifecycle "
    "assessment results. AI suggestions need checking by an engineer. Regulations are a summary for guidance "
    "and are not legal advice."
)

_REPLACEMENTS = str.maketrans(
    {
        "–": "-",
        "—": "-",
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "•": "-",
        "…": "...",
        " ": " ",
    }
)


def _clean(text: str) -> str:
    """The built-in PDF fonts only cover Latin-1, so anything else becomes '?'."""
    return text.translate(_REPLACEMENTS).encode("latin-1", "replace").decode("latin-1")


class _Report(FPDF):
    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", size=8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"GreenSpec AI report - page {self.page_no()}", align="C")


def _heading(pdf: FPDF, text: str) -> None:
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", size=10)


def _paragraph(pdf: FPDF, text: str, **kwargs) -> None:
    pdf.multi_cell(0, 5, _clean(text), new_x="LMARGIN", new_y="NEXT", **kwargs)


def build_report(assessment: dict, ai_text: str | None, regulations: dict[str, list[str]]) -> bytes:
    pdf = _Report(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 10, "GreenSpec Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, f"Generated {date.today():%d %B %Y}", new_x="LMARGIN", new_y="NEXT")

    _heading(pdf, "Product")
    for label, key in (("Name", "product"), ("Material", "material"), ("How it is made", "process"), ("Sold in", "country")):
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(32, 6, label)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, _clean(assessment[key]), new_x="LMARGIN", new_y="NEXT")

    _heading(pdf, "Sustainability score")
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_text_color(*GREEN)
    pdf.cell(26, 14, str(assessment["total"]))
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 14, f"/ 100  -  {assessment['band']}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(*INK)
    for key, label in COMPONENT_LABELS.items():
        value = assessment["points"][key]
        y = pdf.get_y()
        pdf.set_font("Helvetica", size=10)
        pdf.cell(32, 7, label)
        pdf.set_fill_color(*TRACK)
        pdf.rect(pdf.l_margin + 32, y + 2.5, 100, 2.5, style="F")
        pdf.set_fill_color(*GREEN)
        pdf.rect(pdf.l_margin + 32, y + 2.5, value * 10, 2.5, style="F")
        pdf.set_x(pdf.l_margin + 136)
        pdf.cell(0, 7, f"{value:g} / 10", new_x="LMARGIN", new_y="NEXT")

    _heading(pdf, "Greener alternatives (AI suggestions)")
    # Claude's replies use **bold** names, which multi_cell can render directly.
    suggestions = re.sub(r"^#+\s*", "", ai_text, flags=re.MULTILINE) if ai_text else "No AI suggestions were generated."
    _paragraph(pdf, suggestions, markdown=True)

    _heading(pdf, "Regulations to check")
    for name, rules in regulations.items():
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, _clean(name), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        for rule in rules:
            _paragraph(pdf, f"- {rule}")
            pdf.ln(1)

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MUTED)
    _paragraph(pdf, DISCLAIMER)
    return bytes(pdf.output())
