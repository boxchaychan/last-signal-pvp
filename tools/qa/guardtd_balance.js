// guardtd.html balance check: plays whole games with a simple bot, game logic only (?norender=1), and prints lives / gold per wave.
// Bot: keeps a share of gold for upgrades, builds a mix of towers on the pads nearest the road start, upgrades the most used, learns every
// skill it can, casts the skills every few seconds at the monster furthest along the road. python3 -m http.server 8000 ;
//   node tools/qa/guardtd_balance.js [map=forest] [hero=archer] [skill=1] [games=1]
const { chromium } = require('playwright');
(async () => {
  const map = process.argv[2] || 'forest', hero = process.argv[3] || 'archer', useSkill = (process.argv[4] || '1') === '1', games = +(process.argv[5] || 1);
  const b = await chromium.launch(); const errs = [];
  for (let gi = 0; gi < games; gi++) {
    const pg = await b.newPage(); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(`http://localhost:8000/guardtd.html?snd=0&norender=1&maxw=40&mode=road&map=${map}&hero=${hero}`); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 120000 });
    const res = await pg.evaluate(async (useSkill) => {
      const G = GAME.G, out = []; const mix = ['archer', 'mage', 'bomb', 'archer', 'knight', 'mage', 'archer', 'bomb', 'mage', 'archer', 'knight'];
      const spend = () => { for (let k = 0; k < 4; k++) GAME.learnSkill(k);
        const free = GAME.PADS.filter(p => !p.tower); const n = GAME.TOWERS.length;
        if (free.length && G.gold >= GAME.TDEF[mix[n % mix.length]].cost[0] && (n < 4 || G.gold > 140 || GAME.TOWERS.every(t => t.lv >= 1))) GAME.buildTower(free[0], mix[n % mix.length]);
        for (const t of GAME.TOWERS.slice().sort((a, c) => a.lv - c.lv)) if (t.lv < 3 && G.gold >= t.D.cost[t.lv + 1] + 20) GAME.upgradeTower(t);
        if (GAME.TOWERS.every(t => t.lv >= 3) && G.lives < 20 && G.gold >= 100) { G.gold -= 100; G.lives++; } };
      let t = 0; for (let w = 1; w <= (+(new URLSearchParams(location.search).get("maxw")) || 40) && G.state === "play"; w++) {
        await GAME.startWave(); let guard = 0;
        while ((G.queue.length || GAME.MON.length) && G.state === 'play' && guard++ < 4000) { GAME.sim(.5); t += .5; spend();
          if (useSkill && guard % 6 === 0) { const m = GAME.MON.filter(q => !q.dead).sort((a, c) => c.s - a.s)[0]; if (m) for (let k = 0; k < 4; k++) GAME.castSkill(k, m.pos.clone()); } }
        spend(); out.push([w, G.lives, G.gold, GAME.TOWERS.length, GAME.TOWERS.reduce((s, q) => s + q.lv, 0), GAME.HERO.lv]); if (G.state !== 'play') break; G.build = 0; }
      return { out, state: G.state, stars: G.stars || 0 };
    }, useSkill);
    console.log(`${map} ${hero} skills=${useSkill} -> ${res.state} stars ${res.stars}`); console.log(res.out.map(r => `w${r[0]}:L${r[1]} g${r[2]} t${r[3]}/${r[4]} h${r[5]}`).join('  '));
    await pg.close();
  }
  console.log(errs.length ? 'ERRORS ' + [...new Set(errs)].join(' | ') : 'no errors'); await b.close();
})();
