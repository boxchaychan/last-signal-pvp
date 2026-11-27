/* quest/world.js: the map "หุบเขาสามฤดู": land data, ground / water / grass shaders, plants and village from CC0 packs, collision. */
'use strict';
const MS = 128, MH = 64, GN = 256, GC = MS / GN, WY = -.55;
const VILLAGE = { x: 0, z: 36, r: 11 }, LAIR = { x: -34, z: -47, r: 12 }, KINGSPOT = { x: -43, z: 20, r: 8 };
const PATHS = [
  [[0, 46], [0, 36], [-2, 28], [-8, 23], [-6, 17], [2, 9], [14, 5], [26, 8], [36, 1], [40, -10], [34, -20], [22, -28], [8, -34], [-6, -40], [-20, -45], [-34, -47]],
  [[-6, 17], [-18, 14], [-30, 18], [-43, 20]],
];
const PONDS = [[-24, 36, 6.5], [22, -10, 5], [8, -52, 7], [-48, -12, 5.5], [44, 32, 5], [-30, -22, 4.5]];
const ZONES = [
  { id: 'camp', name: 'ค่ายผู้กล้า', sub: 'ที่ปลอดภัย', col: '#ffe9a8' },
  { id: 'meadow', name: 'ทุ่งดอกไม้สายลม', sub: 'เลเวล 1-4', col: '#b8f27a' },
  { id: 'autumn', name: 'ป่าใบไม้แดง', sub: 'เลเวล 5-8', col: '#ffb060' },
  { id: 'glow', name: 'ป่าเห็ดแสงจันทร์', sub: 'เลเวล 9-12', col: '#8ee8ff' },
  { id: 'lair', name: 'รังมังกรราตรี', sub: 'บอส', col: '#ff7a8a' },
];
function segDist(px, pz, a, b) { const dx = b[0] - a[0], dz = b[1] - a[1], l = dx * dx + dz * dz, t = l ? clamp(((px - a[0]) * dx + (pz - a[1]) * dz) / l, 0, 1) : 0; return Math.hypot(px - a[0] - dx * t, pz - a[1] - dz * t); }
function pathDist(x, z) { let d = 1e9; for (const p of PATHS) for (let i = 0; i < p.length - 1; i++) d = Math.min(d, segDist(x, z, p[i], p[i + 1])); return d; }
function zoneW(x, z) { const n = (fbm(x / 14 + 40, z / 14 + 3, 2) - .5) * 10, gl = 1 - sstep(-30, -22, z + n), au = sstep(6, 13, x + n) * (1 - sstep(14, 22, z - n * .5)) * (1 - gl); return [au, gl]; }
function pondF(x, z) { let f = 0; for (const [px, pz, r] of PONDS) { const d = Math.hypot(x - px, z - pz) / r * (1 + (vnoise(x / 3 + 9, z / 3 + 4) - .5) * .45); f = Math.max(f, 1 - sstep(.55, 1.2, d)); } return f; }

/* heights on the vertex grid, then the data textures */
const HGT = new Float32Array((GN + 1) * (GN + 1)), PDV = new Float32Array((GN + 1) * (GN + 1));
(function buildHeights() {
  for (let j = 0; j <= GN; j++) for (let i = 0; i <= GN; i++) { const x = -MH + i * GC, z = -MH + j * GC;
    let h = (fbm(x / 24 + 3.1, z / 24 + 7.7, 3) - .5) * 2.8 + (vnoise(x / 7 + 11, z / 7 + 5) - .5) * .5;
    const pd = pathDist(x, z); PDV[j * (GN + 1) + i] = pd; h = lerp(h * .3, h, sstep(1.5, 7, pd));
    for (const s of [VILLAGE, LAIR, KINGSPOT]) h = lerp(.12, h, sstep(s.r * .7, s.r * 1.25, Math.hypot(x - s.x, z - s.z)));
    h = Math.max(h, WY + .4); h = lerp(h, WY - 1.15, pondF(x, z));
    const e = Math.max(Math.abs(x), Math.abs(z)); h += sstep(50, 62, e) * (3.2 + 3.4 * fbm(x / 8 + 2, z / 8 + 9, 2));
    HGT[j * (GN + 1) + i] = h; }
})();
function groundH(x, z) { const fx = clamp((x + MH) / GC, 0, GN - .001), fz = clamp((z + MH) / GC, 0, GN - .001), i = fx | 0, j = fz | 0, u = fx - i, v = fz - j, w = GN + 1;
  return (HGT[j * w + i] * (1 - u) + HGT[j * w + i + 1] * u) * (1 - v) + (HGT[(j + 1) * w + i] * (1 - u) + HGT[(j + 1) * w + i + 1] * u) * v; }
const MAPD = new Uint8Array(GN * GN * 4);
const tMap = new THREE.DataTexture(MAPD, GN, GN, THREE.RGBAFormat); tMap.minFilter = tMap.magFilter = THREE.LinearFilter;
let tH;
(function buildMaps() {
  const hd = new Float32Array(GN * GN * 4);
  for (let j = 0; j < GN; j++) for (let i = 0; i < GN; i++) { const x = -MH + (i + .5) * GC, z = -MH + (j + .5) * GC, k = (j * GN + i) * 4, h = groundH(x, z);
    const [au, gl] = zoneW(x, z), pd = pathDist(x, z);
    let path = 1 - sstep(1.1, 2.3, pd); path = Math.max(path, 1 - sstep(5.5, 8, Math.hypot(x - VILLAGE.x, z - VILLAGE.z)), (1 - sstep(8, 11, Math.hypot(x - LAIR.x, z - LAIR.z))) * .9);
    const slope = Math.hypot(groundH(x + .5, z) - groundH(x - .5, z), groundH(x, z + .5) - groundH(x, z - .5));
    let gr = (.95 - au * .1 - gl * .2) * sstep(.1, .3, fbm(x / 9 + 5, z / 9 + 1, 2)) * (1 - sstep(.3, .6, path)) * sstep(WY + .12, WY + .3, h) * (1 - sstep(.5, .9, slope));
    MAPD[k] = au * 255; MAPD[k + 1] = gl * 255; MAPD[k + 2] = path * 255; MAPD[k + 3] = clamp(gr, 0, 1) * 255; hd[k] = h; }
  tMap.needsUpdate = true;
  if (THREE.DataUtils && THREE.DataUtils.toHalfFloat) { const hf = new Uint16Array(hd.length); for (let i = 0; i < hd.length; i++) hf[i] = THREE.DataUtils.toHalfFloat(hd[i]);
    tH = new THREE.DataTexture(hf, GN, GN, THREE.RGBAFormat, THREE.HalfFloatType); tH.minFilter = tH.magFilter = THREE.LinearFilter; }
  else { tH = new THREE.DataTexture(hd, GN, GN, THREE.RGBAFormat, THREE.FloatType); tH.minFilter = tH.magFilter = THREE.NearestFilter; }
  tH.needsUpdate = true;
})();
function mapAt(x, z) { const i = clamp(((x + MH) / GC) | 0, 0, GN - 1), j = clamp(((z + MH) / GC) | 0, 0, GN - 1), k = (j * GN + i) * 4; return [MAPD[k] / 255, MAPD[k + 1] / 255, MAPD[k + 2] / 255, MAPD[k + 3] / 255]; }
function zoneAt(x, z) { if (Math.hypot(x - VILLAGE.x, z - VILLAGE.z) < VILLAGE.r + 1) return 0; if (Math.hypot(x - LAIR.x, z - LAIR.z) < LAIR.r + 2) return 4; const m = mapAt(x, z); return m[1] > .5 ? 3 : m[0] > .5 ? 2 : 1; }
function walkable(x, z) { return Math.max(Math.abs(x), Math.abs(z)) < 55 && groundH(x, z) > WY - .12; }

/* ---------- shaders shared by ground / grass / water */
const GLSL_N = `
float h21(vec2 p){ vec3 p3 = fract(vec3(p.xyx) * .1031); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.x + p3.y) * p3.z); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(h21(i), h21(i + vec2(1., 0.)), f.x), mix(h21(i + vec2(0., 1.)), h21(i + vec2(1., 1.)), f.x), f.y); }`;
const GLSL_MAP = `
uniform sampler2D tMap; uniform sampler2D tH; uniform float uT;
vec4 mapAt(vec2 xz){ return texture2D(tMap, (xz + 64.) / 128.); }
float hAt(vec2 xz){ return texture2D(tH, (xz + 64.) / 128.).r; }
vec3 zoneCol(vec2 xz, vec4 m){
  float tone = step(.5, vn(xz * .17) * .7 + vn(xz * .8 + 13.) * .3), zn = vn(xz * .55 + 3.) * .7 + .15;
  vec3 c = mix(vec3(.37, .62, .23), vec3(.52, .73, .27), tone);
  c = mix(c, mix(vec3(.74, .60, .27), vec3(.80, .50, .24), tone), step(zn, m.r));
  c = mix(c, mix(vec3(.22, .30, .46), vec3(.31, .25, .48), tone), step(zn, m.g));
  return c; }`;
const MAPU = { tMap: { value: tMap }, tH: { value: tH }, uT: TIMEU };
function mapShader(mat, key, vsHead, vsBody, fsHead, fsColor, extra) {
  mat.onBeforeCompile = sh => { Object.assign(sh.uniforms, MAPU, extra || {});
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP; varying vec3 vWN;\n' + GLSL_N + GLSL_MAP + (vsHead || ''));
    if (vsBody) sh.vertexShader = sh.vertexShader.replace('#include <begin_vertex>', vsBody).replace('#include <beginnormal_vertex>', 'vec3 objectNormal = vec3(0., 1., 0.);');
    sh.vertexShader = sh.vertexShader.replace('#include <fog_vertex>', '#include <fog_vertex>\nvWP = (modelMatrix * vec4(transformed, 1.)).xyz; vWN = normalize(mat3(modelMatrix) * objectNormal);');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP; varying vec3 vWN;\n' + GLSL_N + GLSL_MAP + (fsHead || ''))
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', fsColor); };
  mat.customProgramCacheKey = () => key; return mat;
}

/* ---------- ground */
let groundMesh, waterMesh, grassMesh;
function buildGround() {
  const w = GN + 1, pos = new Float32Array(w * w * 3), idx = new Uint32Array(GN * GN * 6);
  for (let j = 0; j < w; j++) for (let i = 0; i < w; i++) { const k = (j * w + i) * 3; pos[k] = -MH + i * GC; pos[k + 1] = HGT[j * w + i]; pos[k + 2] = -MH + j * GC; }
  let q = 0; for (let j = 0; j < GN; j++) for (let i = 0; i < GN; i++) { const a = j * w + i, b = a + 1, c = a + w, d = c + 1; idx[q++] = a; idx[q++] = c; idx[q++] = b; idx[q++] = b; idx[q++] = c; idx[q++] = d; }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setIndex(new THREE.BufferAttribute(idx, 1)); g.computeVertexNormals();
  const m = mapShader(toon(), 'q-ground', '', null, '', `
    vec4 m = mapAt(vWP.xz); float n2 = vn(vWP.xz * .9 + 13.), n3 = vn(vWP.xz * 3.1 + 5.);
    vec3 c = zoneCol(vWP.xz, m); c *= 1. - .09 * step(.76, n3);
    { float lf = h21(floor(vWP.xz * 4.)); c = mix(c, mix(vec3(.86, .34, .16), vec3(.95, .74, .22), step(.985, lf)), step(.972, lf) * step(.5, m.r) * (1. - step(.5, m.g))); c += vec3(.10, .28, .30) * step(.988, lf) * step(.5, m.g); }
    c *= 1. - .14 * step(.5, m.a) * (1. - step(.5, m.b));                                   /* earth under the grass is a bit darker */
    vec3 dirt = mix(vec3(.74, .57, .38), vec3(.65, .49, .33), step(.52, n3));
    dirt = mix(dirt, mix(vec3(.76, .52, .33), vec3(.66, .43, .28), step(.52, n3)), step(.5, m.r));
    dirt = mix(dirt, mix(vec3(.36, .33, .47), vec3(.29, .27, .40), step(.52, n3)), step(.5, m.g));
    dirt *= 1. - .12 * step(.84, vn(vWP.xz * 5.3));
    c = mix(c, dirt, step(.5, m.b + (n2 - .5) * .45));
    vec3 sand = mix(vec3(.88, .80, .58), vec3(.60, .54, .44), step(vWP.y, ${(WY + .1).toFixed(2)}));
    sand = mix(sand, sand * vec3(.45, .5, .8), step(.5, m.g));
    c = mix(c, sand, step(vWP.y, ${(WY + .3).toFixed(2)} + (n2 - .5) * .12));
    float steep = step(.36, 1. - vWN.y + (n2 - .5) * .1);
    vec3 rock = mix(vec3(.60, .52, .47), vec3(.48, .42, .42), step(.5, fract(vWP.y * 1.3 + n2 * .7)));
    rock = mix(rock, rock * vec3(.55, .55, .85), step(.5, m.g));
    c = mix(c, rock, steep);
    vec4 diffuseColor = vec4(c, 1.);`);
  groundMesh = new THREE.Mesh(g, m); groundMesh.receiveShadow = true; groundMesh.frustumCulled = false; scene.add(groundMesh);
  /* water: one plane at WY, coloured by how deep the land is under it */
  const wm = mapShader(toon(), 'q-water', '', null, '', `
    vec4 m = mapAt(vWP.xz); float dep = ${WY.toFixed(2)} - hAt(vWP.xz);
    vec3 c = mix(vec3(.42, .82, .80), vec3(.20, .55, .76), step(.22, dep)); c = mix(c, vec3(.13, .38, .66), step(.6, dep));
    c = mix(c, c * vec3(.55, .62, 1.05) + vec3(.02, .0, .1), step(.5, m.g));
    float r = vn(vWP.xz * 1.1 + vec2(uT * .25, uT * .18)) + vn(vWP.xz * 2.3 - vec2(uT * .2, 0.)) * .6;
    c += vec3(.10, .12, .10) * step(1.12, r);
    float fo = step(dep, .07 + .045 * sin(uT * 1.8 + vWP.x * 1.7 + vWP.z * 1.1));
    c = mix(c, vec3(.94, .98, .96), fo);
    c += step(.992, h21(floor(vWP.xz * 9.) + floor(uT * 2.5))) * .45;
    vec4 diffuseColor = vec4(c, 1.);`);
  waterMesh = new THREE.Mesh(new THREE.PlaneGeometry(MS, MS).rotateX(-Math.PI / 2), wm); waterMesh.position.y = WY; waterMesh.receiveShadow = true; scene.add(waterMesh);
}

/* ---------- grass: blades in a tile that wraps round the camera, bent by wind and by the hero */
const GT = 34, GRASSU = { uCam: { value: new V2() }, uHero: { value: new V3() } };
function buildGrass() {
  const NB = Math.round(qn('grass', 26000)), R = mulberry(11), aB = new Float32Array(NB * 12), aC = new Float32Array(NB * 3), pos = new Float32Array(NB * 9);
  for (let i = 0; i < NB; i++) { const x = R() * GT, z = R() * GT, r1 = R(), r2 = R(); for (let c = 0; c < 3; c++) { const k = (i * 3 + c) * 4; aB[k] = x; aB[k + 1] = z; aB[k + 2] = r1; aB[k + 3] = r2; aC[i * 3 + c] = c; } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('aB', new THREE.BufferAttribute(aB, 4)); g.setAttribute('aC', new THREE.BufferAttribute(aC, 1));
  const m = mapShader(toon({ side: THREE.DoubleSide }), 'q-grass',
    `attribute vec4 aB; attribute float aC; uniform vec2 uCam; uniform vec3 uHero; varying float vTip; varying vec2 vGB; varying float vGR; varying vec4 vGM;`,
    `vec2 base = uCam + mod(aB.xy - uCam + ${(GT / 2).toFixed(1)}, ${GT.toFixed(1)}) - ${(GT / 2).toFixed(1)};
     vec4 gm = mapAt(base); float on = step(aB.z, gm.a * 1.02 - .02);
     float hb = (.15 + .2 * aB.w) * (.6 + .4 * gm.a) * on;
     float wv = sin(uT * 1.5 + base.x * .33 + base.y * .19) * .6 + sin(uT * 2.6 + base.x * .9 + base.y * .55) * .28;
     vec2 bend = vec2(wv * .075, wv * .02);
     vec2 dh = base - uHero.xz; float dl = length(dh); bend += dh / max(dl, .01) * .24 * (1. - smoothstep(.15, 1.15, dl));
     vec3 transformed = vec3(base.x, hAt(base), base.y); float wd = .028 + .014 * aB.w;
     if (aC < .5) transformed.x -= wd; else if (aC < 1.5) transformed.x += wd; else { transformed.y += hb; transformed.xz += bend * (hb / .3); }
     vTip = step(1.5, aC); vGB = base; vGR = aB.w; vGM = gm;`,
    `varying float vTip; varying vec2 vGB; varying float vGR; varying vec4 vGM;`,
    `vec3 c = zoneCol(vGB, vGM); float tip = step(.45, vTip);
     c = mix(c * .86, c * 1.17 + vec3(.03, .04, .0), tip);
     float fl = step(.968, vGR) * step(.62, vTip), gz = step(.5, vGM.g), az = step(.5, vGM.r) * (1. - gz);
     vec3 fc = mix(vec3(1., .97, .85), mix(vec3(1., .82, .25), vec3(1., .55, .72), step(.99, vGR)), step(.98, vGR));
     fc = mix(fc, vec3(.95, .25, .2), az); fc = mix(fc, mix(vec3(.45, 1., .95), vec3(1., .5, .95), step(.985, vGR)) * 1.25, gz);
     c = mix(c, fc, fl);
     vec4 diffuseColor = vec4(c, 1.);`, GRASSU);
  grassMesh = new THREE.Mesh(g, m); grassMesh.frustumCulled = false; grassMesh.receiveShadow = true; scene.add(grassMesh);
}

/* ---------- props: pixel sprites made for this game (PixelLab) standing as upright cards. One atlas, one mesh a map chunk.
   1 sprite pixel = 1 texel: a card is w * TW wide and h * TW / cos(pitch) tall, its foot point snapped to the texel grid. */
const TL = new THREE.TextureLoader(), CP = Math.cos(PITCH), SP = Math.sin(PITCH), TWC = TW / CP, VER = '4';
const SPRTINT = { value: new THREE.Color(1, 1, 1) };
let PROPS = null;
function pixTex(t) { t.magFilter = t.minFilter = THREE.NearestFilter; t.generateMipmaps = false; t.encoding = THREE.LinearEncoding; return t; }
async function loadProps() { const [meta, tex] = await Promise.all([fetch('art/quest/props.json?v=' + VER).then(r => r.json()), TL.loadAsync('art/quest/props.png?v=' + VER)]); PROPS = { tex: pixTex(tex), meta }; }
function snapPt(x, y, z) { const sx = Math.round(x / TW) * TW, cu = y * CP - z * SP; return [sx, y + (Math.round(cu / TW) * TW - cu) / CP]; }
const OBST = [], OGRID = new Map(), CH = 16, CHN = MS / CH, CHUNKS = []; for (let i = 0; i < CHN * CHN; i++) CHUNKS.push({ list: [], items: [], vis: true });
function addObst(x, z, r) { const o = { x, z, r }; OBST.push(o); for (let cx = Math.floor((x - r) / 4); cx <= Math.floor((x + r) / 4); cx++) for (let cz = Math.floor((z - r) / 4); cz <= Math.floor((z + r) / 4); cz++) { const k = cx * 1000 + cz; (OGRID.get(k) || OGRID.set(k, []).get(k)).push(o); } }
function collide(p, r) {   /* push a circle out of trunks / rocks / houses */
  const cx = Math.floor(p.x / 4), cz = Math.floor(p.z / 4);
  for (let a = cx - 1; a <= cx + 1; a++) for (let b = cz - 1; b <= cz + 1; b++) { const l = OGRID.get(a * 1000 + b); if (!l) continue;
    for (const o of l) { const dx = p.x - o.x, dz = p.z - o.z, d = Math.hypot(dx, dz), m = o.r + r; if (d < m && d > 1e-4) { p.x = o.x + dx / d * m; p.z = o.z + dz / d * m; } } }
}
const GLOWS = [];   /* light discs under glowing things, drawn into the effect buffer */
function prop(name, x, z, o = {}) {
  const it = PROPS.meta.items[name]; if (!it) return false; const [sx, sy] = snapPt(x, groundH(x, z) - (o.sink || 0) * TWC, z);
  const ci = clamp(Math.floor((sx + MH) / CH), 0, CHN - 1) + clamp(Math.floor((z + MH) / CH), 0, CHN - 1) * CHN;
  CHUNKS[ci].items.push({ it, x: sx, y: sy, z, sway: o.sway || 0, flip: o.flip ? 1 : 0 });
  if (o.r) addObst(sx + (o.ox || 0), z + (o.oz || 0), o.r); if (o.glow) GLOWS.push({ x: sx, y: groundH(sx, z) + .06, z: z + .3, r: o.glow, c: o.gc || 0x46e6d6 });
  return true;
}
const PCARD = new THREE.PlaneGeometry(1, 1).translate(0, .5, 0);
const PROP_VS = `attribute vec3 aPos; attribute vec4 aRect, aSA; attribute vec2 aSw; uniform float uT; varying vec2 vUv;
  void main(){ float fl = aSw.y, ax = mix(aSA.z, aSA.x - aSA.z, fl);
    vec2 px = vec2((position.x + .5) * aSA.x - ax, position.y * aSA.y - (aSA.y - aSA.w));
    float sw = floor(aSw.x * sin(uT * 1.2 + aPos.x * .6 + aPos.z * .4) * position.y * position.y + .5);
    vUv = aRect.xy + vec2(mix(position.x + .5, .5 - position.x, fl), position.y) * aRect.zw;
    gl_Position = projectionMatrix * viewMatrix * vec4(aPos + vec3((px.x + sw) * ${TW.toFixed(5)}, px.y * ${TWC.toFixed(5)}, 0.), 1.); }`;
let PROPMAT, PROPDEPTH;
function flushProps() {
  PROPMAT = new THREE.ShaderMaterial({ uniforms: { map: { value: PROPS.tex }, uT: TIMEU, uTint: SPRTINT, uSee: SEEU.uSee, uSeeR: SEEU.uSeeR }, vertexShader: PROP_VS, side: THREE.DoubleSide,
    fragmentShader: `uniform sampler2D map; uniform vec3 uTint, uSee; uniform float uSeeR; varying vec2 vUv;
    void main(){ vec4 c = texture2D(map, vUv); if (c.a < .5) discard;
      vec2 sd = gl_FragCoord.xy - uSee.xy; sd.y *= .75; if (dot(sd, sd) < uSeeR * uSeeR && gl_FragCoord.z < uSee.z - .003 && mod(floor(gl_FragCoord.x) + floor(gl_FragCoord.y), 2.) < .5) discard;
      gl_FragColor = vec4(c.rgb * uTint, 1.); }` });
  PROPDEPTH = new THREE.ShaderMaterial({ uniforms: { map: { value: PROPS.tex }, uT: TIMEU }, vertexShader: PROP_VS, side: THREE.DoubleSide,
    fragmentShader: `#include <packing>
    uniform sampler2D map; varying vec2 vUv; void main(){ if (texture2D(map, vUv).a < .5) discard; gl_FragColor = packDepthToRGBA(gl_FragCoord.z); }` });
  const W = PROPS.meta.W, H = PROPS.meta.H;
  for (const c of CHUNKS) { const n = c.items.length; if (!n) continue; c.items.sort((a, b) => a.z - b.z);
    const g = new THREE.InstancedBufferGeometry(); g.index = PCARD.index; g.setAttribute('position', PCARD.attributes.position); g.instanceCount = n;
    const aPos = new Float32Array(n * 3), aRect = new Float32Array(n * 4), aSA = new Float32Array(n * 4), aSw = new Float32Array(n * 2);
    c.items.forEach((q, i) => { const t = q.it; aPos.set([q.x, q.y, q.z], i * 3); aRect.set([t.x / W, 1 - (t.y + t.h) / H, t.w / W, t.h / H], i * 4); aSA.set([t.w, t.h, t.ax, t.ay], i * 4); aSw.set([q.sway, q.flip], i * 2); });
    g.setAttribute('aPos', new THREE.InstancedBufferAttribute(aPos, 3)); g.setAttribute('aRect', new THREE.InstancedBufferAttribute(aRect, 4)); g.setAttribute('aSA', new THREE.InstancedBufferAttribute(aSA, 4)); g.setAttribute('aSw', new THREE.InstancedBufferAttribute(aSw, 2));
    const m = new THREE.Mesh(g, PROPMAT); m.customDepthMaterial = PROPDEPTH; m.castShadow = true; m.frustumCulled = false; scene.add(m); c.list.push(m); }
}
function cullChunks() {   /* only the chunks near the view are drawn (and cast shadows) */
  const hw = PX.bw * TW / 2 + 11, hd = PX.bh * TW / 2 / SP, x0 = CAMT.x - hw, x1 = CAMT.x + hw, z0 = CAMT.z - hd - 9, z1 = CAMT.z + hd + 13;
  for (let cz = 0; cz < CHN; cz++) for (let cx = 0; cx < CHN; cx++) { const c = CHUNKS[cz * CHN + cx], ax = -MH + cx * CH, az = -MH + cz * CH, v = ax < x1 && ax + CH > x0 && az < z1 && az + CH > z0;
    if (v !== c.vis) { c.vis = v; for (const o of c.list) o.visible = v; } }
}
const KEEP = [];   /* clearings where no plant may grow: pack homes, village, lair */
function freeSpot(x, z, pad = 0) { for (const k of KEEP) if (Math.hypot(x - k.x, z - k.z) < k.r + pad) return false; return true; }
function pick3(R, a) { return a[(R() * a.length) | 0]; }
const ZTREES = { 1: [['tree_oak', 5], ['tree_cherry', 2], ['tree_birch', 2]], 2: [['tree_maple', 5], ['tree_ginkgo', 3], ['tree_red', 2]], 3: [['tree_pine', 5], ['shroom_cyan', 3], ['shroom_pink', 2], ['tree_twist', 2], ['shroom_violet', 2]] };
function pickW(R, list) { const l = list.filter(e => PROPS.meta.items[e[0]]); let t = 0; for (const e of l) t += e[1]; let r = R() * t; for (const e of l) { r -= e[1]; if (r <= 0) return e[0]; } return l.length ? l[0][0] : null; }
function buildWorld() {
  buildGround(); buildGrass();
  const R = mulberry(20261127), has = n => !!PROPS.meta.items[n];
  KEEP.push({ x: VILLAGE.x, z: VILLAGE.z, r: VILLAGE.r + 2 }, { x: LAIR.x, z: LAIR.z, r: LAIR.r + 1 }, { x: KINGSPOT.x, z: KINGSPOT.z, r: KINGSPOT.r });
  for (const p of PACKS) KEEP.push({ x: p.x, z: p.z, r: p.big ? 6.5 : 3.4 });
  const tree = (x, z, zn) => { const n = pickW(R, ZTREES[zn]); if (!n) return; const sh = /^shroom/.test(n);
    prop(n, x, z, { sway: sh ? 0 : 2.2, flip: R() < .5, r: sh ? .7 : .55, sink: 2, glow: sh ? 3.4 : 0, gc: n === 'shroom_pink' ? 0xff62b0 : n === 'shroom_violet' ? 0x9a80ff : 0x46e6d6 }); };
  for (let gx = -63; gx <= 63; gx += 3.1) for (let gz = -63; gz <= 63; gz += 3.1) { const x = gx + (R() - .5) * 2.6, z = gz + (R() - .5) * 2.6, e = Math.max(Math.abs(x), Math.abs(z));
    if (groundH(x, z) < WY + .45) continue; const m = mapAt(x, z), zn = m[1] > .5 ? 3 : m[0] > .5 ? 2 : 1;
    if (e > 55.5) { if (R() < .78 && (freeSpot(x, z, 0) || e > 58)) tree(x, z, zn); continue; }
    if (!freeSpot(x, z, 1.2) || pathDist(x, z) < 3) continue;
    const cl = sstep(.42, .62, fbm(x / 9 + 30, z / 9 + 12, 2)), p = zn === 1 ? .03 + cl * .2 : zn === 2 ? .2 + cl * .36 : .17 + cl * .34;
    if (R() < p) tree(x, z, zn); }
  const BUSH = { 1: ['bush_green', 'bush_flower', 'flowers_a', 'flowers_b', 'flowers_a'], 2: ['bush_autumn', 'bush_autumn', 'stump', 'flowers_b'], 3: ['bush_moon', 'crystal', 'shroom_small', 'shroom_small'] };
  for (let gx = -56; gx <= 56; gx += 2.6) for (let gz = -56; gz <= 56; gz += 2.6) { const x = gx + (R() - .5) * 2.3, z = gz + (R() - .5) * 2.3;
    if (groundH(x, z) < WY + .45 || pathDist(x, z) < 2 || !freeSpot(x, z, -1.5)) continue; const m = mapAt(x, z), zn = m[1] > .5 ? 3 : m[0] > .5 ? 2 : 1, r = R();
    if (r < (zn === 1 ? .2 : .19)) { const n = pick3(R, BUSH[zn].filter(has)); if (n) prop(n, x, z, { sway: /bush|flowers/.test(n) ? 1 : 0, flip: R() < .5, r: /stump|crystal/.test(n) ? .5 : 0, sink: 1, glow: /crystal|shroom/.test(n) ? 1.6 : 0, gc: n === 'crystal' ? 0x6ab0ff : 0x46e6d6 }); }
    else if (r < (zn === 1 ? .225 : .22)) { const n = pick3(R, ['rock_a', 'rock_b', 'rock_moss'].filter(has)); if (n) prop(n, x, z, { flip: R() < .5, r: .7, sink: 1 }); } }
  for (const [px, pz, pr] of PONDS) for (let i = 0; i < 6; i++) { const a = R() * TAU, d = pr * (1.08 + R() * .22), x = px + Math.cos(a) * d, z = pz + Math.sin(a) * d; if (groundH(x, z) < WY + .25 || pathDist(x, z) < 2) continue; const n = pick3(R, ['rock_a', 'rock_b', 'rock_moss', 'bush_green'].filter(has)); if (n) prop(n, x, z, { flip: R() < .5, r: /rock/.test(n) ? .7 : 0, sink: 1 }); }
  /* the camp */
  const V = VILLAGE;
  prop('house_cottage', V.x - 8, V.z - 4.5, { r: 2.3, oz: -1.4 }); prop(has('house_forge') ? 'house_forge' : 'house_cottage', V.x + 8.2, V.z - 4, { r: 2.3, oz: -1.4, flip: !has('house_forge') });
  prop(has('house_b') ? 'house_b' : 'house_cottage', V.x - 9.5, V.z + 6.5, { r: 2.3, oz: -1.4, flip: true }); prop('tent', V.x + 9, V.z + 6, { r: 1.5, oz: -.8 });
  prop('campfire', V.x, V.z + .5, { r: .7 }); prop('signpost', V.x - 2.2, V.z - 9.5, { r: .3 }); prop('well', V.x + 3.6, V.z + 6.2, { r: 1 }); prop('crates', V.x + 4.6, V.z - 1.6, { r: .9 });
  for (let i = 0; i < 12; i++) { const a = -2.75 + i * .21; if (Math.abs(a + Math.PI / 2) < .3) continue; prop('fence', V.x + Math.cos(a) * 12.4, V.z + Math.sin(a) * 12.4 + 1, { r: .5 }); }
  flushProps();
}
