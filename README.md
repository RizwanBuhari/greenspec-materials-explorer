# GreenSpec AI

AI-assisted sustainable product design advisor (Group 4, AI Lab project).

A user describes a product and gets a sustainability score, greener alternatives from Claude, the regulations to check, and a downloadable PDF report.

## Run it locally

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501. The app works without a Claude API key, except for the AI suggestions. To turn them on, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your key. Never commit that file.

To run the tests: `pip install -r requirements-dev.txt`, then `pytest`.

## Put it online (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. At [share.streamlit.io](https://share.streamlit.io), choose **Create app** and pick this repo, branch `main`, main file `app.py`.
3. Under **Advanced settings**, paste the contents of your `secrets.toml` into **Secrets**, then deploy.

Set a monthly spend limit in the Claude Console as well. The app is public, and each suggestion is billed to the key. Repeated products reuse a saved answer, and `AI_DAILY_LIMIT` caps new requests (100 a day by default).

## Who edits what

| To change | Edit | Stream |
|---|---|---|
| Materials and scores | `data/materials.csv`, or set `GOOGLE_SHEET_CSV_URL` to read a published Google Sheet | Mech / Elec / Civil |
| Score weights and bands | `WEIGHTS` and `BANDS` in `greenspec/scoring.py` | Data Science |
| Regulations (3 to 4 points per market) | `data/regulations.json` | BBA |
| Material descriptions, trade-offs, tips | `data/material_profiles.json` | Mech / Elec / Civil |
| What Claude is asked | `SYSTEM_PROMPT` and `build_prompt` in `greenspec/ai.py` | CS / Engineering |
| Report layout | `greenspec/report.py` | BBA / CS |
| Look and feel | `assets/style.css` and `.streamlit/config.toml` | CS |

## How the score works

The sheet rates each material 0 to 10. Carbon and energy are flipped so higher is always better (`10 - rating`), then:

`score = (carbon points x 40% + recyclability x 30% + energy points x 30%) x 10`

The result is out of 100: 70 or more is Strong, 50 to 69 is Moderate, and below 50 is Low.

## Layout

```
app.py               Entry point: page setup and navigation
greenspec/views.py   The three pages
greenspec/scoring.py Sustainability score
greenspec/data.py    Loads materials and regulations
greenspec/ai.py      Claude suggestions
greenspec/report.py  PDF report
data/                Materials database and written content
tests/               Scoring, data, report and full-app tests
design/              Rayyan's Figma export and notes
prototype/           The earlier static HTML version, kept for reference
```
