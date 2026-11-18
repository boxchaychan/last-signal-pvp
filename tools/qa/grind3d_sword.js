// grind3d.html swordsman check (?hero=wing | demon): loads, 3-hit combo on the dummies, กระโดดฟาด, พายุดาบ, dodge, a fight with monsters (auto),
// the move gallery; screenshots + numbers; no page errors.   python3 -m http.server 8000 ; node tools/qa/grind3d_sword.js [out_dir] [wing|demon]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const out = process.argv[2] || '.', hero = process.argv[3] || 'wing'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto(`http://localhost:8000/grind3d.html?snd=0&hero=${hero}`); await pg.waitForFunction(() => window.GAME && GAME.P.ready, null, { timeout: 120000 });
  await pg.waitForTimeout(2000); await pg.screenshot({ path: `${out}/s1_start.png` });
  const sim = (sec, fn) => pg.evaluate(([sec, fn]) => { if (fn) eval(fn); GAME.sim(sec); }, [sec, fn || null]).then(() => pg.waitForTimeout(120));
  const shot = async (n, sec, fn) => { await sim(sec, fn); await pg.screenshot({ path: `${out}/${n}.png` }); };
  // walk to the dummies and hold attack: combo
  const d0 = await pg.evaluate(() => { const d = GAME.DUM[0]; return [d.pos.x, d.pos.z]; });
  await sim(.1, `GAME.IN.keyAtk = true; GAME.P.pos.set(${d0[0]} + 1.6, 0, ${d0[1]} + 1.2)`);
  await shot('s2_slice', .3); await shot('s3_chop', .45); await shot('s4_spin', .7); await sim(.6, 'GAME.IN.keyAtk = false');
  const combo = await pg.evaluate(() => ({ swings: GAME.P.stats.swings, hits: GAME.P.stats.hits, mode: GAME.P.mode }));
  await shot('s5_slam', .5, `GAME.api.castSlam(new THREE.Vector3(${d0[0]}, 0, ${d0[1]}))`); await sim(.8);
  await shot("s6_skill2", .7, "GAME.api.skill2()"); await sim(1.5);
  await sim(.2, 'GAME.api.dodge()');
  // monsters: auto attack on, run in circles, skills now and then
  await pg.keyboard.press('r');
  for (let i = 0; i < 28; i++) await sim(1, `GAME.IN.keys.a = ${i % 8 < 2}; GAME.IN.keys.d = ${i % 8 >= 6}; if (${i % 6} === 0) GAME.api.castSlam(); if (${i % 7} === 3) GAME.api.skill2(); if (${i % 9} === 5) GAME.api.dodge();`);
  await sim(.2, 'for (const k of "wasd") GAME.IN.keys[k] = false'); await pg.screenshot({ path: `${out}/s7_fight.png` });
  const st = await pg.evaluate(() => ({ hero: GAME.HK, ...GAME.P.stats, lv: GAME.P.lv, kills: GAME.P.kills, hp: Math.round(GAME.P.hp), max: GAME.P.max, mons: GAME.MON.length, fx: GAME.FX.length, mode: GAME.P.mode, sword: !!GAME.HERO.sword }));
  await pg.keyboard.press('r');
  await pg.evaluate(() => { GAME.api.openGallery(); GAME.api.setPose('Melee_2H_Attack_Chop'); }); await pg.waitForTimeout(900); await pg.screenshot({ path: `${out}/s8_gallery.png` });
  await pg.evaluate(() => GAME.api.closeGallery());
  console.log(JSON.stringify({ combo, ...st })); console.log('errors:', errs.length ? errs.join(' | ') : 'none');
  await b.close();
})();
