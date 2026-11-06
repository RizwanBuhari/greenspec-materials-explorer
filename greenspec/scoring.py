"""Sustainability scoring.

The team's sheet rates each material from 0 to 10:
  carbon, energy:  higher means MORE impact (worse)
  recyclability:   higher means easier to recycle (better)

Carbon and energy are flipped so every component reads "higher is better", then
combined into one weighted score out of 100.
"""

from dataclasses import dataclass

# Data Science stream: tune the weights here. They must add up to 1.
WEIGHTS = {"carbon": 0.4, "recyclability": 0.3, "energy": 0.3}

BANDS = ((70, "Strong"), (50, "Moderate"), (0, "Low"))


@dataclass(frozen=True)
class Score:
    total: int
    band: str
    points: dict[str, float]  # Each component out of 10, higher is better.


def calculate_score(carbon: float, recyclability: float, energy: float, weights: dict[str, float] = WEIGHTS) -> Score:
    for value in (carbon, recyclability, energy):
        if not 0 <= value <= 10:
            raise ValueError(f"Scores must be between 0 and 10, got {value}")

    points = {"carbon": 10 - carbon, "recyclability": recyclability, "energy": 10 - energy}
    total = round(sum(points[key] * weights[key] for key in points) * 10)
    band = next(label for threshold, label in BANDS if total >= threshold)
    return Score(total=total, band=band, points=points)
