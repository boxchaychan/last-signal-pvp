// The tribe chief (owner 2026-11-18: the Tripo winged knight, whole, "เอาไว้เป็นหัวหน้า"): loads, idles, throws for a skill, cheers; close-ups; errors.
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_chief.js [out_dir] [scarf|old]   (scarf = red-scarf hero, old = crimson barbarian)
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const out = process.argv[2] || '.'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1280, height: 720 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (/error/.test(m.type()) || /chief|people|demon knight/.test(m.text())) errs.push(m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0' + (process.argv[3] ? '&chief=' + process.argv[3] : ''));
  await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && GAME.G.chief, null, {timeout: 150000});
  const run = s => pg.evaluate(s => { TB.hold = true; for (let t = 0; t < s; t += .05) TB.step(.05); TB.draw(); }, s);
  const close = (dx = -2) => pg.evaluate(dx => { const c = GAME.G.chief; TB.camT.set(c.x + dx, 0, c.z); TB.draw(); }, dx);
  const info = await pg.evaluate(z => { const T = GAME.PEOPLE.tpl.chief; let n = 0; T.root.traverse(o => { if (o.isSkinnedMesh) n++; }); TB.zoomBy(z); return { meshes: n, h: +T.h.toFixed(2) }; }, +(process.env.ZOOM || 6));
  await run(2); await close(); await pg.waitForTimeout(300); await pg.screenshot({ path: out + '/chief_idle.png' });
  await pg.evaluate(() => { GAME.cheat.night(); TB.step(.2); GAME.G.raid = null; const h = GAME.G.hall; for (let i = 0; i < 4; i++) GAME.spawnEnemy('wolf', h.x + 26 + i * 2, h.z + 6); GAME.cast('spear', h.x + 28, h.z + 6); });
  await run(.45); await close(); await pg.screenshot({ path: out + '/chief_throw.png' });
  await run(10); const moves = await pg.evaluate(() => GAME.G.chief.cur);
  console.log(JSON.stringify({ ...info, lastMove: moves })); console.log('errors:', errs.length ? errs.join(' | ') : 'none'); await b.close(); })();
