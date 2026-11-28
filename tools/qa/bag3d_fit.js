// bag3d.html on short phone screens (owner 2026-11-28 "ทำเต็มจอหน่อย กดเข้าเกมไม่ได้": with the browser bar showing, the class cards
// pushed the start button off the screen). Start screen at 6 sizes down to 640 x 280: the start button is on screen and can be tapped;
// the shop's buttons are all inside after it; the fullscreen button turns full screen on and off; tapping start goes full screen;
// the home-screen manifest (bag3d.webmanifest) is fullscreen + landscape with an icon that loads.
// python3 -m http.server 8000 ; node tools/qa/bag3d_fit.js [out=/tmp/bag3d_fit]   (exit 1 on a failure)
const { chromium } = require('playwright'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_fit'; fs.mkdirSync(out, { recursive: true }); let ok = true; const say = (n, v) => { console.log((v ? 'ok  ' : 'FAIL') + ' ' + n); if (!v) ok = false; };
  const b = await chromium.launch(), errs = [];
  for (const [w, h] of [[844, 390], [844, 340], [800, 330], [740, 300], [667, 320], [640, 280]]) {
    const pg = await (await b.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true })).newPage(); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://localhost:8000/bag3d.html?mute=1&t=' + Date.now()); await pg.waitForTimeout(1500); await pg.evaluate(() => localStorage.clear()); await pg.reload(); await pg.waitForTimeout(1800);
    const s = await pg.evaluate(() => { const r = document.getElementById('start').getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2, top = document.elementFromPoint(x, y);
      return { top: Math.round(r.top), bottom: Math.round(r.bottom), hit: !!top && (top.id === 'start' || !!top.closest('#start')), zoom: document.getElementById('homeIn').style.zoom || '1' }; });
    await pg.screenshot({ path: `${out}/home_${w}x${h}.png` });
    say(`${w}x${h} start screen: start button ${s.top}-${s.bottom} px of ${h}, tappable ${s.hit} (scaled x${s.zoom})`, s.top >= 0 && s.bottom <= h && s.hit);
    await pg.tap('#start'); await pg.waitForTimeout(700);
    const r = await pg.evaluate(() => { const o = []; for (const id of ['rr', 'rot', 'sell', 'fs', 'bk', 'go']) { const e = document.getElementById(id); if (!e || getComputedStyle(e).display === 'none') continue; const q = e.getBoundingClientRect(); if (!(q.bottom <= innerHeight + .5 && q.right <= innerWidth + .5 && q.top >= 0)) o.push(id); } return { home: getComputedStyle(document.getElementById('home')).display, cut: o }; });
    await pg.screenshot({ path: `${out}/shop_${w}x${h}.png` });
    say(`${w}x${h} after start: the shop is open, buttons outside the screen: ${r.cut.join(',') || 'none'}`, r.home === 'none' && !r.cut.length); await pg.close();
  }
  { const pg = await (await b.newContext({ viewport: { width: 800, height: 330 }, hasTouch: true })).newPage(); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://localhost:8000/bag3d.html?mute=1&t=' + Date.now()); await pg.waitForTimeout(1500);
    await pg.tap('#hfs'); await pg.waitForTimeout(400); const on = await pg.evaluate(() => !!document.fullscreenElement); await pg.tap('#hfs'); await pg.waitForTimeout(400); const off = await pg.evaluate(() => !document.fullscreenElement);
    await pg.tap('#start'); await pg.waitForTimeout(600); const st = await pg.evaluate(() => !!document.fullscreenElement);
    say(`the fullscreen button turns it on ${on} and off ${off}; tapping start goes full screen ${st}`, on && off && st);
    const m = await pg.evaluate(async () => { const r = await fetch(document.querySelector('link[rel=manifest]').href), m = await r.json(); return { d: m.display, o: m.orientation, s: m.start_url, ic: (await fetch(m.icons[0].src)).status }; });
    say(`home-screen app: ${m.d} ${m.o} ${m.s}, icon ${m.ic}`, m.d === 'fullscreen' && m.o === 'landscape' && m.s === 'bag3d.html' && m.ic === 200); await pg.close(); }
  say('no errors on the page', !errs.length); if (errs.length) console.log([...new Set(errs)].slice(0, 5).join('\n'));
  console.log(ok ? 'FIT OK' : 'FIT FAIL'); await b.close(); process.exit(ok ? 0 : 1);
})();
