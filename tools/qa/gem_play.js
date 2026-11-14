// Plays gem.html (ศึกอัญมณี) like a person: real clicks and drags on the canvas, real time. The page lists its buttons in GM.ui().
//   python3 -m http.server 8000        (repo root, in another shell)
//   node tools/qa/gem_play.js [folder for screenshots]
// Covers: title -> lobby -> map -> briefing -> first-time how-to -> drag swap, tap-tap swap, wrong swap, target, ultimate, pause, quit,
// a whole stage by clicks, result screen, upgrade bought from it, next stage, save kept after a reload.
const {chromium} = require('playwright');
const out = process.argv[2] || '';
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}, deviceScaleFactor: 2}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + '\n' + (e.stack || '').split('\n').slice(0, 5).join('\n'))); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); }); pg.on('requestfailed', r => errs.push('fail ' + r.url())); pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  const shot = async n => { if (out) await pg.screenshot({path: `${out}/${n}.png`}); };
  const idle = () => pg.waitForFunction(() => !GM.fade, null, {timeout: 8000});
  const click = async (id, wait) => { await idle(); await pg.waitForFunction(i => GM.ui().some(b2 => b2.id === i), id, {timeout: 8000}); const p = await pg.evaluate(i => { const L = GM.ui(); for (let k = L.length - 1; k >= 0; k--) if (L[k].id === i) return L[k]; }, id); await pg.mouse.click(p.x, p.y); await pg.waitForTimeout(wait || 250); };
  const D = 2, cellXY = (c, r, L) => [(L.BX + (c + .5) * L.cell) / D, (L.BY + (r + .5) * L.cell) / D];
  try {
  await pg.goto('http://localhost:8000/gem.html'); await pg.waitForFunction(() => window.GM && GM.ready, null, {timeout: 20000}); await pg.waitForTimeout(500); log.push('start screen: ' + await pg.evaluate(() => GM.scr)); await shot('p01_title');
  await pg.mouse.click(420, 200); await pg.waitForFunction(() => GM.scr === 'lobby' && !GM.fade, null, {timeout: 8000}); await pg.waitForTimeout(300); await shot('p02_lobby');
  await click('play'); await pg.waitForFunction(() => GM.scr === 'map' && !GM.fade); await pg.waitForTimeout(500); await shot('p03_map');
  await click('st1'); await pg.waitForTimeout(400); log.push('locked stage tap -> dialog ' + await pg.evaluate(() => GM.dlg));
  await click('st0'); log.push('stage tap -> dialog ' + await pg.evaluate(() => GM.dlg)); await pg.waitForTimeout(300); await shot('p04_prep');
  await click('fight'); await pg.waitForFunction(() => GM.scr === 'battle' && !GM.fade); await pg.waitForTimeout(400); log.push('first battle opens the how-to: ' + await pg.evaluate(() => GM.dlg)); await shot('p05_help');
  await click('hnext'); await click('hnext'); await click('hnext'); log.push('how-to closed: ' + await pg.evaluate(() => GM.dlg === null));
  await pg.waitForFunction(() => GM.phase === 'idle', null, {timeout: 8000}); await pg.waitForTimeout(1500); await shot('p06_hint');
  let mv = await pg.evaluate(() => { const m = GM.botMove(); return {a: [m.a.c, m.a.r], b: [m.b.c, m.b.r], L: GM.lay, moves: GM.B.moves}; });
  let [x0, y0] = cellXY(mv.a[0], mv.a[1], mv.L), [x1, y1] = cellXY(mv.b[0], mv.b[1], mv.L);
  await pg.mouse.move(x0, y0); await pg.mouse.down(); await pg.mouse.move((x0 + x1) / 2, (y0 + y1) / 2, {steps: 3}); await pg.mouse.move(x1, y1, {steps: 3}); await pg.mouse.up(); await pg.waitForTimeout(250);
  log.push('drag -> phase ' + await pg.evaluate(() => GM.phase) + ', moves ' + await pg.evaluate(() => GM.B.moves)); await shot('p07_clear');
  await pg.waitForFunction(() => GM.phase === 'idle' || GM.B.over, null, {timeout: 15000}); await pg.waitForTimeout(200);
  mv = await pg.evaluate(() => { const m = GM.botMove(); return {a: [m.a.c, m.a.r], b: [m.b.c, m.b.r], L: GM.lay, moves: GM.B.moves}; }); [x0, y0] = cellXY(mv.a[0], mv.a[1], mv.L); [x1, y1] = cellXY(mv.b[0], mv.b[1], mv.L);
  await pg.mouse.click(x0, y0); await pg.waitForTimeout(120); await pg.mouse.click(x1, y1); await pg.waitForTimeout(250); log.push('tap-tap -> moves ' + await pg.evaluate(() => GM.B.moves) + ' (was ' + mv.moves + ')');
  await pg.waitForFunction(() => GM.phase === 'idle' || GM.B.over, null, {timeout: 15000});
  const inv = await pg.evaluate(() => { const ok = GM.findMoves(); for (let r = 0; r < 7; r++) for (let c = 0; c < 6; c++) { const a = GM.gemAt(c, r), b2 = GM.gemAt(c + 1, r); if (a.t !== b2.t && a.t < 6 && b2.t < 6 && !a.sp && !b2.sp && !a.lock && !b2.lock && !ok.some(m => (m.a === a && m.b === b2) || (m.a === b2 && m.b === a))) return {a: [c, r], b: [c + 1, r], L: GM.lay, moves: GM.B.moves, ta: a.t, tb: b2.t}; } return null; });
  if (inv) { [x0, y0] = cellXY(inv.a[0], inv.a[1], inv.L); [x1, y1] = cellXY(inv.b[0], inv.b[1], inv.L); await pg.mouse.move(x0, y0); await pg.mouse.down(); await pg.mouse.move(x1, y1, {steps: 4}); await pg.mouse.up(); await pg.waitForTimeout(600);
    log.push('wrong swap -> moves ' + await pg.evaluate(() => GM.B.moves) + ' (was ' + inv.moves + '), phase ' + await pg.evaluate(() => GM.phase) + ', gems back: ' + await pg.evaluate(v => GM.gemAt(v.a[0], v.a[1]).t === v.ta && GM.gemAt(v.b[0], v.b[1]).t === v.tb, inv)); }
  const tg = await pg.evaluate(() => { const f = GM.B.foes.filter(f => f.hp > 0); const t = f[f.length - 1], L = GM.lay; return {x: (t.x * L.K) / 2, y: ((t.y - t.m[1] * .4) * L.K) / 2, n: f.length}; });
  await pg.mouse.click(tg.x, tg.y); await pg.waitForTimeout(100); log.push('target tap (' + tg.n + ' alive) -> ' + await pg.evaluate(() => GM.B.tg ? GM.B.tg.k + ', is the last one: ' + (GM.B.tg === GM.B.foes.filter(f => f.hp > 0).pop()) : 'none'));
  await pg.evaluate(() => { GM.HR[1].ult = 100; }); await pg.waitForTimeout(300); const ub = await pg.evaluate(() => GM.lay.HUD.ult[1]); await shot('p08_ready');
  await pg.mouse.click(ub.x / 2, ub.y / 2); await pg.waitForTimeout(150); log.push('ultimate tap -> phase ' + await pg.evaluate(() => GM.phase + ', ring ' + GM.HR[1].ult)); await pg.waitForTimeout(700); await shot('p09_ult');
  await pg.waitForFunction(() => GM.phase === 'idle' || GM.B.over, null, {timeout: 15000});
  await click('pause'); const t0 = await pg.evaluate(() => GM.T); await pg.waitForTimeout(400); log.push('paused: dialog ' + await pg.evaluate(() => GM.dlg) + ', time stands still ' + (await pg.evaluate(() => GM.T) === t0)); await shot('p10_pause'); await click('resume');
  await click('pause'); await click('quit'); await pg.waitForFunction(() => GM.scr === 'map' && !GM.fade); log.push('quit -> ' + await pg.evaluate(() => GM.scr));
  await click('st0'); await click('fight'); await pg.waitForFunction(() => GM.scr === 'battle' && !GM.fade && GM.phase === 'idle', null, {timeout: 10000}); let n = 0; const tw0 = Date.now();
  while (Date.now() - tw0 < 150000) { const st = await pg.evaluate(() => GM.B ? GM.B.over : 9); if (st) break; if (await pg.evaluate(() => GM.phase) !== 'idle') { await pg.waitForTimeout(120); continue; }
    const m = await pg.evaluate(() => { for (let i = 0; i < 3; i++) if (GM.HR[i].ult >= 100) return {u: GM.lay.HUD.ult[i]}; const m = GM.botMove(); return m ? {a: [m.a.c, m.a.r], b: [m.b.c, m.b.r], L: GM.lay} : null; }); if (!m) { await pg.waitForTimeout(200); continue; }
    if (m.u) { await pg.mouse.click(m.u.x / 2, m.u.y / 2); await pg.waitForTimeout(200); continue; }
    [x0, y0] = cellXY(m.a[0], m.a[1], m.L); [x1, y1] = cellXY(m.b[0], m.b[1], m.L); await pg.mouse.move(x0, y0); await pg.mouse.down(); await pg.mouse.move(x1, y1, {steps: 2}); await pg.mouse.up(); n++; await pg.waitForTimeout(150); }
  await pg.waitForFunction(() => GM.dlg === 'res', null, {timeout: 20000}); await pg.waitForTimeout(700); await shot('p11_res_a'); await pg.waitForTimeout(2600); await shot('p12_res_b');
  log.push('stage played by ' + n + ' drags -> won ' + await pg.evaluate(() => GM.B.over === 1) + ' | save ' + await pg.evaluate(() => localStorage.getItem('ls_gem1')));
  await click('rupg'); await pg.waitForTimeout(300); await shot('p13_upg'); const g0 = await pg.evaluate(() => GM.S.gold); await click('buy0'); log.push('upgrade from the result screen: gold ' + g0 + ' -> ' + await pg.evaluate(() => GM.S.gold + ', levels ' + GM.S.up)); await shot('p14_upg2');
  await click('x'); log.push('upgrade closed -> dialog ' + await pg.evaluate(() => GM.dlg)); await click('rnext'); await pg.waitForFunction(() => GM.scr === 'battle' && GM.B && GM.B.st === 1 && !GM.fade, null, {timeout: 10000}); log.push('next stage: ' + await pg.evaluate(() => (GM.B.ch + 1) + '-' + (GM.B.st + 1)));
  await pg.reload(); await pg.waitForFunction(() => window.GM && GM.ready, null, {timeout: 20000}); log.push('after reload: screen ' + await pg.evaluate(() => GM.scr + ', Lv ' + GM.S.lv + ' gold ' + GM.S.gold + ' stars ' + JSON.stringify(GM.S.st)));
  } catch (e) { errs.push('SCRIPT ' + e.message.split('\n')[0] + ' | state ' + JSON.stringify(await pg.evaluate(() => ({scr: GM.scr, dlg: GM.dlg, phase: GM.phase, fade: GM.fade, ui: GM.ui().map(b2 => b2.id)})).catch(() => null))); }
  console.log(log.join('\n')); console.log('errors', JSON.stringify(errs, null, 1)); await b.close(); process.exit(errs.length ? 1 : 0); })();
