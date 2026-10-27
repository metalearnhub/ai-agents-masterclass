import json,re,math,subprocess,os
P=json.load(open('pages.json'))
T={p['slug']:p['title'] for p in json.load(open('/home/claude/autopilot/pages/blog/list.json'))['posts']}
M={
'what-is-an-ai-agent':['mcp-ai-agent-business-tools','rag-ai-agent-business-knowledge','ai-agent-instructions-template'],
'turn-skills-into-ai-income':['price-ai-automation-services','filipino-freelancers-ai-clients-abroad','blog-traffic-to-chat-leads'],
'dont-automate-chaos':['rag-ai-agent-business-knowledge','chatbot-roi-metrics','ai-chatbot-human-handoff'],
'ai-chatbot-for-small-business':['ai-chatbot-cost','chatrace-vs-chatbotbuilder','rag-ai-agent-business-knowledge'],
'automate-lead-follow-up':['blog-traffic-to-chat-leads','chatbot-sound-human','facebook-messenger-missed-messages'],
'get-more-clients-with-ai':['blog-traffic-to-chat-leads','price-ai-automation-services','filipino-freelancers-ai-clients-abroad'],
'what-does-an-ai-trainer-do':['how-to-become-an-ai-trainer','filipino-freelancers-ai-clients-abroad','price-ai-automation-services'],
'easypc-ai-lead-qualification-case-study':['ai-chatbot-human-handoff','chatbot-roi-metrics','facebook-messenger-missed-messages'],
'pancake-vs-botcake-vs-manychat':['botcake-ai-pancake-setup-guide','chatrace-vs-chatbotbuilder','ai-chatbot-cost'],
'how-to-test-an-ai-chatbot':['rag-ai-agent-business-knowledge','ai-chatbot-human-handoff','chatbot-sound-human'],
'what-is-mcp':['mcp-ai-agent-business-tools','rag-ai-agent-business-knowledge','ai-agent-instructions-template'],
'ai-chatbot-platforms-philippines':['chatrace-vs-chatbotbuilder','ai-chatbot-cost','botcake-ai-pancake-setup-guide'],
'ai-chatbot-for-resorts-hotels-philippines':['ai-chatbot-human-handoff','facebook-messenger-missed-messages','rag-ai-agent-business-knowledge'],
'qualify-leads-messenger-automatically':['blog-traffic-to-chat-leads','facebook-messenger-missed-messages','ai-chatbot-human-handoff'],
'live-selling-automation-philippines':['stop-bogus-cod-orders','botcake-ai-pancake-setup-guide','facebook-messenger-missed-messages'],
'how-to-become-an-ai-trainer':['filipino-freelancers-ai-clients-abroad','price-ai-automation-services'],
'filipino-freelancers-ai-clients-abroad':['price-ai-automation-services','blog-traffic-to-chat-leads','mcp-ai-agent-business-tools'],
'botcake-ai-pancake-setup-guide':['chatbot-sound-human','ai-chatbot-human-handoff','rag-ai-agent-business-knowledge'],
'price-ai-automation-services':['ai-chatbot-cost','chatbot-roi-metrics','mcp-ai-agent-business-tools'],
'chatbot-roi-metrics':['ai-chatbot-cost','ai-chatbot-human-handoff','blog-traffic-to-chat-leads'],
'ai-agent-instructions-template':['chatbot-sound-human','rag-ai-agent-business-knowledge','mcp-ai-agent-business-tools'],
'ai-automation-clinics-med-spas':['ai-chatbot-human-handoff','facebook-messenger-missed-messages','rag-ai-agent-business-knowledge'],
'facebook-messenger-missed-messages':['ai-chatbot-human-handoff','blog-traffic-to-chat-leads','chatbot-sound-human'],
'ai-chatbot-cost':['chatrace-vs-chatbotbuilder','rag-ai-agent-business-knowledge','mcp-ai-agent-business-tools'],
'stop-bogus-cod-orders':['ai-chatbot-human-handoff','chatbot-sound-human','blog-traffic-to-chat-leads'],
'chatbot-sound-human':['ai-chatbot-human-handoff','rag-ai-agent-business-knowledge','blog-traffic-to-chat-leads'],
'ai-chatbot-human-handoff':['rag-ai-agent-business-knowledge','mcp-ai-agent-business-tools','blog-traffic-to-chat-leads'],
'blog-traffic-to-chat-leads':['chatrace-vs-chatbotbuilder','rag-ai-agent-business-knowledge','mcp-ai-agent-business-tools'],
'chatrace-vs-chatbotbuilder':['mcp-ai-agent-business-tools','rag-ai-agent-business-knowledge'],
}
A='style="color:rgba(0,122,102,1);text-decoration:underline"'
L=lambda t,c:math.ceil(len(t)/c)
plan={}
for slug,info in P.items():
    want=[s for s in M.get(slug,[]) if s not in info['links'] and s!=slug]
    if not want: print('skip',slug); continue
    raw=open(info['file']).read();d=json.loads(raw[raw.index('{'):]);src=d['source']
    if info.get('eb'):
        # new template: add editor-blog block
        items=''.join(f"<li style='margin:0 0 8px 0;font-size:15px;line-height:1.6'><a href='https://www.dijaedadula.com/{s}' style='color:#007a66;text-decoration:underline;text-underline-offset:2px'>{T[s]}</a></li>" for s in want)
        html=(f"<div id='bl' style='font-family:Inter,system-ui,-apple-system,Arial,sans-serif;color:#1a1a1a;border:1px solid #b9dcd4;background:#e8f4f1;border-radius:12px;padding:16px 20px 8px 20px'>"
              f"<p style='margin:0 0 8px 0;font-size:13px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:#5b6470'>New guides on this topic</p>"
              f"<ul style='margin:0 0 8px 0;padding:0 0 0 22px;list-style:disc outside'>{items}</ul></div>")
        plan[slug]={'kind':'new','html':html,'want':want}
    else:
        sec=src['page'][1]; kids=sec['children']
        k=[i for i,c in enumerate(kids) if re.sub('<[^>]+>','',(c.get('specials') or {}).get('text','')).strip()=='Keep reading'][0]
        lst=kids[k+1]; txt=lst['specials']['text']
        cut=txt.find('<a href="https://www.dijaedadula.com/blog"')
        assert cut>0,slug
        add=''.join(f'<b><a href="https://www.dijaedadula.com/{s}" {A}>{T[s]}</a></b><br><br>' for s in want)
        new=txt[:cut]+add+txt[cut:]
        fd=lst['responsive']['desktop']['styles'].get('fontSize',19); fm=lst['responsive']['mobile']['styles'].get('fontSize',17)
        ad=sum(math.ceil((L(T[s],int(640/(fd*0.55)))+1)*fd*1.6) for s in want)
        am=sum(math.ceil((L(T[s],int(380/(fm*0.55)))+1)*fm*1.6) for s in want)
        ops=[{"op":"update","id":lst['id'],"specials":{"text":new},"styles":{"desktop":{"height":lst['responsive']['desktop']['styles']['height']+ad},"mobile":{"height":lst['responsive']['mobile']['styles']['height']+am}}}]
        for c in kids[k+2:]:
            ops.append({"op":"update","id":c['id'],"styles":{"desktop":{"top":c['responsive']['desktop']['styles']['top']+ad},"mobile":{"top":c['responsive']['mobile']['styles']['top']+am}}})
        ops.append({"op":"update","id":sec['id'],"styles":{"desktop":{"height":sec['responsive']['desktop']['styles']['height']+ad},"mobile":{"height":sec['responsive']['mobile']['styles']['height']+am}}})
        plan[slug]={'kind':'old','ops':ops,'want':want,'add':[ad,am],'fonts':[fd,fm]}
json.dump(plan,open('plan.json','w'),ensure_ascii=False)
for s,p in plan.items(): print(s,p['kind'],p['want'],p.get('add'),p.get('fonts'))
