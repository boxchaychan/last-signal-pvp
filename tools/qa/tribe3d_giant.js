// The forest giant (comes every night from night 2, never dies: hurt -> flees, grows), stone walls (upgrade all), urgent
// repair button at night. Real taps where it matters; screenshots.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_giant.js [folder for screenshots]
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const run = (sec, dt = .05) => pg.evaluate(([sec, dt]) => { TB.hold = true; for (let t = 0; t < sec; t += dt) TB.step(dt); TB.draw(); }, [sec, dt]);
  try {
    await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && TB.animalsReady && GAME.PEOPLE.ready, null, {timeout: 150000});
    // a small base: hall 2, 4 walls in front of tonight's banner, a fort with soldiers
    log.push('setup: ' + await pg.evaluate(() => {
      const G = GAME.G; GAME.cheat.res(2000); GAME.tryUpgrade(G.hall); GAME.cheat.day(3); GAME.planWave();
      const p = G.next.pts[0], h = G.hall, d = Math.hypot(p.x - h.x, p.z - h.z), ux = (p.x - h.x) / d, uz = (p.z - h.z) / d;
      for (let i = -2; i <= 1; i++) { const x = h.x + ux * 30 - uz * i * 5.6, z = h.z + uz * 30 + ux * i * 5.6; GAME.startBuild('wall'); G.ghostAt = { x, z }; G.ghostOk = true; G.ghost.rotation.y = Math.atan2(ux, uz) + Math.PI / 2; GAME.confirmBuild(); }
      const fp = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = fp; G.ghostOk = true; GAME.confirmBuild(); GAME.startBuild('wall'); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown'));
      return G.next.list.join(',') + ' | clock ' + document.getElementById('gPh').textContent; }));
    await run(40); await pg.evaluate(() => { for (const f of GAME.forts()) GAME.train(f, 99); }); await run(30);
    log.push('built: ' + await pg.evaluate(() => GAME.G.buildings.map(b => b.type + (b.site ? '@' : '')).join(',') + ' soldiers ' + GAME.G.sol.length));
    // upgrade all walls with real taps: tap a wall, "อัปเกรดทุกช่วง"
    await pg.evaluate(() => { const w = GAME.G.buildings.find(b => b.type === 'wall'); TB.camT.set(w.x, 0, w.z); TB.hold = false; }); await pg.waitForTimeout(500);
    await pg.mouse.click(422, 195); await pg.waitForTimeout(300); log.push('wall panel: ' + await pg.locator('#gSel').textContent());
    if (await pg.locator('#gUpAll').count()) await pg.locator('#gUpAll').click(); await pg.waitForTimeout(300);
    log.push('walls: ' + await pg.evaluate(() => GAME.G.buildings.filter(b => b.type === 'wall').map(b => (b.lv || 1) + ':' + b.max).join(',')));
    await pg.evaluate(() => TB.zoomBy(1)); await pg.waitForTimeout(600); await shot('g01_stone_walls'); await pg.evaluate(() => TB.zoomBy(-1));
    // night 2: the giant comes
    await pg.evaluate(() => { TB.hold = true; GAME.cheat.night(); }); await run(1); await run(21);
    const gi = await pg.evaluate(() => { const g = GAME.G.enemies.find(e => e.def.giant); if (g) TB.camT.set(g.x, 0, g.z); TB.draw(); return g ? { lv: g.lv, hp: Math.round(g.hp), max: Math.round(g.max), flee: !!g.flee, anim: g.cur } : null; });
    log.push('giant: ' + JSON.stringify(gi)); await shot('g02_giant');
    log.push('repair button: ' + await pg.evaluate(() => { const b = document.getElementById('gFix'); return b.style.display + ' ' + b.textContent; }));
    if (await pg.locator('#gFix').isVisible()) await pg.locator('#gFix').click();
    await run(50); log.push('end of night: ' + JSON.stringify(await pg.evaluate(() => ({ giantLv: GAME.G.giantLv, beat: GAME.G.giantBeat, walls: GAME.G.buildings.filter(b => b.type === 'wall').length, sol: GAME.G.sol.length, hall: Math.round(GAME.G.hall.hp), over: GAME.G.over }))));
    await run(40); log.push('next day: ' + JSON.stringify(await pg.evaluate(() => ({ day: GAME.G.day, giantLv: GAME.G.giantLv, next: GAME.G.next.list.slice(-2).join(','), clock: document.getElementById('gPh').textContent }))));
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
