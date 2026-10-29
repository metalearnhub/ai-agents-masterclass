"""Link a new post from older posts (RUNBOOK section 15).
Usage: python3 tools/interlink/add_link.py <new-slug> "<new H1>" <get_page_file>... 
Writes tools/interlink/ops.json: {old-slug: {"pid":..., "ops":[...]}} for patch_page. Skips posts that already link it.
Old template: appends to the Keep reading list. New template: appends a <li> to eb_newg (must already exist; otherwise reported)."""
import json,re,math,sys,os
S,T=sys.argv[1],sys.argv[2]
A='style="color:rgba(0,122,102,1);text-decoration:underline"'
L=lambda t,c:math.ceil(len(t)/c)
out={}
for f in sys.argv[3:]:
    raw=open(f).read(); d=json.loads(raw[raw.index('{'):])
    if isinstance(d,list): d=json.loads(d[0]['text'])
    src=d['source']; m=re.search(r'/([a-z0-9-]+)\)$',d['name']); slug=m.group(1) if m else d['name']
    sec=src['page'][1]; kids=sec['children']; ids=[c['id'] for c in kids]
    if S in json.dumps(src): print('skip (already links)',slug); continue
    if 'eb_2120' in ids:
        if 'eb_newg' not in ids: print('NEEDS eb_newg element (new template):',slug); continue
        c=kids[ids.index('eb_newg')]; h=c['specials']['html']
        li=f"<li style='margin:0 0 8px 0;font-size:15px;line-height:1.6'><a href='https://www.dijaedadula.com/{S}' style='color:#007a66;text-decoration:underline;text-underline-offset:2px'>{T}</a></li>"
        h=h.replace('</ul></div>',li+'</ul></div>')
        ad=L(T,74)*24+8; am=L(T,42)*24+8
        ops=[{"op":"update","id":"eb_newg","specials":{"html":h},"styles":{"desktop":{"height":c['responsive']['desktop']['styles']['height']+ad},"mobile":{"height":c['responsive']['mobile']['styles']['height']+am}}}]
        top=c['responsive']['desktop']['styles']['top']
        for x in kids:
            if x is not c and x['responsive']['desktop']['styles'].get('top',0)>top:
                ops.append({"op":"update","id":x['id'],"styles":{"desktop":{"top":x['responsive']['desktop']['styles']['top']+ad},"mobile":{"top":x['responsive']['mobile']['styles']['top']+am}}})
    else:
        k=[i for i,c in enumerate(kids) if re.sub('<[^>]+>','',(c.get('specials') or {}).get('text','')).strip()=='Keep reading'][0]
        lst=kids[k+1]; txt=lst['specials']['text']; cut=txt.find('<a href="https://www.dijaedadula.com/blog"'); assert cut>0,slug
        new=txt[:cut]+f'<b><a href="https://www.dijaedadula.com/{S}" {A}>{T}</a></b><br><br>'+txt[cut:]
        fd=lst['responsive']['desktop']['styles'].get('fontSize',19); fm=lst['responsive']['mobile']['styles'].get('fontSize',17)
        ad=math.ceil((L(T,int(640/(fd*0.55)))+1)*fd*1.6); am=math.ceil((L(T,int(380/(fm*0.55)))+1)*fm*1.6)
        ops=[{"op":"update","id":lst['id'],"specials":{"text":new},"styles":{"desktop":{"height":lst['responsive']['desktop']['styles']['height']+ad},"mobile":{"height":lst['responsive']['mobile']['styles']['height']+am}}}]
        for c in kids[k+2:]:
            ops.append({"op":"update","id":c['id'],"styles":{"desktop":{"top":c['responsive']['desktop']['styles']['top']+ad},"mobile":{"top":c['responsive']['mobile']['styles']['top']+am}}})
    ops.append({"op":"update","id":sec['id'],"styles":{"desktop":{"height":sec['responsive']['desktop']['styles']['height']+ad},"mobile":{"height":sec['responsive']['mobile']['styles']['height']+am}}})
    out[slug]={'pid':d['page_id'],'ops':ops}; print('ok',slug,d['page_id'],'add',ad,am)
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ops.json'),'w'),ensure_ascii=False)
