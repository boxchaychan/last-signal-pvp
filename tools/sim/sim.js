// Headless game simulation (no browser). Loads the <script> from index.html with a stub DOM/canvas.
// Usage (from the repo root):
//   node tools/sim/sim.js demo [runs=3] [seconds=480]   bots vs bots, prints winner/time per run
//   node tools/sim/sim.js boss [leader=queen] [seconds=300]   scripted boss-mode player (ghost side)
//   node tools/sim/sim.js ults                           casts every hero ultimate once
//   node tools/sim/sim.js guns                           the player fires every gun at a pack for 4 s
// Any thrown error prints a stack trace and exits non-zero, so this doubles as a smoke test.
const fs = require('fs'), path = require('path');
const noop = () => {};
const ctxP = new Proxy({}, { get: (t, k) => k === 'createRadialGradient' || k === 'createLinearGradient' ? () => ({ addColorStop: noop }) : (k in t ? t[k] : noop), set: (t, k, v) => { t[k] = v; return true } });
function el() { return { hidden: false, style: { setProperty: noop }, classList: { toggle: noop, add: noop, remove: noop, contains: () => false }, dataset: {}, children: [], textContent: '', innerHTML: '', addEventListener: noop, setAttribute: noop, getContext: () => ctxP, width: 300, height: 224, querySelector: () => el(), querySelectorAll: () => [], insertAdjacentHTML: noop, appendChild() {}, prepend() {}, remove() {}, after() {}, getBoundingClientRect: () => ({ left: 0, top: 0, width: 150, height: 112 }), setPointerCapture: noop } }
global.document = { body: Object.assign(el(), { appendChild() {} }), querySelector: () => el(), querySelectorAll: () => [], createElement: () => el() };
global.window = global; global.innerWidth = 400; global.innerHeight = 800; global.devicePixelRatio = 2;
global.addEventListener = noop; global.matchMedia = () => ({ matches: true }); global.requestAnimationFrame = noop; global.performance = { now: () => 0 };
global.setTimeout = () => 0; global.clearTimeout = noop; global.localStorage = { getItem: () => null, setItem() {} };
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'index.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).sort((a, b) => b.length - a.length)[0];
const mode = process.argv[2] || 'demo', A3 = process.argv[3], A4 = process.argv[4];
eval(code.replace("if(G.side==='demo'&&G.t>540){newGame('demo');return}", '') + `
if(mode==='demo'){const N=+A3||3,T=+A4||480;
  for(let run=0;run<N;run++){newGame('demo');onResize();let minHq=1e9;for(let t=0;t<T&&!G.over;t+=1/60){step(1/60);minHq=Math.min(minHq,G.hq.hp)}
    const L=leaderAlive();console.log('run',run,'t',G.t|0,G.over?'END':'timeout','minHq',minHq|0,'leader',G.leader,L?L.hp|0:0,G.humans.map(h=>h.key+h.lvl).join(','),'kills',G.kills)}}
if(mode==='boss'){const LDR=A3||'queen',TT=+A4||300;
  newGame('zombie',{leader:LDR,units:['walker','runner','spitter','dog','brute'],ztal:[0,0,0,0],mode:'boss'});onResize();usingTouch=true;
  for(let t=0;t<TT&&!G.over;t+=1/60){const L=leaderAlive();
    if(L&&((t*60)|0)%30===0){if(!nests().length)bmNest();else if(G.bio>=ZB.hatch.cost&&nests().length<4)bmNest();
      const hs=G.humans.filter(h=>h.state==='ok').sort((a,b)=>dist(a,L)-dist(b,L));const goal=t<40?null:(L.hp<L.maxHp*.35?nests()[0]:hs[0]&&dist(hs[0],L)<900?hs[0]:G.hq);
      if(goal){const dx=goal.x-L.x,dy=goal.y-L.y,d=Math.hypot(dx,dy)||1;sticks.move=d>60?{ox:0,oy:0,x:dx/d*50,y:dy/d*50}:null}else sticks.move=null;
      const foe=hs[0];for(const sl of ['q','f','g','e'])if(bossReady(L,sl)&&foe&&dist(foe,L)<420){P.cast={slot:sl,pt:{x:foe.x,y:foe.y},ang:Math.atan2(foe.y-L.y,foe.x-L.x)};break}}
    step(1/60);
    if(((t*60)|0)%(60*30)===0){const L2=leaderAlive();console.log((t|0)+'s queen',L2?L2.hp|0:'dead','nests',nests().length,'bio',G.bio|0,'army',G.zombies.length,'eggs',G.zs.filter(s=>s.type==='egg').length,'hq',G.hq.hp|0)}}
  console.log('over',G.over,'t',G.t|0)}
if(mode==='guns'){for(const w of WK.filter(w=>WEAP[w].cat==='gun')){const k=HK.find(k=>canUseW(k,w));const cfg=cfgFor('human');cfg.hero=k;cfg.mates=HK.filter(x=>x!==k).slice(0,2);cfg.weap=[w,'knife'];
  newGame('human',cfg);onResize();const p=G.humans[0];p.x=MW/2;p.y=MH/2;for(const o of G.humans.slice(1)){o.x=p.x-60;o.y=p.y+30;o.hp=o.maxHp*.5}
  for(let i=0;i<10;i++)spawnZ('walker',p.x+rnd(150,300),p.y+rnd(-60,60));const k0=G.kills,h0=G.humans[1].hp;mouse.active=true;mouse.down=true;
  for(let t=0;t<4;t+=1/60){const z=G.zombies.find(z=>!z.dead&&!z.T.leader);if(z){mouse.x=VW/2+(z.x-G.cam.x)*G.scale;mouse.y=VH/2+(z.y-G.cam.y)*G.scale}step(1/60)}
  mouse.down=false;console.log(w.padEnd(8),'ammo',p.ammo,p.reloadT.toFixed(1),p.fireCd.toFixed(2),p.state,k.padEnd(7),'kills',G.kills-k0,'mines',G.mines.length,'mateHeal',(G.humans[1].hp-h0)|0)}}
if(mode==='ults'){for(const k of ['storm','shadow','medic','volt','eng','trap']){const cfg=cfgFor('human');cfg.hero=k;cfg.mates=HK.filter(x=>x!==k).slice(0,2);cfg.weap=weapOf(k);
  newGame('human',cfg);onResize();const p=G.humans[0];p.x=MW/2;p.y=MH/2;for(const o of G.humans.slice(1)){o.x=p.x+60;o.y=p.y+30}
  for(let i=0;i<14;i++)spawnZ(['walker','runner','brute'][i%3],p.x+rnd(-260,260),p.y+rnd(-260,260));
  const k0=G.kills;p.ult=100;P.cast={slot:'e',pt:{x:p.x+150,y:p.y},ang:0};for(let t=0;t<7;t+=1/60)step(1/60);console.log(k,'kills in 7s',G.kills-k0)}}
`);
