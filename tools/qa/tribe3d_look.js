// Overall look of tribe3d.html: a small built base (hut, farm, tower, fort, walls, units) at day, dusk and night, wide and
// close, on a PC (pretty mode) and a phone (pixel mode). Screenshots only (+ errors).
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_look.js <folder> [pc|phone]
const {chromium, devices} = require('playwright');
const out = process.argv[2], only = process.argv[3];
(async () => { const b = await chromium.launch(); const errs = [];
  for (const [name, opts] of [['pc', { viewport: { width: 1280, height: 720 } }], ['phone', { ...devices['Pixel 5 landscape'] }]]) {
    if (only && only !== name) continue;
    const ctx = await b.newContext(opts), pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(name + ' PAGEERR ' + e.message));
    try {
      await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && TB.animalsReady, null, {timeout: 150000});
      await pg.evaluate(() => { const G = GAME.G; GAME.cheat.res(5000); GAME.tryUpgrade(G.hall); GAME.tryUpgrade(G.hall);
        for (const t of ['hut', 'hut', 'farm', 'tower', 'fort', 'tower', 'fire', 'store']) { const p = GAME.spot(t); if (!p) continue; GAME.startBuild(t); G.ghostAt = p; G.ghostOk = true; GAME.confirmBuild(); }
        document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); TB.hold = true; for (let t = 0; t < 60; t += .05) TB.step(.05);
        for (const f of GAME.forts()) { GAME.train(f, 3, 'warrior'); GAME.train(f, 2, 'hunter'); } GAME.train(G.hall, 1, 'shaman'); for (let t = 0; t < 40; t += .05) TB.step(.05);
        GAME.select(null); TB.camT.set(G.hall.x + 14, 0, G.hall.z + 4); TB.hold = false; });
      for (const [tag, setup] of [['day', 'GAME.G.t = 30'], ['dusk', 'GAME.G.t = 114'], ['night', 'GAME.G.t = 140']]) {
        await pg.evaluate(s => { eval(s); TB.hold = true; TB.step(.05); TB.hold = false; }, setup); await pg.waitForTimeout(1200);
        await pg.screenshot({ path: `${out}/look_${name}_${tag}.png` });
      }
      await pg.evaluate(() => { GAME.G.t = 30; TB.zoomBy(-2); }); await pg.waitForTimeout(1200); await pg.screenshot({ path: `${out}/look_${name}_wide.png` });
    } catch (e) { errs.push(name + ' TEST ' + e.message); }
    await ctx.close();
  }
  console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 8).join('\n') : 'none')); await b.close();
})();
