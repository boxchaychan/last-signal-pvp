// guardtd.html check: title (hero cards) -> each hero loads, towers built + upgraded, waves played fast with GAME.sim, the boss wave, pixel mode; screenshots + numbers.
// python3 -m http.server 8000 ; node tools/qa/guardtd_check.js [out_dir] [archer|wing|demon|dark|hood] [waves]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const out = process.argv[2] || '.', hero = process.argv[3] || 'archer', waves = +(process.argv[4] || 6); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/guardtd.html?snd=0&map=' + (process.argv[5] || 'forest') + '&menu=1'); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'title', null, { timeout: 120000 });
  await pg.waitForTimeout(800); await pg.screenshot({ path: `${out}/t1_title.png` });
  await pg.evaluate(h => GAME.pickHero(h), hero); await pg.waitForFunction(() => GAME.G.state === 'play', null, { timeout: 120000 }); await pg.waitForTimeout(600);
  await pg.screenshot({ path: `${out}/t2_start.png` });
  const sim = (sec, fn) => pg.evaluate(([sec, fn]) => { if (fn) eval(fn); GAME.sim(sec); }, [sec, fn || null]).then(() => pg.waitForTimeout(40));
  // build: archer, mage, bomb, knight on the best pads, more as gold comes
  await pg.evaluate(() => { const ks = ['archer', 'knight', 'mage']; GAME.PADS.slice(0, 3).forEach((p, i) => GAME.buildTower(p, ks[i])); });
  await pg.evaluate(() => { const [x, y] = GAME.toScreen(GAME.PADS[3].c.x, .3, GAME.PADS[3].c.z); GAME.tap(x, y); }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/t3_buildmenu.png` });
  await pg.evaluate(() => { GAME.G.menu = null; });
  let shot = 0;
  for (let w = 1; w <= waves; w++) {
    await pg.evaluate(() => GAME.startWave()); await pg.waitForFunction(() => GAME.G.queue.length || GAME.MON.length, null, { timeout: 60000 });
    for (let i = 0; i < 120; i++) { await sim(1, `for (let k = 0; k < 4; k++) GAME.learnSkill(k); if (${i} % 3 === 1) { const m = GAME.MON.filter(q => !q.dead).sort((a, b) => b.s - a.s)[0]; if (m) for (let k = 0; k < 4; k++) GAME.castSkill(k, m.pos.clone()); }`);
      if ((i === 6 || i === 4 && w >= 4) && shot < 5) { shot++; await pg.screenshot({ path: `${out}/t4_wave${w}_${i}.png` }); }
      const st = await pg.evaluate(() => ({ q: GAME.G.queue.length, m: GAME.MON.length, st: GAME.G.state })); if (!st.q && !st.m || st.st !== 'play') break; }
    const s = await pg.evaluate(() => { const G = GAME.G, gold = G.gold; const spend = () => { for (const k of ['bomb', 'archer', 'mage', 'knight']) { const p = GAME.PADS.find(q => !q.tower); if (p && G.gold >= GAME.TDEF[k].cost[0] + 40) GAME.buildTower(p, k); }
      for (const t of GAME.TOWERS) if (t.lv < 2 && G.gold >= t.D.cost[t.lv + 1] + 30) GAME.upgradeTower(t); }; spend();
      return { wave: G.wave, lives: G.lives, gold: G.gold, kills: G.kills, towers: GAME.TOWERS.map(t => t.k[0] + t.lv).join(''), hero: GAME.HERO.lv, sk: GAME.HERO.sk.join(''), state: G.state }; });
    console.log(JSON.stringify(s)); if (s.state !== 'play') break;
  }
  await pg.screenshot({ path: `${out}/t5_end.png` });
  await pg.evaluate(() => { const t = GAME.TOWERS[0]; GAME.closeCam(t.pad.c.x, t.pad.c.z, 4); }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/t5b_close.png` });
  await pg.evaluate(() => { const H = GAME.HERO; GAME.closeCam(H.pos.x, H.pos.z, 3); }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/t5c_hero.png` });
  await pg.evaluate(() => { GAME.setPx(true); }); await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/t6_pixel.png` });
  const fps = await pg.evaluate(() => new Promise(r => { let n = 0; const t0 = performance.now(); const f = () => { n++; if (performance.now() - t0 < 2000) requestAnimationFrame(f); else r(n / 2); }; requestAnimationFrame(f); }));
  console.log('fps (headless, software GL)', fps); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].join('\n') : 'no errors'); await b.close();
})();
