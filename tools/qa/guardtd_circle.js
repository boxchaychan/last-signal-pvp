// guardtd.html CIRCLE mode (owner 2026-11-19 "GREEN CIRCLE TD MEGA", "วิ่งวนไม่หยุด"): monsters loop the road for ever, waves on a timer,
// lost when more than LIMIT are on the map. "look" = screenshots (start, towers, a crowded wave, the monster counter);
// "bot" = a greedy bot (towers on the tiles that see the most road, upgrades, skills) plays until it loses, logic only.
// python3 -m http.server 8000 ; node tools/qa/guardtd_circle.js look [out=/tmp/circ] [hero=archer]  |  node tools/qa/guardtd_circle.js bot [hero=archer] [maxw=40]
const { chromium } = require('playwright');
(async () => {
  const what = process.argv[2] || 'look', b = await chromium.launch(), errs = [];
  if (what === 'look') {
    const out = process.argv[3] || '/tmp/circ', hero = process.argv[4] || 'archer'; require('fs').mkdirSync(out, { recursive: true });
    const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    await pg.goto('http://localhost:8000/guardtd.html?snd=0&hero=' + hero, { waitUntil: 'domcontentloaded', timeout: 120000 }); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 120000 });
    await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/c1_start.png` });
    const r1 = await pg.evaluate(() => { const G = GAME.G; G.gold = 9999; const ks = ['archer', 'mage', 'bomb', 'knight']; const near = GAME.PADS.slice().sort((a, c) => Math.abs(Math.abs(a.c.z) - 2.4) - Math.abs(Math.abs(c.c.z) - 2.4)); near.slice(0, 8).forEach((p, i) => GAME.buildTower(p, ks[i % 4]));
      const p = GAME.PADS.find(q => !q.tower); const [x, y] = GAME.toScreen(p.c.x, .1, p.c.z); GAME.tap(x, y); return { pads: GAME.PADS.length, towers: GAME.TOWERS.length, menu: !!G.menu }; });
    await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/c2_towers_menu.png` });
    await pg.evaluate(async () => { GAME.G.menu = null; await GAME.startWave(); GAME.sim(14); await GAME.startWave(); GAME.sim(6); }); await pg.waitForTimeout(600); await pg.screenshot({ path: `${out}/c3_wave.png` });
    const r2 = await pg.evaluate(async () => { const G = GAME.G; for (const t of [...GAME.TOWERS]) GAME.sellTower(t); for (let k = 0; k < 8 && G.state === 'play'; k++) { G.build = 0; await GAME.startWave(); GAME.sim(8); } return { wave: G.wave, alive: GAME.aliveCount(), state: G.state }; });
    await pg.waitForTimeout(600); await pg.screenshot({ path: `${out}/c4_crowd.png` });
    console.log(JSON.stringify({ r1, r2, info: await pg.evaluate(() => GAME.info()) }));
  } else {
    const hero = process.argv[3] || 'archer', maxw = +(process.argv[4] || 40);
    const pg = await b.newPage(); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(`http://localhost:8000/guardtd.html?snd=0&norender=1&hero=${hero}`, { waitUntil: 'domcontentloaded', timeout: 120000 }); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 120000 });
    const res = await pg.evaluate(async (maxw) => {
      const G = GAME.G, out = [], mix = ['archer', 'mage', 'bomb', 'archer', 'knight', 'mage', 'archer', 'bomb', 'mage', 'archer', 'knight'], tp = new THREE.Vector3();
      const cover = p => { let n = 0; for (let s = 0; s < 33; s += .5) { /* road points within 3 */ const a = s / 33 * Math.PI * 2; tp.set(Math.cos(a) * 6.6, 0, Math.sin(a) * 2.4); if (tp.distanceTo(p.c) < 3) n++; } return n; };
      const spots = GAME.PADS.slice().sort((a, c) => cover(c) - cover(a)); let nt = 0, peak = 0;
      const spend = () => { for (let k = 0; k < 4; k++) GAME.learnSkill(k); const T = GAME.TOWERS, want = mix[nt % mix.length];
        if (G.gold >= GAME.TDEF[want].cost[0] && (T.length < 4 || G.gold > 150 || T.every(t => t.lv >= 1))) { const s = spots.find(p => !p.tower); if (s && GAME.buildTower(s, want)) nt++; }
        for (const t of T.slice().sort((a, c) => a.lv - c.lv)) if (t.lv < 3 && G.gold >= t.D.cost[t.lv + 1] + 20) GAME.upgradeTower(t);
        if (!spots.some(p => !p.tower) && T.every(t => t.lv >= 3)) for (let g = 0; g < 20; g++) { const t = T.slice().sort((a, c) => GAME.starCost(a) - GAME.starCost(c))[0], hc = GAME.trainCost();   /* the gold sinks: stars + hero training, cheapest first */
          if (hc <= GAME.starCost(t)) { if (!GAME.trainHero()) break; } else if (G.gold >= GAME.starCost(t)) GAME.upgradeTower(t); else break; } };
      let t = 0; await GAME.startWave();
      while (G.state === 'play' && G.wave <= maxw && t < 6000) { while (G.starting) await new Promise(r => setTimeout(r, 20)); GAME.sim(.5); t += .5; spend(); peak = Math.max(peak, GAME.aliveCount());
        if ((t * 2) % 6 === 0) { const m = GAME.MON.filter(q => !q.dead).sort((a, c) => c.s - a.s)[0]; if (m) for (let k = 0; k < 4; k++) GAME.castSkill(k, m.pos.clone()); }
        if (!out.length || out[out.length - 1][0] !== G.wave) out.push([G.wave, Math.round(t), GAME.aliveCount(), G.gold, GAME.TOWERS.length, GAME.TOWERS.reduce((s, q) => s + q.lv + (q.star || 0), 0), GAME.HERO.lv + '/' + (GAME.HERO.train || 0)]); }
      return { out, state: G.state, wave: G.wave, peak, t };
    }, maxw);
    console.log(`circle ${hero} -> ${res.state} at wave ${res.wave} (${res.t} s, peak ${res.peak})`); console.log(res.out.map(r => `w${r[0]}@${r[1]}s:a${r[2]} g${r[3]} t${r[4]}/${r[5]} h${r[6]}`).join('  '));
  }
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].join('\n') : 'no errors'); await b.close();
})();
