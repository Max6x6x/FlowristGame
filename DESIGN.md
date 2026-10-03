---
name: Növényismeret
description: A warm pocket coach for one florist student's plant-identification exam.
colors:
  ground: "#f3efe8"
  card: "#ffffff"
  sunk: "#e8e2d7"
  ink: "#1d1b18"
  ink-2: "#5b564e"
  ink-3: "#6f695f"
  go: "#267a41"
  go-ink: "#ffffff"
  go-soft: "#e3f3e8"
  go-text: "#23703c"
  almost: "#9a5b00"
  almost-soft: "#fbeed4"
  bad: "#b3261e"
  bad-soft: "#fbe3e0"
typography:
  display:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "26px"
    fontWeight: 800
    lineHeight: 1.15
  headline:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "21px"
    fontWeight: 700
  title:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 800
  input:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 700
  body:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 500
    lineHeight: 1.45
  hint:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 500
    letterSpacing: "0.06em"
    fontFeature: "tnum"
  label:
    fontFamily: "Nunito, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 700
rounded:
  inner: "10px"
  s: "14px"
  button: "16px"
  m: "20px"
  l: "28px"
  round: "50%"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  xxl: "32px"
components:
  button-go:
    backgroundColor: "{colors.go}"
    textColor: "{colors.go-ink}"
    rounded: "{rounded.button}"
    height: "52px"
    padding: "0 20px"
  button-soft:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.button}"
    height: "52px"
    padding: "0 20px"
  button-soft-disabled:
    backgroundColor: "{colors.sunk}"
    textColor: "{colors.ink-3}"
  input-answer:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    typography: "{typography.input}"
    rounded: "{rounded.s}"
    height: "52px"
    padding: "0 14px"
  input-answer-ok:
    backgroundColor: "{colors.go-soft}"
  input-answer-almost:
    backgroundColor: "{colors.almost-soft}"
  input-answer-bad:
    backgroundColor: "{colors.bad-soft}"
  segmented:
    backgroundColor: "{colors.sunk}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.s}"
    padding: "4px"
  segmented-selected:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.inner}"
    height: "38px"
  panel:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.l}"
    padding: "16px"
  photo-card:
    backgroundColor: "{colors.sunk}"
    rounded: "{rounded.l}"
  solution:
    backgroundColor: "{colors.ground}"
    rounded: "{rounded.m}"
    padding: "16px 18px"
  tile:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.m}"
  chip:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.s}"
    padding: "4px 12px"
  tab-active-desktop:
    backgroundColor: "{colors.go}"
    textColor: "{colors.go-ink}"
---

# Design System: Növényismeret

## Overview

**Creative North Star: "The Pocket Coach"**

A friendly study companion for one exam, not a quiz form. The screen is a warm, tinted ground carrying soft white cards with generous radii; the photo card is the question and gets the biggest share of the viewport. Everything reachable by thumb sits low on the phone, and presses answer with a small spring.

Color is mostly quiet: warm paper, white, and warm-grey ink. One saturated green carries every pressable primary action and the "correct" state. Amber means "almost" (an accent-only miss), red means wrong. Nunito, a rounded humanist sans at heavy weights, keeps the voice friendly and readable at arm's length.

The system refuses the grey form-with-a-header quiz look: no hairline-boxed forms, no flat toolbars, no cold neutrals.

**Key Characteristics:**
- Warm tinted ground (never pure white) under white cards.
- Generous, nested radii: 28px cards, 20px inner surfaces, 14px controls.
- One green for action and correctness; amber and red only as answer feedback.
- Nunito at 700-800 for anything interactive or answering.
- Spring press feedback on buttons; gentle rise-in for the revealed answer.
- Light and dark modes share every token name; dark mode swaps values only.

## Colors

Warm paper neutrals with a single action green and two feedback hues.

### Primary
- **Meadow Green** (`go`): fill for the primary button (Mutasd!, Következő, Mentés, Új kör), the active desktop tab, the focus ring and focused input border, the caret, checkbox accent, and the round-progress fill.
- **Deep Meadow Text** (`go-text`): green as text: correct verdict, active phone tab label, round counter, hint-count badge text.
- **Sprout Wash** (`go-soft`): background of a correct answer field, the hint badge, and text selection.

### Secondary
- **Burnt Amber** (`almost`): "almost" verdict text, the highlighted wrong-letter mark (amber fill, card-colored letter), and the "verify" flag on unconfirmed Hungarian names.
- **Apricot Wash** (`almost-soft`): background of an "almost" answer field.

### Tertiary
- **Brick Red** (`bad`): wrong verdict text only.
- **Blush Wash** (`bad-soft`): background of a wrong answer field.

### Neutral
- **Warm Paper** (`ground`): page background, the revealed-solution block, list rows. Also the browser theme color.
- **Card White** (`card`): cards, panels, inputs, soft buttons, tab bar, chips.
- **Oat** (`sunk`): segmented-control track, input borders at rest, photo/thumbnail placeholders, progress track, disabled soft button, tab bar top rule.
- **Bark Ink** (`ink`): primary text.
- **Driftwood** (`ink-2`): field labels, hints, meta lines, counts, inactive segment text.
- **Pebble** (`ink-3`): inactive phone tab labels, disabled button text.

Dark mode (prefers-color-scheme) keeps the same roles: ground `#1b1916`, card `#262320`, sunk `#33302b`, ink `#f1ece4` / `#c3bbae` / `#a59d90`, go `#4fb06d` with dark ink `#0f1a12`, go-soft `#1f3a27`, go-text `#7fd197`, almost `#f0b44c` / `#3d3020`, bad `#ff8a80` / `#43231f`. The zoom viewer is always near-black (`#0d0c0b`) in both modes.

### Named Rules
**The One Green Rule.** Saturated green marks what can be pressed or what is right (plus the focus ring and round progress). Never use it for decoration, headings, or illustration.

**The Feedback-Only Rule.** Amber and red appear only as answer feedback (verdicts, field washes, the wrong-letter mark, the verify flag). They are never button or chrome colors.

**The Same-Names Rule.** Dark mode overrides values on `:root`; components never branch on theme.

## Typography

**Display Font:** Nunito (with system-ui, sans-serif)
**Body Font:** Nunito
**Label/Mono Font:** Nunito; numbers use tabular figures where they count.

**Character:** One rounded humanist family carried entirely by weight (500 body, 700 labels and fields, 800 actions and answers). Friendly, never fussy.

### Hierarchy
- **Display** (800 italic, 26px / 34px desktop, 1.15): the revealed Latin name. Wraps anywhere rather than overflowing.
- **Headline** (700, 21px / 24px desktop): the revealed official Hungarian name, directly under the Latin. The round summary heading uses 26px 800.
- **Title** (800, 20px): the app name in the header.
- **Input** (700, 18px): typed answers; Latin fields are italic.
- **Body** (500, 16px, 1.45): running text. Buttons are 16px 800.
- **Hint** (500, 15px, 0.06em tracking, tabular): progressive letter hints under fields; words never break internally.
- **Label** (700, 13px, Driftwood): field labels, meta lines, solution keys. Tab labels are 12px 700 on phone, 15px on desktop.

### Named Rules
**The Latin Is Italic Rule.** Every Latin binomial (answer field, revealed name, list tile, admin row) is set italic, matching botanical convention. Hungarian names stay upright.

**The Weight Carries Rank Rule.** Hierarchy comes from weight and size inside Nunito; no second typeface.

## Layout

Phone first, single column: header (app name, today chip), segmented mode control, two category/round selects, photo card at about 42% of the viewport height (34% when both names are asked), then the answer panel. The primary tab bar is fixed to the bottom (64px plus safe area). Below 900px the panel's action row is sticky above the tab bar; while an answer field has focus the tab bar hides and the action row drops to the bottom edge, so the keyboard never covers Mutasd!.

At 900px and up the page becomes two-sided: tabs move into the header as pills, the photo takes the left 7fr column at full viewport height and stays sticky, and controls plus the answer panel stack in the right 5fr column (min 360px), 24px gutter. Content caps at 1320px.

Spacing runs on a 4px base: 4 / 8 / 12 / 16 / 24 / 32. Page gutters are 16px on phone and 32px on desktop; panel padding is 16px on phone and 24px on desktop. The list is an auto-fill grid of 156px-minimum tiles with 10px gaps.

## Elevation & Depth

Soft, ambient lift on a tonal ground. Cards are white on warm paper and carry one diffuse two-layer shadow; recessed areas (segment track, placeholders, progress track) use the darker Oat tone instead of shadow. No hard or offset shadows.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 1px 2px rgba(0,0,0,.07), 0 6px 18px rgba(0,0,0,.05)`; dark: `0 1px 2px rgba(0,0,0,.4), 0 6px 18px rgba(0,0,0,.25)`): panels, tiles, soft buttons, selects, search field, chip, the photo zoom button.
- **Selected segment** (`box-shadow: 0 1px 2px rgba(0,0,0,.12)`): the active option lifting out of the segment track.

### Named Rules
**The Paper-And-Card Rule.** Depth is white card on warm paper plus the single card-lift shadow. Sunk surfaces are tone, not inset shadows.

## Shapes

Generously rounded, nested from outside in: outer cards and the photo at 28px, inner surfaces (solution block, list tiles) at 20px, controls (inputs, selects, segment track, chip, list rows) at 14px, buttons at 16px, and items nested inside a 14px track at 10px. Icon buttons (zoom, viewer close) are full circles at 44-48px. Input borders are 2px Oat at rest; there are no hairline outlines elsewhere except the 1px top rule of the phone tab bar.

## Components

### Buttons
Chunky and thumb-sized, with a spring.
- **Shape:** gently rounded (16px), 52px tall, 20px side padding, 16px 800.
- **Primary (go):** Meadow Green fill, white text; stretches to fill the action row.
- **Soft:** Card White with card lift and ink text; used for Súgó and Bezár. Disabled drops to Oat with Pebble text and no shadow.
- **Press:** scale to 0.96 on `:active` with `cubic-bezier(.3,1.6,.5,1)` over 150ms (the spring). Focus is a 3px green outline at 2px offset, app-wide.
- **Hint badge:** a small Sprout Wash pill (11px radius) inside Súgó counts hints used.

### Segmented Control
- **Style:** Oat track, 14px radius, 4px padding; options 38px tall, 700 14px Driftwood.
- **State:** the pressed option becomes Card White with Bark Ink and the selected-segment shadow, radius 10px; background and color ease over 200ms.

### Cards / Containers
- **Panel:** Card White, 28px, card lift, 16px padding (24px desktop), 6px internal gap.
- **Photo card:** 28px radius, Oat placeholder, cover-cropped image, a circular zoom button top-right and a progress chip top-left.
- **Solution block:** Warm Paper inside the white panel, 20px radius, 16px 18px padding, rises in (8px, 350ms, `cubic-bezier(.2,.8,.2,1)`).

### Inputs / Fields
- **Answer field:** 52px, 14px radius, 2px Oat border, Card White, 18px 700. Label above in 13px 700 Driftwood; hint line below.
- **Focus:** border turns Meadow Green (200ms).
- **Result states:** correct, almost and wrong fill the field and border with Sprout, Apricot or Blush wash; a verdict line in 14px 800 follows in the matching text color, with off letters marked in amber.
- **Search and selects:** borderless Card White with card lift, 14px radius, 40-44px tall.

### Navigation
- **Phone:** fixed bottom bar, Card White with a 1px Oat top rule; three icon-over-label buttons (24px stroke icons, 12px 700). Inactive Pebble, active Deep Meadow Text.
- **Desktop:** the same buttons sit inline in the header as 12px-radius pills with 18px icons and 15px labels; active is a Meadow Green pill with white text, inactive is Driftwood with no fill.
- **Icons:** inline 2px-stroke SVGs with round caps.

### Today Chip
A Card White pill (14px radius, card lift, 14px 700 tabular figures) in the header showing today's correct / total.

### Zoom Viewer
Full-screen near-black dialog; image contained, tap zooms to 2.6x over 250ms. A white 48px circular close button top-right and a 14px translucent-white tip at the bottom.

## Do's and Don'ts

### Do:
- **Do** keep the page on Warm Paper (`#f3efe8`) and put content on white cards with the single card-lift shadow.
- **Do** reserve Meadow Green (`#267a41`) for primary actions, the active tab, focus, correct state and round progress.
- **Do** set every Latin name in italic, and reveal names only after the answer is checked.
- **Do** keep primary actions 52px tall with the 0.96 spring press, and keep the action row within thumb reach on phone.
- **Do** nest radii from 28px (cards) to 20px (inner surfaces) to 14px (controls).
- **Do** define new colors as `:root` custom properties with a dark-mode value under the same name.

### Don't:
- **Don't** build grey form-with-a-header quiz screens: no cold neutral grounds, no hairline-boxed forms.
- **Don't** use amber or red for anything except answer feedback.
- **Don't** add hard or offset shadows; depth is the soft card lift plus tone.
- **Don't** introduce a second typeface; rank comes from Nunito's weights.
- **Don't** use square or barely-rounded corners on cards, controls or buttons.
