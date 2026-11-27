/* Bones2D: pictures in pieces on a small skeleton, like the summon-defence games the owner showed (2026-11-27: one hero of a recording taken
   apart = about 8 rigid pieces, each MOVED, TURNED and SCALED; numbers in docs/action-game.md). No Spine, no engine: one small file.
   - A RIG is data (art/rigs/<name>.json, made / fixed by hand in rig.html):
       { v: 2, name, dir: folder of the piece pictures, ref: optional reference picture, size: [w, h] of the reference space, feet: [x, y],
         zfront: true = raised arms may be drawn in front of the head (only for pieces without visible joint ends; default off = joints stay hidden under the body),
         clips: { move: { dir, frames: [pngs], durs: [ms], foot: [x, y] in the frame, figH: figure height in the frame, ev: [[0..1, 'release']] } } = DRAWN-FRAME moves
           (big moves bones cannot do, like a throw that turns the body) played in place of the pieces, sized to figH (the rig's own figure height), short cross-fades;
         view: 'front' for a hero seen from the front (its far arm mirrors the weapon arm; no walk / run), flip: true when the weapon side is the LEFT of the picture (moves mirrored),
         swaps: { piece: { idle: picture, attack: picture, ... } } = pictures of the SAME size a piece swaps between by move (faces, fists; 'none' = hidden),
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
  const EASE = { lin: t => t, in: t => t * t * t, out: t => 1 - (1 - t) ** 3, io: t => t < .5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2, back: t => 1 + 2.4 * (t - 1) ** 3 + 1.4 * (t - 1) ** 2, hold: t => t >= 1 ? 1 : 0, snap: t => 1 - (1 - t) ** 5 };
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
      armF: [K(.1, { r: -128 }, 'snap'), K(.3, { r: -38 }, 'snap'), K(.6, { r: -14 }), K(1, {}, 'io')], foreF: [K(.1, { r: 58 }, 'snap'), K(.3, { r: 14 }, 'snap'), K(.6, { r: 4 }), K(1, {}, 'io')],
      weapon: [K(.1, { r: -34 }, 'snap'), K(.3, { r: 30, s: 1.18 }, 'snap'), K(.6, { r: 8 }), K(1, {}, 'io')],
      armB: [K(.1, { r: -26 }, 'snap'), K(.3, { r: 30 }, 'snap'), K(1, {}, 'io')], legF: [K(.3, { r: -12 }, 'snap'), K(1, {}, 'io')], legB: [K(.3, { r: 10 }, 'snap'), K(1, {}, 'io')], wing: [K(.1, { r: -25 }), K(.3, { r: 30 }), K(1, {}, 'io')] } },
    shoot: { dur: .4, tracks: {   /* the gunner of the recording, key by key (its head: 140 % / 16 deg at once, 132 / 24, 116 / 32, 108 / 44, 100 / 36, 100 / 20, 108 / 0, then still) */
      body: [K(.06, { r: -9, sy: 1.12, sx: .96 }, 'snap'), K(.14, { r: -14, sy: 1.1, sx: .96 }, 'lin'), K(.21, { r: -18, sy: 1.07, sx: .97 }, 'lin'), K(.31, { r: -24, sy: 1.03, sx: .985 }, 'lin'), K(.39, { r: -20 }, 'lin'), K(.46, { r: -11, sy: .97, sx: 1.02 }, 'lin'), K(.56, { r: 0, sy: 1.03 }, 'lin'), K(.66, { r: 2 }), K(.8, {})],
      head: [K(.06, { s: 1.46, r: -7 }, 'snap'), K(.14, { s: 1.375, r: -10 }, 'lin'), K(.21, { s: 1.2, r: -14 }, 'lin'), K(.31, { s: 1.1, r: -20 }, 'lin'), K(.39, { r: -16 }, 'lin'), K(.46, { r: -9 }, 'lin'), K(.56, { s: 1.08, r: 0 }, 'lin'), K(.64, {}, 'lin')],
      armF: [K(.06, { r: -82 }, 'snap'), K(.14, { r: -112 }, 'lin'), K(.31, { r: -125 }), K(.46, { r: -48 }, 'io'), K(.56, { r: -9 }), K(.68, {})], foreF: [K(.06, { r: 52 }, 'snap'), K(.31, { r: 62 }), K(.56, {}, 'io')],
      weapon: [K(.06, { r: -8, s: 1.12 }, 'snap'), K(.14, { r: -24, s: 1.2 }, 'snap'), K(.31, { r: -16, s: 1.1 }), K(.56, {}, 'io')], armB: [K(.06, { r: 22 }, 'snap'), K(.31, { r: 28 }), K(.56, {}, 'io')], wing: [K(.06, { r: -20 }, 'snap'), K(.46, { r: 8 }), K(.7, {})] } },
    cast: { dur: .7, tracks: {   /* arms up, held, thrown down */
      body: [K(.2, { sy: 1.1, sx: .95, r: -5 }, 'snap'), K(.55, { sy: 1.12, sx: .94, r: -6 }, 'lin'), K(.68, { sy: .92, sx: 1.07, r: 8 }, 'snap'), K(1, {}, 'io')],
      head: [K(.2, { s: 1.14, r: -8 }, 'snap'), K(.55, { s: 1.12, r: -10 }, 'lin'), K(.68, { s: 1.08, r: 10 }, 'snap'), K(1, {}, 'io')],
      armF: [K(.2, { r: -100 }, 'snap'), K(.55, { r: -106 }, 'lin'), K(.68, { r: -30 }, 'snap'), K(1, {}, 'io')], armB: [K(.2, { r: -96 }, 'snap'), K(.55, { r: -102 }, 'lin'), K(.68, { r: -24 }, 'snap'), K(1, {}, 'io')],
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
      head: [K(.3, { s: 1.14, r: -8 }), K(.5, { r: 4 }), K(.72, { s: 1.1, r: -6 }), K(1, {})], armF: [K(.3, { r: -104 }, 'snap'), K(.5, { r: -84 }), K(.72, { r: -106 }), K(1, {}, 'io')], armB: [K(.3, { r: -100 }, 'snap'), K(.5, { r: -80 }), K(.72, { r: -102 }), K(1, {}, 'io')], foreF: [K(.3, { r: 66 }, 'snap'), K(.5, { r: 50 }), K(.72, { r: 68 }), K(1, {}, 'io')], foreB: [K(.3, { r: 62 }, 'snap'), K(.5, { r: 48 }), K(.72, { r: 64 }), K(1, {}, 'io')], weapon: [K(.3, { r: -20 }), K(1, {}, 'io')] } },
  };
  /* a raised arm must not vanish behind a big chibi head: while these moves last the weapon arm (and, on front-view heroes, the far arm) is drawn in front, like the raised gun of the recording */
  for (const [mv, roles] of [['attack', ['armF']], ['shoot', ['armF']], ['cast', ['armF', 'armB']], ['cheer', ['armF', 'armB']]]) for (const ro of roles) { const tr = MOVES[mv].tracks[ro]; if (tr) tr.forEach((key, i) => { if (i < tr.length - 1) key[1].z = 1; }); }
  MOVES.bowshot = { n: 'ยิงธนู', dur: 1.05, ev: [[.55, 'release']], tracks: {   /* raise the bow arm level, the other hand pulls the string back (fx.js draws string + arrow), hold, release: the arrow leaves (event), the pull hand flies back, recoil */
      _root: [K(.3, {}), K(.55, { x: -1 }, 'lin'), K(.6, { x: -3 }, 'snap'), K(1, {}, 'io')],
      body: [K(.3, { r: -3, sy: 1.04, sx: .98 }, 'io'), K(.55, { r: -4, sy: 1.05 }, 'lin'), K(.6, { r: 3, sy: .94, sx: 1.04 }, 'snap'), K(.8, { r: 1, sy: 1.02 }), K(1, {}, 'io')],
      head: [K(.3, { s: 1.06, r: -3 }, 'io'), K(.55, { s: 1.08, r: -4 }, 'lin'), K(.6, { s: 1.28, r: 4 }, 'snap'), K(.75, { s: 1.08, r: 2 }), K(1, {}, 'io')],
      armF: [K(.15, { r: -40 }, 'io'), K(.3, { r: -84 }, 'snap'), K(.55, { r: -86 }, 'lin'), K(.6, { r: -78 }, 'snap'), K(.8, { r: -70 }), K(1, {}, 'io')],
      weapon: [K(.15, { r: 40 }, 'io'), K(.3, { r: 84, s: 1.05 }, 'snap'), K(.55, { r: 86, s: 1.05 }, 'lin'), K(.6, { r: 78, s: 1.15 }, 'snap'), K(.8, { r: 70 }), K(1, {}, 'io')],
      armB: [K(.15, { r: 40, z: 2 }, 'io'), K(.3, { r: 100, z: 2 }, 'io'), K(.55, { r: 88, z: 2 }, 'lin'), K(.6, { r: -60 }, 'snap'), K(.8, { r: -30 }), K(1, {}, 'io')],   /* the pull hand comes across the chest (in front), pulls back, flies out on release */
      legF: [K(.3, { r: -6 }, 'io'), K(1, {}, 'io')], legB: [K(.3, { r: 6 }, 'io'), K(1, {}, 'io')], cape: [K(.3, { r: -4 }), K(.6, { r: 8 }, 'snap'), K(1, {}, 'io')] } };
  MOVES.thrust = { n: 'แทง', dur: .62, ev: [[.42, 'hit']], tracks: {   /* a spear / trident stab: pull back with the point level, lunge, stab out at full reach (event 'hit'), hold a beat, recover */
      _root: [K(.3, { x: -3 }, 'io'), K(.42, { x: 6 }, 'snap'), K(.6, { x: 6.5 }), K(1, {}, 'io')],
      body: [K(.3, { r: -10, sy: 1.06, sx: .96 }, 'io'), K(.42, { r: 14, sy: .92, sx: 1.07 }, 'snap'), K(.6, { r: 12, sy: .95 }), K(1, {}, 'io')],
      head: [K(.3, { s: 1.1, r: -6 }, 'io'), K(.42, { s: 1.34, r: 8 }, 'snap'), K(.6, { s: 1.12, r: 6 }), K(1, {}, 'io')],
      armF: [K(.3, { r: -30 }, 'io'), K(.42, { r: -86 }, 'snap'), K(.6, { r: -82 }), K(1, {}, 'io')], foreF: [K(.3, { r: 70 }, 'io'), K(.42, { r: -4 }, 'snap'), K(.6, { r: 0 }), K(1, {}, 'io')],
      weapon: [K(.3, { r: 60, s: 1.08 }, 'io'), K(.42, { r: 172, s: 1.22 }, 'snap'), K(.6, { r: 168, s: 1.12 }), K(1, {}, 'io')],   /* the arm's own turn carries the weapon: these angles leave the point level and forward */
      armB: [K(.3, { r: 20 }, 'io'), K(.42, { r: 34 }, 'snap'), K(1, {}, 'io')], legF: [K(.42, { r: -16 }, 'snap'), K(.7, { r: -14 }), K(1, {}, 'io')], legB: [K(.42, { r: 14 }, 'snap'), K(.7, { r: 12 }), K(1, {}, 'io')],
      cape: [K(.3, { r: 6 }), K(.42, { r: -10 }, 'snap'), K(1, {}, 'io')], wing: [K(.3, { r: -20 }), K(.42, { r: 25 }, 'snap'), K(1, {}, 'io')] } };
  MOVES.throw = { n: 'ปาสายฟ้า (กระดูก)', dur: 1.1, ev: [[.5, 'release']], tracks: {   /* ปาสายฟ้า, after the owner's 16-frame row: bring the bolt up, cock it high overhead and lean away
     (charge), whip it forward with the whole body, the bolt leaves the hand (event 'release'), follow through low, settle. Hero faces right = throws to the right. */
      _root: [K(.12, {}), K(.3, { x: -2.5 }, 'io'), K(.46, { x: -3.5 }, 'lin'), K(.52, { x: 4.5 }, 'snap'), K(.66, { x: 5.5 }), K(.86, { x: 1 }, 'io'), K(1, {}, 'io')],
      body: [K(.12, { r: -3, sy: 1.02 }), K(.3, { r: -16, sy: 1.08, sx: .94 }, 'io'), K(.46, { r: -19, sy: 1.1, sx: .93 }, 'lin'), K(.52, { r: 18, sy: .9, sx: 1.08 }, 'snap'), K(.66, { r: 22, sy: .84, sx: 1.1 }), K(.86, { r: 4, sy: 1.03 }, 'io'), K(1, {}, 'io')],
      head: [K(.12, { r: -2 }), K(.3, { s: 1.12, r: -12 }, 'io'), K(.46, { s: 1.16, r: -14 }, 'lin'), K(.52, { s: 1.4, r: 14, y: 2 }, 'snap'), K(.6, { s: 1.24, r: 18, y: 4 }), K(.7, { s: 1.08, r: 12, y: 5 }), K(.86, { s: 1.02, r: 2 }, 'io'), K(1, {}, 'io')],
      armF: [K(.12, { r: -32 }, 'io'), K(.3, { r: -114 }, 'io'), K(.46, { r: -120 }, 'lin'), K(.52, { r: -52 }, 'snap'), K(.62, { r: -36 }), K(.72, { r: -20 }), K(.86, { r: -5 }, 'io'), K(1, {}, 'io')],
      foreF: [K(.12, { r: 20 }), K(.3, { r: 70 }, 'io'), K(.46, { r: 76 }, 'lin'), K(.52, { r: -6 }, 'snap'), K(.7, { r: 4 }), K(1, {}, 'io')],
      weapon: [K(.12, { r: -10 }), K(.3, { r: -56, s: 1.45 }, 'io'), K(.46, { r: -60, s: 1.6 }, 'lin'), K(.5, { r: 10, s: 1.3 }, 'snap'), K(.505, { a: 0 }, 'hold'), K(.9, { a: 0 }), K(.95, { s: .4, a: 0 }, 'hold'), K(1, { a: 1 }, 'out')],
      armB: [K(.12, { r: -10 }), K(.3, { r: -70 }, 'io'), K(.46, { r: -74 }, 'lin'), K(.52, { r: 30 }, 'snap'), K(.66, { r: 36 }), K(.86, { r: 6 }, 'io'), K(1, {}, 'io')],
      foreB: [K(.3, { r: 30 }, 'io'), K(.52, { r: 0 }, 'snap'), K(1, {}, 'io')],
      legF: [K(.3, { r: 6 }, 'io'), K(.52, { r: -14 }, 'snap'), K(.86, {}, 'io')], legB: [K(.3, { r: -8 }, 'io'), K(.52, { r: 12 }, 'snap'), K(.86, {}, 'io')],
      wing: [K(.3, { r: -30 }, 'io'), K(.52, { r: 30 }, 'snap'), K(1, {}, 'io')] } };
  const NAMES = { throw: 'ปาสายฟ้า', idle: 'ยืน', attack: 'ตี', shoot: 'ยิง', cast: 'ร่าย', hit: 'โดนตี', die: 'ตาย', spawn: 'เกิด', cheer: 'ดีใจ', walk: 'เดิน', run: 'วิ่ง' };

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
  function images(rig) { prep(rig); rig.img = {}; const clipP0 = []; const one = (key, file) => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(); i.onerror = () => no(new Error('picture ' + i.src)); i.src = rig.dir + file; rig.img[key] = i; });
    if (rig.faces && !rig.swaps) { const f = rig.faces, o = {}; for (const k in f) if (k !== 'part') o[k] = f[k]; rig.swaps = { [f.part]: o }; }   /* old form: faces = one swapping piece */
    if (rig.shot) clipP0.push(one('_shot', rig.shot));
    const extra = rig.swaps ? [...new Set(Object.values(rig.swaps).flatMap(o => Object.values(o)))] : [];   /* faces: { part: 'head', idle: 'face0', attack: 'face1', ... } = the picture (same size) that piece shows during a move */
    const refP = rig.ref ? new Promise(ok => { const i = new Image(); i.onload = () => { rig.img._ref = i; ok(); }; i.onerror = () => ok(); i.src = rig.dir + rig.ref; }) : Promise.resolve();
    const maskP = rig.refMask ? new Promise(ok => { const i = new Image(); i.onload = () => { rig.img._refMask = i; ok(); }; i.onerror = () => ok(); i.src = rig.dir + rig.refMask; }) : Promise.resolve();
    const clipP = []; for (const cn in rig.clips || {}) { const c = rig.clips[cn]; c.img = []; c.frames.forEach((f, i) => clipP.push(new Promise((ok, no) => { const im = new Image(); im.onload = () => ok(); im.onerror = () => no(new Error('frame ' + im.src)); im.src = rig.dir + c.dir + f; c.img[i] = im; }))); c.dur = c.durs.reduce((a, b) => a + b, 0) / 1000; }
    return Promise.all(Object.keys(rig.parts).map(k => one(k, rig.parts[k].img || k + '.png')).concat(extra.map(f => one('@' + f, f + '.png')), [refP, maskP], clipP, clipP0)).then(() => { if (rig.seams === 'paint') seamless(rig); if (rig.bake) bake(rig); return rig; }); }

  /* SEAMS (owner 2026-11-27 "ประกอบเสร็จก็ลบเส้นออกด้วยสิ ทำให้เหมือนตอนยังไม่ต่อกระดูก"): once the pieces are put together, the edge of a piece
     that lies over another piece is painted with what the picture before rigging (rig.ref) shows there, so a joint line the drawing does not have
     goes away; lines the drawing really has (chin, cuffs, skirt hem) stay because the reference is dark there too. Silhouette edges (nothing under them)
     are kept. Done once on load, in the rest pose; the original pictures stay in rig.img0. Only for rigs with seams: 'paint' (a rig cut from its own reference, like zeusgpt, already has no extra lines). */
  function seamless(rig, band = 4, keepR = 1) {
    const R = rig.img._ref; if (!R || !rig.order) return; prep(rig); const [W, H] = rig.size, cv = c => { const e = document.createElement('canvas'); e.width = c[0]; e.height = c[1]; return e; };
    const rc = cv([W, H]), rg = rc.getContext('2d'); rg.drawImage(R, 0, 0, W, H); const ref = rg.getImageData(0, 0, W, H).data, lum = new Float32Array(W * H);
    for (let i = 0; i < W * H; i++) lum[i] = ref[i * 4] * .299 + ref[i * 4 + 1] * .587 + ref[i * 4 + 2] * .114;
    const darkNear = new Uint8Array(W * H);   /* the reference has a line within keepR px */
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (lum[y * W + x] < 80) for (let dy = -keepR; dy <= keepR; dy++) for (let dx = -keepR; dx <= keepR; dx++) { const X = x + dx, Y = y + dy; if (X >= 0 && Y >= 0 && X < W && Y < H && dx * dx + dy * dy <= keepR * keepR) darkNear[Y * W + X] = 1; }
    const M = world(rig, {}, null), cov = cv([W, H]), cg = cov.getContext('2d'); rig.img0 = Object.assign({}, rig.img);
    const alone = {}; for (const k of rig.order) { const c = cv([W, H]), g = c.getContext('2d'); for (const k2 of rig.order) { if (k2 === k) continue; const m2 = M[k2], q2 = rig.parts[k2]; g.setTransform(m2[0], m2[1], m2[2], m2[3], m2[4], m2[5]); g.drawImage(rig.img0[k2], -q2.pv[0], -q2.pv[1]); } alone[k] = g.getImageData(0, 0, W, H).data; }
    const near = (a, j, r) => { const x0 = j % W, y0 = (j / W) | 0; for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) { const X = x0 + dx, Y = y0 + dy; if (X >= 0 && Y >= 0 && X < W && Y < H && a[(Y * W + X) * 4 + 3] > 200) return true; } return false; };
    const pics = k => [k].concat(rig.swaps && rig.swaps[k] ? [...new Set(Object.values(rig.swaps[k]))].map(f => '@' + f) : []);
    for (const k of rig.order) {   /* back to front: what is under this piece = everything drawn before it */
      const q = rig.parts[k], m = M[k], under = cg.getImageData(0, 0, W, H).data;
      for (const key of pics(k)) { const im = rig.img0[key]; if (!im || !im.width) continue; const c = cv([im.width, im.height]), g = c.getContext('2d'); g.drawImage(im, 0, 0); const d = g.getImageData(0, 0, c.width, c.height), p = d.data, w = c.width, h = c.height;
        const edge = new Uint8Array(w * h); for (let i = 0; i < w * h; i++) edge[i] = p[i * 4 + 3] < 128 ? 0 : 255;   /* distance (in px, up to band) to the outside of the piece */
        const dist = new Uint8Array(w * h).fill(255); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = y * w + x; if (!edge[i]) { dist[i] = 0; continue; } let best = 255; for (let dy = -band; dy <= band && best > 1; dy++) for (let dx = -band; dx <= band; dx++) { const X = x + dx, Y = y + dy, o = X < 0 || Y < 0 || X >= w || Y >= h || !edge[Y * w + X]; if (o) { const dd = Math.max(Math.abs(dx), Math.abs(dy)); if (dd < best) best = dd; } } dist[i] = best; }
        let n = 0;
        for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = y * w + x; if (p[i * 4 + 3] < 8 || dist[i] > band) continue; const lx = x + .5 - q.pv[0], ly = y + .5 - q.pv[1], X = Math.floor(m[0] * lx + m[2] * ly + m[4]), Y = Math.floor(m[1] * lx + m[3] * ly + m[5]); if (X < 0 || Y < 0 || X >= W || Y >= H) continue;
          const j = Y * W + X; if (darkNear[j] || !(under[j * 4 + 3] >= 200 || (dist[i] <= 2 && near(alone[k], j, 3) && lum[j] > 90))) continue;   /* over another piece, or a cut edge right next to another piece */ p[i * 4] = ref[j * 4]; p[i * 4 + 1] = ref[j * 4 + 1]; p[i * 4 + 2] = ref[j * 4 + 2]; p[i * 4 + 3] = 255; n++; }
        g.putImageData(d, 0, 0); rig.img[key] = c; rig._seam = (rig._seam || 0) + n; }
      cg.setTransform(m[0], m[1], m[2], m[3], m[4], m[5]); cg.drawImage(rig.img0[k], -q.pv[0], -q.pv[1]); cg.setTransform(1, 0, 0, 1, 0, 0); }
  }
  function unseam(rig) { if (rig.img0) Object.assign(rig.img, rig.img0); rig.img0 = null; }

  /* BAKE = "ลบรอยต่อ" (owner 2026-11-28 "ลบรอยทำไมใช้ไม่ได้"): after the pieces are put together, every pixel of the reference picture's figure goes to the
     piece drawn on top there at rest (gaps go to the nearest piece), and that piece shows the reference's OWN colour there; elsewhere it keeps its own
     picture (hidden under other pieces at rest, it fills what opens when they move). So at rest the hero is the reference, pixel for pixel: no joint
     line, no gap, no piece sticking out past the outline. Works for any rig with a ref picture; rig.bake = true keeps it on (games get it on load).
     The pictures before are kept in rig.img0 (unseam = undo). Pieces that swap pictures (faces, fists) are left as they are. */
  function bake(rig, pad = 8) {
    const R = rig.img._ref; if (!R || !rig.order) return 0; if (rig.img0) unseam(rig); prep(rig); const [W, H] = rig.size, cv = (w, h) => { const e = document.createElement('canvas'); e.width = w; e.height = h; return [e, e.getContext('2d', { willReadFrequently: true })]; };
    const [rc, rg] = cv(W, H); rg.drawImage(R, 0, 0, W, H); const ref = rg.getImageData(0, 0, W, H).data; let fig = new Uint8Array(W * H), hasA = false;
    for (let i = 0; i < W * H; i++) if (ref[i * 4 + 3] < 250) { hasA = true; break; }
    if (hasA) for (let i = 0; i < W * H; i++) fig[i] = ref[i * 4 + 3] > 128 ? 1 : 0;
    else {   /* an opaque reference: the background = what is close to the border colours, reached from the border */
      const bc = []; for (let x = 0; x < W; x += 7) bc.push(x, (H - 1) * W + x); for (let y = 0; y < H; y += 7) bc.push(y * W, y * W + W - 1);
      const seen = new Uint8Array(W * H), q = bc.slice(); const near = (i, j) => Math.abs(ref[i * 4] - ref[j * 4]) + Math.abs(ref[i * 4 + 1] - ref[j * 4 + 1]) + Math.abs(ref[i * 4 + 2] - ref[j * 4 + 2]) < 40;
      for (const i of bc) seen[i] = 1; while (q.length) { const i = q.pop(), x = i % W, y = (i / W) | 0; for (const j of [x > 0 ? i - 1 : -1, x < W - 1 ? i + 1 : -1, y > 0 ? i - W : -1, y < H - 1 ? i + W : -1]) if (j >= 0 && !seen[j] && near(i, j)) { seen[j] = 1; q.push(j); } }
      for (let i = 0; i < W * H; i++) fig[i] = seen[i] ? 0 : 1; }
    const M = world(rig, {}, null), top = new Int16Array(W * H).fill(-1), keys = rig.order.filter(k => !(rig.swaps && rig.swaps[k]) && rig.parts[k].role !== 'weapon' && rig.parts[k].role !== 'weaponB');
    keys.forEach((k, idx) => { const [c, g] = cv(W, H), q = rig.parts[k], m = M[k]; g.setTransform(m[0], m[1], m[2], m[3], m[4], m[5]); g.drawImage(rig.img[k], -q.pv[0], -q.pv[1]); const d = g.getImageData(0, 0, W, H).data; for (let i = 0; i < W * H; i++) if (d[i * 4 + 3] > 128) top[i] = rig.order.indexOf(k); });
    /* figure pixels no piece covers: to the nearest covered pixel's piece (a few px) */
    const own = Int16Array.from(top); for (let pass = 0; pass < pad; pass++) { const nx = Int16Array.from(own); for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) { const i = y * W + x; if (own[i] >= 0 || !fig[i]) continue; for (const j of [i - 1, i + 1, i - W, i + W]) if (own[j] >= 0) { nx[i] = own[j]; break; } } own.set(nx); }
    rig.img0 = Object.assign({}, rig.img); let n = 0;
    for (const k of keys) {
      const q = rig.parts[k], im = rig.img0[k], ki = rig.order.indexOf(k), m = M[k], ox = pad + (((m[4] - q.pv[0]) % 1) + 1) % 1, oy = pad + (((m[5] - q.pv[1]) % 1) + 1) % 1, w = im.width + 2 * pad + 1, h = im.height + 2 * pad + 1, [c, g] = cv(w, h);
      g.drawImage(im, ox, oy); const d = g.getImageData(0, 0, w, h), p = d.data;   /* ox, oy: the new picture lands on whole screen pixels at rest (no blur) */
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const lx = x + .5 - ox - q.pv[0], ly = y + .5 - oy - q.pv[1], X = Math.floor(m[0] * lx + m[2] * ly + m[4]), Y = Math.floor(m[1] * lx + m[3] * ly + m[5]), o = (y * w + x) * 4;
        if (X < 0 || Y < 0 || X >= W || Y >= H) { p[o + 3] = 0; continue; } const j = Y * W + X;
        if (own[j] === ki) { p[o] = ref[j * 4]; p[o + 1] = ref[j * 4 + 1]; p[o + 2] = ref[j * 4 + 2]; p[o + 3] = 255; n++; }   /* this piece shows here at rest: the reference's own colour */
        else if (!fig[j] && top[j] === ki) p[o + 3] = 0; }   /* on top but outside the figure: cut off */
      g.putImageData(d, 0, 0); c._ox = ox; c._oy = oy; rig.img[k] = c; }   /* _off = the picture grew by pad on every side */
    rig._bakePad = pad; rig._baked = true; return n;
  }

  /* AUTOFIT (owner 2026-11-27 "ทำให้จัดกระดูก ภาพถูกต้อง ... ครอสชอบใส่ตัวละครบิดไม่ตรง"): every piece is turned / sized / moved a little until it lies best
     on the reference picture (rig.ref) at rest. At rest a piece is drawn at trs(at, r, s) whatever its parent, so each piece is fitted on its own.
     Search near the present place (coarse then fine), robust colour error so a part the reference hides under another does not pull it away.
     keys = pieces to fit (default all but hidden fillers / weapons). Returns { key: { before, after } } (mean colour error per channel, 0-255). */
  function autofit(rig, keys, opt) {
    opt = Object.assign({ shift: 16, turn: 14, size: .16 }, opt || {}); const R = rig.img._ref; if (!R) return {}; prep(rig);
    const [W, H] = rig.size, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(R, 0, 0, W, H); const ref = g.getImageData(0, 0, W, H).data, res = {};
    keys = keys || rig.order.filter(k => rig.parts[k].role !== 'none' && rig.parts[k].role !== 'weapon' && rig.parts[k].role !== 'weaponB');
    for (const k of keys) {
      const q = rig.parts[k], im = rig.img0 ? rig.img0[k] : rig.img[k]; if (!im || !im.width) continue; const pc = document.createElement('canvas'); pc.width = im.width; pc.height = im.height; const pg = pc.getContext('2d'); pg.drawImage(im, 0, 0); const d = pg.getImageData(0, 0, pc.width, pc.height).data;
      const pts = []; const step = Math.max(1, Math.round(Math.sqrt(im.width * im.height / 3500)));
      for (let y = 1; y < im.height - 1; y += step) for (let x = 1; x < im.width - 1; x += step) { const i = (y * im.width + x) * 4; if (d[i + 3] > 230 && d[i - 1] > 200 && d[i + 7] > 200) pts.push(x - q.pv[0], y - q.pv[1], d[i], d[i + 1], d[i + 2]); }
      const n = pts.length / 5; if (n < 20) continue;
      const err = (ax, ay, r, s) => { const cs = Math.cos(r * D2R) * s * (q.fx ? -1 : 1), sn = Math.sin(r * D2R) * s, cy = Math.cos(r * D2R) * s; let e = 0, m = 0;
        for (let p = 0; p < pts.length; p += 5) { const lx = pts[p], ly = pts[p + 1], X = Math.round(cs * lx - sn * ly + ax), Y = Math.round((q.fx ? -sn : sn) * lx * (q.fx ? -1 : 1) + cy * ly + ay); if (X < 0 || Y < 0 || X >= W || Y >= H) { e += 60; m++; continue; } const j = (Y * W + X) * 4;
          e += Math.min(60, (Math.abs(ref[j] - pts[p + 2]) + Math.abs(ref[j + 1] - pts[p + 3]) + Math.abs(ref[j + 2] - pts[p + 4])) / 3); m++; } return e / m; };
      const before = err(q.at[0], q.at[1], q.r || 0, q.s); let best = [before, q.at[0], q.at[1], q.r || 0, q.s];
      const search = (cx, cy, cr, cs_, sh, shStep, tr, trStep, sz, szStep) => { let b = null; for (let r = cr - tr; r <= cr + tr + 1e-6; r += trStep) for (let s = cs_ * (1 - sz); s <= cs_ * (1 + sz) + 1e-6; s += cs_ * szStep) for (let dy = -sh; dy <= sh; dy += shStep) for (let dx = -sh; dx <= sh; dx += shStep) { const e = err(cx + dx, cy + dy, r, s); if (!b || e < b[0]) b = [e, cx + dx, cy + dy, r, s]; } return b; };
      let b = search(q.at[0], q.at[1], q.r || 0, q.s, opt.shift, 4, opt.turn, 3.5, opt.size, .04); if (b[0] < best[0]) best = b;
      b = search(best[1], best[2], best[3], best[4], 4, 1, 3, 1, .04, .01); if (b[0] < best[0]) best = b;
      b = search(best[1], best[2], best[3], best[4], 1, .5, 1, .5, .01, .005); if (b[0] < best[0]) best = b;
      if (best[0] < before - .3) { q.at = [Math.round(best[1] * 10) / 10, Math.round(best[2] * 10) / 10]; q.r = Math.round(best[3] * 10) / 10; q.s = Math.round(best[4] * 1000) / 1000; }
      res[k] = { before: +before.toFixed(1), after: +Math.min(before, best[0]).toFixed(1) }; }
    prep(rig); return res;
  }
  /* SEAMS IN MOVES: for every move, the share of the figure where a thin gap (no wider than 4 px) opens between exactly two joined pieces (a seam).
     Returns { move: { worst: 0..1, at: seconds } }. Used by the tool's "ตรวจ" button and by tools/qa/rig_check.js. */
  /* MESH = how Spine bends a picture (owner 2026-11-28 "ถ้าไม่แยกใส่กระดูกได้ไหม", "Spine 2D ทำงานแบบไหน ... เอามาทำของเรา").
     Every picture gets a triangle grid; every grid point follows one or more bones by WEIGHTS, so round a joint the two sides bend together like skin
     instead of turning as two stiff cards (no crack, no hinge line, an elbow / waist / neck curves).
     rig.mesh = { mode: 'pieces' = every piece is a mesh: round its own turning point it also follows its parent, round a child's turning point also that child
                       | 'one' = the WHOLE front picture (rig.ref), NOT cut at all: each point follows the bone whose area it lies in at rest, smoothed over `soft`
                         (fine for bends and breathing; where one part lies over another in the picture there is nothing behind it, so big moves stretch),
                  step: grid px (12), soft: joint blend radius px (18), blend: the other bone's share right at the joint (.5) }.
     Drawn with WebGL on one small hidden canvas shared by every rig and copied onto the game's canvas, so it costs about what plain pieces cost;
     without WebGL the pieces are drawn stiff as before. Weapons stay stiff. rig._meshShow = true draws the grid (orange = points that blend bones). */
  const fall = (d, s) => { const t = Math.min(1, d / s); return 1 - t * t * (3 - 2 * t); };
  const NOKID = { weapon: 1, weaponB: 1, none: 1, hair: 1, cape: 1, tail: 1, wing: 1 };   /* a body does not bend toward its swinging hair / cape or a hidden filler */
  function meshOpt(rig) { return Object.assign({ mode: 'pieces', step: 12, soft: 18, blend: .5 }, rig.mesh === true ? {} : rig.mesh || {}); }
  function meshSig(rig) { let s = ''; for (const k of rig.order) { const q = rig.parts[k]; s += k + q.p + q.at + q.pv + q.r + q.s + q.fx + q.role + '|'; } return s + JSON.stringify(rig.mesh) + rig._feet; }
  function meshMake(rig) {
    prep(rig); const o = meshOpt(rig), M0 = world(rig, {}, null), inv0 = {}; for (const k in M0) inv0[k] = inv(M0[k]);
    rig._mesh = { o, M0, inv0, sig: meshSig(rig), gen: (rig._mesh ? rig._mesh.gen : 0) + 1, one: o.mode === 'one' && rig.img._ref ? meshOne(rig, o, M0) : null }; return rig._mesh;
  }
  function meshGrid(W, H, st, has) {   /* cells of about st px over a W x H picture; triangles only on cells with something drawn in them */
    const nx = Math.max(2, Math.ceil(W / st) + 1), ny = Math.max(2, Math.ceil(H / st) + 1), sx = W / (nx - 1), sy = H / (ny - 1), occ = new Uint8Array((nx - 1) * (ny - 1));
    if (!has) occ.fill(1); else for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (has(x, y)) occ[Math.min(ny - 2, (y / sy) | 0) * (nx - 1) + Math.min(nx - 2, (x / sx) | 0)] = 1;
    const id = new Int32Array(nx * ny).fill(-1), u = [], v = [], tri = [], vid = (i, j) => { const n = j * nx + i; if (id[n] < 0) { id[n] = u.length; u.push(i * sx); v.push(j * sy); } return id[n]; };
    for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) if (occ[j * (nx - 1) + i]) { const a = vid(i, j), b = vid(i + 1, j), c = vid(i, j + 1), d = vid(i + 1, j + 1); tri.push(a, b, c, b, d, c); }
    return { u, v, tri: Uint16Array.from(tri) };
  }
  const alphaOf = im => { const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(im, 0, 0); return g.getImageData(0, 0, im.width, im.height).data; };
  function meshPiece(rig, k, im) {   /* one piece's picture as a mesh, weights to itself, its parent (round its turning point) and its children (round theirs) */
    const M = rig._mesh, o = M.o, q = rig.parts[k], W = im.width, H = im.height, rigid = q.role === 'weapon' || q.role === 'weaponB', m0 = M.M0[k];
    const al = rigid ? null : alphaOf(im), G = meshGrid(W, H, rigid ? 1e9 : o.step, al && ((x, y) => al[(y * W + x) * 4 + 3] > 8));
    const par = !rigid && q.p && rig.parts[q.p] && q.p !== k ? q.p : null, kids = rigid ? [] : Object.keys(rig.parts).filter(c => c !== k && rig.parts[c].p === k && !NOKID[rig.parts[c].role]);
    const bones = [k].concat(par ? [par] : [], kids), n = G.u.length, rx = new Float32Array(n), ry = new Float32Array(n), uv = new Float32Array(n * 2), wb = [], ww = [], ox = q.pv[0] + (im._ox || 0), oy = q.pv[1] + (im._oy || 0);
    for (let i = 0; i < n; i++) { const lx = G.u[i] - ox, ly = G.v[i] - oy, X = m0[0] * lx + m0[2] * ly + m0[4], Y = m0[1] * lx + m0[3] * ly + m0[5]; rx[i] = X; ry[i] = Y; uv[i * 2] = G.u[i] / W; uv[i * 2 + 1] = G.v[i] / H;
      const b = [0], w = [1]; if (!rigid) { let s = 0; const add = (bi, J) => { const f = o.blend * fall(Math.hypot(X - J[4], Y - J[5]), o.soft); if (f > .01) { b.push(bi); w.push(f); s += f; } };
        if (par) add(1, m0); kids.forEach((c, j) => add(1 + (par ? 1 : 0) + j, M.M0[c])); w[0] = Math.max(.2, 1 - s); const t = w.reduce((a, e) => a + e, 0); for (let j = 0; j < w.length; j++) w[j] /= t; }
      wb.push(b); ww.push(w); }
    return { k, gen: M.gen, bones, rx, ry, uv, tri: G.tri, wb, ww };
  }
  function meshOne(rig, o, M0) {   /* the whole reference picture as ONE mesh. Which bone each spot follows = which piece covers it at rest (rig.parts only say
       where the bones are and which area is whose; their pictures are not drawn). Round a joint a spot also follows the bone on the other side (like 'pieces').
       Where two areas meet away from a joint (an arm lying over the skirt) the sheet is TORN, so the arm lifts off instead of dragging the skirt with it. */
    const R = rig.img._ref, [W, H] = rig.size, top = k => { while (k && rig.parts[k] && rig.parts[k].role === 'none' && rig.parts[k].p) k = rig.parts[k].p; return k; };
    const bones = [...new Set(rig.order.filter(k => !/weapon/.test(rig.parts[k].role) && !(rig.swaps && rig.swaps[k])).map(top))], bi = Object.fromEntries(bones.map((k, i) => [k, i])), own = new Int16Array(W * H).fill(-1);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d', { willReadFrequently: true });
    const cov = new Uint8Array(W * H); for (const k of rig.order) { if (/weapon/.test(rig.parts[k].role)) continue; const q = rig.parts[k], im = (rig.img0 && rig.img0[k]) || rig.img[k], b = top(k) in bi ? bi[top(k)] : -1; g.clearRect(0, 0, W, H); g.setTransform(...M0[k]); g.drawImage(im, -q.pv[0] - (im._ox || 0), -q.pv[1] - (im._oy || 0)); g.setTransform(1, 0, 0, 1, 0, 0);
      const d = g.getImageData(0, 0, W, H).data; for (let i = 0; i < W * H; i++) if (d[i * 4 + 3] > 128) { cov[i] = 1; if (b >= 0) own[i] = b; } }
    for (let pass = 0; pass < 3; pass++) { const n = Uint8Array.from(cov); for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) { const i = y * W + x; if (!cov[i] && (cov[i - 1] || cov[i + 1] || cov[i - W] || cov[i + W])) n[i] = 1; } cov.set(n); }
    let tex; { const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(R, 0, 0, W, H); const d = g.getImageData(0, 0, W, H), mc = document.createElement('canvas'); mc.width = W; mc.height = H; const mg = mc.getContext('2d', { willReadFrequently: true }); if (rig.img._refMask) mg.drawImage(rig.img._refMask, 0, 0, W, H);
      const md = mg.getImageData(0, 0, W, H).data; for (let i = 0; i < W * H; i++) d.data[i * 4 + 3] = Math.min(d.data[i * 4 + 3], rig.img._refMask ? (md[i * 4 + 3] < 250 ? md[i * 4 + 3] : md[i * 4]) : 255) * (cov[i] ? 1 : 0); g.putImageData(d, 0, 0); tex = c; }   /* the picture only where the pieces are at rest (+3 px), and inside rig.refMask when the reference is opaque: no background, no stray bits */
    for (let pass = 0; pass < 24; pass++) for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) { const i = y * W + x; if (own[i] >= 0) continue; for (const j of [i - 1, i + 1, i - W, i + W]) if (own[j] >= 0) { own[i] = own[j]; break; } }
    const J = b => M0[bones[b]], parOf = b => { const p = top(rig.parts[bones[b]].p); return p in bi && bi[p] !== b ? bi[p] : -1; }, kidsOf = bones.map((_, b) => bones.map((_, c) => c).filter(c => c !== b && parOf(c) === b && !NOKID[rig.parts[bones[c]].role]));
    const ownAt = (x, y) => { for (let r = 0; r <= o.step * 2; r += 2) for (const [dx, dy] of [[0, 0], [r, 0], [-r, 0], [0, r], [0, -r], [r, r], [-r, -r], [r, -r], [-r, r]]) { const X = Math.round(x + dx), Y = Math.round(y + dy); if (X >= 0 && Y >= 0 && X < W && Y < H && own[Y * W + X] >= 0) return own[Y * W + X]; } return 0; };
    const wfun = (x, y, b) => { const l = [[b, 1]]; let s = 0; const add = (c, m) => { const f = o.blend * fall(Math.hypot(x - m[4], y - m[5]), o.soft); if (f > .01) { l.push([c, f]); s += f; } }; const p = parOf(b); if (p >= 0) add(p, J(b)); for (const c of kidsOf[b]) add(c, J(c));
      l[0][1] = Math.max(.2, 1 - s); const t = l.reduce((a, e) => a + e[1], 0); return [l.map(e => e[0]), l.map(e => e[1] / t)]; };
    const al = alphaOf(tex), G = meshGrid(W, H, o.step, (x, y) => al[(y * W + x) * 4 + 3] > 8), rx = [], ry = [], uv = [], wb = [], ww = [], vb = [], cut = [], tri = [];
    const vert = (x, y, b, c) => { const [l, w] = wfun(x, y, b); rx.push(x); ry.push(y); uv.push(x / W, y / H); wb.push(l); ww.push(w); vb.push(b); cut.push(c); return rx.length - 1; };
    const base = G.u.map((x, i) => vert(x, G.v[i], ownAt(x, G.v[i]), -1)); void base;
    const ok = (a, b, cx, cy) => { if (a === b) return true; const ch = parOf(b) === a ? b : parOf(a) === b ? a : -1; if (ch < 0) return false; const m = J(ch); return Math.hypot(cx - m[4], cy - m[5]) < o.soft * 1.3; };
    for (let t = 0; t < G.tri.length; t += 3) { const v = [G.tri[t], G.tri[t + 1], G.tri[t + 2]], cx = (rx[v[0]] + rx[v[1]] + rx[v[2]]) / 3, cy = (ry[v[0]] + ry[v[1]] + ry[v[2]]) / 3, B = v.map(i => vb[i]);
      if (ok(B[0], B[1], cx, cy) && ok(B[1], B[2], cx, cy) && ok(B[0], B[2], cx, cy)) tri.push(...v);
      else { const S = new Set(B); for (const [p, q2] of [[.33, .33], [.6, .2], [.2, .6], [.2, .2], [.5, .5], [0, .5], [.5, 0], [.1, .1], [.8, .1], [.1, .8]]) { const r = 1 - p - q2; S.add(ownAt(rx[v[0]] * r + rx[v[1]] * p + rx[v[2]] * q2, ry[v[0]] * r + ry[v[1]] * p + ry[v[2]] * q2)); }
        for (const b of S) tri.push(...v.map(i => vert(rx[i], ry[i], b, b))); } }   /* torn: one copy of the triangle per area in it, each showing only its own area's pixels (cut exactly on the pixel line, not on the grid) */
    const oc = document.createElement('canvas'); oc.width = W; oc.height = H; const og = oc.getContext('2d'), od = og.createImageData(W, H); for (let i = 0; i < W * H; i++) { od.data[i * 4] = own[i] + 1; od.data[i * 4 + 3] = 255; } og.putImageData(od, 0, 0);   /* whose area each pixel is, for the cut */
    return { k: '_ref', tex, own: oc, bones, rx: Float32Array.from(rx), ry: Float32Array.from(ry), uv: Float32Array.from(uv), cut: Float32Array.from(cut), tri: Uint16Array.from(tri), wb, ww };
  }
  let GLR = null;
  function glr() {   /* the shared WebGL drawer (false when the browser has none) */
    if (GLR !== null) return GLR; GLR = false;
    try { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('webgl', { premultipliedAlpha: true, preserveDrawingBuffer: true, antialias: false, alpha: true }); if (!g) return GLR;
      const sh = (t, s) => { const o = g.createShader(t); g.shaderSource(o, s); g.compileShader(o); return o; }, pr = g.createProgram();
      g.attachShader(pr, sh(g.VERTEX_SHADER, 'attribute vec4 a;attribute float b;uniform vec2 S;varying vec2 t;varying float c;void main(){t=a.zw;c=b;gl_Position=vec4(a.x/S.x*2.-1.,1.-a.y/S.y*2.,0.,1.);}'));
      g.attachShader(pr, sh(g.FRAGMENT_SHADER, 'precision mediump float;uniform sampler2D T;uniform sampler2D O;uniform float A;varying vec2 t;varying float c;void main(){if(c>-.5&&abs(texture2D(O,t).r*255.-c-1.)>.5)discard;gl_FragColor=texture2D(T,t)*A;}'));
      g.linkProgram(pr); if (!g.getProgramParameter(pr, g.LINK_STATUS)) return GLR; g.useProgram(pr);
      const vb = g.createBuffer(), ib = g.createBuffer(); g.bindBuffer(g.ARRAY_BUFFER, vb); g.bindBuffer(g.ELEMENT_ARRAY_BUFFER, ib); const la = g.getAttribLocation(pr, 'a'), lb = g.getAttribLocation(pr, 'b'); g.enableVertexAttribArray(la); g.enableVertexAttribArray(lb); g.uniform1i(g.getUniformLocation(pr, 'T'), 0); g.uniform1i(g.getUniformLocation(pr, 'O'), 1);
      g.enable(g.BLEND); g.blendFunc(g.ONE, g.ONE_MINUS_SRC_ALPHA); g.enable(g.SCISSOR_TEST); g.pixelStorei(g.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
      GLR = { c, g, la, lb, S: g.getUniformLocation(pr, 'S'), A: g.getUniformLocation(pr, 'A'), tex: new WeakMap() };
    } catch (e) { GLR = false; } return GLR;
  }
  function meshRender(rig, P, ctx, V, fade) {   /* true = drawn as meshes (the caller skips the stiff pieces) */
    const R = glr(); if (!R) return false; let M = rig._mesh; if (!M || M.sig !== meshSig(rig)) M = meshMake(rig);
    const T = {}, tb = b => T[b] || (T[b] = mul(V, mul(P.mats[b], M.inv0[b]))), items = [];
    if (M.one) items.push({ m: M.one, im: M.one.tex, a: fade == null ? 1 : fade });
    for (const k of P.order()) { const q = rig.parts[k]; if (M.one && !/weapon/.test(q.role) && !(rig.swaps && rig.swaps[k])) continue;   /* one picture: only weapons and swapping pieces (faces, fists) are drawn on it */ const a = (P.pose[k] && P.pose[k].a != null ? P.pose[k].a : 1) * (fade == null ? 1 : fade); if (a <= .01) continue;
      const im = P.image(k); if (!im || !im.width) continue; let m = im._mesh; if (!m || m.k !== k || m.gen !== M.gen) m = im._mesh = meshPiece(rig, k, im); items.push({ m, im, a }); }
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9, nv = 0, ni = 0;
    for (const it of items) { const m = it.m, n = m.rx.length, xy = it.xy = new Float32Array(n * 2); for (let i = 0; i < n; i++) { let x = 0, y = 0; const b = m.wb[i], w = m.ww[i], X = m.rx[i], Y = m.ry[i];
        for (let j = 0; j < b.length; j++) { const t = tb(m.bones[b[j]]); x += w[j] * (t[0] * X + t[2] * Y + t[4]); y += w[j] * (t[1] * X + t[3] * Y + t[5]); }
        xy[i * 2] = x; xy[i * 2 + 1] = y; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } nv += n; ni += m.tri.length; }
    const cw = ctx.canvas.width, ch = ctx.canvas.height, bx = Math.max(0, Math.floor(x0) - 2), by = Math.max(0, Math.floor(y0) - 2), w = Math.min(cw, Math.ceil(x1) + 2) - bx, h = Math.min(ch, Math.ceil(y1) + 2) - by;
    P._meshItems = items; if (w <= 0 || h <= 0) return true; const g = R.g, c = R.c;
    if (c.width < w || c.height < h) { c.width = Math.max(c.width, Math.ceil(w / 256) * 256); c.height = Math.max(c.height, Math.ceil(h / 256) * 256); g.enable(g.SCISSOR_TEST); }
    const vd = new Float32Array(nv * 5), id = new Uint16Array(ni); let vo = 0, io = 0;
    for (const it of items) { const m = it.m, n = m.rx.length; it.vo = vo; it.io = io; for (let i = 0; i < n; i++) { const o5 = (vo + i) * 5; vd[o5] = it.xy[i * 2] - bx; vd[o5 + 1] = it.xy[i * 2 + 1] - by; vd[o5 + 2] = m.uv[i * 2]; vd[o5 + 3] = m.uv[i * 2 + 1]; vd[o5 + 4] = m.cut ? m.cut[i] : -1; } id.set(m.tri, io); vo += n; io += m.tri.length; }
    g.viewport(0, c.height - h, w, h); g.scissor(0, c.height - h, w, h); g.clearColor(0, 0, 0, 0); g.clear(g.COLOR_BUFFER_BIT); g.uniform2f(R.S, w, h);
    g.bufferData(g.ARRAY_BUFFER, vd, g.STREAM_DRAW); g.bufferData(g.ELEMENT_ARRAY_BUFFER, id, g.STREAM_DRAW); const smooth = ctx.imageSmoothingEnabled !== false ? g.LINEAR : g.NEAREST;
    const texOf = (im, f) => { let t = R.tex.get(im); if (!t) { t = g.createTexture(); g.bindTexture(g.TEXTURE_2D, t); for (const [p, v] of [[g.TEXTURE_WRAP_S, g.CLAMP_TO_EDGE], [g.TEXTURE_WRAP_T, g.CLAMP_TO_EDGE]]) g.texParameteri(g.TEXTURE_2D, p, v); g.texImage2D(g.TEXTURE_2D, 0, g.RGBA, g.RGBA, g.UNSIGNED_BYTE, im); R.tex.set(im, t); } else g.bindTexture(g.TEXTURE_2D, t);
      if (t._f !== f) { g.texParameteri(g.TEXTURE_2D, g.TEXTURE_MIN_FILTER, f); g.texParameteri(g.TEXTURE_2D, g.TEXTURE_MAG_FILTER, f); t._f = f; } return t; };
    for (const it of items) { g.activeTexture(g.TEXTURE1); if (it.m.own) { g.pixelStorei(g.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false); texOf(it.m.own, g.NEAREST); g.pixelStorei(g.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true); } g.activeTexture(g.TEXTURE0); texOf(it.im, smooth);
      g.vertexAttribPointer(R.la, 4, g.FLOAT, false, 20, it.vo * 20); g.vertexAttribPointer(R.lb, 1, g.FLOAT, false, 20, it.vo * 20 + 16); g.uniform1f(R.A, it.a); g.drawElements(g.TRIANGLES, it.m.tri.length, g.UNSIGNED_SHORT, it.io * 2); }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(c, 0, 0, w, h, bx, by, w, h);
    if (rig._meshShow) { ctx.globalAlpha = 1; ctx.lineWidth = 1; for (const it of items) { const m = it.m, xy = it.xy; ctx.strokeStyle = '#ffffff55'; ctx.beginPath(); for (let t = 0; t < m.tri.length; t += 3) { const a = m.tri[t], b = m.tri[t + 1], d = m.tri[t + 2]; ctx.moveTo(xy[a * 2], xy[a * 2 + 1]); ctx.lineTo(xy[b * 2], xy[b * 2 + 1]); ctx.lineTo(xy[d * 2], xy[d * 2 + 1]); ctx.closePath(); } ctx.stroke();
        for (let i = 0; i < m.rx.length; i++) if (m.ww[i].length > 1) { const s = 1 - m.ww[i][0]; ctx.fillStyle = `rgba(255,${160 - s * 160 | 0},40,${.4 + s})`; ctx.fillRect(xy[i * 2] - 2, xy[i * 2 + 1] - 2, 4, 4); } } }
    ctx.restore(); return true;
  }
  function figOf(rig) {   /* the figure of the reference picture (rig.size space): its alpha, or what differs from the border colours */
    if (rig._fig !== undefined) return rig._fig; const R = rig.img._ref; if (!R) return rig._fig = null; const [W, H] = rig.size, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(R, 0, 0, W, H); const a = g.getImageData(0, 0, W, H).data, d = new Uint8Array(W * H);
    let hasA = false; for (let i = 0; i < W * H; i++) if (a[i * 4 + 3] < 250) { hasA = true; break; }
    if (hasA) for (let i = 0; i < W * H; i++) d[i] = a[i * 4 + 3] > 128 ? 1 : 0; else { const b0 = [a[0], a[1], a[2]]; for (let i = 0; i < W * H; i++) d[i] = Math.abs(a[i * 4] - b0[0]) + Math.abs(a[i * 4 + 1] - b0[1]) + Math.abs(a[i * 4 + 2] - b0[2]) > 40 ? 1 : 0; }
    return rig._fig = { w: W, h: H, d };
  }
  function seams(rig, moves) {
    prep(rig); const w = rig.size[0], h = rig.size[1], out = {}, cv = () => { const c = document.createElement('canvas'); c.width = w * 2; c.height = h * 1.6; return [c, c.getContext('2d', { willReadFrequently: true })]; };
    const crack = P => { const [c, g] = cv(); P.draw(g, w, h * 1.4, 1, false); g.setTransform(1, 0, 0, 1, 0, 0); const d = g.getImageData(0, 0, c.width, c.height), a = d.data, W2 = d.width, H2 = d.height, seen = new Uint8Array(W2 * H2), q = []; let fig = 0;
      for (let i = 0; i < W2 * H2; i++) if (a[i * 4 + 3] > 60) fig++; for (let x = 0; x < W2; x++) q.push(x, (H2 - 1) * W2 + x); for (let y = 0; y < H2; y++) q.push(y * W2, y * W2 + W2 - 1);
      while (q.length) { const i = q.pop(); if (seen[i] || a[i * 4 + 3] > 60) continue; seen[i] = 1; const x = i % W2, y = (i / W2) | 0; if (x > 0) q.push(i - 1); if (x < W2 - 1) q.push(i + 1); if (y > 0) q.push(i - W2); if (y < H2 - 1) q.push(i + W2); }
      const opaqueNear = i => { const x = i % W2, y = (i / W2) | 0; for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) { const X = x + dx, Y = y + dy; if (X >= 0 && Y >= 0 && X < W2 && Y < H2 && a[(Y * W2 + X) * 4 + 3] > 60) return true; } return false; };
      let masks = null, hole = 0; const lab = new Uint8Array(W2 * H2);
      for (let i = 0; i < W2 * H2; i++) { if (seen[i] || a[i * 4 + 3] > 60 || lab[i]) continue; const st = [i], comp = []; lab[i] = 1; let wide = false; while (st.length) { const j = st.pop(); comp.push(j); if (!wide && !opaqueNear(j)) wide = true; const x = j % W2, y = (j / W2) | 0; for (const k of [x > 0 ? j - 1 : -1, x < W2 - 1 ? j + 1 : -1, y > 0 ? j - W2 : -1, y < H2 - 1 ? j + W2 : -1]) if (k >= 0 && !lab[k] && !seen[k] && a[k * 4 + 3] <= 60) { lab[k] = 1; st.push(k); } }
        if (wide || P.clip || !P.view) continue;
        if (!masks) { masks = {}; for (const k of rig.order) { if ((P.pose[k] && P.pose[k].a != null ? P.pose[k].a : 1) < .05) continue; const [c2, g2] = cv(), qq = rig.parts[k]; g2.setTransform(...mul(P.view, P.mats[k])); g2.drawImage(P.image(k), -qq.pv[0], -qq.pv[1]); masks[k] = g2.getImageData(0, 0, c2.width, c2.height).data; } }
        const near = new Set(); for (const j of comp) { const x = j % W2, y = (j / W2) | 0; for (const k in masks) { if (near.has(k)) continue; const mk = masks[k]; for (let dy = -3; dy <= 3 && !near.has(k); dy++) for (let dx = -3; dx <= 3; dx++) { const X = x + dx, Y = y + dy; if (X >= 0 && Y >= 0 && X < W2 && Y < H2 && mk[(Y * W2 + X) * 4 + 3] > 60) { near.add(k); break; } } } }
        const top = k => { while (k && rig.parts[k] && rig.parts[k].role === 'none' && rig.parts[k].p) k = rig.parts[k].p; return k; }, ns = [...new Set([...near].map(top))];
        if (!(ns.length === 2 && (rig.parts[ns[0]].p === ns[1] || rig.parts[ns[1]].p === ns[0]))) continue;
        /* a gap the DRAWING has (background between an arm and the body) is not a seam: map the gap back to the rest pose through each of the two pieces;
           it is a seam only if, at rest, that spot was inside the figure of the reference */
        const fig = figOf(rig); if (fig) { const ox = P.view[4], oy = P.view[5]; let inside = 0, n2 = 0;
          for (let c = 0; c < comp.length; c += Math.max(1, (comp.length / 24) | 0)) { const j = comp[c], X = j % W2 - ox, Y = ((j / W2) | 0) - oy; n2++;
            for (const k of ns) { const l = pt(inv(P.mats[k]), X, Y), r = pt(REST0[k], l[0], l[1]), rx = Math.round(r[0]), ry = Math.round(r[1]); if (rx >= 0 && ry >= 0 && rx < fig.w && ry < fig.h && fig.d[ry * fig.w + rx]) { inside++; break; } } }
          if (inside < n2 * .3) continue; }
        hole += comp.length; }
      return hole / Math.max(1, fig); };
    const P0 = player(rig, { base: null }); P0.mats = world(rig, {}, null); const REST0 = P0.mats; const base = crack(P0);
    for (const mv of moves || Object.keys(MOVES).concat(Object.keys(rig.clips || {}))) { if (rig.view === 'front' && (mv === 'walk' || mv === 'run')) continue; const P = player(rig, { base: null }); P.play(mv); const dur = (MOVES[mv] && MOVES[mv].dur) || (rig.clips && rig.clips[mv] && rig.clips[mv].dur) || 1; let worst = 0, at = 0;
      for (let t = 0; t < dur; t += 1 / 15) { P.update(1 / 15); const k = crack(P) - base; if (k > worst) { worst = k; at = t; } } out[mv] = { worst, at: +at.toFixed(2) }; }
    return out;
  }
  /* how well the rest pose matches the reference: mean colour error (0-255) of every visible piece pixel, and per piece */
  function restScore(rig) {
    const R = rig.img._ref; if (!R) return null; prep(rig); const [W, H] = rig.size, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(R, 0, 0, W, H); const ref = g.getImageData(0, 0, W, H).data;
    const P = player(rig, { base: null }); P.mats = world(rig, {}, null); P.pose = {}; for (const k in rig.parts) if (rig.parts[k].role === 'weapon' || rig.parts[k].role === 'weaponB') P.pose[k] = { a: 0 }; g.clearRect(0, 0, W, H); P.draw(g, rig.feet[0], rig.feet[1], 1, false);   /* a weapon not in the reference does not count */ g.setTransform(1, 0, 0, 1, 0, 0); const d = g.getImageData(0, 0, W, H).data; let e = 0, n = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 240) { n++; e += (Math.abs(d[i] - ref[i]) + Math.abs(d[i + 1] - ref[i + 1]) + Math.abs(d[i + 2] - ref[i + 2])) / 3; } return n ? e / n : 0;
  }

  function player(rig, opt) {
    opt = opt || {}; const P = { rig, base: opt.base === undefined ? 'idle' : opt.base, pop: opt.pop == null ? 1 : opt.pop, speed: 1, move: null, name: '', t: 0, done: false, pose: {}, root: Object.assign({}, REST), roles: {}, from: null, fade: 0, sw: {}, mats: null, alpha: 1 };
    const tmp = {};
    P.play = (name, o) => { const cl = rig.clips && rig.clips[name]; if (cl) { o = o || {}; P.clip = cl; P.clipName = name; if (P.name !== name || o.restart || P.done) { P.t = 0; P.done = false; } P.name = name; P.move = { dur: cl.dur, ev: cl.ev, clip: 1 }; P.cf = 0; return P; }
      P.clip = null; const mv = MOVES[name]; if (!mv) return P; o = o || {}; if (P.move && P.name !== name || o.restart) { P.from = { pose: JSON.parse(JSON.stringify(P.pose)), root: Object.assign({}, P.root) }; P.fade = o.fade == null ? .07 : o.fade; P.fadeT = 0; }
      if (P.name !== name || o.restart || P.done) { P.t = 0; P.done = false; } P.move = mv; P.name = name; if (o.speed) P.speed = o.speed; return P; };
    P.fired = []; P.update = dt => { if (!P.move) return; const mv = P.move, t0 = P.t; P.t += dt * P.speed; P.fired = [];
      if (P.clip) { const c = P.clip; for (const [u, nm] of c.ev || []) { const te = u * c.dur; if (t0 < te && P.t >= te) P.fired.push(nm); } if (P.cf > 0) P.cf -= dt;
        if (P.t >= c.dur) { P.done = true; if (P.base && MOVES[P.base]) { const left = P.t - c.dur; P.clip = null; P.play(P.base, { fade: 0 }); P.t = left; P.fromClip = 0; } else P.t = c.dur - 1e-6; }
        if (P.clip) { let t = P.t * 1000, i = 0; while (i < c.durs.length - 1 && t >= c.durs[i]) { t -= c.durs[i]; i++; } P.frame = i; if (!P.mats) P.mats = world(rig, {}, null); return; } }
      if (mv.ev && mv.dur) for (const [u, nm] of mv.ev) { const te = u * mv.dur; if (t0 < te && P.t >= te || (dt === 0 && false)) P.fired.push(nm); }   /* move events (the bolt leaves the hand ...) crossed this frame */
      if (!mv.fn && P.t >= mv.dur) { if (mv.hold) { P.t = mv.dur; P.done = true; } else if (mv.loop) P.t %= mv.dur; else { P.done = true; if (P.base && MOVES[P.base]) { const left = P.t - mv.dur; P.play(P.base, { fade: .1 }); P.t = left; } else P.t = mv.dur; } }
      sample(P.move, P.t, tmp); P.roles = tmp; const pop = P.pop, pose = P.pose; for (const k in pose) delete pose[k];
      const fl = rig.flip ? -1 : 1, front = rig.view === 'front'; for (const k in rig.parts) { const ro = rig.parts[k].role, o = ro && tmp[ro]; if (!o) continue; const far = ro === 'armB' || ro === 'foreB' || ro === 'weaponB', sg = front && far ? -fl : fl, q = pose[k] = { r: o.r * sg * (rig.parts[k].g == null ? 1 : rig.parts[k].g), x: o.x * fl, y: o.y, sx: o.sx, sy: o.sy, a: o.a == null ? 1 : o.a, z: (o.z || 0) > 1.5 ? o.z : !rig.zfront || (far && !front) ? 0 : o.z || 0 };   /* z 2 = in front whatever the rig says (a move that needs it, like the bow pull) */ if (pop !== 1 && (ro === 'head' || ro === 'body' || ro === 'weapon')) { q.sx = 1 + (q.sx - 1) * pop; q.sy = 1 + (q.sy - 1) * pop; } }
      const r0 = tmp._root ? tmp._root : REST; for (const c in REST) P.root[c] = r0[c] == null ? REST[c] : r0[c]; if (fl < 0) { P.root.r = -P.root.r; P.root.x = -P.root.x; }
      if (P.from) { P.fadeT += dt; const f = P.fade > 0 ? Math.min(1, P.fadeT / P.fade) : 1; if (f >= 1) P.from = null; else { for (const k in rig.parts) { const a = P.from.pose[k] || REST, b = pose[k] || (pose[k] = Object.assign({}, REST)); for (const c of ['r', 'x', 'y', 'sx', 'sy', 'a']) b[c] = (a[c] == null ? 1 : a[c]) + ((b[c] == null ? 1 : b[c]) - (a[c] == null ? 1 : a[c])) * f; } for (const c in REST) P.root[c] = P.from.root[c] + (P.root[c] - P.from.root[c]) * f; } }
      /* hair / cape / tail: a spring thrown by how fast their turning point moves */
      let mats = world(rig, pose, P.root); const h = Math.min(dt, .05);
      for (const k in rig.parts) { const sp = SWING[rig.parts[k].role]; if (!sp) continue; const m = mats[k], s = P.sw[k] || (P.sw[k] = { a: 0, v: 0, x: m[4], y: m[5] }); const vx = (m[4] - s.x) / Math.max(h, 1e-3), vy = (m[5] - s.y) / Math.max(h, 1e-3); s.x = m[4]; s.y = m[5];
        const im = rig.img && rig.img[k], lx = (im ? im.width / 2 : 0) - rig.parts[k].pv[0], ly = (im ? im.height / 2 : 40) - rig.parts[k].pv[1], dx = m[0] * lx + m[2] * ly, dy = m[1] * lx + m[3] * ly, dl = Math.hypot(dx, dy) || 1;   /* which way the piece hangs from its turning point: it lags behind the motion */
        const push = Math.max(-900, Math.min(900, (dy * vx - dx * vy) / dl * sp[2] / rig._u)); s.v += (-sp[0] * s.a - sp[1] * s.v + push * 6) * h; s.a = Math.max(-55, Math.min(55, s.a + s.v * h)); const q = pose[k] || (pose[k] = Object.assign({}, REST)); q.r += s.a; }
      P.mats = world(rig, pose, P.root); P.alpha = P.root.a == null ? 1 : P.root.a; };
    const isFront = k => { for (let n = 0; k && n < 8; n++, k = rig.parts[k].p) { if (P.pose[k] && P.pose[k].z > .5) return true; if (!rig.parts[k]) break; } return false; };
    P.image = k => { const f = rig.swaps && rig.swaps[k]; if (f) { const im = rig.img['@' + (f[P.name] || f.idle)]; if (im) return im; } return rig.img[k]; };   /* the picture of a piece right now (faces change with the move) */
    P.order = () => { const a = [], f = []; for (const k of rig.order) (isFront(k) ? f : a).push(k); return f.length ? a.concat(f) : rig.order; };   /* back to front for this pose */
    P.drawClip = (ctx, x, y, scale, left, a) => { const c = P.clip || P.lastClip, im = c && c.img[P.clip ? P.frame : c.img.length - 1]; if (!im) return; const k = scale * (rig.figH || rig.size[1]) / c.figH, a0 = ctx.globalAlpha; ctx.globalAlpha = a0 * a;
      ctx.setTransform(left ? -k : k, 0, 0, k, x, y); ctx.drawImage(im, -c.foot[0], -c.foot[1]); P.clipV = [left ? -k : k, k, x, y, c]; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = a0; };
    P.clipPoint = p => { const v = P.clipV; return v ? [v[2] + (p[0] - v[4].foot[0]) * v[0], v[3] + (p[1] - v[4].foot[1]) * v[1]] : null; };   /* a point of the drawn frame on screen */
    P.draw = (ctx, x, y, scale, left) => { if (P.clip) { P.lastClip = P.clip; if (P.cf > 0) { const f = P.cf / .08; drawBones(ctx, x, y, scale, left, f); P.drawClip(ctx, x, y, scale, left, 1 - f); } else P.drawClip(ctx, x, y, scale, left, 1); return; }
      if (P.fromClip > 0) { const f = P.fromClip / .1; P.fromClip -= 1 / 60; drawBones(ctx, x, y, scale, left, 1 - f); P.drawClip(ctx, x, y, scale, left, f); return; } drawBones(ctx, x, y, scale, left, 1); };
    const drawBones = (ctx, x, y, scale, left, fade) => { if (!P.mats) P.update(0); if (!P.mats) return; const F = rig._feet, sx = left ? -scale : scale, V = [sx, 0, 0, scale, x - F[0] * sx, y - F[1] * scale], a0 = ctx.globalAlpha; ctx.globalAlpha = a0 * Math.max(0, Math.min(1, P.alpha));
      if (rig.mesh && meshRender(rig, P, ctx, V, fade)) { ctx.globalAlpha = a0; P.view = V; return; }   /* Spine-style bending meshes */
      for (const k of P.order()) { const q = rig.parts[k], m = mul(V, P.mats[k]); const pa = (P.pose[k] && P.pose[k].a != null ? P.pose[k].a : 1) * (fade == null ? 1 : fade); if (pa <= .01) continue; ctx.globalAlpha = a0 * Math.max(0, Math.min(1, P.alpha)) * pa; ctx.setTransform(m[0], m[1], m[2], m[3], m[4], m[5]); const im = P.image(k); ctx.drawImage(im, -q.pv[0] - (im._ox || 0), -q.pv[1] - (im._oy || 0)); } ctx.globalAlpha = a0; P.view = V; };
    P.at = (k, lx, ly) => { const m = P.mats && P.mats[k], q = rig.parts[k]; if (!m) return null; const p = pt(m, (lx || 0) - 0, (ly || 0) - 0); return P.view ? pt(P.view, p[0], p[1]) : p; };   /* where a point of a piece (its picture px, from the turning point) is on screen after draw */
    P.centre = k => { const im = rig.img[k], q = rig.parts[k]; return im ? P.at(k, im.width / 2 - q.pv[0], im.height / 2 - q.pv[1]) : null; };
    P.angle = k => { const m = P.mats && P.mats[k]; if (!m) return 0; const V = P.view || [1, 0, 0, 1, 0, 0], n = mul(V, m); return Math.atan2(n[1], n[0]); };
    return P;
  }
  return { load, images, seamless, unseam, bake, meshMake, meshRender, autofit, restScore, seams, prep, player, world, sample, bind, mul, inv, pt, trs, MOVES, NAMES, ROLES, EASE, REST };
})();
if (typeof module !== 'undefined') module.exports = Bones2D;
