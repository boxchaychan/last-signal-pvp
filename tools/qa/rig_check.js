// rig.html (the piece + bone tool) and rig2d/bones.js (the player games use).
// python3 -m http.server 8000 ; node tools/qa/rig_check.js [out=/tmp/rig_check] [char=dagger]
//   - the tool opens at phone (844 x 390) and PC (1280 x 720) size without errors, every move button plays, picking / turning / saving work;
//   - <out>/moves.png = every shared move as a strip of poses drawn with Bones2D.player (what a game would draw), to look at.
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/rig_check', ch = process.argv[3] || 'zeus'; require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; let ok = true; const say = (n, v) => { console.log(v ? 'ok  ' : 'FAIL', n); if (!v) ok = false; };
  for (const [W, H] of [[844, 390], [1280, 720]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 2, hasTouch: W < 900 })).newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto(`http://localhost:8000/rig.html?char=${ch}`); await pg.waitForFunction(() => window.RIG && RIG.PL && RIG.PL.mats, null, { timeout: 20000 });
    const info = await pg.evaluate(() => ({ parts: Object.keys(RIG.R.parts).length, roles: Object.values(RIG.R.parts).map(q => q.role), btn: document.querySelectorAll('#mvs button').length, moves: Object.keys(RIG.B.MOVES) }));
    say(`${W}: rig loaded, ${info.parts} pieces, ${info.btn} move buttons`, info.parts >= 5 && info.btn >= info.moves.length - 1 && info.roles.includes('head') && info.roles.includes('body'));
    await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/${W}_idle.png` });
    for (const mv of info.moves) { if (!await pg.evaluate(mv => { const b = document.querySelector(`#mvs button[data-mv="${mv}"]`); if (b) b.click(); return !!b; }, mv)) continue; await pg.waitForTimeout(mv === 'die' ? 500 : 450);
      const st = await pg.evaluate(() => ({ name: RIG.PL.name, nan: Object.values(RIG.PL.mats).some(m => m.some(v => !isFinite(v))) })); if (st.nan) say(`${W}: ${mv} gives a broken pose`, false); if (mv === 'attack' || mv === 'cast') await pg.screenshot({ path: `${out}/${W}_${mv}.png` }); }
    say(`${W}: every move plays without a broken pose`, true);
    // back to building: stop, pick the head, turn it, the rig is saved in the browser
    await pg.evaluate(() => { document.querySelector('#mvs button[data-mv=""]').click(); document.getElementById('mP').click(); RIG.select(Object.keys(RIG.R.parts).find(k => RIG.R.parts[k].role === 'head')); });
    const r0 = await pg.evaluate(() => { const q = RIG.R.parts[document.getElementById('pick').value]; document.getElementById('sc').value = (q.s * 1.1).toFixed(2); document.getElementById('sc').dispatchEvent(new Event('input')); return { s: RIG.R.parts[document.getElementById('pick').value].s, saved: !!localStorage.getItem('rig2dv2_' + new URLSearchParams(location.search).get('char')) }; });
    say(`${W}: the size slider changes the piece and the rig is kept in the browser`, r0.saved && r0.s > 0);
    await pg.evaluate(() => { document.getElementById('bones').click(); }); await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/${W}_bones.png` });
    const txt = await pg.evaluate(() => { document.getElementById('cp').onclick; const o = JSON.parse(JSON.stringify(RIG.R, (k, v) => k === 'img' && typeof v === 'object' ? undefined : k[0] === '_' ? undefined : v)); return Object.keys(o).join(','); });
    say(`${W}: the saved rig has ${txt}`, /parts/.test(txt) && /order/.test(txt) && /feet/.test(txt));
    if (W > 900) {   // the shooting move against the owner's recording (the gunner's head, measured 2026-11-27): size % and tilt at the same moments
      const CLIP = [[.025, 140, 16], [.055, 132, 24], [.085, 116, 32], [.125, 108, 44], [.155, 100, 36], [.185, 100, 20], [.225, 108, 0], [.255, 100, 0]];
      const got = await pg.evaluate(async ([ch, CLIP]) => { const B = Bones2D, rig = await B.load(`art/rigs/${ch}.json`), hk = Object.keys(rig.parts).find(k => rig.parts[k].role === 'head'), m0 = B.world(rig, {}, null)[hk], out = [];
        for (const [t] of CLIP) { const p = B.player(rig, { base: null }); p.play('shoot'); for (let q = 0; q < Math.round(t * 1000); q++) p.update(.001); const m = p.mats[hk]; out.push([Math.round(Math.hypot(m[0], m[1]) / Math.hypot(m0[0], m0[1]) * 100), Math.round(Math.abs((((Math.atan2(m[1], m[0]) - Math.atan2(m0[1], m0[0])) * 180 / Math.PI + 540) % 360) - 180))]); } return out; }, [ch, CLIP]);
      const worst = CLIP.reduce((w, c, i) => [Math.max(w[0], Math.abs(got[i][0] - c[1])), Math.max(w[1], Math.abs(got[i][1] - c[2]))], [0, 0]);
      console.log('     recording  ' + CLIP.map(c => c[1] + '%/' + c[2]).join('  ') + '\n     this rig   ' + got.map(g => g[0] + '%/' + g[1]).join('  ')); say(`shoot follows the recording: head size within ${worst[0]} points, tilt within ${worst[1]} degrees`, worst[0] <= 6 && worst[1] <= 6);
      const feet = await pg.evaluate(async ch => { const B = Bones2D, rig = await B.load(`art/rigs/${ch}.json`), legs = Object.keys(rig.parts).filter(k => /^(leg|shin)/.test(rig.parts[k].role) && !Object.values(rig.parts).some(q => q.p === k)), p = B.player(rig, { base: null }); let far = 0, top = [1e9, -1e9]; const hk = Object.keys(rig.parts).find(k => rig.parts[k].role === 'head');
        const foot = (M, k) => { const im = rig.img[k], q = rig.parts[k]; return B.pt(M[k], im.width / 2 - q.pv[0], im.height - q.pv[1]); }, M0 = B.world(rig, {}, null);
        p.play('shoot'); for (let i = 0; i < 100; i++) { p.update(.004); for (const k of legs) { const a = foot(p.mats, k), b = foot(M0, k); far = Math.max(far, Math.hypot(a[0] - b[0], a[1] - b[1])); } }
        const q = B.player(rig, { base: null }); q.play('idle'); for (let i = 0; i < 160; i++) { q.update(.008); const im = rig.img[hk], y = B.pt(q.mats[hk], im.width / 2 - rig.parts[hk].pv[0], -rig.parts[hk].pv[1])[1]; top = [Math.min(top[0], y), Math.max(top[1], y)]; }
        return { far: far / rig.size[1] * 100, bob: (top[1] - top[0]) / rig.size[1] * 100 }; }, ch);
      say(`feet stay planted while shooting (they move ${feet.far.toFixed(1)} % of the height)`, feet.far < 6); say(`standing: the head top travels ${feet.bob.toFixed(1)} % of the height (recording about 8 %)`, feet.bob > 4 && feet.bob < 11);
      // the strips: the player a game uses, on a plain canvas
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
