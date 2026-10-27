---
name: technical-writing-ste
description: "House rule for all technical writing in this project. Write it in Simplified Technical English (the ASD-STE100 structural rules). Check it with the STE linter before you commit or publish it. Covers explainer pages, skill files and their references, READMEs and docs, commit messages, pull request descriptions, error and status messages, tool descriptions and code comments. Use this whenever you write or rewrite English text that a person or an agent reads to understand or act. Use it even if the request does not mention STE, plain English or style. Not for verbatim quotes, code, file names, or text that must stay byte-identical."
---

# Technical writing: use Simplified Technical English

Every piece of technical writing in this project follows the structural rules of **ASD-STE100
Simplified Technical English (STE)**. STE removes the two main causes of misreading: words with more
than one meaning, and sentences with more than one possible structure. Our readers include business
owners, bookkeepers, reviewers, readers of English as a second language, translation tools and AI
agents. None of them can ask the author what a sentence meant.

The rules come from the [asd-ste100 skill](https://github.com/danyuchn/asd-ste100-skill) (MIT
licence, checked at commit `cd62d29`). Install it once, outside this repository:

```bash
git clone https://github.com/danyuchn/asd-ste100-skill ~/.claude/skills/asd-ste100
```

Read its `SKILL.md` before your first STE rewrite. This file says where the rules apply in this
project and which mode to use. It also says what must never change, and how you prove that you
applied the rules.

## Where the rules apply

| Text | Mode | How to check it |
|---|---|---|
| Explainer pages (`site/skills/*/*.html`) | STE-flavored | Extract, lint, then run `ste_verify.py` (below) |
| Skill files you write or rewrite (`SKILL.md`, `references/*.md`) | Strict for steps and instructions, STE-flavored for background | Lint the file directly |
| READMEs, workflow docs, reference docs | STE-flavored | Lint the file directly |
| Commit messages and pull request descriptions | STE-flavored | Lint the message text |
| Error messages, status messages, tool descriptions, prompts for other agents | Strict | Lint the text |
| Code comments | STE-flavored | Read them against the rules. The linter is optional. |

**Strict mode** applies every rule, including one word for one meaning. Use it where a wrong reading
has a cost: a step, an instruction, an error, a tool description. **STE-flavored mode** enforces the
structural rules and treats the vocabulary rules as advice. Use it for explanations and background.

## The rules

Apply these in both modes:

1. **Active voice, with the actor named.** "The skill reads the ledger", not "the ledger is read".
   Keep a passive only when the actor is unknown or does not matter.
2. **Short sentences.** At most 20 words for a step or an instruction. At most 25 words for a
   description.
3. **One idea in a sentence. One instruction in a sentence.**
4. **No semicolons.** Write two sentences.
5. **No phrasal verbs.** "Start", not "kick off". "Remove", not "take off".
6. **A verb, not a noun made from it.** "Analyze the log", not "perform an analysis of the log".
7. **Simple tenses.** "The run failed", not "the run has failed". Keep a compound tense only when it
   carries information, such as "may have failed", and say why.
8. **No dropped words.** Keep the subject, the verb and the article, even when the sentence gets longer.
9. **Lists for sequences.** Use a numbered or bulleted list for three or more steps or conditions.
10. **One topic in a paragraph, at most six sentences.**

In strict mode, also:

11. **One word for one meaning.** Choose one verb for one action and use it every time. Do not rotate
    "check", "verify" and "confirm" for the same action.
12. **Define a necessary technical term once**, and keep the term. Add the plain gloss beside it.

This project adds three house rules for all public prose. Use no em dash. Use no filler words
(`leverage`, `robust`, `seamless` and the others in `build.py`). Write no "not X, it's Y" lines.

## What must never change

STE fixes the form of a text, not its content. A rewrite must keep:

- **Every hedge.** "May", "usually", "often" and "about" carry the author's confidence. Never turn a
  hedge into a fact. Never turn a fact into a hedge.
- **Every condition, scope limit and number.** If a shorter sentence loses one, keep the longer
  sentence and write down why.
- **Every verbatim quote.** A rule quoted from a skill, a source title, or a quoted error message stays
  word for word, even when it breaks an STE rule.
- **Code, file names, tool names, commands and identifiers.** These are not prose.
- **Text that must stay byte-identical.** For example, when a skill is split into the card format,
  the original text moves into `references/` unchanged. Apply STE to new text only.

Never add a fact, a cause or an example that the original text did not state. A rewrite that reads
better because it adds a claim is no longer a rewrite.

## How to check

Set the linter path once:

```bash
STE=~/.claude/skills/asd-ste100/scripts/ste-lint.py
```

**A Markdown or text file.**

```bash
python3 -I "$STE" path/to/file.md
```

**A commit message, before you commit.**

```bash
python3 -I "$STE" < message.txt
```

**An explainer page.** Extract the visible prose first, then lint it. For a rewrite of an existing
page, also prove that only the wording changed:

```bash
python3 -I .claude/skills/write-skill-explainers/scripts/ste_extract.py site/skills/<skill>/<kind>.html > /tmp/page.txt
python3 -I "$STE" /tmp/page.txt
python3 -I .claude/skills/write-skill-explainers/scripts/ste_verify.py site/skills/<skill>/<kind>.html
```

The target is zero hard findings. A finding may stay only when the linter is wrong, or when a rule in
"What must never change" requires it. Examples: a quoted rule, a file name, a legend line read as one
long sentence, or two different actions that the linter reads as synonyms. Write each reason in the
commit message.

The linter checks structure only. It does not check meaning, and it does not compare a rewrite with
the original. After the linter passes, read the text once as a person. Re-add every figure you touched.

## What to claim

Say that a text follows the structural rules of ASD-STE100. Do not call it "STE-compliant". The STE
approved-word dictionary is not public to redistribute, and nothing here checks against it.

## Related

- `write-skill-explainers`: the workflow for explainer pages. Its `references/voice.md` has the STE
  pass for pages in detail.
- The asd-ste100 skill's `references/writing-rules.md` and `examples/before-after.md`: the full rule
  summary and worked examples.
