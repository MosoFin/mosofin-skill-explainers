#!/usr/bin/env python3
# Pulls the visible prose of an explainer page, one block per line, so the ASD-STE100 linter can score it.
# Skips scripts, styles, svg, code and every blockquote (quoted skill rules stay word for word).
# usage: python3 -I ste_extract.py site/skills/<skill>/<kind>.html > /tmp/page.txt
import sys,re,html,json
from html.parser import HTMLParser
BLOCK={'p','li','h1','h2','h3','h4','div','section','header','footer','td','th','figcaption','span','blockquote','label','summary','dd','dt','tr','br'}
SKIP={'script','style','svg','code','pre','blockquote','cite','title'}   # blockquote = verbatim skill rules
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.cur=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in SKIP: s.skip+=1
        if t in BLOCK: s.flush()
    def handle_endtag(s,t):
        if t in SKIP and s.skip: s.skip-=1
        if t in BLOCK: s.flush()
    def handle_data(s,d):
        if not s.skip: s.cur.append(d)
    def flush(s):
        x=re.sub(r'\s+',' ',''.join(s.cur)).strip()
        if x: s.out.append(x)
        s.cur=[]
def extract(path):
    t=open(path).read()
    p=P(); p.feed(t); p.flush()
    blocks=p.out
    # JS string fields that are visible prose (learn page)
    for m in re.finditer(r'\b(plain|backed|where_plain|note|desc|w|what|why|result|intro|lede)\s*:\s*"((?:[^"\\]|\\.)*)"',t):
        k=m.group(1)
        if k=='w' and re.match(r'^(references|SKILL)',m.group(2)): continue
        try: v=json.loads('"'+m.group(2)+'"')
        except Exception: continue
        v=re.sub(r'<[^>]+>','',v)
        if len(v.split())>3: blocks.append(re.sub(r'\s+',' ',v).strip())
    # de-duplicate keeping order
    seen=set(); res=[]
    for b in blocks:
        if b not in seen and len(b.split())>=3: seen.add(b); res.append(b)
    return res
if __name__=='__main__':
    for b in extract(sys.argv[1]): print(b+'\n')
