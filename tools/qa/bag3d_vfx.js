// bag3d.html battle effects: a round-8 fight with crafted ★3 items (flame sword, thunder hammer, vampire claw, fortress shield), shots along the way + the KO.
// python3 -m http.server 8000 ; node tools/qa/bag3d_vfx.js [out=/tmp/bag3d_vfx] [device scale 1]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_vfx', dsf = +(process.argv[3] || 1); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf })).newPage();
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/bag3d.html'); await pg.waitForTimeout(1500); await pg.click('#start'); await pg.waitForTimeout(800);
  await pg.evaluate(() => { G.round = +(new URLSearchParams(location.search).get('r') || 8); G.items = []; for (let y = 0; y < 5; y++) for (let x = 0; x < 8; x++) G.open[x + ',' + y] = 1;
    for (const [id, x, y] of [['flamesword', 0, 0], ['thunderhammer', 1, 0], ['vampclaw', 3, 0], ['fortress', 4, 0], ['feast', 4, 1], ['frostbow', 6, 0]]) { const o = give(id, x, y, 0); o.lv = 3; } draw(); });
  await pg.evaluate(() => $('#go').click()); let n = 0, ko = 0;
  for (let i = 0; i < 90 && n < 14; i++) { const st = await pg.evaluate(() => BT ? { pv: BT.pv.map(v => v.nm.split('/')[1]).join(','), slow: BT.slow > 0, T: +BT.T.toFixed(1), hp: [Math.round(BT.A.hp), Math.round(BT.B.hp)] } : null); if (!st) break;
    if ((st.pv && i % 2 === 0) || (st.slow && !ko)) { if (st.slow) ko = 1; await pg.screenshot({ path: `${out}/fx_${String(n++).padStart(2, '0')}${st.slow ? '_ko' : ''}.png` }); console.log(n, JSON.stringify(st)); } }
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
