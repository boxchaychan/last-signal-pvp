// pixgrind.html (pixel 3D level grinder, map 1 = desert oasis): screenshots at phone size + page errors.
// python3 -m http.server 8000 ; node tools/qa/pixgrind_check.js [out=/tmp/pixgrind] [extra query] [device scale 3] [spots=start,pool,north,east]
// spots: the hero is moved there (PG.HERO) and the game runs a moment (PG.sim) before the shot; "walk" = holds right for 1.5 s (run frames).
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/pixgrind', extra = process.argv[3] || '', dsf = +(process.argv[4] || 3), spots = (process.argv[5] || 'start,walk,pool,north,east').split(',');
  require('fs').mkdirSync(out, { recursive: true }); const errs = [];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf })).newPage();
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
  const t0 = Date.now(); await pg.goto('http://localhost:8000/pixgrind.html?noui=0' + extra, { waitUntil: 'load', timeout: 180000 });
  await pg.waitForFunction(() => window.PG && PG.propsReady && PG.frames > 3, null, { timeout: 180000 }); console.log('ready ms', Date.now() - t0);
  console.log(JSON.stringify(await pg.evaluate(() => ({ px: [PG.PX.bw, PG.PX.bh, PG.PX.k], tris: PG.renderer.info.render.triangles, calls: PG.renderer.info.render.calls }))));
  const SP = { start: null, pool: [64, 66], ledge: [60, 57], ramp: [74, 56], upper: [92, 40], north: [44, 27], east: [104, 40], south: [40, 92] };
  for (const sp of spots) {
    await pg.evaluate(([sp, p]) => { PG.auto = null; if (p) { PG.HERO.x = p[0]; PG.HERO.z = p[1]; } if (sp === 'walk') PG.auto = [1, 0]; PG.sim(sp === 'walk' ? 1.5 : 1.2); }, [sp, SP[sp] || null]);
    await pg.waitForTimeout(400); await pg.screenshot({ path: `${out}/${sp}.png` }); console.log('shot', `${out}/${sp}.png`);
  }
  if (errs.length) console.log('ERRORS:\n' + [...new Set(errs)].slice(0, 12).join('\n')); else console.log('no errors'); await b.close();
})();
