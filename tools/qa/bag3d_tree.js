// bag3d.html MOBA build tree (owner 2026-11-27 "ทำเลยโมบ้ากระเป๋า"): build shop, partial prices, joining by drop, unique ultimates, a fight with tree items.
// Since the BIG ITEM REDESIGN (2026-11-28) the 7 old parts are MATERIALS: bought into the pouch G.mats (not the bag), used up by a recipe; two crafted
// items dropped on each other make the biggest ones (m_mail + m_charm = f_bastion).
// python3 -m http.server 8000 ; node tools/qa/bag3d_tree.js [out=/tmp/bag3d_tree] [device scale 1]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_tree', dsf = +(process.argv[3] || 1); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; let ok = true;
  for (const [W, H] of [[844, 390], [740, 360]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dsf })).newPage();
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto('http://localhost:8000/bag3d.html?fight=side'); await pg.waitForTimeout(1500); await pg.click('#start'); await pg.waitForTimeout(500);
    await pg.evaluate(() => { G.gold = 80; for (let y = 0; y < 5; y++) for (let x = 0; x < 8; x++) G.open[x + ',' + y] = 1; draw(); $('#bk').click(); });
    await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/${W}_1_shop.png` });
    const r = await pg.evaluate(() => { const R = {}, g0 = G.gold;
      treeBuy('p_blade'); treeBuy('p_fang'); R.pouch = (G.mats.p_blade | 0) + (G.mats.p_fang | 0); R.parts_in_bag = G.items.filter(o => IT[o.id].mat).length; R.edge_cost_with_parts = treeCost('m_edge').cost; treeBuy('m_edge'); R.pouch_after_edge = (G.mats.p_blade | 0) + (G.mats.p_fang | 0); R.after_edge = G.items.map(o => o.id).filter(k => IT[k].tree).join(',');
      treeBuy('p_feather'); R.claws_cost = treeCost('m_claws').cost; treeBuy('m_claws'); R.king_cost = treeCost('f_kingslayer').cost; treeBuy('f_kingslayer'); R.king2 = treeBuy('f_kingslayer');
      R.tree_items = G.items.map(o => o.id).filter(k => IT[k].tree).join(','); R.spent = g0 - G.gold;
      const h = give('m_mail', 0, 4, 0), p = give('m_charm', 2, 4, 0), g1 = G.gold; R.join = tryBuild(p, h); R.join_fee = g1 - G.gold;   /* two crafted items dropped on each other */
      mats().p_hide = 1; mats().p_plate = 1; R.mail_cost_pouch = treeCost('m_mail').cost; R.mail_buy = treeBuy('m_mail'); R.pouch_after_mail = (G.mats.p_hide | 0) + (G.mats.p_plate | 0);   /* both materials in the pouch: only the fee */ R.after_join = G.items.map(o => o.id).filter(k => IT[k].tree).join(',');
      const f = build(G.items.filter(o => o.bag), 100, {}, {}); R.all = +f.all.toFixed(2); R.gcrit = +f.crit.toFixed(2); R.hp = f.max; R.inShop = G.shop.some(s => IT[s.id].tree);
      draw(); pop(treeHtml()); return R; });
    console.log(W, JSON.stringify(r));
    const pass = r.pouch === 2 && r.parts_in_bag === 0 && r.pouch_after_edge === 0 && r.edge_cost_with_parts === 3 && r.claws_cost === 6 && r.king_cost === 6 && r.king2 === false && r.join === true && r.join_fee === 6 && /f_bastion/.test(r.after_join) && r.mail_cost_pouch === 3 && r.mail_buy === true && r.pouch_after_mail === 0 && !r.inShop && /f_kingslayer/.test(r.tree_items); console.log(W, pass ? 'ok  ' : 'FAIL', 'materials in the pouch, recipes, two-item join, unique ultimate'); ok = ok && pass;
    await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/${W}_2_after.png` });
    const bx = await pg.evaluate(() => { closePop(); sel = G.items.find(o => o.id === 'f_kingslayer'); draw(); return [...document.querySelectorAll('#btns button')].filter(e => e.offsetParent).map(e => { const q = e.getBoundingClientRect(); return [e.id, Math.round(q.right), Math.round(q.bottom)]; }); });
    console.log(W, 'buttons inside:', bx.every(([, x, y]) => x <= W && y <= H)); await pg.screenshot({ path: `${out}/${W}_3_bag.png` });
    if (W === 844) { await pg.evaluate(() => { G.round = 9; $('#go').click(); }); await pg.waitForTimeout(6000); await pg.screenshot({ path: `${out}/${W}_4_fight.png` }); }
  }
  console.log(ok ? 'TREE OK' : 'TREE FAIL'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
