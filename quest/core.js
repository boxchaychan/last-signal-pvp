/* quest/core.js: utils, the pixel renderer (low-res target + depth outline + effect buffer with glow), toon materials.
   Part of quest.html "ผู้กล้าแดนพิกเซล". Plain scripts sharing globals, loaded in the order core, world, fx, game, ui. */
'use strict';
const Q = new URLSearchParams(location.search), qn = (k, d) => (Q.has(k) ? +Q.get(k) : d);
const V3 = THREE.Vector3, V2 = THREE.Vector2, TAU = Math.PI * 2;
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v), lerp = (a, b, t) => a + (b - a) * t;
const sstep = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const rnd = (a = 0, b = 1) => a + Math.random() * (b - a), pick = a => a[(Math.random() * a.length) | 0];
const angDiff = (a, b) => { let d = (b - a) % TAU; if (d > Math.PI) d -= TAU; if (d < -Math.PI) d += TAU; return d; };
const dist2 = (ax, az, bx, bz) => Math.hypot(ax - bx, az - bz);
function mulberry(s) { return () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function hash2(x, y) { let h = (Math.imul(x | 0, 374761393) + Math.imul(y | 0, 668265263)) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
function vnoise(x, y) { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash2(xi, yi), b = hash2(xi + 1, yi), c = hash2(xi, yi + 1), d = hash2(xi + 1, yi + 1); return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; }
function fbm(x, y, o = 3) { let s = 0, a = .5, f = 1, n = 0; for (let i = 0; i < o; i++) { s += a * vnoise(x * f, y * f); n += a; f *= 2; a *= .5; } return s / n; }

/* ---------- look: texel size, camera */
const PXH = qn('pxh', 380);            /* texels across the short side of the screen (about) */
const TW = qn('tw', .03);              /* world units a texel: the hero (1.75 tall) is about 48 texels */
const PITCH = qn('pitch', 40) * Math.PI / 180, CAMD = 70;
const PX = { k: 4, w: 0, h: 0, bw: 0, bh: 0, m: 2, T: 1, dpr: 1, SW: 0, SH: 0 };
const glc = document.getElementById('gl'), loC = document.getElementById('lo'), hiC = document.getElementById('hi');
const lo = loC.getContext('2d'), hi = hiC.getContext('2d');
const renderer = new THREE.WebGLRenderer({ canvas: glc, antialias: false, alpha: false, powerPreference: 'high-performance' });
renderer.setPixelRatio(1); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.BasicShadowMap; renderer.outputEncoding = THREE.LinearEncoding;
const scene = new THREE.Scene(), fxScene = new THREE.Scene();
scene.background = new THREE.Color(0x1c2233);
const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 240);
const TIMEU = { value: 0 };
const FXU = { tDepth: { value: null }, uRes: { value: new V2(1, 1) } };
let rt = null, fxRT = null, glowRT = null;

const QUAD = new THREE.PlaneGeometry(2, 2), VS_FULL = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }';
const glowMat = new THREE.ShaderMaterial({ uniforms: { tF: { value: null }, px: { value: new V2() } }, vertexShader: VS_FULL, depthTest: false, depthWrite: false,
  fragmentShader: `uniform sampler2D tF; uniform vec2 px; varying vec2 vUv;
  void main(){ vec3 s = texture2D(tF, vUv).rgb * 2.;
    for (int i = 0; i < 8; i++) { float a = float(i) * .7854; vec2 d = vec2(cos(a), sin(a)); s += texture2D(tF, vUv + d * px * 2.5).rgb + texture2D(tF, vUv + d * px * 6.).rgb * .7; }
    gl_FragColor = vec4(s / 15.6, 1.); }` });
const postMat = new THREE.ShaderMaterial({ uniforms: { tC: { value: null }, tD: { value: null }, tF: { value: null }, tG: { value: null }, px: { value: new V2() }, edge: { value: .35 / 239 },
  uGrade: { value: new V3(1, 1, 1) }, uFlash: { value: 0 }, uDark: { value: 0 } }, vertexShader: VS_FULL, depthTest: false, depthWrite: false,
  fragmentShader: `uniform sampler2D tC, tD, tF, tG; uniform vec2 px; uniform float edge, uFlash, uDark; uniform vec3 uGrade; varying vec2 vUv;
  void main(){ vec3 c = texture2D(tC, vUv).rgb; float d = texture2D(tD, vUv).r;
    float dl = texture2D(tD, vUv + vec2(-px.x, 0.)).r, dr = texture2D(tD, vUv + vec2(px.x, 0.)).r, du = texture2D(tD, vUv + vec2(0., px.y)).r, dd = texture2D(tD, vUv + vec2(0., -px.y)).r;
    float far = max(max(dl, dr), max(du, dd)) - d;
    if (far > edge) c *= vec3(.30, .24, .36);                              /* dark violet outline on the near side of a depth edge */
    c *= uGrade; c = mix(c, c * vec3(.45, .45, .62), uDark);
    vec3 f = texture2D(tF, vUv).rgb, g = texture2D(tG, vUv).rgb;
    c += f + g * 1.1; c = mix(c, vec3(1.), uFlash);
    gl_FragColor = vec4(c, 1.); }` });
const postScene = new THREE.Scene(), postCam = new THREE.Camera(), postQuad = new THREE.Mesh(QUAD, postMat); postQuad.frustumCulled = false; postScene.add(postQuad);

function resize() {
  const SW = innerWidth, SH = innerHeight, dpr = devicePixelRatio || 1, dw = Math.round(SW * dpr), dh = Math.round(SH * dpr);
  PX.SW = SW; PX.SH = SH; PX.dpr = dpr; PX.k = Math.max(1, Math.round(Math.min(dw, dh) / PXH)); PX.T = PX.k / dpr;
  PX.w = Math.ceil(dw / PX.k); PX.h = Math.ceil(dh / PX.k); PX.w += PX.w & 1; PX.h += PX.h & 1;   /* even: sprite pixels land on texel edges */ PX.bw = PX.w + PX.m * 2; PX.bh = PX.h + PX.m * 2;
  renderer.setSize(PX.bw, PX.bh, false); glc.style.width = PX.bw * PX.T + 'px'; glc.style.height = PX.bh * PX.T + 'px';
  if (rt) { rt.dispose(); fxRT.dispose(); glowRT.dispose(); }
  rt = new THREE.WebGLRenderTarget(PX.bw, PX.bh, { minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
  rt.depthTexture = new THREE.DepthTexture(PX.bw, PX.bh); rt.depthTexture.type = THREE.UnsignedIntType;
  fxRT = new THREE.WebGLRenderTarget(PX.bw, PX.bh, { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, depthBuffer: false });
  glowRT = new THREE.WebGLRenderTarget(Math.ceil(PX.bw / 2), Math.ceil(PX.bh / 2), { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, depthBuffer: false });
  const u = postMat.uniforms; u.tC.value = rt.texture; u.tD.value = rt.depthTexture; u.tF.value = fxRT.texture; u.tG.value = glowRT.texture; u.px.value.set(1 / PX.bw, 1 / PX.bh);
  glowMat.uniforms.tF.value = fxRT.texture; glowMat.uniforms.px.value.set(1 / PX.bw, 1 / PX.bh);
  FXU.tDepth.value = rt.depthTexture; FXU.uRes.value.set(PX.bw, PX.bh);
  cam.left = -PX.bw * TW / 2; cam.right = PX.bw * TW / 2; cam.top = PX.bh * TW / 2; cam.bottom = -PX.bh * TW / 2; cam.updateProjectionMatrix();
  loC.width = PX.w; loC.height = PX.h; loC.style.width = PX.w * PX.T + 'px'; loC.style.height = PX.h * PX.T + 'px';
  hiC.width = dw; hiC.height = dh; hiC.style.width = SW + 'px'; hiC.style.height = SH + 'px';
  if (typeof layoutUI === 'function') layoutUI();
}
addEventListener('resize', resize);

/* camera: orthographic, fixed pitch, looking north (-z); snapped to whole texels, the canvas takes the rest */
const CAMT = new V3(0, 0, 40), SHAKE = { a: 0, x: 0, y: 0 };
function placeCamera() {
  const sp = Math.sin(PITCH), cp = Math.cos(PITCH);
  const px = CAMT.x + SHAKE.x, py = CAMT.y + sp * CAMD + SHAKE.y * cp, pz = CAMT.z + cp * CAMD - SHAKE.y * sp;
  const cr = px, cu = py * cp - pz * sp, crs = Math.round(cr / TW) * TW, cus = Math.round(cu / TW) * TW;
  cam.position.set(px + (crs - cr), py + cp * (cus - cu), pz - sp * (cus - cu)); cam.rotation.set(-PITCH, 0, 0); cam.updateMatrixWorld();
  const sd = v => Math.round(v * PX.dpr) / PX.dpr, offR = (cr - crs) / TW, offU = (cu - cus) / TW;
  PX.ox = offR; PX.oy = offU;
  glc.style.transform = `translate(${sd(-(PX.m + offR) * PX.T)}px, ${sd(-(PX.m - offU) * PX.T)}px)`;
}
const _pv = new V3();
function toLo(x, y, z) { _pv.set(x, y, z).project(cam); return [(_pv.x * .5 + .5) * PX.bw - PX.m, (1 - (_pv.y * .5 + .5)) * PX.bh - PX.m, _pv.z * .5 + .5]; }   /* world -> UI texel */
function groundAt(tx, ty) {   /* UI texel -> point on the plane y = h (the hero's feet height) */
  const nx = ((tx + PX.m) / PX.bw) * 2 - 1, ny = (1 - (ty + PX.m) / PX.bh) * 2 - 1, o = new V3(nx, ny, -1).unproject(cam), sp = Math.sin(PITCH), cp = Math.cos(PITCH);
  const h = (typeof P !== 'undefined' && P) ? P.y : 0, t = (o.y - h) / sp; return new V3(o.x, h, o.z - cp * t);
}

/* ---------- lights */
const SUNDIR = new V3(-.5, 1, .42).normalize();
const hemi = new THREE.HemisphereLight(0xa9b6ff, 0x8a7a92, .5); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff0d0, .62); sun.castShadow = true; scene.add(sun, sun.target);
sun.shadow.mapSize.set(2048, 2048); const SHB = 19; Object.assign(sun.shadow.camera, { left: -SHB, right: SHB, top: SHB, bottom: -SHB, near: 1, far: 140 }); sun.shadow.bias = -.0006; sun.shadow.normalBias = .03;
const _lx = new V3().crossVectors(new V3(0, 1, 0), SUNDIR).normalize(), _ly = new V3().crossVectors(SUNDIR, _lx).normalize();
function placeSun() {   /* the shadow box follows the view, moved in whole shadow texels so shadows do not swim */
  const ts = SHB * 2 / 2048, a = Math.round(CAMT.dot(_lx) / ts) * ts, b = Math.round(CAMT.dot(_ly) / ts) * ts, c = CAMT.dot(SUNDIR);
  sun.target.position.set(0, 0, 0).addScaledVector(_lx, a).addScaledVector(_ly, b).addScaledVector(SUNDIR, c);
  sun.position.copy(sun.target.position).addScaledVector(SUNDIR, 70); sun.target.updateMatrixWorld();
}
const LPOOL = []; for (let i = 0; i < 4; i++) { const l = new THREE.PointLight(0xffffff, 0, 9, 1.6); l.userData = { t: 0, life: 1, i0: 0 }; scene.add(l); LPOOL.push(l); }
function flashLight(x, y, z, col, inten = 2.2, life = .35, dist = 9) { let l = LPOOL[0]; for (const q of LPOOL) if (q.intensity < l.intensity) l = q;
  l.position.set(x, y, z); l.color.set(col); l.distance = dist; l.userData.t = 0; l.userData.life = life; l.userData.i0 = inten; l.intensity = inten; }
function updLights(dt) { for (const l of LPOOL) if (l.intensity > 0) { const u = l.userData; u.t += dt; l.intensity = Math.max(0, u.i0 * (1 - u.t / u.life)); } }

/* ---------- toon materials */
const GRAD = (() => { const d = new Uint8Array([70, 70, 70, 255, 150, 150, 150, 255, 232, 232, 232, 255, 255, 255, 255, 255]), t = new THREE.DataTexture(d, 4, 1, THREE.RGBAFormat);
  t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t; })();
const SEEU = { uSee: { value: new V3(-999, -999, 0) }, uSeeR: { value: 30 } };
function seeThrough(mat) {   /* props in front of the hero get a checker hole round her so she is never hidden */
  const prev = mat.onBeforeCompile;
  mat.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r); sh.uniforms.uSee = SEEU.uSee; sh.uniforms.uSeeR = SEEU.uSeeR;
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform vec3 uSee; uniform float uSeeR;')
      .replace('#include <clipping_planes_fragment>', `#include <clipping_planes_fragment>
      { vec2 sd = gl_FragCoord.xy - uSee.xy; sd.y *= .8; if (dot(sd, sd) < uSeeR * uSeeR && gl_FragCoord.z < uSee.z - .004 && mod(floor(gl_FragCoord.x) + floor(gl_FragCoord.y), 2.) < .5) discard; }`); };
  mat.customProgramCacheKey = () => (mat.userData.key || '') + '|see';
  return mat;
}
function toon(o = {}) { const m = new THREE.MeshToonMaterial(Object.assign({ gradientMap: GRAD }, o)); return m; }
function rawTex(t) { if (t) { t.encoding = THREE.LinearEncoding; t.needsUpdate = true; } return t; }
function toonify(root, { cast = true, recv = true, own = false, see = false } = {}) {   /* glTF materials -> toon, colours shown as they are (no sRGB step in this pipeline) */
  const cache = new Map(), mats = [];
  root.traverse(o => { if (!o.isMesh) return; o.castShadow = cast; o.receiveShadow = recv;
    const conv = m => { if (!own && cache.has(m)) return cache.get(m);
      const t = toon({ color: m.color ? m.color.clone().convertLinearToSRGB() : new THREE.Color(1, 1, 1), map: rawTex(m.map) || null, transparent: m.transparent, alphaTest: m.alphaTest || 0, side: m.side });
      if (t.map) { t.map.magFilter = THREE.NearestFilter; }
      t.name = m.name; if (see) seeThrough(t); cache.set(m, t); mats.push(t); return t; };
    o.material = Array.isArray(o.material) ? o.material.map(conv) : conv(o.material); });
  return mats;
}

/* ---------- frame render */
function renderFrame() {
  renderer.setRenderTarget(rt); renderer.render(scene, cam);
  renderer.setRenderTarget(fxRT); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(fxScene, cam);
  postQuad.material = glowMat; renderer.setRenderTarget(glowRT); renderer.render(postScene, postCam);
  postQuad.material = postMat; renderer.setRenderTarget(null); renderer.render(postScene, postCam);
}
