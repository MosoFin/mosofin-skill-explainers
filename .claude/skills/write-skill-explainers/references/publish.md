# Register, build, publish, keep current

## Getting the skill to read

Without cloning the whole skills repository:

```bash
T=$(mktemp -d)
curl -sL https://github.com/MosoFin/mosofin-finance-skills/archive/refs/heads/main.tar.gz \
  | tar -xz -C "$T" --strip-components=2 mosofin-finance-skills-main/skills/<skill>
```

If the skill is on a branch and not on `main`, read it from the local checkout and treat
`skill_status` as `prototype`.

## The tracker

`tracker.tsv` is the source of truth. One row per skill:

```
skill  genre  skill_status  title  plain  learn  anatomy  sources  verified  summary  notes
```

- `skill_status`: `shipped` (on the skills repo's `main`) or `prototype`. Set it with
  `python3 build.py --sync ../mosofin-finance-skills mosofin/main`, not by hand.
- each kind: `published` | `internal` | `todo`. The file must exist for the first two and
  must not exist for `todo`.
- `sources`: how many outside sources the public pages cite. `verified`: the date you
  opened them all.
- `summary`: one sentence for the skill page's lede. `notes`: one line for its footer.

Adding a skill that is not tracked yet: `--sync` adds every skill on the repo as `todo`.

## Build and check

```bash
python3 build.py            # regenerates site/index.html and each site/skills/<skill>/index.html
python3 build.py --check    # tracker ↔ files ↔ titles ↔ sources; non-zero on any drift
```

The check fails on: a kind marked published/internal with no file; a file with the tracker
saying todo; a page without `<title>`; a public page without `id="sources"` and outside
links; a stray file under `site/skills/`; an untracked skill folder; an unknown kind.

Titles, descriptions and the sitemap are part of the check (see `page-contract.md`, "Search"). The
sitemap's `lastmod` is the row's `verified` date, so reopen and re-date sources whenever a page's facts
change — it is the honest "last reviewed" date, not a file timestamp.

**Prove the check still bites.** Before committing, break one thing on purpose — rename
`id="sources"`, or delete the title — run `--check`, see it fail, restore. A check that was
never seen failing is not known to work.

## Commit and push

- Commit the page(s), `tracker.tsv`, and the generated `index.html` files together.
- `Travisliang001` has no push access to this repository. Switch to the owner account, push,
  switch back in the same command so the shell never stays on the owner account:

```bash
gh auth switch -u mosofin && git push origin main; gh auth switch -u Travisliang001
```

- Two workflows run: `check.yml` (runs `--check`) and `pages.yml` (check, then
  `--stage _site`, which copies the site without internal pages, then deploys). Watch both:

```bash
gh run list -R MosoFin/mosofin-skill-explainers -L2
gh run watch <id> -R MosoFin/mosofin-skill-explainers --exit-status
```

- Then confirm the live URL serves the new content (`curl -s <url> | grep -c 'id="src'`),
  and that an internal page returns 404, and that `/sitemap.xml` lists the new URLs. Crawlers only read
`robots.txt` at a domain's root, which a GitHub Pages project site cannot serve, so the sitemap is
submitted in Google Search Console and Bing Webmaster Tools instead of being declared there. Pages can take a minute after the deploy job ends.

Live site: https://mosofin.github.io/mosofin-skill-explainers/

## Keeping explainers current

| Change in the skills repo | Do here |
|---|---|
| skill ships to `main` | `--sync`; change "in review" wording on all three pages; add the GitHub link; anatomy eyebrow/footer/Passed |
| a rule's wording changes | update every verbatim quote of it on the learn page |
| a Required input or intake question changes | plain page steps 4–5, learn page "Using it" |
| reference files change size | anatomy counts and bars |
| a cited page changes its figure | recompute the examples that used it; re-verify; update `verified` |
| skill renamed | rename `site/skills/<old>` → `<new>`, the tracker row, and rerun `--sync` |

Re-open every cited URL whenever you touch a page's sources, and set `verified` to that day.
