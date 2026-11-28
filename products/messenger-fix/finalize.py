import json,re,sys
url=sys.argv[1] if len(sys.argv)>1 else 'PAYPAL_URL'
S=json.load(open('source.json')); m=json.load(open('meta.json'))
U='https://www.dijaedadula.com/'; page=U+m['slug']
for c in S['page'][1]['children']:
    sp=c['specials']
    if c['id']=='t_2109': sp['text']='<a href="https://www.dijaedadula.com/home" style="color:rgba(0,122,102,1);text-decoration:underline">Home</a> · Ebook'
    if c['id']=='t_2112': sp['text']='By <a href="https://www.dijaedadula.com/home" style="color:rgba(0,122,102,1);text-decoration:underline">Dijae Dadula</a> · 23-page PDF · ₱299'
    if c['id']=='eb_2120': sp['html']=sp['html'].replace('PAYPAL_URL',url)
st=S['settings']; b=st['bhet']
lds=re.findall(r'<script type="application/ld\+json">(.*?)</script>',b)
rest=re.sub(r'<script type="application/ld\+json">.*?</script>','',b)
new=[]
for x in lds:
    j=json.loads(x)
    if j['@type']=='BlogPosting':
        j={"@context":"https://schema.org","@type":"Product","@id":page+"#product","name":"The 60-Minute Messenger Fix","description":m['desc'],"image":m['cover'],"brand":{"@type":"Brand","name":"Dijae Dadula"},"author":{"@type":"Person","@id":U+"home#person","name":"Dijae Dadula"},
           "offers":{"@type":"Offer","url":page,"price":"299","priceCurrency":"PHP","availability":"https://schema.org/InStock"}}
    if j['@type']=='BreadcrumbList':
        j['itemListElement']=[{"@type":"ListItem","position":1,"name":"Home","item":U+"home"},{"@type":"ListItem","position":2,"name":m['short'],"item":page}]
    new.append('<script type="application/ld+json">%s</script>'%json.dumps(j,ensure_ascii=False))
rest=rest.replace("<meta property='og:type' content='article'>","<meta property='og:type' content='product'>")
st['bhet']=''.join(new)+rest
json.dump(S,open('source.json','w'),ensure_ascii=False,separators=(',',':'))
print('ok', url in json.dumps(S,ensure_ascii=False))
