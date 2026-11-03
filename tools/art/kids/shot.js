const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:1700},deviceScaleFactor:1});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]+'/kids.html');await p.waitForTimeout(300);await p.screenshot({path:process.argv[2]+'/sheet.png',fullPage:true});
if(process.argv[3]==='each'){await p.setViewportSize({width:1600,height:1700});const p2=await b.newPage({viewport:{width:1600,height:2000},deviceScaleFactor:3});await p2.goto('file://'+process.argv[2]+'/kids.html');await p2.waitForTimeout(300);
  for(const id of await p2.evaluate(()=>[...document.querySelectorAll('body>div')].map(d=>d.id))){const e=await p2.$('#'+id+' svg');await e.screenshot({path:process.argv[2]+'/src_'+id+'.png'})}}
console.log('errors:',errs.join(' | ')||'none');await b.close()})();
