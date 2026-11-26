// cards.html: record a bot-vs-bot game as a video (Playwright recordVideo -> ffmpeg mp4). node tools/qa/cards_clip.js [out=/tmp/cards_clip] [seconds 45]
const { chromium } = require('playwright'), { execSync } = require('child_process'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/cards_clip', secs = +(process.argv[3] || 45); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, recordVideo: { dir: out, size: { width: 1266, height: 585 } } });
  const pg = await ctx.newPage(); await pg.goto('http://localhost:8000/cards.html?bot=1'); await pg.waitForTimeout(secs * 1000);
  const v = await pg.video().path(); await ctx.close(); await b.close();
  execSync(`ffmpeg -y -loglevel error -i ${v} -c:v libx264 -pix_fmt yuv420p -crf 23 ${out}/cards.mp4`); console.log('wrote', out + '/cards.mp4');
})();
