/* quest/fx.js: effects. Bright things (slashes, rings, sparks, bolts, glows) are drawn additive into the effect buffer (same texels as
   the world, so they come out as pixel art, then glow); smoke, decals, warnings and solid pieces go into the world scene. */
'use strict';
const VS_UV = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }';
const FXH = `uniform sampler2D tDepth; uniform vec2 uRes; uniform float uT;
float occ(){ float d = texture2D(tDepth, gl_FragCoord.xy / uRes).r; return gl_FragCoord.z > d + .0009 ? .25 : 1.; }
`;
function fxMat(frag, uni = {}, vert = VS_UV) {
  return new THREE.ShaderMaterial({ uniforms: Object.assign({ tDepth: FXU.tDepth, uRes: FXU.uRes, uT: TIMEU }, uni), vertexShader: vert, fragmentShader: FXH + frag,
    transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
}
function fxClone(p) { const m = p.clone(); m.uniforms.tDepth = FXU.tDepth; m.uniforms.uRes = FXU.uRes; m.uniforms.uT = TIMEU; return m; }   /* clone() copies textures: point the shared ones back */
const C = h => new THREE.Color(h);
const FLAT = new THREE.PlaneGeometry(2, 2).rotateX(Math.PI / 2), BILL = new THREE.PlaneGeometry(2, 2);   /* FLAT lies on the ground, its +y is world +z (forward at heading 0) */
const SWG = (() => { const N = 40, aP = new Float32Array((N + 1) * 4), pos = new Float32Array((N + 1) * 6), idx = [];
  for (let i = 0; i <= N; i++) { aP[i * 4] = aP[i * 4 + 2] = i / N; aP[i * 4 + 1] = 0; aP[i * 4 + 3] = 1; if (i < N) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('aP', new THREE.BufferAttribute(aP, 2)); g.setIndex(idx); return g; })();
const M_SWOOSH = fxMat(`uniform float uProg, uA, uTail, uMode; uniform vec3 uC1, uC2; varying vec2 vP;
  void main(){ float s;
    if (uMode < .5) { s = (vP.x - (uProg - uTail)) / uTail; if (s < 0. || vP.x > uProg) discard; } else { s = pow(1. - abs(vP.x * 2. - 1.), .6); }
    float w = mix(.1, 1., s * s), e = (vP.y - (1. - w)) / w; if (e < 0.) discard;
    float v = floor(s * (.3 + .7 * e) * 4. + .6) / 4.; if (v <= 0.) discard;
    gl_FragColor = vec4(mix(uC2, uC1, step(.7, v)) * min(v, 1.) * uA * occ(), 1.); }`,
  { uProg: { value: 0 }, uA: { value: 1 }, uTail: { value: .6 }, uMode: { value: 0 }, uC1: { value: C(0xffffff) }, uC2: { value: C(0xffc040) }, uArc: { value: 3 }, uR0: { value: 1 }, uR1: { value: 2.4 }, uLift: { value: 0 } },
  `attribute vec2 aP; uniform float uArc, uR0, uR1, uLift; varying vec2 vP;
  void main(){ vP = aP; float a = (aP.x - .5) * uArc, r = mix(uR0, uR1, aP.y); gl_Position = projectionMatrix * modelViewMatrix * vec4(sin(a) * r, uLift * sin(aP.x * 3.1416), cos(a) * r, 1.); }`);
const M_RING = fxMat(`uniform float uR, uW, uA; uniform vec3 uC1, uC2; varying vec2 vUv;
  void main(){ float d = length(vUv * 2. - 1.), v = 1. - abs(d - uR) / uW; if (v <= 0. || d > 1.) discard; v = floor(v * 3. + .7) / 3.;
    gl_FragColor = vec4(mix(uC2, uC1, step(.9, v)) * min(v, 1.) * uA * occ(), 1.); }`, { uR: { value: .5 }, uW: { value: .12 }, uA: { value: 1 }, uC1: { value: C(0xffffff) }, uC2: { value: C(0xffc040) } });
const M_DISC = fxMat(`uniform float uA, uH; uniform vec3 uC1, uC2; varying vec2 vUv;
  void main(){ float d = length(vUv * 2. - 1.); if (d >= 1.) discard; float v = floor(pow(1. - d, uH) * 5. + .8) / 5.;
    gl_FragColor = vec4(mix(uC2, uC1, step(.55, v)) * min(v, 1.) * uA * occ(), 1.); }`, { uA: { value: 1 }, uH: { value: 1 }, uC1: { value: C(0xffffff) }, uC2: { value: C(0xffc040) } });
const M_BEAM = fxMat(`uniform float uA; uniform vec3 uC1, uC2; varying vec2 vUv;
  void main(){ float v = (1. - vUv.y) * (.5 + .5 * step(.5, fract(vUv.x * 5. + uT * 1.6 + vUv.y * 1.5))); v = floor(v * 4. + .5) / 4.; if (v <= 0.) discard;
    gl_FragColor = vec4(mix(uC2, uC1, step(.7, v)) * v * uA * occ(), 1.); }`, { uA: { value: 1 }, uC1: { value: C(0xffffff) }, uC2: { value: C(0xffc040) } });
const M_LINE = fxMat(`uniform float uA; uniform vec3 uC1; void main(){ gl_FragColor = vec4(uC1 * uA * occ(), 1.); }`, { uA: { value: 1 }, uC1: { value: C(0xffffff) } }, 'void main(){ gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }');
const M_TEXG = fxMat(`uniform float uA; uniform vec3 uC1; uniform sampler2D tx; varying vec2 vUv; void main(){ float a = texture2D(tx, vUv).a; if (a < .3) discard; gl_FragColor = vec4(uC1 * uA * occ(), 1.); }`, { uA: { value: 1 }, uC1: { value: C(0xffa040) }, tx: { value: null } });
const M_TEL = new THREE.ShaderMaterial({ uniforms: { uShape: { value: 0 }, uProg: { value: 0 }, uA: { value: 1 }, uArc: { value: 1 }, uC: { value: C(0xff2a22) }, uE: { value: new V2(.05, .05) }, uT: TIMEU }, vertexShader: VS_UV,
  transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -3, side: THREE.DoubleSide,
  fragmentShader: `uniform float uShape, uProg, uA, uArc, uT; uniform vec3 uC; uniform vec2 uE; varying vec2 vUv;
  void main(){ vec2 p = vUv * 2. - 1.; float ins = 1., edg = 0., fil = 0.;
    if (uShape < .5) { float d = length(p); ins = step(d, 1.); edg = step(1. - uE.x, d); fil = step(d, uProg); }
    else if (uShape < 1.5) { float d = length(p), a = abs(atan(p.x, p.y)); ins = step(d, 1.) * step(a, uArc * .5); edg = max(step(1. - uE.x, d), step(uArc * .5 - uE.x / max(d, .06), a)); fil = step(d, uProg); }
    else { edg = max(step(1. - uE.x, abs(p.x)), step(1. - uE.y, abs(p.y))); fil = step(p.y * .5 + .5, uProg); }
    if (ins < .5) discard;
    float al = (.15 + .3 * fil + edg * .55) * (.86 + .14 * step(.5, fract(uT * 7.)));
    gl_FragColor = vec4(mix(uC, vec3(1., .9, .75), edg * .45), al * uA); }` });

function mkTex(sz, draw) { const c = document.createElement('canvas'); c.width = c.height = sz; draw(c.getContext('2d'), sz); const t = new THREE.CanvasTexture(c); t.magFilter = t.minFilter = THREE.NearestFilter; t.generateMipmaps = false; return t; }
const TEX_CRACK = mkTex(96, (g, s) => { const R = mulberry(5); g.strokeStyle = '#fff'; g.lineCap = 'round';
  for (let b = 0; b < 9; b++) { let a = b / 9 * TAU + R() * .5, x = s / 2, y = s / 2, w = 3.2; g.beginPath(); g.moveTo(x, y);
    for (let i = 0; i < 9; i++) { a += (R() - .5) * 1.1; x += Math.cos(a) * s * .055; y += Math.sin(a) * s * .055; g.lineTo(x, y); if (R() < .3) { g.lineWidth = w; g.stroke(); const a2 = a + (R() < .5 ? 1 : -1) * .9; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a2) * s * .09, y + Math.sin(a2) * s * .09); g.lineWidth = 1.2; g.stroke(); g.beginPath(); g.moveTo(x, y); w *= .8; } }
    g.lineWidth = w; g.stroke(); } });
const TEX_SCORCH = mkTex(64, (g, s) => { const R = mulberry(9), im = g.createImageData(s, s); for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) { const d = Math.hypot(x - s / 2, y - s / 2) / (s / 2), n = vnoise(x / 6, y / 6) * .5 + R() * .12, a = d + n * .5 < .8 ? (d < .45 ? 200 : 140) : 0, k = (y * s + x) * 4; im.data[k] = im.data[k + 1] = im.data[k + 2] = 255; im.data[k + 3] = a; } g.putImageData(im, 0, 0); });
const TEX_BLOB = mkTex(32, (g, s) => { const im = g.createImageData(s, s); for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) { const d = Math.hypot(x - s / 2 + .5, y - s / 2 + .5) / (s / 2), k = (y * s + x) * 4; im.data[k + 3] = d < .72 ? 255 : d < .95 ? 130 : 0; } g.putImageData(im, 0, 0); });
const M_BLOB = new THREE.MeshBasicMaterial({ map: TEX_BLOB, color: 0x1a1030, transparent: true, opacity: .36, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
function blobShadow(r) { const m = new THREE.Mesh(FLAT, M_BLOB); m.scale.set(r, 1, r * .8); m.renderOrder = 1; return m; }

/* ---------- effect list */
const FXL = [];
function addFx(o, life, up, sc = fxScene, end = null) { o.frustumCulled = false; sc.add(o); const f = { o, t: 0, life, up, sc, end }; FXL.push(f); return f; }
function updFx(dt) { for (let i = FXL.length - 1; i >= 0; i--) { const f = FXL[i]; f.t += dt; const k = f.t / f.life;
  if (k >= 1) { f.sc.remove(f.o); f.o.traverse(o => { if (o.material && o.material.userData.own) o.material.dispose(); }); FXL.splice(i, 1); if (f.end) f.end(f); continue; }
  if (f.up) f.up(f, k, dt); } }
function own(m) { m.userData.own = true; return m; }
const ease = k => 1 - (1 - k) * (1 - k) * (1 - k);
function gy(x, z) { return Math.max(groundH(x, z), WY) + .06; }

function swoosh(x, y, z, ang, o = {}) {
  const { r0 = 1.0, r1 = 2.5, arc = 3.0, dur = .14, hold = .12, c1 = 0xffffff, c2 = 0xffc040, tilt = 0, flip = 1, lift = 0, mode = 0, a = 1, tail = .6 } = o;
  const m = own(fxClone(M_SWOOSH)), u = m.uniforms; u.uR0.value = r0; u.uR1.value = r1; u.uArc.value = arc; u.uC1.value.set(c1); u.uC2.value.set(c2); u.uLift.value = lift; u.uMode.value = mode; u.uTail.value = tail;
  const me = new THREE.Mesh(SWG, m); me.position.set(x, y, z); me.rotation.order = 'YXZ'; me.rotation.set(0, ang, tilt); me.scale.x = flip;
  return addFx(me, dur + hold, f => { u.uProg.value = Math.min(1, f.t / dur) * (1 + tail * .55); u.uA.value = a * (f.t < dur ? 1 : 1 - (f.t - dur) / hold); });
}
function ring(x, y, z, R, o = {}) {
  const { life = .4, c1 = 0xffffff, c2 = 0xffc040, w = .14, from = .15, a = 1, delay = 0 } = o;
  const m = own(fxClone(M_RING)), u = m.uniforms; u.uC1.value.set(c1); u.uC2.value.set(c2); u.uW.value = w; u.uA.value = 0;
  const me = new THREE.Mesh(FLAT, m); me.position.set(x, y, z); me.scale.set(R, 1, R);
  return addFx(me, life + delay, f => { const k = Math.max(0, (f.t - delay) / life); u.uR.value = lerp(from, 1 - w, ease(k)); u.uA.value = f.t < delay ? 0 : a * (1 - k * k); });
}
function disc(x, y, z, R, o = {}) {   /* flat glow on the ground, or bill = true: a round flash facing the camera */
  const { life = .25, c1 = 0xffffff, c2 = 0xffc040, h = 1, a = 1, grow = .4, bill = false } = o;
  const m = own(fxClone(M_DISC)), u = m.uniforms; u.uC1.value.set(c1); u.uC2.value.set(c2); u.uH.value = h;
  const me = new THREE.Mesh(bill ? BILL : FLAT, m); me.position.set(x, y, z); if (bill) me.quaternion.copy(cam.quaternion);
  return addFx(me, life, (f, k) => { const s = R * (1 - grow + grow * ease(k)); if (bill) me.scale.set(s, s, s); else me.scale.set(s, 1, s); u.uA.value = a * (1 - k); });
}
const BEAMG = new THREE.CylinderGeometry(1, 1, 1, 12, 1, true).translate(0, .5, 0);
function pillar(x, y, z, r, h, o = {}) { const { life = .6, c1 = 0xffffff, c2 = 0xffc040, a = 1 } = o, m = own(fxClone(M_BEAM)), u = m.uniforms; u.uC1.value.set(c1); u.uC2.value.set(c2);
  const me = new THREE.Mesh(BEAMG, m); me.position.set(x, y, z); return addFx(me, life, (f, k) => { const s = r * (k < .15 ? k / .15 : 1 - (k - .15) * .6); me.scale.set(s, h, s); u.uA.value = a * (1 - k * k); }); }
function decal(tex, x, z, R, o = {}) { const { life = 3.5, col = 0x2a1c18, op = .7, rot = Math.random() * TAU } = o;
  const m = own(new THREE.MeshBasicMaterial({ map: tex, color: col, transparent: true, opacity: op, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }));
  const me = new THREE.Mesh(FLAT, m); me.position.set(x, gy(x, z), z); me.scale.set(R, 1, R); me.rotation.y = rot; me.renderOrder = 2;
  return addFx(me, life, (f, k) => { m.opacity = op * (k < .7 ? 1 : 1 - (k - .7) / .3); }, scene); }
function glowTex(tex, x, z, R, o = {}) { const { life = .7, col = 0xffa040, rot = 0 } = o, m = own(fxClone(M_TEXG)); m.uniforms.tx = { value: tex }; m.uniforms.uC1.value.set(col);
  const me = new THREE.Mesh(FLAT, m); me.position.set(x, gy(x, z) + .02, z); me.scale.set(R, 1, R); me.rotation.y = rot; return addFx(me, life, (f, k) => { m.uniforms.uA.value = 1 - k; }); }
function bolt(x, z, o = {}) {   /* a lightning bolt from the sky: 1-texel jagged lines, doubled for a thick core */
  const { col = 0xbfe4ff, life = .26, h = 13, lean = 2.5 } = o, y0 = gy(x, z), pts = [], N = 11; let px = x + rnd(-lean, lean), pz = z + rnd(-1, 1) - 2;
  const path = []; for (let i = 0; i <= N; i++) { const k = i / N, j = i === N ? 0 : .55; path.push([lerp(px, x, k) + rnd(-j, j), lerp(y0 + h, y0, k), lerp(pz, z, k) + rnd(-j, j) * .4]); }
  for (let i = 0; i < N; i++) { pts.push(...path[i], ...path[i + 1]); if (Math.random() < .3 && i > 2) { const b = path[i]; pts.push(...b, b[0] + rnd(-1.4, 1.4), b[1] - rnd(.6, 1.6), b[2] + rnd(-.4, .4)); } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
  const grp = new THREE.Group(), m = own(fxClone(M_LINE)); m.uniforms.uC1.value.set(col);
  for (const dx of [-TW, 0, TW]) { const l = new THREE.LineSegments(g, m); l.position.x = dx; l.frustumCulled = false; grp.add(l); }
  const mw = own(fxClone(M_LINE)); mw.uniforms.uC1.value.set(0xffffff); const core = new THREE.LineSegments(g, mw); core.frustumCulled = false; grp.add(core);
  addFx(grp, life, (f, k) => { const fl = (Math.random() < .25 ? .35 : 1) * (1 - k * k); m.uniforms.uA.value = fl; mw.uniforms.uA.value = fl; }, fxScene, () => g.dispose());
}

/* ---------- particles: square points sized in texels */
class Pool {
  constructor(n, add) { this.n = n; this.add = add; this.cnt = 0; this.S = 19; this.d = new Float32Array(n * this.S);
    const g = this.g = new THREE.BufferGeometry(); this.pos = new Float32Array(n * 3); this.col = new Float32Array(n * 4); this.siz = new Float32Array(n);
    g.setAttribute('position', new THREE.BufferAttribute(this.pos, 3)); g.setAttribute('aCol', new THREE.BufferAttribute(this.col, 4)); g.setAttribute('aSize', new THREE.BufferAttribute(this.siz, 1));
    const vs = 'attribute vec4 aCol; attribute float aSize; varying vec4 vCol; void main(){ vCol = aCol; gl_PointSize = aSize; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }';
    const m = add ? fxMat('varying vec4 vCol; void main(){ gl_FragColor = vec4(vCol.rgb * vCol.a * occ(), 1.); }', {}, vs)
      : new THREE.ShaderMaterial({ vertexShader: vs, fragmentShader: 'varying vec4 vCol; void main(){ gl_FragColor = vCol; }', transparent: true, depthWrite: false });
    this.o = new THREE.Points(g, m); this.o.frustumCulled = false; (add ? fxScene : scene).add(this.o); g.setDrawRange(0, 0); }
  spawn(x, y, z, vx, vy, vz, life, s0, s1, c0, c1, a = 1, grav = 0, drag = 0) { if (this.cnt >= this.n) return; const d = this.d, k = this.cnt++ * this.S;
    d[k] = x; d[k + 1] = y; d[k + 2] = z; d[k + 3] = vx; d[k + 4] = vy; d[k + 5] = vz; d[k + 6] = 0; d[k + 7] = life; d[k + 8] = s0; d[k + 9] = s1;
    d[k + 10] = c0[0]; d[k + 11] = c0[1]; d[k + 12] = c0[2]; d[k + 13] = c1[0]; d[k + 14] = c1[1]; d[k + 15] = c1[2]; d[k + 16] = a; d[k + 17] = grav; d[k + 18] = drag; }
  update(dt) { const d = this.d, S = this.S; let i = 0;
    while (i < this.cnt) { const k = i * S; d[k + 6] += dt; if (d[k + 6] >= d[k + 7]) { const l = --this.cnt * S; if (l !== k) d.copyWithin(k, l, l + S); continue; }
      const q = d[k + 6] / d[k + 7], dr = Math.max(0, 1 - d[k + 18] * dt); d[k + 3] *= dr; d[k + 4] = d[k + 4] * dr - d[k + 17] * dt; d[k + 5] *= dr;
      d[k] += d[k + 3] * dt; d[k + 1] += d[k + 4] * dt; d[k + 2] += d[k + 5] * dt;
      this.pos[i * 3] = d[k]; this.pos[i * 3 + 1] = d[k + 1]; this.pos[i * 3 + 2] = d[k + 2];
      this.col[i * 4] = d[k + 10] + (d[k + 13] - d[k + 10]) * q; this.col[i * 4 + 1] = d[k + 11] + (d[k + 14] - d[k + 11]) * q; this.col[i * 4 + 2] = d[k + 12] + (d[k + 15] - d[k + 12]) * q; this.col[i * 4 + 3] = d[k + 16] * (1 - q * q * q);
      this.siz[i] = Math.max(1, Math.round(d[k + 8] + (d[k + 9] - d[k + 8]) * q)); i++; }
    const a = this.g.attributes; a.position.needsUpdate = a.aCol.needsUpdate = a.aSize.needsUpdate = true; this.g.setDrawRange(0, this.cnt); }
}
let PA, PN;
const rgb = h => [((h >> 16) & 255) / 255, ((h >> 8) & 255) / 255, (h & 255) / 255];
const K = { white: [1, 1, 1], gold: rgb(0xffc23d), orange: rgb(0xff7a1a), red: rgb(0xff3a1a), ember: rgb(0xb02a10), cyan: rgb(0x5af0e0), teal: rgb(0x26b8a8), blue: rgb(0x58a8ff), ice: rgb(0xbfeaff), violet: rgb(0xa070ff), pink: rgb(0xff6ac0),
  dust: rgb(0xd8c49a), smoke: rgb(0x55505e), dark: rgb(0x2a2630), green: rgb(0x8ef060), leaf: rgb(0x6fbf45), spore: rgb(0xe8c0ff) };
function sparks(x, y, z, n, c0 = K.white, c1 = K.gold, spd = 7, life = .28, size = 2) { for (let i = 0; i < n; i++) { const a = rnd(0, TAU), e = rnd(-.2, 1), s = spd * rnd(.4, 1); PA.spawn(x, y, z, Math.cos(a) * s, e * s * .6 + 1.5, Math.sin(a) * s * .6, life * rnd(.6, 1.2), size, 1, c0, c1, 1, 9, 3); } }
function embers(x, y, z, n, r, c0 = K.gold, c1 = K.red, up = 3) { for (let i = 0; i < n; i++) { const a = rnd(0, TAU), d = Math.sqrt(Math.random()) * r; PA.spawn(x + Math.cos(a) * d, y + rnd(0, .3), z + Math.sin(a) * d, rnd(-.5, .5), rnd(.5, 1) * up, rnd(-.3, .3), rnd(.4, .9), 2, 1, c0, c1, 1, -1, 1); } }
function smoke(x, y, z, n, r, c0 = K.smoke, c1 = K.dark, up = 1.4, size = 4) { for (let i = 0; i < n; i++) { const a = rnd(0, TAU), d = Math.sqrt(Math.random()) * r; PN.spawn(x + Math.cos(a) * d, y + rnd(0, .4), z + Math.sin(a) * d, Math.cos(a) * .6, rnd(.5, 1) * up, Math.sin(a) * .4, rnd(.5, 1.1), size, size + 2, c0, c1, .7, -.3, 1.2); } }
function dustRing(x, y, z, r, n = 14, c = K.dust) { for (let i = 0; i < n; i++) { const a = i / n * TAU + rnd(0, .3), s = rnd(2.5, 4.5); PN.spawn(x + Math.cos(a) * r * .5, y + .1, z + Math.sin(a) * r * .5, Math.cos(a) * s, rnd(.4, 1.2), Math.sin(a) * s * .7, rnd(.35, .6), 3, 5, c, c, .75, 1.5, 3.5); } }
function shake(a) { SHAKE.a = Math.max(SHAKE.a, a); }
function updShake(dt) { SHAKE.a = Math.max(0, SHAKE.a - dt * 1.6 - SHAKE.a * dt * 5); const q = Math.round(SHAKE.a / TW); SHAKE.x = Math.round(rnd(-q, q)) * TW; SHAKE.y = Math.round(rnd(-q, q)) * TW; }

/* ---------- composites */
function hitSpark(x, y, z, c1 = K.white, c2 = K.gold, big = false) {
  sparks(x, y, z, big ? 12 : 6, c1, c2, big ? 9 : 6.5, big ? .34 : .24, big ? 3 : 2);
  disc(x, y, z, big ? 1.0 : .6, { bill: true, life: .12, c2: c2 === K.gold ? 0xffc23d : 0xffffff, h: .7, grow: .5 });
}
function shock(x, z, R, c1 = 0xffffff, c2 = 0xffc040, dust = true) { const y = gy(x, z); ring(x, y, z, R, { c1, c2, life: .38, w: .16 }); ring(x, y + .02, z, R * .72, { c1, c2, life: .3, w: .22, delay: .05, a: .7 }); if (dust) dustRing(x, y, z, R * .8, 16); }
function cracks(x, z, R, glow = 0xff9a30) { const r = Math.random() * TAU; decal(TEX_CRACK, x, z, R, { rot: r, life: 4, col: 0x241a1e, op: .75 }); glowTex(TEX_CRACK, x, z, R, { rot: r, col: glow, life: .8 }); }
function explosion(x, z, R, o = {}) {
  const { c1 = 0xffffff, c2 = 0xff8a20, ka = K.gold, kb = K.red, scorch = true, pow = 1 } = o, y = gy(x, z);
  disc(x, y + .1, z, R * 1.05, { c1, c2, life: .3, h: .6, grow: .6 }); disc(x, y + R * .35, z, R * .8, { c1, c2, life: .22, h: .5, grow: .7, bill: true });
  ring(x, y, z, R * 1.15, { c1, c2, life: .42, w: .18 }); ring(x, y, z, R * 1.5, { c1: c2, c2, life: .55, w: .08, delay: .06, a: .6 });
  sparks(x, y + .4, z, 18 * pow, ka, kb, 11, .45, 3); embers(x, y, z, 14 * pow, R * .7, ka, kb, 4.5); smoke(x, y + .3, z, 10 * pow, R * .6);
  if (scorch) decal(TEX_SCORCH, x, z, R * .95, { life: 5, col: 0x1c1418, op: .55 });
  flashLight(x, y + 1.2, z, c2, 2.6 * pow, .4, R * 3.2); shake(.1 + .1 * pow);
}
const ICEG = new THREE.ConeGeometry(.5, 1, 4).translate(0, .5, 0);
let ICEM;
function iceSpikes(x, z, R, n = 14, life = 2.2) {
  if (!ICEM) ICEM = toon({ color: 0xcdf3ff, emissive: 0x4aa8ff, emissiveIntensity: .55, flatShading: true });
  const grp = new THREE.Group(), sp = [];
  for (let i = 0; i < n; i++) { const ringI = i % 2, a = i / n * TAU + rnd(-.2, .2), d = R * (ringI ? .55 : .92) * rnd(.85, 1), m = new THREE.Mesh(ICEG, ICEM), px = x + Math.cos(a) * d, pz = z + Math.sin(a) * d;
    m.position.set(px, groundH(px, pz) - .1, pz); m.rotation.set(Math.sin(a) * -.5, rnd(0, TAU), Math.cos(a) * .5); m.castShadow = true; const h = rnd(1.1, 2.1) * (ringI ? .8 : 1), w = rnd(.5, .85); sp.push([m, h, w, i / n * .12]); m.scale.set(.01, .01, .01); grp.add(m); }
  addFx(grp, life, f => { for (const [m, h, w, dl] of sp) { const t = f.t - dl, up = clamp(t / .1, 0, 1), dn = clamp((life - f.t) / .3, 0, 1), s = Math.max(.01, ease(up) * dn); m.scale.set(w * s, h * s, w * s); } }, scene);
  const y = gy(x, z); ring(x, y, z, R * 1.1, { c1: 0xffffff, c2: 0x6ad0ff, life: .45, w: .2 }); disc(x, y, z, R, { c1: 0xffffff, c2: 0x4aa8ff, life: .5, h: .5, a: .8 });
  for (let i = 0; i < 40; i++) { const a = rnd(0, TAU), s = rnd(2, 8); PA.spawn(x, y + .3, z, Math.cos(a) * s, rnd(1, 4), Math.sin(a) * s * .7, rnd(.4, .9), 2, 1, K.white, K.ice, 1, 4, 2.5); }
  flashLight(x, y + 1, z, 0x7ad0ff, 2.2, .5, R * 3);
}
function levelUpFx(x, y, z) {
  pillar(x, y, z, 1.1, 9, { c1: 0xffffff, c2: 0xffd24a, life: 1.1 }); ring(x, y + .05, z, 3.2, { c2: 0xffd24a, life: .7, w: .12 }); ring(x, y + .05, z, 2.2, { c2: 0xffd24a, life: .6, w: .2, delay: .12 });
  for (let i = 0; i < 46; i++) { const a = rnd(0, TAU), d = rnd(.2, 1.3); PA.spawn(x + Math.cos(a) * d, y + rnd(0, .5), z + Math.sin(a) * d, 0, rnd(2.5, 7), 0, rnd(.6, 1.3), 2, 1, K.white, K.gold, 1, 0, .6); }
  flashLight(x, y + 1.5, z, 0xffd24a, 2.4, .8, 10);
}
function deathPoof(x, y, z, r, col = K.spore) { smoke(x, y + r * .5, z, 9, r * .6, [.9, .88, .95], [.5, .46, .6], 1.8, 4); sparks(x, y + r * .6, z, 8, K.white, col, 5, .5, 2);
  for (let i = 0; i < 6; i++) PA.spawn(x + rnd(-.3, .3), y + rnd(.2, 1), z + rnd(-.3, .3), 0, rnd(1.5, 3), 0, rnd(.6, 1), 2, 1, K.white, col, 1, 0, .5); }

/* enemy warning on the ground: fills up, then fires */
function tele(kind, x, z, ang, sz, warn, fire, o = {}) {
  const m = own(M_TEL.clone()), u = m.uniforms; u.uT = TIMEU; u.uShape.value = kind === 'circle' ? 0 : kind === 'cone' ? 1 : 2; if (o.col) u.uC.value.set(o.col);
  const me = new THREE.Mesh(FLAT, m); me.renderOrder = 3; let cx = x, cz = z;
  if (kind === 'rect') { cx = x + Math.sin(ang) * sz[0] / 2; cz = z + Math.cos(ang) * sz[0] / 2; me.scale.set(sz[1] / 2, 1, sz[0] / 2); u.uE.value.set(TW * 3 / sz[1], TW * 3 / sz[0]); }
  else { me.scale.set(sz, 1, sz); u.uE.value.set(TW * 1.6 / sz, 0); u.uArc.value = o.arc || 1; }
  me.position.set(cx, gy(cx, cz) + .03, cz); me.rotation.y = ang;
  return addFx(me, warn, (f, k) => { u.uProg.value = k; u.uA.value = Math.min(1, f.t / .12) * (o.soft || 1); }, scene, fire);
}
function inShape(kind, x, z, ang, sz, px, pz, pr = 0, arc = 1) {
  const dx = px - x, dz = pz - z;
  if (kind === 'circle') return Math.hypot(dx, dz) < sz + pr;
  if (kind === 'cone') { const d = Math.hypot(dx, dz); return d < sz + pr && (d < pr + .3 || Math.abs(angDiff(ang, Math.atan2(dx, dz))) < arc / 2 + Math.atan2(pr, d)); }
  const f = dx * Math.sin(ang) + dz * Math.cos(ang), s = dx * Math.cos(ang) - dz * Math.sin(ang); return f > -pr && f < sz[0] + pr && Math.abs(s) < sz[1] / 2 + pr;
}

/* ---------- always-on things: mushroom glows, campfire, drifting motes */
let fireLight;
function buildAmbientFx() {
  PA = new Pool(2600, true); PN = new Pool(900, false);
  for (const g of GLOWS) { const m = fxClone(M_DISC), u = m.uniforms; u.uC1.value.set(g.c); u.uC2.value.set(g.c); u.uH.value = 1.4; u.uA.value = .34; const me = new THREE.Mesh(FLAT, m); me.position.set(g.x, g.y, g.z); me.scale.set(g.r, 1, g.r); me.userData.ph = Math.random() * 6; me.matrixAutoUpdate = true; fxScene.add(me); g.m = m; g.o = me; }
  fireLight = new THREE.PointLight(0xffa040, 1.5, 13, 1.5); fireLight.position.set(VILLAGE.x, groundH(VILLAGE.x, VILLAGE.z + .5) + 1.2, VILLAGE.z + .5); scene.add(fireLight);
}
let ambT = 0;
function updAmbient(dt, hx, hz) {
  for (const g of GLOWS) { const near = Math.abs(g.x - CAMT.x) < 22 && Math.abs(g.z - CAMT.z) < 20; g.o.visible = near; if (near) g.m.uniforms.uA.value = .3 + .1 * Math.sin(TIMEU.value * 1.6 + g.o.userData.ph); }
  const fx = VILLAGE.x, fz = VILLAGE.z + .5;
  if (Math.abs(fx - CAMT.x) < 20 && Math.abs(fz - CAMT.z) < 18) { const fy = groundH(fx, fz) + .35; fireLight.intensity = 1.3 + Math.sin(TIMEU.value * 11) * .2 + Math.random() * .15;
    if (Math.random() < dt * 34) PA.spawn(fx + rnd(-.22, .22), fy, fz + rnd(-.15, .15), rnd(-.2, .2), rnd(1.4, 2.6), 0, rnd(.3, .6), 3, 1, K.gold, K.red, 1, -.5, .5);
    if (Math.random() < dt * 5) PN.spawn(fx + rnd(-.1, .1), fy + .8, fz, rnd(-.2, .2), rnd(.8, 1.3), 0, rnd(.8, 1.4), 2, 4, K.smoke, K.dark, .45, -.2, .4); }
  ambT += dt; if (ambT < .05) return; ambT = 0;
  const x = hx + rnd(-13, 13), z = hz + rnd(-9, 8), m = mapAt(x, z), y = groundH(x, z);
  if (y < WY) { if (Math.random() < .3) PA.spawn(x, WY + .05, z, 0, 0, 0, .35, 1, 1, K.white, K.cyan, .9); return; }
  if (m[1] > .5) { PA.spawn(x, y + rnd(.3, 2.2), z, rnd(-.3, .3), rnd(-.1, .25), rnd(-.2, .2), rnd(1.6, 3.2), 2, 1, pick([K.green, K.cyan, K.pink]), K.teal, .9, 0, .2); if (Math.random() < .4) PA.spawn(x + 1, y + .2, z - 1, 0, rnd(.3, .7), 0, rnd(1.5, 2.5), 1, 1, K.spore, K.violet, .8); }
  else if (m[0] > .5) { if (Math.random() < .5) PN.spawn(x, y + rnd(4, 7), z, rnd(.5, 1.3), rnd(-1.4, -.8), rnd(-.2, .4), rnd(3, 4.5), 2, 2, pick([rgb(0xf08a3c), rgb(0xe2573a), rgb(0xf5b53c)]), rgb(0xc86a2a), 1, 0, 0); }
  else if (Math.random() < .35) PN.spawn(x, y + rnd(.4, 2.5), z, rnd(.4, 1), rnd(-.1, .3), rnd(-.2, .2), rnd(2, 3.5), 1, 1, pick([[1, 1, .9], [1, .8, .9]]), [1, 1, 1], .9, 0, 0);
}
function warmFx() {   /* compile every effect shader once so the first hit does not hitch */
  const s = new THREE.Scene(); for (const m of [M_SWOOSH, M_RING, M_DISC, M_BEAM, M_TEXG, M_TEL]) s.add(new THREE.Mesh(m === M_SWOOSH ? SWG : FLAT, m)); s.add(new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, 1, 1, 1], 3)), M_LINE));
  M_TEXG.uniforms.tx.value = TEX_CRACK; renderer.compile(s, cam);
}
