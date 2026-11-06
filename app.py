"""GreenSpec AI. Run with: streamlit run app.py"""

from pathlib import Path

import streamlit as st

from greenspec.icons import icon
from greenspec.views import assess_page, explorer_page, impact_page

st.set_page_config(page_title="GreenSpec AI", page_icon="🌱", layout="wide")

st.html(f"<style>{(Path(__file__).parent / 'assets' / 'style.css').read_text(encoding='utf-8')}</style>")

PAGES = [
    st.Page(assess_page, title="Assess a product", default=True),
    st.Page(explorer_page, title="Materials explorer", url_path="materials"),
    st.Page(impact_page, title="Understanding impact", url_path="impact"),
]

current = st.navigation(PAGES, position="hidden")

with st.container(key="topnav", horizontal=True, vertical_alignment="center", gap=None):
    st.html(
        f"""<div class="brand"><span class="brand-mark">{icon("sprout", 18)}</span>
        <span class="brand-name">GreenSpec AI</span>
        <span class="brand-descriptor">Material<br>intelligence</span></div>"""
    )
    with st.container(key="navlinks", horizontal=True, gap=None, width="content"):
        for page in PAGES:
            state = "on" if page.url_path == current.url_path else "off"
            with st.container(key=f"navlink_{page.url_path}_{state}", width="content"):
                st.page_link(page, label=page.title)
    st.html('<div class="nav-controls"><span class="status-badge">AI Lab prototype</span></div>')

current.run()
