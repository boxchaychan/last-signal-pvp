// Saves the class portrait sheets of bag3d.html: art/bag3d/cls_<class>.png (450 x 150, 3 poses). python3 -m http.server 8000 ; node tools/art/cls_portraits.js [class ...] (none = all five) | --icon (the app icon picture, then python3 tools/art/bag_app_icon.py)
const { chromium } = require('playwright'), fs = require('fs');
(async () => {
  const b = await chromium.launch(), pg = await b.newPage(), errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/tools/art/cls_portraits.html?t=' + Date.now()); await pg.waitForFunction(() => typeof window.render === 'function');
  const icon = process.argv.includes('--icon'), only = process.argv.slice(2).filter(a => a !== '--icon');
  if (icon) {   /* --icon: the knight's first pose at 512 px for the home-screen icon (tools/art/bag_app_icon.py frames it) */
    const o = await pg.evaluate(() => window.render(['knight'], 512)); fs.mkdirSync('/tmp/bag_icon', { recursive: true }); fs.writeFileSync('/tmp/bag_icon/knight512.png', Buffer.from(o.knight.split(',')[1], 'base64')); console.log('/tmp/bag_icon/knight512.png');
  } else { const out = await pg.evaluate(o => window.render(o), only);
    for (const k in out) { fs.writeFileSync(`art/bag3d/cls_${k}.png`, Buffer.from(out[k].split(',')[1], 'base64')); console.log('art/bag3d/cls_' + k + '.png'); } }
  console.log(errs.length ? 'ERRORS ' + errs.join(' | ') : 'no errors'); await b.close();
})();
