// The building panel (stars, stats now -> next, cost chips, upgrade button) + range ring + upgrade burst, PC and phone.
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_panel.js <folder>
const {chromium, devices} = require('playwright');
const out = process.argv[2];
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  for (const [name, opts] of [['pc', { viewport: { width: 1280, height: 720 } }], ['phone', { ...devices['Pixel 5 landscape'] }]]) {
    const ctx = await b.newContext(opts), pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(name + ' PAGEERR ' + e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(name + ' console ' + m.text()); });
    try {
      await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && TB.animalsReady, null, {timeout: 150000});
      const tw = await pg.evaluate(() => { const G = GAME.G; GAME.cheat.res(400); GAME.tryUpgrade(G.hall); const p = GAME.spot('tower'); GAME.startBuild('tower'); G.ghostAt = p; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); TB.hold = true; for (let t = 0; t < 30; t += .05) TB.step(.05); TB.camT.set(p.x, 0, p.z - 6); TB.hold = false; return p; });
      await pg.waitForTimeout(500); await pg.evaluate(() => GAME.select(GAME.G.buildings.find(b => b.type === 'tower'))); await pg.waitForTimeout(500);
      log.push(name + ' panel: ' + (await pg.locator('#gSel').textContent()).replace(/\s+/g, ' ').slice(0, 160));
      await pg.screenshot({ path: `${out}/panel_${name}_tower.png` });
      await pg.locator('#gUp').click(); await pg.waitForTimeout(250); await pg.screenshot({ path: `${out}/panel_${name}_upgrading.png` });
      log.push(name + ' after up: lv ' + await pg.evaluate(() => GAME.G.buildings.find(b => b.type === 'tower').lv) + ' | ' + (await pg.locator('#gSel').textContent()).replace(/\s+/g, ' ').slice(0, 120));
      await pg.evaluate(() => { GAME.cheat.res(5); }); await pg.waitForTimeout(400); await pg.screenshot({ path: `${out}/panel_${name}_poor.png` });
      await pg.evaluate(() => { GAME.cheat.res(500); GAME.select(GAME.G.hall); TB.camT.set(GAME.G.hall.x, 0, GAME.G.hall.z - 6); }); await pg.waitForTimeout(600); await pg.screenshot({ path: `${out}/panel_${name}_hall.png` });
      await pg.locator('#gX').click(); await pg.waitForTimeout(200); log.push(name + ' closed: ' + await pg.evaluate(() => document.getElementById('gSel').style.display));
    } catch (e) { errs.push(name + ' TEST ' + e.message); }
    await ctx.close();
  }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 8).join('\n') : 'none')); await b.close();
})();
