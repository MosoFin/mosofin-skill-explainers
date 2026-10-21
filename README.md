# MosoFin skill explainers

Human-facing pages for the skills in
[MosoFin/mosofin-finance-skills](https://github.com/MosoFin/mosofin-finance-skills). They live
here, separately, so nothing on this site is ever installed with a skill.

Every skill can have three explainers:

| Kind | File | For | What it is |
|---|---|---|---|
| `plain` | `site/skills/<skill>/plain.html` | Business owners | What the skill checks and the mistake it catches, in everyday terms; facts cited to an authority |
| `learn` | `site/skills/<skill>/learn.html` | Owners and bookkeepers | Worked levels, simple to cross-source; rules quoted from the skill, facts cited to an authority, examples worked out on published figures; a calculator |
| `anatomy` | `site/skills/<skill>/anatomy.html` | Reviewers and builders | How the skill is built, the stages it runs, and its audit |

## The tracker

[`tracker.tsv`](tracker.tsv) is the source of truth: one row per skill, with a status for each
kind — `published`, `internal` or `todo` — plus whether the skill itself is `shipped` or still a
`prototype`, how many outside sources the explainers cite, and when they were last verified.

`build.py` generates the site index and each skill's landing page from it. The explainer pages
themselves are hand-made.

**`internal` pages stay in this repository and never appear on the site** — not published, not
linked, no card on the skill's page. The index shows a kind's column only once some skill has a
published page of that kind, so an internal-only kind doesn't look like missing work. The Pages
workflow runs `build.py --stage`, which copies `site/` without them. Because the repository is
public, an internal page is still readable here in the source — use `internal` for pages meant
for reviewers, not for anything confidential.

```bash
python3 build.py                              # rebuild the index and landing pages
python3 build.py --check                      # what CI runs: tracker and site must agree
python3 build.py --stage                      # copy the public site to _site/, internal pages left out
python3 build.py --sync ../mosofin-finance-skills   # add any new skill as todo; refresh shipped status
```

`--check` fails if a tracked page is missing, a page exists that the tracker calls `todo`, a page
or folder isn't tracked, a status is invalid, or a generated page is out of date. Dependency-free
Python; no build step beyond that.

## Adding an explainer

1. Put the page at `site/skills/<skill>/<kind>.html`.
2. Set that kind to `published` (or `internal`) in `tracker.tsv`, and fill in `sources` and `verified`.
3. Run `python3 build.py`, then commit both.

## Writing a new explainer with Claude

The workflow — read the skill, collect and verify sources, write the three pages in order,
register, build, check, publish — is packaged as a Claude Code skill in
[`.claude/skills/write-skill-explainers/`](.claude/skills/write-skill-explainers/SKILL.md).
It loads automatically in a Claude Code session opened in this repository.

## Standard for `plain` and `learn` pages

`build.py --check` fails a `plain` or `learn` page that has no `id="sources"` section with outside links.

- **Rules** (`learn`) are quoted word for word from the skill, with the file and step.
- **Facts** are cited to an outside authority — the payment apps' own documentation, regulators,
  standard-setters — numbered and linked. Paraphrased, not copied.
- **Examples** are made-up figures, worked out on the published rates so a reader can check them.
- Anything with no outside authority is labelled as practice, not presented as a standard.
