# Figma design notes: "Forma · Materials explorer" (by Rayyan)

Source: figma.com/design/pw897OYOc19NFNIJ5d6JM9 (CSS copied from Figma, plus a screenshot)

## Colour tokens
| Token | Hex | Used for |
|---|---|---|
| bg | #F4F3EE | page background, inactive filter chips, table header |
| surface | #FEFEFB | nav bar, cards, table rows |
| border | #DEDFD6 | all 1px borders |
| primary | #244D3E | brand mark, active nav underline, active chip, "good" score bars |
| primary-soft | #E8EDE2 | status badge, profile avatar |
| sprout | #D7E5BB | logo icon stroke |
| text | #24392F | headings, values |
| muted | #73796F | labels, secondary text |
| bronze | #A47843 | "worse" score bars, info icon |
| notice-bg | #F1E9DB | demo-data disclaimer banner |
| track | #E5E7DF | score bar track |

Font: Inter (400 / 500 / 600). Icons: Lucide (sprout, search, info, chevron-right/down, arrow-down-wide-narrow).

## Layout (desktop 1536px frame)
- Page padding 40px left/right
- **Nav** 76px high: brand (leaf mark 32×36, radius `16px 4px`, name 27px), 2 nav tabs (active = 3px bottom border), status badge plus initials avatar
- **Intro**: eyebrow 10px, title 37px/45px, description 14px, catalog summary on the right
- **Disclaimer banner**: "Illustrative demo data. Scores are fictional examples…" (radius 6, padding 12×15)
- **Workspace**: 2 columns, gap 24
  - **Catalog card** (flex 1, ~950px, radius 12): title "All materials" + count, search (42px high) + sort dropdown (154px), family filter chips (All materials / Metals / Minerals / …), scale note, table
    - Table columns: Material (swatch 32px radius 5 + name 13px/500) · Family (11px) · 3 × score (value 13px + 68×4 bar) · chevron
    - Row height 49px, header 36px
  - **Material profile panel** (right, ~520px): hero image, "Selected" badge, description, 3 scores (Carbon / Recyclability / Energy, out of 100, with "lower/higher is better"), "Read the trade-offs" callout, "Before you choose" checklist, "Compare the same function" note
- **Footer band** (dark green): "Beyond the score: A material is only part of the story" + 3 columns (How it is made / How far it travels / What happens next)

## Scores in the design
- Carbon: lower is better
- Recyclability: higher is better
- Energy: lower is better
- Bar colour: green (#244D3E) = favourable, bronze (#A47843) = unfavourable
- 16 placeholder materials: Steel, Glass, Aluminium, Concrete, Plastic, Paper, Cardboard, Leather, Copper, Brick, Rubber, Cotton fabric, Polyester fabric, PVC, Wood, Clay
  - **These will be replaced by the 15 materials and real scores from the team's Excel sheet.**

## Copy (from full export: materials-explorer.png)
- Brand: "forma" + "MATERIAL INTELLIGENCE"; nav: **Materials explorer** (active) · **Understanding impact** (second page, not designed yet); badge "Demo workspace"; avatar "JD"
- Eyebrow "THE MATERIAL LIBRARY"; title "Better choices start with materials."; sub "Explore the trade-offs. Select a material to understand its environmental profile."; right "16 materials · 3 impact dimensions"
- Filters: All materials · Metals · Minerals · Polymers · Fibres & textiles · Other
- Sort dropdown: "Default order"; card corner: "Library view"; search placeholder "Search materials or families…" (⌘K)
- Scale note: "Demo scale 0–100 · Carbon & energy: lower is better · Recyclability: higher is better"
- Table footer: "Showing all 16 materials" / "✓ Wood selected"; selected row = light green bg + left border + arrow icon
- Profile panel: "MATERIAL PROFILE" + ⋯ menu; hero photo with family chip ("Plant-based material"); name 40px + "Selected" pill; description; "Environmental profile" / "ILLUSTRATIVE SCORES"; each score: icon (cloud / recycle / zap), name, big value "/ 100", bar, sub-label ("Relative greenhouse-gas impact", "Potential for material recovery", "Relative production energy demand"), direction hint
- Per-material text needed: description, "Read the trade-offs" paragraph, 3 "Before you choose" tips
- Footer band copy: "BEYOND THE SCORE / A material is only part of the story." · How it is made: "Recycled content, production methods and the energy mix matter." · How far it travels: "Weight, transport distance and local sourcing affect the footprint." · What happens next: "Longer use, repair and a realistic recovery route can change the outcome."
- Page footer: "Forma / Material intelligence, with context." · "Exploration, not certification. No material is sustainable in every application."

## Open issues / to confirm with team
- Design brand name is **"Forma"** but the project is **GreenSpec AI**. Which one do we use?
- Swatch images in Figma are AI image prompts, not real files. We need real photos or textures.
- The design doesn't show the **input form** (Task 2) yet. Check the brief for the required fields.
