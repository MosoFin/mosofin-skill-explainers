#!/usr/bin/env python3
"""Build the MosoFin skill explainers site from tracker.tsv.

    python3 build.py                     write site/index.html and each skill's landing page
    python3 build.py --check             fail if the site or the tracker has drifted (CI runs this)
    python3 build.py --stage [DIR]       copy site/ to DIR (default _site/) without internal pages, for Pages
    python3 build.py --sync PATH [REF]   add any skill in a mosofin-finance-skills checkout that the
                                         tracker is missing, and refresh title-less summaries.
                                         REF is the branch that counts as shipped (default mosofin/main)

The tracker is the source of truth. Explainer pages themselves are hand-made and live at
site/skills/<skill>/<kind>.html; this script writes only the index and the landing pages.
Dependency-free on purpose.
"""
import csv, html, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TRACKER = os.path.join(ROOT, "tracker.tsv")
SITE = os.path.join(ROOT, "site")
SKILLS_REPO = "https://github.com/MosoFin/mosofin-finance-skills"
COLUMNS = ["skill", "genre", "skill_status", "title", "plain", "learn", "anatomy",
           "sources", "verified", "summary", "notes"]
KINDS = [
    ("plain",   "Plain-language overview", "Business owners",
     "What the skill checks and the mistake it catches, in everyday terms."),
    ("learn",   "Learn it step by step",   "Owners and bookkeepers",
     "Worked levels from simple to cross-source, every rule and number cited, with a calculator to check your own figures."),
    ("anatomy", "How it's built",          "Reviewers and builders",
     "The card, its reference files, the stages it runs, and the audit behind it."),
]
STATUSES = {"published", "internal", "todo"}
e = lambda s: html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- tracker
def read_tracker():
    with open(TRACKER, newline="") as f:
        rows = [r for r in csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t")]
    return rows

def write_tracker(rows):
    head = [l for l in open(TRACKER) if l.startswith("#")]
    with open(TRACKER, "w", newline="") as f:
        f.writelines(head)
        w = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=sort_key):
            w.writerow({c: r.get(c, "") for c in COLUMNS})

def sort_key(r):
    has = any(r[k] != "todo" for k, *_ in KINDS)
    return (0 if has else 1, r["genre"], r["skill"])

def title_of(r):
    return r["title"] or r["skill"].replace("-", " ").capitalize()

def page_title(path):
    m = re.search(r"<title>(.*?)</title>", open(path).read(), re.S)
    return m.group(1).strip() if m else ""


# --------------------------------------------------------------------------- checks
def problems(rows):
    out = []
    seen = set()
    for r in rows:
        s = r["skill"]
        if s in seen: out.append(f"{s}: listed twice")
        seen.add(s)
        if r["skill_status"] not in {"shipped", "prototype"}:
            out.append(f"{s}: skill_status must be shipped or prototype, got {r['skill_status']!r}")
        for k, *_ in KINDS:
            st = r[k]
            p = os.path.join(SITE, "skills", s, f"{k}.html")
            if st not in STATUSES:
                out.append(f"{s}: {k} status must be one of {sorted(STATUSES)}, got {st!r}")
            elif st == "todo" and os.path.exists(p):
                out.append(f"{s}: {k}.html exists but the tracker says todo")
            elif st != "todo" and not os.path.exists(p):
                out.append(f"{s}: tracker says {k} is {st} but site/skills/{s}/{k}.html is missing")
            elif st != "todo" and not page_title(p):
                out.append(f"{s}: {k}.html has no <title>")
    # every explainer file on disk must be tracked
    base = os.path.join(SITE, "skills")
    for s in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        if not os.path.isdir(os.path.join(base, s)):
            if s != ".DS_Store": out.append(f"site/skills/{s}: stray file — explainers go in site/skills/<skill>/<kind>.html")
            continue
        for fn in sorted(os.listdir(os.path.join(base, s))):
            if fn == "index.html" or not fn.endswith(".html"): continue
            k = fn[:-5]
            if s not in seen: out.append(f"site/skills/{s}/ exists but {s} is not in the tracker")
            elif k not in dict((x[0], 1) for x in KINDS): out.append(f"site/skills/{s}/{fn}: unknown kind {k!r}")
    return out


# --------------------------------------------------------------------------- shared page shell
STYLE = """
:root{--ground:#f7f8f6;--panel:#fff;--sunk:#f1f4f2;--ink:#14201b;--muted:#56655f;--faint:#86948e;
 --rule:#dfe6e2;--rule-strong:#c6d1cb;--green:#0b8f5a;--green-soft:#e3f3ea;--blue:#3f6d96;--blue-soft:#e7eff6;
 --hold:#a06a12;--hold-soft:#f7eedb;--shadow:0 1px 2px rgba(20,32,27,.05),0 10px 28px -18px rgba(20,32,27,.3)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ground:#0d1210;--panel:#151c19;--sunk:#111815;
 --ink:#e8eeea;--muted:#9eaba5;--faint:#76857e;--rule:#26312c;--rule-strong:#34413b;--green:#43c78e;--green-soft:#123024;
 --blue:#8db3d8;--blue-soft:#15202b;--hold:#dba657;--hold-soft:#2d2413;--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -18px rgba(0,0,0,.8)}}
:root[data-theme="dark"]{--ground:#0d1210;--panel:#151c19;--sunk:#111815;--ink:#e8eeea;--muted:#9eaba5;--faint:#76857e;
 --rule:#26312c;--rule-strong:#34413b;--green:#43c78e;--green-soft:#123024;--blue:#8db3d8;--blue-soft:#15202b;
 --hold:#dba657;--hold-soft:#2d2413;--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -18px rgba(0,0,0,.8)}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:Archivo,"Helvetica Neue",Arial,sans-serif;font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:960px;margin:0 auto;padding:48px 16px 88px;display:flex;flex-direction:column;gap:44px}
@media (min-width:700px){.wrap{padding-left:28px;padding-right:28px}}
a{color:var(--green)} a:focus-visible{outline:2px solid var(--green);outline-offset:2px;border-radius:4px}
.label{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint)}
h1{margin:0;font-size:clamp(32px,5.5vw,50px);line-height:1.05;font-weight:800;letter-spacing:-.03em;text-wrap:balance}
h2{margin:0;font-size:24px;font-weight:700;letter-spacing:-.015em}
p{margin:0;max-width:66ch}
.lede{font-size:19px;color:var(--muted)}
header,section{display:flex;flex-direction:column;gap:14px}
.crumb{font-size:14px;color:var(--muted)} .crumb a{color:inherit}
.pill{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:5px;background:var(--sunk);color:var(--muted)}
.pill.ok{background:var(--green-soft);color:var(--green)} .pill.int{background:var(--hold-soft);color:var(--hold)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--rule);border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:10px;box-shadow:var(--shadow);text-decoration:none;color:inherit;border-top:4px solid var(--green)}
.card:hover{border-color:var(--green)} .card.todo{border-top-color:var(--rule-strong);box-shadow:none;opacity:.75}
.card b{font-size:18px} .card .who{font-size:13.5px;color:var(--faint)} .card p{font-size:15px;color:var(--muted)}
.card .go{font-weight:600;color:var(--green);font-size:15px;margin-top:auto}
.panel{background:var(--panel);border:1px solid var(--rule);border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:10px}
pre{margin:0;background:var(--sunk);border-radius:8px;padding:12px;overflow-x:auto;font-family:"IBM Plex Mono",monospace;font-size:13px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.stat{background:var(--panel);border:1px solid var(--rule);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:2px}
.stat .v{font-size:30px;font-weight:800;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat .s{font-size:14px;color:var(--muted)}
.tbl{overflow-x:auto;background:var(--panel);border:1px solid var(--rule);border-radius:14px}
table{border-collapse:collapse;width:100%;font-size:15px}
th,td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--rule);white-space:nowrap}
th{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);font-weight:500}
tbody tr:last-child td{border-bottom:none}
td.c{text-align:center} .dash{color:var(--faint)}
footer{border-top:1px solid var(--rule);padding-top:18px;color:var(--faint);font-size:13.5px}
"""

def shell(title, body, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{STYLE}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
"""


# --------------------------------------------------------------------------- pages
def landing(r):
    s, t = r["skill"], title_of(r)
    cards = []
    for k, label, who, blurb in KINDS:
        st = r[k]
        if st == "todo":
            cards.append(f'<div class="card todo"><span class="label">{e(label)}</span><b>Not written yet</b>'
                         f'<span class="who">For {e(who.lower())}</span><p>{e(blurb)}</p></div>')
            continue
        pt = page_title(os.path.join(SITE, "skills", s, f"{k}.html"))
        if st == "internal":
            cards.append(f'<div class="card todo"><span class="label">{e(label)} <span class="pill int">internal</span></span>'
                         f'<b>{e(pt)}</b><span class="who">For {e(who.lower())}</span>'
                         f'<p>Kept for reviewers in the repository; not published on this site.</p></div>')
            continue
        cards.append(f'<a class="card" href="{k}.html"><span class="label">{e(label)}</span><b>{e(pt)}</b>'
                     f'<span class="who">For {e(who.lower())}</span><p>{e(blurb)}</p><span class="go">Open →</span></a>')
    if r["skill_status"] == "shipped":
        use = f"""<p>Install just this skill — no clone needed:</p>
<pre>curl -sL {SKILLS_REPO}/archive/refs/heads/main.tar.gz | tar -xz -C ~/.claude/skills --strip-components=2 mosofin-finance-skills-main/skills/{e(s)}</pre>
<p><a href="{SKILLS_REPO}/tree/main/skills/{e(s)}">Read the skill on GitHub →</a></p>"""
    else:
        use = ("<p><b>In review.</b> This skill is not in the skills repository yet, so there is nothing to install. "
               "The explainers describe the version under review.</p>")
    meta = []
    if r["sources"]: meta.append(f'{e(r["sources"])} outside sources cited')
    if r["verified"]: meta.append(f'last verified {e(r["verified"])}')
    status = '<span class="pill ok">shipped</span>' if r["skill_status"] == "shipped" else '<span class="pill int">in review</span>'
    body = f"""<header>
  <div class="crumb"><a href="../../">All skills</a> › {e(t)}</div>
  <span class="label">{e(r["genre"])} skill · <code>{e(s)}</code> {status}</span>
  <h1>{e(t)}</h1>
  <p class="lede">{e(r["summary"])}</p>
</header>
<section>
  <h2>Explainers</h2>
  <div class="cards">{"".join(cards)}</div>
</section>
<section>
  <h2>Use the skill</h2>
  <div class="panel">{use}</div>
</section>
<footer>{" · ".join(meta) or "Explainers not yet verified"}. {e(r["notes"])}</footer>"""
    return shell(t, body, r["summary"])

def chip(r, k):
    st = r[k]
    if st == "todo": return '<td class="c"><span class="dash">—</span></td>'
    if st == "internal": return '<td class="c"><span class="pill int">internal</span></td>'
    return f'<td class="c"><a href="skills/{e(r["skill"])}/{k}.html"><span class="pill ok">view</span></a></td>'

def index(rows):
    n = len(rows)
    with_any = [r for r in rows if any(r[k] != "todo" for k, *_ in KINDS)]
    pages = sum(1 for r in rows for k, *_ in KINDS if r[k] == "published")
    trs = []
    for r in rows:
        name = (f'<a href="skills/{e(r["skill"])}/">{e(title_of(r))}</a>' if r in with_any else e(title_of(r)))
        trs.append(f'<tr><td>{name}<br><code style="font-size:12px;color:var(--faint)">{e(r["skill"])}</code></td>'
                   f'<td>{e(r["genre"])}</td>' + "".join(chip(r, k) for k, *_ in KINDS) + "</tr>")
    body = f"""<header>
  <span class="label">MosoFin finance skills</span>
  <h1>Skill explainers</h1>
  <p class="lede">Each finance skill, explained three ways: in plain words for business owners, step by step with
  worked examples and cited sources, and how it is built. Generated from <code>tracker.tsv</code>.</p>
</header>
<section>
  <div class="stats">
    <div class="stat"><span class="label">Skills tracked</span><span class="v">{n}</span><span class="s">in the tracker</span></div>
    <div class="stat"><span class="label">With explainers</span><span class="v">{len(with_any)}</span><span class="s">at least one page</span></div>
    <div class="stat"><span class="label">Pages</span><span class="v">{pages}</span><span class="s">published, of {n * len(KINDS)} possible</span></div>
  </div>
</section>
<section>
  <h2>All skills</h2>
  <div class="tbl"><table>
    <thead><tr><th>Skill</th><th>Genre</th>{"".join(f'<th class="c">{e(l)}</th>' for _, l, *__ in KINDS)}</tr></thead>
    <tbody>{"".join(trs)}</tbody>
  </table></div>
</section>
<footer>The skills themselves live in <a href="{SKILLS_REPO}">MosoFin/mosofin-finance-skills</a>. Explainers live here, separately, so nothing on this site is installed with a skill.</footer>"""
    return shell("Skill Explainers", body, "Each MosoFin finance skill explained in plain words, step by step, and how it is built.")

def outputs(rows):
    out = {os.path.join(SITE, "index.html"): index(rows)}
    for r in rows:
        if any(r[k] != "todo" for k, *_ in KINDS):
            out[os.path.join(SITE, "skills", r["skill"], "index.html")] = landing(r)
    return out


# --------------------------------------------------------------------------- sync
def frontmatter_summary(path):
    t = open(path).read()
    m = re.search(r'^description:\s*"?(.*?)"?\s*$', t, re.M)
    d = re.sub(r"\s+", " ", m.group(1)) if m else ""
    first = re.split(r"(?<=[.!?])\s", d, maxsplit=1)[0]
    return first[:240]

def sync(path, ref):
    rows = {r["skill"]: r for r in read_tracker()}
    added = 0
    for genre, folder in [("analysis", "skills"), ("dashboard", "dashboards")]:
        base = os.path.join(path, folder)
        if not os.path.isdir(base): continue
        for s in sorted(os.listdir(base)):
            sk = os.path.join(base, s, "SKILL.md")
            if not os.path.exists(sk): continue
            shipped = subprocess.run(["git", "-C", path, "cat-file", "-e", f"{ref}:{folder}/{s}/SKILL.md"],
                                     capture_output=True).returncode == 0
            r = rows.get(s) or {c: "" for c in COLUMNS}
            if s not in rows:
                r.update(skill=s, genre=genre, plain="todo", learn="todo", anatomy="todo"); added += 1
            r["skill_status"] = "shipped" if shipped else "prototype"
            if not r["summary"]: r["summary"] = frontmatter_summary(sk)
            rows[s] = r
    write_tracker(list(rows.values()))
    print(f"sync: {added} added, {len(rows)} tracked")


# --------------------------------------------------------------------------- stage
def stage(dest):
    import shutil
    rows = read_tracker()
    internal = {os.path.join("skills", r["skill"], f"{k}.html") for r in rows for k, *_ in KINDS if r[k] == "internal"}
    if os.path.exists(dest): shutil.rmtree(dest)
    kept = dropped = 0
    for d, _, files in os.walk(SITE):
        for fn in files:
            if fn == ".DS_Store": continue
            rel = os.path.relpath(os.path.join(d, fn), SITE)
            if rel in internal: dropped += 1; continue
            os.makedirs(os.path.join(dest, os.path.dirname(rel)), exist_ok=True)
            shutil.copy2(os.path.join(d, fn), os.path.join(dest, rel)); kept += 1
    print(f"staged {kept} file(s) to {dest}; left out {dropped} internal page(s)")


# --------------------------------------------------------------------------- main
def main(argv):
    if argv[:1] == ["--stage"]:
        stage(argv[1] if len(argv) > 1 else os.path.join(ROOT, "_site")); return
    if argv[:1] == ["--sync"]:
        if len(argv) < 2: sys.exit("usage: build.py --sync PATH [REF]")
        sync(argv[1], argv[2] if len(argv) > 2 else "mosofin/main"); return
    rows = sorted(read_tracker(), key=sort_key)
    bad = problems(rows)
    if bad:
        print("\n".join("  FAIL  " + b for b in bad)); print(f"\n{len(bad)} problem(s)"); sys.exit(1)
    outs = outputs(rows)
    if argv[:1] == ["--check"]:
        stale = [os.path.relpath(p, ROOT) for p, h in outs.items() if not os.path.exists(p) or open(p).read() != h]
        orphans = [os.path.relpath(os.path.join(SITE, "skills", s, "index.html"), ROOT)
                   for s in (os.listdir(os.path.join(SITE, "skills")) if os.path.isdir(os.path.join(SITE, "skills")) else [])
                   if os.path.join(SITE, "skills", s, "index.html") not in outs
                   and os.path.exists(os.path.join(SITE, "skills", s, "index.html"))]
        for p in stale: print(f"  STALE {p} — run python3 build.py")
        for p in orphans: print(f"  ORPHAN {p} — no tracked explainers for this skill")
        if stale or orphans: sys.exit(1)
        print(f"ok: {len(rows)} skills tracked, {len(outs)} generated pages up to date"); return
    for p, h in outs.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(h)
    print(f"built {len(outs)} page(s) from {len(rows)} tracked skills")

if __name__ == "__main__":
    main(sys.argv[1:])
