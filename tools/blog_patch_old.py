"""Add a post to the top of the /blog list (page 51cab93b-210b-4516-aa6f-f7f94c533eb6).
Usage: python3 tools/blog_patch.py <get_page_result.json> <slug> "<full H1 title>" "<one-sentence blurb>"
Writes blog_patch.json -> patch_page(page_id, patches=<contents>, dry_run=false), then publish_page(custom_path='blog')."""
import json,math,sys
from _load import load_source
src=load_source(sys.argv[1]); slug,title,blurb=sys.argv[2:5]
A='style="color:rgba(0,122,102,1);text-decoration:underline"'
sec=[s for s in src['page'] if s['id']=='sec_0237'][0]; k={c['id']:c for c in sec['children']}
txt=k['t_0240']['specials']['text']
if '/'+slug+'"' in txt: sys.exit('already listed')
mk='.<br><br>'; i=txt.index(mk)+len(mk)
new=txt[:i]+f'<b><a href="https://www.dijaedadula.com/{slug}" {A}>{title}</a></b><br>{blurb}<br><br>'+txt[i:]
L=lambda t,c:math.ceil(len(t)/c)
ad=math.ceil((L(title,58)+L(blurb,68)+1)*19*1.65*0.8); am=math.ceil((L(title,36)+L(blurb,42)+1)*17*1.65*0.9)
g=lambda e,bp,key:e['responsive'][bp]['styles'][key]
P=[{"op":"update","id":"t_0240","specials":{"text":new},"styles":{"desktop":{"height":g(k['t_0240'],'desktop','height')+ad},"mobile":{"height":g(k['t_0240'],'mobile','height')+am}}},
 {"op":"update","id":"t_0241","styles":{"desktop":{"top":g(k['t_0241'],'desktop','top')+ad},"mobile":{"top":g(k['t_0241'],'mobile','top')+am}}},
 {"op":"update","id":"sec_0237","styles":{"desktop":{"height":g(sec,'desktop','height')+ad},"mobile":{"height":g(sec,'mobile','height')+am}}}]
json.dump(P,open('blog_patch.json','w'),ensure_ascii=False); print('added',ad,am)
