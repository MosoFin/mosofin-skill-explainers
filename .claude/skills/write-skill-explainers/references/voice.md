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

## After editing, re-check the arithmetic

Rewriting a sentence can quietly break a figure. Re-add every worked total after a pass: a verdict that
said "$150 of price and $174 for chairs" disputed $318 but summed to $324, and only a re-add caught it.
Re-run the verbatim-quote check on the learn page, then `python3 build.py --check`.
