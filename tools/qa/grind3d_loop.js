// grind3d.html grinding-loop check: packs spawn, kills fill the zone bar, the boss comes with red ground warnings, beating it opens zone 2,
// gold -> shop, zone 2 loads its monsters, the save restores. python3 -m http.server 8000 ; node tools/qa/grind3d_loop.js [out_dir] [hero]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const out = process.argv[2] || '.', hero = process.argv[3] || 'wing'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 844, height: 390 } }); const pg = await ctx.newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto(`http://localhost:8000/grind3d.html?snd=0&reset=1&hero=${hero}`); await pg.waitForFunction(() => window.GAME && GAME.P.ready && GAME.G.ready, null, { timeout: 120000 });
  await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/l1_start.png` });
  const sim = (sec, fn) => pg.evaluate(([sec, fn]) => { if (fn) eval(fn); GAME.sim(sec); }, [sec, fn || null]).then(() => pg.waitForTimeout(60));
  const st = () => pg.evaluate(() => ({ lv: GAME.P.lv, hp: Math.round(GAME.P.hp), max: GAME.P.max, dmg: GAME.P.dmg, kills: GAME.P.kills, gold: GAME.G.gold, prog: GAME.G.prog, zone: GAME.G.zone, unl: GAME.G.unl, boss: !!GAME.G.boss, mons: GAME.MON.filter(m => !m.dead).length, elites: GAME.MON.filter(m => m.elite).length }));
  // fight with auto-attack on, wander a little; god mode off: a real run
  await sim(.1, 'GAME.api && 0; GAME.IN.keyAtk = true');
  let t0 = 0, bossSeen = false, warnShot = false, deaths = 0;
  for (let i = 0; i < 600; i++) {
    await sim(1, `GAME.IN.keyAtk = true; const m = GAME.MON.filter(q => !q.dead).sort((a, b) => a.pos.distanceTo(GAME.P.pos) - b.pos.distanceTo(GAME.P.pos))[0]; for (const k of 'wasd') GAME.IN.keys[k] = false;
      if (m && m.pos.distanceTo(GAME.P.pos) > 1.8) { const dx = m.pos.x - GAME.P.pos.x, dz = m.pos.z - GAME.P.pos.z; if (Math.abs(dx) > .6) GAME.IN.keys[dx > 0 ? 'd' : 'a'] = true; if (Math.abs(dz) > .6) GAME.IN.keys[dz > 0 ? 's' : 'w'] = true; }
      if (${i} % 5 === 0) GAME.api.skill1(); if (${i} % 7 === 2) GAME.api.skill2();`);
    const s = await st(); if (s.hp === 0) deaths++;
    if (i === 20) await pg.screenshot({ path: `${out}/l2_packs.png` });
    if (s.boss && !bossSeen) { bossSeen = true; t0 = i; console.log('boss at', i, 's', JSON.stringify(s)); await pg.screenshot({ path: `${out}/l3_boss.png` }); }
    if (s.boss && !warnShot && i > t0 + 4) { const w = await pg.evaluate(() => GAME.FX.length); if (w > 6) { warnShot = true; await pg.screenshot({ path: `${out}/l4_warning.png` }); } }
    if (s.unl >= 1) { console.log('boss down at', i, 's', JSON.stringify(s)); await sim(.6); await pg.screenshot({ path: `${out}/l5_win.png` }); break; }
    if (i % 60 === 0) console.log(i, JSON.stringify(s));
  }
  console.log('deaths(sampled)', deaths);
  // shop
  await pg.evaluate(() => { GAME.G.gold += 500; GAME.G.panel = 'shop'; }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/l6_shop.png` });
  const before = await st(); await pg.evaluate(() => { GAME.buy('atk'); GAME.buy('hp'); GAME.buy('crit'); GAME.G.panel = 'zone'; }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/l7_zones.png` });
  const after = await st(); console.log('shop', before.dmg, '->', after.dmg, before.max, '->', after.max);
  await pg.evaluate(() => { GAME.G.panel = null; GAME.setZone(1); }); await pg.waitForFunction(() => GAME.G.ready, null, { timeout: 60000 }); await sim(8); await pg.screenshot({ path: `${out}/l8_zone2.png` });
  for (const z of [2, 3]) { await pg.evaluate(z => { GAME.G.unl = z; GAME.setZone(z); }, z); await pg.waitForFunction(() => GAME.G.ready, null, { timeout: 60000 }); await sim(6); await pg.screenshot({ path: `${out}/l9_zone${z + 1}.png` });
    await pg.evaluate(() => GAME.callBoss()); await sim(5); await pg.screenshot({ path: `${out}/l9_zone${z + 1}_boss.png` }); }
  const z4 = await st(); console.log('zone4', JSON.stringify(z4));
  // save restores
  await pg.evaluate(() => { GAME.setZone(1); }); await pg.waitForTimeout(500);
  await pg.goto(`http://localhost:8000/grind3d.html?snd=0&hero=${hero}`); await pg.waitForFunction(() => window.GAME && GAME.P.ready && GAME.G.ready, null, { timeout: 120000 });
  console.log('after reload', JSON.stringify(await st()));
  console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'no errors'); await b.close();
})();
