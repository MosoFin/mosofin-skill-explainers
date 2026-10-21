# The anatomy page — how the skill is built (internal)

Reference: `site/skills/merchant-and-payment-processor-rec/anatomy.html`.

## Who reads it

Whoever reviews the skill before it ships, or maintains it after. It names commits, line
counts, tool catalogues and audit findings, so it is `internal` in the tracker: kept in this
repository, never built into the public site, never linked. If a skill's anatomy is ever
worth publishing, strip the commit hashes and tool names first, then flip the status.

## Structure

1. **Header** — eyebrow: skill name · where it stands ("shipped on main" / "branch x, not
   pushed"); title; lede with the one-line construction fact (862 lines → a 121-line card
   and seven reference files).
2. **Stats** — card size, number of reference files, content kept (lines unchanged of the
   original), findings fixed.
3. **Construction** — an SVG: the card on the left with its stages, the reference files on
   the right with line counts, an arrow from each stage to the file it loads. Bars sized to
   line count so a reader sees where the weight is. Update the counts when files change.
4. **The run, stage by stage** — one row per stage: what it asks or reads, what it
   computes, what it hands to the next stage, which file it loads.
5. **Audit** — each finding: what was wrong, the evidence, the fix, the source behind the
   fix (cited the same way as public pages).
6. **Passed** — what checked out, each as a verifiable claim ("every QuickBooks tool named
   exists in the catalogue read on <date>"; "validator: 31 skills, 0 failures").
7. **Not yet tested** — say it plainly. A live run against real connections is the usual gap.
8. **Footer** — commits by hash, the repository, what still has to happen.

## Keeping it true

This page goes stale fastest, because it describes the build. When the skill ships, change
the eyebrow, the footer and the Passed list in the same commit that flips the tracker. When
reference files change, recount lines (`wc -l`) and resize the bars.
