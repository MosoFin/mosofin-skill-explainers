# Builds review/chat-demo.html: the chat replay for one skill, self-contained, for design review.
import sys, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO); os.chdir(REPO)
import build
skill = sys.argv[1] if len(sys.argv) > 1 else "bank-reconciliation"
title = "Bank reconciliation" if skill == "bank-reconciliation" else skill.replace("-", " ").capitalize()
rd = lambda p: open(p).read()
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chat Replay Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{rd("site/assets/brand.css")}</style>
<style>body{{margin:0;background:var(--ground);color:var(--ink);font-family:Archivo,system-ui,sans-serif}}.wrap{{max-width:920px;margin:0 auto;padding:36px 16px 64px}}h2{{font-size:clamp(24px,3.5vw,32px);margin:0 0 6px;letter-spacing:-.02em}}.eyebrow{{font:500 12px "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}}</style>
<style>{rd("site/assets/chat.css")}</style>
</head><body><main class="wrap">
<div class="eyebrow">Design review · {build.e(title)}</div>
{build.chat_section(skill, title)}
</main>
<script>{rd("site/assets/chat.js")}</script>
</body></html>
"""
open(os.path.join(REPO, "review", "chat-demo.html"), "w").write(page)
print("wrote review/chat-demo.html", len(page) // 1024, "KB")
