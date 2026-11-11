import re,sys
from playwright.sync_api import sync_playwright
s=open(sys.argv[1]).read()
css=open('/home/claude/autopilot/tools/style.css').read()
svgs=re.findall(r'<svg.*?</svg>',s,re.S)
with sync_playwright() as p:
  b=p.chromium.launch(); pg=b.new_page(viewport={'width':700,'height':500})
  for i,v in enumerate(svgs):
    pg.set_content('<html><head><style>'+css+'</style></head><body><div class="dd-article" style="width:640px"><figure class="dd-fig">'+v+'</figure></div></body></html>')
    pg.locator('svg').screenshot(path=f'{sys.argv[2]}/svg{i+1}.png')
  b.close()
print(len(svgs))
