"""Add a 'Transparency' link to the footer nav of a page.
Usage: python3 tools/footer_link.py <get_page_result_file> [out.json]
Finds the text element whose links include Threads/YouTube in the dark footer and appends ' · Transparency'."""
import json,sys,re
from _load import load_source
raw=open(sys.argv[1]).read()
try: src=load_source(sys.argv[1])
except Exception:
    d=json.loads(raw[raw.index('{'):]); src=d['source']
L='https://www.dijaedadula.com/transparency'
hits=[]
def walk(n):
    if isinstance(n,dict):
        t=n.get('specials',{}).get('text') if isinstance(n.get('specials'),dict) else None
        if t and 'threads.com/@dijaedadula' in t and 'Book a call' in t: hits.append(n)
        for v in n.values(): walk(v)
    elif isinstance(n,list):
        for v in n: walk(v)
walk(src['page'])
out=[]
for n in hits:
    t=n['specials']['text']
    if '/transparency' in t: continue
    m=re.findall(r'<a href="https://www\.threads\.com/@dijaedadula"( style="[^"]*")?>Threads</a>',t)
    if not m: print('NOMATCH',n['id'],t[-200:]); continue
    st=m[-1]
    t2=re.sub(r'(<a href="https://www\.threads\.com/@dijaedadula"[^>]*>Threads</a>)',r'\1 · <a href="%s"%s>Transparency</a>'%(L,st),t,count=1)
    out.append({"op":"update","id":n['id'],"specials":{"text":t2}})
print(json.dumps({"name":None,"ids":[o['id'] for o in out]}))
if len(sys.argv)>2: json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
