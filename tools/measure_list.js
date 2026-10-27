// Measure the /blog post-list HTML at desktop (640) and mobile (380) widths with the same Inter weights the live page loads (500, 800).
const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const F=w=>'file://'+path.resolve(__dirname,'node_modules/@fontsource/inter/files/inter-latin-'+w+'-normal.woff2');
const ff=[500,800].map(w=>`@font-face{font-family:Inter;font-weight:${w};src:url(${F(w)})}`).join('');
(async()=>{
 const b=await chromium.launch({executablePath:process.env.CHROME||'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const html=fs.readFileSync(process.argv[2],'utf8'),out={};
 for(const w of [640,380]){
  const p=await b.newPage({viewport:{width:w+40,height:900}});
  await p.setContent(`<html><head><style>${ff}body{margin:0;padding:0 20px}</style></head><body><div style="width:${w}px">${html}</div></body></html>`);
  await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
  out[w]=await p.evaluate(()=>document.querySelector('#bl').getBoundingClientRect().height);
  if(process.argv[3])await p.screenshot({path:process.argv[3]+'_'+w+'.png',fullPage:true});
 }
 console.log(JSON.stringify(out));await b.close();
})();
