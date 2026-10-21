# Citation standard

Applies to every public page (`plain`, `learn`). `build.py --check` fails a public page that
has no `<section id="sources">` with outside links.

## Three kinds of statement, three treatments

| Statement | Treatment | On the page |
|---|---|---|
| **Rule** — what the skill does | quote it from the skill's file, name file and step | `references/method.md, Step 4` |
| **Fact** — a rate, timing, tax or accounting rule | cite an outside authority, numbered | superscript `1` linking to `#src1` |
| **Example** — a worked number | compute it from a published rate shown on the page | "$100 × 2.9% + 30¢ = $3.20" |
| **Practice** — bookkeeping convention with no published authority | say so in the sentence | "…that last rule is bookkeeping practice, not a published standard" |

Do not promote practice to fact by finding a blog that agrees. If a search turns up only
practitioner guides, the claim stays labelled as practice or as the skill's own.

## What counts as an authority

In order of preference:

1. The platform's own documentation — Stripe docs, Square Help, PayPal fee page. For a fee,
   the pricing page; for a definition (dispute, reserve, payout), the docs page that defines it.
2. The regulator or standard-setter — IRS instructions and pages, IFRS/IASB, FASB.
3. Nothing else for facts. Vendor blogs, accounting-firm articles and aggregator sites are
   not authorities; they may point you at one.

## Verifying

- Open every URL on the day you cite it; it must return 200. Record that date on the page
  ("as published when checked on 20 October 2026").
- Read enough of the page to be sure it says what you cite it for. A fetch tool summary is a
  pointer, not a verification.
- Prefer stable URLs: `docs.stripe.com/...`, `irs.gov/instructions/...`. Avoid help-centre
  search results and URLs with session or locale noise.

## Paraphrase, never copy

Vendor and regulator pages are copyrighted. State the fact in your own words and link.
At most one short quotation per page, under 15 words, in quotation marks, attributed.
The skill's own files are ours — quote them freely; that is what makes a rule checkable.

## Numbering

- One `SOURCES` list per page, numbered in order of first use.
- Each entry: a short title ("Stripe — Payouts"), the URL, and one line saying what it is
  cited for ("US accounts are paid on a 2-business-day schedule").
- Inline: `<sup class="c"><a href="#src3" aria-label="source 3">3</a></sup>`. On the learn
  page the `C(3)` helper renders this; on the plain page write it inline.
- The learn page may reuse the plain page's sources; keep the per-page numbering independent
  and complete — a reader lands on one page.

## Sources used so far (checked 2026-10-20)

Reuse these before searching; re-check each the day you cite it.

| # | Title | Cited for |
|---|---|---|
| Stripe — Pricing | https://stripe.com/pricing | 2.9% + 30¢ US card rate |
| Stripe — Payouts | https://docs.stripe.com/payouts | 2-business-day US settlement |
| Stripe — Payout reconciliation report | https://docs.stripe.com/reports/payout-reconciliation | ending = starting + activity − payouts; unsettled balance |
| Stripe API — Balance transaction | https://docs.stripe.com/api/balance_transactions/object | gross, fee and net carried separately |
| Stripe — Disputes | https://docs.stripe.com/disputes | chargeback reverses payment; amount + dispute fee debited |
| Stripe Support — Reserves FAQ | https://support.stripe.com/questions/reserves-faq | reserve held for a term, paid out minus refunds/disputes |
| Square — Our fees | https://squareup.com/us/en/payments/our-fees | in-person and online rates |
| Square — Transfer options | https://squareup.com/help/us/en/article/3807-deposit-options-with-square | next-business-day transfers |
| PayPal — Business fees | https://www.paypal.com/us/business/paypal-business-fees | Checkout rate |
| IRS — Instructions for Form 1099-K | https://www.irs.gov/instructions/i1099k | gross before fees and refunds |
| IRS — What to do with Form 1099-K | https://www.irs.gov/businesses/what-to-do-with-form-1099-k | fees and refunds handled on the return |
| IFRS 10 | https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/ | single economic entity; intercompany eliminated |
| IRS — Publication 583 | https://www.irs.gov/publications/p583 | reconcile the bank account monthly; keep slips, cheques, statements (checked 2026-10-21) |
| FDIC — Reg CC / EFAA manual | https://www.fdic.gov/consumer-compliance-examination-manual/vi-1-expedited-funds-availability-act | next-day items; other cheques by the second business day (2026-10-21; ecfr.gov blocks fetch tools) |
| Intuit — Reconcile in QuickBooks Online | https://quickbooks.intuit.com/learn-support/en-us/help-article/statement-reconciliation/reconcile-account-quickbooks-online/L3XzsllsK_US_en_US | difference must reach $0.00; don't force an adjustment (2026-10-21; blocks curl, use the fetch tool) |
| NAUPA — What is unclaimed property? | https://unclaimed.org/what-is-unclaimed-property/ | uncashed cheques; dormancy; holder turns over to the state (2026-10-21) |
| CFPB — Bulletin 2022-06 | https://www.consumerfinance.gov/compliance/supervisory-guidance/cfpb-bulletin-2022-06-unfair-returned-deposited-item-fee-assessment-practices/ | returned deposited item definition (2026-10-21) |
| GAO — Green Book GAO-25-107721 ¶10.21–10.23 | https://www.gao.gov/greenbook | segregation of duties; alternatives when impractical (2026-10-21; 403 to curl, PDF opens via fetch tool) |
| Anthropic — Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | SKILL.md under 500 lines; references one level deep (for anatomy findings) |
