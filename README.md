# Forma · Materials explorer (GreenSpec AI, Group 4)

Web app built from Rayyan's Figma design ([design/materials-explorer.png](design/materials-explorer.png)).

## Run it
Double-click `index.html`, or serve the folder:

```
npx serve .        # or: python -m http.server 8000
```

No build step and no dependencies (Inter font loads from Google Fonts).

## Files
| File | What it is |
|---|---|
| `index.html` | Page structure: nav, explorer page, "Understanding impact" page, footer |
| `css/styles.css` | All styling. Colours are CSS variables at the top (from Figma) |
| `js/data.js` | **The materials.** Edit this to change materials, scores and text |
| `js/app.js` | Search, filters, sort, selection, routing (`#/materials/wood`, `#/impact`) |
| `js/icons.js` | Lucide icons used in the design |
| `design/` | Figma export and design notes |

## Updating the data
Each material in `js/data.js` has `name`, `family`, `group` (filter chip), `scores`
(carbon / recyclability / energy, 0–100), `description`, `tradeoff`, and 3 `tips`.
Swatches are CSS textures; add `image: "assets/materials/<id>.jpg"` to use a real photo.

Bar colour is automatic: green when favourable (carbon/energy < 50, recyclability ≥ 50), bronze otherwise.

## Still to do
- Replace demo data with the 15 materials from the team's Excel sheet
- Task 2: input form + database (see GreenSpec brief)
- Confirm the app name: "Forma" (design) vs "GreenSpec AI" (project)
- Real material photos
