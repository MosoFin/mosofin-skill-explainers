#!/usr/bin/env python3
"""Check that every figure in a chat replay comes from the skill's worked examples.

usage: python3 .claude/skills/write-chat-replay/scripts/check_figures.py <skill>
       (run from the repository root)

The chat may only use figures that the skill's learn page states: dollar amounts,
cheque and payment numbers, masked account numbers, dates. This script lists every
figure in chats/<skill>.json and looks for it in site/skills/<skill>/learn.html,
including the page's script data. A figure that is not there is either a mistake
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
    """Dollar amounts, #numbers, masked account endings and 3+ digit numbers."""
    out = set(re.findall(r"\$-?[\d,]+(?:\.\d+)?", text))
    out |= set(re.findall(r"#\d+", text))
    out |= set(re.findall(r"(?:…|\.\.\.)\d{3,}", text))
    out |= {n for n in re.findall(r"(?<![\d$#.,])\d{3,}(?![\d,])", text)}
    return out


def variants(fig):
    """Ways the learn page may write the same figure: 1,250 / 1250 / 1,250.00 / $1,250."""
    v = {fig}
    if fig.startswith("$"):
        n = fig[1:].replace(",", "")
        try:
            x = float(n)
        except ValueError:
            return v
        whole = f"{x:,.0f}" if x == int(x) else None
        v |= {f"${x:,.2f}", f"{x:,.2f}", f"{x:.2f}"}
        if whole:
            v.add(f"${whole}")
            # A bare whole number ("1860" in the page's data) counts only from 100 up.
            # "10" or "25" alone is too common ("10 business days") to prove anything.
            if abs(x) >= 100:
                v |= {whole, whole.replace(",", "")}
    if fig.startswith("#"):
        v.add(fig[1:])
    if fig.startswith("…") or fig.startswith("..."):
        v.add(fig.lstrip("…."))
    return v


def main(skill):
    chat_path = os.path.join(ROOT, "chats", f"{skill}.json")
    learn_path = os.path.join(ROOT, "site", "skills", skill, "learn.html")
    if not os.path.exists(chat_path):
        sys.exit(f"no {os.path.relpath(chat_path, ROOT)}")
    if not os.path.exists(learn_path):
        sys.exit(f"no {os.path.relpath(learn_path, ROOT)}: write the learn page first, the chat takes its figures from it")
    data = json.load(open(chat_path))
    chosen = data.get("chosen", {})   # values the user picks in the chat, each with a reason
    chat = json.dumps({k: v for k, v in data.items() if k != "chosen"}, ensure_ascii=False)
    chat = chat.replace("\\u2026", "…")
    page = open(learn_path).read()
    # Look only at what the page says: drop styles, meta tags and the generated SEO and citation blocks.
    page = re.sub(r"<style>.*?</style>|<meta[^>]*>|<link[^>]*>|<!-- seo:start.*?seo:end -->", " ", page, flags=re.S)
    page_flat = re.sub(r"\s+", " ", html.unescape(page))

    def on_page(v):
        # A whole figure only: "10" must not match inside "#0d1210" or "2010".
        return re.search(r"(?<![\w.,#])" + re.escape(v) + r"(?![\d])(?!,\d)", page_flat) is not None

    missing = []
    for fig in sorted(figures(chat)):
        if fig in chosen:
            continue
        if not any(on_page(v) for v in variants(fig)):
            missing.append(fig)
    for fig, why in sorted(chosen.items()):
        print(f"  chosen by the user in the chat, not from the page: {fig} ({why})")
    found = len(figures(chat)) - len(missing) - len(set(chosen) & figures(chat))
    print(f"{skill}: {found} figure(s) found on the learn page")
    if missing:
        print("Not on the learn page. Fix each one. If it is a derived total, show the sum in your report.")
        print("If the user chooses it in the chat (a threshold, a file name), list it under \"chosen\" with a reason.")
        for m in missing:
            print(f"  {m}")
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
