// bag3d.html look shots: home, shop (with a few items and a crafted one), a fight moment. node tools/qa/bag3d_look.js [out] [scale 2] [w 844] [h 390]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_look', dsf = +(process.argv[3] || 2), W = +(process.argv[4] || 844), H = +(process.argv[5] || 390); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; const pg = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dsf })).newPage();
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/bag3d.html?fight=side' + (process.argv[6] || '')); await pg.waitForTimeout(2500); await pg.screenshot({ path: `${out}/home_${W}.png` });
  await pg.click('#start'); await pg.waitForTimeout(800);
  await pg.evaluate(() => { G.round = 6; G.gold = 40; for (const [id, x, y, lv] of [['flamesword', 2, 2, 3], ['shield', 4, 2, 2], ['meat', 4, 3, 1], ['clover', 3, 1, 1]]) { G.open[x + ',' + y] = 1; const o = give(id, x, y, 0); o.lv = lv; } G.open['5,2'] = G.open['5,3'] = G.open['4,3'] = 1; roll(true); draw(); });
  await pg.waitForTimeout(600); await pg.screenshot({ path: `${out}/shop_${W}.png` });
  await pg.evaluate(() => $('#go').click()); await pg.waitForTimeout(5000); await pg.screenshot({ path: `${out}/fight_${W}.png` });
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
