#!/usr/bin/env python3
"""Prove that a card-format split moved the original text and lost nothing. Read-only.

usage: python3 -I split_proof.py <original SKILL.md> <skill folder after the split>

1. Every non-blank line of the original appears in the card or the references, as many times as before.
   Lines that do not are listed. Expect exactly two: the frontmatter description (rewritten for the card)
   and the shared/onboarding.md link (one more ../ for the new depth). Any other line is a loss.
2. Every section between two headings of the original (shared blocks aside) appears contiguous, byte for
   byte, in one reference file.
3. Every relative link in the folder resolves.
Exit 1 if a section is missing or a link is broken."""
import collections, glob, os, re, sys

orig, folder = sys.argv[1], sys.argv[2]
L = open(orig).read().split("\n")
files = [os.path.join(folder, "SKILL.md")] + sorted(glob.glob(os.path.join(folder, "references", "*.md")))
texts = {f: open(f).read() for f in files}
have = collections.Counter(l.rstrip() for t in texts.values() for l in t.split("\n"))
need = collections.Counter(l.rstrip() for l in L)
content = [l for l in L if l.strip()]
missing = [(i, l) for i, l in enumerate(L, 1) if l.strip() and have[l.rstrip()] < need[l.rstrip()]]
print(f"content lines kept: {len(content) - len(missing)} of {len(content)}")
for i, l in missing: print(f"  not found, line {i}: {l[:100]}")

refs = "\n".join(t for f, t in texts.items() if "/references/" in f)
heads = [i for i, l in enumerate(L) if re.match(r"^#{1,3} ", l)]
bad = 0
for a, b in zip(heads, heads[1:] + [len(L)]):
    block = "\n".join(L[a:b]).strip("\n")
    while block.endswith("---") or block.endswith("\n"): block = block.rstrip("-").rstrip("\n")
    if "<!-- shared" in block or not block: continue
    if block not in refs: bad += 1; print(f"  section not contiguous: {L[a][:80]}")
print(f"sections checked: {len(heads)}, not contiguous: {bad}")

broken = 0
for f, t in texts.items():
    for p in re.findall(r"\]\((\.{0,2}/?[^)#:]+\.md)", t):
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), p))): broken += 1; print(f"  broken link in {f}: {p}")
print(f"broken links: {broken}")
sys.exit(1 if bad or broken else 0)
