// Plays tribe3d.html as a game: title screen click, villagers gathering, building with the build bar (real clicks), a night raid
// at high speed (towers shoot, villagers fight), the dawn. Collects errors and saves screenshots.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_game.js [folder for screenshots]
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const run = (sec, dt = .05) => pg.evaluate(([sec, dt]) => { TB.hold = true; for (let t = 0; t < sec; t += dt) TB.step(dt); TB.draw(); }, [sec, dt]);
  try {
    await pg.goto('http://localhost:8000/tribe3d.html'); await pg.waitForFunction(() => window.TB && TB.ready && document.querySelector('.gScreen'), null, {timeout: 60000});
    await pg.waitForFunction(() => TB.animalsReady, null, {timeout: 90000});
    await shot('g01_title');
    await pg.locator('.gScreen button').first().click(); await pg.waitForTimeout(500);
    log.push('started: ' + JSON.stringify(await pg.evaluate(() => ({ on: GAME.on, vill: GAME.G.vill.length, b: GAME.G.buildings.length, nodes: GAME.G.nodes.length, res: GAME.G.res }))));
    await pg.evaluate(() => { TB.hold = false; }); await pg.waitForTimeout(1500); await shot('g02_start');
    await run(25);
    log.push('after 25 s: ' + JSON.stringify(await pg.evaluate(() => ({ res: GAME.G.res, states: GAME.G.vill.map(v => v.st).join(',') }))));
    await pg.evaluate(() => { TB.hold = false; }); await pg.waitForTimeout(800); await shot('g03_gather');
    // build a hut with real clicks: build button -> hut card -> tap ground -> confirm
    await pg.evaluate(() => GAME.cheat.res(400));
    await pg.locator('#gBuildBtn').click(); await pg.waitForTimeout(300); await shot('g04_bar');
    await pg.locator('.gCard[data-t="hut"]').click(); await pg.waitForTimeout(300);
    // pan the camera onto a free spot (as a player would), then tap the middle of the screen
    const sp = await pg.evaluate(() => { const p = GAME.spot('hut'); if (p) TB.camT.set(p.x, 0, p.z); TB.hold = false; return p; });
    await pg.waitForTimeout(600);
    await pg.mouse.click(422, 175); await pg.waitForTimeout(300);
    let placed = await pg.evaluate(() => GAME.G.ghostOk);
    if (!placed) for (const [x, y] of [[400, 160], [450, 190], [380, 200], [470, 150]]) { await pg.mouse.click(x, y); await pg.waitForTimeout(200); if (await pg.evaluate(() => GAME.G.ghostOk)) { placed = true; break; } }
    log.push('ghost ok: ' + placed + ' tip: ' + await pg.locator('#gTip').textContent());
    await shot('g05_ghost');
    const nb = await pg.evaluate(() => GAME.G.buildings.length);
    if (placed) { await pg.locator('#gOk').click(); await pg.waitForTimeout(300); }
    log.push('buildings ' + nb + ' -> ' + await pg.evaluate(() => GAME.G.buildings.length) + ', popCap ' + await pg.evaluate(() => GAME.G.popCap));
    await pg.locator('#gNo').click(); await pg.waitForTimeout(200);
    // night raid
    await pg.evaluate(() => { GAME.cheat.night(); });
    await run(1); log.push('night: ' + JSON.stringify(await pg.evaluate(() => ({ raid: GAME.G.raid && GAME.G.raid.list.length, en: GAME.G.enemies.length }))));
    await run(14); await pg.evaluate(() => { TB.hold = false; }); await pg.waitForTimeout(900); await shot('g06_raid');
    log.push('raid +15 s: ' + JSON.stringify(await pg.evaluate(() => ({ en: GAME.G.enemies.length, alive: GAME.G.enemies.filter(e => !e.dead).length, killed: GAME.G.killed, shots: GAME.G.shots.length, vill: GAME.G.vill.length, hall: Math.round(GAME.G.hall.hp) }))));
    await run(50); log.push('end of night: ' + JSON.stringify(await pg.evaluate(() => ({ day: GAME.G.day, t: Math.round(GAME.G.t), killed: GAME.G.killed, vill: GAME.G.vill.length, b: GAME.G.buildings.length, res: GAME.G.res }))));
    await run(10); await pg.evaluate(() => { TB.hold = false; }); await pg.waitForTimeout(800); await shot('g07_dawn');
    log.push('dawn: ' + JSON.stringify(await pg.evaluate(() => ({ day: GAME.G.day, en: GAME.G.enemies.length, over: GAME.G.over }))));
    // boss night
    await pg.evaluate(() => { GAME.cheat.day(5); GAME.cheat.night(); }); await run(1); await run(20);
    await pg.evaluate(() => { const e = GAME.G.enemies.find(x => x.def.boss); if (e) TB.camT.set(e.x, 0, e.z); TB.hold = false; }); await pg.waitForTimeout(900); await shot('g08_boss');
    log.push('boss night: ' + JSON.stringify(await pg.evaluate(() => ({ boss: (GAME.G.enemies.find(x => x.def.boss) || {}).kind, en: GAME.G.enemies.length, over: GAME.G.over }))));
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
