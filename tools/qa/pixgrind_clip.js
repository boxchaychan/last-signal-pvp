// pixgrind.html: record a short clip of the hero running round the oasis (frames from PG.sim, so the timing is exact), then ffmpeg -> mp4 + gif.
// python3 -m http.server 8000 ; node tools/qa/pixgrind_clip.js [out=/tmp/pixgrind_clip] [fps 15]
// Path: right along the south shore, up past the palms, left, down. Phone landscape 844 x 390 at device scale 1 (1 texel = 1 px), scaled x2 nearest.
const { chromium } = require('playwright'), { execSync } = require('child_process'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/pixgrind_clip', fps = +(process.argv[3] || 15); fs.mkdirSync(out + '/f', { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 1 })).newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/pixgrind.html?noui=1', { waitUntil: 'load', timeout: 180000 });
  await pg.waitForFunction(() => window.PG && PG.propsReady && PG.frames > 3, null, { timeout: 180000 });
  await pg.evaluate(() => { PG.HERO.x = 50; PG.HERO.z = 77; PG.sim(1); });
  const path = [[0, 0, .8], [1, 0, 2.6], [.6, -.8, 1.6], [0, -1, .9], [-1, 0, 2.4], [-.5, .9, 1.4], [0, 0, 1.2]];   /* dx, dz, seconds */
  let n = 0;
  for (const [dx, dz, sec] of path) for (let t = 0; t < sec; t += 1 / fps) {
    await pg.evaluate(([dx, dz, dt]) => { PG.auto = dx || dz ? [dx, dz] : null; PG.sim(dt, dt / 4); }, [dx, dz, 1 / fps]);
    await pg.screenshot({ path: `${out}/f/${String(n++).padStart(4, '0')}.png` });
  }
  await b.close(); console.log('frames', n, errs.length ? 'ERRORS ' + errs.join(' | ') : 'no errors');
  execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${out}/f/%04d.png -vf "scale=iw*2:ih*2:flags=neighbor" -c:v libx264 -pix_fmt yuv420p -crf 18 ${out}/run.mp4`);
  execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${out}/f/%04d.png -vf "scale=iw:ih:flags=neighbor,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none" ${out}/run.gif`);
  console.log('wrote', `${out}/run.mp4`, `${out}/run.gif`);
})();
