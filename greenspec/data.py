"""Loads the materials database and the content shown alongside it."""

import io
import json
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from greenspec.scoring import Score, calculate_score

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

COLUMNS = {"Carbon_Score": "carbon", "Recyclability_Score": "recyclability", "Energy_Score": "energy"}

GROUPS = {
    "all": "All materials",
    "metals": "Metals",
    "minerals": "Minerals",
    "polymers": "Polymers",
    "fibres": "Fibres & textiles",
    "other": "Other",
}

# Used when the sheet gains a material that has no written profile yet.
DEFAULT_PROFILE = {
    "family": "Other",
    "group": "other",
    "texture": "linear-gradient(135deg, #cfd2c8, #b5b9ad)",
    "description": "No description has been added for this material yet.",
    "tradeoff": "Compare this material's scores against others that could do the same job.",
    "tips": ["Check where the material comes from.", "Design for repair and reuse.", "Confirm local recovery options."],
}


@dataclass(frozen=True)
class Material:
    id: str
    name: str
    carbon: float
    recyclability: float
    energy: float
    family: str
    group: str
    texture: str
    description: str
    tradeoff: str
    tips: tuple[str, ...]

    @property
    def score(self) -> Score:
        return calculate_score(self.carbon, self.recyclability, self.energy)


def _read_table(sheet_csv_url: str | None) -> pd.DataFrame:
    if sheet_csv_url:
        with urllib.request.urlopen(sheet_csv_url, timeout=10) as response:
            return pd.read_csv(io.BytesIO(response.read()))
    return pd.read_csv(DATA_DIR / "materials.csv")


def _parse(table: pd.DataFrame) -> list[Material]:
    missing = {"Material", *COLUMNS} - set(table.columns)
    if missing:
        raise ValueError(f"Materials sheet is missing columns: {sorted(missing)}")

    profiles = json.loads((DATA_DIR / "material_profiles.json").read_text(encoding="utf-8"))
    materials = []
    for row in table.dropna(subset=["Material"]).to_dict("records"):
        name = str(row["Material"]).strip()
        scores = {field: float(row[column]) for column, field in COLUMNS.items()}
        calculate_score(**scores)  # Rejects out-of-range values.
        profile = {**DEFAULT_PROFILE, **profiles.get(name, {})}
        materials.append(
            Material(
                id=re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
                name=name,
                **scores,
                family=profile["family"],
                group=profile["group"],
                texture=profile["texture"],
                description=profile["description"],
                tradeoff=profile["tradeoff"],
                tips=tuple(profile["tips"]),
            )
        )
    if not materials:
        raise ValueError("Materials sheet has no rows")
    return materials


def load_materials(sheet_csv_url: str | None = None) -> list[Material]:
    """Reads the published Google Sheet if one is configured, otherwise the bundled CSV."""
    return _parse(_read_table(sheet_csv_url))


def load_regulations() -> dict[str, list[str]]:
    return json.loads((DATA_DIR / "regulations.json").read_text(encoding="utf-8"))


def regulations_for(country: str, regulations: dict[str, list[str]]) -> dict[str, list[str]]:
    """The market's own rules (if we have them) followed by the international standards."""
    return {name: regulations[name] for name in (country, "International") if name in regulations}
