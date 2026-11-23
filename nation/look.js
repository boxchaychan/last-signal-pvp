'use strict';
/* ก่อร่างสร้างชาติ: what the country's state looks like on the map: collapsed and abandoned buildings, factory smoke, street trees. */
if (typeof ISO_ON === 'undefined' || !ISO_ON) (function () {
  /* ---------- ruins and closed factories ---------- */
  const rubG = new THREE.IcosahedronGeometry(.3, 0), rubM = [0x5d5a55, 0x7b6a58, 0x8d8a83, 0x3f3b37].map(c => new THREE.MeshLambertMaterial({ color: c, flatShading: true })), shade = new THREE.MeshBasicMaterial({ color: 0x20242a, transparent: true, opacity: .38, depthWrite: false });
  W.ruinLook = function (b, on) {
    const s = W.sites.get(b.id); if (!s) return; const mesh = s.gr.children[0]; for (let i = 1; i < s.gr.children.length; i++) s.gr.children[i].visible = !on || s.gr.children[i] === s.rub;
    if (s.rub) { s.gr.remove(s.rub); s.rub = null; } const hk = W.heightK ? W.heightK(b) : 1;
    if (!on) { mesh.scale.y = hk; s.geo.setDrawRange(0, Math.floor(s.total * b.prog / 3) * 3); return; }
    const d = G.S.r && G.S.r.dmg[b.id], rub = new THREE.Group(); s.rub = rub; s.gr.add(rub);
    if (d && d.c) { mesh.scale.y = hk; s.geo.setDrawRange(0, s.total); s.geo.computeBoundingBox && 0; const g = W.geoFor(b.t, b.v); if (!g.boundingBox) g.computeBoundingBox(); const B = g.boundingBox, h = (B.max.y - B.min.y) * hk + .04, w = B.max.x - B.min.x + .05, l = B.max.z - B.min.z + .05, m = new THREE.Mesh(new THREE.BoxGeometry(w, h, l), shade); m.position.set((B.max.x + B.min.x) / 2, h / 2, (B.max.z + B.min.z) / 2); rub.add(m); return; }
    mesh.scale.y = hk * .34; s.geo.setDrawRange(0, Math.floor(s.total * .62 / 3) * 3); let seed = b.id * 73 + 11; const R = () => (seed = (seed * 16807) % 2147483647) / 2147483647, n = 4 + Math.min(5, b.w + b.d - 2);
    for (let i = 0; i < n; i++) { const p = new THREE.Mesh(rubG, rubM[i % 4]), k = .55 + R() * 1.1; p.scale.set(k, k * (.5 + R() * .4), k * (.7 + R() * .5)); p.position.set((R() - .5) * b.w * .82, .1 + R() * .16, (R() - .5) * b.d * .82); p.rotation.set(R() * 3, R() * 3, R() * 3); p.castShadow = true; rub.add(p); }
  };
  /* ---------- smoke from working factories ---------- */
  const N_S = MOBILE ? 70 : 170, SMOKY = { coal: [[0, 0]], steel: [[-1.7, -.8], [-.5, -.8]], plant: [[0, -1.2]], factory: [[.8, -.8]], workshop: [[.4, -.4]], mine: [[1.05, -.55]], machine: [[1.2, -.6]] }; let P = null, pos, aA, aS, list = [], tList = 0, emit = 0, head = 0; const vel = new Float32Array(N_S), life = new Float32Array(N_S), wx = new Float32Array(N_S);
  function initSmoke() {
    const g = new THREE.BufferGeometry(); pos = new Float32Array(N_S * 3); aA = new Float32Array(N_S); aS = new Float32Array(N_S); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('aA', new THREE.BufferAttribute(aA, 1)); g.setAttribute('aS', new THREE.BufferAttribute(aS, 1));
    const m = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { k: { value: 300 }, col: { value: new THREE.Color(.52, .51, .5) } }, vertexShader: 'attribute float aA,aS;varying float a;uniform float k;void main(){a=aA;vec4 mv=modelViewMatrix*vec4(position,1.);gl_PointSize=aS*k/-mv.z;gl_Position=projectionMatrix*mv;}', fragmentShader: 'varying float a;uniform vec3 col;void main(){vec2 p=gl_PointCoord-.5;float d=length(p);if(d>.5)discard;float s=1.-smoothstep(.05,.5,d);gl_FragColor=vec4(col*(.9+p.y*.28),s*a);}' });
    P = new THREE.Points(g, m); P.frustumCulled = false; W.scene.add(P);
  }
  function stepSmoke(dt) {
    if (!G.started || !G.S) return; if (!P) initSmoke(); tList -= dt; if (tList <= 0) { tList = 2; const c = W.cam, L = G.blds.filter(b => b.done && SMOKY[b.t]).map(b => [Math.hypot(b.x - c.tx, b.z - c.tz), b]).sort((p, q) => p[0] - q[0]).slice(0, MOBILE ? 8 : 22); list = []; for (const [, b] of L) { const g = W.geoFor(b.t, b.v); if (!g.boundingBox) g.computeBoundingBox(); const r = b.rot * Math.PI / 2, co = Math.cos(r), si = Math.sin(r), hk = W.heightK ? W.heightK(b) : 1; for (const o of SMOKY[b.t]) list.push([b.x + b.w / 2 + o[0] * co + o[1] * si, W.h(b.x + b.w / 2, b.z + b.d / 2) + g.boundingBox.max.y * hk + .05, b.z + b.d / 2 - o[0] * si + o[1] * co]); } }
    const run = G.modal || G.prop || !G.speed ? .35 : 1; emit += dt * list.length * 1.25 * run; while (emit >= 1 && list.length) { emit -= 1; const s = list[Math.random() * list.length | 0], i = head; head = (head + 1) % N_S; pos[i * 3] = s[0] + (Math.random() - .5) * .08; pos[i * 3 + 1] = s[1]; pos[i * 3 + 2] = s[2] + (Math.random() - .5) * .08; life[i] = 1; vel[i] = .42 + Math.random() * .3; wx[i] = .1 + Math.random() * .12; }
    for (let i = 0; i < N_S; i++) { if (life[i] <= 0) { aA[i] = 0; continue; } life[i] -= dt / 5.4; const q = Math.max(0, life[i]); pos[i * 3 + 1] += vel[i] * dt * (.45 + q * .55); pos[i * 3] += wx[i] * dt * (1.3 - q); pos[i * 3 + 2] -= wx[i] * dt * .55 * (1.3 - q); aA[i] = Math.min(.7, (1 - q) * 3.8) * Math.sqrt(q) * .92; aS[i] = .42 + (1 - q) * 1.75; }
    P.geometry.attributes.position.needsUpdate = true; P.geometry.attributes.aA.needsUpdate = true; P.geometry.attributes.aS.needsUpdate = true; P.material.uniforms.k.value = W.renderer.domElement.height * 1.05;
  }
  const clouds0 = W.stepClouds; W.stepClouds = function (dt) { clouds0(dt); stepSmoke(dt); };
  /* ---------- trees along real streets ---------- */
  const MAX_T = MOBILE ? 180 : 420; let crown = null, trunk = null; const done = new Set(), C = [0x5f9a4d, 0x6fa653, 0x4f8c49, 0x83ad58].map(c => new THREE.Color(c));
  function initTrees() { const lam = new THREE.MeshLambertMaterial({ flatShading: true }); crown = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(.2, 0), lam, MAX_T); trunk = new THREE.InstancedMesh(new THREE.CylinderGeometry(.024, .034, .3, 5), new THREE.MeshLambertMaterial({ color: 0x70533a }), MAX_T); crown.count = trunk.count = 0; crown.castShadow = trunk.castShadow = true; crown.frustumCulled = trunk.frustumCulled = false; W.scene.add(crown, trunk); }
  function streetTree(x, z) {
    if ((x * 5 + z * 3) % 5 !== 0 || done.size >= MAX_T) return; const c = ci(x, z); if (done.has(c) || W.T[c] === 1 || W.T[c] === 0) return; let dx = 0, dz = 0; for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (inMap(x + a, z + b) && W.road[ci(x + a, z + b)] >= 2) { dx = Math.abs(a); dz = Math.abs(b); break; } if (!dx && !dz) return;
    const side = (x + z) % 2 ? 1 : -1, sx = x + (dz ? side : 0), sz = z + (dx ? side : 0); if (!inMap(sx, sz) || W.road[ci(sx, sz)] >= 2) return; if (!crown) initTrees(); const ox = x + .5 + dz * side * .44, oz = z + .5 + dx * side * .44, y = W.h(ox, oz), o = W._o, i = done.size, k = .82 + ((x * 13 + z * 7) % 5) * .09; done.add(c);
    o.position.set(ox, y + .15 * k, oz); o.rotation.set(0, 0, 0); o.scale.set(k, k, k); o.updateMatrix(); trunk.setMatrixAt(i, o.matrix); o.position.set(ox, y + .42 * k, oz); o.rotation.set(x, z, 0); o.scale.set(k, k * 1.08, k); o.updateMatrix(); crown.setMatrixAt(i, o.matrix); crown.setColorAt(i, C[(x + z * 3) % 4]); crown.count = trunk.count = done.size; crown.instanceMatrix.needsUpdate = trunk.instanceMatrix.needsUpdate = true; if (crown.instanceColor) crown.instanceColor.needsUpdate = true; W.needShadow = true;
  }
  const paint1 = W.paintRoad; W.paintRoad = function (x, z) { paint1(x, z); if (W.road[ci(x, z)] >= 2) streetTree(x, z); };
})();
