// All KayKit adventurers as units in tribe3d.html: warriors (knight) + crossbow hunters (hooded rogue) from the fort,
// shamans (mage) from the hall. Real taps on the panels; a night fight: bolts fly, the shaman heals; screenshots.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_units.js [folder for screenshots]
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const run = (sec, dt = .05) => pg.evaluate(([sec, dt]) => { TB.hold = true; for (let t = 0; t < sec; t += dt) TB.step(dt); TB.draw(); }, [sec, dt]);
  const tapAt = async (o) => { await pg.evaluate(o => { TB.camT.set(o.x, 0, o.z); TB.hold = false; }, o); await pg.waitForTimeout(400); await pg.mouse.click(422, 195); await pg.waitForTimeout(300); };
  try {
    await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && TB.animalsReady && GAME.PEOPLE.ready, null, {timeout: 150000});
    log.push('templates: ' + await pg.evaluate(() => ['warrior', 'hunter', 'shaman'].map(k => k + ':' + (GAME.PEOPLE.tpl[k] !== GAME.PEOPLE.tpl.chief)).join(' ')));
    const fort = await pg.evaluate(() => { const G = GAME.G; GAME.cheat.res(3000); GAME.tryUpgrade(G.hall); const p = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = p; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); return p; });
    await run(25);
    await tapAt(fort); log.push('fort panel: ' + await pg.locator('#gSel').textContent());
    for (const id of ['#gTr', '#gTr', '#gTrH', '#gTrH']) { if (await pg.locator(id).count()) await pg.locator(id).click(); await pg.waitForTimeout(150); }
    await pg.evaluate(() => { GAME.select(GAME.G.hall); TB.hold = false; }); await pg.waitForTimeout(300); log.push('hall panel: ' + await pg.locator('#gSel').textContent());
    if (await pg.locator('#gTrS').count()) await pg.locator('#gTrS').click();
    await run(30); log.push('units: ' + await pg.evaluate(() => GAME.G.sol.map(s => s.kind).join(',') + ' | hud ' + document.getElementById('gR_sol').textContent));
    await pg.evaluate(o => { TB.camT.set(o.x, 0, o.z + 4); TB.zoomBy(3); TB.hold = false; }, fort); await pg.waitForTimeout(900); await shot('u01_units_by_fort'); await pg.evaluate(() => TB.zoomBy(-3));
    // night: a pack right in front of the fort
    await pg.evaluate(o => { const G = GAME.G; GAME.cheat.night(); TB.hold = true; TB.step(.2); G.raid = null; for (let i = 0; i < 6; i++) GAME.spawnEnemy(i % 2 ? 'wolf' : 'tribal', o.x + 22 + (i % 3) * 2, o.z + (i / 3 | 0) * 3); for (const s of G.sol) s.hp *= .6; }, fort);
    let bolts = 0; for (let i = 0; i < 40; i++) { await run(.25); bolts += await pg.evaluate(() => GAME.G.shots.length); }
    await pg.evaluate(o => { TB.camT.set(o.x + 12, 0, o.z); TB.zoomBy(2); TB.draw(); }, fort); await shot('u02_night_fight'); await pg.evaluate(() => TB.zoomBy(-2));
    log.push('fight: ' + JSON.stringify(await pg.evaluate(() => ({ alive: GAME.G.enemies.filter(e => !e.dead).length, killed: GAME.G.killed, units: GAME.G.sol.map(s => s.kind[0] + Math.round(s.hp / s.max * 100)).join(','), healed: GAME.G.healN || 0, moves: [...new Set(GAME.G.sol.map(s => s.cur))].join(',') }))) + ' bolts seen ' + bolts);
    await run(20);
    // save -> reload -> continue keeps the kinds
    await pg.evaluate(() => GAME.save()); await pg.goto('http://localhost:8000/tribe3d.html'); await pg.waitForFunction(() => window.TB && TB.ready && document.querySelector('.gScreen'), null, {timeout: 150000});
    await pg.waitForFunction(() => GAME.PEOPLE.ready, null, {timeout: 60000}); await pg.locator('.gScreen button').first().click(); await pg.waitForTimeout(800);
    log.push('continued: ' + await pg.evaluate(() => GAME.G.sol.map(s => s.kind).join(',')));
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
