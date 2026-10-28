# MosoFin Finance Workflow Explainers

This repository builds the public [MosoFin finance workflow guides](https://skills.mosofin.com/). The guides explain how MosoFin finance skills work. The executable skills live in [MosoFin/mosofin-finance-skills](https://github.com/MosoFin/mosofin-finance-skills).

**For people and agents:** [Browse the guides](https://skills.mosofin.com/) · [AI-readable index](https://skills.mosofin.com/llms.txt) · [Sitemap](https://skills.mosofin.com/sitemap.xml)

## Project scope and current content

The site provides static, source-linked explanations for accounting workflows. It does not install skills, connect to accounting data, or run reconciliations.

The tracker lists 32 shipped skills. Seven have public guide sets with a plain-language overview and a step-by-step guide. The other 25 have no explainer pages. Each published skill also has an anatomy page marked `internal`. The Pages workflow omits those pages. This GitHub repository is public. The `internal` status controls website publication, but it does not make source files private. Do not commit confidential information.

## Published guide index

| Finance workflow | Guide | Plain-language overview | Step-by-step examples |
|---|---|---|---|
| Bank reconciliation | [Guide](https://skills.mosofin.com/skills/bank-reconciliation/) | [Overview](https://skills.mosofin.com/skills/bank-reconciliation/plain.html) | [Examples](https://skills.mosofin.com/skills/bank-reconciliation/learn.html) |
| 13-week cash flow forecast | [Guide](https://skills.mosofin.com/skills/cash-flow-forecast-13-week/) | [Overview](https://skills.mosofin.com/skills/cash-flow-forecast-13-week/plain.html) | [Examples](https://skills.mosofin.com/skills/cash-flow-forecast-13-week/learn.html) |
| Credit card reconciliation | [Guide](https://skills.mosofin.com/skills/credit-card-reconciliation/) | [Overview](https://skills.mosofin.com/skills/credit-card-reconciliation/plain.html) | [Examples](https://skills.mosofin.com/skills/credit-card-reconciliation/learn.html) |
| Duplicate invoice detection | [Guide](https://skills.mosofin.com/skills/duplicate-invoice-detection/) | [Overview](https://skills.mosofin.com/skills/duplicate-invoice-detection/plain.html) | [Examples](https://skills.mosofin.com/skills/duplicate-invoice-detection/learn.html) |
| Payment processor reconciliation | [Guide](https://skills.mosofin.com/skills/merchant-and-payment-processor-rec/) | [Overview](https://skills.mosofin.com/skills/merchant-and-payment-processor-rec/plain.html) | [Examples](https://skills.mosofin.com/skills/merchant-and-payment-processor-rec/learn.html) |
| Three-way match | [Guide](https://skills.mosofin.com/skills/three-way-match/) | [Overview](https://skills.mosofin.com/skills/three-way-match/plain.html) | [Examples](https://skills.mosofin.com/skills/three-way-match/learn.html) |
| Vendor statement reconciliation | [Guide](https://skills.mosofin.com/skills/vendor-statement-reconciliation/) | [Overview](https://skills.mosofin.com/skills/vendor-statement-reconciliation/plain.html) | [Examples](https://skills.mosofin.com/skills/vendor-statement-reconciliation/learn.html) |

Public pages separate skill rules from outside finance facts. Each page links skill rules to the source. It links factual claims to outside authorities. Worked examples use labeled figures. The pages explain the skills. They do not access a reader's books.

## Repository map

- [`tracker.tsv`](tracker.tsv) is the source of truth for skill names, publication status, source counts, verification dates, summaries, and notes. Page statuses are `published`, `internal`, or `todo`.
- [`build.py`](build.py) checks tracker and page consistency, generates the homepage and skill landing pages, adds search metadata, and generates `robots.txt`, `sitemap.xml`, and `llms.txt`.
- [`site/`](site/) contains hand-authored explainer HTML, generated pages, styles, scripts, and crawler files.
- [`.claude/skills/write-skill-explainers/SKILL.md`](.claude/skills/write-skill-explainers/SKILL.md) describes the content and citation workflow for new explainers.
- [`.github/workflows/check.yml`](.github/workflows/check.yml) checks the repository on pushes and pull requests. [`.github/workflows/pages.yml`](.github/workflows/pages.yml) stages and deploys the static site to GitHub Pages.

## Build, check, and preview

Python 3 is the only build requirement. The build script uses the standard library and needs no package installation.

```sh
python3 build.py --check
python3 build.py
python3 build.py --stage _site
python3 -m http.server 8765 --directory site
```

- `--check` checks tracker statuses, required source citations, page metadata and headings, generated files, and selected prose rules.
- `build.py` updates generated pages and crawler files. Do not hand-edit generated files. Edit the source page or tracker, then rebuild.
- `--stage _site` copies the deployable site and leaves out pages marked `internal`. It includes `robots.txt`, `sitemap.xml`, and `llms.txt` at the site root.
- The local server command serves the site at `http://127.0.0.1:8765/`. Stop it with Ctrl+C.

## Update and publish a guide

1. Read the [explainer writing workflow](.claude/skills/write-skill-explainers/SKILL.md) and the source skill in `MosoFin/mosofin-finance-skills`.
2. Edit or add `site/skills/<skill>/<kind>.html`, where `<kind>` is `plain`, `learn`, or `anatomy`.
3. Update the matching row in `tracker.tsv`, including publication status, source count, and verification date.
4. Run `python3 build.py`, then `python3 build.py --check`.
5. Commit the source page, tracker, and generated files together. A push to `main` that changes `site/**`, `tracker.tsv`, or `build.py` runs the Pages deployment workflow.

The `plain` and `learn` pages are public when their tracker status is `published`. `anatomy` pages are internal by default and should only be published after an explicit review.

## Search and AI-agent discovery

- [`site/robots.txt`](site/robots.txt) allows public crawlers and points to the sitemap and AI-readable index.
- [`site/sitemap.xml`](site/sitemap.xml) lists canonical URLs for the homepage and published explainer pages.
- [`site/llms.txt`](site/llms.txt) gives AI agents a concise site description and links with page summaries. `build.py` generates it from published pages.
- After a deployment, submit `https://skills.mosofin.com/sitemap.xml` in [Google Search Console](https://search.google.com/search-console) or [Bing Webmaster Tools](https://www.bing.com/webmasters/) to monitor discovery. These files help crawlers find pages but do not guarantee indexing.

## Help and source material

For a page correction, open an [issue in this repository](https://github.com/MosoFin/mosofin-skill-explainers/issues). For a question about the finance skill's behavior, use the source skill in [MosoFin/mosofin-finance-skills](https://github.com/MosoFin/mosofin-finance-skills).
