"""Runs the real Streamlit app headlessly, using the products the brief suggests testing."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")

PRODUCTS = [
    ("Steel chair", "Steel", "Cut, welded and powder coated", "United Arab Emirates", 52),
    ("Plastic bottle", "Plastic (PET)", "Blow moulded", "European Union", 43),
    ("Glass window", "Glass", "Float glass process", "United Arab Emirates", 60),
    ("Copper wire", "Copper", "Drawn and annealed", "European Union", 52),
    ("Concrete block", "Concrete", "Cast and cured", "Other (international standards only)", 49),
    ("Paper notebook", "Paper / Cardboard", "Pressed and bound", "United Arab Emirates", 77),
    ("Wooden table", "Wood", "Cut and joined", "European Union", 70),
    ("Leather bag", "Leather", "Tanned and stitched", "European Union", 29),
    ("Aluminium can", "Aluminium", "Drawn and ironed", "United Arab Emirates", 38),
    ("PVC pipe", "PVC", "Extruded", "Other (international standards only)", 37),
]


def submit(at, product="", material=None, process="", country=None):
    at.text_input[0].set_value(product)
    at.selectbox[0].set_value(material)
    at.text_input[1].set_value(process)
    at.selectbox[1].set_value(country)
    at.button[0].click()
    return at.run(timeout=30)


@pytest.fixture(autouse=True)
def no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


def test_form_has_four_fields_and_shows_no_result_yet():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert len(at.text_input) == 2 and len(at.selectbox) == 2
    assert "assessment" not in at.session_state


def test_blank_fields_are_reported():
    at = submit(AppTest.from_file(APP, default_timeout=30).run(), product="   ", material="Steel")
    assert not at.exception
    assert "product name" in at.error[0].value and "country" in at.error[0].value
    assert "assessment" not in at.session_state


@pytest.mark.parametrize("product, material, process, country, expected", PRODUCTS)
def test_ten_products(product, material, process, country, expected):
    at = submit(AppTest.from_file(APP, default_timeout=30).run(), product, material, process, country)
    assert not at.exception
    assert at.session_state.assessment["total"] == expected
    # Without a key the app explains itself rather than failing, and the rest still works.
    assert "no Claude API key" in at.warning[0].value
    assert not any(b.label == "Try again" for b in at.button)


def test_unreachable_claude_shows_a_message_and_a_retry(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:9")  # Nothing listens here.
    at = submit(AppTest.from_file(APP, default_timeout=60).run(timeout=60), "Glass jar", "Glass", "Blown", "European Union")
    assert not at.exception
    assert "Could not reach Claude" in at.warning[0].value
    assert any(b.label == "Try again" for b in at.button)
    assert at.session_state.assessment["total"] == 60  # The rest of the result still works.


def test_daily_limit_stops_further_calls():
    from greenspec.views import _AIStore

    store = _AIStore()
    assert [store.try_start_call(limit=2) for _ in range(3)] == [True, True, False]
