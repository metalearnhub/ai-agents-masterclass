def fig(id_,vb_h,title,desc,body,cap):
    return f'''<figure class="dd-fig">
<svg viewBox="0 0 640 {vb_h}" role="img" aria-labelledby="{id_}t {id_}d" xmlns="http://www.w3.org/2000/svg">
<title id="{id_}t">{title}</title>
<desc id="{id_}d">{desc}</desc>
<defs><marker id="{id_}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#5b6470"/></marker></defs>
<rect x="0" y="0" width="640" height="{vb_h}" rx="14" fill="#f6f8fa"/>
{body}
</svg>
<figcaption><b>Figure N.</b> {cap}</figcaption>
</figure>'''
# LEAK: pipeline with 5 leak points
st=[('Message','arrives'),('Seen','by someone'),('First reply','with an answer'),('Next step','price, slot, order'),('Sale','or booking')]
leaks=['Lands at night','No owner','Slow or vague','Left hanging','']
b=['<text x="24" y="34" class="svg-k">THE MESSENGER INBOX LEAK</text>']
w=104;g=18;x0=24
for i,(t,s) in enumerate(st):
    x=x0+i*(w+g)
    dark=i in (0,4)
    b.append(f'<rect x="{x}" y="58" width="{w}" height="62" rx="10" fill="{"#007a66" if dark else "#e8f4f1"}" stroke="#007a66"/>')
    c1,c2=('svg-w','svg-ws') if dark else ('svg-t','svg-s')
    b.append(f'<text x="{x+w/2}" y="85" text-anchor="middle" class="{c1}">{t}</text><text x="{x+w/2}" y="104" text-anchor="middle" class="{c2}">{s}</text>')
    if i<4: b.append(f'<path d="M{x+w+2} 89 L{x+w+g-2} 89" stroke="#5b6470" stroke-width="1.6" marker-end="url(#fl1a)"/>')
    if leaks[i]:
        b.append(f'<path d="M{x+w/2} 122 L{x+w/2} 150" stroke="#c2410c" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#fl1a)"/>')
        b.append(f'<rect x="{x+2}" y="156" width="{w-4}" height="30" rx="8" fill="#fff4ec" stroke="#c2410c"/><text x="{x+w/2}" y="176" text-anchor="middle" class="svg-o">{leaks[i]}</text>')
b.append('<rect x="24" y="204" width="592" height="34" rx="8" fill="#fff4ec" stroke="#c2410c"/><text x="320" y="226" text-anchor="middle" class="svg-o">After 24 hours of silence, Meta limits what a page can still send</text>')
LEAK=fig('fl1',258,'The Messenger inbox leak','Five stages: a message arrives, someone sees it, the first reply answers the question, the next step is offered, then the sale or booking. Customers leak out at four points: messages that land at night, messages with no owner, slow or vague first replies, and conversations left hanging after the first reply. After 24 hours of silence, Meta limits what the page can still send.','\n'.join(b),'Four places a Messenger conversation leaks before it becomes a sale. The 24-hour window makes every leak more expensive.')
# FLOW: AI + human handoff
b=['<text x="24" y="34" class="svg-k">ASSISTIVE SETUP: AI ANSWERS, PEOPLE CLOSE</text>']
def box(x,y,w,h,t,s,dark=False,warn=False):
    fill='#007a66' if dark else ('#fff4ec' if warn else '#e8f4f1'); st='#c2410c' if warn else '#007a66'
    c1,c2=('svg-w','svg-ws') if dark else (('svg-o','svg-s') if warn else ('svg-t','svg-s'))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{st}"/><text x="{x+w/2}" y="{y+h/2-3}" text-anchor="middle" class="{c1}">{t}</text><text x="{x+w/2}" y="{y+h/2+15}" text-anchor="middle" class="{c2}">{s}</text>'
def ar(x1,y1,x2,y2,dash=False,col='#5b6470'):
    d=' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="1.6"{d} marker-end="url(#ff1a)"/>'
b+= [box(24,60,128,62,'New message','any hour',True),
     ar(154,91,186,91),
     box(188,60,156,62,'Botcake AI','answers known questions'),
     ar(346,91,392,91),
     box(394,60,222,62,'Ready to buy or complex','tag + assign in Pancake'),
     ar(266,124,266,168,True,'#c2410c'),
     box(188,170,156,62,'Bot reply failed','marked unread',warn=True),
     ar(505,124,505,168),
     ar(346,201,392,201),
     box(394,170,222,62,'Staff closes','price, slot, order',True),
     '<text x="24" y="190" class="svg-s">The bot pauses</text><text x="24" y="208" class="svg-s">while a person</text><text x="24" y="226" class="svg-s">is replying.</text>']
FLOW=fig('ff1',256,'Assistive setup: AI answers, people close','A new message arrives at any hour. Botcake AI answers the known questions. Customers who are ready to buy or have complex requests are tagged and assigned to a person in Pancake. If the bot reply fails, the conversation is marked unread for staff. Staff close the sale. The bot pauses while a person is replying.','\n'.join(b),'The AI handles speed and the known answers. Your team handles judgment and closing. Failed bot replies come back to a person instead of disappearing.')
