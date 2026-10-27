"""Build the /blog post list (element t_0240, an editor-blog card list) from pages/blog/list.json.
Usage: python3 tools/blog_list.py [<slug> "<H1>" "<blurb>"] [--shot prefix]
Adds the new post on top (if given), saves list.json, writes pages/blog/list.html and blog_patch.json
(patch_page ops for page 51cab93b-210b-4516-aa6f-f7f94c533eb6), then publish_page(custom_path blog)."""
import json,math,os,subprocess,sys,html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LJ=os.path.join(ROOT,'pages/blog/list.json')
args=[a for a in sys.argv[1:]]
shot=None
if '--shot' in args:i=args.index('--shot');shot=args[i+1];del args[i:i+2]
d=json.load(open(LJ))
if len(args)>=3:
    slug,title,blurb=args[:3]
    d['posts']=[p for p in d['posts'] if p['slug']!=slug]
    d['posts'].insert(0,{"slug":slug,"title":title,"blurb":blurb})
    json.dump(d,open(LJ,'w'),indent=1,ensure_ascii=False)
F="font-family:Inter,system-ui,-apple-system,Arial,sans-serif"
out=[f"<div id='bl' style=\"{F};color:#1a1a1a\">",
 f"<p style='margin:0 0 22px 0;padding:14px 18px;background:#e8f4f1;border-radius:10px;font-size:15px;line-height:1.55;font-weight:500;color:#1a1a1a'><b style='font-weight:800'>Hiring?</b> See <a href='https://www.dijaedadula.com/ai-automation-philippines' style='color:#007a66;text-decoration:underline;font-weight:800'>AI chatbot, AI agent and automation services</a> for businesses in the Philippines and Southeast Asia.</p>"]
out.append("<div style='display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px'>")
for i,p in enumerate(d['posts']):
    badge="<span style='display:inline-block;margin:0 0 8px 0;padding:2px 8px;border-radius:999px;background:#fff4ec;color:#c2410c;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase'>New</span>" if i==0 else ""
    out.append(f"<a href='https://www.dijaedadula.com/{p['slug']}' style='display:block;text-decoration:none;color:#1a1a1a;border:1px solid #e3e8ee;border-radius:12px;padding:16px 18px;margin:0;background:#ffffff'>{badge}"
      f"<span style='display:block;font-size:17px;line-height:1.35;font-weight:800;color:#1a1a1a;margin:0 0 6px 0'>{p['title']}</span>"
      f"<span style='display:block;font-size:15px;line-height:1.6;font-weight:500;color:#5b6470'>{p['blurb']}</span>"
      f"<span style='display:block;margin:8px 0 0 0;font-size:13px;font-weight:800;color:#007a66'>Read the guide &rarr;</span></a>")
out.append("</div></div>")
html="\n".join(out).replace('"',"'")
open(os.path.join(ROOT,'pages/blog/list.html'),'w').write(html)
cmd=['node',os.path.join(ROOT,'tools/measure_list.js'),os.path.join(ROOT,'pages/blog/list.html')]+([shot] if shot else [])
m=json.loads(subprocess.check_output(cmd,cwd=os.path.join(ROOT,'tools')).decode().strip().splitlines()[-1])
# live Webcake render runs taller than the headless measure (wider letter-spacing); the gap grows with each card, so pad per post
n=len(d['posts']); DH=math.ceil(m['640']+2.3*n); MH=math.ceil(m['380']+7.8*n)
TD,TM=162,130            # list top (desktop, mobile)
CD,CM=TD+DH+36,TM+MH+28  # CTA t_0241 top
P=[{"op":"replace","id":"t_0240","element":{"id":"t_0240","type":"editor-blog","specials":{"html":html},
   "responsive":{"desktop":{"styles":{"top":TD,"left":160,"width":640,"height":DH}},"mobile":{"styles":{"top":TM,"left":20,"width":380,"height":MH}}}}},
   {"op":"update","id":"t_0241","styles":{"desktop":{"top":CD},"mobile":{"top":CM}}},
   {"op":"update","id":"sec_0237","styles":{"desktop":{"height":CD+65+64},"mobile":{"height":CM+88+48}}}]
json.dump(P,open('blog_patch.json','w'),ensure_ascii=False)
print(json.dumps({"posts":len(d['posts']),"measured":m,"DH":DH,"MH":MH,"cta":[CD,CM]}))
