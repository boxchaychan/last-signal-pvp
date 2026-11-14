// Fuzz test for gem.html (ศึกอัญมณี): 36 stages of random moves with special gems, prisms, locks and rocks thrown onto the board and
// ultimates fired at random, sound on; fails loudly on a page error or a stage that never ends.
//   python3 -m http.server 8000        (repo root, in another shell)
//   node tools/qa/gem_fuzz.js [seed]
const {chromium} = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
  const pg = await b.newPage({viewport: {width: 844, height: 390}, deviceScaleFactor: 1});
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + '\n' + (e.stack || '').split('\n').slice(0, 6).join('\n'))); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  await pg.goto('http://localhost:8000/gem.html?new=1&seed=' + (process.argv[2] || 77)); await pg.waitForFunction(() => window.GM && GM.ready, null, {timeout: 20000});
  await pg.mouse.click(5, 380);   // a real click (title -> lobby) so the audio context starts: sound code runs in this test
  await pg.waitForFunction(() => GM.scr === 'lobby' && !GM.fade, null, {timeout: 8000});
  const res = await pg.evaluate(() => { GM.hold = true; GM.S.snd = 1; GM.S.mus = 1; const out = []; let R = 12345; const rnd = () => { R = (R * 1103515245 + 12345) & 0x7fffffff; return R / 0x7fffffff; };
    for (let run = 0; run < 36; run++) { const g = run % 30; GM.S.lv = 1 + g; GM.S.up = [g >> 1, g >> 1, g >> 1, g >> 1, g >> 1, g >> 1]; GM.startStage(g / 5 | 0, g % 5); let guard = 0, idleN = 0, last = '';
      while (!GM.B.over && guard++ < 40000) { if (GM.phase === 'idle') { idleN++;
          const gr = GM.grid, pick = () => gr[rnd() * 7 | 0][rnd() * 7 | 0];
          if (rnd() < .35) { const x = pick(); if (x && x.t < 6) x.sp = 1 + (rnd() * 3 | 0); } if (rnd() < .12) { const x = pick(); if (x && x.t < 6) { x.t = 6; x.sp = 0; x.lock = 0; } } if (rnd() < .1) { const x = pick(); if (x && x.t < 6) x.lock = 1; } if (rnd() < .06) { const x = pick(); if (x && x.t < 6 && !x.sp) { x.t = 7; } }
          if (rnd() < .2) GM.B.hp = GM.B.hpMax;                                  // keep the fight going
          for (let i = 0; i < 3; i++) if (rnd() < .5) { GM.HR[i].ult = 100; GM.castUlt(i); }
          if (GM.phase === 'idle') { const M = GM.findMoves(); if (M.length) { const m = M[rnd() * M.length | 0]; GM.trySwap(m.a, m.b); } else { last = 'no moves in idle'; break; } } }
        GM.step(.04); if (guard % 3 === 0) GM.draw(); }
      out.push(g + ':' + (GM.B.over === 1 ? 'W' : GM.B.over === -1 ? 'L' : 'STUCK ' + GM.phase + ' ' + JSON.stringify(GM.counts) + last) + '/' + idleN); for (let i = 0; i < 70; i++) GM.step(.04); GM.draw(); }
    return out.join(' '); });
  console.log(res); console.log('errors', JSON.stringify(errs.slice(0, 6), null, 1), errs.length); await b.close(); })();
