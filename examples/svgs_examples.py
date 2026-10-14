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
# STACK
groups=[('IDENTITY','#007a66','#fff',['1. Role','2. Goal']),('FACTS','#e8f4f1','#1a1a1a',['3. Business facts','4. Products and prices','5. Policies']),('BEHAVIOR','#fff','#1a1a1a',['6. Tone and language','7. Conversation steps']),('SAFETY','#fff4ec','#1a1a1a',['8. Rules','9. Handoff'])]
b=[];y=20
for g,fill,tc,items in groups:
    h=len(items)*38+10
    b.append(f'<text x="24" y="{y+h/2+4}" class="svg-k">{g}</text>')
    for i,it in enumerate(items):
        yy=y+5+i*38
        stroke='#007a66' if g!='SAFETY' else '#c2410c'
        cls='svg-w' if tc=='#fff' else 'svg-t'
        b.append(f'<rect x="150" y="{yy}" width="460" height="32" rx="8" fill="{fill}" stroke="{stroke}"/><text x="170" y="{yy+21}" class="{cls}">{it}</text>')
    y+=h+8
STACK=fig('fa1',y+12,'The 9-part instruction structure in four layers','Four layers from top to bottom. Identity: role and goal. Facts: business facts, products and prices, policies. Behavior: tone and language, conversation steps. Safety: rules and handoff.','\n'.join(b),'The nine parts grouped into four layers. Identity first, safety last, so the limits are the freshest thing the model reads.')
# LOOP
import math
nodes=['Write the test questions','Write or edit the instruction','Run every test','Read real conversations','Fix the instruction or file']
cx,cy,r=320,205,140
b=[]
pts=[(cx+225*math.cos(-math.pi/2+2*math.pi*i/5),cy+150*math.sin(-math.pi/2+2*math.pi*i/5)) for i in range(5)]
for i in range(5):
    x1,y1=pts[i];x2,y2=pts[(i+1)%5]
    # shorten
    dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy);s=min(0.42,(92 if abs(dy)<20 else 62)/L)
    b.append(f'<path d="M{x1+dx*s:.0f} {y1+dy*s:.0f} L{x2-dx*s:.0f} {y2-dy*s:.0f}" stroke="#5b6470" stroke-width="1.6" fill="none" marker-end="url(#fa2a)"/>')
for i,(x,y_) in enumerate(pts):
    fill='#007a66' if i==2 else '#fff'; cls='svg-w' if i==2 else 'svg-t'
    words=nodes[i].split(' ');l1=' '.join(words[:2]);l2=' '.join(words[2:])
    b.append(f'<rect x="{x-85:.0f}" y="{y_-26:.0f}" width="170" height="52" rx="10" fill="{fill}" stroke="#007a66"/><text x="{x:.0f}" y="{y_-4:.0f}" text-anchor="middle" class="{cls}">{l1}</text><text x="{x:.0f}" y="{y_+15:.0f}" text-anchor="middle" class="{"svg-ws" if i==2 else "svg-s"}">{l2}</text>')
b.append(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" class="svg-k">REPEAT AFTER EVERY CHANGE</text>')
LOOP=fig('fa2',410,'Instruction test loop','A five-step loop: write the test questions, write or edit the instruction, run every test, read real conversations, fix the instruction or knowledge file, then repeat.','\n'.join(b),'The test loop. Run every test after every change, because a fix for one answer can break another.')
# SPEED
b=['<text x="24" y="34" class="svg-k">LIKELIHOOD OF QUALIFYING A LEAD WHEN CONTACTED WITHIN AN HOUR</text>']
X0,W=230,370
for i,(lab,sub,v,col) in enumerate([('vs. one hour later','nearly 7x',7,'#5b9e90'),('vs. 24+ hours later','more than 60x',60,'#007a66')]):
    yy=70+i*70
    b.append(f'<text x="24" y="{yy+20}" class="svg-t">{lab}</text>')
    b.append(f'<rect x="{X0}" y="{yy}" width="{W*v/60:.0f}" height="32" rx="6" fill="{col}"/>')
    tx=X0+W*v/60+10; b.append(f'<text x="{tx:.0f}" y="{yy+21}" class="svg-t">{sub}</text>' if v<40 else f'<text x="{X0+W-10}" y="{yy+21}" text-anchor="end" class="svg-w">{sub}</text>')
for t in (0,15,30,45,60):
    x=X0+W*t/60; b.append(f'<line x1="{x:.0f}" y1="200" x2="{x:.0f}" y2="206" stroke="#5b6470"/><text x="{x:.0f}" y="222" text-anchor="middle" class="svg-s">{t}x</text>')
b.append(f'<line x1="{X0}" y1="200" x2="{X0+W}" y2="200" stroke="#cfd6dd"/>')
b.append('<text x="24" y="250" class="svg-s">Source: Oldroyd, McElheran and Elkington, Harvard Business Review, 2011.</text>')
SPEED=fig('fb1',270,'Lead response speed and qualification','Bar chart. Companies that contacted leads within an hour were nearly 7 times as likely to qualify them as companies that waited one more hour, and more than 60 times as likely as companies that waited 24 hours or longer.','\n'.join(b),'Why speed to first reply matters: answering within an hour multiplies the chance of qualifying a lead.')
# ROI
rows=[('Value of time saved',600,'#007a66','$600'),('Value of extra sales',320,'#007a66','$320'),('Subscriptions and maintenance',150,'#c2410c','$150'),('AI usage',23.4,'#c2410c','$23.40')]
b=['<text x="24" y="34" class="svg-k">EXAMPLE MONTH: VALUE VS. COST (ILLUSTRATIVE)</text>']
X0,W=250,330
for i,(lab,v,col,t) in enumerate(rows):
    yy=56+i*48
    b.append(f'<text x="24" y="{yy+20}" class="svg-t">{lab}</text><rect x="{X0}" y="{yy}" width="{max(3,W*v/600):.0f}" height="28" rx="6" fill="{col}"/><text x="{X0+max(3,W*v/600)+8:.0f}" y="{yy+19}" class="svg-t">{t}</text>')
b.append('<rect x="24" y="252" width="14" height="14" rx="3" fill="#007a66"/><text x="44" y="264" class="svg-s">Value</text><rect x="110" y="252" width="14" height="14" rx="3" fill="#c2410c"/><text x="130" y="264" class="svg-s">Cost</text><text x="616" y="264" text-anchor="end" class="svg-t">Return on cost: about 4.3x</text>')
ROI=fig('fb2',290,'Example monthly value versus cost of an AI agent','Horizontal bars for an illustrative month: value of time saved 600 dollars, value of extra sales 320 dollars, subscriptions and maintenance 150 dollars, AI usage 23.40 dollars. Return on cost about 4.3 times.','\n'.join(b),'The worked example as a chart. AI usage is the smallest line; staff time and sales carry the value.')
# LADDER
tiers=[('Starter','Fast answers to|common questions',80,'#e8f4f1','svg-t','svg-s'),('Growth','Chats turned into|qualified leads',145,'#5b9e90','svg-w','svg-ws'),('Scale','The whole customer|journey automated',210,'#007a66','svg-w','svg-ws')]
b=[]
for i,(n,d,h,f,c1,c2) in enumerate(tiers):
    x=40+i*195; y_=260-h
    b.append(f'<rect x="{x}" y="{y_}" width="175" height="{h}" rx="10" fill="{f}" stroke="#007a66"/><text x="{x+87}" y="{y_+28}" text-anchor="middle" class="{c1}">{n}</text><text x="{x+87}" y="{y_+50}" text-anchor="middle" class="{c2}">{d.split("|")[0]}</text><text x="{x+87}" y="{y_+66}" text-anchor="middle" class="{c2}">{d.split("|")[1]}</text>')
b.append('<path d="M40 290 L600 290" stroke="#5b6470" stroke-width="1.6" marker-end="url(#fc1a)"/><text x="40" y="314" class="svg-s">Bigger problem solved, bigger outcome, higher price</text>')
LADDER=fig('fc1',330,'Three-tier package ladder','Three ascending steps. Starter: answer common questions fast. Growth: turn chats into qualified leads. Scale: automate the whole customer journey. Each tier solves a bigger problem at a higher price.','\n'.join(b),'Each tier solves a bigger problem, not just a longer feature list.')
# VALUE
b=['<text x="24" y="34" class="svg-k">EXAMPLE: ANNUAL VALUE AND PRICE RANGE (ILLUSTRATIVE)</text>']
X0,W=24,592
w1=W*2400/6000
b.append(f'<rect x="{X0}" y="60" width="{w1:.0f}" height="44" rx="6" fill="#5b9e90"/><text x="{X0+12}" y="87" class="svg-w">Time saved $2,400</text>')
b.append(f'<rect x="{X0+w1:.0f}" y="60" width="{W-w1:.0f}" height="44" rx="6" fill="#007a66"/><text x="{X0+w1+12:.0f}" y="87" class="svg-w">Extra sales $3,600</text>')
b.append(f'<text x="{X0+W}" y="128" text-anchor="end" class="svg-t">Total annual value $6,000</text>')
p1,p2=X0+W*0.1,X0+W*0.3
b.append(f'<rect x="{p1:.0f}" y="150" width="{p2-p1:.0f}" height="30" rx="6" fill="#fff4ec" stroke="#c2410c"/><text x="{(p1+p2)/2:.0f}" y="170" text-anchor="middle" class="svg-o">$600 to $1,800</text>')
b.append(f'<line x1="{p1:.0f}" y1="104" x2="{p1:.0f}" y2="150" stroke="#c2410c" stroke-dasharray="4 3"/><line x1="{p2:.0f}" y1="104" x2="{p2:.0f}" y2="150" stroke="#c2410c" stroke-dasharray="4 3"/>')
b.append(f'<text x="{p2+12:.0f}" y="170" class="svg-s">Project price: 10% to 30% of annual value</text>')
VALUE=fig('fc2',200,'Annual value and price range','Stacked bar: 2,400 dollars of time saved plus 3,600 dollars of extra sales gives 6,000 dollars of annual value. The project price range of 600 to 1,800 dollars is 10 to 30 percent of that value.','\n'.join(b),'The client keeps most of the value. Your price is a fraction of what the work is worth to them.')
