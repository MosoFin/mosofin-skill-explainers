# Voice: write it like a person, not a model

Applies to the prose of every public page. `build.py --check` enforces the two rules a machine can
test (no em dashes in prose, no filler words); the rest is judgement.

## What the build fails on

- **Em dashes in prose.** Use a comma, a colon, brackets or a full stop. Exempt: verbatim quotes of the
  skill (they must match the skill word for word) and the lone "—" used as an empty table cell.
- **Filler words:** leverage, utilize, delve, robust, seamless, streamline, empower, foster, pivotal,
  game changer, paradigm, cutting-edge, tapestry, supercharge, and their endings.

## What to fix by hand

- **"Not X, it's Y."** Say Y. "Your policy, not the skill's" is fine when it answers a real question;
  "This is not a bug. It's a feature" is not.
- **Colon reveals and one-word verdicts.** Not "The part that matters: …", not a lone "Found." or
  "Flagged." The verdict badge already says it.
- **Mic-drop endings.** If the last line of a section is an aphorism, cut it and end on the concrete
  sentence before it.
- **Telling the reader what to feel.** Drop "the point is", "that matters", "here's the thing". Show
  the amount, the date, the consequence.
- **Claims the page can't know.** "Next month the same supplier does it again" asserts a future. Say what
  the process fails to do instead.
- **Empty adverbs** (simply, actually, truly, literally). Keep "actually" only where it contrasts with
  something ("what actually arrived" against what was ordered).
- **One sentence shape repeated.** Vary the length. A list of five bullets that all start "Never" is
  fine as a list; five paragraphs that all open the same way are not.

## What to leave alone

Plain, specific sentences. Numbers with the arithmetic beside them. A joke is fine; a flourish is not.
Quoted rules, source titles and the sources' own wording stay exactly as they are.

## The Simplified Technical English pass (every page, every kind)

This section is the page-specific part of the project rule in `.claude/skills/technical-writing-ste/`,
which covers all technical writing: skill files, docs, commit messages and pull request descriptions too.

Owners, bookkeepers and AI agents all read these pages, and some of them read English as a second
language or through a translator. Simplified Technical English (ASD-STE100) removes the two things that
cause misreading: words with more than one meaning, and sentences with more than one possible shape.
Run the pass on all three pages after the prose is written and before the arithmetic check below.

**The style skill.** [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), MIT licence,
last checked at commit `cd62d29`. It is third-party code, so it is not copied into this repository.
Install it with `git clone https://github.com/danyuchn/asd-ste100-skill ~/.claude/skills/asd-ste100`
(or `npx skills add danyuchn/asd-ste100-skill`), read its `SKILL.md` first, and run only its
`scripts/ste-lint.py`, with `python3 -I`.

**Mode.** Always its "STE-flavored" mode: the structural rules are enforced, the vocabulary rules are advice.
Active voice with the actor named. At most 25 words a sentence, 20 for a step. One idea per sentence. No
semicolons. No phrasal verbs. A verb, not a noun made from it. One word for one action, kept for the whole
page. Keep the professional term and put the plain gloss beside it.

**The commands**, from the repository root:

```bash
python3 -I .claude/skills/write-skill-explainers/scripts/ste_extract.py site/skills/<skill>/<kind>.html > /tmp/page.txt
python3 -I ~/.claude/skills/asd-ste100/scripts/ste-lint.py /tmp/page.txt     # target: 0 hard findings
python3 -I .claude/skills/write-skill-explainers/scripts/ste_verify.py site/skills/<skill>/<kind>.html
```

`ste_extract.py` pulls the visible prose, and leaves out every quoted skill rule, the diagrams and the code.
`ste_verify.py` compares the page with the last commit and fails if anything but wording changed: the HTML
structure, links, source titles, formulas, quoted rules, cite numbers, and every number, date and amount
must be identical. Script code must be identical too: only quoted strings and the prose between tags and
`${...}` in calculator templates may change. A cite marker `C(n)` may be added to a sentence you split, never
removed. It reports any change in the count of hedge words (may, usually, often, about) so you can restore one
that a rewrite removed. The extractor also pulls the prose that lives inside the learn page's script
(situations, facts, verdicts, calculator text), so the linter sees everything a reader sees.

**What the pass must never do.** Turn "may" into a fact. Drop a condition or a scope qualifier to fit the
word limit. Add a cause, a frequency or an example the page did not state. Touch a quoted rule, a source
title or a number. Make a page shorter than it needs to be: the aim is no ambiguity, not fewest words.
A finding may stay when the linter is wrong (a verdict tag such as `[auto]` counted as a word) or a passive is
the honest choice (the actor is unknown). Write the reason in the commit message.

**What the pages may claim.** They follow the structural rules of ASD-STE100. The approved-word dictionary is
not public to redistribute, and nothing here checks against it, so no page calls itself STE-compliant.
The repository's own voice rules still apply on top: no em dash in prose (STE allows it, this repository
does not), no filler words, no "not X, it's Y".

## After editing, re-check the arithmetic

Rewriting a sentence can quietly break a figure. Re-add every worked total after a pass: a verdict that
said "$150 of price and $174 for chairs" disputed $318 but summed to $324, and only a re-add caught it.
Re-run the verbatim-quote check on the learn page, then `python3 build.py --check`.
