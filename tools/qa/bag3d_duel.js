// bag3d.html DUELS IN THE ARENA (owner 2026-11-28 "รอบคนสู้กัน ให้ทำแบบมอนเลย"): a duel round is fought in horde.html?bag=1 like the monster rounds.
// python3 -m http.server 8000 ; node tools/qa/bag3d_duel.js [out=/tmp/bag3d_duel]       = flow: a duel round in the iframe, both champions, both bags fire, result pop
// node tools/qa/bag3d_duel.js bal [duels per pair 6] [rounds 3,6,9,12]                    = balance: bot bags of our classes against the rivals in the arena, no drawing
//   melee players (knight, barbarian, rogue) meet the ranged rivals (archer, hood), ranged players (ranger, mage) meet the melee rivals (wing, demon, dark);
//   DUEL='{"back":0.7,"dmg":0.6}' = try other BAG_DUEL numbers (bag3d/arena.js); the target is melee vs ranged near 50 / 50 (the owner: "เจอยิงไกลมันก็แพ้ 100 %" must not happen). CLS=knight,ranger = only those classes.
const { chromium } = require('playwright');
const mode = process.argv[2] === 'bal' ? 'bal' : 'flow';
const MEL = ['knight', 'barbarian', 'rogue'], RNG = ['ranger', 'mage'], RV_MEL = ['wing', 'demon', 'dark'], RV_RNG = ['archer', 'hood'];
const TREE = { knight: 'f_kingslayer', barbarian: 'f_titan', rogue: 'f_kingslayer', ranger: 'f_godbow', mage: 'f_archmage' };
(async () => {
  const b = await chromium.launch(); const errs = []; let ok = true; const say = (n, v) => { console.log(v ? 'ok  ' : 'FAIL', n); if (!v) ok = false; };
  const watch = pg => { pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); };
  if (mode === 'bal') {
    const n = +(process.argv[3] || 6), rounds = (process.argv[4] || '3,6,9,12').split(',').map(Number), only = process.env.CLS ? process.env.CLS.split(',') : null;
    const ctx = await b.newContext({ viewport: { width: 844, height: 390 } }), shop = await ctx.newPage(); watch(shop);
    await shop.goto('http://localhost:8000/bag3d.html?mute=1&fight=side'); await shop.waitForTimeout(1500); await shop.click('#start'); await shop.waitForTimeout(300);
    const tot = { mel: [0, 0], rng: [0, 0] }, rows = [];
    for (const cls of MEL.concat(RNG)) { if (only && !only.includes(cls)) continue;
      const are = await ctx.newPage(); watch(are); await are.goto('http://localhost:8000/horde.html?bag=1&nopause=1&snd=0&norender=1&map=arena&land=forest&cls=' + cls); await are.waitForFunction(() => window.BAGAPI && BAGAPI.BAG.ready, null, { timeout: 60000 }); if (process.env.DUEL) await are.evaluate(j => Object.assign(BAGAPI.DUEL, JSON.parse(j)), process.env.DUEL);   /* DUEL='{"back":.7}' tries other BAG_DUEL numbers */
      const foes = MEL.includes(cls) ? RV_RNG : RV_MEL;
      for (const round of rounds) for (const rk of foes) { let w = 0, t = 0, hp = 0, rhp = 0;
        for (let i = 0; i < n; i++) {
          const cfg = await shop.evaluate(([round, cls, rk, tree]) => { const save = G, hk = HK; QUIET++; try { HK = cls; newGameQuiet();
              for (let r2 = 1; r2 <= round; r2++) { G.round = r2; if (r2 >= 3) BG.botTree(tree); BG.botShop(true); BG.botMerge(); if (r2 < round) { G.gold += 11 + Math.min(6, r2 >> 1); roll(true); } }
              const H = HEROES[HK], f = build(G.items.filter(o => o.bag), H.base.hp + 4 + round * 6, H.aff, H.base), c = BG.hordeCfg(f, round), op = BG.rivalMake(round, rk); c.rv = rivalCfg(BG.rivalFoe(op), op); return c; } finally { G = save; HK = hk; QUIET--; } }, [round, cls, rk, TREE[cls]]);
          const r = await are.evaluate(async cfg => { BAGAPI.start(cfg); for (let k = 0; k < 400 && GAME.G.state !== 'play'; k++) await new Promise(r => setTimeout(r, 25));
            for (let i = 0; i < 400 && GAME.G.state === 'play'; i++) { GAME.sim(.5, 1 / 30); await Promise.resolve(); } return BAGAPI.BAG.result || { win: false, t: 99, hp: 0, rhp: 1, rmax: 1 }; }, cfg);
          w += r.win ? 1 : 0; t += r.t; hp += r.hp / cfg.hp; rhp += (r.rhp || 0) / (r.rmax || 1); }
        const k = MEL.includes(cls) ? 'mel' : 'rng'; tot[k][0] += w; tot[k][1] += n;
        const line = `round ${String(round).padStart(2)}  ${cls.padEnd(9)} vs ${rk.padEnd(6)}  win ${(w / n).toFixed(2)}  time ${(t / n).toFixed(0)} s  our life ${(hp / n * 100).toFixed(0)} %  rival life ${(rhp / n * 100).toFixed(0)} %`; rows.push(line); console.log(line); }
      await are.close(); }
    const mw = tot.mel[1] ? tot.mel[0] / tot.mel[1] : NaN, rw = tot.rng[1] ? tot.rng[0] / tot.rng[1] : NaN;
    console.log(`MELEE players vs ranged rivals win ${mw.toFixed(2)} (${tot.mel[0]}/${tot.mel[1]})   RANGED players vs melee rivals win ${rw.toFixed(2)} (${tot.rng[0]}/${tot.rng[1]})   melee side overall ${(((tot.mel[0]) + (tot.rng[1] - tot.rng[0])) / Math.max(1, tot.mel[1] + tot.rng[1])).toFixed(2)}`);
    console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close(); return;
  }
  const out = process.argv[2] || '/tmp/bag3d_duel'; require('fs').mkdirSync(out, { recursive: true });
  for (const [W, H] of [[844, 390], [740, 340]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H } })).newPage(); watch(pg);
    await pg.goto('http://localhost:8000/bag3d.html?mute=1'); await pg.waitForTimeout(1500); await pg.click('#start'); await pg.waitForTimeout(300);
    await pg.evaluate(() => { G.round = 6; G.hp = 5; for (const id of ['hammer', 'club', 'shield', 'ember']) { const o = give(id), f = firstFit(o); if (f) { [o.x, o.y, o.r] = f; o.bag = true; } } G.opp = BG.rivalMake(6, 'archer'); draw(); $('#go').click(); });
    await pg.waitForFunction(() => HZ.ready, null, { timeout: 60000 }); const fr = pg.frames().find(f => /horde\.html/.test(f.url()));
    say(W + ' a duel round opens the arena iframe', !!fr && await pg.evaluate(() => !!BT && BT.duel === 1 && getComputedStyle(document.getElementById('hz')).display === 'block'));
    await fr.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 60000 });
    const st = await fr.evaluate(() => ({ duel: BAGAPI.BAG.duel, sides: BAGAPI.SIDES.length, mine: BAGAPI.BAG.its.length, theirs: BAGAPI.SIDES[1].b.its.length, rv: BAGAPI.SIDES[1].hero.k, inScene: !!BAGAPI.SIDES[1].hero.M.T.root.parent, mon: GAME.MON.length }));
    say(W + ' two champions: ' + JSON.stringify(st), st.duel && st.sides === 2 && st.mine >= 3 && st.theirs >= 2 && st.rv === 'archer' && st.inScene && st.mon === 1);
    await pg.waitForTimeout(2600); await pg.screenshot({ path: `${out}/${W}_1_duel.png` });
    await pg.waitForTimeout(2600); await pg.screenshot({ path: `${out}/${W}_2_duel.png` });
    const hp = await fr.evaluate(() => BAGAPI.SIDES.map(s => s.hero.hp / s.hero.max)); say(W + ' both champions were hit: ' + hp.map(v => v.toFixed(2)).join(' / '), hp[0] < 1 && hp[1] < 1);
    const sx = await fr.evaluate(() => { const m = BAGAPI.SIDES[1].me; m.frzT = .8; m.burnT = 2; m.burnD = 2; m.slowT = 1; m.slowK = .6; return 1; }); await pg.waitForTimeout(400);
    say(W + ' statuses on the rival (stun, burn, slow) tick', await fr.evaluate(() => { const m = BAGAPI.SIDES[1].me; return m.frzT < .8 && m.slowT < 1; }));
    await fr.evaluate(() => { BAGAPI.BAG.spd = 2; });
    await pg.waitForFunction(() => !BT && $('#pop').style.display === 'flex', null, { timeout: 200000 }); await pg.screenshot({ path: `${out}/${W}_3_end.png` });
    const res = await pg.evaluate(() => ({ t: $('#pop div').textContent, round: G.round, hz: getComputedStyle(document.getElementById('hz')).display, cups: G.cups })); say(W + ' result: ' + res.t.slice(0, 70).replace(/\s+/g, ' '), res.round === 7 && res.hz === 'none' && /ชนะผู้เล่น|แพ้ผู้เล่น/.test(res.t));
    await pg.evaluate(() => closePop()); await pg.close();
  }
  console.log(ok ? 'DUEL OK' : 'DUEL FAIL'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
