// Chief's skills in tribe3d.html with real clicks: spear rain (tap button -> tap the pack), fire pot (day 2), war drum (day 3).
// Checks damage, cooldowns, effect sprites, no errors; saves screenshots mid-effect.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_skills.js [folder for screenshots]
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const run = (sec, dt = .05) => pg.evaluate(([sec, dt]) => { TB.hold = true; for (let t = 0; t < sec; t += dt) TB.step(dt); TB.draw(); }, [sec, dt]);
  // a pack of 6 beasts just outside the east gate, held still, camera on them; returns the pack centre on screen
  const pack = (kinds) => pg.evaluate((kinds) => {
    const G = GAME.G; for (const e of G.enemies) { e.dead = true; e.gone = true; TB.scene.remove(e.root); if (e.ring) TB.scene.remove(e.ring); } G.enemies = []; G.raid = null;
    const h = G.hall, cx = h.x + 40, cz = h.z + 2;
    kinds.forEach((k, i) => { const e = GAME.spawnEnemy(k, cx + (i % 3) * 2.2 - 2, cz + (i / 3 | 0) * 2.4 - 1); if (e) e.target = { x: e.x, z: e.z, r: 0, dead: false }; });
    TB.camT.set(cx - 4, 0, cz); TB.hold = true; TB.draw();
    const v = new THREE.Vector3(cx, groundY(cx, cz) + .5, cz).project(cam), rc = document.querySelector('canvas').getBoundingClientRect();
    return { x: (v.x + 1) / 2 * rc.width + rc.left, y: (1 - v.y) / 2 * rc.height + rc.top, hp: G.enemies.reduce((s, e) => s + e.hp, 0) };
  }, kinds);
  const state = () => pg.evaluate(() => ({ alive: GAME.G.enemies.filter(e => !e.dead).length, hp: Math.round(GAME.G.enemies.filter(e => !e.dead).reduce((s, e) => s + e.hp, 0)), cd: Object.fromEntries(Object.entries(GAME.G.cd).map(([k, v]) => [k, +v.toFixed(1)])), fx: GAME.fxCount, aim: GAME.G.aim, buff: +GAME.G.buff.toFixed(1) }));
  try {
    await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && TB.animalsReady, null, {timeout: 150000});
    await pg.waitForTimeout(1500);
    await pg.evaluate(() => { GAME.cheat.night(); TB.hold = true; TB.step(.2); GAME.G.raid = null; });
    // 1. spear rain with real clicks
    let p = await pack(['wolf', 'wolf', 'wolf', 'fox', 'fox', 'wolf']);
    log.push('pack hp ' + Math.round(p.hp));
    await pg.locator('.sk[data-k="spear"]').click(); log.push('after button: ' + JSON.stringify(await state()));
    await pg.evaluate(() => TB.draw()); await shot('s01_aim');
    await pg.mouse.click(p.x, p.y); log.push('after tap: ' + JSON.stringify(await state()));
    await run(.75); await shot('s02_spears');
    await run(.7); await shot('s03_slam');
    await run(1.5); log.push('spear rain done: ' + JSON.stringify(await state()));
    // 2. fire pot (unlocks on day 2)
    await pg.evaluate(() => { GAME.cheat.day(2); });
    p = await pack(['bull', 'wolf', 'wolf', 'stag', 'fox', 'wolf']); log.push('pack2 hp ' + Math.round(p.hp));
    await pg.locator('.sk[data-k="pot"]').click(); await pg.mouse.click(p.x, p.y);
    await run(1.05); await shot('s04_pot_boom');
    await run(1.6); await shot('s05_fire_zone');
    await run(4); log.push('fire pot done: ' + JSON.stringify(await state()));
    // 3. war drum (day 3): villagers buffed
    await pg.evaluate(() => { GAME.cheat.day(3); TB.camT.set(GAME.G.hall.x + 6, 0, GAME.G.hall.z); });
    await pg.locator('.sk[data-k="drum"]').click(); await run(.6); await shot('s06_drum');
    log.push('drum: ' + JSON.stringify(await state()));
    // locked / cooldown handling: pressing a cooling skill does not aim
    await pg.locator('.sk[data-k="spear"]').click(); log.push('spear during cooldown -> aim = ' + (await state()).aim);
    await run(13); log.push('after buff: ' + JSON.stringify(await state()));
    // the auto-caster used by the balance run
    await pg.evaluate(() => { for (const k in GAME.G.cd) GAME.G.cd[k] = 0; });
    p = await pack(['wolf', 'wolf', 'wolf', 'wolf']); log.push('autoCast: ' + await pg.evaluate(() => GAME.autoCast())); await run(8); log.push('after autoCast: ' + JSON.stringify(await state()));
    await pg.evaluate(() => { TB.hold = false; }); await pg.waitForTimeout(600); await shot('s07_hud');
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
