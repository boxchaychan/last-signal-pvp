// Saves the class portrait sheets of bag3d.html: art/bag3d/cls_<class>.png (450 x 150, 3 poses). python3 -m http.server 8000 ; node tools/art/cls_portraits.js
const { chromium } = require('playwright'), fs = require('fs');
(async () => {
  const b = await chromium.launch(), pg = await b.newPage(), errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/tools/art/cls_portraits.html'); await pg.waitForFunction(() => typeof window.render === 'function');
  const out = await pg.evaluate(() => window.render());
  for (const k in out) { fs.writeFileSync(`art/bag3d/cls_${k}.png`, Buffer.from(out[k].split(',')[1], 'base64')); console.log('art/bag3d/cls_' + k + '.png'); }
  console.log(errs.length ? 'ERRORS ' + errs.join(' | ') : 'no errors'); await b.close();
})();
