---
name: write-chat-replay
description: Writes the "Watch someone use it" chat replay for a MosoFin finance skill's landing page on skills.mosofin.com. A simulated conversation in which a person uses the skill in an AI chat, with MosoFin tool cards that load the books, results cards that tie to the cent, and a look-only switcher for ChatGPT, Claude, Muse and Grok. It writes the chat file in chats/ from the skill's own worked example, checks every figure, tests the page in a browser and publishes it when asked. Use this whenever someone asks for a chat replay, a chat demo, a simulated conversation, an "animation of someone using the skill", a use-case walkthrough on a skill page, or the same chat for another skill or for the remaining skills, even if they do not say "chat replay".
---

# Write a chat replay

A chat replay shows a person who uses one finance skill, from their first message to the result.
It sits under **"Watch someone use it"** on `site/skills/<skill>/index.html` and plays like a live
chat: the person's message types into the box, the agent's reply streams in, MosoFin tool cards
tick off each call, and result cards fill one row at a time.

The reader is a business owner or a bookkeeper who has not used the skill. In about a minute, they
should see what they must give the agent, what the agent reads, and what they get back. They should
also see that the result is checkable.

The reference implementation is `chats/bank-reconciliation.json`, live at
`https://skills.mosofin.com/skills/bank-reconciliation/`. Read it before you write a new one.

## What is already built, and stays the same

These parts are shared by every skill. A chat replay for a new skill is a new data file. It is not
new code.

- `build.py`: `chat_section` renders the chat, and `chat_problems` checks it in `--check`. A
  skill with `chats/<skill>.json` gets the chat on its landing page.
- `site/assets/chat.js` and `chat.css`: the replay, the four assistant styles and the MosoFin card.
- `site/assets/ai/`: the ChatGPT, Claude, Muse and Grok logos, with their source in `NOTICE.txt`.

Do not change these files to make one skill's chat look different. A change there changes every
skill page. If a skill needs something the format cannot show, stop and ask the user.

The assistant switcher changes the **look only**: the logo, the name, the colors and the font. The
words of every message stay the same in all four styles, and Claude is the default because the
skills run in Claude. The note under the chat says this and names the trademarks. Keep it.

## Workflow

### 1. Read the sources for this skill

The chat has two jobs. It must behave the way the skill behaves, and it must use figures that the
site already publishes. Read:

- **`site/skills/<skill>/anatomy.html`**, section "The run". This page is internal, and it is the
  most exact record of the skill's run on this site. Take the intake questions, the gates, the
  steps, the outputs and what the skill never does from it.
- **`site/skills/<skill>/learn.html`**: the worked examples. The figures live in the `LEVELS` array
  in the page script and in the visible text. Choose the scenario here.
- **`site/skills/<skill>/plain.html`**: the plain words a business owner uses for the same things.
- **The skill itself**, in `MosoFin/mosofin-finance-skills` (`skills/<skill>/SKILL.md` and
  `references/`), if you can reach it. Where it disagrees with the anatomy page, the skill wins.
  Tell the user, because then the anatomy page needs a fix too.

If the skill has no learn page yet, stop. The chat takes its figures from that page, so write the
explainers first (the `write-skill-explainers` skill).

### 2. Choose one scenario

Pick one company, one account or scope, and one period from the learn page, for example
"Northbrook Trading, Operating (…4471), September". Then pick the levels that show the most with the
least: about three findings, of different kinds. For example, one timing item, one item only the
bank knows, and one error inside the books.

Levels often build on each other in the same month. When you combine them, recompute every total
that changes, and check it against the page. In the reference chat, the book balance of $12,155.50
is the $12,180.50 of level 2 minus the duplicate $25 of level 3. The learn page's own calculator
also shows it, so `check_figures.py` finds it.

### 3. Write the conversation

Follow the run of the skill. The usual shape is below. Change it where the skill works differently,
for example a skill that builds a schedule instead of finding differences.

1. **The user asks**, in one plain sentence.
2. **The agent asks its intake questions** in one message, as a numbered `list`. Use the skill's own
   questions in the skill's own order.
3. **The user answers** in one message, and attaches what the skill needs (`attach`).
4. **A MosoFin card checks the connection**: workspace, company file, read-only tools.
5. **The agent reads back its plan** and asks to start. **The user says yes.** This is the skill's
   "read back and wait for a yes" gate, shown as a normal exchange.
6. **A MosoFin card reads the books**, with one row for each tool call that the skill makes.
7. **The agent gives the results**: one message for each finding, each with its card (`bridge` for
   arithmetic, `table` for lists).
8. **The agent proposes what the person does next**, for example entries with their evidence, and gives the
   sign-off (`signoff` card).
9. **The agent offers to save the settings**, if the skill does that. The user says yes, and the agent
   confirms what it saved.

Write it as a real chat. Use the first person for the agent and short messages for the user. Add no
notes, no labels and no warnings under the replies. Users read these chats as a simulation of the
real thing, and earlier drafts that showed red "safeguard" notes felt artificial. When a safeguard
matters to the story, the agent says it in a normal sentence: "A person posts these entries. I do
not." is fine as part of a reply.

Every figure must come from the learn page, from a sum of figures on it, or from a choice that the user
makes in the chat. Record a user choice (a threshold, a file name) under `"chosen"` with a reason. In a
MosoFin card, a row result is a fact that the chat states somewhere else. Otherwise it is `""` and
shows "Read". Never write a row count, a record total or a balance that the page does not give. An
invented figure on a page that claims to tie to the cent undoes the trust that the page is built
for.

The field-by-field format is in `references/chat-format.md`.

The text is public prose, so the house rule applies: write it in Simplified Technical English
(the `technical-writing-ste` skill). Use short sentences, active voice, no em dash, no semicolon
and no filler words. `build.py --check` enforces the mechanical part.

### 4. Check it

Run these from the repository root. Fix each problem. Do not explain it away.

```bash
python3 build.py
```

```bash
python3 build.py --check
```

```bash
python3 .claude/skills/write-chat-replay/scripts/check_figures.py <skill>
```

`--check` checks the format, the arithmetic of every bridge card, and the voice rules. `check_figures.py`
lists every figure that is not on the learn page. For each one, fix it, show the sum it comes from,
or record it under `"chosen"`.

### 5. Test it in a browser

```bash
python3 build.py --stage _site
```

```bash
python3 -m http.server 8765 --directory _site
```

Run the server in the background, then:

```bash
node .claude/skills/write-chat-replay/scripts/test_chat.js <skill>
```

The test checks two widths and both color themes. It checks that the chat starts by itself, that
"Show all" shows every message, and that every MosoFin call finishes. It also checks that the four
styles show the same words, and that the page has no errors, no notes and no sideways scrolling.

Then read the whole conversation once as the business owner. Does each message follow from the last
one? Would the person know what to do next? The test cannot judge this.

### 6. Show it, then publish when asked

```bash
python3 .claude/skills/write-chat-replay/scripts/preview_page.py <skill>
```

This writes `review/<skill>-page.html`, one file with the page and its chat, which the user can open
before anything is published. Send it to them.

Commit on the working branch. Write the commit message in STE. Publish only when the user asks: open
a pull request to `main` and merge it. The Pages workflow then deploys the site in about 90 seconds.
Check that the run succeeded before you say the page is live. If you cannot open
`skills.mosofin.com` from your environment, say so, and ask the user to look.

## When the user asks for several skills

Write, check and test one skill completely first, and show it. Then do the others the same way, one
file each. A shared mistake is cheaper to fix in one chat than in thirty.

## Report

When you finish, tell the user:

- the scenario (company, scope, period) and which learn-page levels it combines
- every derived total, with its sum, and every `"chosen"` value
- the results of the checks and the browser test
- the preview file, and whether the page is live
