#!/usr/bin/env python3
"""Write a self-contained preview of a skill's landing page, chat replay included.

usage: python3 .claude/skills/write-chat-replay/scripts/preview_page.py <skill>
       (run from the repository root, after python3 build.py)

The preview goes to review/<skill>-page.html. It puts the site's styles and scripts
inside the page, so it opens as one file before anything is published. Links and
images that are not inside the file point at the live site.
"""
import os
import re
import sys

SITE_URL = "https://skills.mosofin.com/"


def main(skill):
    src = os.path.join("site", "skills", skill, "index.html")
    if not os.path.exists(src):
        sys.exit(f"no {src}: run python3 build.py first")
    page = open(src).read()
    if 'class="chat"' not in page:
        sys.exit(f"{src} has no chat replay: write chats/{skill}.json and run python3 build.py")
    read = lambda p: open(os.path.join("site", "assets", p)).read()
    for css in ("brand.css", "chat.css"):
        page = page.replace(f'<link rel="stylesheet" href="../../assets/{css}">', f"<style>{read(css)}</style>")
    for js in ("theme.js", "chat.js"):
        page = page.replace(f'<script src="../../assets/{js}" defer></script>', "")
    page = page.replace("</body>", f"<script>{read('theme.js')}</script>\n<script>{read('chat.js')}</script>\n</body>", 1)
    page = re.sub(r'(href|src)="\.\./\.\./', rf'\1="{SITE_URL}', page)
    page = re.sub(r'href="(plain|learn)/"', rf'href="{SITE_URL}skills/{skill}/\1/"', page)
    os.makedirs("review", exist_ok=True)
    out = os.path.join("review", f"{skill}-page.html")
    open(out, "w").write(page)
    print(f"wrote {out} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
