# Chat replay audit: problems in the skills themselves

Four independent auditors compared each of the 32 chat replays with its skill's own `SKILL.md` and
`references/` in MosoFin/mosofin-finance-skills (clone at commit b200ad9). All 32 chats had at least one
mismatch, and the chats are now fixed. While they worked, the auditors also found the problems below in
the skills' own files. Only a skill owner can fix these. The chats follow `SKILL.md` where two files disagree.

## Problems that affect many skills

1. **"Read nothing before the yes" conflicts with the MosoFin path (most skills).** Each `SKILL.md` says
   the skill reads nothing until the user confirms the read-back. On the MosoFin path, the same file asks
   the skill to read before that yes: the company profile (Gate 3), the chart of accounts, clearing-account
   activity or spend history. Examples: merchant `SKILL.md:20` and `:53`, bank `:22` and `:58`, credit card
   `:24` and `:63`, payroll journal entries `:62` and `:74`, AP accrual cutoff `:70`, month-end close `:77`.
2. **One read-back or two? (all skills).** `SKILL.md` asks for one read-back of the workspace and the company
   file together (Gates 0–1). `gates.md` Gate 0 asks for a yes on the workspace before
   `get_agent_datasources`, and `mosofin-protocol.md:187-198` says the scope steps may not be merged.
   Stage 1 and Stage 2 also run in a different order in different parts of the file.
   **Effect on the site:** the auditors read this differently. The accruals and entries chats show two
   separate yes steps (workspace, then plan). The others show one yes at the plan read-back. Choose one
   reading in the skills, and the chats can then match it.
3. **Sign-off blocks differ between skills.** Bank reconciliation, AP accrual cutoff, AP aging and AR aging
   have a sign-off block. The other skills produce a workpaper with no sign-off. Decide if this is intended.
4. **Some skills name no data tools.** Three-way match, vendor statement reconciliation and prepaid
   amortization have no `tools-and-glossary.md`.

## Problems in one skill

| Skill | Problem |
|---|---|
| ar-aging-and-collections | `SKILL.md:56` says to state the accrual-basis note first. `edge-cases.md:49-51` says not to raise it unprompted. |
| customer-invoicing | The read-back example (`SKILL.md:95-97`) shows the next invoice number, which needs a read that `SKILL.md:30` forbids before the yes. The skill's example also uses NT-1043 and 30 September, but the learn page uses NT-2026-0418 and 31 October. |
| invoice-data-extractor | `SKILL.md:59` says to confirm before extracting a non-invoice document. The output and the learn page treat a pro forma as "Excluded" in the extracted count. |
| merchant-and-payment-processor-rec | The skill card calls the bank statement "strongly recommended". `gates.md` calls it "Required". |
| multi-entity-forecast-dashboard | "P90 uses the higher of the upside and base rates" is in the template and on the learn page, but not in `forecast-method.md`. |
| month-end-close-checklist | Question I is "upload path only" (`SKILL.md:59`), but Stage 1 asks every question before the user chooses a path. |
| inventory-to-gl-reconciliation | `search_items` returns current quantity only (`method.md:44-48`). No tool gives a valuation at a past date, so the subledger leg may often be manual. |
| payroll-journal-entry-builder | `SKILL.md:62` sends clearing to Step 5, but the read-back example funds net pay on the same day. |
| balance-sheet-reconciliations | No status fits an account that is reconciled but has unposted proposed entries (anatomy finding A5). The upload path never asks for the write-off limit that Step 5 needs (A4). |
| accruals-and-deferrals | The read-back and Step 9 call the $240k a "pool". Step 3 calls it a best-estimate payout (A6). Gate 3 has no row for accrual or cash basis (A4). `overview.md` says the skill "books" entries (A7). |
| recurring-transaction-builder | The file-name pattern at `method.md:262` leaves out the entity name that `method.md:264` requires. |
| prepaid-amortization-schedule | Question H takes the currency "from the company record", but the skill names no tool for it. |
| journal-entry-review | The intake letters run A–G, then I, then H (`SKILL.md:62-63`). |
| bank-reconciliation | `overview.md` says the skill finds wrong dates without the statement, but `method.md` marks them as candidates only. The Gate 3 table leaves out next period's activity. |

## Problems in this site's own pages

- **credit-card-reconciliation:** learn Levels 2 and 3 cannot both be true for the same month. The 42-charge
  receipt split does not count the grocery charge with no receipt. The chat avoids these counts.
- **cash-flow-forecast-13-week:** the learn and plain pages give no year, and their weekdays (Monday
  6 October, Wednesday 5 November) fall in 2025. The site's other examples use 2026.
