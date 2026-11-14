"""Community queue. python3 tools/community/cq.py next group|ig  -> next item (JSON) or {"none":true}
python3 tools/community/cq.py mark group|ig <slug> <url> <YYYY-MM-DD>
python3 tools/community/cq.py sync   -> append new page posts from newsletter/queue.json fb list"""
import json,sys,os
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'queue.json')
q=json.load(open(F))
def save(): json.dump(q,open(F,'w'),indent=1,ensure_ascii=False)
a=sys.argv[1]
if a=='next':
    ch=sys.argv[2]; done={x['slug'] for x in q[ch]}
    n=[i for i in q['items'] if i['slug'] not in done]
    print(json.dumps(n[0] if n else {"none":True},indent=1,ensure_ascii=False))
elif a=='mark':
    ch,s,u,d=sys.argv[2:6]; q[ch].append({'slug':s,'url':u,'date':d}); save(); print('marked',ch,s)
elif a=='sync':
    base=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fbq=json.load(open(os.path.join(base,'newsletter','queue.json')))['fb']
    have={i['slug'] for i in q['items']}
    try: cb={f['slug']:f for f in json.load(open('/home/claude/cvl/assets/content-bank/posts.json'))['facebook']}
    except Exception: cb={}
    for x in sorted(fbq,key=lambda e:e['date']):
        if x['slug'] not in have:
            q['items'].append({'slug':x['slug'],'date':x['date'],'page_post':x.get('url',''),'blog':'https://www.dijaedadula.com/'+x['slug'],'page_text':cb.get(x['slug'],{}).get('message','')})
    save(); print('items',len(q['items']))
