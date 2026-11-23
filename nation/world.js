'use strict';
/* ก่อร่างสร้างชาติ: the 3D country. Terrain, roads, trees, buildings and people are all made in code. */
const N = 180, MOBILE = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent) || Math.min(innerWidth, innerHeight) < 500;
const MAX_AGENTS = MOBILE ? 110 : 170, TEX = MOBILE ? 1080 : 1620, MAX_INST = 420;
const ci = (x, z) => x + z * N, inMap = (x, z) => x >= 0 && z >= 0 && x < N && z < N;
function RNG(seed) { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t ^= t + Math.imul(t ^ t >>> 7, 61 | t); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

/* ---------- mesh builder: flat-shaded parts with colours and night-window glow ---------- */
const hex = c => [(c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255];
class MB {
  constructor() { this.parts = []; }
  tri(arr, a, b, c) { arr.push(a, b, c); }
  add(miny, verts, col, glow) { this.parts.push({ miny, verts, col: hex(col), glow }); }
  box(x, y, z, w, h, d, c, g = 0) {
    const a = x - w / 2, b = x + w / 2, e = z - d / 2, f = z + d / 2, t = y + h;
    const q = (p, r, s, u) => [p, r, s, p, s, u];
    const V = [...q([a, y, f], [b, y, f], [b, t, f], [a, t, f]), ...q([b, y, e], [a, y, e], [a, t, e], [b, t, e]), ...q([b, y, f], [b, y, e], [b, t, e], [b, t, f]), ...q([a, y, e], [a, y, f], [a, t, f], [a, t, e]), ...q([a, t, f], [b, t, f], [b, t, e], [a, t, e])];
    this.add(y, V, c, g); return this;
  }
  roof(x, y, z, w, h, d, c) {
    const a = x - w / 2, b = x + w / 2, e = z - d / 2, f = z + d / 2, t = y + h, L = [a, t, z], R = [b, t, z];
    this.add(y, [[a, y, f], [b, y, f], R, [a, y, f], R, L, [b, y, e], [a, y, e], L, [b, y, e], L, R, [a, y, e], [a, y, f], L, [b, y, f], [b, y, e], R], c, 0); return this;
  }
  cyl(x, y, z, r, h, c, r2 = r, n = 8, g = 0) {
    const V = [], t = y + h;
    for (let i = 0; i < n; i++) {
      const p = i / n * 6.2832, q = (i + 1) / n * 6.2832, A = [x + Math.cos(p) * r, y, z + Math.sin(p) * r], B = [x + Math.cos(q) * r, y, z + Math.sin(q) * r], C = [x + Math.cos(q) * r2, t, z + Math.sin(q) * r2], D = [x + Math.cos(p) * r2, t, z + Math.sin(p) * r2];
      V.push(A, C, B, A, D, C); if (r2 > .001) V.push(D, [x, t, z], C);
    }
    this.add(y, V, c, g); return this;
  }
  /* floors of window strips, with solid columns between */
  floors(w, d, y0, n, fh, glass) { for (let i = 0; i < n; i++) this.box(0, y0 + fh * (i + .3), 0, w + .03, fh * .46, d + .03, glass, 1); return this; }
  win(x, y, z, w, h, side = 0) { const t = .05; return side ? this.box(x, y, z, t, h, w, 0xbfe3ee, 1) : this.box(x, y, z, w, h, t, 0xbfe3ee, 1); }
  build() {
    this.parts.sort((p, q) => p.miny - q.miny);
    let n = 0; for (const p of this.parts) n += p.verts.length;
    const P = new Float32Array(n * 3), NR = new Float32Array(n * 3), C = new Float32Array(n * 3), G = new Float32Array(n), UVS = new Float32Array(n * 2); for (let q = 0; q < n; q++) { UVS[q * 2] = 8 / 1536; UVS[q * 2 + 1] = 1 - 8 / 1024; } let i = 0;
    let top = 0; for (const p of this.parts) for (const v of p.verts) top = Math.max(top, v[1]);
    for (const p of this.parts) {
      for (let j = 0; j < p.verts.length; j += 3) {
        const a = p.verts[j], b = p.verts[j + 1], c = p.verts[j + 2], ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
        let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
        let vi = j; for (const v of [a, b, c]) {
          if (p.uvs) { UVS[i * 2] = p.uvs[vi * 2]; UVS[i * 2 + 1] = p.uvs[vi * 2 + 1]; vi++; }
          P[i * 3] = v[0]; P[i * 3 + 1] = v[1]; P[i * 3 + 2] = v[2]; NR[i * 3] = nx; NR[i * 3 + 1] = ny; NR[i * 3 + 2] = nz;
          const sh = p.glow || p.flat ? 1 : .8 + .2 * Math.min(1, (v[1] + .1) / Math.max(.8, top * .5));
          C[i * 3] = p.col[0] * sh; C[i * 3 + 1] = p.col[1] * sh; C[i * 3 + 2] = p.col[2] * sh; G[i] = p.glow; i++;
        }
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.BufferAttribute(NR, 3)); g.setAttribute('color', new THREE.BufferAttribute(C, 3)); g.setAttribute('aGlow', new THREE.BufferAttribute(G, 1)); g.setAttribute('uv', new THREE.BufferAttribute(UVS, 2));
    g.computeBoundingSphere(); return g;
  }
}

/* ---------- every building, drawn from boxes ---------- */
const WALLS = [0xe9dcc3, 0xd8c7a8, 0xc9d6d8, 0xe3b98f, 0xb9c8b0, 0xf0ece2], ROOFS = [0xb5533c, 0x7a4f35, 0x466a7d, 0x8c3f36, 0x5d6b4a, 0x54565f], GLASS = [0x8fc6d8, 0x6fa9c8, 0x9ad0c8];
const CROPS = [0x7fbf3f, 0xd9c04a, 0x5da34a];
function drawB(m, t, v) {
  if (typeof drawFancy === 'function' && drawFancy(m, t, v)) return;
  const W_ = WALLS[v % WALLS.length], R_ = ROOFS[(v * 2 + 1) % ROOFS.length], Gl = GLASS[v % 3];
  m.box(0, -.7, 0, ...(() => { const s = BT[t].s; return [s[0] - .06, .74, s[1] - .06]; })(), t === 'farm' || t === 'bigfarm' || t === 'park' ? 0x6f8f3f : 0x9a917f);
  const door = (x, z, c = 0x5b3f2c, h = .42, w = .24) => m.box(x, .04, z, w, h, .05, c);
  const flag = (x, z, h, c) => { m.box(x, 0, z, .05, h, .05, 0xdddddd); m.box(x + .2, h - .24, z, .36, .22, .03, c); };
  const cross = (x, y, z, c) => { m.box(x, y, z, .34, .11, .05, c); m.box(x, y - .115, z, .11, .34, .05, c); };
  const stack = (x, z, r, h, c = 0x8b8580) => { m.cyl(x, 0, z, r, h, c, r * .8); m.cyl(x, h, z, r * .86, .12, 0xc0483a, r * .86); };
  const tree = (x, z, s = 1) => { m.cyl(x, 0, z, .05 * s, .25 * s, 0x6e4f33, .04 * s, 5); m.cyl(x, .2 * s, z, .24 * s, .55 * s, 0x4f9a48, 0, 7); };
  switch (t) {
    case 'hut': m.box(0, 0, 0, 1.24, .55, 1.1, 0xb48a5c); m.roof(0, .55, 0, 1.56, .55, 1.48, 0xc9a659); door(0, .57); m.win(.42, .22, .57, .18, .16); break;
    case 'house': m.box(0, 0, 0, 1.42, .86, 1.3, W_); m.roof(0, .86, 0, 1.68, .55, 1.56, R_); door(-.3, .67); m.win(.3, .36, .67, .32, .28); m.win(-.72, .36, 0, .3, .28, 1); m.win(.72, .36, 0, .3, .28, 1); if (v % 2) m.box(.42, 1, -.2, .16, .42, .16, 0x80584a); break;
    case 'row': for (let i = 0; i < 3; i++) { const x = -1.26 + i * 1.26; m.box(x, 0, 0, 1.22, 1.4 + (i + v) % 2 * .25, 1.66, WALLS[(v + i) % 6]); m.box(x, .52, .86, 1.12, .07, .2, ROOFS[(v + i) % 6]); m.box(x, .05, .84, .86, .42, .04, Gl, 1); m.win(x, .82, .84, .6, .26); m.box(x, 1.4 + (i + v) % 2 * .25, 0, 1.26, .08, 1.7, 0x6d6a64); } break;
    case 'apt': m.box(0, 0, 0, 2.3, 3.6, 2.3, W_); m.floors(2.3, 2.3, .15, 6, .56, Gl); for (let i = 0; i < 6; i++) m.box(0, .24 + .56 * i, 1.22, 1.5, .05, .22, 0xf2f0ea); m.box(0, 3.6, 0, 2.4, .1, 2.4, 0x6d6a64); m.box(.5, 3.7, .4, .5, .3, .5, 0x8c8a84); door(0, 1.17, 0x3f3f46, .5, .5); break;
    case 'tower': m.box(0, 0, 0, 2.2, 9, 2.2, [0xd9d4cb, 0xb9c3cc, 0xcfc2ae][v % 3]); m.floors(2.2, 2.2, .3, 15, .57, Gl); m.box(0, 9, 0, 1.5, .5, 1.5, 0x78808a); m.box(0, 9.5, 0, .1, .9, .1, 0xdddddd); m.box(0, 0, 0, 2.6, .36, 2.6, 0x5f6670); break;
    case 'mega': m.box(0, 0, 0, 3.1, 11, 3.1, 0xc5d0d8); m.floors(3.1, 3.1, .3, 18, .58, Gl); m.box(0, 11, 0, 2.3, 7, 2.3, 0xbcc9d2); m.floors(2.3, 2.3, 11.2, 11, .6, Gl); m.box(0, 18, 0, 1.4, 2.8, 1.4, 0xb0bec9); m.floors(1.4, 1.4, 18.1, 4, .62, Gl); m.cyl(0, 20.8, 0, .25, 2.4, 0xe4e7ea, .01, 6); break;
    case 'farm': case 'bigfarm': { const b = BT[t].s, rows = t === 'farm' ? 5 : 8, c = CROPS[v % 3]; for (let i = 0; i < rows; i++) { const z = -b[1] / 2 + .45 + i * (b[1] - .9) / (rows - 1); m.box(-.3, .02, z, b[0] - 1.3, .07, .34, 0x6a4b2e); m.box(-.3, .09, z, b[0] - 1.45, .2, .2, c); } m.box(b[0] / 2 - .55, 0, -b[1] / 2 + .6, .8, .6, .8, 0xa65b3f); m.roof(b[0] / 2 - .55, .6, -b[1] / 2 + .6, .96, .34, .96, 0x6b4a36); if (t === 'bigfarm') { m.cyl(b[0] / 2 - .55, 0, b[1] / 2 - .8, .42, 1.8, 0xc8ccd0); m.cyl(b[0] / 2 - .55, 1.8, b[1] / 2 - .8, .42, .32, 0x9ba1a8, .04); } break; }
    case 'lumber': for (let i = 0; i < 4; i++) m.box(-.55, .05 + i * .2, -.5 + i * .08, 1.5 - i * .15, .18, .22, 0x9a6b3f); for (let i = 0; i < 3; i++) m.box(-.55, .05 + i * .2, .1 - i * .05, 1.4, .18, .22, 0x7d5533); m.box(.72, 0, .3, 1.1, .7, 1.4, 0xa8845a); m.roof(.72, .7, .3, 1.3, .3, 1.6, 0x6c6a62); break;
    case 'shop': m.box(0, 0, 0, 1.5, 1, 1.4, W_); m.box(0, .62, .86, 1.6, .06, .42, [0xd84b3e, 0x3f8fd8, 0x3fae6e][v % 3]); m.box(0, .06, .71, 1.1, .5, .04, Gl, 1); m.box(0, 1, 0, 1.6, .1, 1.5, 0x6d6a64); m.box(0, .78, .72, 1.26, .2, .05, 0xf2d24a); break;
    case 'workshop': m.box(0, 0, 0, 2.5, 1, 2.4, 0xa9a59b); for (let i = 0; i < 3; i++) m.roof(-.82 + i * .82, 1, 0, .82, .34, 2.4, 0x6a7078); m.box(0, .06, 1.21, .9, .62, .04, 0x4f5660); stack(.9, -.75, .17, 2); m.box(-.7, .4, 1.21, .5, .25, .04, Gl, 1); break;
    case 'market': for (let i = 0; i < 2; i++) for (let j = 0; j < 3; j++) { const x = -1.2 + j * 1.2, z = -.65 + i * 1.3; m.box(x, .34, z, .9, .05, .78, 0xb48a5c); m.roof(x, .86, z, 1.08, .24, .96, [0xd84b3e, 0xf0b93a, 0x3f8fd8, 0x3fae6e][(i + j + v) % 4]); for (const a of [-1, 1]) for (const b of [-1, 1]) m.box(x + a * .42, 0, z + b * .36, .05, .88, .05, 0x77573a); m.box(x, .39, z, .6, .1, .42, CROPS[(j + v) % 3]); } break;
    case 'office': m.box(0, 0, 0, 2.3, 6.2, 2.3, [0x88a2b2, 0x9aa7ad, 0x7f96a8][v % 3]); m.floors(2.3, 2.3, .4, 10, .56, Gl); m.box(0, 0, 0, 2.6, .4, 2.6, 0x4f5660); m.box(0, 6.2, 0, 1.2, .35, 1.2, 0x5f6670); break;
    case 'factory': m.box(-.5, 0, 0, 3.6, 1.5, 3.2, 0x9ea3a4); for (let i = 0; i < 4; i++) m.roof(-1.85 + i * .9, 1.5, 0, .9, .4, 3.2, 0x6a7078); m.box(-.5, .1, 1.61, 1.4, .95, .04, 0x4f5660); m.floors(3.6, 3.2, 1, 1, .5, Gl); stack(1.8, -.9, .3, 3.5); stack(1.8, .35, .3, 2.9); m.cyl(1.75, 0, 1.45, .38, .95, 0xc8c2b4); break;
    case 'cbd': m.box(0, 0, 0, 2.5, 8.5, 2.5, [0x5f88a6, 0x6a9aa0, 0x7a8fae][v % 3]); m.floors(2.5, 2.5, .45, 14, .58, Gl); m.box(0, 8.5, 0, 1.8, 5, 1.8, 0x6d95ae); m.floors(1.8, 1.8, 8.6, 8, .6, Gl); m.box(0, 13.5, 0, .9, 1.2, .9, 0x88a0b0); m.cyl(0, 14.7, 0, .12, 1.4, 0xe4e7ea, .01, 5); break;
    case 'plant': for (let i = 0; i < 3; i++) { m.box(-2 + i * 2, 0, -1.2, 1.8, 1.8, 3, 0x9ea3a4); m.roof(-2 + i * 2, 1.8, -1.2, 1.8, .4, 3, 0x6a7078); } for (let i = 0; i < 4; i++) m.cyl(-2.3 + i * 1.5, 0, 1.75, .55, 1.6, 0xd2cfc6); stack(2.8, -2.2, .34, 5); stack(2.8, -.9, .34, 4.2); stack(2.8, .4, .34, 4.6); break;
    case 'techpark': m.box(-1, 0, -.8, 2.4, 2.1, 2.2, 0x9cc4d6); m.floors(2.4, 2.2, .1, 3, .66, 0xa8e0ee); m.cyl(1.25, 0, -1, .95, 1.5, 0xbfeaf4, .25, 12, 1); m.box(.8, 0, 1.25, 3, 1.1, 1.5, 0xd8e3e8); m.floors(3, 1.5, .1, 1, .8, 0x8fd4e6); tree(-1.9, 1.5, 1.3); tree(-1, 1.7, 1); break;
    case 'well': m.cyl(0, 0, 0, .34, .34, 0x9c9a92, .34, 10); m.cyl(0, .3, 0, .25, .05, 0x3f8fb8, .25, 10); m.box(-.3, 0, 0, .05, .75, .05, 0x6e4f33); m.box(.3, 0, 0, .05, .75, .05, 0x6e4f33); m.roof(0, .72, 0, .8, .24, .6, 0x8c3f36); break;
    case 'waterworks': m.cyl(-1, 0, 0, .85, 1.1, 0x9ec6d8, .85, 12); m.cyl(-1, 1.1, 0, .85, .2, 0x7da7bc, .05, 12); m.cyl(.8, 0, -.5, .55, 1.7, 0xc8d2d8, .55, 10); m.box(.8, 0, .85, 1.5, .8, .9, W_); m.win(.8, .3, 1.31, .9, .3); break;
    case 'dam': m.box(0, 0, 0, 5.8, 2, 1.2, 0xb6b2a8); m.box(0, 2, 0, 5.9, .2, .7, 0x8f8b82); for (let i = 0; i < 5; i++) m.box(-2.2 + i * 1.1, .2, .62, .5, 1.5, .1, 0x7fb6d0); m.box(0, 0, 1.2, 5.6, .06, 1.1, 0x5da7c8); break;
    case 'gen': m.box(0, 0, 0, 1.3, .7, 1, 0xd6a13a); m.cyl(-.3, .7, 0, .16, .3, 0x63605a); m.box(.72, 0, .4, .07, 1.6, .07, 0x7a5a3c); m.box(.72, 1.45, .4, .7, .05, .05, 0x7a5a3c); break;
    case 'coal': m.box(-.8, 0, .6, 2.8, 1.4, 2.5, 0x8f8f8d); m.cyl(1.4, 0, -1, .85, 2.6, 0xc9c6bf, .6, 12); m.cyl(-.9, 0, -1.2, .7, 2.2, 0xc9c6bf, .5, 12); stack(1.7, 1.2, .24, 4.4); m.box(-.5, 0, 1.7, 1.4, .4, .5, 0x28282c); break;
    case 'solar': for (let i = 0; i < 4; i++) for (let j = 0; j < 5; j++) { m.box(-2.4 + j * 1.2, .08, -1.8 + i * 1.2, .08, .22, .08, 0x777777); m.add(.25, (() => { const x = -2.4 + j * 1.2, z = -1.8 + i * 1.2, a = [x - .5, .24, z + .42], b = [x + .5, .24, z + .42], c = [x + .5, .62, z - .42], d = [x - .5, .62, z - .42]; return [a, b, c, a, c, d]; })(), 0x1f4f8f, 0); } break;
    case 'nuclear': m.cyl(-1.2, 0, 1.1, 1.1, 1.5, 0xe0ddd5, 1.05, 14); m.cyl(-1.2, 1.5, 1.1, 1.05, .8, 0xd2cec4, .1, 14); m.cyl(1.3, 0, -1.3, 1.2, 3.3, 0xcac7c0, .78, 14); m.cyl(-1, 0, -1.6, 1, 2.8, 0xcac7c0, .66, 14); m.box(1.5, 0, 1.5, 2.2, 1.2, 2, 0x9ea3a4); break;
    case 'school': m.box(0, 0, -.55, 3.4, 1.3, 1.25, 0xf1e4bf); m.floors(3.4, 1.25, .08, 2, .6, Gl); m.box(-1.45, 0, .55, .5, 1, 1.1, 0xf1e4bf); m.box(1.45, 0, .55, .5, 1, 1.1, 0xf1e4bf); m.roof(0, 1.3, -.55, 3.6, .4, 1.5, 0xb5533c); door(0, .08, 0x5b3f2c, .55, .4); flag(0, 1.1, 1.7, 0x2f62b5); break;
    case 'hischool': m.box(0, 0, -.8, 4.3, 2.3, 1.6, 0xefe0b8); m.floors(4.3, 1.6, .1, 3, .72, Gl); m.box(-1.9, 0, .7, .7, 1.5, 1.5, 0xe4d3a8); m.box(1.9, 0, .7, .7, 1.5, 1.5, 0xe4d3a8); m.box(0, 2.3, -.8, 4.4, .12, 1.7, 0x8c3f36); m.box(0, .01, 1, 2.6, .03, 1.5, 0xc2894f); flag(0, 1.6, 2.4, 0x2f62b5); break;
    case 'univ': m.box(0, 0, -.7, 5, 2.4, 2, 0xe6d5b8); m.floors(5, 2, .15, 3, .72, Gl); for (let i = 0; i < 6; i++) m.cyl(-1.5 + i * .6, 0, .42, .1, 1.8, 0xf4efe4); m.box(0, 1.8, .42, 3.6, .2, .5, 0xf4efe4); m.cyl(0, 2.4, -.7, .8, .7, 0xd9c7a6, .78, 12); m.cyl(0, 3.1, -.7, .78, .75, 0x4f8f8a, .04, 12); tree(-2.2, 1.7, 1.2); tree(2.2, 1.7, 1.2); break;
    case 'clinic': m.box(0, 0, 0, 2.5, 1.05, 1.6, 0xf6f6f2); m.box(0, 1.05, 0, 2.6, .1, 1.7, 0x4fa66f); m.floors(2.5, 1.6, .25, 1, .55, Gl); door(0, .81, 0x4fa66f, .55, .4); cross(0, 1, .83, 0x3fa863); break;
    case 'hospital': m.box(0, 0, 0, 4.2, 1.2, 3, 0xf4f4ef); m.box(-.3, 1.2, -.3, 2.8, 3.4, 2, 0xf8f8f4); m.floors(2.8, 2, 1.3, 5, .64, Gl); m.floors(4.2, 3, .1, 1, 1, Gl); cross(-.3, 4.2, .72, 0xd63c35); m.box(1.2, 1.2, .9, 1.2, .05, 1.1, 0xd9d9d0); m.cyl(1.2, 1.25, .9, .42, .02, 0xd63c35, .42, 10); break;
    case 'medcenter': for (const a of [-1, 1]) { m.box(a * 1.45, 0, -.5, 2, 6.5, 2.4, 0xf6f6f2); m.floors(2, 2.4, 1.3, 8, .62, Gl); } m.box(0, 0, .3, 5.5, 1.2, 3.8, 0xeef0ea); m.box(0, 3, -.5, 1.1, .6, .7, 0xbfe3ee, 1); cross(-1.45, 6.2, .73, 0xd63c35); cross(1.45, 6.2, .73, 0xd63c35); break;
    case 'police': m.box(0, 0, 0, 1.55, .95, 1.5, 0xe8edf2); m.box(0, .95, 0, 1.65, .14, 1.6, 0x2f4f8f); m.box(0, .62, .76, 1.56, .12, .03, 0x2f4f8f); door(0, .76, 0x2f4f8f, .5, .34); m.cyl(.55, 1.09, .5, .09, .14, 0xe0423b); m.cyl(.3, 1.09, .5, .09, .14, 0x3f7ae0); break;
    case 'policehq': m.box(0, 0, 0, 3.4, 2.6, 2.3, 0xdde3ea); m.floors(3.4, 2.3, .15, 3, .78, 0x88a7c8); m.box(0, 2.6, 0, 3.5, .16, 2.4, 0x2f4f8f); flag(1.3, 1.45, 2.3, 0x2f4f8f); door(0, 1.17, 0x2f4f8f, .6, .6); break;
    case 'base': m.box(-1.3, 0, -.9, 2.7, 1.2, 2.5, 0x7a8560); m.roof(-1.3, 1.2, -.9, 2.8, .55, 2.6, 0x5f6a4b); m.box(1.7, 0, -1.1, 1.5, .9, 1.9, 0x6a7558); m.box(.3, .02, 1.5, 5.2, .05, 1.1, 0x8d8a78); for (let i = 0; i < 3; i++) { m.box(-1.5 + i * 1.5, .07, 1.5, .8, .32, .46, 0x4f5a3c); m.box(-1.2 + i * 1.5, .34, 1.5, .5, .05, .05, 0x3a4230); } flag(2.6, 1.9, 2.3, 0x2f62b5); break;
    case 'trash': m.box(-.3, 0, 0, 1, .46, 1.4, 0x5f7f6a); m.cyl(.5, 0, .4, .3, .34, 0x8a7a55, .08, 7); m.cyl(.48, 0, -.3, .36, .4, 0x70654d, .08, 7); break;
    case 'recycle': m.box(-.4, 0, 0, 3.5, 1.5, 3, 0x6fa080); m.roof(-.4, 1.5, 0, 3.6, .5, 3.1, 0x4f7d62); m.box(1.9, 0, 0, 1, .8, 2, 0x8fae8f); m.cyl(1.9, .8, 0, .5, .5, 0x4fa66f, .04, 7); stack(-1.7, 1.1, .16, 2.6, 0x9aa5a0); break;
    case 'park': m.cyl(.45, .02, .45, .75, .05, 0x54a9cc, .75, 12); for (const p of [[-.9, -.9, 1.3], [.9, -.9, 1], [-.9, .85, 1.1], [-.2, -.2, .8]]) tree(p[0], p[1], p[2]); m.box(0, .02, -1.3, 2.8, .03, .22, 0xd9c39a); m.box(-1.3, .02, 0, .22, .03, 2.8, 0xd9c39a); break;
    case 'port': m.box(.5, 0, .9, 3.8, .4, 2, 0x8a8a84); for (let i = 0; i < 4; i++) for (let j = 0; j < 2; j++) m.box(-.5 + i * .72, .4, .5 + j * .75, .62, .3 + (i + j) % 2 * .3, .34, [0xc8483f, 0x3f8fd8, 0xe0a83a, 0x3fae6e][(i + j) % 4]); m.box(-1.7, 0, -1, 1.2, 1.4, 1.6, 0xa5a59d); for (const x of [.5, 1.9]) { m.box(x - .45, .4, -.5, .08, 2.6, .08, 0xe0983a); m.box(x + .45, .4, -.5, .08, 2.6, .08, 0xe0983a); m.box(x, 3, -.5, 1.1, .1, .1, 0xe0983a); m.box(x, 3, .3, .1, .1, 1.7, 0xe0983a); } break;
    case 'airport': m.box(0, .01, 1.5, 7.8, .04, 1.3, 0x45474c); for (let i = 0; i < 7; i++) m.box(-3.2 + i * 1.07, .05, 1.5, .5, .01, .06, 0xf2f2ee); m.box(-.5, 0, -1, 5.2, 1.1, 2, 0xdfe6ea); m.floors(5.2, 2, .15, 1, 1, Gl); m.cyl(2.8, 0, -1, .3, 2.5, 0xe8e8e2, .22); m.cyl(2.8, 2.5, -1, .55, .4, 0x7dbad0, .5, 8, 1); m.box(.5, .1, .5, 1.6, .18, .22, 0xf4f4f4); m.box(.5, .12, .5, .3, .06, 1, 0xf4f4f4); m.box(1.25, .2, .5, .14, .36, .05, 0x2f62b5); break;
    case 'parliament': m.box(0, 0, -.2, 4.6, 1.6, 2.7, 0xf0ebdf); m.floors(4.6, 2.7, .25, 1, 1, Gl); for (let i = 0; i < 8; i++) m.cyl(-1.75 + i * .5, 0, 1.2, .09, 1.5, 0xfbf8f0); m.box(0, 1.5, 1.2, 4, .16, .3, 0xfbf8f0); m.cyl(0, 1.6, -.2, 1.05, .6, 0xe7e0d0, 1, 14); m.cyl(0, 2.2, -.2, 1, 1.1, 0xd4b25a, .06, 14); flag(0, -.2, 4, 0x2f62b5); break;
    default: m.box(0, 0, 0, 1, 1, 1, 0xffffff);
  }
}
function drawHall(m, lv) { const f = Math.min(5, 1 + Math.floor(lv / 2)); m.box(0, -.7, 0, 2.94, .74, 2.94, 0x9a917f); m.box(0, 0, 0, 2.5, f * .72, 2.1, 0xf2ead8); m.floors(2.5, 2.1, .08, f, .72, 0x8fc6d8); m.roof(0, f * .72, 0, 2.8, .7, 2.45, 0x8c3f36); for (let i = 0; i < 4; i++) m.cyl(-.75 + i * .5, 0, 1.2, .07, .86, 0xfbf8f0, .07, 6); m.box(0, .84, 1.2, 1.9, .1, .3, 0xfbf8f0); m.box(1.15, 0, 1.3, .05, f * .72 + 1.3, .05, 0xdddddd); m.box(1.36, f * .72 + .98, 1.3, .4, .26, .03, 0x2f62b5); }

/* ---------- the world object ---------- */
const W = {
  H: new Float32Array((N + 1) * (N + 1)), T: new Uint8Array(N * N), occ: new Int32Array(N * N), wear: new Float32Array(N * N), road: new Uint8Array(N * N), reserved: new Uint8Array(N * N), treeAt: new Map(),
  cam: { x: 90, z: 90, dist: 26, yaw: .7, tDist: 26, tx: 90, tz: 90 }, agents: [], arch: {}, dirty: false, roadCount: 0, treeTotal: 1, treeLive: 1, sites: new Map(), start: null
};

W.gen = function (seed) {
  const R = RNG(seed), G = 64, g1 = new Float32Array(G * G); for (let i = 0; i < G * G; i++) g1[i] = R();
  const smooth = t => t * t * (3 - 2 * t), vn = (x, z) => { const a = Math.floor(x), b = Math.floor(z), f = smooth(x - a), e = smooth(z - b), q = (p, r) => g1[((p % G) + G) % G + (((r % G) + G) % G) * G]; return (q(a, b) * (1 - f) + q(a + 1, b) * f) * (1 - e) + (q(a, b + 1) * (1 - f) + q(a + 1, b + 1) * f) * e; };
  const fbm = (x, z) => vn(x, z) * .55 + vn(x * 2.1 + 9, z * 2.1 + 4) * .28 + vn(x * 4.3 + 3, z * 4.3 + 7) * .12 + vn(x * 8.7, z * 8.7) * .05;
  W.fbm = fbm;
  const E = new Float32Array((N + 1) * (N + 1));
  for (let z = 0; z <= N; z++) for (let x = 0; x <= N; x++) { const nx = (x - N / 2) / (N / 2), nz = (z - N / 2) / (N / 2), d = Math.sqrt(nx * nx + nz * nz); E[x + z * (N + 1)] = fbm(x * .022 + 5, z * .022 + 11) * 1.42 - d * d * 1.18 - .075; }
  /* two rivers from the highest ground down to the sea */
  const riv = new Uint8Array((N + 1) * (N + 1)), carve = (sx, sz) => {
    let x = sx, z = sz, dir = Math.atan2(z - N / 2, x - N / 2);
    for (let s = 0; s < 340; s++) {
      const i = Math.round(x) + Math.round(z) * (N + 1); if (x < 2 || z < 2 || x > N - 2 || z > N - 2 || E[i] < -.05) break;
      const r = Math.min(3.3, 1.55 + s * .017);
      for (let a = -4; a <= 4; a++) for (let b = -4; b <= 4; b++) { const p = Math.round(x) + a, q = Math.round(z) + b; if (p < 0 || q < 0 || p > N || q > N) continue; const dd = Math.hypot(a, b); if (dd <= r) riv[p + q * (N + 1)] = 1; }
      let best = dir, bv = 1e9; for (let k = -3; k <= 3; k++) { const t = dir + k * .24, px = Math.round(x + Math.cos(t) * 3), pz = Math.round(z + Math.sin(t) * 3); if (px < 0 || pz < 0 || px > N || pz > N) continue; const v = E[px + pz * (N + 1)] + R() * .05 + Math.abs(k) * .004; if (v < bv) { bv = v; best = t; } }
      dir = dir * .55 + best * .45; x += Math.cos(dir) * 1.1; z += Math.sin(dir) * 1.1;
    }
  };
  const tops = []; for (let i = 0; i < 500; i++) { const x = 30 + R() * (N - 60) | 0, z = 30 + R() * (N - 60) | 0, v = E[x + z * (N + 1)]; if (v > .23 && v < .36) tops.push([v, x, z]); }
  tops.sort((p, q) => q[0] - p[0]); const rs = []; for (const t of tops) { if (rs.every(r => Math.hypot(r[1] - t[1], r[2] - t[2]) > 50)) rs.push(t); if (rs.length >= 3) break; }
  rs.forEach(r => carve(r[1], r[2]));
  const yOf = e => e < 0 ? e * 7 : e < .2 ? e * 1.5 : .3 + Math.pow(e - .2, 1.7) * 27;
  const rd = new Uint8Array((N + 1) * (N + 1)).fill(9); for (let i = 0; i < rd.length; i++) if (riv[i]) rd[i] = 0;
  for (let st = 1; st <= 4; st++) for (let z = 0; z <= N; z++) for (let x = 0; x <= N; x++) { const i = x + z * (N + 1); if (rd[i] !== 9) continue; for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]) { const p = x + a, q = z + b; if (p >= 0 && q >= 0 && p <= N && q <= N && rd[p + q * (N + 1)] === st - 1) { rd[i] = st; break; } } }
  const bank = [-.44, .03, .12, .22, .34], blend = [1, .92, .74, .5, .25];
  for (let z = 0; z <= N; z++) for (let x = 0; x <= N; x++) { const i = x + z * (N + 1); let y = yOf(E[i]); if (rd[i] <= 4 && y > bank[rd[i]]) y += (bank[rd[i]] - y) * blend[rd[i]]; W.H[i] = y; }
  for (let z = 0; z < N; z++) for (let x = 0; x < N; x++) {
    const c = ci(x, z), h = (W.H[x + z * (N + 1)] + W.H[x + 1 + z * (N + 1)] + W.H[x + (z + 1) * (N + 1)] + W.H[x + 1 + (z + 1) * (N + 1)]) / 4, isR = riv[x + z * (N + 1)] && h < -.05;
    let t = 3; if (h < -.04) t = isR ? 1 : 0; else if (h < .1 && !isR) t = 2; else if (h > 3.2) t = 6; else if (h > 1.35) t = 5; else if (fbm(x * .05 + 40, z * .05 + 2) > .52) t = 4;
    W.T[c] = t;
  }
  /* best first valley: flat land by a river, not too close to the sea */
  let best = -1e9, bx = N / 2, bz = N / 2;
  for (let i = 0; i < 2600; i++) {
    const x = 18 + R() * (N - 36) | 0, z = 18 + R() * (N - 36) | 0; let flat = 0, water = 0, bad = 0;
    for (let a = -9; a <= 9; a += 3) for (let b = -9; b <= 9; b += 3) { const t = W.T[ci(x + a, z + b)]; if (t === 3 || t === 4) flat++; else if (t === 1) water++; else bad++; }
    const s = flat * 1 + Math.min(water, 3) * 3 - bad * 1.4 - Math.hypot(x - N / 2, z - N / 2) * .24; if (s > best && water > 0) { best = s; bx = x; bz = z; }
  }
  W.start = { x: bx, z: bz };
};
W.h = function (x, z) { x = clamp(x, 0, N - .001); z = clamp(z, 0, N - .001); const a = x | 0, b = z | 0, f = x - a, e = z - b, q = (p, r) => W.H[p + r * (N + 1)]; return (q(a, b) * (1 - f) + q(a + 1, b) * f) * (1 - e) + (q(a, b + 1) * (1 - f) + q(a + 1, b + 1) * f) * e; };

W.paintGround = function () {
  const c = document.createElement('canvas'); c.width = c.height = TEX; const g = c.getContext('2d'); W.gctx = g; W.gcv = c; W.paintRect(0, 0, TEX, TEX); g.lineCap = 'round'; g.lineJoin = 'round';
  const tx = new THREE.CanvasTexture(c); tx.anisotropy = MOBILE ? 2 : 4; tx.wrapS = tx.wrapT = THREE.ClampToEdgeWrapping; W.gtex = tx;
};
W.paintRect = function (x0, y0, x1, y1) {
  const g = W.gctx, w = x1 - x0, h0 = y1 - y0, im = g.createImageData(w, h0), d = im.data, k = N / TEX, pal = { sea: [188, 178, 132], sand: [226, 207, 156], g1: [120, 162, 80], g2: [92, 142, 66], f: [72, 128, 58], hill: [132, 142, 92], rock: [132, 126, 118], snow: [226, 228, 228], dirt: [156, 132, 90] }; if (typeof ISO_ON !== 'undefined' && ISO_ON) { pal.g1 = [104, 168, 70]; pal.g2 = [66, 134, 60]; pal.f = [48, 110, 52]; pal.hill = [80, 150, 68]; pal.rock = [98, 130, 82]; }
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
    const wx = x * k, wz = y * k, h = W.h(wx, wz), n = W.fbm(wx * .16, wz * .16), n2 = W.fbm(wx * .9 + 7, wz * .9), t = W.T[ci(Math.min(N - 1, wx | 0), Math.min(N - 1, wz | 0))]; let C;
    if (h < .1) { const m = clamp((h + .2) / .3); C = [pal.sea[0] + (pal.sand[0] - pal.sea[0]) * m, pal.sea[1] + (pal.sand[1] - pal.sea[1]) * m, pal.sea[2] + (pal.sand[2] - pal.sea[2]) * m]; }
    else { const v = clamp((n - .36) / .28), base = [pal.g1[0] + (pal.g2[0] - pal.g1[0]) * v, pal.g1[1] + (pal.g2[1] - pal.g1[1]) * v, pal.g1[2] + (pal.g2[2] - pal.g1[2]) * v]; C = base; if (h < .2) { const m = clamp((h - .1) / .1); C = [pal.sand[0] + (base[0] - pal.sand[0]) * m, pal.sand[1] + (base[1] - pal.sand[1]) * m, pal.sand[2] + (base[2] - pal.sand[2]) * m]; } if (t === 4) C = [C[0] * .8 + pal.f[0] * .2, C[1] * .8 + pal.f[1] * .2, C[2] * .8 + pal.f[2] * .2]; if (h > 1.2) { const m = clamp((h - 1.2) / 1.6); C = [C[0] + (pal.hill[0] - C[0]) * m, C[1] + (pal.hill[1] - C[1]) * m, C[2] + (pal.hill[2] - C[2]) * m]; } if (h > 2.8) { const m = clamp((h - 2.8) / 1.5); C = [C[0] + (pal.rock[0] - C[0]) * m, C[1] + (pal.rock[1] - C[1]) * m, C[2] + (pal.rock[2] - C[2]) * m]; } if (h > 8.6) { const m = clamp((h - 8.6) / 2.4) * .72 * clamp(n2 * 1.5); C = [C[0] + (pal.snow[0] - C[0]) * m, C[1] + (pal.snow[1] - C[1]) * m, C[2] + (pal.snow[2] - C[2]) * m]; } }
    const hx = W.h(wx + .6, wz) - W.h(wx - .6, wz), hz = W.h(wx, wz + .6) - W.h(wx, wz - .6), sh = (.94 + n2 * .13) * clamp(1 + (-hx * .55 + hz * .45) * .34, .7, 1.18), i = ((x - x0) + (y - y0) * w) * 4; d[i] = C[0] * sh; d[i + 1] = C[1] * sh; d[i + 2] = C[2] * sh; d[i + 3] = 255;
  }
  g.putImageData(im, x0, y0); W.dirty = true;
};
const ROAD_STYLE = [null, ['#b89f70', .26, 0], ['#a98a58', .42, 0], ['#8f8a7c', .52, '#6f6b60'], ['#4f5157', .68, '#34353a']];
W.paintRoad = function (x, z) {
  const t = W.road[ci(x, z)]; if (!t) return; const g = W.gctx, p = TEX / N, X = (x + .5) * p, Z = (z + .5) * p, st = ROAD_STYLE[t], lines = [];
  for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { if (!a && !b || !inMap(x + a, z + b) || (W.plan && a && b)) continue; if (W.road[ci(x + a, z + b)] >= Math.min(t, 2)) lines.push([(x + a + .5) * p, (z + b + .5) * p]); }
  const draw = (col, w) => { g.strokeStyle = col; g.fillStyle = col; g.lineWidth = w * p; g.beginPath(); g.arc(X, Z, w * p / 2, 0, 7); g.fill(); g.beginPath(); for (const l of lines) { g.moveTo(X, Z); g.lineTo(l[0], l[1]); } g.stroke(); };
  if (st[2]) draw(st[2], st[1] + .14); draw(st[0], st[1]);
  if (t === 4) { g.strokeStyle = 'rgba(240,230,190,.72)'; g.lineWidth = .05 * p; g.setLineDash([.22 * p, .22 * p]); g.beginPath(); for (const l of lines) { g.moveTo(X, Z); g.lineTo(l[0], l[1]); } g.stroke(); g.setLineDash([]); }
  W.dirty = true; if (t >= 2) { const c = ci(x, z); for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { if ((!a && !b) || !inMap(x + a, z + b)) continue; const d = ci(x + a, z + b); if (W.road[d] >= 2 && (W.T[c] === 1 || W.T[d] === 1)) W.bridgeSeg(x, z, a, b, c, d); } }
};
W.bridgeSeg = function (x, z, a, b, c, d) { if (!W._br) W._br = new Set(); const key = Math.min(c, d) + '_' + Math.max(c, d); if (W._br.has(key) || W._br.size >= 700) return; W._br.add(key); const m = W.brMesh, i = W._br.size - 1, o = W._o; o.position.set(x + .5 + a / 2, .14, z + .5 + b / 2); o.rotation.set(0, Math.atan2(a, b), 0); o.scale.set(.66, 1, Math.hypot(a, b) + .14); o.updateMatrix(); m.setMatrixAt(i, o.matrix); m.count = W._br.size; m.instanceMatrix.needsUpdate = true; W.needShadow = true; };

W.init = function (canvas, seed) {
  W.gen(seed); W.paintGround(); W._m4 = new THREE.Matrix4(); W._o = new THREE.Object3D();
  const r = W.renderer = new THREE.WebGLRenderer({ canvas, antialias: !MOBILE, powerPreference: 'high-performance' });
  r.setPixelRatio(Math.min(devicePixelRatio || 1, MOBILE ? 1.5 : 2)); r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap; r.shadowMap.autoUpdate = false;
  const sc = W.scene = new THREE.Scene(); sc.background = new THREE.Color(0x8fcfe8); sc.fog = new THREE.FogExp2(0xbfdfea, .0035);
  W.camera = new THREE.PerspectiveCamera(36, 1, .3, 1300);
  W.hemi = new THREE.HemisphereLight(0xdff2ff, 0x7c8a5a, .62); sc.add(W.hemi);
  const sun = W.sun = new THREE.DirectionalLight(0xfff2d8, .85); sun.castShadow = true; sun.shadow.mapSize.set(MOBILE ? 1024 : 2048, MOBILE ? 1024 : 2048); sun.shadow.bias = -.0012; sun.shadow.normalBias = .03; sc.add(sun, sun.target);
  /* terrain */
  const gg = W.groundGeo = new THREE.BufferGeometry(), P = new Float32Array((N + 1) * (N + 1) * 3), UV = new Float32Array((N + 1) * (N + 1) * 2), I = new Uint32Array(N * N * 6);
  for (let z = 0, j = 0; z <= N; z++) for (let x = 0; x <= N; x++, j++) { P[j * 3] = x; P[j * 3 + 1] = W.H[j]; P[j * 3 + 2] = z; UV[j * 2] = x / N; UV[j * 2 + 1] = 1 - z / N; }
  for (let z = 0, q = 0; z < N; z++) for (let x = 0; x < N; x++) { const a = x + z * (N + 1), b = a + 1, c = a + N + 1, d = c + 1; I[q++] = a; I[q++] = c; I[q++] = b; I[q++] = b; I[q++] = c; I[q++] = d; }
  gg.setAttribute('position', new THREE.BufferAttribute(P, 3)); gg.setAttribute('uv', new THREE.BufferAttribute(UV, 2)); gg.setIndex(new THREE.BufferAttribute(I, 1)); gg.computeVertexNormals();
  W.gtex.flipY = true; const ground = new THREE.Mesh(gg, new THREE.MeshLambertMaterial({ map: W.gtex })); ground.receiveShadow = true; sc.add(ground);
  /* sea and rivers */
  const dt = new Uint8Array((N + 1) * (N + 1) * 4); for (let z = 0; z <= N; z++) for (let x = 0; x <= N; x++) { const i = (x + z * (N + 1)) * 4, v = clamp(-W.H[x + z * (N + 1)] / 2.4) * 255; dt[i] = v; dt[i + 1] = v; dt[i + 2] = v; dt[i + 3] = 255; }
  const depth = new THREE.DataTexture(dt, N + 1, N + 1, THREE.RGBAFormat); depth.magFilter = depth.minFilter = THREE.LinearFilter; depth.wrapS = depth.wrapT = THREE.ClampToEdgeWrapping; depth.needsUpdate = true; W.depthData = dt; W.depthTex = depth;
  W.waterU = { sK: { value: 1 }, t: { value: 0 }, d: { value: depth }, L: { value: 1 }, N: { value: N } };
  const water = W.water = new THREE.Mesh(new THREE.PlaneGeometry(N * 7, N * 7), new THREE.ShaderMaterial({
    uniforms: W.waterU, transparent: true,
    vertexShader: 'varying vec3 p;void main(){vec4 w=modelMatrix*vec4(position,1.);p=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
    fragmentShader: 'uniform float t,L,N,sK;uniform sampler2D d;varying vec3 p;float W_(vec2 q){return sin(q.x)*cos(q.y);}float H(vec2 q){mat2 r=mat2(.8,.6,-.6,.8);float a=W_(q*1.1+vec2(t*.7,t*.5));q=r*q;a+=.55*W_(q*2.3-vec2(t*.9,-t*.6));q=r*q;a+=.28*W_(q*4.7+vec2(-t*1.2,t*.8));return a;}void main(){vec2 u=p.xz/N,q=p.xz;float e=(u.x<0.||u.y<0.||u.x>1.||u.y>1.)?1.:texture2D(d,u).r,h=H(q);float dl=length(cameraPosition-p),nr=smoothstep(105.,16.,dl);vec3 n=normalize(vec3((h-H(q+vec2(.12,0.)))*nr,.42,(h-H(q+vec2(0.,.12)))*nr)),v=normalize(cameraPosition-p),s=normalize(vec3(-.48,.72,.5)),b=normalize(v+s);float sp=pow(max(dot(n,b),0.),120.)*.9*nr*sK,fr=pow(1.-max(dot(n,v),0.),3.);vec3 c=mix(vec3(.36,.86,.78),vec3(.1,.57,.68),smoothstep(.0,.2,e));c=mix(c,vec3(.04,.27,.49),smoothstep(.18,.72,e));c=mix(c,vec3(.64,.84,.93),fr*.42);float f=smoothstep(.055,.012,e+.012*h)*(.58+.42*sin(e*120.-t*1.6));c=mix(c,vec3(.97,.99,.96),clamp(f,0.,1.)*.8);c=c*L+sp*vec3(1.,.95,.82)*L*L;gl_FragColor=vec4(c,mix(.74,.96,smoothstep(.0,.3,e)));}'
  }));
  water.rotation.x = -Math.PI / 2; water.position.set(N / 2, 0, N / 2); sc.add(water);
  /* bridges appear wherever people keep crossing a river */
  const bg = new THREE.BoxGeometry(1.04, .1, 1.04); W.brMesh = new THREE.InstancedMesh(bg, new THREE.MeshLambertMaterial({ color: 0x8c6a45 }), 700); W.brMesh.count = 0; W.brMesh.frustumCulled = false; sc.add(W.brMesh);
  W.initTrees(seed); W.initBuildMat(); W.initPeople();
  const ring = W.ring = new THREE.Mesh(new THREE.RingGeometry(.86, 1, 40), new THREE.MeshBasicMaterial({ color: 0xffd34d, transparent: true, opacity: .95, side: THREE.DoubleSide, depthTest: false })); ring.rotation.x = -Math.PI / 2; ring.visible = false; ring.renderOrder = 5; sc.add(ring);
  W.cam.x = W.cam.tx = W.start.x; W.cam.z = W.cam.tz = W.start.z; W.resize(); addEventListener('resize', W.resize); W.bindInput(canvas);
};
W.resize = function () { const w = innerWidth, h = innerHeight; W.renderer.setSize(w, h, false); W.camera.aspect = w / h; W.camera.updateProjectionMatrix(); };

W.initTrees = function (seed) {
  const R = RNG(seed + 77), m = new MB(); m.cyl(0, 0, 0, .09, .36, 0x6e4f33, .06, 5); m.cyl(0, .26, 0, .48, .72, 0xffffff, .1, 6); m.cyl(0, .72, 0, .34, .66, 0xe9f4df, 0, 6);
  const geo = m.build(), mat = new THREE.MeshLambertMaterial({ vertexColors: true }), list = [];
  for (let z = 0; z < N; z++) for (let x = 0; x < N; x++) { const t = W.T[ci(x, z)], p = t === 4 ? .62 : t === 5 ? .3 : t === 3 ? .035 : t === 6 ? .05 : 0; if (R() < p && (Math.hypot(x - W.start.x, z - W.start.z) > 5 || R() < .15)) list.push([x, z]); }
  const cap = MOBILE ? 3000 : 5600; while (list.length > cap) list.splice(R() * list.length | 0, 1);
  const im = W.trees = new THREE.InstancedMesh(geo, mat, list.length), dummy = new THREE.Object3D(), C = new THREE.Color(); im.castShadow = !MOBILE; im.receiveShadow = false; im.frustumCulled = false;
  list.forEach((l, i) => {
    const px = l[0] + .2 + R() * .6, pz = l[1] + .2 + R() * .6, s = .85 + R() * .85; dummy.position.set(px, W.h(px, pz) - .04, pz); dummy.rotation.y = R() * 6; dummy.scale.set(s, s * (.9 + R() * .45), s); dummy.updateMatrix(); im.setMatrixAt(i, dummy.matrix);
    const v = R(); C.setRGB(.3 + v * .16, .56 + v * .14, .24 + v * .07); im.setColorAt(i, C); const c = ci(l[0], l[1]); if (!W.treeAt.has(c)) W.treeAt.set(c, []); W.treeAt.get(c).push(i);
  });
  W.treeTotal = W.treeLive = Math.max(1, list.length);
};
W.clearTrees = function (x, z, w, d) {
  let ch = false; const zero = new THREE.Matrix4().makeScale(0, 0, 0);
  for (let a = x; a < x + w; a++) for (let b = z; b < z + d; b++) { const c = ci(a, b), l = W.treeAt.get(c); if (l) { l.forEach(i => { W.trees.setMatrixAt(i, zero); W.treeLive--; }); W.treeAt.delete(c); ch = true; } }
  if (ch) { W.trees.instanceMatrix.needsUpdate = true; W.needShadow = true; }
};
W.initBuildMat = function () {
  W.nightU = { value: 0 };
  const mat = W.bmat = new THREE.MeshLambertMaterial({ vertexColors: true });
  if (W.hasAtlas) { const tx = new THREE.Texture(W.atlasImg); tx.anisotropy = MOBILE ? 2 : 8; tx.needsUpdate = true; mat.map = tx; }
  mat.onBeforeCompile = s => { s.uniforms.uNight = W.nightU; s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nattribute float aGlow;varying float vGlow;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvGlow=aGlow;'); s.fragmentShader = s.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uNight;varying float vGlow;').replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\nfloat gl=smoothstep(.2,.45,vGlow),lt=smoothstep(.75,.95,vGlow);float fr=pow(1.-clamp(dot(normalize(normal),normalize(vViewPosition)),0.,1.),2.6);totalEmissiveRadiance+=gl*(1.-uNight)*(vec3(.06,.12,.18)+fr*vec3(.5,.62,.72))+lt*uNight*vec3(.98,.72,.37);\n#ifdef USE_MAP\nfloat wm=texture2D(map,vUv).a,rr=fract(sin(dot(floor(vUv*vec2(58.,44.)),vec2(12.9898,78.233)))*43758.5453);totalEmissiveRadiance+=wm*(smoothstep(.7,.74,rr)*uNight*vec3(.92,.66,.33)+(1.-uNight)*vec3(.025,.045,.065));\n#endif\n'); };
};
W.geoFor = function (t, v) { const key = t + v; if (!W['g_' + key]) { const m = new MB(); if (t === 'hall') drawHall(m, v); else drawB(m, t, v); W['g_' + key] = m.build(); } return W['g_' + key]; };
W.inst = function (t, v) { const key = t + v; if (!W.arch[key]) { const im = new THREE.InstancedMesh(W.geoFor(t, v), W.bmat, MAX_INST); im.count = 0; im.castShadow = im.receiveShadow = true; im.frustumCulled = false; W.scene.add(im); W.arch[key] = { im, list: [] }; } return W.arch[key]; };

/* building placement */
W.canPlace = function (x, z, w, d, soft) {
  if (x < 1 || z < 1 || x + w >= N - 1 || z + d >= N - 1) return false; let lo = 99, hi = -99;
  for (let a = x; a < x + w; a++) for (let b = z; b < z + d; b++) { const c = ci(a, b), t = W.T[c]; if (t < 2 || t === 6 || W.occ[c] || W.reserved[c] || W.road[c] >= 2) return false; const y = W.h(a + .5, b + .5); lo = Math.min(lo, y); hi = Math.max(hi, y); }
  return hi - lo < .75 && lo > .06;
};
W.doorFor = function (x, z, w, d, cx, cz) {
  const opts = [[x + (w >> 1), z + d, 0]], sq = w === d; opts.push([x + (w >> 1), z - 1, 2]); if (sq) opts.push([x + w, z + (d >> 1), 1], [x - 1, z + (d >> 1), 3]);
  let best = null, bs = 1e9; for (const o of opts) { if (!inMap(o[0], o[1])) continue; const c = ci(o[0], o[1]); if (W.T[c] < 2 || W.occ[c]) continue; const s = Math.hypot(o[0] - cx, o[1] - cz) - W.road[c] * 2; if (s < bs) { bs = s; best = o; } } return best;
};
W.findSpot = function (city, t, R0) {
  const b = BT[t] || { s: [3, 3] }, w = b.s[0], d = b.s[1], big = w * d >= 16, out = t === 'farm' || t === 'bigfarm' || b.cat === 'power' && t !== 'gen', dirty = (b.g && b.g.dirty) > 0;
  for (let round = 0; round < 5; round++) {
    const Rr = (R0 || 5 + Math.sqrt(city.n + 1) * 1.8) * (1 + round * .55); let best = null, bs = -1e9;
    for (let i = 0; i < 90; i++) {
      const a = Math.random() * 6.2832, r = Math.sqrt(Math.random()) * Rr + (out ? Rr * .35 : 0), x = Math.round(city.x + Math.cos(a) * r - w / 2), z = Math.round(city.z + Math.sin(a) * r - d / 2); if (!W.canPlace(x, z, w, d, !big)) continue; const door = W.doorFor(x, z, w, d, city.x, city.z); if (!door) continue;
      let near = 0, rw = 0; for (let p = -3; p <= w + 2; p += 2) for (let q = -3; q <= d + 2; q += 2) { if (!inMap(x + p, z + q)) continue; const c = ci(x + p, z + q); if (W.T[c] === 1) rw++; if (W.road[c] >= 2) near++; if (W.occ[c]) near += .3; }
      const dist = Math.hypot(x + w / 2 - city.x, z + d / 2 - city.z); let s = -dist * (out ? .15 : .75) + near * .9 + Math.random() * 1.6; if (t === 'farm' || t === 'bigfarm') s += rw * 1.3; if (dirty) s += dist * .7 - rw * .5; if (t === 'well') s += rw * .6;
      if (s > bs) { bs = s; best = { x, z, w, d, door, rw }; }
    }
    if (best) return best;
  }
  return null;
};
W.occupy = function (b) { if (inMap(b.door[0], b.door[1])) W.reserved[ci(b.door[0], b.door[1])] = 1; for (let a = b.x; a < b.x + b.w; a++) for (let c = b.z; c < b.z + b.d; c++) W.occ[ci(a, c)] = b.id; W.clearTrees(b.x, b.z, b.w, b.d); };
W.placeInstance = function (b) {
  const A = W.inst(b.t, b.v); if (A.list.length >= MAX_INST) return; const im = A.im, i = A.list.length, cx = b.x + b.w / 2, cz = b.z + b.d / 2;
  const o = new THREE.Object3D(); o.position.set(cx, W.h(cx, cz) + .02, cz); o.rotation.y = b.rot * Math.PI / 2; o.scale.set(b.sc || 1, W.heightK ? W.heightK(b) : 1, b.sc || 1); o.updateMatrix(); im.setMatrixAt(i, o.matrix); im.count = i + 1; im.instanceMatrix.needsUpdate = true; A.list.push(b.id); b._i = i; W.needShadow = true;
};
W.removeInstance = function (b) {
  const A = W.arch[b.t + b.v]; if (!A || b._i == null) return; const last = A.list.length - 1, m = new THREE.Matrix4();
  if (b._i !== last) { A.im.getMatrixAt(last, m); A.im.setMatrixAt(b._i, m); A.list[b._i] = A.list[last]; const o = G.byId.get(A.list[b._i]); if (o) o._i = b._i; } A.list.pop(); A.im.count = last; A.im.instanceMatrix.needsUpdate = true; b._i = null; W.needShadow = true;
};
W.addSite = function (b) {
  const g = W.geoFor(b.t, b.v), geo = new THREE.BufferGeometry(); for (const n of ['position', 'normal', 'color', 'aGlow', 'uv']) geo.setAttribute(n, g.attributes[n]); geo.boundingSphere = g.boundingSphere; geo.setDrawRange(0, 0);
  const cx = b.x + b.w / 2, cz = b.z + b.d / 2, y = b.t === 'reclaim' ? .02 : W.h(cx, cz) + .02, gr = new THREE.Group(), mesh = new THREE.Mesh(geo, W.bmat); mesh.castShadow = mesh.receiveShadow = true; mesh.scale.set(b.sc || 1, W.heightK ? W.heightK(b) : 1, b.sc || 1); gr.add(mesh); gr.position.set(cx, y, cz); gr.rotation.y = b.rot * Math.PI / 2;
  const box = new THREE.Box3().setFromBufferAttribute(g.attributes.position), top = Math.max(.9, box.max.y + .15), pm = new THREE.MeshLambertMaterial({ color: 0xd8b24a }), pg = new THREE.CylinderGeometry(.035, .035, top, 5);
  if (b.t !== 'reclaim') for (const a of [-1, 1]) for (const e of [-1, 1]) { const p = new THREE.Mesh(pg, pm); p.position.set(a * (b.w / 2 - .08), top / 2, e * (b.d / 2 - .08)); gr.add(p); }
  const bar = new THREE.Mesh(new THREE.BoxGeometry(1, .09, .09), new THREE.MeshBasicMaterial({ color: 0xffd34d })); bar.position.y = top + .16; bar.scale.x = .001; gr.add(bar);
  const bbg = new THREE.Mesh(new THREE.BoxGeometry(Math.max(1, b.w * .8) + .08, .06, .06), new THREE.MeshBasicMaterial({ color: 0x24272c })); bbg.position.y = top + .16; bbg.position.z = -.03; gr.add(bbg);
  W.scene.add(gr); W.sites.set(b.id, { gr, geo, bar, total: g.attributes.position.count, bw: Math.max(1, b.w * .8) });
};
W.siteProgress = function (b, p) { const s = W.sites.get(b.id); if (!s) return; const n = Math.floor(s.total * p / 3) * 3; if (n !== s.geo.drawRange.count) s.geo.setDrawRange(0, n); s.bar.scale.x = Math.max(.001, p) * s.bw; s.bar.position.x = -s.bw / 2 * (1 - p); };
W.removeSite = function (b) { const s = W.sites.get(b.id); if (!s) return; W.scene.remove(s.gr); s.geo.dispose(); s.gr.traverse(o => { if (o !== s.gr && o.geometry && o.geometry !== s.geo) o.geometry.dispose(); }); W.sites.delete(b.id); W.needShadow = true; };

/* land reclamation: the sea bed really rises and the island gets bigger */
W.findCoast = function (city) {
  let best = null, bs = -1e9; const reach = Math.sqrt(city.n + 1) * 2.2 + 26;
  for (let i = 0; i < 1100; i++) {
    const a = Math.random() * 6.2832, r = 5 + Math.random() * reach, x = Math.round(city.x + Math.cos(a) * r), z = Math.round(city.z + Math.sin(a) * r); if (x < 12 || z < 12 || x > N - 13 || z > N - 13 || W.T[ci(x, z)] !== 0) continue;
    let near = null, nd = 99; for (let p = -7; p <= 7; p++) for (let q = -7; q <= 7; q++) { const c = ci(x + p, z + q), t = W.T[c]; if (t >= 2 && t <= 4 && !W.occ[c]) { const dd = Math.hypot(p, q); if (dd < nd) { nd = dd; near = [x + p, z + q]; } } } if (!near || nd < 2.5) continue;
    const s = -Math.hypot(x - city.x, z - city.z) * .5 + W.h(x + .5, z + .5) * 1.2 - Math.abs(nd - 4.5) * .8 + Math.random() * 1.5; if (s > bs) { bs = s; best = { x: x - 1, z: z - 1, w: 3, d: 3, door: [near[0], near[1], 0], rw: 1 }; }
  }
  return best;
};
W.reclaim = function (cx, cz, R) {
  const pad = R * 1.25 + 4, x0 = Math.max(1, Math.floor(cx - pad)), x1 = Math.min(N - 1, Math.ceil(cx + pad)), z0 = Math.max(1, Math.floor(cz - pad)), z1 = Math.min(N - 1, Math.ceil(cz + pad)), pos = W.groundGeo.attributes.position, E = 2.6;
  for (let z = z0; z <= z1; z++) for (let x = x0; x <= x1; x++) {
    const i = x + z * (N + 1), bump = W.fbm(x * .16 + cx * .37, z * .16 + cz * .41), rr = R * (.72 + bump * .62), f = clamp((rr + E - Math.hypot(x - cx, z - cz)) / E); if (f <= 0) continue;
    const sm = f * f * (3 - 2 * f), y = W.H[i] + (.34 + bump * .1 - W.H[i]) * sm; if (y > W.H[i]) { W.H[i] = y; pos.setY(i, y); const q = i * 4, v = clamp(-y / 2.4) * 255; W.depthData[q] = v; W.depthData[q + 1] = v; W.depthData[q + 2] = v; }
  }
  pos.needsUpdate = true; W.groundGeo.computeVertexNormals(); W.depthTex.needsUpdate = true;
  for (let z = z0; z < z1; z++) for (let x = x0; x < x1; x++) { const c = ci(x, z), t = W.T[c]; if (t !== 0 && t !== 2) continue; const h = (W.H[x + z * (N + 1)] + W.H[x + 1 + z * (N + 1)] + W.H[x + (z + 1) * (N + 1)] + W.H[x + 1 + (z + 1) * (N + 1)]) / 4; W.T[c] = h < -.04 ? 0 : h < .1 ? 2 : 3; }
  const p = TEX / N; W.paintRect(Math.max(0, Math.floor(x0 * p) - 2), Math.max(0, Math.floor(z0 * p) - 2), Math.min(TEX, Math.ceil(x1 * p) + 2), Math.min(TEX, Math.ceil(z1 * p) + 2));
  if (W.paintPad && typeof G !== 'undefined') for (const b of G.blds) if (b.x + b.w >= x0 && b.x <= x1 && b.z + b.d >= z0 && b.z <= z1) W.paintPad(b);
  for (let z = Math.max(0, z0 - 1); z <= Math.min(N - 1, z1); z++) for (let x = Math.max(0, x0 - 1); x <= Math.min(N - 1, x1); x++) if (W.road[ci(x, z)]) W.paintRoad(x, z);
  W.needShadow = true; W.dirty = true;
};

/* roads grow from where people really walk */
W.walkOn = function (x, z, weight) {
  if (!inMap(x, z)) return; const c = ci(x, z); if (W.occ[c]) return; W.wear[c] += weight; if (W.wear[c] >= 4 && !W.road[c]) { W.road[c] = 1; W.paintRoad(x, z); }
};
/* real roads (tier 2+) only come from paid government road crews */
W.setRoad = function (c, t) { const o = W.road[c]; if (t <= o) return; if (o < 2 && t >= 2) W.roadCount++; W.road[c] = t; W.paintRoad(c % N, c / N | 0); };
const heapG = new Float32Array(N * N), heapF = new Float32Array(N * N), came = new Int32Array(N * N), stamp = new Uint32Array(N * N); let stampV = 1;
W.path = function (sx, sz, tx, tz, limit = 2600) {
  const S = ci(clamp(sx | 0, 0, N - 1), clamp(sz | 0, 0, N - 1)), T = ci(tx, tz); if (S === T) return []; if (W.T[T] === 0) return null; stampV++;
  const H = [], push = c => { let i = H.length; H.push(c); while (i > 0) { const p = (i - 1) >> 1; if (heapF[H[p]] <= heapF[c]) break; H[i] = H[p]; i = p; } H[i] = c; }, pop = () => { const top = H[0], l = H.pop(); if (H.length) { let i = 0; const n = H.length; for (;;) { let c = 2 * i + 1; if (c >= n) break; if (c + 1 < n && heapF[H[c + 1]] < heapF[H[c]]) c++; if (heapF[H[c]] >= heapF[l]) break; H[i] = H[c]; i = c; } H[i] = l; } return top; };
  const hx = (c) => { const x = c % N, z = c / N | 0, a = Math.abs(x - tx), b = Math.abs(z - tz); return (a + b - .59 * Math.min(a, b)) * .8; };
  heapG[S] = 0; heapF[S] = hx(S); stamp[S] = stampV; came[S] = -1; push(S); let n = 0;
  const COST = [1.35, 1.14, 1, .86, .78];
  while (H.length && n++ < limit) {
    const c = pop(); if (c === T) { const out = []; for (let q = T; q !== S; q = came[q]) out.push(q); return out.reverse(); }
    const x = c % N, z = c / N | 0;
    for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) {
      if (!a && !b) continue; const p = x + a, q = z + b; if (!inMap(p, q)) continue; const d = ci(p, q), ty = W.T[d]; if (ty === 0 || (W.occ[d] && d !== T)) continue;
      if (a && b) { const e = ci(x + a, z), f = ci(x, z + b); if (W.occ[e] || W.occ[f] || W.T[e] === 0 || W.T[f] === 0) continue; }
      const g = heapG[c] + (a && b ? 1.41 : 1) * COST[W.road[d]] * (ty === 1 && W.road[d] < 1 && !(W.plan && W.plan[d]) ? 4.5 : ty === 5 ? 1.5 : ty === 6 ? 3 : 1) * (W.plan ? (W.plan[d] ? .62 : 1.45) : 1);
      if (stamp[d] !== stampV || g < heapG[d]) { stamp[d] = stampV; heapG[d] = g; heapF[d] = g + hx(d); came[d] = c; push(d); }
    }
  }
  return null;
};

/* ---------- people ---------- */
W.initPeople = function () {
  const b = new MB(); b.cyl(0, .17, 0, .1, .23, 0xffffff, .075, 6); b.box(-.045, 0, 0, .05, .19, .06, 0x54505a); b.box(.045, 0, 0, .05, .19, .06, 0x54505a); const body = b.build(), h = new MB(); h.cyl(0, .4, 0, .075, .13, 0xffffff, .05, 7); const head = h.build(), l = new MB(); l.box(0, .46, 0, .17, .1, .17, 0xffffff); const load = l.build();
  const mat = new THREE.MeshLambertMaterial({ vertexColors: true });
  W.pBody = new THREE.InstancedMesh(body, mat, MAX_AGENTS); W.pHead = new THREE.InstancedMesh(head, mat, MAX_AGENTS); W.pLoad = new THREE.InstancedMesh(load, mat, MAX_AGENTS);
  for (const m of [W.pBody, W.pHead, W.pLoad]) { m.count = 0; m.frustumCulled = false; W.scene.add(m); } W.pBody.castShadow = true; W.pHead.setColorAt(0, new THREE.Color(1, 1, 1)); W.pBody.setColorAt(0, new THREE.Color(1, 1, 1)); W.pLoad.setColorAt(0, new THREE.Color(1, 1, 1));
  W._c = new THREE.Color();
};
W.drawAgents = function (t) {
  const o = W._o; let n = 0, ln = 0; const A = W.agents;
  for (let i = 0; i < A.length && n < MAX_AGENTS; i++) {
    const a = A[i]; if (a.indoor) continue; const mv = a.moving ? Math.abs(Math.sin(t * 9 + i)) * .05 : 0, sc = a.kid ? .68 : 1, y = W.h(a.x, a.z) + (W.T[ci(clamp(a.x | 0, 0, N - 1), clamp(a.z | 0, 0, N - 1))] === 1 ? .16 : .02) + mv;
    o.position.set(a.x, y, a.z); o.rotation.set(0, a.dir || 0, a.moving ? Math.sin(t * 9 + i) * .08 : 0); o.scale.setScalar(sc * 1.05); o.updateMatrix(); W.pBody.setMatrixAt(n, o.matrix); W.pHead.setMatrixAt(n, o.matrix);
    W._c.setHex(a.crew ? 0xf28c1e : a.shirt); W.pBody.setColorAt(n, W._c); W._c.setHex(a.skin); W.pHead.setColorAt(n, W._c);
    if (a.carry) { W.pLoad.setMatrixAt(ln, o.matrix); W._c.setHex(a.carry); W.pLoad.setColorAt(ln, W._c); ln++; } n++;
  }
  W.pBody.count = W.pHead.count = n; W.pLoad.count = ln;
  for (const m of [W.pBody, W.pHead, W.pLoad]) { m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true; }
};

/* ---------- camera + input ---------- */
W.bindInput = function (c) {
  const P = new Map(); let downAt = 0, moved = 0, last = null, pinchD = 0, pinchA = 0;
  const pan = (dx0, dy) => { const dx = W.fixPitch != null ? dx0 * .5 : dx0, k = W.cam.dist * .0021 * (800 / Math.max(innerHeight, 320)) * 1.35, s = Math.sin(W.cam.yaw), cs = Math.cos(W.cam.yaw); W.cam.tx = clamp(W.cam.tx - (dx * cs + dy * s) * k, 4, N - 4); W.cam.tz = clamp(W.cam.tz - (-dx * s + dy * cs) * k, 4, N - 4); };
  c.addEventListener('pointerdown', e => { c.setPointerCapture(e.pointerId); P.set(e.pointerId, [e.clientX, e.clientY]); if (P.size === 1) { downAt = performance.now(); moved = 0; last = [e.clientX, e.clientY]; } else if (P.size === 2) { const [a, b] = [...P.values()]; pinchD = Math.hypot(a[0] - b[0], a[1] - b[1]); pinchA = Math.atan2(b[1] - a[1], b[0] - a[0]); moved = 99; } });
  c.addEventListener('pointermove', e => { if (!P.has(e.pointerId)) return; P.set(e.pointerId, [e.clientX, e.clientY]); if (P.size === 1 && last) { const dx = e.clientX - last[0], dy = e.clientY - last[1]; moved += Math.abs(dx) + Math.abs(dy); if (moved > 7) pan(dx, dy); last = [e.clientX, e.clientY]; } else if (P.size === 2) { const [a, b] = [...P.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]), an = Math.atan2(b[1] - a[1], b[0] - a[0]); W.zoom(pinchD / Math.max(d, 1)); W.cam.yaw += (an - pinchA); pinchD = d; pinchA = an; } });
  const up = e => { const had = P.has(e.pointerId); P.delete(e.pointerId); if (had && P.size === 0 && moved <= 7 && performance.now() - downAt < 450 && W.onTap) W.onTap(e.clientX, e.clientY); if (P.size === 1) { last = [...P.values()][0]; } };
  c.addEventListener('pointerup', up); c.addEventListener('pointercancel', e => P.delete(e.pointerId));
  c.addEventListener('wheel', e => { e.preventDefault(); W.zoom(Math.exp(e.deltaY * .0012)); }, { passive: false });
  addEventListener('keydown', e => { if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return; const q = e.key.toLowerCase(), v = 34; if (q === 'a' || q === 'arrowleft') pan(v, 0); else if (q === 'd' || q === 'arrowright') pan(-v, 0); else if (q === 'w' || q === 'arrowup') pan(0, v); else if (q === 's' || q === 'arrowdown') pan(0, -v); else if (q === 'q') W.cam.yaw -= .2; else if (q === 'e') W.cam.yaw += .2; });
};
W.zoom = f => { W.cam.tDist = clamp(W.cam.tDist * f, 7, 190); };
W.fly = function (x, z, dist) { W.cam.tx = x; W.cam.tz = z; if (dist) W.cam.tDist = dist; };
W.project = function (x, y, z) { const v = new THREE.Vector3(x, y, z).project(W.camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight, v.z]; };
W.groundAt = function (sx, sy) {
  const v = new THREE.Vector3(sx / innerWidth * 2 - 1, 1 - sy / innerHeight * 2, .5).unproject(W.camera), o = W.camera.position, d = v.sub(o).normalize();
  let t = 0; for (let i = 0; i < 260; i++) { const x = o.x + d.x * t, y = o.y + d.y * t, z = o.z + d.z * t; if (x >= 0 && z >= 0 && x < N && z < N && y <= W.h(x, z) + .03) return [x, z]; t += Math.max(.12, (y - .5) * .12); if (t > 1200) break; } return null;
};
let shadowT = 0, sx0 = 0, sz0 = 0, sd0 = 0;
W.setDay = function (f, smog) {
  /* f: 0 dawn .. .5 dusk .. 1 next dawn */
  const dayL = clamp(Math.sin(f * Math.PI * 2 - .1) * 2.2 + .55), golden = clamp(1 - Math.abs(Math.sin(f * Math.PI * 2)) * 2.2);
  W.sun.intensity = .2 + dayL * .72; W.hemi.intensity = .44 + dayL * .26; W.sun.color.setRGB(1, .9 - golden * .2, .76 - golden * .34);
  const top = W.scene.background; top.setRGB(.1 + dayL * .45 + golden * .24, .16 + dayL * .61 + golden * .05, .32 + dayL * .57 - golden * .12);
  const smg = clamp((smog - .12) * 2.1); W.scene.fog.color.setRGB(top.r + smg * .35, top.g + smg * .25, top.b + smg * .05); W.scene.fog.density = (.0022 + smg * .0058) * (W.cam.dist > 90 ? .55 : 1);
  W.nightU.value = clamp(1 - dayL * 1.5); W.waterU.L.value = .58 + dayL * .42;
};
W.render = function (t, dt) {
  const C = W.cam, kk = 1 - Math.exp(-dt * 7); C.x += (C.tx - C.x) * kk; C.z += (C.tz - C.z) * kk; C.dist += (C.tDist - C.dist) * kk;
  const pitch = W.fixPitch != null ? W.fixPitch : .62 + clamp((C.dist - 7) / 90) * .5, ground = Math.max(0, W.h(C.x, C.z)), cam = W.camera;
  cam.position.set(C.x + Math.sin(C.yaw) * Math.cos(pitch) * C.dist, ground + Math.sin(pitch) * C.dist, C.z + Math.cos(C.yaw) * Math.cos(pitch) * C.dist); cam.lookAt(C.x, ground, C.z);
  W.waterU.t.value = t; const sz = clamp(C.dist * 1.1, 14, 92), sun = W.sun;
  if (W.needShadow || Math.hypot(C.x - sx0, C.z - sz0) > sz * .16 || Math.abs(C.dist - sd0) > sd0 * .12) {
    if (t - shadowT > .22) { shadowT = t; sx0 = C.x; sz0 = C.z; sd0 = C.dist; W.needShadow = false; const sc = sun.shadow.camera; sc.left = sc.bottom = -sz; sc.right = sc.top = sz; sc.near = 1; sc.far = 260; sc.updateProjectionMatrix(); sun.target.position.set(C.x, 0, C.z); sun.position.set(C.x - 46, 54, C.z + 32); sun.target.updateMatrixWorld(); W.renderer.shadowMap.needsUpdate = true; }
  }
  if (W.dirty && t - (W._upT || 0) > .7) { W._upT = t; W.dirty = false; W.gtex.needsUpdate = true; }
  if (W.ring.visible) W.ring.material.opacity = .62 + Math.sin(t * 5) * .35;
  if (W.post) W.post(); else W.renderer.render(W.scene, cam);
};
