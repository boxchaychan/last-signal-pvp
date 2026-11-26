// cardtest.html: video of the 3D card being tilted by the pointer, then flipped (tap) and back. node tools/qa/cardtest_clip.js [out=/tmp/cardtest_clip]
const { chromium } = require('playwright'), { execSync } = require('child_process'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/cardtest_clip'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 420, height: 560 }, deviceScaleFactor: 1, recordVideo: { dir: out, size: { width: 420, height: 560 } } });
  const pg = await ctx.newPage(); await pg.goto('http://localhost:8000/cardtest.html'); await pg.waitForTimeout(3000);
  const path = [[210, 280], [380, 140], [60, 120], [40, 460], [390, 470], [210, 280]];
  for (const [x, y] of path) { await pg.mouse.move(x, y, { steps: 25 }); await pg.waitForTimeout(500); }
  await pg.mouse.click(210, 280); await pg.waitForTimeout(2200); await pg.mouse.click(210, 280); await pg.waitForTimeout(2500);
  const v = await pg.video().path(); await ctx.close(); await b.close();
  execSync(`ffmpeg -y -loglevel error -ss 2.5 -i ${v} -vf scale=630:840:flags=lanczos -c:v libx264 -pix_fmt yuv420p -crf 22 ${out}/card3d.mp4`); console.log('wrote', out + '/card3d.mp4');
})();
