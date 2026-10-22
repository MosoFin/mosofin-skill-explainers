---
name: write-skill-explainers
description: Builds the explainer pages for a MosoFin finance skill — a plain-language page for business owners, a cited learn-it-step-by-step page with worked levels from one source to cross-source, and an internal anatomy page for reviewers — then registers them in tracker.tsv and publishes them through this repository's GitHub Pages site. Use this whenever someone asks to explain a skill to business owners or bookkeepers, make a skill "easy to understand", visualise what a skill does, build a learning page, add citations or authority sources to an explainer, add a skill to the explainers site, or update an explainer after the skill changes or ships — even if they don't say "explainer".
---

# Write skill explainers

One finance skill, explained three ways, each on its own page in `site/skills/<skill>/`:

| Kind | File | For | Public? |
|---|---|---|---|
| plain | `plain.html` | business owners | yes |
| learn | `learn.html` | owners and bookkeepers | yes |
| anatomy | `anatomy.html` | reviewers and builders | no — `internal` |

The skills themselves live in `MosoFin/mosofin-finance-skills`. Explainers live here, separately,
so nothing on this site is installed with a skill. Never put an explainer inside a skill folder.

Reference implementation, read it before writing a page of the same kind:
`site/skills/merchant-and-payment-processor-rec/{plain,learn,anatomy}.html`.

## Why the pages are built this way

A business owner will only trust a skill they can check for themselves. So every page goes from
simple to complex — one sale, then a month, then several processors — and every number is one
the reader can recompute from a published rate. Nothing on a page is "because the skill says
so": a **rule** is quoted from the skill's own file, a **fact** is cited to an outside
authority, an **example** is arithmetic on published figures. The build refuses a public page
with no sources, because an uncited page is the thing we are trying not to ship.

## Workflow

### 1. Read the skill, all of it

Read `SKILL.md` and every file in `references/` of the skill in `mosofin-finance-skills`
(clone or `curl` the tarball; the install line is in `references/publish.md`). Write down,
with file and line:

- the rules that never bend (read-only, asks first, never estimates)
- the intake questions and the inputs marked Required
- what it produces, and what it never does
- each stage, and the calculation or test each stage runs
- the glossary terms a reader will meet

Do not invent behaviour the skill does not have. Two earlier drafts went wrong exactly here —
one marked a Required input optional, one described a detection step that did not exist.
Everything you say the skill does must point at a line in the skill.

### 2. Collect the sources

For every fact a page will state — a fee rate, a settlement time, a tax-form rule, an
accounting standard — find the authority and verify the URL returns 200 today. Record the
check date; it goes on the page. Read `references/citation-standard.md` first: it says what
counts as an authority, what to do when there is none (label it practice), and why quotes
from the web are paraphrased, never copied.

### 3. Write the plain page

Read `references/plain-page.md` for the section order and what each section must do. The test
for this page: a shop owner with no bookkeeping background reads it in five minutes and can
say what the skill checks, what mistake it catches, what it will ask them, and what it will
never do.

### 4. Write the learn page

Read `references/learn-page.md`. Levels run from one transaction on one source to several
sources and several entities; each level shows the situation, the facts it rests on (cited),
what the skill sees, the rule it applies (quoted), and the result worked out. Finish with a
calculator so the reader can put in their own month.

### 5. Write the anatomy page

Read `references/anatomy-page.md`. This is for whoever reviews or maintains the skill:
construction diagram, stage-by-stage run, audit findings and how each was fixed, what passed,
what is untested. It names commits and line counts, so it is `internal` by default.

### 6. Apply the page contract, then register and publish

Every page follows `references/page-contract.md` (doctype, title, theme tokens, breadcrumb,
fonts, phone width, `id="sources"`). Write the page's `<title>` and meta description as `page-contract.md` says; `build.py` generates the rest
of the search markup and the sitemap. Then follow `references/publish.md`: tracker row, build,
check, a negative test of the check, commit, push with the account that has access, watch
both workflows, confirm the live URL, switch the account back.

### 7. Keep it true

An explainer describes a version of the skill. When the skill changes, ships, or is renamed,
the pages must change with it — `references/publish.md` has the update procedure, including
`build.py --sync`, which flips `skill_status` from what is on the skills repo's `main`.
A page that says "in review" about a shipped skill is wrong, not merely stale.

## Anti-patterns

- A fact with no citation, or a citation that was not opened and checked today.
- Copying sentences from a vendor or regulator page. Paraphrase, and link.
- Numbers that cannot be recomputed from a published rate on the page.
- Describing a step the skill does not have, or softening a Required input.
- Explainer HTML inside the skill's own folder, or in the skills repository at all.
- Editing `site/index.html` or a skill's `index.html` by hand — `build.py` generates them.
- Editing the generated `seo` block, or a page's title past 65 characters or description past 160.
- Marking a page `published` to make a gap disappear. `todo` is honest; `internal` hides it.
- Three pages written at once from memory. Write them in order; each one checks the last.
