// pixmap.html combat check: the dragon is moved next to a monster pack, then the combo and each skill are used; a screenshot at each hit moment,
// damage dealt, kills, XP / level, hero HP, page errors. python3 -m http.server 8000 ; node tools/qa/pixmap_fight.js [out=/tmp/pixfight] [scale=1] [hero=dragon|archer]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/pixfight', dsf = +(process.argv[3] || 1); require('fs').mkdirSync(out, { recursive: true }); const errs = [];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf })).newPage();
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  const hero = process.argv[4] || 'dragon'; await pg.goto('http://localhost:8000/pixmap.html?hero=' + hero, { waitUntil: 'load', timeout: 180000 });
  await pg.waitForFunction(() => window.MAP && MAP.MOBS.length > 10 && MAP.renderer.info.render.frame > 3, null, { timeout: 180000 }); await pg.waitForTimeout(1500);
  const pack = await pg.evaluate(() => { const M = MAP, H = M.HERO, m = M.MOBS.find(m => m.k === 'wolf' || m.k === 'scorp') || M.MOBS[0]; H.x = m.x + (MAP.SK.a1.range ? 5 : 2.2); H.z = m.z + .6; H.y = M.groundH(H.x, H.z); M.CAM.look.set(H.x * M.WS, H.y * M.WS + .5, H.z * M.WS);
    return { mobs: M.MOBS.length, packs: new Set(M.MOBS.map(m => m.P)).size, kinds: [...new Set(M.MOBS.map(m => m.k))].join(','), at: m.k }; });
  console.log('monsters', JSON.stringify(pack)); await pg.waitForTimeout(900); await pg.screenshot({ path: `${out}/0_pack.png` });
  const hpSum = () => pg.evaluate(() => MAP.MOBS.reduce((s, m) => s + Math.max(0, m.dead ? 0 : m.hp), 0));
  const sim = sec => pg.evaluate(s => { MAP.paused = true; MAP.sim(s); }, sec);   /* game time, not wall time (the check browser draws slowly) */
  const shot = async (name, fn, wait) => { const h0 = await hpSum(); await pg.evaluate(fn); await sim(wait / 1000); await pg.waitForTimeout(400); await pg.screenshot({ path: `${out}/${name}.png` }); await sim(.5); const h1 = await hpSum(); console.log(name, 'damage', Math.round(h0 - h1)); };
  const T = hero === 'archer' ? [380, 520, 560, 560, 900, 900] : [310, 310, 420, 380, 820, 640];
  await shot('1_thrust', () => MAP.heroAttack(), T[0]);
  await sim(.02); await shot('2_sweep', () => { MAP.heroAttack(); }, T[1]);
  await sim(.02); await shot('3_slam', () => { MAP.heroAttack(); }, T[2]);
  await sim(.6); await shot('4_dash', () => MAP.heroSkill('dash'), T[3]);
  await sim(.7); await shot('5_rain', () => MAP.heroSkill('rain'), T[4]);
  await sim(.8); await shot('6_ring', () => MAP.heroSkill('ring'), T[5]);
  await sim(2.5); await pg.waitForTimeout(400); await pg.screenshot({ path: `${out}/7_after.png` });
  console.log('after', JSON.stringify(await pg.evaluate(() => ({ lv: MAP.HERO.lv, xp: MAP.HERO.xp, hp: Math.round(MAP.HERO.hp), dead: MAP.MOBS.filter(m => m.dead).length, cd: MAP.HERO.cd }))));
  if (errs.length) console.log('ERRORS:\n' + [...new Set(errs)].slice(0, 12).join('\n')); else console.log('no errors'); await b.close();
})();
