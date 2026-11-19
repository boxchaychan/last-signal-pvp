// guardtd.html MAZE balance: a bot builds a zig-zag of stone walls (4 wall lines, gaps at alternate ends), turns walls into towers from the
// middle rows out, upgrades, learns and casts skills; game logic only (?norender=1). "naive=1": no walls, towers in two rows beside the straight way
// (a player who does not maze). python3 -m http.server 8000 ; node tools/qa/guardtd_mazebal.js [hero=archer] [naive=0] [games=1] [maxw=40]
const { chromium } = require('playwright');
(async () => {
  const hero = process.argv[2] || 'archer', naive = process.argv[3] === '1', games = +(process.argv[4] || 1), maxw = +(process.argv[5] || 40);
  const b = await chromium.launch(); const errs = [];
  for (let gi = 0; gi < games; gi++) {
    const pg = await b.newPage(); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(`http://localhost:8000/guardtd.html?snd=0&norender=1&hero=${hero}`); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 120000 });
    const res = await pg.evaluate(async ([naive, maxw]) => {
      const G = GAME.G, out = [], P = (i, j) => GAME.PADAT[GAME.cId(i, j)], mix = ['archer', 'mage', 'bomb', 'archer', 'knight', 'mage', 'archer', 'bomb', 'mage', 'archer', 'knight'];
      const plan = [], spots = [], stuck = [];
      if (!naive) { for (const [i, gapLow] of [[3, true], [6, false], [10, true], [13, false]]) for (let j = 1; j <= 8; j++) if (gapLow ? j !== 8 : j !== 1) plan.push(P(i, j));
        for (const j of [4, 5, 3, 6, 2, 7]) for (const i of [3, 6, 10, 13]) { const p = P(i, j); if (p) spots.push(p); } }
      else for (const i of [3, 5, 7, 9, 11, 13, 4, 6, 10, 12]) for (const j of [3, 6]) spots.push(P(i, j));
      let nt = 0; const towers = () => GAME.TOWERS.filter(t => !t.D.wall);
      const spend = () => { for (let k = 0; k < 4; k++) GAME.learnSkill(k);
        const T = towers(), want = mix[nt % mix.length], c = GAME.TDEF[want].cost[0];
        if (T.length < 3 || G.gold >= c + (T.length < 5 ? 0 : 60)) { const s = spots.find(p => !p.tower || p.tower.D.wall); if (s && G.gold >= c && GAME.buildTower(s, want)) nt++; }
        if (towers().length >= 3) for (const p of plan) { if (G.gold < 10 + GAME.TDEF[mix[nt % mix.length]].cost[0] * .5) break; if (!p.tower) GAME.buildTower(p, 'wall'); }
        if (plan.every(p => p.tower) || naive) for (const t of towers().sort((a, c) => a.lv - c.lv)) if (t.lv < 3 && G.gold >= t.D.cost[t.lv + 1] + 20) GAME.upgradeTower(t);
        if (towers().every(t => t.lv >= 3) && spots.every(p => p.tower && !p.tower.D.wall) && G.lives < 20 && G.gold >= 100) { G.gold -= 100; G.lives++; } };
      for (let w = 1; w <= maxw && G.state === 'play'; w++) {
        spend(); await GAME.startWave(); let guard = 0;
        while ((G.queue.length || GAME.MON.length) && G.state === 'play' && guard++ < 6000) { GAME.sim(.5); spend();
          if (guard % 6 === 0) { const m = GAME.MON.filter(q => !q.dead).sort((a, c) => c.s - a.s)[0]; if (m) for (let k = 0; k < 4; k++) GAME.castSkill(k, m.pos.clone()); } }
        if (GAME.MON.length && G.state === 'play') stuck.push({ w, n: GAME.MON.length, q: G.queue.length, starting: !!G.starting, m: GAME.MON.slice(0, 4).map(m => ({ k: m.k, x: +m.pos.x.toFixed(2), z: +m.pos.z.toFixed(2), tgt: m.tgt, d: m.tgt != null ? GAME.DIST[m.tgt] : null, fly: m.fly, st: +m.stunT.toFixed(1), hp: Math.round(m.hp), dead: m.dead, fs: m.fs, s: m.s, row: m.row, fight: !!m.fight, slowK: m.slowK })) });
        spend(); out.push([w, G.lives, G.gold, towers().length, towers().reduce((s, q) => s + q.lv, 0), GAME.TOWERS.length - towers().length, GAME.HERO.lv, +GAME.DIST[GAME.SPC[0]].toFixed(0)]); if (G.state !== 'play') break; G.build = 0; }
      return { out, state: G.state, stuck, wd: GAME.WDLOG };
    }, [naive, maxw]);
    console.log(`maze ${hero} naive=${naive} -> ${res.state}`); if (res.stuck.length) console.log('STUCK ' + JSON.stringify(res.stuck)); if (res.wd.length) console.log('WATCHDOG ' + JSON.stringify(res.wd)); console.log(res.out.map(r => `w${r[0]}:L${r[1]} g${r[2]} t${r[3]}/${r[4]} wl${r[5]} h${r[6]} d${r[7]}`).join('  '));
    await pg.close();
  }
  console.log(errs.length ? 'ERRORS ' + [...new Set(errs)].join(' | ') : 'no errors'); await b.close();
})();
