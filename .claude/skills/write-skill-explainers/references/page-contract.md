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

- `<title>` is the search title, 25–65 characters, in the form `<Topic> <format> | MosoFin` — for
  example "Bank Reconciliation Explained in Plain English | MosoFin". Lead with the words a person
  would type. It differs from the `<h1>`, which stays in the human voice ("Does your bank match your
  books?"); the skill page's cards use the `<h1>`.
- Directly under it, `<meta name="description" content="…">`: 70–160 characters, unique on the site,
  says what the page shows, and claims nothing the page doesn't. `build.py --check` fails a published
  page without one.
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

## Search

Everything else search engines read is **generated** by `build.py` between `<!-- seo:start -->` and
`<!-- seo:end -->`: canonical URL, robots, Open Graph, Twitter card, favicon, theme colour and JSON-LD
(an `Article` and a `BreadcrumbList`, `dateModified` taken from the tracker's `verified` date). Never
edit that block by hand; change the title, description or tracker row and run `python3 build.py`.

`--check` also fails a published page that has more than one `<h1>`, a heading that skips a level
(h2 straight to h4), a title or description shared with another page, a canonical that is not the
page's own URL, or JSON-LD that does not parse. `site/sitemap.xml` is generated from the tracker and
lists published pages only, so internal pages never appear.

Limits to know: pages have no social image (cards show text only), and the learn pages build their
levels and source lists in JavaScript, which Google renders but simpler crawlers do not.

## Check before registering

```bash
# in the browser: no broken citation anchors, no horizontal scroll
[...document.querySelectorAll('sup.c a')].filter(a=>!document.querySelector(a.getAttribute('href'))).length
document.documentElement.scrollWidth > innerWidth
```

Open the page in both light and dark, and at phone width, before committing.
