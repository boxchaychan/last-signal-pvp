// Tangled-arm check for front-view rigs (owner 2026-11-28 "แขนยังพันกันอยู่เลย"): plays every move as a game would (rig2d/bones.js player) and, 30 times a
// second, tests (1) do the two arms cross each other (upper arm / forearm segments of the left and right arm intersect), (2) does a hand or a held weapon
// lie on the face (inside the head picture). Moves that reach across on purpose (a key with z 2, like the bow pull) skip test 1.
// python3 -m http.server 8000 ; node tools/qa/rig_tangle.js <char> [out.png]   -> per move: frames crossed / on the face; exit 1 when any move fails.
const { chromium } = require('playwright');
(async () => {
  const ch = process.argv[2] || 'zeusgpt', b = await chromium.launch(), pg = await (await b.newContext({ viewport: { width: 400, height: 300 } })).newPage(), errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/rig.html?char=' + ch + '&play=0&t=' + Date.now()); await pg.waitForFunction(() => typeof Bones2D !== 'undefined', null, { timeout: 20000 });
  const r = await pg.evaluate(async ch => {
    const B = Bones2D, rig = await B.load(`art/rigs/${ch}.json?` + Date.now()); if (rig.view !== 'front') return { skip: 'not a front-view rig' };
    const P0 = B.player(rig, { base: null }); P0.update(0); const parts = rig.parts, bk = Object.keys(rig.parts).find(k => rig.parts[k].role === 'body'), bx = rig.parts[bk].at[0], side = Object.fromEntries(Object.keys(rig.parts).filter(k => /^arm[FB]$/.test(rig.parts[k].role)).map(k => [k, rig.parts[k].at[0] < bx ? -1 : 1])), kids = k => Object.keys(parts).filter(c => parts[c].p === k && c !== k), down = k => kids(k).flatMap(c => [c, ...down(c)]);
    const hk = Object.keys(parts).find(k => parts[k].role === 'head'), him = rig.img[hk], hq = parts[hk];
    const chains = Object.keys(side).map(a => { const f = kids(a).find(c => /^fore[FB]$/.test(parts[c].role)); return { a, f, sd: side[a], tips: (f ? [f] : [a]).concat(down(f || a).filter(c => /weapon/.test(parts[c].role))) }; });
    const far = (M, k) => { const im = rig.img[k], q = parts[k]; let best = null; for (const [u, v] of [[.5, 0], [.5, 1], [0, .5], [1, .5]]) { const p = B.pt(M[k], im.width * u - q.pv[0], im.height * v - q.pv[1]), d = Math.hypot(p[0] - M[k][4], p[1] - M[k][5]); if (!best || d > best[1]) best = [p, d]; } return best[0]; };
    const pts = (M, c) => { const s = [M[c.a][4], M[c.a][5]], e = c.f ? [M[c.f][4], M[c.f][5]] : far(M, c.a), h = c.f ? far(M, c.f) : e; return [s, e, h]; };
    const X = (p, q, r, s) => { const d = (a, b, c) => (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); const d1 = d(p, q, r), d2 = d(p, q, s), d3 = d(r, s, p), d4 = d(r, s, q); return d1 * d2 < 0 && d3 * d4 < 0; };
    const depth = (M, c, P) => { const Hi = B.inv(M[hk]); let deep = 0, what = null; for (const k of c.tips) { const im = rig.img[k], q = parts[k]; if (!im || (P && P.pose[k] && P.pose[k].a != null && P.pose[k].a < .1)) continue; const isW = /weapon/.test(parts[k].role), grid = isW ? [[.5, .1], [.5, .3], [.5, .5], [.5, .7], [.5, .9]] : [[.5, .5], [.5, .85]];
        for (const [u, v] of grid) { const p = B.pt(M[k], im.width * u - q.pv[0], im.height * v - q.pv[1]), l = B.pt(Hi, p[0], p[1]), x = (l[0] + hq.pv[0]) / him.width, y = (l[1] + hq.pv[1]) / him.height; if (x > .2 && x < .8 && y > .3 && y < .88) { const d = (c.sd < 0 ? x - .2 : .8 - x) * him.width * (hq.s || 1); if (d > deep) { deep = d; what = k; } } } } return [deep, what]; };
    const M0 = B.world(rig, {}, null), base = chains.map(c => depth(M0, c, null)[0]);   /* the standing picture itself is fine: only overlap BEYOND it counts (4 px slack) */
    const onFace = (M, c, P, i) => { const [d, k] = depth(M, c, P); return d > base[i] + 4 ? k : null; };
    const moves = Object.keys(B.MOVES).concat(Object.keys(rig.moves || {})).filter(m => m !== 'walk' && m !== 'run' && !(m === 'bowshot' && !rig.shot)), out = {};
    for (const mv of moves) { const m = B.moveOf ? B.moveOf(rig, mv) : B.MOVES[mv]; if (!m) continue; const P = B.player(rig, { base: null }); P.play(mv, { restart: true }); const dur = m.fn ? 1.3 : m.dur, n = Math.round(dur * 30); let cross = 0, face = 0, what = '';
      const delib = !m.fn && Object.values(m.tracks).some(tr => tr.some(k => (k[1].z || 0) > 1.5));
      for (let i = 0; i < n; i++) { P.update(1 / 30); const M = P.mats; if (chains.length === 2 && !delib) { const [a, c] = chains.map(c => pts(M, c)); if (X(a[0], a[1], c[0], c[1]) || X(a[0], a[1], c[1], c[2]) || X(a[1], a[2], c[0], c[1]) || X(a[1], a[2], c[1], c[2])) cross++; }
        for (const [ci, c] of chains.entries()) { const k = onFace(M, c, P, ci); if (k) { face++; what = parts[k].n || k; break; } } }
      out[mv] = { n, cross, face, what, delib }; }
    return { out };
  }, ch);
  if (r.skip) { console.log('skip:', r.skip); await b.close(); return; }
  let ok = true; for (const [mv, v] of Object.entries(r.out)) { const bad = v.cross > 0 || v.face > 2; if (bad) ok = false; console.log((bad ? 'FAIL' : 'ok  ') + ' ' + mv.padEnd(9) + ` arms crossed ${v.cross}/${v.n}` + (v.delib ? ' (reach on purpose: not tested)' : '') + `, on the face ${v.face}/${v.n}` + (v.what ? ' (' + v.what + ')' : '')); }
  console.log(ok ? 'NO TANGLES' : 'TANGLES FOUND', errs.length ? 'ERRORS ' + errs.join(' | ') : 'no errors'); await b.close(); process.exit(ok ? 0 : 1);
})();
