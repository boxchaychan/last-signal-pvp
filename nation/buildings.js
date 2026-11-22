'use strict';
/* ก่อร่างสร้างชาติ: the good-looking homes and towers. All drawn in code from small parts. */
const B_WALL = [0xf4ecdc, 0xe9dcc5, 0xdfe6e3, 0xf1dac2, 0xd8e0cf, 0xf7f3ea, 0xe8cfb7, 0xd2dade];
const B_ROOF = [0xb6543a, 0x8b4b37, 0x4f7084, 0x9c4034, 0x607456, 0x5b5f69, 0xc56d46, 0x405767];
const B_ACC = [0xd9654b, 0x3f90a9, 0xe2ab40, 0x4f9b71, 0x7b70b1, 0xca587f];
const B_GLASS = [0x2f6080, 0x2b6c7b, 0x3a6090, 0x25526c];
const LIT_GLASS = 0x6f8fa0, FRAME = 0x59616b;
const mixC = (a, b, t) => { const q = s => (a >> s & 255) * (1 - t) + (b >> s & 255) * t; return (q(16) << 16) | (q(8) << 8) | q(0); };

const box0 = MB.prototype.box;
MB.prototype.box = function (x, y, z, w, h, d, c, g = 0) { (this.boxes = this.boxes || []).push({ x, z, w, d }); return box0.call(this, x, y, z, w, h, d, c, g); };
/* one flat rectangle on a wall. side: 0 front, 1 right, 2 back, 3 left */
function rect(out, side, cx, cz, hw, hd, off, u, y0, uw, y1) {
  const a = u - uw / 2, b = u + uw / 2; let P;
  if (side === 0) { const z = cz + hd + off; P = [[cx + a, y0, z], [cx + b, y0, z], [cx + b, y1, z], [cx + a, y1, z]]; }
  else if (side === 2) { const z = cz - hd - off; P = [[cx - a, y0, z], [cx - b, y0, z], [cx - b, y1, z], [cx - a, y1, z]]; }
  else if (side === 1) { const x = cx + hw + off; P = [[x, y0, cz - a], [x, y0, cz - b], [x, y1, cz - b], [x, y1, cz - a]]; }
  else { const x = cx - hw - off; P = [[x, y0, cz + a], [x, y0, cz + b], [x, y1, cz + b], [x, y1, cz + a]]; }
  out.push(P[0], P[1], P[2], P[0], P[2], P[3]);
}
/* a real grid of windows on all four walls; some are lit at night */
MB.prototype.grid = function (cx, cz, w, d, y0, n, fh, o = {}) {
  const glass = o.glass || B_GLASS[0], step = (o.step || .44) * (MOBILE ? 1.55 : 1), pw = o.pw || .68, ph = o.ph || .6, lit = o.lit == null ? .34 : o.lit >= .9 ? o.lit : o.lit * .58, frame = o.frame == null ? FRAME : o.frame, sides = o.sides || [0, 1, 2, 3]; let hash = (o.seed || 11) * 7919;
  for (let i = 0; i < n; i++) {
    const F = [], D = [], L = [], y = y0 + fh * i + fh * (1 - ph) * .55, t = y + fh * ph;
    for (const sd of sides) {
      const span = sd % 2 ? d : w, c = Math.max(1, Math.round((span - .14) / step)), cw = (span - .1) / c;
      for (let j = 0; j < c; j++) { const u = -span / 2 + .05 + cw * (j + .5), pwid = cw * pw; hash = (hash * 31 + j + i * 3 + sd) % 10007; if (!MOBILE && frame) rect(F, sd, cx, cz, w / 2, d / 2, .008, u, y - .025, pwid + .05, t + .025); rect(hash % 100 < lit * 100 ? L : D, sd, cx, cz, w / 2, d / 2, .016, u, y, pwid, t); }
    }
    if (F.length) this.add(y, F, frame, 0); const top = mixC(glass, 0x9fd0e0, clamp(i / Math.max(n, 1)) * .3); if (D.length) this.add(y + .001, D, top, .5); if (L.length) this.add(y + .001, L, mixC(top, LIT_GLASS, .35), 1);
  }
  return this;
};
/* every older drawing that asks for window floors now gets the real grid, on the right block */
MB.prototype.floors = function (w, d, y0, n, fh, glass) { const q = (this.boxes || []).slice().reverse().find(b => Math.abs(b.w - w) < .01 && Math.abs(b.d - d) < .01) || { x: 0, z: 0 }; return this.grid(q.x, q.z, w, d, y0, n, fh, { glass: mixC(glass, 0x2f6080, .6), seed: Math.round(w * 13 + d * 7 + n) }); };
MB.prototype.hip = function (x, y, z, w, h, d, c) {
  const a = x - w / 2, b = x + w / 2, e = z - d / 2, f = z + d / 2, t = y + h, r = Math.max(0, (w - d) / 2 + d * .12), L = [x - r, t, z], R = [x + r, t, z];
  this.add(y, [[a, y, f], [b, y, f], R, [a, y, f], R, L, [b, y, e], [a, y, e], L, [b, y, e], L, R, [a, y, e], [a, y, f], L, [b, y, f], [b, y, e], R], c, 0); return this;
};

MB.prototype.roundGrid = function (cx, cz, r, y0, n, fh, o = {}) {
  const segs = MOBILE ? 10 : 16, glass = o.glass || B_GLASS[0], lit = o.lit == null ? .34 : o.lit, taper = o.taper || 0; let hash = (o.seed || 3) * 6151;
  for (let i = 0; i < n; i++) {
    const R = r + taper * i + .014, y = y0 + fh * i + fh * .18, tp = y + fh * .62, D = [], L = [];
    for (let j = 0; j < segs; j++) { const a = (j + .1) / segs * 6.2832, b = (j + .9) / segs * 6.2832, A = [cx + Math.cos(a) * R, y, cz + Math.sin(a) * R], B_ = [cx + Math.cos(b) * R, y, cz + Math.sin(b) * R], C = [cx + Math.cos(b) * R, tp, cz + Math.sin(b) * R], E = [cx + Math.cos(a) * R, tp, cz + Math.sin(a) * R]; hash = (hash * 31 + i + j) % 10007; (hash % 100 < lit * 100 ? L : D).push(A, C, B_, A, E, C); }
    if (D.length) this.add(y, D, glass, .5); if (L.length) this.add(y, L, mixC(glass, LIT_GLASS, .4), 1);
  } return this;
};
function altTower(m, v, lot) {
  const k = v % 6, gl = B_GLASS[v % 4], c = [0xd9e1e6, 0xcdd6d2, 0xe0d7c9][v % 3]; lot(0xc4c0b8); m.box(0, .04, 0, 2.72, .56, 2.72, 0x59616b); m.grid(0, 0, 2.72, 2.72, .08, 1, .46, { glass: 0x78b2c6, lit: .95, step: .6, pw: .88, ph: .84 }); m.box(0, .6, 0, 2.84, .05, 2.84, 0xe8e4da);
  if (k === 3) { m.cyl(0, .64, 0, 1.1, 9.1, c, 1.1, MOBILE ? 12 : 18); m.roundGrid(0, 0, 1.1, .7, 16, .56, { glass: gl, seed: v + 30 }); for (let i = 0; i <= 4; i++) m.cyl(0, .66 + i * 2.24, 0, 1.16, .05, 0xf0efe9, 1.16, MOBILE ? 12 : 18); m.cyl(0, 9.74, 0, 1.12, .55, 0x8fb4c2, .35, 14); m.cyl(0, 10.28, 0, .05, 1, 0xe7e9ea, .008, 5); }
  else if (k === 4) { for (const [x, h, n] of [[-.62, 9.2, 16], [.62, 7.5, 13]]) { m.box(x, .64, 0, .98, h, 1.96, c); m.grid(x, 0, .98, 1.96, .7, n, .56, { glass: gl, seed: v + n, step: .32, pw: .76, ph: .68, frame: mixC(c, 0, .3) }); m.box(x, .64 + h, 0, 1.06, .08, 2.04, mixC(c, 0, .2)); m.box(x, .72 + h, -.3, .4, .28, .5, 0x9aa3ab); } m.box(0, 5.1, 0, .38, .42, .76, 0x8fc4d6, .5); m.box(0, 5.06, 0, .42, .05, .8, 0xe8e4da); m.box(0, 5.52, 0, .42, .05, .8, 0xe8e4da); }
  else { let y = .64; for (const [w, n] of [[2.2, 8], [1.7, 6], [1.14, 4]]) { const h = n * .56 + .06; m.box(0, y, 0, w, h, w, c); m.grid(0, 0, w, w, y + .04, n, .56, { glass: gl, seed: v + n * 3, step: .34, pw: .76, ph: .68, frame: mixC(c, 0, .3) }); y += h; m.box(0, y, 0, w + .1, .07, w + .1, 0xf0efe9); y += .07; } m.cyl(0, y, 0, .3, .5, 0xcfd6da, .1, 8); m.cyl(0, y + .5, 0, .05, 1.2, 0xe7e9ea, .008, 5); }
}

function drawFancy(m, t, v) {
  const def = BT[t]; if (!def) return false; const W0 = def.s[0], D0 = def.s[1], wall = B_WALL[v % 8], roof = B_ROOF[(v * 3 + 1) % 8], acc = B_ACC[(v + 2) % 6], gl = B_GLASS[v % 4];
  const lot = (top, edge = 0xcfc8b8) => { m.box(0, -.7, 0, W0 - .04, .72, D0 - .04, edge); m.box(0, .02, 0, W0 - .17, .025, D0 - .17, top); };
  const bush = (x, z, r = .13, c = 0x4f9148) => { m.cyl(x, .04, z, r, r * 1.05, c, r * .72, 6); m.cyl(x, .04 + r * 1.05, z, r * .72, r * .55, mixC(c, 0xa8d070, .25), .01, 6); };
  const tree = (x, z, s = 1) => { m.cyl(x, .04, z, .045 * s, .28 * s, 0x6e4f33, .03 * s, 5); m.cyl(x, .24 * s, z, .23 * s, .24 * s, 0x4f9a4c, .2 * s, 7); m.cyl(x, .48 * s, z, .2 * s, .24 * s, 0x68ad58, .02 * s, 7); };
  const door = (x, z, c = 0x6b4630, h = .4, w = .2) => { m.box(x, .04, z, w + .05, h + .03, .025, 0xf5f0e6); m.box(x, .04, z + .012, w, h, .025, c); m.box(x + w * .32, .04 + h * .45, z + .03, .025, .025, .012, 0xe7c35a); };
  const pane = (x, y, z, w, h, side = 0, lit = 1) => { const o = []; rect(o, side, 0, 0, side % 2 ? Math.abs(x) : 0, side % 2 ? 0 : Math.abs(z), .018, side % 2 ? (side === 1 ? -z : z) : (side === 0 ? x : -x), y, w, y + h); const f = []; rect(f, side, 0, 0, side % 2 ? Math.abs(x) : 0, side % 2 ? 0 : Math.abs(z), .008, side % 2 ? (side === 1 ? -z : z) : (side === 0 ? x : -x), y - .03, w + .06, y + h + .03); m.add(y, f, 0xf8f4ea, 0); m.add(y, o, lit ? 0x5f8ba2 : gl, lit ? 1 : .5); };
  const fence = (x, z, len, axis) => { for (let i = 0; i <= Math.floor(len / .2); i++) { const q = -len / 2 + i * .2; m.box(axis ? x : x + q, .04, axis ? z + q : z, .025, .15, .025, 0xf1ece0); } m.box(x, .13, z, axis ? .018 : len, .02, axis ? len : .018, 0xf1ece0); };
  const ac = (x, y, z) => { m.box(x, y, z, .18, .1, .14, 0xc9cdd0); m.box(x, y + .1, z, .1, .015, .08, 0x8d9398); };
  const parapet = (x, y, z, w, d, c) => { m.box(x, y, z + d / 2 - .03, w, .09, .06, c); m.box(x, y, z - d / 2 + .03, w, .09, .06, c); m.box(x + w / 2 - .03, y, z, .06, .09, d, c); m.box(x - w / 2 + .03, y, z, .06, .09, d, c); };
  const balcony = (x, y, z, w) => { m.box(x, y, z, w, .035, .2, 0xf4f1e9); m.box(x, y + .035, z + .095, w, .13, .012, 0x8fb4c2); m.box(x, y + .165, z + .095, w, .014, .02, 0x59616b); };

  if (W.hasAtlas && texBuilding(m, t, v, { lot, bush, tree, fence, ac, parapet })) return true;
  switch (t) {
    case 'hut': {
      lot(0x8cb561, 0xa78e64); m.box(.02, .04, .68, .3, .012, .6, 0xcdb88d); m.box(0, .04, -.05, 1.22, .48, 1.02, 0xb98f60);
      for (let i = 0; i < 4; i++) { m.box(0, .1 + i * .11, .463, 1.22, .016, .012, 0x8d6a45); m.box(.617, .1 + i * .11, -.05, .012, .016, 1.02, 0x8d6a45); }
      m.hip(0, .52, -.05, 1.6, .58, 1.42, 0xd5b264); m.hip(0, .79, -.05, .86, .32, .74, 0xc29c50); door(.02, .47, 0x6b4630, .36, .2); pane(.4, .24, .47, .18, .15); pane(-.38, .24, .47, .18, .15, 0, 0);
      m.box(-.72, .04, .55, .34, .08, .16, 0x8a6240); m.box(-.72, .12, .55, .24, .07, .14, 0x9b7048); bush(.74, .62); break;
    }
    case 'house': {
      lot(0x86b45d); const k = v % 3;
      if (k === 0) { m.box(0, .04, -.16, 1.46, .74, 1.14, wall); m.box(0, .04, -.16, 1.5, .08, 1.18, 0xa9a297); m.hip(0, .78, -.16, 1.76, .58, 1.42, roof); m.box(.36, .04, .52, .62, .03, .34, 0xd8cfbd); m.box(.36, .62, .53, .72, .04, .42, roof); for (const x of [.06, .66]) m.box(x, .06, .68, .05, .57, .05, 0xf7f3ea); door(.36, .43); pane(-.4, .34, .43, .36, .28); pane(.74, .34, -.16, .3, .26, 1, v % 2); pane(-.74, .34, -.16, .3, .26, 3, 0); m.box(-.4, .3, .46, .42, .03, .05, 0xf8f4ea); m.box(-.42, 1.05, -.4, .16, .4, .16, 0x9a6b56); }
      else if (k === 1) { m.box(-.2, .04, -.14, 1.1, .74, 1.2, wall); m.roof(-.2, .78, -.14, 1.3, .48, 1.42, roof); m.box(.56, .04, .16, .62, .62, .72, mixC(wall, acc, .22)); m.roof(.56, .66, .16, .76, .3, .92, mixC(roof, 0, .08)); door(-.34, .47); pane(.08, .34, .47, .3, .26); pane(.56, .26, .53, .36, .26, 0, 0); pane(-.76, .34, -.14, .32, .26, 3); m.box(.56, .045, .75, .5, .012, .42, 0xd7d0c2); bush(-.72, .68); bush(-.5, .72, .1); }
      else { m.box(-.1, .04, -.12, 1.34, 1.34, 1.14, wall); m.box(-.1, 1.38, -.12, 1.46, .07, 1.26, 0x5b5f69); parapet(-.1, 1.42, -.12, 1.42, 1.22, wall); m.box(.5, .04, .1, .62, .66, .78, mixC(wall, acc, .35)); m.box(.5, .7, .1, .7, .05, .86, 0x5b5f69); door(-.42, .46); pane(0, .3, .46, .46, .3); pane(-.1, .9, .46, .78, .3); balcony(-.1, .78, .55, .92); pane(.81, .28, .1, .36, .26, 1, 0); }
      fence(0, -.9, 1.7, 0); fence(-.9, 0, 1.75, 1); bush(.76, -.72); bush(-.72, -.7, .11); if (k !== 1) tree(-.72, .62, .9); break;
    }
    case 'row': {
      lot(0xc9c3b6); for (let i = 0; i < 3; i++) {
        const x = -1.27 + i * 1.27, c = B_WALL[(v + i * 3) % 8], tall = 1.45 + ((i + v) % 2) * .42, a2 = B_ACC[(v + i) % 6]; m.box(x, .04, -.05, 1.23, tall, 1.6, c); m.box(x, .04, .75, 1.13, .52, .02, 0x3a4048); m.box(x, .08, .765, .98, .42, .02, 0x7fb2c6, 1);
        for (let j = 0; j < 4; j++) m.box(x - .36 + j * .24, .08, .78, .018, .42, .015, 0x59616b); m.box(x, .57, .9, 1.17, .045, .34, a2); m.box(x, .62, .77, 1.04, .15, .03, mixC(a2, 0xffffff, .72)); m.box(x, .66, .79, .68, .055, .012, a2);
        pane(x - .28, .92, .75, .36, .34, 0, (i + v) % 2); pane(x + .28, .92, .75, .36, .34, 0, (i + v + 1) % 2); if (tall > 1.7) { pane(x - .28, 1.42, .75, .36, .28, 0, i % 2); pane(x + .28, 1.42, .75, .36, .28, 0, 1); } parapet(x, tall + .04, -.05, 1.23, 1.6, mixC(c, 0, .12)); ac(x - .25, tall + .04, -.3);
      } break;
    }
    case 'apt': {
      lot(0xc8c2b5); const h = .58, n = 5 + v % 3, tone = mixC(wall, acc, .12); m.box(0, .04, -.04, 2.28, h * n + .42, 2.14, tone); m.box(0, .04, -.04, 2.36, .44, 2.22, 0x70757c); m.box(0, .06, 1.08, 1.5, .34, .03, 0x7fb2c6, 1); door(0, 1.1, 0x3f464e, .34, .42);
      m.grid(0, -.04, 2.28, 2.14, .48, n, h, { glass: gl, seed: 20 + v, step: .42 }); for (let i = 0; i < n; i++) { balcony(-.62, .46 + h * i, 1.13, .72); balcony(.62, .46 + h * i, 1.13, .72); } m.box(0, .46, 1.04, .22, h * n, .06, mixC(tone, acc, .55));
      const top = .46 + h * n; parapet(0, top, -.04, 2.28, 2.14, mixC(tone, 0, .14)); m.box(.5, top, -.42, .62, .42, .62, 0xaeb2b6); m.cyl(-.55, top, .3, .25, .45, 0x89a7b6, .25, 8); ac(-.3, top, -.6); ac(.1, top, .55); bush(-.98, 1, .12); bush(.98, 1, .12); break;
    }
    case 'tower': {
      if (v % 6 >= 3) { altTower(m, v, lot); break; }
      lot(0xc4c0b8); const sh = [0xd7dfe4, 0xc7d0d8, 0xddd4c6, 0xbfd0cb][v % 4], n = 15 + v % 4, f = .54; m.box(0, .04, 0, 2.72, .62, 2.72, 0x5e6670); m.grid(0, 0, 2.72, 2.72, .1, 1, .5, { glass: 0x6fa6bc, lit: .9, step: .6, pw: .86, ph: .82 }); m.box(0, .66, 0, 2.86, .05, 2.86, 0xe8e4da);
      m.box(0, .7, 0, 2.14, f * n + .1, 2.14, sh); m.grid(0, 0, 2.14, 2.14, .74, n, f, { glass: gl, seed: 40 + v, step: .36, pw: .76, ph: .68, frame: mixC(sh, 0, .3) }); for (const a of [-1, 1]) for (const b of [-1, 1]) m.box(a * 1.05, .7, b * 1.05, .11, f * n + .16, .11, mixC(sh, 0, .18));
      const top = .8 + f * n; parapet(0, top, 0, 2.14, 2.14, mixC(sh, 0, .22)); if (v % 2) { m.box(0, top + .02, 0, 1.5, .05, 1.5, 0x4a4f57); m.cyl(0, top + .07, 0, .44, .012, 0xf3d04d, .44, 14); m.cyl(0, top + .08, 0, .34, .012, 0x4a4f57, .34, 14); } else { m.box(.2, top, -.1, 1.1, .5, 1, 0x9aa3ab); m.grid(.2, -.1, 1.1, 1, top + .06, 1, .4, { glass: gl, seed: 7, step: .3 }); m.box(.2, top + .5, -.1, .05, .85, .05, 0xe7e9ea); m.cyl(.2, top + 1.3, -.1, .05, .05, 0xf05040, .05, 6, 1); } break;
    }
    case 'mega': {
      lot(0xbdbbb5); const c = [0xcfdbe3, 0xc3d3d8, 0xd6d7d2][v % 3]; m.box(0, .04, 0, 3.7, .9, 3.7, 0x4f5862); m.grid(0, 0, 3.7, 3.7, .12, 1, .72, { glass: 0x78b2c6, lit: .95, step: .7, pw: .88, ph: .84 }); m.box(0, .94, 0, 3.86, .06, 3.86, 0xe6e2d8);
      m.box(0, 1, 0, 3, 9.7, 3, c); m.grid(0, 0, 3, 3, 1.04, 18, .53, { glass: gl, seed: 61, step: .36, pw: .78, ph: .7, frame: mixC(c, 0, .26) }); m.box(0, 10.7, 0, 3.12, .12, 3.12, 0xeef0f0);
      m.box(0, 10.82, 0, 2.2, 6.3, 2.2, mixC(c, 0xffffff, .12)); m.grid(0, 0, 2.2, 2.2, 10.86, 12, .52, { glass: mixC(gl, 0x4d90b0, .3), seed: 62, step: .36, pw: .78, ph: .7 }); m.box(0, 17.12, 0, 2.3, .1, 2.3, 0xeef0f0);
      m.box(0, 17.22, 0, 1.3, 3, 1.3, c); m.grid(0, 0, 1.3, 1.3, 17.26, 5, .56, { glass: gl, seed: 63, step: .32 }); m.cyl(0, 20.22, 0, .62, .5, 0xdde4e8, .22, 8); m.cyl(0, 20.72, 0, .12, 3.1, 0xe9ecee, .012, 6); m.cyl(0, 23.76, 0, .05, .05, 0xf05040, .05, 6, 1); break;
    }
    case 'shop': {
      lot(0xd2cbbd); m.box(0, .04, -.14, 1.56, 1, 1.26, wall); m.box(0, .04, .5, 1.42, .52, .02, 0x3a4048); m.box(0, .08, .515, 1.22, .44, .02, 0x82b8cc, 1); door(.46, .53, 0x3f464e, .44, .24);
      for (let i = 0; i < 5; i++) m.box(-.72 + i * .29 + .145, .58, .68, .29, .035, .36, i % 2 ? 0xfaf6ee : acc); m.box(0, .66, .51, 1.42, .22, .04, mixC(acc, 0xffffff, .8)); m.box(0, .72, .535, .88, .1, .012, acc); parapet(0, 1.04, -.14, 1.56, 1.26, mixC(wall, 0, .14)); ac(-.3, 1.04, -.3);
      m.box(-.5, .04, .8, .36, .17, .2, 0xa8784c); m.box(-.5, .21, .8, .3, .05, .15, B_ACC[(v + 3) % 6]); bush(.76, .84, .1); break;
    }
    case 'office': {
      lot(0xc8c4bb); const c = [0x7f9fb2, 0x8fa7ad, 0x7890aa, 0x88a5a0][v % 4], n = 10 + v % 3, f = .54; m.box(0, .04, 0, 2.72, .54, 2.72, 0x3f4851); m.grid(0, 0, 2.72, 2.72, .08, 1, .46, { glass: 0x7cb6ca, lit: .95, step: .55, pw: .88, ph: .85 }); m.box(0, .58, 0, 2.82, .05, 2.82, 0xe5e6e2);
      m.box(0, .62, 0, 2.2, f * n + .08, 2.2, c); m.grid(0, 0, 2.2, 2.2, .66, n, f, { glass: mixC(gl, 0x4e93b4, .35), seed: 80 + v, step: .27, pw: .9, ph: .78, frame: mixC(c, 0, .35), lit: .62 }); for (let i = 0; i < 5; i++) { const q = -.88 + i * .44; m.box(q, .62, 1.11, .035, f * n + .08, .05, 0xdfe5e8); m.box(1.11, .62, q, .05, f * n + .08, .035, 0xdfe5e8); }
      const top = .7 + f * n; parapet(0, top, 0, 2.2, 2.2, 0xdde2e4); m.box(0, top, 0, 1.2, .38, 1.2, 0x7c858d); ac(-.7, top, .6); ac(.7, top, .6); m.box(-1.2, .06, 1.25, .04, .4, .04, 0x59616b); bush(1.2, 1.2, .13); break;
    }
    case 'cbd': {
      if (v % 4 === 2) { lot(0xc2bfb7); m.box(0, .04, 0, 2.8, .7, 2.8, 0x363f48); m.grid(0, 0, 2.8, 2.8, .08, 1, .62, { glass: 0x86c3d4, lit: 1, step: .6, pw: .9, ph: .86 }); m.cyl(0, .74, 0, 1.3, 7.6, 0x4f7f9c, 1.1, MOBILE ? 12 : 18); m.roundGrid(0, 0, 1.2, .8, 13, .56, { glass: 0x2a6685, seed: v + 5, taper: -.0145 }); m.cyl(0, 8.34, 0, 1.12, 2.5, 0x6fa6bf, .62, MOBILE ? 12 : 18); m.roundGrid(0, 0, .9, 8.4, 4, .55, { glass: 0x2a6685, seed: v + 6, taper: -.05 }); m.cyl(0, 10.84, 0, .62, 1.5, 0xb9d6e2, .03, 12); m.cyl(0, 12.3, 0, .05, 1.2, 0xe9ecee, .008, 5); break; }
      lot(0xc2bfb7); const c = [0x5d88a8, 0x68999f, 0x7690b4, 0x5e7e98][v % 4]; m.box(0, .04, 0, 2.8, .7, 2.8, 0x363f48); m.grid(0, 0, 2.8, 2.8, .08, 1, .62, { glass: 0x86c3d4, lit: 1, step: .6, pw: .9, ph: .86 }); m.box(0, .74, 0, 2.92, .05, 2.92, 0xe5e6e2);
      m.box(0, .78, 0, 2.4, 8.4, 2.4, c); m.grid(0, 0, 2.4, 2.4, .82, 15, .55, { glass: mixC(c, 0x18435e, .55), seed: 90 + v, step: .25, pw: .92, ph: .8, frame: mixC(c, 0xffffff, .22), lit: .66 }); m.box(0, 9.18, 0, 2.5, .1, 2.5, 0xe9edf0);
      m.box(0, 9.28, 0, 1.76, 4.5, 1.76, mixC(c, 0xffffff, .1)); m.grid(0, 0, 1.76, 1.76, 9.32, 8, .55, { glass: mixC(c, 0x18435e, .45), seed: 91 + v, step: .25, pw: .92, ph: .8, frame: mixC(c, 0xffffff, .28), lit: .66 }); m.box(0, 13.78, 0, 1.86, .08, 1.86, 0xe9edf0);
      if (v % 2) { m.hip(0, 13.86, 0, 1.76, 1.5, 1.76, 0x9fc6d8); m.cyl(0, 15.3, 0, .06, 1.5, 0xe9ecee, .01, 5); } else { m.box(0, 13.86, 0, .9, 1, .9, 0x88a0b0); m.grid(0, 0, .9, .9, 13.9, 2, .44, { glass: 0x2f6080, lit: .9, step: .22 }); m.cyl(0, 14.86, 0, .1, 1.8, 0xe9ecee, .01, 5); } break;
    }
    case 'reclaim': { m.box(0, 0, 0, 2.7, .22, 1.5, 0x8a4b3a); m.box(0, .22, 0, 2.8, .05, 1.6, 0xe9e2d3); m.box(-.75, .27, .1, .85, .55, .9, 0xf0efe9); m.grid(-.75, .1, .85, .9, .3, 1, .46, { glass: 0x2f6080, step: .3 }); m.box(.55, .27, -.2, .16, 1.5, .16, 0xe2ab40); m.box(.2, 1.72, -.2, 1.5, .09, .09, 0xe2ab40); m.cyl(.85, .27, .35, .42, .38, 0xdcc48d, .06, 8); m.box(1.5, .12, .35, .9, .07, .07, 0x4c5158); break; }
    default: return false;
  }
  return true;
}

/* ---------- painted fronts (Codex sheet) wrapped round the 3D blocks ---------- */
W.atlasP = new Promise(res => { const im = new Image(); let late = false; im.onload = () => { if (!late) { W.atlasImg = im; W.hasAtlas = true; } res(); }; im.onerror = () => res(); im.src = 'art/nation/facades.webp?b=' + BUILD; setTimeout(() => { late = true; res(); }, 7000); });
MB.prototype.tex = function (side, cx, cz, w, d, y0, y1, cell, o = {}) {
  const span = side % 2 ? d : w, c = FACADE.cells[cell]; let u0 = c[0], u1 = c[2], top = c[1], bot = c[3];
  if (o.slice && o.slice < 1) { const mid = (u0 + u1) / 2, hw = (u1 - u0) * o.slice / 2; u0 = mid - hw; u1 = mid + hw; }
  if (o.vf && o.vf < 1) top = bot - (bot - c[1]) * o.vf;
  const hr = Math.max(1, o.hrep || 1), tileW = span / hr, ratio = (bot - top) / (u1 - u0), vr = o.tile ? Math.max(1, Math.round((y1 - y0) / (tileW * ratio))) : 1;
  if (vr > 1) { const trim = (bot - top) * .035; top += trim; bot -= trim; }
  const a = u0 / FACADE.w, b = u1 / FACADE.w, vb = 1 - bot / FACADE.h, vt = 1 - top / FACADE.h, col = hex(o.tint || 0xffffff);
  for (let i = 0; i < hr; i++) for (let j = 0; j < vr; j++) { const V = [], ya = y0 + (y1 - y0) * j / vr, yb = y0 + (y1 - y0) * (j + 1) / vr; rect(V, side, cx, cz, w / 2, d / 2, .007, -span / 2 + tileW * (i + .5), ya, tileW, yb); this.parts.push({ miny: ya + .001, verts: V, col, glow: 0, uvs: [a, vb, b, vb, b, vt, a, vb, b, vt, a, vt], flat: 1 }); }
  return this;
};
function texBuilding(m, t, v, h) {
  /* painted fronts look best at their natural size; tall glass towers stay clean and code-drawn */
  if (t === 'tower' || t === 'office' || t === 'cbd' || t === 'mega') return false;
  const tint = [0xffffff, 0xfff0df, 0xe6f1ff, 0xf1ffe6, 0xffe8e2, 0xeeeaff][v % 6], { lot, bush, tree, fence, ac, parapet } = h;
  const wrap = (cx, cz, w, d, y0, y1, cell, top, o = {}) => { m.box(cx, y0, cz, w, y1 - y0, d, top); for (let s = 0; s < 4; s++) m.tex(s, cx, cz, w, d, y0, y1, cell, { tint: o.tint || tint, vf: cell >= 3 && cell <= 5 ? 0 : o.vf, tile: cell >= 3 && cell <= 5, hrep: cell === 5 ? 2 : 1, slice: s % 2 ? clamp(d / w, .3, 1) : clamp(w / d, .3, 1) }); };
  const slab = (cx, y, cz, w, d, c = 0xe9e2d3) => m.box(cx, y, cz, w + .1, .07, d + .1, c);
  switch (t) {
    case 'house': { if (v % 3 === 1) return false; lot(0x86b45d); wrap(0, -.12, 1.68, 1.4, .04, 1.72, 0, 0xd9c6a6); slab(0, 1.72, -.12, 1.68, 1.4, 0xcdb896); fence(0, -.9, 1.7, 0); fence(-.9, 0, 1.75, 1); m.box(.42, .045, .75, .4, .012, .34, 0xd8cfbd); bush(-.74, .72); bush(.76, .7, .11); tree(.74, -.72, .85); return true; }
    case 'row': { lot(0xc9c3b6); wrap(0, -.05, 3.76, 1.62, .04, 2.05, 1, 0xd9c7ae, { tint: 0xffffff }); parapet(0, 2.05, -.05, 3.76, 1.62, 0xcbb99f); ac(-1, 2.05, -.3); ac(.9, 2.05, .1); return true; }
    case 'apt': { lot(0xc8c2b5); const y = 3.5 + v % 3 * .55; wrap(0, -.04, 2.3, 2.16, .04, y, 2, 0xe6d4b8); parapet(0, y, -.04, 2.3, 2.16, 0xd6c3a6); m.box(.5, y, -.42, .6, .42, .6, 0xb3b1aa); m.cyl(-.55, y, .3, .25, .45, 0x89a7b6, .25, 8); ac(-.3, y, -.6); bush(-1, 1.02, .12); bush(1, 1.02, .12); return true; }
    case 'tower': {
      const k = v % 6; if (k === 3) return false; lot(0xc4c0b8); m.box(0, .04, 0, 2.74, .62, 2.74, 0xd5c6ab); m.grid(0, 0, 2.74, 2.74, .1, 1, .5, { glass: 0x6fa6bc, lit: .9, step: .6, pw: .86, ph: .82, frame: 0 }); slab(0, .66, 0, 2.74, 2.74);
      if (k === 4) { for (const [x, y] of [[-.62, 9.6], [.62, 7.8]]) { wrap(x, 0, 1, 2, .72, y, 3, 0xe6d6bd); slab(x, y, 0, 1, 2); m.box(x, y + .07, -.3, .4, .28, .5, 0x9aa3ab); } m.box(0, 5.1, 0, .3, .42, .78, 0x8fc4d6, .5); m.box(0, 5.06, 0, .32, .05, .82, 0xe8e4da); m.box(0, 5.52, 0, .32, .05, .82, 0xe8e4da); return true; }
      if (k === 5) { let y = .72; for (const [w, n] of [[2.2, 4.4], [1.72, 3.3], [1.16, 2.2]]) { wrap(0, 0, w, w, y, y + n, 3, 0xe6d6bd, { vf: n / 7.6 + .12 }); y += n; slab(0, y, 0, w, w); y += .07; } m.cyl(0, y, 0, .3, .5, 0xcfd6da, .1, 8); m.cyl(0, y + .5, 0, .05, 1.2, 0xe7e9ea, .008, 5); return true; }
      const y = 9 + k * .55; wrap(0, 0, 2.16, 2.16, .72, y, 3, 0xe6d6bd); parapet(0, y, 0, 2.16, 2.16, 0xd8c8ae); if (k === 1) { m.box(0, y + .02, 0, 1.5, .05, 1.5, 0x4a4f57); m.cyl(0, y + .07, 0, .44, .012, 0xf3d04d, .44, 14); m.cyl(0, y + .08, 0, .34, .012, 0x4a4f57, .34, 14); } else { m.box(.2, y, -.1, 1.1, .5, 1, 0xb5b0a6); m.box(.2, y + .5, -.1, .05, .85, .05, 0xe7e9ea); } return true;
    }
    case 'office': { lot(0xc8c4bb); m.box(0, .04, 0, 2.74, .54, 2.74, 0x3f4851); m.grid(0, 0, 2.74, 2.74, .08, 1, .46, { glass: 0x7cb6ca, lit: .95, step: .55, pw: .88, ph: .85, frame: 0 }); slab(0, .58, 0, 2.74, 2.74); const y = 6.4 + v % 3 * .6; wrap(0, 0, 2.22, 2.22, .64, y, 4, 0xdfe3e2); parapet(0, y, 0, 2.22, 2.22, 0xdde2e4); m.box(0, y, 0, 1.2, .38, 1.2, 0x7c858d); ac(-.7, y, .6); ac(.7, y, .6); bush(1.2, 1.2, .13); return true; }
    case 'cbd': { if (v % 4 === 2) return false; lot(0xc2bfb7); m.box(0, .04, 0, 2.82, .7, 2.82, 0x363f48); m.grid(0, 0, 2.82, 2.82, .08, 1, .62, { glass: 0x86c3d4, lit: 1, step: .6, pw: .9, ph: .86, frame: 0 }); slab(0, .74, 0, 2.82, 2.82); wrap(0, 0, 2.42, 2.42, .8, 9.2, 5, 0xe9dcc2); slab(0, 9.2, 0, 2.42, 2.42); wrap(0, 0, 1.78, 1.78, 9.27, 13.8, 5, 0xe9dcc2); slab(0, 13.8, 0, 1.78, 1.78); if (v % 2) { m.hip(0, 13.87, 0, 1.78, 1.5, 1.78, 0x9fc6d8); m.cyl(0, 15.3, 0, .06, 1.5, 0xe9ecee, .01, 5); } else { m.box(0, 13.87, 0, .9, 1, .9, 0xd9c9aa); m.cyl(0, 14.87, 0, .1, 1.8, 0xe9ecee, .01, 5); } return true; }
    case 'mega': { lot(0xbdbbb5); m.box(0, .04, 0, 3.72, .9, 3.72, 0x4f5862); m.grid(0, 0, 3.72, 3.72, .12, 1, .72, { glass: 0x78b2c6, lit: .95, step: .7, pw: .88, ph: .84, frame: 0 }); slab(0, .94, 0, 3.72, 3.72); wrap(0, 0, 3.02, 3.02, 1, 10.7, 5, 0xe9dcc2); slab(0, 10.7, 0, 3.02, 3.02); wrap(0, 0, 2.22, 2.22, 10.77, 17.1, 5, 0xe9dcc2); slab(0, 17.1, 0, 2.22, 2.22); wrap(0, 0, 1.32, 1.32, 17.17, 20.2, 5, 0xe9dcc2); m.cyl(0, 20.2, 0, .62, .5, 0xe2d5bb, .22, 8); m.cyl(0, 20.7, 0, .12, 3.1, 0xe9ecee, .012, 6); m.cyl(0, 23.76, 0, .05, .05, 0xf05040, .05, 6, 1); return true; }
    case 'school': { lot(0xbfc7a0); wrap(0, -.28, 3.5, 1.9, .04, 2.1, 6, 0xd8b18f, { vf: .68, tint: 0xffffff }); parapet(0, 2.1, -.28, 3.5, 1.9, 0xd18f6c); m.box(1.6, .04, 1.1, .05, 1.7, .05, 0xdddddd); m.box(1.8, 1.48, 1.1, .36, .22, .03, 0x2f62b5); m.box(-.9, .045, 1.02, 1.5, .012, .62, 0xc2894f); bush(-1.75, 1.2, .13); bush(.3, 1.2, .12); return true; }
    case 'hischool': { lot(0xbfc7a0); wrap(0, -.42, 4.5, 2.6, .04, 3.3, 6, 0xd8b18f, { tint: 0xffffff }); parapet(0, 3.3, -.42, 4.5, 2.6, 0xd18f6c); m.box(2.1, .04, 1.6, .05, 2.4, .05, 0xdddddd); m.box(2.3, 2.16, 1.6, .36, .22, .03, 0x2f62b5); m.box(-.6, .045, 1.45, 2.4, .012, .7, 0xc2894f); return true; }
    case 'clinic': { lot(0xcdd6c4); wrap(0, -.08, 2.6, 1.56, .04, 1.5, 7, 0xe8e0d0, { vf: .5, tint: 0xffffff }); parapet(0, 1.5, -.08, 2.6, 1.56, 0x4fa66f); m.box(0, 1.08, .71, .34, .11, .03, 0x3fa863); m.box(0, .965, .71, .11, .34, .03, 0x3fa863); return true; }
    case 'hospital': { lot(0xcdd6c4); wrap(0, -.2, 4.5, 3.2, .04, 4.6, 7, 0xeee7d8, { tint: 0xffffff }); parapet(0, 4.6, -.2, 4.5, 3.2, 0xd9d2c3); m.box(1.2, 4.6, -.2, 1.2, .05, 1.1, 0xd9d9d0); m.cyl(1.2, 4.65, -.2, .42, .02, 0xd63c35, .42, 10); m.box(0, 3.95, 1.42, .44, .14, .03, 0xd63c35); m.box(0, 3.8, 1.42, .14, .44, .03, 0xd63c35); return true; }
    case 'medcenter': { lot(0xcdd6c4); for (const x of [-1.42, 1.42]) { wrap(x, -.5, 2.1, 2.5, .04, 7, 7, 0xeee7d8, { tint: 0xffffff }); parapet(x, 7, -.5, 2.1, 2.5, 0xd9d2c3); m.box(x, 6.45, .77, .44, .14, .03, 0xd63c35); m.box(x, 6.3, .77, .14, .44, .03, 0xd63c35); } m.box(0, 3, -.5, .9, .6, .8, 0xbfe3ee, .5); wrap(0, 1.15, 5.5, 1.4, .04, 1.3, 7, 0xeee7d8, { vf: .32, tint: 0xffffff }); return true; }
    default: return false;
  }
}
