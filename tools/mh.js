const { chromium } = require('playwright');const path=require('path');
const F=p=>'file://'+path.resolve('node_modules/@fontsource/inter/files/inter-latin-'+p+'-normal.woff2');
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME||'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
const H1=process.argv[2],D=process.argv[3];
await p.setContent(`<style>@font-face{font-family:Inter;font-weight:400;src:url(${F(400)})}@font-face{font-family:Inter;font-weight:800;src:url(${F(800)})}div{font-family:Inter}</style>
<div id=a style="width:640px;font-size:42px;font-weight:800;line-height:1.18">${H1}</div><div id=b style="width:380px;font-size:30px;font-weight:800;line-height:1.18">${H1}</div>
<div id=c style="width:640px;font-size:21px;line-height:1.5">${D}</div><div id=d style="width:380px;font-size:18px;line-height:1.5">${D}</div>`);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
console.log(await p.evaluate(()=>['a','b','c','d'].map(i=>document.getElementById(i).getBoundingClientRect().height)));await b.close()})();
