# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS/JS, single `index.html` + `data.json` + `images/`, no build step. Hosted on GitHub Pages (public repo Max6x6x/FlowristGame).

## Users

One person: a florist student (Hungarian) preparing for the plant-identification exam of a florist course (Virágbolti Virágkötészet). Practices equally on phone (short bursts) and PC (longer sessions).

## Product Purpose

Memorize ~650 plants from the course list "Növényismereti jegyzék". At the exam ~50 plants are shown and she must write each one's Latin name and its official Hungarian botanical name (hivatalos magyar név). Success = she recognizes plants from a photo and writes both names exactly.

## Positioning

Built around her exact course list and exam format, not a generic plant app: same names, same categories, same exam shape (photo -> write Latin + official Hungarian name).

## Operating Context

- Practice: photo shown, she types Latin and/or Hungarian name, checks, sees the answer revealed. Wrongly answered plants return more often (per-device Leitner boxes).
- Exam simulation: 50 random plants, both names, feedback only at the end.
- List: browse/search all plants by category.
- Admin: she corrects names, aliases, notes, replaces photos; saves commit to GitHub via her personal token.

## Capabilities and Constraints

- Answer checking: case-insensitive; accents count (accent-only mismatch is shown as "almost", not correct). Aliases are accepted.
- The official Hungarian name is the thing to learn. Names from the course sheet are authoritative; names found automatically (Wikidata/iNaturalist) are flagged "verify" until she confirms them.
- 26 categories from the course sheet (e.g. "Vágott zöldek", "Orchideák"); a plant may be in several.
- Images come from Wikimedia Commons / iNaturalist; credit is shown only after reveal (the file name can spoil the answer).
- UI language: Hungarian.

## Evidence on Hand

- Source list: `Növénylista 2025 (1).xlsx` -> `data.json` (653 plants, 124 with Hungarian names from the course).
- No logo, brand, or visual assets exist.

## Product Principles

1. The photo is the question; nothing on screen may leak the answer before reveal.
2. Typing both names fast must feel effortless on a phone keyboard.
3. Exact spelling matters because the exam grades it; feedback shows precisely what was off.
4. Her own corrections are the source of truth over any scraped data.
