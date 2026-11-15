// Plays kaiju.html (อสูรถล่มเมือง, 3D-pixel test) like a person on a phone in landscape: touch-drag joystick, stomp button, breath button,
// camera button; checks errors, that buildings fall, that each camera preset renders, and saves screenshots.
//   python3 -m http.server 8000        (repo root, in another shell)
//   node tools/qa/kaiju_play.js [folder for screenshots] [dpr, 3 = real phone]
const {chromium} = require('playwright');
const out = process.argv[2] || '', DPR = +(process.argv[3] || 3);
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: DPR, hasTouch: true}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message)); pg.on('console', m => { if (m.type() === 'error' || /WARNING|THREE/.test(m.text())) errs.push('console ' + m.text()); });
  pg.on('requestfailed', r => errs.push('fail ' + r.url())); pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const box = async sel => { const r = await pg.locator(sel).boundingBox(); return [r.x + r.width / 2, r.y + r.height / 2]; };
  // a pointer "finger" on the left half: press, drag, hold, release (mouse events are pointer events in Chromium)
  const walk = async (dx, dy, ms) => { await pg.mouse.move(200, 250); await pg.mouse.down(); await pg.mouse.move(200 + dx, 250 + dy, {steps: 4}); await pg.waitForTimeout(ms); await pg.mouse.up(); };
  const press = async (sel, ms) => { const [x, y] = await box(sel); await pg.mouse.move(x, y); await pg.mouse.down(); await pg.waitForTimeout(ms || 80); await pg.mouse.up(); };
  try {
    const t0 = Date.now();
    await pg.goto('http://localhost:8000/kaiju.html'); await pg.waitForFunction(() => window.KJ && KJ.ready, null, {timeout: 30000});
    log.push('ready in ' + (Date.now() - t0) + ' ms, ' + JSON.stringify(await pg.evaluate(() => KJ.info())));
    await pg.waitForTimeout(600); await shot('k01_start');
    // every camera preset by the real button
    for (let i = 0; i < 4; i++) { await pg.waitForTimeout(400); await shot('k02_cam' + (await pg.evaluate(() => KJ.info().cam))); await press('#bCam'); }
    log.push('camera after 4 presses: ' + await pg.evaluate(() => KJ.info().cam));
    // walk right, into the block, push buildings
    const p0 = await pg.evaluate(() => [KJ.K.x, KJ.K.z]);
    await walk(60, 0, 900); const p1 = await pg.evaluate(() => [KJ.K.x, KJ.K.z, KJ.K.sprN]);
    log.push(`walk right: (${p0.map(v => v.toFixed(1))}) -> (${p1.slice(0, 2).map(v => (+v).toFixed(1))}) sprite ${p1[2]}`);
    await walk(0, 60, 700); log.push('walk down -> sprite ' + await pg.evaluate(() => KJ.K.sprN));
    await walk(0, -60, 700); log.push('walk up -> sprite ' + await pg.evaluate(() => KJ.K.sprN));
    await walk(-60, 0, 500); log.push('walk left -> sprite ' + await pg.evaluate(() => KJ.K.sprN) + ' flip ' + await pg.evaluate(() => KJ.K.flip));
    await shot('k03_walked');
    // walk to the nearest building and stomp it
    const tgt = await pg.evaluate(() => { let best = null, bd = 1e9; for (const b of KJ.B) { if (!b.alive) continue; const d = Math.hypot(b.x - KJ.K.x, b.z - KJ.K.z); if (d < bd) { bd = d; best = b; } } return {x: best.x, z: best.z, hp: best.hp}; });
    await pg.evaluate(t => { KJ.K.x = t.x + 9; KJ.K.z = t.z + 9; }, tgt);
    for (let i = 0; i < 5; i++) { await press('#bStomp'); await pg.waitForTimeout(i === 0 ? 260 : 560); if (i === 0) await shot('k04_stomp_hit'); }
    await pg.waitForTimeout(300); await shot('k05_collapse');
    log.push('after 5 stomps: ' + JSON.stringify(await pg.evaluate(() => ({pct: KJ.info().pct, fallen: KJ.B.filter(b => !b.alive).length}))));
    // breath: hold the fire button while facing a block
    await walk(-60, 30, 300);
    const [fx, fy] = await box('#bFire'); await pg.mouse.move(fx, fy); await pg.mouse.down(); await pg.waitForTimeout(700); await shot('k06_breath'); await pg.waitForTimeout(1500); await pg.mouse.up();
    await pg.waitForTimeout(1500); await shot('k07_after');
    log.push('after breath: ' + JSON.stringify(await pg.evaluate(() => ({pct: KJ.info().pct, fallen: KJ.B.filter(b => !b.alive).length, burning: KJ.B.filter(b => b.fire > 0).length}))));
    // frame time
    const ft = await pg.evaluate(() => new Promise(res => { let n = 0, t0 = performance.now(); const f = () => { if (++n === 60) res((performance.now() - t0) / 60); else requestAnimationFrame(f); }; requestAnimationFrame(f); }));
    log.push('avg frame ' + ft.toFixed(1) + ' ms (headless, software GL)');
    // zoom buttons
    await press('#bZo'); await pg.waitForTimeout(300); log.push('zoom out -> ' + JSON.stringify(await pg.evaluate(() => KJ.info()))); await shot('k08_zoomout');
    await press('#bZi'); await press('#bZi'); await pg.waitForTimeout(300); await shot('k09_zoomin');
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.join('\n') : 'none'));
  await b.close();
})();
