// Balance check for gem.html (ศึกอัญมณี): an auto-player plays the whole campaign 1-1 .. 6-5 with the page's own code
// (rewards, greedy upgrades; 4 losses in a row = replay the stage before for gold and XP) and prints tries / moves / HP left per stage.
//   python3 -m http.server 8000        (repo root, in another shell)
//   node tools/qa/gem_balance.js [seed] [skill 0..1, default .85] ['{"matk":1.8}' = overrides of the BAL table in gem.html]
// Target (2026-11-13): chapter 1 at the first try, later chapters 1-3 tries, the whole campaign about 55-65 runs.
const {chromium} = require('playwright');
const seed = process.argv[2] || 5, skill = +(process.argv[3] || .85), bal = process.argv[4] || '{}';
(async () => { const b = await chromium.launch(); const errs = [];
  const pg = await b.newPage({viewport: {width: 844, height: 390}, deviceScaleFactor: 1});
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + '\n' + (e.stack || '').split('\n').slice(0, 6).join('\n'))); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  await pg.goto('http://localhost:8000/gem.html?new=1&seed=' + seed); await pg.waitForFunction(() => window.GM && document.getElementById('home').classList.contains('show'), null, {timeout: 15000});
  const res = await pg.evaluate(([skill, bal]) => { GM.hold = true; Object.assign(GM.BAL, JSON.parse(bal)); const log = []; let g = 0, runs = 0, tries = 0, grind = 0, stuck = '';
    const shop = () => { for (let k = 0; k < 80; k++) { let best = 0, bc = 1e9; for (let t = 0; t < 6; t++) { const c = GM.upCost(t) * (t === 5 ? 1.3 : 1); if (c < bc) { bc = c; best = t; } } if (GM.S.gold >= GM.upCost(best)) { GM.S.gold -= GM.upCost(best); GM.S.up[best]++; } else break; } };
    while (g < 30 && runs < 260) { runs++; let gg = g; if (tries >= 4 && g > 0) { gg = g - 1; grind++; }      // 4 losses in a row: go back one stage for gold and XP, then try again
      const r = GM.simStage(gg / 5 | 0, gg % 5, skill); GM.grant(r.win); shop(); if (r.guard >= 60000) { stuck = 'STUCK at ' + gg + ' phase ' + GM.phase; break; }
      if (gg !== g) { tries = 2; continue; }
      if (r.win) { log.push(((g / 5 | 0) + 1) + '-' + (g % 5 + 1) + '  tries ' + (tries + 1) + '  moves ' + String(r.moves).padStart(3) + '  hp ' + String(r.hp).padStart(3) + '%  took ' + String(r.taken).padStart(3) + '%+' + String(r.blocked).padStart(3) + '%  Lv ' + String(GM.S.lv).padStart(2) + '  up ' + GM.S.up.join(',') + '  gold ' + GM.S.gold); g++; tries = 0; } else tries++; }
    return {log, runs, grind, stuck, g}; }, [skill, bal]);
  console.log(res.log.join('\n')); console.log('runs', res.runs, 'grind runs', res.grind, 'reached', res.g, res.stuck); if (errs.length) console.log('errors', JSON.stringify(errs, null, 1)); await b.close(); })();
