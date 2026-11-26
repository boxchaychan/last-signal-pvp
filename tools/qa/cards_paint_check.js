// cards.html painted cards (Lu Bu legendary): hand, summon splash, board, zoom, attack. ?skip=1 starts at turn 1.
// python3 -m http.server 8000 ; node tools/qa/cards_paint_check.js [out=/tmp/cards_paint] [device scale 2]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/cards_paint', dsf = +(process.argv[3] || 2); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf }); const errs = [];
  const pg = await ctx.newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/cards.html?skip=1'); await pg.waitForTimeout(1800);
  await pg.evaluate(() => { const S = CG.S, P = S.p[0], E = S.p[1]; P.maxMana = P.mana = 10; P.hand.unshift(CG.mkCard('lubuC', 0));
    for (const k of ['mummy', 'cactus', 'wolf']) { const c = CG.mkCard(k, 1); c.sleep = false; E.board.push(c); } });
  await pg.waitForTimeout(900); await pg.screenshot({ path: out + '/1_hand.png' });
  await pg.evaluate(() => { const S = CG.S; CG.ZOOM(S.p[0].hand[0]); }); await pg.waitForTimeout(400); await pg.screenshot({ path: out + '/2_zoom_hand.png' });
  await pg.evaluate(() => { CG.ZOOM(null); const S = CG.S; CG.play(S.p[0], S.p[0].hand[0], null); });
  await pg.waitForTimeout(450); await pg.screenshot({ path: out + '/3_splash.png' });
  await pg.waitForTimeout(700); await pg.screenshot({ path: out + '/4_splash_out_sweep.png' });
  await pg.waitForTimeout(1500); await pg.screenshot({ path: out + '/5_board.png' });
  const st = await pg.evaluate(() => { const S = CG.S; return { mine: S.p[0].board.map(c => c.k + ' ' + c.a + '/' + c.h), foe: S.p[1].board.map(c => c.k + ' ' + c.a + '/' + c.h), busy: S.busy }; }); console.log(JSON.stringify(st));
  await pg.evaluate(() => { const S = CG.S, c = S.p[0].board.find(c => c.k === 'lubuC'); const t = S.p[1].board.find(x => CG.legalTarget(c, x)) || 'leader'; console.log('atk', CG.attack(c, t)); });
  await pg.waitForTimeout(330); await pg.screenshot({ path: out + '/6_attack.png' }); await pg.waitForTimeout(1500);
  await pg.evaluate(() => { const S = CG.S; CG.ZOOM(S.p[0].board.find(c => c.k === 'lubuC')); }); await pg.waitForTimeout(400); await pg.screenshot({ path: out + '/7_zoom_board.png' });
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
