/* Checks for clash.html "ศึกหกเผ่า" battle test (needs: python3 -m http.server 8000 in the repo).
   node tools/qa/clash_check.js look <outPrefix> [w h]   -> pictures before / during / after a battle + console errors + frame rate
   node tools/qa/clash_check.js bal [n]                  -> n headless battles (?norender=1): wins left / right, seconds */
const { chromium, devices } = require('playwright');
const MODE = process.argv[2] || 'look', ARG = process.argv[3] || 'clash';
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const W = +process.argv[4] || 0, H = +process.argv[5] || 0;
  const ctx = await b.newContext(W ? { viewport: { width: W, height: H }, deviceScaleFactor: 1 } : { ...devices['iPhone 13 landscape'] });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push('ERR ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });
  const ready = async () => { for (let i = 0; i < 60; i++) { await p.waitForTimeout(500); if (await p.evaluate(() => window.CLASH && CLASH.ready).catch(() => 0)) return; } throw new Error('no load ' + errs.join(' | ')); };
  if (MODE === 'bal') { await p.goto('http://localhost:8000/clash.html?norender=1'); await ready(); console.log(JSON.stringify(await p.evaluate(n => CLASH.quick(n), +ARG || 20))); }
  else {
    await p.goto('http://localhost:8000/clash.html'); await ready(); await p.waitForTimeout(1500);
    await p.screenshot({ path: `${ARG}_1deploy.png` });
    await p.click('#go'); await p.waitForTimeout(4500); await p.screenshot({ path: `${ARG}_2clash.png` });
    const fps = await p.evaluate(() => new Promise(r => { let n = 0; const t0 = performance.now(); const f = () => { n++; if (performance.now() - t0 < 2000) requestAnimationFrame(f); else r(Math.round(n / 2)); }; requestAnimationFrame(f); }));
    await p.waitForTimeout(3000); await p.screenshot({ path: `${ARG}_3fight.png` });
    for (let i = 0; i < 160; i++) { await p.waitForTimeout(1000); if (await p.evaluate(() => CLASH.B.phase === 'over')) break; }
    await p.waitForTimeout(1800); await p.screenshot({ path: `${ARG}_4end.png` });
    console.log(JSON.stringify(await p.evaluate(() => ({ phase: CLASH.B.phase, win: CLASH.B.win, t: Math.round(CLASH.B.t), PIX: CLASH.PIX, left: CLASH.B.units.filter(u => !u.dead && !u.side).length, right: CLASH.B.units.filter(u => !u.dead && u.side).length }))), 'fps', fps);
  }
  console.log(errs.length ? errs.join('\n') : 'no errors'); await b.close();
})();
