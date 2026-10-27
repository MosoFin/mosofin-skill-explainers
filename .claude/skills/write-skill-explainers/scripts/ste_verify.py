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
def cites(t):
    return collections.Counter(re.findall(r'C\((\d+(?:,\d+)*)\)',t))
def mask_js(code):
    """Keep script code exactly; blank out prose only: quoted strings, and the text between tags and ${...} in template literals."""
    out=[]; i=0; n=len(code)
    def string(i,q):
        j=i+1
        while j<n and code[j]!=q:
            j+=2 if code[j]=='\\' else 1
        if j>=n: raise ValueError('unterminated string')
        return j+1
    def template(i):                      # code[i]=='`'; returns (end, masked text)
        j=i+1; res=['`']; text=False
        while True:
            if j>=n: raise ValueError('unterminated template')
            c=code[j]
            if c=='`': res.append('`'); return j+1,''.join(res)
            if c=='\\': text=True; j+=2; continue
            if c=='$' and code[j+1:j+2]=='{':
                text=False
                depth=1; k=j+2
                while depth:
                    if k>=n: raise ValueError('unterminated expression')
                    d=code[k]
                    if d in '"\'': k=string(k,d); continue
                    if d=='`': k,_=template(k); continue
                    depth+= (d=='{')-(d=='}'); k+=1
                res.append('${'+mask_js(code[j+2:k-1])+'}'); j=k; continue
            if c=='<':
                text=False
                k=code.find('>',j); k=n if k<0 else k+1
                res.append(code[j:k]); j=k; continue
            text=True; j+=1
    while i<n:
        c=code[i]
        if c=='/' and code[i+1:i+2]=='/':
            k=code.find('\n',i); k=n if k<0 else k; out.append(code[i:k]); i=k
        elif c=='/' and code[i+1:i+2]=='*':
            k=code.find('*/',i); k=n if k<0 else k+2; out.append(code[i:k]); i=k
        elif c in '"\'':
            i=string(i,c); out.append(c+'#'+c)
        elif c=='`':
            i,seg=template(i); out.append(seg)
        else: out.append(c); i+=1
    return ''.join(out)
def skeleton(t):
    codes=[]
    def js(m):
        c=mask_js(m.group(1))
        c=re.sub(r'(?:\+\s*)?C\(\d+(?:,\d+)*\)(?:\s*\+)?','',c)       # cite markers: adding is fine, removing is caught by cites()
        c=re.sub(r'(?:"#"\s*){2,}','"#"',c)                                # a string split in two is still one string
        codes.append(c); return '<script></script>'
    t=re.sub(r'<script>(.*?)</script>',js,t,flags=re.S)
    return re.sub(r'>[^<]*<','><',t)+'\n@@CODE@@\n'+'\n@@\n'.join(codes)   # HTML text may change; script code may not
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
co,cn=cites(old),cites(new)
lost={k:(co[k],cn[k]) for k in co if cn[k]<co[k]}
if lost: bad.append('cite markers C(n) removed (old,new): '+json.dumps(lost))
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
