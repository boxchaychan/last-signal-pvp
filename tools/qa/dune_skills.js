// dune.html "ตำนานมังกรทราย": screenshots of every skill (frozen game clock, stepped by hand) + a map tour, no web server needed
// (the page is served from the repo through page.route).
//   node tools/qa/dune_skills.js skills [out=/tmp/dune] [hero=moon] [w=1280] [h=720]   -> <out>/<key>_<n>.png for each skill + errors
//   node tools/qa/dune_skills.js map    [out=/tmp/dune] [hero=moon] [w=1280] [h=720]   -> <out>/map_<x>.png along the field
//   node tools/qa/dune_skills.js perf   [hero=moon] [w=740] [h=360]                      -> frame time of draw() at a few places
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..'), TYPES = { html: 'text/html', js: 'text/javascript', json: 'application/json', webp: 'image/webp', png: 'image/png', mp3: 'audio/mpeg', ogg: 'audio/ogg', wav: 'audio/wav', css: 'text/css', woff2: 'font/woff2', ttf: 'font/ttf' };
(async () => {
  const what = process.argv[2] || 'skills', out = what === 'perf' ? null : (process.argv[3] || '/tmp/dune'), hero = process.argv[what === 'perf' ? 3 : 4] || 'moon', W = +(process.argv[what === 'perf' ? 4 : 5] || (what === 'perf' ? 740 : 1280)), H = +(process.argv[what === 'perf' ? 5 : 6] || (what === 'perf' ? 360 : 720));
  if (out) fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, hasTouch: W < 900, isMobile: false }), pg = await ctx.newPage();
  await pg.route('http://dune.local/**', r => { const u = new URL(r.request().url()), f = path.join(ROOT, decodeURIComponent(u.pathname)); if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' }); r.fulfill({ status: 200, body: fs.readFileSync(f), contentType: TYPES[path.extname(f).slice(1)] || 'application/octet-stream' }); });
  await pg.route(/^https?:\/\/(?!dune\.local)/, r => r.abort());   /* no outside fonts / CDNs in the check */
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errs.push('console: ' + m.text()); });
  await pg.goto(`http://dune.local/${process.env.PAGE || 'dune.html'}?hero=${hero}&test=1&snd=0${process.env.Q || ''}`, { waitUntil: 'domcontentloaded' }); await pg.waitForFunction(() => window.DUNE && DUNE.ready, null, { timeout: 120000 });
  await pg.evaluate(() => { DUNE.begin(true); DUNE.G.state = 'qa'; DUNE.P.lv = 10; });   /* 'qa' = the page loop only draws; the clock moves when this script steps it */
  const step = (s, dt = 1 / 60) => pg.evaluate(([s, dt]) => { for (let t = 0; t < s; t += dt) DUNE.stepWorld(dt); DUNE.draw(); }, [s, dt]);
  if (what === 'skills') {
    const keys = await pg.evaluate(() => DUNE.SKILLS.map(s => s.key));
    for (const k of ['J', ...keys]) {
      await pg.evaluate(() => { const { P, G } = DUNE; Object.assign(P, { x: 2740, y: 1200, vx: 0, vy: 0, dir: 1, st: 'idle', a: 'hero_idle', f: 0, cds: {}, mp: 999, hp: 9999, dead: false, awake: 0, clone: 0 }); for (const L of ['fx', 'rings', 'slashes', 'impacts', 'ghosts', 'mw', 'mbl', 'msl', 'msig', 'cuts', 'pools', 'parts', 'nums', 'after']) if (G[L]) G[L].length = 0; G.night = null; G.fz = G.fzT = 0;
        G.mobs = []; for (let i = 0; i < 5; i++) { const m = DUNE.spawn([['scorpion', 'wolf', 'mummy'][i % 3], 2830 + i * 70, 2831 + i * 70, 1200]); m.elite = false; m.hp = m.max = 1e7; m.x = 2830 + i * 70; m.wait = 99; G.mobs.push(m); } G.camX = P.x + 54 - innerWidth * DUNE.VIEW_H / innerHeight / 2; G.shake = 0; G.dim = 0; });
      await step(.6);
      if (k === 'J') { for (let i = 0; i < 3; i++) { await pg.evaluate(() => { DUNE.I.attack = 1; DUNE.EDGE.attack = 1; }); await step(.12); await pg.evaluate(() => { DUNE.I.attack = 0; }); await pg.screenshot({ path: `${out}/J_${i}.png` }); await step(.2); } continue; }
      await pg.evaluate(k => { const S = DUNE.SKILLS.find(s => s.key === k); DUNE.useSkill(S); }, k);
      const T = [.1, .25, .4, .6, .85, 1.1, 1.45];
      let last = 0; for (let i = 0; i < T.length; i++) { await step(T[i] - last); last = T[i]; await pg.evaluate(() => { DUNE.G.shake = 0; DUNE.draw(); }); await pg.screenshot({ path: `${out}/${k}_${i}.png` }); }
    }
  } else if (what === 'map') {
    const mapw = await pg.evaluate(() => DUNE.MAPW || 10080);
    for (let x = 300; x < mapw; x += 900) { await pg.evaluate(x => { const { P, G } = DUNE; Object.assign(P, { x, y: 1200, vx: 0, vy: 0, hp: 9999, dead: false }); G.mobs.forEach(m => m.wait = 99); G.camX = x - 400; }, x); await step(1.2); await pg.screenshot({ path: `${out}/map_${String(x).padStart(5, '0')}.png` }); }
  } else {
    for (const x of [600, 2600, 5200, 8200]) { await pg.evaluate(x => { Object.assign(DUNE.P, { x, y: 1200, hp: 9999 }); }, x); await step(1); const ms = await pg.evaluate(() => { const t0 = performance.now(); for (let i = 0; i < 60; i++) { DUNE.stepWorld(1 / 60); DUNE.draw(); } return (performance.now() - t0) / 60; }); console.log(`x=${x}: ${ms.toFixed(2)} ms a frame (step + draw)`); }
  }
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 12).join('\n') : 'no errors'); await b.close();
})();
