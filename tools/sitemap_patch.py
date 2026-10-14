"""Add a post to the /sitemap page (page e103c11c-eedf-40ff-802c-bc35bc7e6d81) and to sitemap.xml.
Usage: python3 tools/sitemap_patch.py <get_page_result.json> "<group>" <slug> "<short title>" "<short blurb>" <YYYY-MM-DD>
Groups: "AI agents and chatbots" | "Sales and lead automation" | "Case studies" | "Careers and income in the AI era"
Writes sitemap_patch.json -> patch_page(..., dry_run=false), then publish_page(custom_path='sitemap'). Updates ../sitemap.xml in place."""
import json,math,sys,os,re
from _load import load_source
src=load_source(sys.argv[1]); group,slug,title,blurb,date=sys.argv[2:7]
A='style="color:rgba(0,122,102,1);text-decoration:underline"'
body=[s for s in src['page'] if s['id']=='sec_2308'][0]; kids=body['children']
h=[c for c in kids if c['id'].startswith('t_23h') and c['specials']['text']==group]
if not h: sys.exit('group not found: '+group)
n=h[0]['id'][-1]; lst=[c for c in kids if c['id']=='t_23l'+n][0]
txt=lst['specials']['text']
if '/'+slug+'"' in txt: sys.exit('already listed')
txt+=f'<br><br><b><a href="https://www.dijaedadula.com/{slug}" {A}>{title}</a></b><br>{blurb}'
L=lambda t,c:math.ceil(len(t)/c)
ad=math.ceil((L(title,60)+L(blurb,68)+1)*17*1.6); am=math.ceil((L(title,36)+L(blurb,42)+1)*16*1.6)
P=[]; lt={bp:lst['responsive'][bp]['styles']['top'] for bp in ('desktop','mobile')}
for c in kids:
    st={}
    for bp,add in (('desktop',ad),('mobile',am)):
        s=c['responsive'][bp]['styles']
        if c is lst: st[bp]={'height':s['height']+add}
        elif s['top']>lt[bp]: st[bp]={'top':s['top']+add}
    if st:
        op={"op":"update","id":c['id'],"styles":st}
        if c is lst: op['specials']={"text":txt}
        P.append(op)
P.append({"op":"update","id":"sec_2308","styles":{bp:{"height":body['responsive'][bp]['styles']['height']+add} for bp,add in (('desktop',ad),('mobile',am))}})
json.dump(P,open('sitemap_patch.json','w'),ensure_ascii=False)
x=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'sitemap.xml'); s=open(x).read()
if '/'+slug+'<' not in s:
    s=s.replace('</urlset>',f'  <url><loc>https://www.dijaedadula.com/{slug}</loc><lastmod>{date}</lastmod></url>\n</urlset>')
    s=re.sub(r'(dijaedadula\.com/(?:blog|sitemap)</loc><lastmod>)[\d-]+',r'\g<1>'+date,s); open(x,'w').write(s)
print('added',ad,am,len(P),'ops')
