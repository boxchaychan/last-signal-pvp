// bag3d.html balance: BG.sim(n) with the smart and the random shop bot (rounds reached). python3 -m http.server 8000 ; node tools/qa/bag3d_sim.js [games 60]
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/bag3d.html'); await pg.waitForTimeout(1500); await pg.click('#start'); await pg.waitForTimeout(500);
  console.log(JSON.stringify(await pg.evaluate(n => [BG.sim(n, true), BG.sim(n, false)], +(process.argv[2] || 60)))); console.log(errs.length ? errs : 'no errors'); await b.close(); })();
