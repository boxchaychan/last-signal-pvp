// bag3d.html item skill effects (bag3d/cast.js): freezes a fight and plays every item's own effect, 3 frames each, for a contact sheet.
// python3 -m http.server 8000 ; node tools/qa/bag3d_cast.js [out=/tmp/bag3d_cast] [ids,comma (default: every item that fires)] [side 0 hero / 1 enemy]
// then: python3 tools/qa/bag3d_cast_sheet.py <out>   (joins the frames into sheet_*.png)
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_cast', only = process.argv[3] && process.argv[3] !== 'all' ? process.argv[3].split(',') : null, side = +(process.argv[4] || 0);
  require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 1 })).newPage(), errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/bag3d.html?mute=1'); await pg.waitForTimeout(2500); await pg.click('#start'); await pg.waitForTimeout(400);
  await pg.evaluate(() => { G.round = 4; $('#go').click(); }); await pg.waitForTimeout(2500);
  const ids = await pg.evaluate(only => { window.tick = () => {}; window.requestAnimationFrame = () => 0; BT.px.length = 0; BT.wp.length = 0; BT.fx.length = 0; $('#mybag').style.display = $('#fbag').style.display = 'none';
    return only || Object.keys(IT).filter(k => CAST[k] || CASTSELF[k]); }, only);
  const T = [.1, .24, .4];
  for (const id of ids) {
    await pg.evaluate(([id, side]) => { const b = BT; b.px.length = 0; b.wp.length = 0; b.fx.length = 0; b.sh = 0; b.flash = 0; b.punch = 0; b.eh = b.hh = 0; window.__t = 0; const it = { u: 99000, id, lv: 1 }, d = IT[id], e = { s: side, k: d.blk ? 'blk' : d.heal ? 'heal' : 'hit', v: 12, u: it.u, big: (d.dmg || 0) >= 12, mg: d.ty === 'mag' };
      if (e.k === 'hit') { const dl = castHit(b, e, it); if (!NOPOP[CAST[id][0]]) b.wp.push({ s: side, id, i: d.i, t: 0 }); b.fx.push({ x: side ? .26 : .74, t: -dl, v: 12, c: '#fff', dx: 0 }); } else castSelf(b, e, it); }, [id, side]);
    for (let i = 0; i < T.length; i++) {
      await pg.evaluate(t1 => { const b = BT; while (window.__t < t1 - 1e-6) { const dt = Math.min(1 / 60, t1 - window.__t); window.__t += dt; vfxStep(b, dt); for (const w of b.wp) w.t += dt; for (const f of b.fx) f.t += dt; for (const k of ['ha', 'ea', 'hh', 'eh', 'sh']) b[k] = Math.max(0, b[k] - dt); b.flash = Math.max(0, b.flash - dt * 2.2); } paint(performance.now() / 1000); }, T[i]);
      await pg.screenshot({ path: `${out}/${id}_${i}.png`, clip: { x: 0, y: 0, width: 844, height: 290 } });
    }
  }
  require('fs').writeFileSync(`${out}/ids.json`, JSON.stringify(ids)); console.log(ids.length, 'items'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
