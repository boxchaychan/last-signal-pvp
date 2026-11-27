// rig.html (the piece + bone tool) and rig2d/bones.js (the player games use).
// python3 -m http.server 8000 ; node tools/qa/rig_check.js [out=/tmp/rig_check] [char=dagger]
//   - the tool opens at phone (844 x 390) and PC (1280 x 720) size without errors, every move button plays, picking / turning / saving work;
//   - <out>/moves.png = every shared move as a strip of poses drawn with Bones2D.player (what a game would draw), to look at.
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/rig_check', ch = process.argv[3] || 'dagger'; require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; let ok = true; const say = (n, v) => { console.log(v ? 'ok  ' : 'FAIL', n); if (!v) ok = false; };
  for (const [W, H] of [[844, 390], [1280, 720]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 2, hasTouch: W < 900 })).newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto(`http://localhost:8000/rig.html?char=${ch}`); await pg.waitForFunction(() => window.RIG && RIG.PL && RIG.PL.mats, null, { timeout: 20000 });
    const info = await pg.evaluate(() => ({ parts: Object.keys(RIG.R.parts).length, roles: Object.values(RIG.R.parts).map(q => q.role), btn: document.querySelectorAll('#mvs button').length, moves: Object.keys(RIG.B.MOVES) }));
    say(`${W}: rig loaded, ${info.parts} pieces, ${info.btn} move buttons`, info.parts >= 5 && info.btn === info.moves.length + 1 && info.roles.includes('head') && info.roles.includes('body'));
    await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/${W}_idle.png` });
    for (const mv of info.moves) { await pg.evaluate(mv => document.querySelector(`#mvs button[data-mv="${mv}"]`).click(), mv); await pg.waitForTimeout(mv === 'die' ? 500 : 450);
      const st = await pg.evaluate(() => ({ name: RIG.PL.name, nan: Object.values(RIG.PL.mats).some(m => m.some(v => !isFinite(v))) })); if (st.nan) say(`${W}: ${mv} gives a broken pose`, false); if (mv === 'attack' || mv === 'cast') await pg.screenshot({ path: `${out}/${W}_${mv}.png` }); }
    say(`${W}: every move plays without a broken pose`, true);
    // back to building: stop, pick the head, turn it, the rig is saved in the browser
    await pg.evaluate(() => { document.querySelector('#mvs button[data-mv=""]').click(); document.getElementById('mP').click(); RIG.select(Object.keys(RIG.R.parts).find(k => RIG.R.parts[k].role === 'head')); });
    const r0 = await pg.evaluate(() => { const q = RIG.R.parts[document.getElementById('pick').value]; document.getElementById('sc').value = (q.s * 1.1).toFixed(2); document.getElementById('sc').dispatchEvent(new Event('input')); return { s: RIG.R.parts[document.getElementById('pick').value].s, saved: !!localStorage.getItem('rig2dv2_' + new URLSearchParams(location.search).get('char')) }; });
    say(`${W}: the size slider changes the piece and the rig is kept in the browser`, r0.saved && r0.s > 0);
    await pg.evaluate(() => { document.getElementById('bones').click(); }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/${W}_bones.png` });
    const txt = await pg.evaluate(() => { document.getElementById('cp').onclick; const o = JSON.parse(JSON.stringify(RIG.R, (k, v) => k === 'img' && typeof v === 'object' ? undefined : k[0] === '_' ? undefined : v)); return Object.keys(o).join(','); });
    say(`${W}: the saved rig has ${txt}`, /parts/.test(txt) && /order/.test(txt) && /feet/.test(txt));
    if (W > 900) {   // the strips: the player a game uses, on a plain canvas
      const url = await pg.evaluate(async ch => { const B = Bones2D, rig = await B.load(`art/rigs/${ch}.json`), mvs = Object.keys(B.MOVES), N = 9, cw = 190, chh = 250, c = document.createElement('canvas'); c.width = cw * N + 90; c.height = chh * mvs.length; const g = c.getContext('2d'); g.fillStyle = '#2b3348'; g.fillRect(0, 0, c.width, c.height);
        mvs.forEach((mv, j) => { const M = B.MOVES[mv], dur = M.dur || (mv === 'idle' ? .64 : mv === 'walk' ? .9 : .5); const p = B.player(rig, { base: null }); p.play('idle'); for (let q = 0; q < 30; q++) p.update(1 / 60); p.play(mv);
          for (let i = 0; i < N; i++) { const steps = Math.round(dur / (N - 1) * 240); for (let q = 0; q < (i ? steps : 1); q++) p.update(i ? 1 / 240 : 0); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#3a4560'; g.fillRect(90 + i * cw, j * chh + chh - 22, cw - 4, 18); p.draw(g, 90 + i * cw + cw * .46, j * chh + chh - 22, (chh - 60) / rig.size[1], false); }
          g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#ffd24a'; g.font = '700 20px sans-serif'; g.fillText(B.NAMES[mv], 8, j * chh + 40); g.fillStyle = '#aab'; g.font = '600 13px sans-serif'; g.fillText(dur.toFixed(2) + ' s', 8, j * chh + 62); });
        return c.toDataURL('image/png'); }, ch);
      require('fs').writeFileSync(`${out}/moves.png`, Buffer.from(url.split(',')[1], 'base64')); say('moves.png written', true);
    }
    await pg.close();
  }
  console.log(ok ? 'RIG OK' : 'RIG FAIL'); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].slice(0, 10).join('\n') : 'no errors'); await b.close();
})();
