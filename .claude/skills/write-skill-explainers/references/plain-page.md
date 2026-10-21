# The plain page — for business owners

Reference: `site/skills/merchant-and-payment-processor-rec/plain.html`. Copy its `<style>`
block and section skeleton; replace the content.

## Who reads it, and the test

A shop owner, a founder, a practice manager. No bookkeeping vocabulary assumed. After five
minutes they can say: what the skill checks, the mistake it catches, what it will ask, what
they must provide, what they get back, what it never does. If a sentence needs an accounting
term, give the plain word first and the accountant's word in passing ("the waiting room —
accountants call it a clearing account").

## Section order

Keep this order; each section answers the question the previous one raises.

1. **Header** — eyebrow label "MosoFin · <topic>, in plain words"; a one-line question as
   the title ("Does Stripe match your books?"); a lede naming the apps and the books; then
   a boxed **20-second version**: give it a month, it compares, tells you yes or no and why,
   suggests the fix, never changes anything.
2. **Where the money goes** — one worked transaction as an SVG flow (customer → app keeps
   fee → waiting room → bank). Real published rate, cited. Caption says these are example
   figures and names the accountant's term.
3. **The mistake it catches** — two side-by-side ledgers, right and wrong, same cash and
   profit, different sales and fees. Then the scaling stats (per month, per year), with the
   arithmetic shown, and why a lender or the tax form would see the difference (cited).
4. **How a run starts** — the intake questions as a numbered list, one line each on why it
   asks; then the read-back sentence it waits on. Take these from the skill's Stage 1.
5. **What you need** — two cards: connected with MosoFin (what it reads, what it still asks
   for) versus uploading (the exact files, with formats). Take from the skill's upload list.
6. **What you get back** — four short cards: the answer, what's off and why, suggested
   corrections (suggestions only), where every number came from.
7. **What it never does** — the read-only rules, as a short list. Quote the skill's wording
   where it is already plain.
8. **Words you'll hear** — five or six terms, one sentence each, cited where a vendor defines
   the term (dispute, reserve, payout). Flag practice as practice.
9. **Sources** — `<section id="sources">` with the numbered list and the check date.
10. **About this skill** — the skill's name as code, the repository link, and a link to the
    skill on GitHub (or a sentence saying it is in review, if not yet shipped).
11. **Footer** — figures are illustrative; jurisdiction caveat for tax sources.

## Writing

- Short sentences. One idea each. "It" is the skill; "you" is the owner.
- Say the number, then what it means: "$3,200 of sales and fees missing from your reports,
  every month."
- Never "simply", "just", "obviously". Never reassure; show.
- Everything the skill does must trace to a line in the skill (see SKILL.md step 1).

## Dark mode and the SVG

Colours in the SVG come from the CSS tokens (`fill="var(--ink)"`), so the diagram flips
with the theme. The wrong/red hue is reserved for the mistake; emerald is the only loud
brand hue; amber marks "held".
