// Opens tribe3d.html (stone-age tribe, wide 3D-pixel map) like a phone in landscape: loads, pans by dragging, zooms with the buttons,
// cycles the camera and the time of day; collects errors and saves screenshots.
//   python3 -m http.server 8000        (repo root, in another shell)
//   node tools/qa/tribe3d_check.js [folder for screenshots] [dpr, 3 = real phone]
const {chromium} = require('playwright');
const out = process.argv[2] || '', DPR = +(process.argv[3] || 3);
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: DPR}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  pg.on('requestfailed', r => errs.push('fail ' + r.url())); pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const press = async sel => { const r = await pg.locator(sel).boundingBox(); await pg.mouse.click(r.x + r.width / 2, r.y + r.height / 2); await pg.waitForTimeout(350); };
  try {
    const t0 = Date.now();
    await pg.goto('http://localhost:8000/tribe3d.html'); await pg.waitForFunction(() => window.TB && TB.ready, null, {timeout: 60000});
    log.push('ready in ' + (Date.now() - t0) + ' ms ' + JSON.stringify(await pg.evaluate(() => TB.info())));
    await pg.waitForTimeout(800); await shot('t01_village');
    await pg.mouse.move(420, 200); await pg.mouse.down(); await pg.mouse.move(250, 280, {steps: 6}); await pg.mouse.up(); await pg.waitForTimeout(300);
    log.push('after drag camT ' + JSON.stringify(await pg.evaluate(() => [TB.camT.x.toFixed(1), TB.camT.z.toFixed(1)])));
    await shot('t02_dragged');
    await press('#bZo'); log.push('zoom out ' + JSON.stringify(await pg.evaluate(() => TB.info().S))); await shot('t03_zoomout');
    await press('#bTime'); await pg.waitForTimeout(400); await shot('t04_sunset'); await press('#bTime'); await pg.waitForTimeout(600); await shot('t05_night'); await press('#bTime');
    await press('#bZi'); await press('#bCam'); await pg.waitForTimeout(300); await shot('t06_camC');
    const ft = await pg.evaluate(() => new Promise(res => { let n = 0, t0 = performance.now(); const f = () => { if (++n === 30) res((performance.now() - t0) / 30); else requestAnimationFrame(f); }; requestAnimationFrame(f); }));
    log.push('avg frame ' + ft.toFixed(0) + ' ms (headless software GL, not a phone number)');
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.join('\n') : 'none'));
  await b.close();
})();
