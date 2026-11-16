// Animated villagers + chief in tribe3d.html (CC0 KayKit people): they load, replace the old Blender poses, work, fight,
// die and cheer without errors; close-up screenshots.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_people.js [folder for screenshots]
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error' || (m.type() === 'warning' && m.text().startsWith('people'))) errs.push('console ' + m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const run = (sec, dt = .05) => pg.evaluate(([sec, dt]) => { TB.hold = true; for (let t = 0; t < sec; t += dt) TB.step(dt); TB.draw(); }, [sec, dt]);
  const look = (f) => pg.evaluate(f);
  try {
    await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && TB.animalsReady && GAME.PEOPLE.ready, null, {timeout: 150000});
    await pg.waitForTimeout(500);
    log.push('people: ' + JSON.stringify(await look(() => ({ animated: GAME.G.vill.filter(v => v.mixer).length, all: GAME.G.vill.length, chief: !!GAME.G.chief, clips: GAME.PEOPLE.clips.length, calls: TB.renderer.info.render.calls }))));
    await run(14);
    log.push('jobs: ' + await look(() => GAME.G.vill.map(v => v.st + ':' + (v.cur || '')).join(' ')));
    // close-up on a villager at work
    await look(() => { TB.zoomBy(3); const v = GAME.G.vill.find(v => v.st === 'work') || GAME.G.vill[0]; TB.camT.set(v.x, 0, v.z); TB.draw(); });
    await shot('p01_work');
    await look(() => { const c = GAME.G.chief; TB.camT.set(c.x - 3, 0, c.z); TB.draw(); }); await shot('p02_chief');
    // chief throws when a skill is cast, villagers fight at night
    await look(() => { GAME.cheat.night(); TB.step(.2); GAME.G.raid = null; const h = GAME.G.hall; for (let i = 0; i < 5; i++) GAME.spawnEnemy('wolf', h.x + 26 + i * 2, h.z + 6); GAME.cast('spear', h.x + 28, h.z + 6); });
    await run(.45); await look(() => { const c = GAME.G.chief; TB.camT.set(c.x + 4, 0, c.z); TB.draw(); }); await shot('p03_chief_throw');
    await run(6); await look(() => { const e = GAME.G.enemies.find(e => !e.dead) || GAME.G.hall; TB.camT.set(e.x, 0, e.z); TB.draw(); }); await shot('p04_fight');
    log.push('night: ' + JSON.stringify(await look(() => ({ alive: GAME.G.enemies.filter(e => !e.dead).length, vill: GAME.G.vill.length, moves: [...new Set(GAME.G.vill.map(v => v.cur))].join(',') }))));
    // a villager dies (plays the death move), dawn = everyone cheers
    await look(() => { const v = GAME.G.vill[0]; GAME.G.vill[0].hp = 1; v.dead = false; }); await look(() => { /* hurt through the game */ const v = GAME.G.vill[0]; v.hp = 0.5; });
    await look(() => { GAME.G.t = 110 + 10 + 65 - .1; }); await run(1.2);
    await look(() => { TB.zoomBy(-1); const h = GAME.G.hall; TB.camT.set(h.x + 12, 0, h.z); TB.draw(); }); await shot('p05_dawn_cheer');
    log.push('dawn moves: ' + await look(() => [...new Set(GAME.G.vill.map(v => v.cur))].join(',')));
    await look(() => { TB.zoomBy(-2); TB.hold = false; }); await pg.waitForTimeout(1200);
    log.push('fps check: ' + JSON.stringify(await look(() => ({ calls: TB.renderer.info.render.calls, tris: TB.renderer.info.render.triangles }))));
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
