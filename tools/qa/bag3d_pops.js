// bag3d.html: weapon pops + projectiles point at the enemy (owner "หน้าเวลายิงหันให้ถูกด้าน"). Freezes a fight and draws the pop / flying shot of each weapon for both sides.
// python3 -m http.server 8000 ; node tools/qa/bag3d_pops.js [out=/tmp/bag3d_pops] [ids bow,frostbow,javelin,frostlance,wand]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_pops', ids = (process.argv[3] || 'bow,frostbow,javelin,frostlance,wand').split(','); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 1 })).newPage(); pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/bag3d.html'); await pg.waitForTimeout(2000); await pg.click('#start'); await pg.waitForTimeout(400);
  await pg.evaluate(() => { G.items = []; give('plate', 0, 0, 0).lv = 3; give('bow', 3, 0, 0); draw(); $('#go').click(); }); await pg.waitForTimeout(1500); await pg.evaluate(() => { spd = 1e-9; });
  for (const id of ids) for (const [tag, t] of [['pop', .22], ['fly', .1]]) {
    await pg.evaluate(([id, tag, t]) => { const b = BT; b.px = []; b.fx = []; b.sl = []; b.wp = []; b.pj = []; const i = IT[id].i;
      if (tag === 'pop') b.wp.push({ s: 0, id, i, t }, { s: 1, id, i, t }); else b.pj.push({ s: 0, id, i, t }, { s: 1, id, i, t: t + .04 });
      clearInterval(window.__hold); window.__hold = setInterval(() => { for (const w of b.wp) w.t = .22; for (const q of b.pj) q.t = q.s ? .14 : .1; }, 4); }, [id, tag, t]);
    await pg.waitForTimeout(tag === 'pop' ? 160 : 110); await pg.screenshot({ path: `${out}/${id}_${tag}.png`, clip: { x: 0, y: 40, width: 844, height: 230 } });
  }
  console.log(errs.length ? errs : 'no errors'); await b.close();
})();
