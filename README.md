# MosoFin Finance Skill Explainers

[Read the finance guides](https://skills.mosofin.com/)

The public site features guides to bank reconciliation, credit card reconciliation, payment processor reconciliation, and three-way matching. This repository also tracks guides in progress for cash flow forecasting, duplicate invoice detection, and vendor statement reconciliation.

The published guides explain what each skill checks, how its steps work, and how reviewers can inspect its design. The site serves business owners, bookkeepers, and finance automation reviewers.

## Explore the guides

Each skill can have three pages:

| Page | What you can learn |
|---|---|
| Plain-language guide | What the skill checks and which errors it can find. |
| Step-by-step guide | How the rules work, with cited facts, worked examples, and a calculator. |
| Skill anatomy | How the skill is built, which stages it runs, and how reviewers can audit it. |

The guides link to outside authorities for finance facts. They identify skill rules and label examples so readers can review the source of each claim.

## About this project

The explainers describe skills from [MosoFin finance skills](https://github.com/MosoFin/mosofin-finance-skills). This repository stores the human-facing guides separately from those skills. Nothing here is installed as a finance skill.

The public site is built with static HTML and hosted by GitHub Pages. GitHub Actions checks the site and publishes it from `main`. The deployment stages only pages marked `published` in `tracker.tsv`. Pages marked `internal` stay out of the deployed site. This public repository still contains its source files, so do not put confidential material in it.

## Build and check the site

Python 3 is the only build requirement. The build script has no external dependencies.

```bash
python3 build.py --check
python3 build.py
python3 build.py --stage
```

`--check` verifies that the tracker and generated pages agree. `build.py` updates the index and skill landing pages. `--stage` creates `_site/` with published pages only.

## Add or update a guide

1. Add the page at `site/skills/<skill>/<kind>.html`.
2. Set its status in `tracker.tsv` to `published`, `internal`, or `todo`.
3. Add source counts and the last verified date to the tracker.
4. Run `python3 build.py` and `python3 build.py --check`.
5. Commit the page, tracker, and generated files together.

The tracker is the source of truth for each skill and page status. Read the [writing workflow](.claude/skills/write-skill-explainers/SKILL.md) before you create an explainer.

## Search and page metadata

Each published page has a unique title and description. The build script adds canonical URLs, social sharing metadata, structured data, a sitemap, and an `llms.txt` overview for AI agents. `robots.txt` allows public crawlers and points to the sitemap. The sitemap and `llms.txt` include published pages only; the Pages staging step copies both files to the site root.

After deployment, submit `https://skills.mosofin.com/sitemap.xml` to [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters/). Search engines can use the sitemap for page discovery; AI agents can start with `https://skills.mosofin.com/llms.txt`.

## Writing standard

Project documentation and public guides follow the structural rules of ASD Simplified Technical English. The checks favor short, active sentences and clear terms. They do not check the approved-word dictionary, so this project does not claim full STE compliance.
