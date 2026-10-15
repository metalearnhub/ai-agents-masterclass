"""Weekly Facebook post queue (oldest blog post first, 1 per week). Shares the post list in newsletter/queue.json.
  python3 tools/fbq.py next                          -> next unposted blog post (JSON)
  python3 tools/fbq.py mark YYYY-MM-DD <slug> <scheduledPostInfo>"""
import json,sys,os
F=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'newsletter','queue.json')
q=json.load(open(F)); q.setdefault('fb',[]); done={x['slug'] for x in q['fb']}
if sys.argv[1]=='next':
    n=[p for p in q['posts'] if p['slug'] not in done]; print(json.dumps(n[0] if n else {"none":True},indent=1,ensure_ascii=False))
elif sys.argv[1]=='mark':
    q['fb'].append({'date':sys.argv[2],'slug':sys.argv[3],'info':sys.argv[4] if len(sys.argv)>4 else ''}); json.dump(q,open(F,'w'),indent=1,ensure_ascii=False); print('marked')
