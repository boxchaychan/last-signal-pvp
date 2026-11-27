// bag3d.html round format (owner 2026-11-27): monster rounds, a duel with a rival PLAYER every 3rd round, a boss every 5th.
// Checks the schedule, the top-bar track, the "look into the rival's bag" pop, a duel against each of the 5 rival champions (3D model, skill, result pop), buttons inside the screen.
// python3 -m http.server 8000 ; node tools/qa/bag3d_rounds.js [out=/tmp/bag3d_rounds] [device scale 1]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_rounds', dsf = +(process.argv[3] || 1); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; let ok = true; const say = (n, v) => { console.log(v ? 'ok  ' : 'FAIL', n); if (!v) ok = false; };
  for (const [W, H] of [[844, 390], [740, 360]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dsf })).newPage();
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto('http://localhost:8000/bag3d.html'); await pg.waitForTimeout(2000); await pg.click('#start'); await pg.waitForTimeout(400);
    const sch = await pg.evaluate(() => Array.from({ length: 15 }, (_, i) => kindOf(i + 1)[0]).join(''));
    say(W + ' schedule ' + sch, sch === 'mmpmbpmmpbmpmmb');
    say(W + ' track in the top bar', await pg.evaluate(() => document.querySelectorAll('#top .trk i').length === 5 && !!document.querySelector('#top .trk i.on')));
    await pg.screenshot({ path: `${out}/${W}_1_shop_r1.png` });
    // round 3 = a duel: the rival is made when the shop opens
    await pg.evaluate(() => { G.round = 3; G.gold = 40; nextOpp(); for (let y = 0; y < 5; y++) for (let x = 0; x < 8; x++) G.open[x + ',' + y] = 1; give('bow', 0, 0, 0); give('hammer', 1, 0, 0); give('shield', 6, 4, 0); give('wand', 7, 0, 0); give('cactus', 5, 0, 0); give('feather', 3, 0, 0); draw(); document.querySelector('#top .rd').click(); });
    const r3 = await pg.evaluate(() => ({ opp: !!G.opp, k: G.opp && G.opp.k, n: G.opp && G.opp.items.length, info: $('#info').textContent }));
    say(W + ' rival made for round 3: ' + r3.k + ', ' + r3.n + ' items', r3.opp && r3.n >= 2 && /ดวลกับผู้เล่น/.test(r3.info));
    await pg.waitForTimeout(200);
    if (H > 370) { say(W + ' link in the info line', await pg.evaluate(() => !!document.querySelector('#info .lk2') && $('#pop').style.display === 'flex')); }   /* the tap on the round chip opened the rival's bag already */
    say(W + ' rival bag pop', await pg.evaluate(() => $('#pop').style.display === 'flex' && document.querySelectorAll('#sct .it').length === G.opp.items.length));
    await pg.screenshot({ path: `${out}/${W}_3_scout.png` }); await pg.evaluate(() => closePop()); await pg.waitForTimeout(150); await pg.screenshot({ path: `${out}/${W}_2_shop_duel.png` });
    const bx = await pg.evaluate(() => [...document.querySelectorAll('#btns button')].filter(e => e.offsetParent).map(e => { const q = e.getBoundingClientRect(); return [e.id, Math.round(q.right), Math.round(q.bottom)]; }));
    say(W + ' buttons inside', bx.every(([, x, y]) => x <= W && y <= H)); const tb = await pg.evaluate(() => { const q = $('#top').getBoundingClientRect(); return [Math.round(q.right), Math.round(q.height)]; }); console.log(W, 'top bar right / height', tb);
    if (W === 844) for (const k of ['wing', 'demon', 'dark', 'hood', 'archer']) {
      await pg.evaluate(k => { G.round = 6; G.hp = 5; G.opp = rivalMake(6, k); d3Rival(k); draw(); }, k); await pg.waitForTimeout(2500);
      await pg.evaluate(() => $('#go').click()); await pg.waitForTimeout(900); await pg.screenshot({ path: `${out}/duel_${k}_0.png` });
      const st = await pg.evaluate(() => ({ foe: D3.foe && D3.foe.rv, pvp: BT && BT.B.pvp, sk: BT && BT.B.sk && BT.B.sk.k, bag: document.querySelectorAll('#fbag .it').length, zone: ZONE }));
      say('duel vs ' + k + ' (3D ' + st.foe + ', zone ' + st.zone + ', bag ' + st.bag + ')', st.foe === k && st.pvp === 1 && st.sk === k && st.bag > 0 && st.zone === 'duel');
      await pg.evaluate(() => { BT.B.sk.g = BT.B.sk.cd - .35; }); await pg.waitForTimeout(1050); await pg.screenshot({ path: `${out}/duel_${k}_1_skill.png` });   /* its champion skill */
      await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/duel_${k}_2.png` });
      await pg.evaluate(() => { spd = 4; BT.B.hp = Math.min(BT.B.hp, 30); }); await pg.waitForFunction(() => !BT && $('#pop').style.display === 'flex', null, { timeout: 60000 });
      const res = await pg.evaluate(() => ({ t: $('#pop div').textContent, cups: G.cups, round: G.round })); say('result vs ' + k + ': ' + res.t.slice(0, 40).replace(/\s+/g, ' '), /ผู้เล่น/.test(res.t) && res.round === 7);
      await pg.screenshot({ path: `${out}/duel_${k}_3_end.png` }); await pg.evaluate(() => { closePop(); spd = 1; });
    }
    if (W === 844) { // a monster round and a boss round still work
      for (const r of [7, 10]) { await pg.evaluate(r => { G.round = r; G.hp = 5; nextOpp(); draw(); $('#go').click(); }, r); await pg.waitForTimeout(1200); await pg.screenshot({ path: `${out}/mon_r${r}.png` });
        const st = await pg.evaluate(() => ({ n: BT.B.name, pvp: !!BT.B.pvp, boss: !!BT.B.boss })); say('round ' + r + ': ' + st.n, !st.pvp && st.boss === (r === 10) && /Lv\./.test(st.n));
        await pg.evaluate(() => { spd = 4; BT.B.hp = 5; }); await pg.waitForFunction(() => !BT && $('#pop').style.display === 'flex', null, { timeout: 60000 }); await pg.evaluate(() => { closePop(); spd = 1; }); } }
    await pg.close();
  }
  console.log(ok ? 'ROUNDS OK' : 'ROUNDS FAIL'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
