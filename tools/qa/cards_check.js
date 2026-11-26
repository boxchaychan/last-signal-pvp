// cards.html "ศึกการ์ดอสูร": title shot + a bot-vs-bot game (?bot=1) with shots along the way + page errors + who won.
// python3 -m http.server 8000 ; node tools/qa/cards_check.js [out=/tmp/cards] [seconds 120] [device scale 2]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/cards', secs = +(process.argv[3] || 120), dsf = +(process.argv[4] || 2); require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf }); const errs = [];
  let pg = await ctx.newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/cards.html'); await pg.waitForTimeout(1500); await pg.screenshot({ path: out + '/title.png' });
  pg = await ctx.newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/cards.html?bot=1'); let n = 0;
  for (let t = 0; t < secs; t += 4) { await pg.waitForTimeout(4000); const st = await pg.evaluate(() => { const S = CG.S; return { turn: S.turnN, cur: S.cur, hp: S.p.map(p => p.hp), board: S.p.map(p => p.board.length), hand: S.p.map(p => p.hand.length), fury: S.p.map(p => p.fury), phase: S.phase, win: S.winner }; });
    if (t % 12 === 0) { await pg.screenshot({ path: `${out}/game_${String(n++).padStart(2, '0')}.png` }); console.log(JSON.stringify(st)); }
    if (st.phase === 'over') { await pg.screenshot({ path: `${out}/over.png` }); console.log('OVER', JSON.stringify(st)); break; } }
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
