"""Prove an STE rewrite changed wording only.
usage: ste_verify.py PAGE.html [REF]   (REF = git ref holding the original, default HEAD)
Checks: (1) HTML skeleton identical (tags, attributes, order) outside text; (2) every number/currency/percent/date token
count identical; (3) hrefs and sup cite ids identical; (4) quoted rules (blockquote, q: fields, SOURCE urls) byte-identical;
(5) hedge words (may, might, could, can, usually, often, about, roughly) counts reported if changed."""
import sys,re,subprocess,json,collections
page=sys.argv[1]; ref=sys.argv[2] if len(sys.argv)>2 else 'HEAD'
new=open(page).read()
import os
root=subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()
old=subprocess.run(['git','-C',root,'show',f'{ref}:{os.path.relpath(os.path.abspath(page),root)}'],capture_output=True,text=True).stdout
assert old, 'no original at '+ref
KEYS=r'plain|backed|where_plain|note|desc|w|what|why|result|intro|lede'
PROT=r'q|t|u|formula|where|src|kind|id|cites|tier_id'
def prot(t):
    out=[]
    for m in re.finditer(r'<script>(.*?)</script>',t,re.S):
        out+=re.findall(r'\b(?:'+PROT+r')\s*:\s*(?:"(?:[^"\\]|\\.)*"|\[[^\]]*\])',m.group(1))
    return out
def skeleton(t):
    def js(m): return '<script>'+re.sub(r'"(?:[^"\\]|\\.)*"','"#"',m.group(1))+'</script>'
    t=re.sub(r'<script>(.*?)</script>',js,t,flags=re.S)
    return re.sub(r'>[^<]*<','><',t)
def jsq(t): return re.findall(r'\bq\s*:\s*"((?:[^"\\]|\\.)*)"',t)
def bq(t): return re.findall(r'<blockquote.*?</blockquote>',t,re.S)
def vis(t):
    t=re.sub(r'<(script|style)\b.*?</\1>',lambda m:m.group(0) if m.group(1)=='script' else '',t,flags=re.S)
    t=re.sub(r'<svg.*?</svg>','',t,flags=re.S)
    t=re.sub(r'<[^>]+>',' ',t); import html; return html.unescape(t)
NUM=re.compile(r'[£$€]?\d[\d,]*(?:\.\d+)?%?')
def nums(t): return collections.Counter(NUM.findall(vis(t)))
HEDGE=re.compile(r'\b(may|might|could|can|usually|often|about|roughly|generally|most|some|typically)\b',re.I)
def hedges(t): return collections.Counter(w.lower() for w in HEDGE.findall(vis(t)))
bad=[]
if skeleton(old)!=skeleton(new): bad.append('HTML skeleton/attributes changed (structure, ids, classes or hrefs differ)')
if prot(old)!=prot(new): bad.append('a protected script field changed (q, t, u, formula, where, src, cites ...)')
if jsq(old)!=jsq(new): bad.append('a quoted rule (q:) changed')
if bq(old)!=bq(new): bad.append('a <blockquote> changed')
if re.findall(r'href="[^"]+"',old)!=re.findall(r'href="[^"]+"',new): bad.append('hrefs changed')
if re.findall(r'\bu:"[^"]+"',old)!=re.findall(r'\bu:"[^"]+"',new): bad.append('source URLs changed')
no,nn=nums(old),nums(new)
if no!=nn:
    d={k:(no[k],nn[k]) for k in set(no)|set(nn) if no[k]!=nn[k]}
    bad.append('number tokens differ (old,new): '+json.dumps(d,ensure_ascii=False))
ho,hn=hedges(old),hedges(new)
note=''
if ho!=hn:
    note='hedge-word counts changed (review): '+json.dumps({k:(ho[k],hn[k]) for k in set(ho)|set(hn) if ho[k]!=hn[k]})
print(('FAIL ' if bad else 'OK   ')+page)
for b in bad: print('   -',b)
if note: print('   ~',note)
sys.exit(1 if bad else 0)
