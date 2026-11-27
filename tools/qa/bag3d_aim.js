// bag3d.html: does the hero face the enemy while she shoots? Shots of the hero during a fight + her facing (world direction of the bow hand from the chest).
// python3 -m http.server 8000 ; node tools/qa/bag3d_aim.js [out=/tmp/bag3d_aim] [item bow]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_aim', item = process.argv[3] || 'bow'; require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 2 })).newPage();
  pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/bag3d.html' + (process.argv[4] || '')); await pg.waitForTimeout(2000); await pg.click('#start'); await pg.waitForTimeout(600);
  await pg.evaluate(it => { G.round = 6; G.items = []; for (let y = 0; y < 5; y++) for (let x = 0; x < 8; x++) G.open[x + ',' + y] = 1; give(it, 0, 0, 0).lv = 3; give('plate', 3, 0, 0).lv = 3; give('meat', 3, 2, 0).lv = 3; draw(); }, item);
  await pg.evaluate(() => $('#go').click()); await pg.waitForTimeout(1500);
  for (let i = 0; i < 8; i++) {
    const st = await pg.evaluate(() => { const H = D3.hero; if (!H) return null; const c = H.cur && H.cur.getClip().name, t = H.cur && +H.cur.time.toFixed(2);
      const v = new THREE.Vector3(), w = new THREE.Vector3(); H.bone.chest.getWorldPosition(v); (H.bone.handl || H.bone.wristl).getWorldPosition(w); const hl = w.clone().sub(v); (H.bone.handr || H.bone.wristr).getWorldPosition(w); const hr = w.clone().sub(v);
      return { clip: c, t, handL: [hl.x, hl.z].map(n => +n.toFixed(2)), handR: [hr.x, hr.z].map(n => +n.toFixed(2)), rootY: +H.root.rotation.y.toFixed(2) }; });
    await pg.screenshot({ path: `${out}/aim_${i}.png`, clip: { x: 60, y: 60, width: 300, height: 260 } }); console.log(i, JSON.stringify(st)); await pg.waitForTimeout(180);
  }
  console.log(errs.length ? errs : 'no errors'); await b.close();
})();
