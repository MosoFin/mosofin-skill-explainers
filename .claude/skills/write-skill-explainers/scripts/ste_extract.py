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

PROTECTED=('q','t','u','formula','where','src','kind','id','type','cites','chips')
def js_prose(code):
    """Prose a reader sees that lives in script code: quoted strings and the text of template literals (${...} becomes N)."""
    found=[]; n=len(code)
    def string(i,q):
        j=i+1
        while j<n and code[j]!=q: j+=2 if code[j]=='\\' else 1
        return j+1
    def template(i):
        j=i+1; buf=[]
        while j<n and code[j]!='`':
            c=code[j]
            if c=='\\': buf.append(code[j+1:j+2]); j+=2
            elif c=='$' and code[j+1:j+2]=='{':
                d=1; k=j+2
                while d and k<n:
                    if code[k] in '"\'': k=string(k,code[k]); continue
                    if code[k]=='`': k,_=template(k); continue
                    d+=(code[k]=='{')-(code[k]=='}'); k+=1
                buf.append('N'); j=k
            elif c=='<':
                k=code.find('>',j); k=n if k<0 else k+1; buf.append(' '); j=k
            else: buf.append(c); j+=1
        return j+1,''.join(buf)
    i=0
    while i<n:
        c=code[i]
        if c=='/' and code[i+1:i+2]=='/': k=code.find('\n',i); i=n if k<0 else k
        elif c=='/' and code[i+1:i+2]=='*': k=code.find('*/',i); i=n if k<0 else k+2
        elif c in '"\'':
            j=string(i,c); text=code[i+1:j-1]
            key=re.search(r'(\w+)\s*:\s*$',code[max(0,i-30):i])
            if not (key and key.group(1) in PROTECTED): found.append(text)
            i=j
        elif c=='`':
            i,text=template(i); found.append(text)
        else: i+=1
    out=[]
    for f in found:
        f=re.sub(r'\{\d+(?:,\d+)*\}','',f)   # inline cite tokens such as {3}
        f=re.sub(r'<[^>]+>','',f.replace('\\n',' ')); f=re.sub(r'\s+',' ',f).strip()
        if len(f.split())>=4 and re.search(r'[A-Za-z]{3}',f) and not re.search(r'[{};=]|=>|\.querySelector',f): out.append(f)
    return out
def extract(path):
    t=open(path).read()
    p=P(); p.feed(t); p.flush()
    blocks=p.out
    for m in re.finditer(r'<script>(.*?)</script>',t,re.S): blocks+=js_prose(m.group(1))
    # (older field-name pass kept below; duplicates are removed)
    # JS string fields that are visible prose (learn page)
    for m in re.finditer(r'\b(plain|backed|where_plain|note|desc|w|what|why|result|intro|lede)\s*:\s*"((?:[^"\\]|\\.)*)"',t):
        k=m.group(1)
        if k=='w' and re.match(r'^(references|SKILL)',m.group(2)): continue
        try: v=json.loads('"'+m.group(2)+'"')
        except Exception: continue
        v=re.sub(r'<[^>]+>','',re.sub(r'\{\d+(?:,\d+)*\}','',v))   # drop inline cite tokens such as {3}
        if len(v.split())>3: blocks.append(re.sub(r'\s+',' ',v).strip())
    # de-duplicate keeping order
    seen=set(); res=[]
    for b in blocks:
        if b not in seen and len(b.split())>=3: seen.add(b); res.append(b)
    return res
if __name__=='__main__':
    for b in extract(sys.argv[1]): print(b+'\n')
