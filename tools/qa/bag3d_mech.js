// bag3d item mechanics in the arena (2026-11-28 cloud batch 3): sprint boots, retreat boots, real skeleton warriors of the skeleton staff.
// python3 -m http.server 8000 ; node tools/qa/bag3d_mech.js [out=/tmp/bag3d_mech]
//   a mage with the skeleton staff + retreat boots and a knight with sprint boots fight round 4 in horde.html?bag=1 (drawn, so the skeletons are
//   seen on the screenshot); then the mage with the staff in a duel (its skeletons hit the rival champion).
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_mech'; require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; let ok = true; const say = (n, v) => { console.log(v ? 'ok  ' : 'FAIL', n); if (!v) ok = false; };
  const watch = pg => { pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); };
  const ctx = await b.newContext({ viewport: { width: 844, height: 390 } }), shop = await ctx.newPage(); watch(shop);
  await shop.goto('http://localhost:8000/bag3d.html?mute=1&fight=side'); await shop.waitForTimeout(1500); await shop.click('#start'); await shop.waitForTimeout(300);
  const cfgOf = (cls, ids, rv) => shop.evaluate(([cls, ids, rv]) => { const save = G, hk = HK; QUIET++; try { HK = cls; newGameQuiet(); G.items = []; G.round = 4; for (let y = 0; y < 5; y++) for (let x = 0; x < 8; x++) G.open[x + ',' + y] = 1;
      for (const id of ids) { const o = give(id), f = firstFit(o); if (f) { [o.x, o.y, o.r] = f; o.bag = true; } } const H = HEROES[HK], f = build(G.items.filter(o => o.bag), H.base.hp + 4 + 4 * 6, H.aff, H.base), c = BG.hordeCfg(f, 4);
      if (rv) { G.round = 6; const op = BG.rivalMake(6, rv); c.rv = rivalCfg(BG.rivalFoe(op), op); c.round = 6; } return c; } finally { G = save; HK = hk; QUIET--; } }, [cls, ids, rv]);
  const arena = async cls => { const pg = await ctx.newPage(); watch(pg); await pg.goto('http://localhost:8000/horde.html?bag=1&nopause=1&snd=0&map=arena&land=forest&cls=' + cls); await pg.waitForFunction(() => window.BAGAPI && BAGAPI.BAG.ready, null, { timeout: 60000 }); return pg; };
  { const pg = await arena('mage'), cfg = await cfgOf('mage', ['wand', 'sp_skel', 'bt_retreat', 'book']);
    say('mage bag: staff + retreat boots are working items', cfg.items.some(w => w.id === 'sp_skel') && cfg.st.gx && cfg.st.gx.retreat > 0);
    await pg.evaluate(c => BAGAPI.start(c), cfg); await pg.waitForFunction(() => GAME.G.state === 'play', null, { timeout: 30000 }); await pg.evaluate(() => { for (const W of BAGAPI.BAG.its) if (W.id === 'sp_skel') W.t = W.cd - 2; });
    await pg.waitForFunction(() => BAGAPI.BAG.allies && BAGAPI.BAG.allies.some(a => !a.dead), null, { timeout: 30000 }).catch(() => { }); await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/mage_skeletons.png` });
    const r = await pg.evaluate(async () => { const B = BAGAPI.BAG, n = B.allies.filter(a => !a.dead).length; for (let i = 0; i < 40 && GAME.G.state === 'play'; i++) { GAME.sim(.25, 1 / 30); await Promise.resolve(); } return { n, dmg: GAME.STATS.sp_skel || 0, rt: B.rtT || 0 }; });
    say(`skeleton warriors: ${r.n} up, their hits ${Math.round(r.dmg)}`, r.n >= 2 && r.dmg > 0); say('retreat boots rolled away from a monster (next at ' + r.rt.toFixed(1) + ' s)', r.rt > 0); await pg.close(); }
  { const pg = await arena('knight'), cfg = await cfgOf('knight', ['sword', 'bt_sprint', 'buckler']);
    await pg.evaluate(c => BAGAPI.start(c), cfg); await pg.waitForFunction(() => GAME.G.state === 'play', null, { timeout: 30000 });
    const r = await pg.evaluate(async () => { const B = BAGAPI.BAG; let fast = 0; for (let i = 0; i < 120 && GAME.G.state === 'play'; i++) { GAME.sim(.1, 1 / 30); if (B.spT > B.t && GAME.P.spd > B.mv0 * 1.5) fast++; await Promise.resolve(); } return { fast, base: B.mv0 }; });
    say(`sprint boots: faster after a hit (${r.fast} checks fast, base speed ${r.base.toFixed(2)})`, r.fast > 0); await pg.close(); }
  { const pg = await arena('mage'), cfg = await cfgOf('mage', ['wand', 'sp_skel', 'book'], 'wing');
    await pg.evaluate(c => BAGAPI.start(c), cfg); await pg.waitForFunction(() => GAME.G.state === 'play', null, { timeout: 60000 }); await pg.evaluate(() => { for (const W of BAGAPI.BAG.its) if (W.id === 'sp_skel') W.t = W.cd - .3; });   /* the staff casts at once */ await pg.waitForTimeout(2500); await pg.screenshot({ path: `${out}/duel_skeletons.png` });
    const r = await pg.evaluate(async () => { for (let i = 0; i < 60 && GAME.G.state === 'play'; i++) { GAME.sim(.25, 1 / 30); await Promise.resolve(); } return { dmg: GAME.STATS.sp_skel || 0, duel: BAGAPI.BAG.duel }; });
    say('in a duel the skeletons hit the rival champion: ' + Math.round(r.dmg), r.duel && r.dmg > 0); await pg.close(); }
  console.log(ok ? 'MECH OK' : 'MECH FAIL'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
