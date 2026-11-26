// bag3d.html crafting (owner 2026-11-26 "ระบบผสมไอเทม"): flask hints, craft by drop logic, toast, recipe book, a fight with crafted items, phone sizes.
// python3 -m http.server 8000 ; node tools/qa/bag3d_craft.js [out=/tmp/bag3d_craft] [device scale 1]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_craft', dsf = +(process.argv[3] || 1); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = [];
  for (const [W, H] of [[844, 390], [740, 360]]) {
    const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dsf }); const pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto('http://localhost:8000/bag3d.html'); await pg.waitForTimeout(1500); await pg.click('#start'); await pg.waitForTimeout(800);
    await pg.evaluate(() => { G.gold = 60; give('ember'); give('shield', 0, 1, 0); give('helm'); G.open['0,1'] = G.open['1,1'] = 1; G.shop[0] = { id: 'poison' }; G.shop[1] = { id: 'cactus' }; draw(); });
    await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/${W}_1_hints.png` });
    const r = await pg.evaluate(() => { const sw = G.items.find(o => o.id === 'sword'), em = G.items.find(o => o.id === 'ember'); const ok = tryCraft(em, sw); draw(); return { ok, items: G.items.map(o => o.id + (o.bag ? '@' + o.x + ',' + o.y : ' tray')) }; });
    console.log(W, JSON.stringify(r)); await pg.waitForTimeout(250); await pg.screenshot({ path: `${out}/${W}_2_toast.png` });
    await pg.evaluate(() => { const s = G.items.find(o => o.id === 'shield'), h = G.items.find(o => o.id === 'helm'); tryCraft(h, s); draw(); }); await pg.waitForTimeout(1800);
    await pg.evaluate(() => $('#bk').click()); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/${W}_3_book.png` });
    const bx = await pg.evaluate(() => [...document.querySelectorAll('#btns button')].filter(e => e.offsetParent).map(e => { const r = e.getBoundingClientRect(); return [e.id, Math.round(r.right), Math.round(r.bottom)]; }));
    console.log(W, 'buttons', JSON.stringify(bx), 'screen', W, H, bx.every(([, r, bt]) => r <= W && bt <= H) ? 'ALL INSIDE' : 'SOME OUTSIDE');
    await pg.evaluate(() => { closePop(); sel = null; draw(); }); await pg.screenshot({ path: `${out}/${W}_4_bag.png` });
    if (W === 844) { await pg.evaluate(() => $('#go').click()); await pg.waitForTimeout(7000); await pg.screenshot({ path: `${out}/${W}_5_fight.png` }); }
    await ctx.close();
  }
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
