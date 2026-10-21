# The learn page — worked levels, every number checkable

Reference: `site/skills/merchant-and-payment-processor-rec/learn.html`. Reuse its rendering
code (`SOURCES`, `C()`, `LEVELS`, the level renderer, the calculator) and replace the data.

## Who reads it

An owner who wants to trust the skill by checking it, and a bookkeeper who wants to know
the rule behind each step. They should be able to take any level, redo the arithmetic on a
napkin from the published rate, and get the same answer.

## Structure

1. **Header** — eyebrow with the skill name; title as a journey ("From one sale to three
   processors"); a lede saying each level is worked and cited.
2. **Legend** — three chips: Rule (quoted from the skill), Fact (cited authority, numbered),
   Example (worked on published rates). The reader learns to tell them apart.
3. **How it thinks** — the skill's rules that never bend, quoted, with file and step.
4. **Learning path** — the levels (below).
5. **Check it yourself** — a calculator: the reader enters their own month (gross, charges,
   fees paid, payouts, opening balance) and gets the closing balance, expected fees at the
   published rate, and whether revenue looks net. Inputs are theirs; nothing is sent anywhere.
6. **Sources** — `<section id="sources">`, numbered, with the check date, and a line naming
   anything on the page that is practice rather than cited.
7. **Using it** — asks first / needs / gives back / never, one line each.
8. **Footer** — which skill files the rules are quoted from; figures are examples;
   jurisdiction caveat; repository link.

## The levels

Seven is a good number; fewer if the skill is simpler. Order them so each adds one thing:

| Level | Adds | Example from the processor skill |
|---|---|---|
| 1 | one transaction, one source | $100 sale → $3.20 fee → $96.80 payout |
| 2 | a whole clean month | 100 charges, $48,000 gross, fees, net, payouts tie |
| 3 | timing across a month end | last two days paid out next month; roll-forward |
| 4 | the mistake the skill catches | revenue booked net; sales understated by the fee total |
| 5 | early warnings | fee rate drift against the published rate; payout lag growing |
| 6 | several sources | Stripe + Square + PayPal into one bank; a mispost between clearing accounts |
| 7 | several entities | one processor account, two companies; intercompany owed |

Each level object carries:

- `n`, `title`, `src` — which sources appear ("Stripe", "Stripe + Square + PayPal")
- `situation` — two sentences, plain words
- `facts[]` — each ending in `C(n)` citations
- what the skill sees — a small table or pair list of the inputs
- `rule` (and `rule2`) — quoted verbatim from the skill, with file and step
- the result — numbers, worked, with the arithmetic visible
- `cites[]` — the source numbers used, shown in the level header

## Numbers

- Use published rates from the sources section and show the multiplication.
- Keep one running example across levels (same merchant, same month) so the reader
  carries the figures forward.
- Round the way the processor rounds (cents). State totals to the cent.
- Thresholds the skill leaves loose ("≈", "near-empty") get a stated value on the page
  ("this page treats within 1% as ≈") and a note that the reader's judgement may differ.

## Quotes from the skill

Verbatim — the reader may open the file and search for the sentence. If the skill's
wording changes, the quote changes. Earlier drafts paraphrased and had to be redone.
