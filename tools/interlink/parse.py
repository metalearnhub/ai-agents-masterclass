import json,glob,re,os
R='/root/.claude/projects/-home-claude/a0ddebc3-1c9f-5dc3-9d51-6b734607f315/tool-results/'
out={}
for f in sorted(glob.glob(R+'mcp-Webcake-get_page-17931002*.txt')+glob.glob(R+'mcp-Webcake-get_page-17931003*.txt')):
    raw=open(f).read()
    try: d=json.loads(raw[raw.index('{'):])
    except Exception as e:
        # maybe wrapped
        print('fail',f,e); continue
    if 'source' not in d: print('nosrc',f); continue
    src=d['source']; pid=d['page_id']; name=d['name']
    m=re.search(r'/([a-z0-9-]+)\)$',name); slug=m.group(1) if m else name
    if 'Blog Post' not in name: continue
    info={'file':f,'pid':pid,'slug':slug,'version':d.get('source_version')}
    for si,sec in enumerate(src['page']):
        for c in sec.get('children',[]):
            h=(c.get('specials') or {}).get('html','')
            if c['type']=='editor-blog' and 'dd-article' in h:
                info['sec']=sec['id']; info['eb']=c['id']
                info['eb_d']=c['responsive']['desktop']['styles']; info['eb_m']=c['responsive']['mobile']['styles']
                info['sec_h']=[sec['responsive']['desktop']['styles']['height'],sec['responsive']['mobile']['styles']['height']]
                info['links']=sorted(set(re.findall(r"dijaedadula\.com/([a-z0-9-]+)",h)))
                info['after']=[(x['id'],x['type'],x['responsive']['desktop']['styles'].get('top'),x['responsive']['mobile']['styles'].get('top')) for x in sec['children'] if x is not c and x['responsive']['desktop']['styles'].get('top',0)>c['responsive']['desktop']['styles']['top']]
                info['ids']=[x['id'] for x in sec['children']]
    out[slug]=info
json.dump(out,open('pages.json','w'),indent=1)
for s,i in out.items():
    print(s, i.get('eb'), i.get('sec'), i.get('sec_h'), i.get('eb_d',{}).get('top'),i.get('eb_d',{}).get('height'), i.get('eb_m',{}).get('top'),i.get('eb_m',{}).get('height'), i.get('after'))
print(len(out))
