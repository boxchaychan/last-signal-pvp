// pixmap.html "แมพพิกเซล" (3D map + 2D hero). Screenshots of a few places + build numbers (time, triangles, walkable area) + page errors.
// python3 -m http.server 8000 ; node tools/qa/pixmap_check.js [out=/tmp/pixmap] [extra query, e.g. "&look=px"] [scale=1] [spots=start,oasis,falls,stairs,plateau,far,temple,camp,arch]
// spots: start = where the hero starts; oasis / falls / stairs / plateau / far = the hero is moved there (MAP.HERO) and the camera snaps onto it.
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/pixmap', extra = process.argv[3] || '', dsf = +(process.argv[4] || 1), spots = (process.argv[5] || 'start,oasis,falls,stairs,plateau,far').split(',');
  require('fs').mkdirSync(out, { recursive: true }); const errs = [];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf })).newPage();
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  const t0 = Date.now(); await pg.goto('http://localhost:8000/pixmap.html?noui=0' + extra, { waitUntil: 'load', timeout: 180000 });
  await pg.waitForFunction(() => window.MAP && MAP.renderer.info.render.frame > 3, null, { timeout: 180000 }); const load = Date.now() - t0; await pg.waitForTimeout(2500);
  const info = await pg.evaluate(() => { const { A, sizes } = MAP.areas(); const r = MAP.renderer.info; return { N: MAP.N, tris: r.render.triangles, calls: r.render.calls, geos: r.memory.geometries, tex: r.memory.textures, areas: sizes.filter(s => s > 3).length, biggest: Math.max(...sizes), build: MAP.BUILD_MS }; });
  console.log('load ms', load, JSON.stringify(info));
  for (const sp of spots) {
    const ok = await pg.evaluate(sp => { const M = MAP, H = M.HERO, N = M.N; let p = null;
      const find = fn => { let best = null; for (let k = 0; k < 40000 && !best; k++) { const x = 2 + Math.random() * (N - 4), z = 2 + Math.random() * (N - 4); if (fn(x, z) && M.walkable(x, z)) best = [x, z]; } return best; };
      if (sp === 'start') p = [M.START[0], M.START[1]];
      else if (sp === 'oasis') p = find((x, z) => M.kAt(x, z) === 1 && M.kAt(x + 1.5, z) === 2);
      else if (sp === 'falls') { const F = M.FALLS[Math.floor(M.FALLS.length / 2)]; if (F) p = find((x, z) => Math.hypot(x - F.b[0], z - F.b[1] - 3) < 3); }
      else if (sp === 'stairs') { for (let c = 0; c < N * N && !p; c++) if (M.STAIR[c] >= 0 && Math.random() < .2) p = [c % N + .5, Math.floor(c / N) + 2.5]; if (p && !M.walkable(p[0], p[1])) p = find((x, z) => Math.hypot(x - p[0], z - p[1]) < 3); }
      else if (sp === 'plateau') p = find((x, z) => M.L[Math.floor(z) * N + Math.floor(x)] >= 2);
      else if (sp === 'temple' && M.SPOTS.temple) p = [M.SPOTS.temple[0] + 1, M.SPOTS.temple[1] + 8.5];
      else if (sp === 'camp' && M.SPOTS.camp) p = [M.SPOTS.camp[0] + 1.5, M.SPOTS.camp[1] + 5.5];
      else if (sp === 'arch' && M.SPOTS.arches && M.SPOTS.arches[0]) p = [M.SPOTS.arches[0][0], M.SPOTS.arches[0][1] + 3];
      else if (sp === 'far') p = find((x, z) => x > N * .7 && z > N * .6);
      if (!p) return false; H.x = p[0]; H.z = p[1]; H.y = M.groundH(p[0], p[1]); M.CAM.look.set(H.x * M.WS, H.y * M.WS + .5, H.z * M.WS); return true; }, sp);
    if (!ok) { console.log('spot', sp, 'not found'); continue; }
    await pg.waitForTimeout(900); await pg.screenshot({ path: `${out}/${sp}.png` }); console.log('shot', `${out}/${sp}.png`);
  }
  if (errs.length) console.log('ERRORS:\n' + [...new Set(errs)].slice(0, 12).join('\n')); else console.log('no errors'); await b.close();
})();
