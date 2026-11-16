// The base-builder opening of tribe3d.html (batch 10) with real taps: start from scratch (hall + 4 villagers), quest panel ->
// build a hut -> villagers walk over and build it -> quests advance; tonight's banners / arrows; "call them now"; the night
// comes from the banners; hall upgrade unlocks more. Prints the state, saves screenshots.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_base.js [folder for screenshots]
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const run = (sec, dt = .05) => pg.evaluate(([sec, dt]) => { TB.hold = true; for (let t = 0; t < sec; t += dt) TB.step(dt); TB.draw(); }, [sec, dt]);
  const st = () => pg.evaluate(() => { const G = GAME.G; return { day: G.day, t: Math.round(G.t), q: G.q, b: G.buildings.map(b => b.type + (b.site ? '@' + Math.round(b.prog * 100) : '')).join(','), vill: G.vill.length, cap: G.popCap, hall: GAME.hallLv(), res: Object.values(G.res).map(Math.round).join('/'), en: G.enemies.filter(e => !e.dead).length, sol: G.sol.length, kill: G.killed }; });
  const tapGround = async () => { for (const [x, y] of [[422, 200], [380, 230], [470, 180], [350, 170], [500, 240], [300, 220]]) { await pg.mouse.click(x, y); await pg.waitForTimeout(150); if (await pg.evaluate(() => GAME.G.ghostOk)) return true; } return false; };
  try {
    await pg.goto('http://localhost:8000/tribe3d.html'); await pg.waitForFunction(() => window.TB && TB.ready && document.querySelector('.gScreen') && TB.animalsReady, null, {timeout: 90000});
    await pg.evaluate(() => localStorage.clear());
    await pg.locator('.gScreen button').first().click(); await pg.waitForTimeout(800);
    log.push('start: ' + JSON.stringify(await st()) + ' quest: ' + await pg.locator('#gQ').textContent());
    log.push('wave: ' + JSON.stringify(await pg.evaluate(() => ({ pts: GAME.G.next.pts.length, list: GAME.G.next.list.join(','), clock: document.getElementById('gPh').textContent }))));
    await pg.evaluate(() => { TB.zoomBy(-1); TB.hold = false; }); await pg.waitForTimeout(900); await shot('b01_start');
    // quest 1 = hut: tap the quest panel, tap the ground, confirm
    await pg.evaluate(() => { const p = GAME.spot('hut'); TB.camT.set(p.x, 0, p.z); });
    await pg.locator('#gQ').click(); await pg.waitForTimeout(300);
    log.push('quest tap -> mode ' + await pg.evaluate(() => GAME.G.mode));
    if (await tapGround()) { await pg.locator('#gOk').click(); await pg.waitForTimeout(200); }
    await pg.locator('#gNo').click();
    log.push('placed: ' + JSON.stringify(await st()));
    await run(4); await pg.evaluate(() => { const s = GAME.G.buildings.find(b => b.site); if (s) TB.camT.set(s.x, 0, s.z); TB.zoomBy(2); TB.draw(); }); await shot('b02_building');
    await run(14); log.push('after 18 s: ' + JSON.stringify(await st()));
    // tower by quest (cheat resources so the test does not wait)
    await pg.evaluate(() => { GAME.cheat.res(300); TB.zoomBy(-2); const p = GAME.spot('tower'); TB.camT.set(p.x, 0, p.z); TB.draw(); });
    await pg.locator('#gQ').click(); await pg.waitForTimeout(200); if (await tapGround()) await pg.locator('#gOk').click(); await pg.locator('#gNo').click();
    log.push('cap check: ' + JSON.stringify(await pg.evaluate(() => ({ tower: GAME.countOf('tower') + '/' + GAME.capOf('tower'), why: (GAME.startBuild('tower'), document.getElementById('gTip').textContent) }))));
    await pg.locator('#gNo').click();
    await run(20); log.push('after tower: ' + JSON.stringify(await st()));
    // quest: fort, then quest: train soldiers (the quest panel selects the fort, "ฝึกให้เต็ม")
    await pg.evaluate(() => { GAME.cheat.res(300); const p = GAME.spot('fort'); TB.camT.set(p.x, 0, p.z); TB.draw(); });
    await pg.locator('#gQ').click(); await pg.waitForTimeout(200); log.push('fort quest -> mode ' + await pg.evaluate(() => GAME.G.mode));
    if (await tapGround()) await pg.locator('#gOk').click(); await pg.locator('#gNo').click();
    await run(20); log.push('after fort: ' + JSON.stringify(await st()));
    await pg.evaluate(() => { TB.hold = false; }); await pg.locator('#gQ').click(); await pg.waitForTimeout(300);
    log.push('fort panel: ' + await pg.locator('#gSel').textContent());
    if (await pg.locator('#gTrAll').count()) await pg.locator('#gTrAll').click();
    await run(26); log.push('soldiers: ' + await pg.evaluate(() => GAME.G.sol.length + ' hud ' + document.getElementById('gR_sol').textContent + ' quest ' + GAME.G.q));
    await pg.evaluate(() => { const f = GAME.forts()[0]; TB.camT.set(f.x, 0, f.z); TB.zoomBy(2); TB.hold = false; }); await pg.waitForTimeout(900); await shot('b06_fort'); await pg.evaluate(() => TB.zoomBy(-2));
    // the wave preview from far out, then call them now
    await pg.evaluate(() => { const p = GAME.G.next.pts[0], h = GAME.G.hall; TB.camT.set((p.x + h.x) / 2, 0, (p.z + h.z) / 2); TB.zoomBy(-1); TB.hold = false; }); await pg.waitForTimeout(900); await shot('b03_wave_preview');
    await pg.evaluate(() => { TB.hold = true; }); await pg.locator('#gGo').click(); log.push('called early: ' + JSON.stringify(await st()));
    await run(14); const sp = await pg.evaluate(() => { const p = GAME.G.next.pts[0]; return GAME.G.enemies.map(e => Math.round(Math.min(...GAME.G.next.pts.map(q => Math.hypot(q.x - e.x, q.z - e.z))))).join(','); });
    log.push('night: ' + JSON.stringify(await st()) + ' enemy distance from banners: ' + sp);
    await pg.evaluate(() => { const e = GAME.G.enemies.find(e => !e.dead); if (e) TB.camT.set(e.x, 0, e.z); TB.draw(); }); await shot('b04_night');
    log.push('night fight: soldiers ' + await pg.evaluate(() => GAME.G.sol.map(x => x.cur || '').join(',') + ' villagers sitting ' + GAME.G.vill.filter(v => v.sit).length + '/' + GAME.G.vill.length + ' food ' + Math.round(GAME.G.res.food)));
    await pg.evaluate(() => { const v = GAME.G.vill.find(v => v.sit) || GAME.G.vill[0]; TB.camT.set(v.x, 0, v.z); TB.zoomBy(2); TB.draw(); }); await shot('b07_night_fire'); await pg.evaluate(() => TB.zoomBy(-2));
    await run(70); log.push('dawn: ' + JSON.stringify(await st()) + ' soldiers ' + await pg.evaluate(() => GAME.G.sol.length));
    // hall upgrade with a real tap on the hall
    await pg.evaluate(() => { GAME.cheat.res(400); const h = GAME.G.hall; TB.camT.set(h.x, 0, h.z); TB.hold = false; }); await pg.waitForTimeout(500);
    await pg.mouse.click(422, 195); await pg.waitForTimeout(300); log.push('hall panel: ' + await pg.locator('#gSel').textContent());
    if (await pg.locator('#gUp').count()) await pg.locator('#gUp').click(); await pg.waitForTimeout(300);
    log.push('after upgrade: ' + JSON.stringify(await st()) + ' tower cap ' + await pg.evaluate(() => GAME.capOf('tower')) + ' quest: ' + await pg.locator('#gQ').textContent());
    await shot('b05_hall2');
    // save -> reload -> continue
    await pg.reload(); await pg.waitForFunction(() => window.TB && TB.ready && document.querySelector('.gScreen'), null, {timeout: 90000});
    await pg.locator('.gScreen button').first().click(); await pg.waitForTimeout(800); log.push('continued: ' + JSON.stringify(await st()));
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
