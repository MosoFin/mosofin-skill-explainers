# Chat file format: `chats/<skill>.json`

`build.py` reads this file, renders the whole conversation as plain HTML on
`site/skills/<skill>/index.html`, and checks it in `--check`. `site/assets/chat.js` replays it.
The reference file is `chats/bank-reconciliation.json`. Read it before you write a new one.

## Top level

```json
{
  "example": "Example run with fictional figures: <company>, <account or scope>, <period>. The figures match the worked examples on the step-by-step page.",
  "chosen": { "$10": "the user's own threshold for which differences to chase" },
  "messages": [ ... ]
}
```

| Field | Required | What it is |
|---|---|---|
| `example` | yes | One or two sentences above the chat. Say that the figures are fictional, and where they come from. |
| `chosen` | no | Figures that the user picks in the chat and the learn page does not state, such as a threshold or a file name. Give each one a reason. `check_figures.py` prints them for the reviewer. |
| `messages` | yes | At least 6. The first one comes from the user. |

## Messages

Three roles. A field that is not in this table fails `build.py --check`.

### `user`

```json
{"role": "user", "text": "Can you reconcile our operating account for September?",
 "attach": ["operating-4471-september.pdf"]}
```

- `text`: what the person types. It types into the message box during the replay, so keep it short and natural.
- `attach`: optional file names, shown as file chips under the bubble.

### `agent`

```json
{"role": "agent",
 "text": "Your books say **$12,155.50**. Three statement lines are not in the books:",
 "list": ["...", "..."],
 "card": { ... },
 "after": "Cheque #1031 to Acme Supplies is in the books twice."}
```

The parts show in this order: `text`, `list`, `card`, `after`. `text` is required.

- `**bold**` works in `text`, `list` items and `after`. Nothing else is markup.
- `list` renders as a numbered list. Use it for the intake questions.
- There is no `guard` field. The chat imitates a real chat, and a real chat shows no notes under a
  reply. If a safeguard matters, the agent says it in a normal sentence.

### `tool`

A MosoFin tool card. Use it for every step where the agent reads the books through MosoFin.

```json
{"role": "tool", "source": "mosofin",
 "label": "Read the books in one batch", "tag": "read-only",
 "rows": [["search_accounts", "Operating (…4471)"],
          ["get_trial_balance", ""]],
 "summary": "9 reads in one batch. Nothing in your books changed."}
```

- `rows`: `[name, result]` pairs, one for each call or check. A name in `lower_snake_case` shows in
  code type; any other name shows in bold (use that for checks such as "Workspace").
- `result`: only a fact that the conversation states somewhere else, such as an account, a balance or an
  item that the agent names later. Write `""` when the chat states no result, and the card shows
  "Read". An invented row count or total is the main way a chat goes wrong.
- `tag`: `read-only` for every MosoFin read.
- `summary`: one short line that closes the card.
- Without `"source": "mosofin"`, a tool step renders as a plain grey line with `calls` (a list of
  strings). Use that only for a step that does not go through MosoFin.

## Cards (`card` in an agent message)

### `bridge`: arithmetic that must tie

```json
{"type": "bridge", "title": "Book side", "rows": [
  ["Book balance", "$12,155.50"],
  ["− Bank fee, statement line 14 Sep", "$15.00"],
  ["+ Interest, statement line 30 Sep", "$4.50"],
  ["= Adjusted book balance", "$11,870.00", "total"],
  ["Difference to the adjusted bank balance", "$0.00", "ok"]
]}
```

- The first row is the starting amount, in $, £ or €. Every next label starts with `+`, `−` or `=`.
- `build.py --check` adds and subtracts the rows and fails if an `=` row does not match.
- The third item styles a row: `total` (bold, with a rule above it) or `ok` (green). An `ok` row is not part
  of the sum.

### `table`

```json
{"type": "table", "title": "Proposed entries", "head": ["Entry", "Amount", "Evidence"],
 "rows": [["Record the bank fee", "$15.00", "Statement line, 14 Sep"]]}
```

The second column aligns right, so put the amount there.

### `signoff`

```json
{"type": "signoff", "title": "Sign-off", "rows": [["Prepared by", ""], ["Reviewed by", ""]]}
```

An empty value draws a signature line.

## Voice checks that `build.py --check` runs on every text field

- No em dash and no semicolon.
- At most 25 words in a sentence.
- None of the filler words in `BANNED` in `build.py`.
