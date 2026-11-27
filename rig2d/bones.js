/* Bones2D: pictures in pieces on a small skeleton, like the summon-defence games the owner showed (2026-11-27: one hero of a recording taken
   apart = about 8 rigid pieces, each MOVED, TURNED and SCALED; numbers in docs/action-game.md). No Spine, no engine: one small file.
   - A RIG is data (art/rigs/<name>.json, made / fixed by hand in rig.html):
       { v: 2, name, dir: folder of the piece pictures, ref: optional reference picture, size: [w, h] of the reference space, feet: [x, y],
         view: 'front' for a hero seen from the front (its far arm mirrors the weapon arm; no walk / run), flip: true when the weapon side is the LEFT of the picture (moves mirrored),
         parts: { key: { img, n: Thai label, role, pv: [x, y] turning point inside the picture, at: [x, y] where that point sits, s: size,
                         r: start angle (deg), p: parent key or '', fx: mirrored, g: how far the shared moves turn THIS piece (1 = as written; fits a move to a hero's own build) } }, order: [keys back to front] }
   - MOVES are written once for ROLES (body, head, armF, weapon, legF ...), not for one hero: every rig whose pieces carry those roles plays them.
       keyed moves: { dur: seconds, loop, tracks: { role: [[time 0..1, { r, x, y, s, sx, sy, a }, ease], ...] } }  (r = degrees, x / y = hundredths of
       the hero's height, s = size; '_root' = the whole hero about its feet). Loops (idle, walk, run) are small functions of time.
       A hero facing left is the same rig drawn mirrored.
   - Hair, capes and tails (roles hair / cape / tail) swing late by themselves (a spring), whatever the move.
   Use:  const rig = await Bones2D.load('art/rigs/dagger.json');  const h = Bones2D.player(rig);  h.play('idle');
         each frame: h.update(dt); h.draw(ctx, x, y, scale, facingLeft);       one-shot moves fall back to h.base ('idle') when they end. */
'use strict';
const Bones2D = (() => {
  const D2R = Math.PI / 180, TAU = Math.PI * 2, S = Math.sin, C = Math.cos;
  /* 2-D matrices as [a, b, c, d, e, f] (canvas order) */
  const mul = (m, n) => [m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]];
  const inv = m => { const d = m[0] * m[3] - m[1] * m[2]; return [m[3] / d, -m[1] / d, -m[2] / d, m[0] / d, (m[2] * m[5] - m[3] * m[4]) / d, (m[1] * m[4] - m[0] * m[5]) / d]; };
  const trs = (x, y, deg, sx, sy) => { const c = C(deg * D2R), s = S(deg * D2R); return [c * sx, s * sx, -s * sy, c * sy, x, y]; };
  const pt = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];
  const bind = q => trs(q.at[0], q.at[1], q.r || 0, q.s * (q.fx ? -1 : 1), q.s);
  const REST = { r: 0, x: 0, y: 0, sx: 1, sy: 1, a: 1, z: 0 };   /* z > .5 = this piece (and what hangs from it) is drawn in FRONT of everything while the key lasts */
  const EASE = { lin: t => t, in: t => t * t * t, out: t => 1 - (1 - t) ** 3, io: t => t < .5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2, back: t => 1 + 2.4 * (t - 1) ** 3 + 1.4 * (t - 1) ** 2, snap: t => 1 - (1 - t) ** 5 };
  const ROLES = { body: 'ลำตัว', head: 'หัว', hair: 'ผม / หางม้า (แกว่งตาม)', cape: 'ผ้าคลุม (แกว่งตาม)', tail: 'หาง (แกว่งตาม)', armF: 'แขนหน้า (มืออาวุธ)', foreF: 'แขนล่าง หน้า', weapon: 'อาวุธ', armB: 'แขนหลัง', foreB: 'แขนล่าง หลัง',
    weaponB: 'อาวุธมือหลัง', legF: 'ขาหน้า', shinF: 'แข้งหน้า', legB: 'ขาหลัง', shinB: 'แข้งหลัง', wing: 'ปีก', none: 'ไม่ขยับเอง' };
  const SWING = { hair: [70, 9, .5], cape: [45, 7, .42], tail: [55, 8, .5] };   /* spring, damping, how hard the body's motion throws it */

  /* ---- the shared moves. Timing of attack / shoot follows the recording: no wind-up, a hard size pop inside 1/30 s, fast out, slower back,
     size leads and tilt follows. The hero faces RIGHT: minus = lean / swing back, plus = forward. */
  const K = (t, o, e) => [t, o, e || 'out'];
  const MOVES = {
    idle: { loop: true, fn(t) { const b = S(t / .64 * TAU), b2 = S(t / .64 * TAU - .7); return { _root: { sy: 1 + .036 * b, sx: 1 - .02 * b }, body: { sy: 1 + .012 * b }, head: { r: 1.6 * b2 }, armF: { r: 3 * b2 }, armB: { r: -3 * b2 }, weapon: { r: 2.5 * b2 }, weaponB: { r: -2 * b2 }, wing: { r: 10 * b, sy: 1 + .08 * b } }; } },
    walk: { loop: true, fn(t) { const p = t / .9 * TAU, s = S(p), c = C(p); return { _root: { y: -Math.abs(c) * 1 }, body: { r: 4, sy: 1 + .02 * Math.abs(c) }, head: { r: -3 }, armF: { r: 20 * s }, armB: { r: -20 * s }, foreF: { r: -10 }, foreB: { r: -10 },
      legF: { r: -26 * s }, legB: { r: 26 * s }, shinF: { r: 26 * Math.max(0, -s) }, shinB: { r: 26 * Math.max(0, s) }, wing: { r: 8 * s } }; } },
    run: { loop: true, fn(t) { const p = t / .5 * TAU, s = S(p), c = C(p); return { _root: { y: -Math.abs(c) * 2.4 + .7 }, body: { r: 12, sy: 1 + .04 * Math.abs(c) }, head: { r: -10 }, armF: { r: 44 * s }, armB: { r: -44 * s }, foreF: { r: -30 - 20 * Math.max(0, -s) }, foreB: { r: -30 - 20 * Math.max(0, s) },
      legF: { r: -46 * s - 6 }, legB: { r: 46 * s - 6 }, shinF: { r: 10 + 70 * Math.max(0, S(p + .9)) }, shinB: { r: 10 + 70 * Math.max(0, -S(p + .9)) }, wing: { r: 14 * s } }; } },
    attack: { dur: .42, tracks: {   /* an overhead chop on the weapon's own side: pop and lean back with the weapon up, chop down, settle */
      _root: [K(.1, { x: -1.5 }, 'snap'), K(.3, { x: 3.5 }, 'snap'), K(.7, { x: 1 }), K(1, {})],
      body: [K(.1, { r: -11, sy: 1.12, sx: .95 }, 'snap'), K(.3, { r: 13, sy: .92, sx: 1.07 }, 'snap'), K(.6, { r: 4, sy: 1.02 }), K(1, {}, 'io')],
      head: [K(.1, { s: 1.34, r: -7 }, 'snap'), K(.3, { s: 1.12, r: 11 }, 'snap'), K(.6, { s: 1.03, r: 4 }), K(1, {}, 'io')],
      armF: [K(.1, { r: -158 }, 'snap'), K(.3, { r: -38 }, 'snap'), K(.6, { r: -14 }), K(1, {}, 'io')], foreF: [K(.1, { r: 58 }, 'snap'), K(.3, { r: 14 }, 'snap'), K(.6, { r: 4 }), K(1, {}, 'io')],
      weapon: [K(.1, { r: -34 }, 'snap'), K(.3, { r: 30, s: 1.18 }, 'snap'), K(.6, { r: 8 }), K(1, {}, 'io')],
      armB: [K(.1, { r: -26 }, 'snap'), K(.3, { r: 30 }, 'snap'), K(1, {}, 'io')], legF: [K(.3, { r: -12 }, 'snap'), K(1, {}, 'io')], legB: [K(.3, { r: 10 }, 'snap'), K(1, {}, 'io')], wing: [K(.1, { r: -25 }), K(.3, { r: 30 }), K(1, {}, 'io')] } },
    shoot: { dur: .4, tracks: {   /* the gunner of the recording, key by key (its head: 140 % / 16 deg at once, 132 / 24, 116 / 32, 108 / 44, 100 / 36, 100 / 20, 108 / 0, then still) */
      body: [K(.06, { r: -9, sy: 1.12, sx: .96 }, 'snap'), K(.14, { r: -14, sy: 1.1, sx: .96 }, 'lin'), K(.21, { r: -18, sy: 1.07, sx: .97 }, 'lin'), K(.31, { r: -24, sy: 1.03, sx: .985 }, 'lin'), K(.39, { r: -20 }, 'lin'), K(.46, { r: -11, sy: .97, sx: 1.02 }, 'lin'), K(.56, { r: 0, sy: 1.03 }, 'lin'), K(.66, { r: 2 }), K(.8, {})],
      head: [K(.06, { s: 1.46, r: -7 }, 'snap'), K(.14, { s: 1.375, r: -10 }, 'lin'), K(.21, { s: 1.2, r: -14 }, 'lin'), K(.31, { s: 1.1, r: -20 }, 'lin'), K(.39, { r: -16 }, 'lin'), K(.46, { r: -9 }, 'lin'), K(.56, { s: 1.08, r: 0 }, 'lin'), K(.64, {}, 'lin')],
      armF: [K(.06, { r: -82 }, 'snap'), K(.14, { r: -112 }, 'lin'), K(.31, { r: -125 }), K(.46, { r: -48 }, 'io'), K(.56, { r: -9 }), K(.68, {})], foreF: [K(.06, { r: 52 }, 'snap'), K(.31, { r: 62 }), K(.56, {}, 'io')],
      weapon: [K(.06, { r: -8, s: 1.12 }, 'snap'), K(.14, { r: -24, s: 1.2 }, 'snap'), K(.31, { r: -16, s: 1.1 }), K(.56, {}, 'io')], armB: [K(.06, { r: 22 }, 'snap'), K(.31, { r: 28 }), K(.56, {}, 'io')], wing: [K(.06, { r: -20 }, 'snap'), K(.46, { r: 8 }), K(.7, {})] } },
    cast: { dur: .7, tracks: {   /* arms up, held, thrown down */
      body: [K(.2, { sy: 1.1, sx: .95, r: -5 }, 'snap'), K(.55, { sy: 1.12, sx: .94, r: -6 }, 'lin'), K(.68, { sy: .92, sx: 1.07, r: 8 }, 'snap'), K(1, {}, 'io')],
      head: [K(.2, { s: 1.22, r: -10 }, 'snap'), K(.55, { s: 1.18, r: -12 }, 'lin'), K(.68, { s: 1.08, r: 10 }, 'snap'), K(1, {}, 'io')],
      armF: [K(.2, { r: -118 }, 'snap'), K(.55, { r: -126 }, 'lin'), K(.68, { r: -30 }, 'snap'), K(1, {}, 'io')], armB: [K(.2, { r: -110 }, 'snap'), K(.55, { r: -118 }, 'lin'), K(.68, { r: -24 }, 'snap'), K(1, {}, 'io')],
      foreF: [K(.2, { r: 68 }, 'snap'), K(.55, { r: 72 }, 'lin'), K(.68, { r: 10 }, 'snap'), K(1, {}, 'io')], foreB: [K(.2, { r: 64 }, 'snap'), K(.55, { r: 68 }, 'lin'), K(.68, { r: 10 }, 'snap'), K(1, {}, 'io')],
      weapon: [K(.2, { r: -20, s: 1.15 }, 'snap'), K(.55, { r: -26, s: 1.2 }, 'lin'), K(.68, { r: 25 }, 'snap'), K(1, {}, 'io')], _root: [K(.2, { y: -2 }, 'snap'), K(.55, { y: -2.6 }, 'lin'), K(.68, { y: 0 }, 'snap'), K(1, {})], wing: [K(.2, { r: -30 }), K(.68, { r: 25 }, 'snap'), K(1, {})] } },
    hit: { dur: .3, tracks: {   /* knocked back, squashed, back up */
      _root: [K(.2, { x: -4 }, 'snap'), K(1, {}, 'io')], body: [K(.2, { r: -13, sy: .88, sx: 1.1 }, 'snap'), K(.6, { r: 3, sy: 1.04 }), K(1, {})],
      head: [K(.2, { r: -18, s: 1.12 }, 'snap'), K(.6, { r: 5 }), K(1, {})], armF: [K(.2, { r: -32 }, 'snap'), K(1, {}, 'io')], armB: [K(.2, { r: -26 }, 'snap'), K(1, {}, 'io')], weapon: [K(.2, { r: -18 }, 'snap'), K(1, {}, 'io')] } },
    die: { dur: .8, hold: true, tracks: {   /* a hop, fall on the back, fade */
      _root: [K(.15, { y: -5, r: -8 }, 'out'), K(.5, { y: 0, r: -84 }, 'in'), K(.58, { r: -78 }), K(.66, { r: -84 }), K(.8, { r: -84 }, 'lin'), K(1, { r: -84, a: 0 }, 'lin')],
      body: [K(.15, { sy: 1.1, sx: .94 }, 'snap'), K(.5, { sy: .9, sx: 1.08 }, 'in'), K(.66, { sy: 1 }), K(1, {})], head: [K(.15, { r: 12, s: 1.15 }, 'snap'), K(.5, { r: -10 }, 'in'), K(1, { r: -6 })],
      armF: [K(.15, { r: -60 }, 'snap'), K(.5, { r: -110 }, 'in'), K(1, { r: -100 })], armB: [K(.15, { r: 50 }, 'snap'), K(.5, { r: 70 }, 'in'), K(1, { r: 60 })], legF: [K(.5, { r: 22 }, 'in'), K(1, { r: 18 })], legB: [K(.5, { r: -10 }, 'in'), K(1, { r: -8 })] } },
    spawn: { dur: .5, tracks: {   /* pops out of nothing, overshoots, settles */
      _root: [K(0, { s: .05, a: 0 }), K(.3, { s: 1.18, a: 1, y: -3 }, 'snap'), K(.55, { s: .94, y: 0 }, 'io'), K(.8, { s: 1.03 }), K(1, {})],
      body: [K(.3, { sy: 1.12, sx: .92 }, 'snap'), K(.55, { sy: .9, sx: 1.1 }, 'io'), K(1, {})], head: [K(.3, { s: 1.15 }, 'snap'), K(.55, { s: .97 }), K(1, {})], armF: [K(.3, { r: -70 }, 'snap'), K(1, {}, 'io')], armB: [K(.3, { r: 60 }, 'snap'), K(1, {}, 'io')] } },
    cheer: { dur: .9, tracks: {   /* two happy hops, arms up */
      _root: [K(.12, { y: 0 }), K(.3, { y: -9 }, 'out'), K(.48, { y: 0 }, 'in'), K(.56, { y: 0 }), K(.72, { y: -6 }, 'out'), K(.88, { y: 0 }, 'in'), K(1, {})],
      body: [K(.12, { sy: .9, sx: 1.08 }, 'snap'), K(.3, { sy: 1.1, sx: .94 }), K(.5, { sy: .9, sx: 1.08 }, 'in'), K(.72, { sy: 1.08, sx: .95 }), K(.9, { sy: .94, sx: 1.05 }, 'in'), K(1, {})],
      head: [K(.3, { s: 1.14, r: -8 }), K(.5, { r: 4 }), K(.72, { s: 1.1, r: -6 }), K(1, {})], armF: [K(.3, { r: -122 }, 'snap'), K(.5, { r: -98 }), K(.72, { r: -126 }), K(1, {}, 'io')], armB: [K(.3, { r: -116 }, 'snap'), K(.5, { r: -94 }), K(.72, { r: -120 }), K(1, {}, 'io')], foreF: [K(.3, { r: 66 }, 'snap'), K(.5, { r: 50 }), K(.72, { r: 68 }), K(1, {}, 'io')], foreB: [K(.3, { r: 62 }, 'snap'), K(.5, { r: 48 }), K(.72, { r: 64 }), K(1, {}, 'io')], weapon: [K(.3, { r: -20 }), K(1, {}, 'io')] } },
  };
  /* a raised arm must not vanish behind a big chibi head: while these moves last the weapon arm (and, on front-view heroes, the far arm) is drawn in front, like the raised gun of the recording */
  for (const [mv, roles] of [['attack', ['armF']], ['shoot', ['armF']], ['cast', ['armF', 'armB']], ['cheer', ['armF', 'armB']]]) for (const ro of roles) { const tr = MOVES[mv].tracks[ro]; if (tr) tr.forEach((key, i) => { if (i < tr.length - 1) key[1].z = 1; }); }
  const NAMES = { idle: 'ยืน', attack: 'ตี', shoot: 'ยิง', cast: 'ร่าย', hit: 'โดนตี', die: 'ตาย', spawn: 'เกิด', cheer: 'ดีใจ', walk: 'เดิน', run: 'วิ่ง' };

  function sample(mv, t, out) {   /* pose of every role at time t (seconds) of a move -> out[role] = { r, x, y, sx, sy, a } */
    for (const k in out) delete out[k];
    if (mv.fn) { const o = mv.fn(t); for (const k in o) out[k] = Object.assign({}, REST, o[k]); return out; }
    const u = Math.min(1, Math.max(0, t / mv.dur));
    for (const role in mv.tracks) { const tr = mv.tracks[role]; let a = null, b = null; for (const key of tr) { if (key[0] <= u) a = key; else { b = key; break; } }
      const A = full(a ? a[1] : null), o = out[role] = {}; if (!b) { Object.assign(o, A); continue; } const B = full(b[1]), t0 = a ? a[0] : 0, f = EASE[b[2]]((u - t0) / Math.max(1e-6, b[0] - t0)); for (const c in REST) o[c] = A[c] + (B[c] - A[c]) * f; }
    return out;
  }
  function full(o) { const q = Object.assign({}, REST); if (o) { for (const c in o) if (c === 's') q.sx = q.sy = o.s; else q[c] = o[c]; if (o.s != null) { if (o.sx != null) q.sx = o.sx; if (o.sy != null) q.sy = o.sy; } } return q; }

  /* ---- a rig posed: world matrix of every part. pose = { partKey: { r, x, y, sx, sy } }, root = { x, y, r, sx, sy } about the feet */
  function prep(rig) { const B = {}, BI = {}; for (const k in rig.parts) { B[k] = bind(rig.parts[k]); BI[k] = inv(B[k]); } rig._b = B; rig._bi = BI; rig._plant = {}; for (const k in rig.parts) { const q = rig.parts[k], p = q.p && rig.parts[q.p]; rig._plant[k] = !!(p && (q.role === 'legF' || q.role === 'legB') && p.role === 'body'); } rig._u = (rig.size ? rig.size[1] : 500) / 100; rig._feet = rig.feet || [rig.size[0] / 2, rig.size[1]]; return rig; }
  function world(rig, pose, root, memo) {
    memo = memo || {}; const F = rig._feet, u = rig._u, R0 = root || REST;
    const base = mul(trs(F[0] + (R0.x || 0) * u, F[1] + (R0.y || 0) * u, R0.r || 0, R0.sx == null ? 1 : R0.sx, R0.sy == null ? 1 : R0.sy), [1, 0, 0, 1, -F[0], -F[1]]);
    const get = k => { if (memo[k]) return memo[k]; const q = rig.parts[k], P = pose[k]; let d = base; if (q.p && rig.parts[q.p] && q.p !== k && !rig._plant[k]) d = mul(get(q.p), rig._bi[q.p]);   /* a planted leg keeps its place under the hero whatever the body does */
      let m = P && (P.x || P.y) ? mul(mul(d, [1, 0, 0, 1, P.x * u, P.y * u]), rig._b[k]) : mul(d, rig._b[k]); if (P && (P.r || P.sx !== 1 || P.sy !== 1)) m = mul(m, trs(0, 0, (P.r || 0) * (q.fx ? -1 : 1), P.sx == null ? 1 : P.sx, P.sy == null ? 1 : P.sy)); return memo[k] = m; };
    for (const k in rig.parts) get(k); return memo;
  }

  function load(url) { return fetch(url).then(r => { if (!r.ok) throw new Error(url + ' ' + r.status); return r.json(); }).then(rig => images(rig)); }
  function images(rig) { prep(rig); rig.img = {}; return Promise.all(Object.keys(rig.parts).map(k => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(); i.onerror = () => no(new Error('picture ' + i.src)); i.src = rig.dir + (rig.parts[k].img || k + '.png'); rig.img[k] = i; }))).then(() => rig); }

  function player(rig, opt) {
    opt = opt || {}; const P = { rig, base: opt.base === undefined ? 'idle' : opt.base, pop: opt.pop == null ? 1 : opt.pop, speed: 1, move: null, name: '', t: 0, done: false, pose: {}, root: Object.assign({}, REST), roles: {}, from: null, fade: 0, sw: {}, mats: null, alpha: 1 };
    const tmp = {};
    P.play = (name, o) => { const mv = MOVES[name]; if (!mv) return P; o = o || {}; if (P.move && P.name !== name || o.restart) { P.from = { pose: JSON.parse(JSON.stringify(P.pose)), root: Object.assign({}, P.root) }; P.fade = o.fade == null ? .07 : o.fade; P.fadeT = 0; }
      if (P.name !== name || o.restart || P.done) { P.t = 0; P.done = false; } P.move = mv; P.name = name; if (o.speed) P.speed = o.speed; return P; };
    P.update = dt => { if (!P.move) return; const mv = P.move; P.t += dt * P.speed;
      if (!mv.fn && P.t >= mv.dur) { if (mv.hold) { P.t = mv.dur; P.done = true; } else if (mv.loop) P.t %= mv.dur; else { P.done = true; if (P.base && MOVES[P.base]) { const left = P.t - mv.dur; P.play(P.base, { fade: .1 }); P.t = left; } else P.t = mv.dur; } }
      sample(P.move, P.t, tmp); P.roles = tmp; const pop = P.pop, pose = P.pose; for (const k in pose) delete pose[k];
      const fl = rig.flip ? -1 : 1, front = rig.view === 'front'; for (const k in rig.parts) { const ro = rig.parts[k].role, o = ro && tmp[ro]; if (!o) continue; const far = ro === 'armB' || ro === 'foreB' || ro === 'weaponB', sg = front && far ? -fl : fl, q = pose[k] = { r: o.r * sg * (rig.parts[k].g == null ? 1 : rig.parts[k].g), x: o.x * fl, y: o.y, sx: o.sx, sy: o.sy, z: far && !front ? 0 : o.z || 0 }; if (pop !== 1 && (ro === 'head' || ro === 'body' || ro === 'weapon')) { q.sx = 1 + (q.sx - 1) * pop; q.sy = 1 + (q.sy - 1) * pop; } }
      const r0 = tmp._root ? tmp._root : REST; for (const c in REST) P.root[c] = r0[c] == null ? REST[c] : r0[c]; if (fl < 0) { P.root.r = -P.root.r; P.root.x = -P.root.x; }
      if (P.from) { P.fadeT += dt; const f = P.fade > 0 ? Math.min(1, P.fadeT / P.fade) : 1; if (f >= 1) P.from = null; else { for (const k in rig.parts) { const a = P.from.pose[k] || REST, b = pose[k] || (pose[k] = Object.assign({}, REST)); for (const c of ['r', 'x', 'y', 'sx', 'sy']) b[c] = a[c] + (b[c] - a[c]) * f; } for (const c in REST) P.root[c] = P.from.root[c] + (P.root[c] - P.from.root[c]) * f; } }
      /* hair / cape / tail: a spring thrown by how fast their turning point moves */
      let mats = world(rig, pose, P.root); const h = Math.min(dt, .05);
      for (const k in rig.parts) { const sp = SWING[rig.parts[k].role]; if (!sp) continue; const m = mats[k], s = P.sw[k] || (P.sw[k] = { a: 0, v: 0, x: m[4], y: m[5] }); const vx = (m[4] - s.x) / Math.max(h, 1e-3), vy = (m[5] - s.y) / Math.max(h, 1e-3); s.x = m[4]; s.y = m[5];
        const im = rig.img && rig.img[k], lx = (im ? im.width / 2 : 0) - rig.parts[k].pv[0], ly = (im ? im.height / 2 : 40) - rig.parts[k].pv[1], dx = m[0] * lx + m[2] * ly, dy = m[1] * lx + m[3] * ly, dl = Math.hypot(dx, dy) || 1;   /* which way the piece hangs from its turning point: it lags behind the motion */
        const push = Math.max(-900, Math.min(900, (dy * vx - dx * vy) / dl * sp[2] / rig._u)); s.v += (-sp[0] * s.a - sp[1] * s.v + push * 6) * h; s.a = Math.max(-55, Math.min(55, s.a + s.v * h)); const q = pose[k] || (pose[k] = Object.assign({}, REST)); q.r += s.a; }
      P.mats = world(rig, pose, P.root); P.alpha = P.root.a == null ? 1 : P.root.a; };
    const isFront = k => { for (let n = 0; k && n < 8; n++, k = rig.parts[k].p) { if (P.pose[k] && P.pose[k].z > .5) return true; if (!rig.parts[k]) break; } return false; };
    P.order = () => { const a = [], f = []; for (const k of rig.order) (isFront(k) ? f : a).push(k); return f.length ? a.concat(f) : rig.order; };   /* back to front for this pose */
    P.draw = (ctx, x, y, scale, left) => { if (!P.mats) P.update(0); if (!P.mats) return; const F = rig._feet, sx = left ? -scale : scale, V = [sx, 0, 0, scale, x - F[0] * sx, y - F[1] * scale], a0 = ctx.globalAlpha; ctx.globalAlpha = a0 * Math.max(0, Math.min(1, P.alpha));
      for (const k of P.order()) { const q = rig.parts[k], m = mul(V, P.mats[k]); ctx.setTransform(m[0], m[1], m[2], m[3], m[4], m[5]); ctx.drawImage(rig.img[k], -q.pv[0], -q.pv[1]); } ctx.globalAlpha = a0; };
    return P;
  }
  return { load, images, prep, player, world, sample, bind, mul, inv, pt, trs, MOVES, NAMES, ROLES, EASE, REST };
})();
if (typeof module !== 'undefined') module.exports = Bones2D;
