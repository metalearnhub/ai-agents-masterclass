const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const F=p=>'file://'+path.resolve('node_modules/@fontsource/'+p);
const ff=`@font-face{font-family:Inter;font-weight:400;src:url(${F('inter/files/inter-latin-400-normal.woff2')})}
@font-face{font-family:Inter;font-weight:600;src:url(${F('inter/files/inter-latin-600-normal.woff2')})}
@font-face{font-family:Inter;font-weight:700;src:url(${F('inter/files/inter-latin-700-normal.woff2')})}
@font-face{font-family:Inter;font-weight:800;src:url(${F('inter/files/inter-latin-800-normal.woff2')})}
@font-face{font-family:"JetBrains Mono";font-weight:400;src:url(${F('jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2')})}`;
(async()=>{
 const b=await chromium.launch({executablePath:process.env.CHROME||'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const art=fs.readFileSync(process.argv[2]||'article.html','utf8');
 const css=fs.readFileSync('style.css','utf8');
 const out={};
 for(const w of [640,380]){
  const p=await b.newPage({viewport:{width:w+40,height:900}});
  await p.setContent(`<html><head><style>${ff}${css} body{margin:0;padding:0 20px}</style></head><body><div id="box" style="width:${w}px">${art}</div></body></html>`);
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(300);
  out[w]=await p.evaluate(()=>document.querySelector('.dd-article').getBoundingClientRect().height);
  await p.screenshot({path:`m_${w}.png`,fullPage:true});
 }
 console.log(JSON.stringify(out));
 await b.close();
})();
