#!/usr/bin/env python3
"""Check that every figure in a chat replay comes from the skill's published pages.

usage: python3 .claude/skills/write-chat-replay/scripts/check_figures.py <skill>
       (run from the repository root)

The chat may only use figures that the skill's learn page states: dollar amounts,
cheque and payment numbers, masked account numbers, dates. This script lists every
figure in chats/<skill>.json and looks for it in site/skills/<skill>/learn.html
(including the page's script data) and plain.html. A figure that is not there is either a mistake
or a derived total (a sum of figures that are there). The script cannot tell the
two apart, so it prints each one for you to explain or fix. Exit code 1 means at
least one figure needs an explanation.
"""
import html
import json
import os
import re
import sys

ROOT = os.getcwd()


def figures(text):
    """Amounts in $, £ or €, #numbers, masked account endings and 3+ digit numbers."""
    out = set(re.findall(r"[$£€]-?[\d,]+(?:\.\d+)?", text))
    out |= set(re.findall(r"#\d+", text))
    out |= set(re.findall(r"(?:…|\.\.\.)\d{3,}", text))
    out |= {n for n in re.findall(r"(?<![\d$#.,])\d{3,}(?![\d,])", text)}
    return out


def main(skill):
    chat_path = os.path.join(ROOT, "chats", f"{skill}.json")
    learn_path = os.path.join(ROOT, "site", "skills", skill, "learn.html")
    plain_path = os.path.join(ROOT, "site", "skills", skill, "plain.html")
    if not os.path.exists(chat_path):
        sys.exit(f"no {os.path.relpath(chat_path, ROOT)}")
    if not os.path.exists(learn_path):
        sys.exit(f"no {os.path.relpath(learn_path, ROOT)}: write the learn page first, the chat takes its figures from it")
    data = json.load(open(chat_path))
    chosen = data.get("chosen", {})   # values the user picks in the chat, each with a reason
    chat = json.dumps({k: v for k, v in data.items() if k != "chosen"}, ensure_ascii=False)
    chat = chat.replace("\\u2026", "…")
    # The learn page is the main source. The plain page is published too, and it may show a total
    # (a weekly balance, a summary table) that the learn page only computes in its script.
    page = open(learn_path).read() + (open(plain_path).read() if os.path.exists(plain_path) else "")
    # Look only at what the page says: drop styles, meta tags and the generated SEO and citation blocks.
    page = re.sub(r"<style>.*?</style>|<meta[^>]*>|<link[^>]*>|<!-- seo:start.*?seo:end -->", " ", page, flags=re.S)
    page_flat = re.sub(r"\s+", " ", html.unescape(page))

    # Every number on the page, as a value. "12,480.00" is one number. "46200,31800" (a data array)
    # is two. "#0d1210" (a colour) and "v2.4" are not numbers.
    values = []
    for m in re.finditer(r"(?<![\w.#])([$£€])?(\d[\d,]*\d|\d)(\.\d+)?", page_flat):
        dollar, body, cents = m.group(1), m.group(2), m.group(3) or ""
        parts = body.split(",")
        if len(parts) > 1 and len(parts[0]) <= 3 and all(len(x) == 3 for x in parts[1:]):
            values.append((float(body.replace(",", "") + cents), bool(dollar or cents)))
        else:
            for i, x in enumerate(parts):
                if x:
                    values.append((float(x + (cents if i == len(parts) - 1 else "")), bool(dollar and i == 0)))

    def on_page(fig):
        if fig[:1] in "$£€":
            x = float(fig[1:].replace(",", ""))
            if x == 0:
                return True   # a zero difference ("$0.00") states that something ties. It is never an invented figure.
            # A small bare number ("10", "25") is too common to prove anything. It counts only with a currency sign or cents.
            return any(abs(v - x) < 0.005 and (marked or abs(x) >= 100) for v, marked in values)
        if fig.startswith("#") or fig.startswith("…") or fig.startswith("..."):
            core = fig.lstrip("#….")
            return re.search(r"(?<![\w])#?" + re.escape(core) + r"(?![\d])", page_flat) is not None
        return any(abs(v - float(fig)) < 0.005 for v, _ in values)

    missing = []
    for fig in sorted(figures(chat)):
        if fig in chosen:
            continue
        if not on_page(fig):
            missing.append(fig)
    for fig, why in sorted(chosen.items()):
        print(f"  chosen by the user in the chat, not from the page: {fig} ({why})")
    found = len(figures(chat)) - len(missing) - len(set(chosen) & figures(chat))
    print(f"{skill}: {found} figure(s) found on the learn or plain page")
    if missing:
        print("Not on the learn or plain page. Fix each one. If it is a derived total, show the sum in your report.")
        print("If the user chooses it in the chat (a threshold, a file name), list it under \"chosen\" with a reason.")
        for m in missing:
            print(f"  {m}")
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
