---
name: process-finance-skill
description: "Takes one MosoFin finance skill through the whole process, in order. It audits the skill and fixes the findings. It splits the skill into the card format and proves that no line was lost. It writes the three explainer pages with cited sources, applies Simplified Technical English to every new text, then registers, checks and publishes. Use this when someone asks to process, rewrite, convert, audit or explain the next finance skill, or to continue with the next skills. Use it also to repeat for one skill the work done for bank, three-way match, credit card or vendor statement reconciliation. It works in two repositories: the skill in MosoFin/mosofin-finance-skills, its pages in this one."
---

# Process a finance skill, end to end

One finance skill goes through twelve steps. The skill itself lives in `MosoFin/mosofin-finance-skills`.
Its explainer pages live in this repository. The steps run in order, and each step has a test. Do not
start a step before the step before it passes.

This skill joins three things that already exist. Read them when a step points to them:

- `.claude/skills/write-skill-explainers/`: how to write the three pages, cite sources and publish.
- `.claude/skills/technical-writing-ste/`: the Simplified Technical English (STE) rule for every new text.
- The skills repository's `CONTRIBUTING.md`, `.github/validate-skill.sh` and `.github/sync-shared.sh`.

Four skills went through this process first: bank-reconciliation, three-way-match,
credit-card-reconciliation and vendor-statement-reconciliation. Their commits and pages are the
reference. When this file and a reference disagree, follow this file and say so.

## The twelve steps

### 1. Choose the skill

Take the next skill in the same family as the last one, from `tracker.tsv` and the skills repository's
`deploy-queue.tsv`. A skill whose pages are all `todo` and whose `SKILL.md` has no `references/`
folder is a candidate. Say which skill you chose, and why, before you start.

### 2. Audit it

```bash
python3 -I .claude/skills/process-finance-skill/scripts/audit_skill.py <skills repo> <skill> origin/main
```

The script finds candidates. It reports these items:

- the size, and the description length
- references to skills that are not in the library
- sandbox-only paths, tool names and verdict counts
- the section map that the split will follow

Then read the whole
`SKILL.md` yourself. Look for what a script cannot see:

- A step marked `[auto]` that needs data no ledger holds. Example: "vendors never reconciled".
- A claim that the skill reads something that no connection exposes.
- A figure stated as a standard with no source. It is practice, and the skill must say so.

Write each finding down with its line number and the published guidance behind it.

### 3. Fix the findings, one commit each

Work on a new branch from `origin/main`, named `claude/<skill>-card-format`. Fix each finding in its own
commit, before the split. Keep each fix as small as the finding. For a reference to a skill that is not
in the library, make the sentence stand on its own. Fix a wrong skill name. Keep only library skills
in the Related skills table, and add one line that says the others will be linked when they ship.

### 4. Split into the card format

Write a card `SKILL.md` of about 120 to 145 lines. It holds these parts:

- what the skill does, and five or six rules that never bend
- a six-question intake, an upload checklist and a read-back
- six stages that each point at one reference file

Move the original text, unchanged, into `references/`. Use the reference
skill whose layout matches: three-way-match or vendor-statement-reconciliation for the "seed" layout,
bank-reconciliation or credit-card-reconciliation for the "Part B" layout.

- Copy `mosofin-protocol.md` from a reference skill. The sync script fills its shared blocks.
- Give every reference file over 100 lines a contents list.
- Keep the description under 1,024 characters.
- Write all new card text in STE. Do not apply STE to the moved text: it must stay byte-identical.
- Check every statement on the card against the reference line it summarises. Remove anything the
  skill does not say.

### 5. Prove the split

```bash
python3 -I .claude/skills/process-finance-skill/scripts/split_proof.py <original SKILL.md> <skill folder>
bash .github/sync-shared.sh && bash .github/sync-shared.sh --check
bash .github/validate-skill.sh skills
```

The proof must report all content lines kept except two: the description and the onboarding link. It
must report zero sections broken and zero broken links. The validator must report zero failures.

### 6. Commit, then push or make a patch

Write each commit message in STE and lint it. State the counts the proof gave. Push the branch. If
this session cannot push to the skills repository, run `git format-patch` and give the person the path.
Never push to `main` without permission.

### 7. Find the sources

Read `write-skill-explainers/references/citation-standard.md`. Find an outside authority for every fact
a page will state, on the publisher's own site. Record where in the source the fact sits, and only
record a location that a result showed. If you cannot open the page itself, say so on the source with
`via: "from search results, page not opened"`. Check old sources too: a source can be withdrawn.

### 8. Write a content spec, then the pages

Write a spec before any page. It lists the sources with facts, locations and dates, the quotes with
their file and section, and the worked example with every figure. Run a script that checks each quote
in its file and section, and re-add every figure. Then write `plain.html`, `learn.html` and
`anatomy.html` from the spec, as `write-skill-explainers` says. Copy the newest pages of the same kind
as templates.

### 9. Place the citations

A sentence that states a figure from a source carries its marker. A run of sentences from one source
carries one marker, at the end. The skill's own rules and your inferences carry none. Give every source
`data-checked` (or `checked:`), and `data-at`, `data-via` and `data-status` where they apply.
`build.py` adds the citation block. Never edit that block by hand.

### 10. Apply STE

Run the STE pass from `technical-writing-ste` on all three pages. The target is zero hard findings.
Any finding that stays needs a reason in the commit message.

### 11. Check everything

```bash
python3 build.py && python3 build.py --check
```

Also run the quote check on the learn page, the linter, and a Playwright render at 1100 and 390 pixels
wide. The render must show no console errors and no page overflow, and the calculator preset must tie.
Break one thing on purpose, see `--check` fail, and restore it.

### 12. Register, publish, keep it true

Add the tracker row. Set a page to `published` only when you opened every source it cites. Otherwise
set it to `internal`, and name in the notes the sources you still have to open. Commit the pages and the tracker row
together. When the skill's rewrite reaches `main`, replace the local commit hashes on the anatomy page
with the merged ones. Publish the explainer commits only after their skill ships.

## Rules that never bend

- **One skill at a time.** Finish the twelve steps, or say exactly where you stopped.
- **The moved text stays byte-identical.** The proof shows it.
- **Every statement points at a line in the skill.** Every fact points at a source a person can open.
- **Never present a search-only check as an opened page**, and never present a branch as `main`.
- **Never edit generated blocks** (`seo`, `cite`, the shared blocks in `mosofin-protocol.md`).
- **Every new text follows STE**, and so does every commit message.

## When you stop

Report these items:

1. the branch and the commits, and the proof counts
2. the findings fixed and the findings still open
3. the page statuses
4. what the person must do next: push, open sources, or merge in order
