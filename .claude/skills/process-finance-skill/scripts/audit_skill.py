#!/usr/bin/env python3
"""First-pass audit of one finance skill, before a rewrite. Read-only.

usage: python3 -I audit_skill.py <path to mosofin-finance-skills> <skill> [git ref, default: working tree]

Reports what every earlier rewrite had to fix: size against the 500-line guide, references to skills that
are not in the library, the description length against the 1,024-character limit, sandbox-only paths,
the tool names the skill uses, verdict counts, and the section map that the card split will follow.
It finds candidates. A person reads each one in context before changing anything."""
import os, re, subprocess, sys

repo, skill = sys.argv[1], sys.argv[2]
ref = sys.argv[3] if len(sys.argv) > 3 else None
path = f"skills/{skill}/SKILL.md"
if ref:
    text = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"], capture_output=True, text=True, check=True).stdout
else:
    text = open(os.path.join(repo, path)).read()
lines = text.split("\n")
if lines and lines[-1] == "": lines.pop()   # a trailing newline is not a line
library = set(os.listdir(os.path.join(repo, "skills"))) | set(os.listdir(os.path.join(repo, "dashboards")))
card = os.path.isdir(os.path.join(repo, "skills", skill, "references"))

print(f"== {skill}  ({'card format' if card else 'one file'}{', ' + ref if ref else ''})")
print(f"SKILL.md lines: {len(lines)}  (guide: under 500)")
m = re.search(r'^description:\s*"(.*)"\s*$', text, re.M)
d = m.group(1) if m else ""
print(f"description: {len(d)} characters  (limit: 1,024){'  OVER' if len(d) > 1024 else ''}")

print("\nreferences to other skills (backticked names):")
seen = {}
for i, l in enumerate(lines, 1):
    for name in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", l):
        if name == skill or re.match(r"(search|get|list|invoke|create)[_-]", name): continue
        seen.setdefault(name, []).append(i)
for name, at in sorted(seen.items()):
    print(f"  {'in library ' if name in library else 'NOT IN LIBRARY'}  {name}  lines {','.join(map(str, at))}")

print("\nsandbox-only paths:", [i for i, l in enumerate(lines, 1) if "/mnt/" in l] or "none")
tools = sorted(set(re.findall(r"`((?:search|get|list|invoke|create)[_-][a-z_-]+)`", text)))
workflow = {"list_workspaces", "get_agent_datasources", "get_datasource_tools", "invoke_datasource_api_tool", "get_skills", "get_my_skill", "create_skill"}
print(f"\nMosofin workflow tools: {sorted(set(tools) & workflow)}")
print(f"evidence tools named ({len(set(tools) - workflow)}): {sorted(set(tools) - workflow)}")
print("verdicts [auto] [gated] [manual]:", [len(re.findall(r"\[" + v + r"\]", text)) for v in ("auto", "gated", "manual")])

print("\nsection map (the card split follows these headings):")
for i, l in enumerate(lines, 1):
    if re.match(r"^#{1,2} ", l) or "<!-- shared:" in l:
        print(f"  {i:5}  {l[:90]}")
