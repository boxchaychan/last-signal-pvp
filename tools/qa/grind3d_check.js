// grind3d.html check: loads, the huntress moves / shoots / dodges / casts both skills, monsters come and die, the move gallery opens; no page errors.
//   python3 -m http.server 8000 ; node tools/qa/grind3d_check.js [out_dir]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const out = process.argv[2] || '.'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/grind3d.html?snd=0&hero=archer'); await pg.waitForFunction(() => window.GAME && GAME.P.ready, null, { timeout: 120000 });
  await pg.waitForTimeout(2500); await pg.screenshot({ path: `${out}/g1_start.png` });
  const sim = (sec, fn) => pg.evaluate(([sec, fn]) => { if (fn) eval(fn); GAME.sim(sec); }, [sec, fn || null]).then(() => pg.waitForTimeout(150));
  // walk right while holding attack (J): shoots the nearest target while moving
  await sim(1, 'GAME.IN.keys.d = true; GAME.IN.keyAtk = true'); await pg.screenshot({ path: `${out}/g2_run_shoot.png` });
  await sim(1.5, 'GAME.IN.keys.d = false'); await sim(.1, 'GAME.IN.keyAtk = false');
  await sim(.15, 'GAME.api.dodge()'); await pg.screenshot({ path: `${out}/g3_dodge.png` }); await sim(.6);
  await sim(.75, 'GAME.api.castRain(new THREE.Vector3(0, 0, -5))'); await pg.screenshot({ path: `${out}/g4_rain.png` }); await sim(1);
  await sim(.5, 'GAME.api.castPierce(new THREE.Vector3(0, 0, -8))'); await pg.screenshot({ path: `${out}/g5_pierce.png` }); await sim(1);
  // monsters come; auto-fire on, kite in a circle, use skills now and then
  await pg.keyboard.press('r');
  for (let i = 0; i < 24; i++) { await sim(1, `GAME.IN.keys.a = ${i % 6 < 3}; GAME.IN.keys.d = ${i % 6 >= 3}; GAME.IN.keys.s = ${i % 4 < 2}; GAME.IN.keys.w = ${i % 4 >= 2}; if (${i % 5} === 0) GAME.api.castRain(); if (${i % 3} === 0) GAME.api.castPierce(); if (${i % 4} === 1) GAME.api.dodge();`); }
  await sim(.2, 'for (const k of "wasd") GAME.IN.keys[k] = false'); await pg.screenshot({ path: `${out}/g6_fight.png` });
  const st = await pg.evaluate(() => ({ ...GAME.P.stats, lv: GAME.P.lv, xp: GAME.P.xp, kills: GAME.P.kills, hp: GAME.P.hp, mons: GAME.MON.length, fx: GAME.FX.length, flying: GAME.ARROWS.length, mode: GAME.P.mode }));
  await pg.keyboard.press('r');
  await pg.evaluate(() => { GAME.api.openGallery(); GAME.api.setPose('Ranged_Bow_Draw'); }); await pg.waitForTimeout(1200); await pg.screenshot({ path: `${out}/g7_gallery.png` });
  await pg.evaluate(() => GAME.api.setPose('Dodge_Forward')); await pg.waitForTimeout(300); await pg.evaluate(() => GAME.api.closeGallery());
  console.log(JSON.stringify(st)); console.log('errors:', errs.length ? errs.join(' | ') : 'none');
  await b.close();
})();
