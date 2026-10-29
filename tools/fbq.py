"""Facebook queue (shares the post list in newsletter/queue.json). See SOCIAL.md.
  python3 tools/fbq.py next                                   -> oldest blog post not yet on Facebook (backlog), JSON or {"none":true}
  python3 tools/fbq.py done <slug>                            -> exit 0 if the slug is already posted/scheduled on Facebook, 1 if not
  python3 tools/fbq.py mark YYYY-MM-DD <slug> "<info>" [fb_url] [image_url]
  python3 tools/fbq.py seturl <slug> <fb_url>                 -> fill the Facebook link once a scheduled post has published
  python3 tools/fbq.py pending                                -> entries still missing a Facebook link (scheduled, not yet published)"""
import json,sys,os
F=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'newsletter','queue.json')
q=json.load(open(F)); q.setdefault('fb',[]); done={x['slug'] for x in q['fb']}
a=sys.argv[1]
def save(): json.dump(q,open(F,'w'),indent=1,ensure_ascii=False)
if a=='next':
    n=[p for p in q['posts'] if p['slug'] not in done]; print(json.dumps(n[0] if n else {"none":True},indent=1,ensure_ascii=False))
elif a=='done':
    sys.exit(0 if sys.argv[2] in done else 1)
elif a=='mark':
    e={'date':sys.argv[2],'slug':sys.argv[3],'info':sys.argv[4] if len(sys.argv)>4 else '','url':sys.argv[5] if len(sys.argv)>5 else ''}
    if len(sys.argv)>6: e['image']=sys.argv[6]
    q['fb'].append(e); save(); print('marked',sys.argv[3])
elif a=='seturl':
    for x in q['fb']:
        if x['slug']==sys.argv[2]: x['url']=sys.argv[3]
    save(); print('ok')
elif a=='pending':
    print(json.dumps([x for x in q['fb'] if not x.get('url')],indent=1,ensure_ascii=False))
