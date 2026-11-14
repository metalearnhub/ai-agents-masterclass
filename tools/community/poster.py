"""Render a dark-theme 1080x1350 community poster (FB group / IG).
Usage: python3 tools/community/poster.py "<LABEL>" "<Headline with \\n for breaks>" <out.png> [motif]
motif: chat | ladder | funnel | gauge | shield | network (default chat)"""
import sys,os
from playwright.sync_api import sync_playwright
label,head,out=sys.argv[1],sys.argv[2].replace('\\n','<br>'),sys.argv[3]
motif=sys.argv[4] if len(sys.argv)>4 else 'chat'
G='#3fbfa6';D='#17191b';S='#3a3f43'
M={
'chat':f"<rect x='60' y='60' width='420' height='150' rx='40' fill='{D}' stroke='{S}' stroke-width='4'/><rect x='110' y='110' width='240' height='18' rx='9' fill='#3a3f43'/><rect x='110' y='148' width='160' height='18' rx='9' fill='#3a3f43'/><rect x='300' y='250' width='420' height='150' rx='40' fill='#10302a' stroke='{G}' stroke-width='5'/><rect x='350' y='300' width='260' height='18' rx='9' fill='{G}'/><rect x='350' y='338' width='180' height='18' rx='9' fill='{G}' opacity='.6'/><circle cx='740' cy='130' r='46' fill='{D}' stroke='{S}' stroke-width='4'/><path d='M718 130 l16 16 l30 -34' stroke='{G}' stroke-width='8' fill='none' stroke-linecap='round'/>",
'ladder':"".join(f"<rect x='{60+i*150}' y='{380-i*70}' width='130' height='{40+i*70}' rx='14' fill='{G if i==4 else D}' fill-opacity='{1 if i==4 else 1}' stroke='{G if i==4 else S}' stroke-width='4'/>" for i in range(5)),
'funnel':f"<path d='M120 80 h640 l-220 220 v140 l-200 -60 v-80 z' fill='{D}' stroke='{S}' stroke-width='5'/><circle cx='440' cy='160' r='22' fill='{G}'/><circle cx='360' cy='130' r='16' fill='#3a3f43'/><circle cx='520' cy='120' r='16' fill='#3a3f43'/><circle cx='440' cy='300' r='18' fill='{G}'/>",
'gauge':f"<path d='M140 380 A300 300 0 0 1 740 380' fill='none' stroke='{S}' stroke-width='40' stroke-linecap='round'/><path d='M140 380 A300 300 0 0 1 560 120' fill='none' stroke='{G}' stroke-width='40' stroke-linecap='round'/><line x1='440' y1='380' x2='580' y2='170' stroke='#fff' stroke-width='12' stroke-linecap='round'/><circle cx='440' cy='380' r='26' fill='#fff'/>",
'shield':f"<path d='M440 60 l260 90 v130 c0 120 -110 180 -260 220 c-150 -40 -260 -100 -260 -220 v-130 z' fill='{D}' stroke='{S}' stroke-width='6'/><path d='M360 270 l60 60 l120 -130' stroke='{G}' stroke-width='22' fill='none' stroke-linecap='round' stroke-linejoin='round'/>",
'network':f"<line x1='440' y1='240' x2='180' y2='110' stroke='{S}' stroke-width='6'/><line x1='440' y1='240' x2='700' y2='110' stroke='{S}' stroke-width='6'/><line x1='440' y1='240' x2='160' y2='380' stroke='{S}' stroke-width='6'/><line x1='440' y1='240' x2='720' y2='380' stroke='{G}' stroke-width='8'/><circle cx='440' cy='240' r='70' fill='#10302a' stroke='{G}' stroke-width='6'/>"+"".join(f"<circle cx='{x}' cy='{y}' r='44' fill='{D}' stroke='{S}' stroke-width='5'/>" for x,y in [(180,110),(700,110),(160,380)])+f"<circle cx='720' cy='380' r='44' fill='{D}' stroke='{G}' stroke-width='6'/>",
}[motif]
html=f"""<html><head><link href='https://fonts.googleapis.com/css2?family=Inter:wght@700;800;900&display=swap' rel='stylesheet'><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;font-family:Inter,Arial,sans-serif;background:linear-gradient(180deg,#0a0b0c 0%,#1f2224 100%);color:#fff;position:relative;overflow:hidden}}
.k{{position:absolute;left:90px;top:100px;font-size:28px;font-weight:900;letter-spacing:6px;color:#4fd1b5;text-transform:uppercase}}
h1{{position:absolute;left:90px;right:90px;top:160px;font-size:88px;line-height:1.04;font-weight:900;letter-spacing:-2px}}
svg{{position:absolute;left:100px;bottom:200px;width:880px;height:460px}}
.pill{{position:absolute;left:90px;bottom:90px;border:3px solid #fff;border-radius:40px;padding:14px 28px;font-size:24px;font-weight:900;letter-spacing:5px}}
.u{{position:absolute;right:90px;bottom:104px;font-size:24px;font-weight:800;color:#8a8f94}}</style></head><body>
<div class='k'>{label}</div><h1>{head}</h1><svg viewBox='0 0 880 460'>{M}</svg><div class='pill'>DIJAE DADULA</div><div class='u'>dijaedadula.com</div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1350})
    pg.set_content(html);pg.wait_for_timeout(900);pg.screenshot(path=out);b.close()
print(out)
