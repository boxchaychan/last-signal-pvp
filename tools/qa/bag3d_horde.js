// bag3d.html HORDE FIGHT (owner 2026-11-27 "ตัวเดียวสู้กับฝูงมอนตามไอเทมในกระเป๋าเรา"): monster / boss rounds are fought in horde.html?bag=1 (bag3d/arena.js) inside an iframe.
// python3 -m http.server 8000 ; node tools/qa/bag3d_horde.js [out=/tmp/bag3d_horde] [device scale 1]
//   flow: start -> round 1 fight in the iframe (AUTO) -> result pop -> shop; a round-5 boss fight; a duel round still uses the side view; 844 x 390 and 740 x 360.
// node tools/qa/bag3d_horde.js bal [games per round 12] [last round 15]   = balance: bot-filled bags of each round against that round's horde, no drawing
const { chromium } = require('playwright');
const mode = process.argv[2] === 'bal' ? 'bal' : 'flow';
(async () => {
  const b = await chromium.launch(); const errs = []; let ok = true; const say = (n, v) => { console.log(v ? 'ok  ' : 'FAIL', n); if (!v) ok = false; };
  const watch = pg => { pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); };
  if (mode === 'bal') {
    const n = +(process.argv[3] || 12), last = +(process.argv[4] || 15), ctx = await b.newContext({ viewport: { width: 844, height: 390 } }), shop = await ctx.newPage(), are = await ctx.newPage(); watch(shop); watch(are);
    await shop.goto('http://localhost:8000/bag3d.html?mute=1&fight=side'); await shop.waitForTimeout(1500); await shop.click('#start'); await shop.waitForTimeout(300);
    await are.goto('http://localhost:8000/horde.html?bag=1&nopause=1&snd=0&norender=1&map=forest'); await are.waitForFunction(() => window.BAGAPI && BAGAPI.BAG.ready, null, { timeout: 60000 });
    for (let round = 1; round <= last; round++) { let w = 0, t = 0, hp = 0, left = 0, tk = 0;
      for (let i = 0; i < n; i++) {
        const cfg = await shop.evaluate(round => { const save = G; QUIET++; G = { round: 1, hp: 5, gold: 12, open: {}, items: [], shop: [], best: 0, buys: 0, wins: 0, cups: 0 }; for (let y = 1; y < 4; y++) for (let x = 2; x < 6; x++) G.open[x + ',' + y] = 1; give('sword', 3, 1, 0); give('apple', 4, 1, 0); roll(true);
          for (let r2 = 1; r2 <= round; r2++) { G.round = r2; if (r2 >= 3) BG.botTree('f_kingslayer'); BG.botShop(true); BG.botMerge(); if (r2 < round) { G.gold += 11 + Math.min(6, r2 >> 1); roll(true); } }
          const H = HEROES[HK], f = build(G.items.filter(o => o.bag), H.base.hp + 4 + round * 6, H.aff, H.base), c = BG.hordeCfg(f, round); G = save; QUIET--; return c; }, round);
        const r = await are.evaluate(async cfg => { BAGAPI.start(cfg); await new Promise(r => setTimeout(r, 30)); for (let i = 0; i < 360 && GAME.G.state === 'play'; i++) { GAME.sim(.5, 1 / 30); await Promise.resolve(); }   /* in half seconds: a boss arrives through a promise */ return Object.assign({ taken: GAME.G.taken }, BAGAPI.BAG.result || { win: false, t: 180, hp: 0, left: 99 }); }, cfg);
        w += r.win ? 1 : 0; t += r.t; hp += r.hp / cfg.hp; left += r.left; tk += r.taken / cfg.hp; }
      console.log(`round ${String(round).padStart(2)} ${round % 5 === 0 ? 'boss' : '    '}  win ${(w / n).toFixed(2)}  time ${(t / n).toFixed(0)} s  life left ${(hp / n * 100).toFixed(0)} %  monsters left ${(left / n).toFixed(1)}  damage taken ${(tk / n * 100).toFixed(0)} % of life`); }
    console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close(); return;
  }
  const out = process.argv[2] || '/tmp/bag3d_horde', dsf = +(process.argv[3] || 1); require('fs').mkdirSync(out, { recursive: true });
  for (const [W, H] of [[844, 390], [740, 360]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dsf })).newPage(); watch(pg);
    await pg.goto('http://localhost:8000/bag3d.html?mute=1'); await pg.waitForTimeout(1500); await pg.click('#start'); await pg.waitForTimeout(300);
    say(W + ' the info line names the horde', /ฝูงมอน/.test(await pg.evaluate(() => { document.querySelector('#top .rd').click(); const t = $('#info').textContent + $('#pop div').textContent; closePop(); return t; })));
    await pg.evaluate(() => { give('bow', 0, 1, 0); give('wand', 6, 1, 0); draw(); $('#go').click(); });
    await pg.waitForFunction(() => HZ.ready, null, { timeout: 60000 });
    const fr = pg.frames().find(f => /horde\.html/.test(f.url())); say(W + ' the arena iframe is there and shown', !!fr && await pg.evaluate(() => getComputedStyle(document.getElementById('hz')).display === 'block'));
    await fr.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 60000 }); await pg.waitForTimeout(2600); await pg.screenshot({ path: `${out}/${W}_1_fight.png` });
    const st = await fr.evaluate(() => ({ items: BAGAPI.BAG.its.length, total: BAGAPI.BAG.total, hp: GAME.HERO.max, kinds: BAGAPI.BAG.kinds.length })); say(W + ' round 1: ' + JSON.stringify(st), st.items >= 4 && st.total >= 14 && st.kinds >= 3);
    await pg.waitForTimeout(2500); await pg.screenshot({ path: `${out}/${W}_2_fight.png` }); await fr.evaluate(() => { BAGAPI.BAG.spd = 2; });
    await pg.waitForFunction(() => !BT && $('#pop').style.display === 'flex', null, { timeout: 120000 }); await pg.screenshot({ path: `${out}/${W}_3_end.png` });
    const res = await pg.evaluate(() => ({ t: $('#pop div').textContent, round: G.round, hz: getComputedStyle(document.getElementById('hz')).display })); say(W + ' result: ' + res.t.slice(0, 60).replace(/\s+/g, ' '), res.round === 2 && res.hz === 'none' && /ชนะ|แพ้/.test(res.t)); await pg.evaluate(() => closePop());
    if (W === 844) {
      await pg.evaluate(() => { G.round = 5; G.hp = 5; for (let y = 0; y < 5; y++) for (let x = 0; x < 8; x++) G.open[x + ',' + y] = 1; for (const id of ['hammer', 'scythe', 'orb', 'shield', 'meat', 'chakram', 'icestaff', 'bomb', 'twinblades']) { const o = give(id), f = firstFit(o); if (f) { [o.x, o.y, o.r] = f; o.bag = true; o.lv = 2; } } nextOpp(); draw(); $('#go').click(); });
      await fr.waitForFunction(() => GAME.G.state === 'play' && GAME.G.boss, null, { timeout: 60000 }); await pg.waitForTimeout(3500); await pg.screenshot({ path: `${out}/${W}_4_boss.png` }); say('round 5 has a boss', await fr.evaluate(() => !!GAME.G.boss && BAGAPI.BAG.cfg.boss));
      await pg.waitForTimeout(3000); await pg.screenshot({ path: `${out}/${W}_5_boss.png` }); await fr.evaluate(() => { BAGAPI.BAG.spd = 2; for (const m of GAME.MON) m.hp = Math.min(m.hp, 20); });
      await pg.waitForFunction(() => !BT && $('#pop').style.display === 'flex', null, { timeout: 180000 }); say('boss round ends: ' + (await pg.evaluate(() => $('#pop div').textContent)).slice(0, 50).replace(/\s+/g, ' '), true); await pg.evaluate(() => closePop());
      await pg.evaluate(() => { G.round = 6; G.hp = 5; nextOpp(); draw(); $('#go').click(); }); await pg.waitForTimeout(1500); say('a duel round keeps the side view', await pg.evaluate(() => !!BT && !BT.horde && BT.B.pvp === 1 && getComputedStyle(document.getElementById('hz')).display === 'none'));
    }
    await pg.close();
  }
  console.log(ok ? 'HORDE OK' : 'HORDE FAIL'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
