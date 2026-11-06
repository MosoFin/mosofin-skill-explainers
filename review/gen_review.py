import sys, os, json, html
REPO = "/home/user/mosofin-skill-explainers"
sys.path.insert(0, REPO); os.chdir(REPO)
import build
S = os.path.dirname(os.path.abspath(__file__))   # variants.css and variants.js sit next to this script
skill = "bank-reconciliation"
flow = build.flow_of(skill)
rd = lambda p: open(p).read()
ctrl = lambda: """<div class="pl-bar"><div class="flow-btns">
<button type="button" class="flow-btn primary" data-act="play">▶ Play</button>
<button type="button" class="flow-btn" data-act="prev" aria-label="Previous step">◀</button>
<button type="button" class="flow-btn" data-act="next" aria-label="Next step">▶︎</button>
<button type="button" class="flow-btn" data-act="restart" aria-label="Start again">↺</button></div>
<div class="flow-paths" role="group" aria-label="Choose a path"></div></div>"""
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flow Design Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{rd("site/assets/brand.css")}</style>
<style>body{{margin:0;background:var(--ground);color:var(--ink);font-family:Archivo,system-ui,sans-serif}}.wrap{{max-width:1120px;margin:0 auto;padding:36px 16px 64px}}h1{{font-size:clamp(26px,4vw,38px);margin:6px 0 8px;letter-spacing:-.02em}}.eyebrow{{font:500 12px "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}.lede{{color:var(--muted);max-width:70ch;margin:0}}</style>
<style>{rd("site/assets/flow.css")}</style>
<style>{rd(os.path.join(S, "variants.css"))}</style>
</head><body><main class="wrap">
<div class="eyebrow">Design review · bank reconciliation</div>
<h1>Pick a style for the step-by-step flow</h1>
<p class="lede">The same run, three ways. Each one plays like a movie. Press play, switch the path, or select a step. Pick the style you like, and every skill gets it.</p>
<div class="rv-tabs" role="tablist">
<button role="tab" aria-selected="true" data-tab="a"><b>A · Swimlanes</b><span>The whole map at once, in three columns</span></button>
<button role="tab" aria-selected="false" data-tab="b"><b>B · Storyboard</b><span>One big scene at a time, with a who-does-what track</span></button>
<button role="tab" aria-selected="false" data-tab="c"><b>C · Chat replay</b><span>The run as a conversation with the agent</span></button>
</div>
<div class="rv-panel" data-panel="a">{build.flow_section(skill, "Bank reconciliation").replace('<h2 id="flow-h">Watch a run, step by step</h2>', '')}</div>
<div class="rv-panel" data-panel="b" hidden><div class="pl" id="pl-b">{ctrl()}<div class="sb-track"></div><div class="sb-stage" aria-live="polite"></div><div class="sb-strip" aria-label="All steps"></div><div class="pl-time"></div></div>
<p class="rv-note">Best for: telling the story clearly, one idea at a time. The track above the scene shows who acts at each step.</p></div>
<div class="rv-panel" data-panel="c" hidden><div class="pl" id="pl-c">{ctrl()}<div class="ch-win" aria-live="polite"></div><div class="pl-time" style="padding-top:12px"></div></div>
<p class="rv-note">Best for: showing what working with the agent feels like. Reads from your books appear as tool-call chips.</p></div>
</main>
<script type="application/json" id="flow-src">{json.dumps(flow, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>{rd("site/assets/flow.js")}</script>
<script>{rd(os.path.join(S, "variants.js"))}</script>
<script>
document.querySelectorAll('[role="tab"]').forEach((t) => t.addEventListener("click", () => {{
  document.querySelectorAll('[role="tab"]').forEach((x) => x.setAttribute("aria-selected", String(x === t)));
  document.querySelectorAll(".rv-panel").forEach((p) => p.hidden = p.dataset.panel !== t.dataset.tab);
  Object.entries(window.__rvPlayers || {{}}).forEach(([k, p]) => {{ if (k !== t.dataset.tab) p.pause(); }});
  document.querySelector('.flow [data-act="play"]')?.textContent.includes("Pause") && t.dataset.tab !== "a" && document.querySelector('.flow [data-act="play"]').click();
  const p = window.__rvPlayers?.[t.dataset.tab]; if (p && !p.playing) p.play();
}}));
</script>
</body></html>
"""
os.makedirs("review", exist_ok=True)
open("review/flow-variants.html", "w").write(page)
print("wrote review/flow-variants.html", len(page)//1024, "KB")
