"""Mirror the blog content calendar into the content bank (cvl crm/content-bank/posts.json -> "blog").
Usage: python3 tools/calendar_bank.py [cvl_path]   (default /home/claude/cvl). Run after every checklist change, then commit+push cvl.
Planned posts that need no recording get consecutive daily dates from tomorrow (Manila) in queue order, matching checklist.py next."""
import openpyxl,json,os,sys,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CVL=sys.argv[1] if len(sys.argv)>1 else '/home/claude/cvl'
wb=openpyxl.load_workbook(os.path.join(K,'checklist','Blog content checklist.xlsx'))
today=(datetime.datetime.utcnow()+datetime.timedelta(hours=8)).date()
out=[];queue=[]
for ti,tab in enumerate(['Website Blog Plan','Botcake Series']):
    ws=wb[tab];hdr={ws.cell(4,c).value:c for c in range(1,ws.max_column+1)}
    for r in range(5,ws.max_row+1):
        if ws.cell(r,1).value is None: continue
        v={k:ws.cell(r,c).value for k,c in hdr.items()}
        rec=str(v.get('Screen recording needed from Dijae') or '')
        notes=str(v.get('Notes') or '')
        series='GEO' if 'GEO' in notes or 'GEO' in str(v.get('Why it wins / funnel role') or '') else 'Expert data' if 'xpert data' in notes+str(v.get('Why it wins / funnel role') or '') else ''
        e={'tab':tab,'num':v['#'],'title':v['Working title'],'stage':v.get('Funnel stage') or '','keyword':v.get('Main search target') or '','series':series}
        if v['Status']=='Published':
            d=v.get('Publish date'); e.update(status='published',date=d.strftime('%Y-%m-%d') if hasattr(d,'strftime') else str(d or ''),url=v.get('Blog URL') or '')
            out.append(e)
        elif v['Status']=='Planned':
            rank=0 if rec.startswith('No') else 1 if rec.startswith('Optional') else None
            if rank is None: e.update(status='hold',date='',note='Needs a screen recording from Dijae'); out.append(e)
            else: queue.append((rank,ti,v['Priority order'] or 999,e))
queue.sort(key=lambda x:x[:3])
for i,(_,_,_,e) in enumerate(queue):
    e.update(status='planned',date=(today+datetime.timedelta(days=1+i)).isoformat()); out.append(e)
p=os.path.join(CVL,'crm','content-bank','posts.json'); d=json.load(open(p))
d['blog']=out; d['updated']=today.isoformat(); json.dump(d,open(p,'w'),indent=1,ensure_ascii=False)
print('blog entries',len(out),'planned',len(queue),'published',sum(1 for e in out if e['status']=='published'),'hold',sum(1 for e in out if e['status']=='hold'))
