"""Build a complete Webcake page source for one blog post.
Usage: python3 tools/make_post.py posts/<slug>
Needs posts/<slug>/meta.json and posts/<slug>/article.html (see RUNBOOK.md).
Writes posts/<slug>/source.json (pass its contents as `source` to create_page)."""
import json,re,html,copy,subprocess,sys,os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
d=sys.argv[1]; m=json.load(open(os.path.join(d,'meta.json')))
art=open(os.path.join(d,'article.html')).read()
art=art.replace('<!--COVER-->','<figure class="dd-fig"><div class="dd-shot" style="aspect-ratio:16/9"><img src="%s" alt="%s" width="1536" height="864" loading="lazy"></div></figure>'%(m['cover'],html.escape(m['cover_alt'],quote=True)))
n=[0]
def num(_): n[0]+=1; return '<b>Figure %d.</b>'%n[0]
art=re.sub(r'<b>Figure N\.</b>',num,art)
assert '<!--' not in art, 'unreplaced marker in article.html'
# blank lines collapse, but keep blank lines inside <pre>
parts=re.split(r'(<pre>.*?</pre>)',art,flags=re.S)
art=''.join(p if p.startswith('<pre>') else re.sub(r'\n\s*\n','\n',p) for p in parts)
def q(h):  # quote-free: single-quoted attrs, curly quotes in text
    out=[]
    for part in re.split(r'(<[^>]+>)',h):
        if part.startswith('<'):
            part=re.sub(r'="([^"]*)"',lambda mm:"='%s'"%mm.group(1).replace("'","&#39;"),part)
        else:
            part=re.sub(r'(^|[\s(\[>/])"',lambda mm:mm.group(1)+'“',part); part=part.replace('"','”')
        out.append(part)
    return ''.join(out)
art=q(art); assert '"' not in art
open(os.path.join(d,'article_final.html'),'w').write(art)
env=dict(os.environ)
def node(script,*a):
    return subprocess.check_output(['node',os.path.join(HERE,script),*a],cwd=HERE,env=env).decode()
hh=json.loads(node('mh.js',m['h1'],m['dek']))
meas=json.loads(node('measure.js',os.path.abspath(os.path.join(d,'article_final.html'))))
h1d,h1m,dkd,dkm=int(hh[0]+6),int(hh[1]+6),int(hh[2]+4),int(hh[3]+4)
ad,am=meas['640'],meas['380']
# calibration (fitted on 3 live posts): live code blocks render ~8px/line taller than the local measurement.
codelines=sum(x.count('\n')+1 for x in re.findall(r'<pre>(.*?)</pre>',art,re.S))
DH=int(ad+8*codelines+60); MH=int(am*1.005+8.5*codelines+60)
if 'DH' in m: DH=m['DH']
if 'MH' in m: MH=m['MH']
T=json.load(open(os.path.join(ROOT,'template','live_src.json')))['source']
S=copy.deepcopy(T); body=S['page'][1]
dtop1=105+h1d+18; btop=dtop1+dkd+18; etop=btop+57
mtop1=84+h1m+14; mbtop=mtop1+dkm+14; metop=mbtop+52
words=len(re.sub('<[^>]+>',' ',art).split()); mins=max(3,round(words/230))
date=m['date']; import datetime
dd=datetime.date.fromisoformat(date); human=dd.strftime('%B ')+str(dd.day)+dd.strftime(', %Y')
for c in body['children']:
    r=c['responsive']
    if c['id']=='t_2109': c['specials']['text']=re.sub(r'</a> · .*$','</a> · '+m['cat'],c['specials']['text'])
    if c['id']=='t_2110': c['specials']['text']=m['h1']; r['desktop']['styles']['height']=h1d; r['mobile']['styles']['height']=h1m
    if c['id']=='t_2111': c['specials']['text']=m['dek']; r['desktop']['styles'].update(top=dtop1,height=dkd); r['mobile']['styles'].update(top=mtop1,height=dkm)
    if c['id']=='t_2112':
        t=re.sub(r'\d+ min read','%d min read'%mins,c['specials']['text'])
        t=re.sub(r'· [A-Z][a-z]+ \d{1,2}, \d{4} ·','· %s ·'%human,t)
        c['specials']['text']=t; r['desktop']['styles']['top']=btop; r['mobile']['styles']['top']=mbtop
    if c['id']=='eb_2120': c['specials']['html']=art; r['desktop']['styles'].update(top=etop,height=DH); r['mobile']['styles'].update(top=metop,height=MH)
    if c['id']=='h_css2121':
        c['specials']['html']=c['specials']['html'].split('&lt;script')[0]
        r['desktop']['styles']['top']=etop+DH+47; r['mobile']['styles']['top']=metop+MH+39
body['responsive']['desktop']['styles']['height']=etop+DH+57
body['responsive']['mobile']['styles']['height']=metop+MH+49
U='https://www.dijaedadula.com/'; url=U+m['slug']; st=S['settings']
st.update(title=m['seo'],description=m['desc'],keywords=m['kw'],canonical=url,thumbnail=m['cover'])
pil=st['bhet']; rest=pil[pil.find("<link rel='preconnect'"):]
faq=[]
if "id='faq'" in art:
    for mm in re.finditer(r'<h3>(.*?)</h3>\n<p>(.*?)</p>',art.split("id='faq'")[1].split("dd-cta")[0],re.S):
        faq.append({"@type":"Question","name":html.unescape(mm.group(1)),"acceptedAnswer":{"@type":"Answer","text":html.unescape(re.sub('<[^>]+>','',mm.group(2)))}})
post={"@context":"https://schema.org","@type":"BlogPosting","@id":url+"#post","mainEntityOfPage":url,"headline":m['h1'][:110],"description":m['desc'],"image":{"@type":"ImageObject","url":m['cover'],"width":1536,"height":864,"caption":m['cover_alt']},"datePublished":date,"dateModified":date,"inLanguage":"en","wordCount":words,"articleSection":m['cat'],"keywords":m['kw'],
  "author":{"@type":"Person","@id":U+"home#person","name":"Dijae Dadula","url":U+"home"},"publisher":{"@type":"Person","@id":U+"home#person","name":"Dijae Dadula"},"isPartOf":{"@type":"Blog","@id":U+"blog#blog","url":U+"blog"}}
lds=[post]
if faq: lds.append({"@context":"https://schema.org","@type":"FAQPage","@id":url+"#faq","mainEntity":faq})
lds.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":U+"home"},{"@type":"ListItem","position":2,"name":"Blog","item":U+"blog"},{"@type":"ListItem","position":3,"name":m['short'],"item":url}]})
ld=''.join('<script type="application/ld+json">%s</script>'%json.dumps(x,ensure_ascii=False) for x in lds)
e=lambda x:html.escape(x,quote=True)
assert len(m['seo'])<=60, 'seo title over 60 chars: %d'%len(m['seo'])
assert 120<=len(m['desc'])<=160, 'meta description must be 120-160 chars: %d'%len(m['desc'])
meta=("<meta property='og:type' content='article'><meta property='og:site_name' content='Dijae Dadula'>"
 "<meta property='og:url' content='%s'><meta property='og:title' content='%s'><meta property='og:description' content='%s'>"
 "<meta property='og:image' content='%s'><meta property='og:image:width' content='1536'><meta property='og:image:height' content='864'>"
 "<meta property='og:image:alt' content='%s'><meta name='twitter:card' content='summary_large_image'>"
 "<meta name='twitter:title' content='%s'><meta name='twitter:description' content='%s'><meta name='twitter:image' content='%s'>"
 "<meta name='twitter:image:alt' content='%s'><meta name='author' content='Dijae Dadula'>")%(url,e(m['h1']),e(m['desc']),m['cover'],e(m['cover_alt']),e(m['h1']),e(m['desc']),m['cover'],e(m['cover_alt']))
st['bhet']=ld+meta+rest
json.dump(S,open(os.path.join(d,'source.json'),'w'),ensure_ascii=False,separators=(',',':'))
geo=dict(eb_top_d=etop,DH=DH,hcss_top_d=etop+DH+47,sec_d=etop+DH+57,eb_top_m=metop,MH=MH,hcss_top_m=metop+MH+39,sec_m=metop+MH+49,words=words,mins=mins,faq=len(faq),measured=[ad,am])
json.dump(geo,open(os.path.join(d,'geometry.json'),'w'))
print(json.dumps(geo))
