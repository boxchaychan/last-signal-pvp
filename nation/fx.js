'use strict';
/* ก่อร่างสร้างชาติ: the life of the map: tree species, cars, street lamps, pavements, skyline, clouds. All made in code. */
if (!MOBILE) document.body.classList.add('hi');
ROAD_STYLE[2] = ['#b39568', .44, 0]; ROAD_STYLE[3] = ['#85878a', .54, '#d8d1c2']; ROAD_STYLE[4] = ['#5a5c62', .62, '#d6d0c2'];

/* ---------- trees: broadleaf, pine, palm ---------- */
W.initTrees = function (seed) {
  const R = RNG(seed + 77), B = new MB(), P = new MB(), L = new MB();
  B.cyl(0, 0, 0, .08, .34, 0x6e4f33, .055, 5); B.cyl(0, .26, 0, .44, .36, 0xffffff, .5, 6); B.cyl(0, .62, 0, .5, .44, 0xf2f7ea, .08, 6); B.cyl(.22, .34, .12, .25, .3, 0xe8f2dd, .05, 5);
  P.cyl(0, 0, 0, .08, .3, 0x5f4630, .05, 5); P.cyl(0, .22, 0, .44, .56, 0xe3eedb, .14, 6); P.cyl(0, .58, 0, .34, .54, 0xf0f6e8, .08, 6); P.cyl(0, .98, 0, .2, .46, 0xffffff, 0, 6);
  L.cyl(0, 0, 0, .06, 1.02, 0x8a6b48, .035, 5); for (let i = 0; i < 6; i++) { const a = i / 6 * 6.283, c = Math.cos(a), s = Math.sin(a), px = -s * .1, pz = c * .1, tip = [c * .62, .76, s * .62], A = [px, 1.02, pz], D = [-px, 1.02, -pz], M = [c * .32 + px * .9, 1.12, s * .32 + pz * .9], N2 = [c * .32 - px * .9, 1.12, s * .32 - pz * .9]; L.add(1, [A, M, D, D, M, N2, M, tip, N2, D, M, A, N2, M, D, N2, tip, M], 0xffffff, 0); }
  const geos = [B.build(), P.build(), L.build()], lists = [[], [], []], mat = new THREE.MeshLambertMaterial({ vertexColors: true });
  for (let z = 0; z < N; z++) for (let x = 0; x < N; x++) { const t = W.T[ci(x, z)], p = t === 4 ? .62 : t === 5 ? .32 : t === 3 ? .035 : t === 6 ? .05 : t === 2 ? .09 : 0; if (R() >= p || (Math.hypot(x - W.start.x, z - W.start.z) <= 5 && R() > .15)) continue; lists[t === 2 ? 2 : (t === 5 || t === 6 || R() < .22) ? 1 : 0].push([x, z]); }
  const cap = MOBILE ? 2600 : 5200, total = lists[0].length + lists[1].length + lists[2].length, keep = Math.min(1, cap / Math.max(total, 1));
  const dummy = new THREE.Object3D(), C = new THREE.Color(); W.treeMeshes = []; let live = 0;
  lists.forEach((l0, sp) => {
    const l = l0.filter(() => R() < keep), im = new THREE.InstancedMesh(geos[sp], mat, Math.max(1, l.length)); im.castShadow = !MOBILE; im.frustumCulled = false; im.count = l.length;
    l.forEach((q, i) => {
      const px = q[0] + .2 + R() * .6, pz = q[1] + .2 + R() * .6, s = (sp === 2 ? 1 : .85) + R() * .75; dummy.position.set(px, W.h(px, pz) - .04, pz); dummy.rotation.y = R() * 6; dummy.scale.set(s, s * (.9 + R() * .42), s); dummy.updateMatrix(); im.setMatrixAt(i, dummy.matrix); const v = R();
      if (sp === 0) { const au = R() < .07; au ? C.setRGB(.82 + v * .1, .56 + v * .14, .24) : C.setRGB(.34 + v * .2, .58 + v * .16, .25 + v * .08); } else if (sp === 1) C.setRGB(.2 + v * .1, .42 + v * .12, .29 + v * .08); else C.setRGB(.42 + v * .14, .68 + v * .1, .3); im.setColorAt(i, C);
      const c = ci(q[0], q[1]); if (!W.treeAt.has(c)) W.treeAt.set(c, []); W.treeAt.get(c).push(sp * 100000 + i); live++;
    }); W.scene.add(im); W.treeMeshes.push(im);
  }); W.treeTotal = W.treeLive = Math.max(1, live);
};
W.clearTrees = function (x, z, w, d) {
  const zero = new THREE.Matrix4().makeScale(0, 0, 0); let ch = false;
  for (let a = x; a < x + w; a++) for (let b = z; b < z + d; b++) { const c = ci(a, b), l = W.treeAt.get(c); if (!l) continue; for (const e of l) { const im = W.treeMeshes[Math.floor(e / 100000)]; im.setMatrixAt(e % 100000, zero); im.instanceMatrix.needsUpdate = true; W.treeLive--; } W.treeAt.delete(c); ch = true; }
  if (ch) W.needShadow = true;
};

/* ---------- pavement under city buildings ---------- */
const PAD = { row: 1, apt: 1, tower: 1, mega: 1, shop: 1, office: 1, cbd: 1, market: 1, hall: 1, school: 1, hischool: 1, univ: 1, clinic: 1, hospital: 1, medcenter: 1, police: 1, policehq: 1, parliament: 1 };
const paintRoad0 = W.paintRoad;
W.paintPad = function (b) {
  if (!PAD[b.t] || !W.gctx) return; const g = W.gctx, p = TEX / N, m = .3, x = (b.x - m) * p, y = (b.z - m) * p, w = (b.w + m * 2) * p, h = (b.d + m * 2) * p, r = .34 * p;
  g.fillStyle = 'rgba(92,88,78,.28)'; g.beginPath(); g.moveTo(x + r, y + 2); g.arcTo(x + w + 2, y + 2, x + w + 2, y + h + 2, r); g.arcTo(x + w + 2, y + h + 2, x, y + h + 2, r); g.arcTo(x, y + h + 2, x, y, r); g.arcTo(x, y + 2, x + w, y + 2, r); g.fill();
  g.fillStyle = '#d5cfc1'; g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.fill();
  for (let a = b.x - 2; a < b.x + b.w + 2; a++) for (let c = b.z - 2; c < b.z + b.d + 2; c++) if (inMap(a, c) && W.road[ci(a, c)]) paintRoad0(a, c); W.dirty = true;
};
const occupy0 = W.occupy; W.occupy = function (b) { occupy0(b); W.paintPad(b); };

/* ---------- skyline: taller in the middle of each city ---------- */
const TALL = { apt: 1, tower: 1, mega: 1, office: 1, cbd: 1 };
W.heightK = function (b) { if (!TALL[b.t]) return 1; const C = G.cities[b.city]; if (!C) return 1; const R = Math.sqrt(C.n + 1) * 1.8 + 6, r = Math.hypot(b.x + b.w / 2 - C.x, b.z + b.d / 2 - C.z) / R; return clamp(1.3 - r * .78, .6, 1.32) * (.88 + ((b.id * 37) % 24) / 100); };

/* ---------- street lamps ---------- */
W.initLamps = function () {
  const m = new MB(); m.box(0, 0, 0, .035, .62, .035, 0x4c5158); m.box(.09, .6, 0, .2, .025, .03, 0x4c5158); m.box(.18, .565, 0, .08, .035, .06, 0xffe7a8, 1);
  W.lampMesh = new THREE.InstancedMesh(m.build(), W.bmat, 460); W.lampMesh.count = 0; W.lampMesh.frustumCulled = false; W.scene.add(W.lampMesh); W.lampSet = new Set();
  const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'), rg = g.createRadialGradient(32, 32, 1, 32, 32, 32); rg.addColorStop(0, 'rgba(255,240,190,1)'); rg.addColorStop(.25, 'rgba(255,205,120,.55)'); rg.addColorStop(1, 'rgba(255,180,80,0)'); g.fillStyle = rg; g.fillRect(0, 0, 64, 64);
  const geo = new THREE.BufferGeometry(); W.lampPos = new Float32Array(460 * 3); geo.setAttribute('position', new THREE.BufferAttribute(W.lampPos, 3)); geo.setDrawRange(0, 0);
  W.lampGlow = new THREE.Points(geo, new THREE.PointsMaterial({ size: 1.15, map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0 })); W.lampGlow.frustumCulled = false; W.scene.add(W.lampGlow);
};
W.lampAt = function (x, z) {
  if (!W.lampMesh || (x * 7 + z * 3) % 4 !== 0) return; const c = ci(x, z); if (W.lampSet.has(c) || W.lampSet.size >= 460 || W.T[c] === 1) return; let dx = 0, dz = 0; for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (inMap(x + a, z + b) && W.road[ci(x + a, z + b)] >= 2) { dx = a; dz = b; break; }
  const side = (x + z) % 2 ? 1 : -1, ox = x + .5 - dz * .4 * side, oz = z + .5 + dx * .4 * side, y = W.h(ox, oz), o = W._o, i = W.lampSet.size; W.lampSet.add(c); o.position.set(ox, y, oz); o.rotation.set(0, Math.atan2(dz * side, dx * side) + Math.PI, 0); o.scale.set(1, 1, 1); o.updateMatrix(); W.lampMesh.setMatrixAt(i, o.matrix); W.lampMesh.count = i + 1; W.lampMesh.instanceMatrix.needsUpdate = true;
  W.lampPos[i * 3] = ox + dz * side * .16; W.lampPos[i * 3 + 1] = y + .58; W.lampPos[i * 3 + 2] = oz - dx * side * .16; W.lampGlow.geometry.attributes.position.needsUpdate = true; W.lampGlow.geometry.setDrawRange(0, i + 1);
};
W.paintRoad = function (x, z) { paintRoad0(x, z); if (W.road[ci(x, z)] >= 3) W.lampAt(x, z); };

/* ---------- cars on real roads ---------- */
const CAR_COL = [0xe9e9e6, 0x2f3238, 0xc8423a, 0x3a78c9, 0xd9d4c6, 0x8f969e, 0xe6b23a, 0x3f9a78]; const CAR_MAX = MOBILE ? 34 : 80;
W.initCars = function () {
  const m = new MB(); m.box(0, .045, 0, .19, .075, .42, 0xffffff); m.box(0, .12, -.025, .16, .07, .22, 0xffffff); m.box(0, .125, -.025, .168, .05, .19, 0x2c3a46, .5); m.box(0, .125, -.025, .13, .05, .232, 0x2c3a46, .5); for (const a of [-1, 1]) for (const b of [-1, 1]) m.box(a * .095, .012, b * .135, .03, .06, .08, 0x1f2125); for (const a of [-1, 1]) m.box(a * .065, .07, .213, .04, .025, .012, 0xfff2c0, 1);
  const im = W.carMesh = new THREE.InstancedMesh(m.build(), W.bmat, CAR_MAX); im.count = 0; im.frustumCulled = false; im.castShadow = !MOBILE; const C = new THREE.Color(); for (let i = 0; i < CAR_MAX; i++) { C.setHex(CAR_COL[i % CAR_COL.length]); im.setColorAt(i, C); } W.scene.add(im); W.cars = []; W._roadT = 0; W.roadCells = [];
};
function roadNext(c, from) { const x = c % N, z = c / N | 0, o = []; for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) { if (!inMap(x + a, z + b)) continue; const d = ci(x + a, z + b); if (W.road[d] >= 2 && d !== from) o.push(d); } return o.length ? o[Math.random() * o.length | 0] : from; }
W.stepCars = function (dt, t) {
  if (t - W._roadT > 4) { W._roadT = t; const L = []; for (let c = 0; c < N * N; c++) if (W.road[c] >= 2) L.push(c); W.roadCells = L; }
  const pop = (G.S.x && G.S.x.pop) || 0, want = W.roadCells.length < 8 ? 0 : Math.min(CAR_MAX, Math.floor(W.roadCells.length / 4), Math.floor(pop / 45)), o = W._o;
  while (W.cars.length < want) { const c = pick(W.roadCells), n = roadNext(c, -1); W.cars.push({ c, n, f: 0, sp: 1.5 + Math.random() * 1.3, x: c % N + .5, z: (c / N | 0) + .5, a: 0 }); } W.cars.length = Math.min(W.cars.length, want);
  W.cars.forEach((q, i) => {
    if (W.road[q.c] < 2) { q.c = pick(W.roadCells); q.n = roadNext(q.c, -1); q.f = 0; } const ax = q.c % N + .5, az = (q.c / N | 0) + .5, bx = q.n % N + .5, bz = (q.n / N | 0) + .5, dx = bx - ax, dz = bz - az, l = Math.hypot(dx, dz) || 1;
    q.f += dt * q.sp * (W.road[q.c] >= 4 ? 1.3 : W.road[q.c] === 3 ? 1 : .68) / l; if (q.f >= 1) { const old = q.c; q.c = q.n; q.n = roadNext(q.c, old); q.f = 0; }
    const px = ax + dx * q.f - dz / l * .13, pz = az + dz * q.f + dx / l * .13, tg = Math.atan2(dx, dz); let d = tg - q.a; while (d > Math.PI) d -= 6.2832; while (d < -Math.PI) d += 6.2832; q.a += d * Math.min(1, dt * 9); const ty = W.T[ci(clamp(px | 0, 0, N - 1), clamp(pz | 0, 0, N - 1))] === 1 ? .2 : W.h(px, pz) + .03;
    o.position.set(px, ty, pz); o.rotation.set(0, q.a, 0); o.scale.setScalar(1); o.updateMatrix(); W.carMesh.setMatrixAt(i, o.matrix);
  }); W.carMesh.count = W.cars.length; W.carMesh.instanceMatrix.needsUpdate = true;
};

/* ---------- clouds drift over the country when zoomed out ---------- */
W.initClouds = function () {
  const m = new MB(); for (const q of [[0, 0, 2.4], [2.3, .4, 1.8], [-2.2, -.3, 1.7], [.7, -1.5, 1.5], [-.8, 1.5, 1.5]]) { m.cyl(q[0], 0, q[1], q[2], q[2] * .5, 0xffffff, q[2] * .86, 8); m.cyl(q[0], q[2] * .5, q[1], q[2] * .86, q[2] * .55, 0xffffff, .1, 8); }
  const mat = W.cloudMat = new THREE.MeshLambertMaterial({ vertexColors: true, transparent: true, opacity: 0, depthWrite: false, emissive: 0x777777 }), im = W.clouds = new THREE.InstancedMesh(m.build(), mat, 13); im.frustumCulled = false; im.renderOrder = 4; W.scene.add(im); W.cloudD = [];
  for (let i = 0; i < 13; i++) W.cloudD.push({ x: Math.random() * (N + 80) - 40, z: Math.random() * (N + 80) - 40, y: 30 + Math.random() * 9, s: .9 + Math.random() * 1.5, r: Math.random() * 6, v: .25 + Math.random() * .4 });
};
W.stepClouds = function (dt) {
  const op = clamp((W.cam.dist - 44) / 52) * .82; W.cloudMat.opacity = op; W.clouds.visible = op > .01; if (!W.clouds.visible) return; const o = W._o;
  W.cloudD.forEach((c, i) => { c.x += c.v * dt; if (c.x > N + 46) c.x = -46; o.position.set(c.x, c.y, c.z); o.rotation.set(0, c.r, 0); o.scale.set(c.s, c.s * .72, c.s); o.updateMatrix(); W.clouds.setMatrixAt(i, o.matrix); }); W.clouds.instanceMatrix.needsUpdate = true;
};

const init0 = W.init; W.init = function (cv, seed) { init0(cv, seed); W.initLamps(); W.initCars(); W.initClouds(); };
const render0 = W.render;
W.render = function (t, dt) {
  if (G.started && G.S) { const run = G.modal || G.prop || !G.speed ? 0 : Math.min(G.speed, 3); W.stepCars(dt * run, t); W.stepClouds(dt); W.lampGlow.material.opacity = clamp(W.nightU.value * 1.15); }
  render0(t, dt);
};
