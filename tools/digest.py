"""Friday digest queue (oldest first). Usage:
  python3 tools/digest.py next                       -> the next 3 unsent posts (JSON)
  python3 tools/digest.py mark YYYY-MM-DD <broadcastId> -> record those 3 as sent/scheduled in that digest
  python3 tools/digest.py last                       -> the 3 posts of the most recent digest (for the Tuesday email)
  python3 tools/digest.py add <slug> "<title>" "<blurb>" -> append a newly published post (daily run)"""
import json,sys,os
F=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'newsletter','queue.json')
q=json.load(open(F)); done={s for d in q['sent'] for s in d['slugs']}
cmd=sys.argv[1]
if cmd=='next':
    print(json.dumps([p for p in q['posts'] if p['slug'] not in done][:3],indent=1,ensure_ascii=False))
elif cmd=='mark':
    nxt=[p['slug'] for p in q['posts'] if p['slug'] not in done][:3]
    q['sent'].append({'date':sys.argv[2],'broadcastId':sys.argv[3],'slugs':nxt}); json.dump(q,open(F,'w'),indent=1,ensure_ascii=False); print('marked',nxt)
elif cmd=='last':
    last=q['sent'][-1]; by={p['slug']:p for p in q['posts']}
    print(json.dumps({'date':last['date'],'posts':[by[s] for s in last['slugs']]},indent=1,ensure_ascii=False))
elif cmd=='add':
    s,t,b=sys.argv[2:5]
    if s not in {p['slug'] for p in q['posts']}: q['posts'].append({'slug':s,'title':t,'blurb':b}); json.dump(q,open(F,'w'),indent=1,ensure_ascii=False)
    print('queue length',len(q['posts']))
