// Graphics modes of tribe3d.html (owner 2026-11-16 "12"): a PC viewport starts in the pretty mode (smooth, supersampled, soft
// shadows, rim light), a phone starts in the pixel mode; the fort / hall panels show unit cards with rendered portraits.
//   python3 -m http.server 8000        (repo root)
//   node tools/qa/tribe3d_gfx.js [folder for screenshots]
const {chromium, devices} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  for (const [name, opts] of [['pc', { viewport: { width: 1280, height: 720 } }], ['phone', { ...devices['Pixel 5 landscape'] }]]) {
    const ctx = await b.newContext(opts), pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(name + ' PAGEERR ' + e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(name + ' console ' + m.text()); });
    try {
      await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && TB.animalsReady, null, {timeout: 150000});
      const st = await pg.evaluate(() => ({ gfx: GFX, label: document.getElementById('pixL').textContent, shadow: TB.renderer.shadowMap.type, buf: TB.renderer.domElement.width + 'x' + TB.renderer.domElement.height, portraits: Object.keys(GAME.PEOPLE.portrait || {}).join(',') }));
      log.push(name + ': ' + JSON.stringify(st));
      const f = await pg.evaluate(() => { const G = GAME.G; GAME.cheat.res(3000); GAME.tryUpgrade(G.hall); const p = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = p; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); TB.hold = true; for (let t = 0; t < 30; t += .05) TB.step(.05); for (const f of GAME.forts()) { GAME.train(f, 2, 'warrior'); GAME.train(f, 2, 'hunter'); } GAME.train(G.hall, 1, 'shaman'); for (let t = 0; t < 30; t += .05) TB.step(.05); TB.camT.set(p.x, 0, p.z + 3); TB.zoomBy(2); TB.hold = false; return p; });
      await pg.waitForTimeout(1500); if (out) await pg.screenshot({ path: `${out}/gfx_${name}_units.png` });
      await pg.evaluate(() => { GAME.select(GAME.forts()[0]); }); await pg.waitForTimeout(400); if (out) await pg.screenshot({ path: `${out}/gfx_${name}_fortcard.png` });
      log.push(name + ' card imgs: ' + await pg.locator('#gSel .uc img').count());
      if (name === 'pc') { for (let i = 0; i < 3; i++) { await pg.locator('#bPix').click(); await pg.waitForTimeout(400); log.push('toggle -> ' + await pg.evaluate(() => GFX + ' ' + document.getElementById('pixL').textContent)); } }
    } catch (e) { errs.push(name + ' TEST ' + e.message); }
    await ctx.close();
  }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 12).join('\n') : 'none'));
  await b.close();
})();
