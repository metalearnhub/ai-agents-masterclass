import json,sys,html as H
from playwright.sync_api import sync_playwright
OUT='/tmp/claude-0/-home-claude/a0ddebc3-1c9f-5dc3-9d51-6b734607f315/scratchpad/ca'
d=[{'slug':'facebook-messenger-missed-messages','message':"Most pages don't have a traffic problem. They have an inbox problem."}]
LBL={0:'MESSENGER'};_X={0:'AI AGENTS',2:'DIGITAL INCOME',3:'AUTOMATION',4:'DATA PRIVACY',5:'LEAD FOLLOW-UP',6:'AI CHATBOTS',7:'CLIENT GROWTH',8:'AI TRAINING',9:'CASE STUDY',10:'CHAT TOOLS',11:'AI QUALITY',12:'MCP',13:'PLATFORMS',14:'RESORTS AND HOTELS',15:'LEAD QUALIFICATION',16:'LIVE SELLING',17:'AI CAREERS',18:'FREELANCING',19:'PRICING',20:'CHATBOT ROI',21:'AI AGENTS',22:'CLINICS AND MED SPAS'}
MOT={0:'chat'};_Y={0:'network',2:'ladder',3:'funnel',4:'shield',5:'chat',6:'chat',7:'funnel',8:'gauge',9:'funnel',10:'network',11:'gauge',12:'network',13:'network',14:'chat',15:'funnel',16:'chat',17:'ladder',18:'network',19:'ladder',20:'gauge',21:'chat',22:'funnel'}
src=open('/home/claude/autopilot/tools/community/poster.py').read()
M_start=src.index("M={"); M_end=src.index("}[motif]")+1
G='#3fbfa6';D='#17191b';S='#3a3f43'
ns={'G':G,'D':D,'S':S}
Mdict=eval(src[M_start+2:M_end-0].rsplit('[motif]',1)[0] if False else src[M_start+2:src.index("}[motif]")+1],ns)
out=[]
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':1012,'height':1350})
  for i,f in enumerate(d):
    if i==1: continue
    head=H.escape(f['message'].split('\n')[0].strip())
    n=len(head); fs=88 if n<=48 else 76 if n<=64 else 66
    html=f"""<html><head><link href='https://fonts.googleapis.com/css2?family=Inter:wght@700;800;900&display=swap' rel='stylesheet'><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1012px;height:1350px;font-family:Inter,Arial,sans-serif;background:linear-gradient(180deg,#0a0b0c 0%,#1f2224 100%);color:#fff;position:relative;overflow:hidden}}
.k{{position:absolute;left:70px;top:100px;font-size:28px;font-weight:900;letter-spacing:6px;color:#4fd1b5}}
h1{{position:absolute;left:70px;right:70px;top:160px;font-size:{fs}px;line-height:1.05;font-weight:900;letter-spacing:-2px}}
svg{{position:absolute;left:66px;bottom:190px;width:880px;height:460px}}
.pill{{position:absolute;left:70px;bottom:90px;border:3px solid #fff;border-radius:40px;padding:14px 28px;font-size:24px;font-weight:900;letter-spacing:5px}}
.u{{position:absolute;right:70px;bottom:104px;font-size:24px;font-weight:800;color:#8a8f94}}</style></head><body>
<div class='k'>{LBL[i]}</div><h1>{head}</h1><svg viewBox='0 0 880 460'>{Mdict[MOT[i]]}</svg><div class='pill'>CHATBOT AUTHORITY</div><div class='u'>dijaedadula.com</div></body></html>"""
    pg.set_content(html);pg.wait_for_timeout(700)
    hb=pg.evaluate("document.querySelector('h1').getBoundingClientRect().bottom")
    fn=f"{OUT}/fb-1120-.png"; pg.screenshot(path=fn); out.append((i,fn,round(hb)))
  b.close()
for o in out: print(o)
