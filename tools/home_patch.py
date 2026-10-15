"""Put a new post at the top of "Latest from the blog" on /home (page e4442f32-e964-4556-9573-02beece9a76e, element t_home_ll).
Keeps the 7 newest posts plus "See all posts on the blog", so the element height stays the same.
Usage: python3 tools/home_patch.py <get_page_result_file> <slug> "<full H1 title>"
get_page on /home is large: the tool saves it to a file; pass that file path.
Writes home_patch.json -> patch_page(page_id, patches=<contents>, dry_run=false), then publish_page(custom_domain www.dijaedadula.com, custom_path home)."""
import json,re,sys
from _load import load_source
raw=open(sys.argv[1]).read()
try: src=load_source(sys.argv[1])
except Exception: d=json.loads(raw[raw.index('{'):]); src=d['source']
slug,title=sys.argv[2:4]
A='style="color:rgba(0,122,102,1);text-decoration:underline"'
def find(n):
    if n.get('id')=='t_home_ll': return n
    for c in n.get('children',[]):
        r=find(c)
        if r: return r
el=None
for s in src['page']:
    el=find(s) or el
txt=el['specials']['text']
links=re.findall(r'<a href="https://www\.dijaedadula\.com/([^"]+)"[^>]*>(.*?)</a>',txt)
links=[(s,t) for s,t in links if s!='blog' and s!=slug]
links=[(slug,title)]+links[:6]
new='<br>'.join(f'<a href="https://www.dijaedadula.com/{s}" {A}>{t}</a>' for s,t in links)+f'<br><a href="https://www.dijaedadula.com/blog" {A}>See all posts on the blog</a>'
json.dump([{"op":"update","id":"t_home_ll","specials":{"text":new}}],open('home_patch.json','w'),ensure_ascii=False)
print('home list:',[s for s,_ in links])
