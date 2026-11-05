// Headless run of Babies & Beasts (bb.html): 5 bots play until one is left.
// Usage (repo root): node tools/sim/bb_sim.js [games=5] [--klv N] [--map cross]   (--klv: player 0 has kid level N in every class; bots get levels near it)
const fs=require('fs'),path=require('path'),vm=require('vm');
const html=fs.readFileSync(path.join(__dirname,'..','..','bb.html'),'utf8');
const js=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).sort((a,b)=>b.length-a.length)[0];
const N=+process.argv[2]||5,rows=[],ki=process.argv.indexOf('--klv'),KL=ki>0?+process.argv[ki+1]:0,mi=process.argv.indexOf('--map'),MAP=mi>0?process.argv[mi+1]:undefined;
for(let g=0;g<N;g++){
  const ctx={window:{BB_HEADLESS:true},module:{exports:{}},console,Math,JSON};vm.createContext(ctx);vm.runInContext(js,ctx);
  const B=ctx.module.exports;B.newGame(Object.assign(KL?{klv:Object.fromEntries(B.CK.map(k=>[k,KL]))}:{},MAP?{map:MAP}:{}));const G=B.G;G.players[0].human=false;
  const out=[];let t=0;const dt=1/30;
  while(!G.over&&t<3600){B.step(dt);t+=dt;for(const p of G.players)if(!p.alive&&!out.includes(p.i)){out.push(p.i);p.outW=G.wave;p.outT=t}}
  const win=G.players.find(p=>p.rank===1);
  const units=win?win.units.filter(Boolean).map(u=>(u.b?u.b[0].toUpperCase():u.c[0])+u.t).join(' '):'';const reds=G.players.reduce((a,p)=>a+p.units.filter(u=>u&&u.t===3).length,0),golds=G.players.reduce((a,p)=>a+p.units.filter(u=>u&&u.t===4).length,0);const beasts=G.players.reduce((a,p)=>a+p.units.filter(u=>u&&u.t===6).length,0);
  rows.push({game:g,winStyle:win&&(win.ai.style||'bal'),minutes:(t/60).toFixed(1),waves:G.wave,outs:G.players.filter(p=>p.outW).sort((a,b)=>a.outW-b.outW).map(p=>(p.ai.style||'bal')[0]+p.outW).join(','),winner:win&&win.name,winGold:win&&win.gold,winInc:win&&win.inc,reds,golds,beasts,units});
  console.log(JSON.stringify(rows[rows.length-1]));
}
