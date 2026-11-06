import pandas as pd
import pytest

from greenspec.ai import build_prompt
from greenspec.data import DATA_DIR, _parse, load_materials, load_regulations, regulations_for
from greenspec.report import _clean, build_report
from greenspec.scoring import WEIGHTS, calculate_score


def by_name():
    return {m.name: m for m in load_materials()}


def test_weights_add_up_to_one():
    assert sum(WEIGHTS.values()) == pytest.approx(1)


def test_carbon_and_energy_are_flipped():
    best = calculate_score(carbon=0, recyclability=10, energy=0)
    worst = calculate_score(carbon=10, recyclability=0, energy=10)
    assert (best.total, best.band) == (100, "Strong")
    assert (worst.total, worst.band) == (0, "Low")


@pytest.mark.parametrize(
    "material, expected",
    [("Steel", 52), ("Aluminium", 38), ("Paper / Cardboard", 77), ("Wood", 70), ("Leather", 29)],
)
def test_score_from_team_data(material, expected):
    assert by_name()[material].score.total == expected


def test_out_of_range_score_rejected():
    with pytest.raises(ValueError):
        calculate_score(carbon=11, recyclability=5, energy=5)


def test_database_matches_team_sheet():
    materials = load_materials()
    assert len(materials) == 15
    assert len({m.id for m in materials}) == 15
    steel = by_name()["Steel"]
    assert (steel.carbon, steel.recyclability, steel.energy) == (6, 9, 7)


def test_every_material_has_a_written_profile():
    for m in load_materials():
        assert not m.description.startswith("No description"), m.name
        assert len(m.tips) == 3, m.name


def test_sheet_without_required_column_is_rejected():
    with pytest.raises(ValueError, match="Carbon_Score"):
        _parse(pd.DataFrame({"Material": ["Steel"], "Recyclability_Score": [9], "Energy_Score": [7]}))


def test_new_material_without_profile_still_works():
    table = pd.DataFrame({"Material": ["Bamboo"], "Carbon_Score": [2], "Recyclability_Score": [6], "Energy_Score": [2]})
    assert _parse(table)[0].family == "Other"


def test_regulations_have_three_or_four_points_each():
    for rules in load_regulations().values():
        assert 3 <= len(rules) <= 4


def test_regulations_for_market_include_international():
    rules = load_regulations()
    assert list(regulations_for("European Union", rules)) == ["European Union", "International"]
    assert list(regulations_for("Other (international standards only)", rules)) == ["International"]


def test_prompt_asks_the_briefs_question_and_includes_database():
    prompt = build_prompt("Chair", "Steel", "Welded", "European Union", load_materials())
    assert "This product uses Steel. Suggest two greener alternatives and explain why." in prompt
    assert "Wood: carbon 3, recyclability 7, energy 3" in prompt


ASSESSMENT = {
    "product": "Steel chair",
    "material": "Steel",
    "process": "Cut and welded",
    "country": "United Arab Emirates",
    "total": 52,
    "band": "Moderate",
    "points": {"carbon": 4, "recyclability": 9, "energy": 3},
}


def test_report_is_a_pdf():
    pdf = build_report(ASSESSMENT, "**Wood**\nLower carbon.", regulations_for("United Arab Emirates", load_regulations()))
    assert pdf.startswith(b"%PDF")


def test_report_handles_no_ai_text_and_non_latin_input():
    assessment = {**ASSESSMENT, "product": "كرسي 🪑 — chair " + "x" * 90}
    pdf = build_report(assessment, None, regulations_for("European Union", load_regulations()))
    assert pdf.startswith(b"%PDF")


def test_clean_replaces_typographic_characters():
    assert _clean("a – b’s “c”") == "a - b's \"c\""


def test_data_files_exist():
    assert (DATA_DIR / "materials.csv").exists()
