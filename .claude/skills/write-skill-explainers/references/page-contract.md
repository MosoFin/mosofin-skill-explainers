# Page contract

Every explainer is a self-contained HTML file. The generated `index.html` pages are built by
`build.py`; never hand-edit them.

## Head

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Does Stripe Match Your Books?</title>
```

- `<title>` is a name of two to five words. `build.py` reads it for the card on the skill
  page and fails a page without one.
- Fonts only from Google Fonts (Archivo for text, IBM Plex Mono for labels and numbers).
  No other external stylesheets; scripts inline. The pages must work from a file:// open.

## Theme

Colours are tokens on `:root`, redefined for dark mode twice — under
`@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {…} }` and under
`:root[data-theme="dark"] {…}` — and `body` has an explicit background. Copy the block from
the reference page. Emerald is the only loud brand hue; red marks the mistake; amber marks
"held"; blue marks citations on the learn page.

## Body

- Wrap everything in `<div class="wrap">`.
- First child of the wrap is the breadcrumb:
  `<nav aria-label="Breadcrumb">` with `./` (the skill page) and `../../` (all skills).
- Sections in the order the kind's reference file gives.
- `<section id="sources">` on every public page, with an `<ol class="srcs">` of
  `<li id="srcN">` entries. Citations are `<sup class="c"><a href="#srcN">N</a></sup>`.
- SVG diagrams use `fill="var(--token)"` so they follow the theme, and carry a
  `role="img"` with an `aria-label` that tells the whole picture in words.

## Layout

- Works at phone width: 16px side gutter, no horizontal page scroll. Wide diagrams sit in a
  `.canvas` that scrolls on its own.
- Tabular numerals on money (`font-variant-numeric: tabular-nums`).
- Under 16 MB including any data URIs; in practice these pages are under 100 KB.

## Check before registering

```bash
# in the browser: no broken citation anchors, no horizontal scroll
[...document.querySelectorAll('sup.c a')].filter(a=>!document.querySelector(a.getAttribute('href'))).length
document.documentElement.scrollWidth > innerWidth
```

Open the page in both light and dark, and at phone width, before committing.
