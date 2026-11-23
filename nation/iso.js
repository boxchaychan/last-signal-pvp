'use strict';
/* ก่อร่างสร้างชาติ: the painted 2D look (?look=2d). Same game and map, drawn as hand-painted sprites from a fixed isometric camera. */
const ISO_ON = new URLSearchParams(location.search).get('look') === '2d';
if (ISO_ON) (function () {
  const S2 = Math.SQRT2, AW = 2048, AH = 2048, CAP = MOBILE ? 4200 : 8000;
  const MAP = { hut: 0, house: 1, row: 2, shop: 2, market: 3, apt: 4, tower: 5, office: 6, cbd: 7, mega: 7, school: 8, hischool: 8, univ: 8, clinic: 9, hospital: 9, medcenter: 9, farm: 10, bigfarm: 10, park: 11 };
  const FIT = { hut: 1.15, house: 1.2, shop: 1.05, market: 1.08, apt: 1.25, tower: 1.3, office: 1.3, cbd: 1.4, mega: 1.5, school: 1.12, hischool: 1.3, univ: 1.45, clinic: 1, hospital: 1.2, medcenter: 1.5, farm: 1.04, bigfarm: 1.1, park: 1.15, row: 1.08 };
  let art = null, ctx, tex, mesh, geo, iA, iS, iU, iX, stat = [], statKey = '', baked = {}, bakeX = 0, bakeY = 1040, people = [], carU = [], treeU = null, shadowU = null;
  W.atlasP = Promise.all([W.atlasP, new Promise(res => { const im = new Image(); im.onload = () => { art = im; res(); }; im.onerror = () => res(); im.src = 'art/nation/iso.webp?b=' + BUILD; setTimeout(res, 9000); })]);
  const uvOf = (x0, y0, x1, y1) => [x0 / AW, 1 - y1 / AH, x1 / AW, 1 - y0 / AH];

  function buildAtlas() {
    const c = document.createElement('canvas'); c.width = AW; c.height = AH; ctx = c.getContext('2d', { willReadFrequently: true }); if (art) ctx.drawImage(art, 0, 0);
    /* soft ground shadow */
    let g = ctx.createRadialGradient(1984, 1984, 2, 1984, 1984, 60); g.addColorStop(0, 'rgba(24,30,40,.55)'); g.addColorStop(.7, 'rgba(24,30,40,.22)'); g.addColorStop(1, 'rgba(24,30,40,0)'); ctx.fillStyle = g; ctx.fillRect(1920, 1920, 128, 128); shadowU = uvOf(1921, 1921, 2047, 2047);
    /* tiny people and cars, painted in code to sit in the same world */
    const shirts = ['#d9534f', '#3f8fd8', '#f0b93a', '#3fae6e', '#8e6bbf', '#e07b39', '#f4efe2', '#2f9fa8', '#f28c1e'];
    shirts.forEach((s, i) => { const x = 8 + i * 22, y = 1960; ctx.fillStyle = 'rgba(20,24,34,.32)'; ctx.beginPath(); ctx.ellipse(x + 7, y + 38, 7, 3, 0, 0, 7); ctx.fill(); ctx.fillStyle = '#3d3a44'; ctx.fillRect(x + 3, y + 25, 3.4, 12); ctx.fillRect(x + 8, y + 25, 3.4, 12); ctx.fillStyle = s; ctx.beginPath(); ctx.roundRect(x + 1.5, y + 11, 11, 16, 4); ctx.fill(); ctx.fillStyle = '#e8b98e'; ctx.beginPath(); ctx.arc(x + 7, y + 6.5, 5.4, 0, 7); ctx.fill(); ctx.fillStyle = i % 3 ? '#2b2420' : '#5b3a28'; ctx.beginPath(); ctx.arc(x + 7, y + 5, 5.5, 3.14, 6.28); ctx.fill(); people.push(uvOf(x - 1, y, x + 15, y + 42)); });
    ['#e9e9e6', '#c8423a', '#3a78c9', '#e6b23a', '#3f9a78', '#2f3238'].forEach((s, i) => { const x = 240 + i * 62, y = 1964; ctx.fillStyle = 'rgba(20,24,34,.34)'; ctx.beginPath(); ctx.ellipse(x + 26, y + 29, 26, 7, 0, 0, 7); ctx.fill(); ctx.fillStyle = s; ctx.beginPath(); ctx.roundRect(x + 2, y + 13, 48, 15, 6); ctx.fill(); ctx.beginPath(); ctx.roundRect(x + 12, y + 3, 26, 14, 6); ctx.fill(); ctx.fillStyle = '#2c4252'; ctx.fillRect(x + 15, y + 6, 9, 8); ctx.fillRect(x + 26, y + 6, 9, 8); ctx.fillStyle = '#17191d'; ctx.beginPath(); ctx.arc(x + 13, y + 28, 5, 0, 7); ctx.arc(x + 39, y + 28, 5, 0, 7); ctx.fill(); carU.push(uvOf(x, y, x + 52, y + 37)); });
    tex = new THREE.CanvasTexture(c); tex.anisotropy = MOBILE ? 2 : 4; tex.minFilter = THREE.LinearMipmapLinearFilter;
    if (art) { const q = ISO_ART.cells[11], sw = q[2] - q[0], sh = Math.round((q[3] - q[1]) * .74), dx = 1560, dy = 20; ctx.drawImage(art, q[0], q[1], sw, sh, dx, dy, sw, sh); ctx.globalCompositeOperation = 'destination-out'; const fd = ctx.createLinearGradient(0, dy + sh * .78, 0, dy + sh); fd.addColorStop(0, 'rgba(0,0,0,0)'); fd.addColorStop(1, 'rgba(0,0,0,1)'); ctx.fillStyle = fd; ctx.fillRect(dx, dy + sh * .78, sw, sh * .22 + 1); ctx.globalCompositeOperation = 'source-over'; treeU = uvOf(dx, dy, dx + sw, dy + sh); tex.needsUpdate = true; }
  }
  /* buildings with no painting yet: photograph the 3D model from the same angle */
  function bake(t, v) {
    const key = t + (t === 'hall' ? v : 0); if (baked[key]) return baked[key]; const SZ = 168; if (bakeX + SZ > AW) { bakeX = 0; bakeY += SZ; } if (bakeY + SZ > 1910) return null; const s = (BT[t] || { s: [3, 3] }).s;
    const m = new THREE.Mesh(W.geoFor(t, t === 'hall' ? v : 0), W.bmat), sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xfff4e0, 0x8a8468, .75)); const d = new THREE.DirectionalLight(0xfff0d0, .8); d.position.set(-3, 6, 4); sc.add(d, m);
    const box = new THREE.Box3().setFromObject(m), W0 = (s[0] + s[1]) / S2, half = Math.max(W0 * .62, (box.max.y * .9 + W0 * .3) * .62), cm = new THREE.OrthographicCamera(-half, half, half * 1.75 - W0 * .32, -half * .25 - W0 * .32, -80, 80); cm.position.set(10, 10 * Math.tan(Math.PI / 6) * S2, 10); cm.lookAt(0, 0, 0); cm.updateProjectionMatrix();
    const rt = new THREE.WebGLRenderTarget(SZ, SZ, { samples: 0 }), r = W.renderer, night = W.nightU.value, oldC = new THREE.Color(); r.getClearColor(oldC); const oldA = r.getClearAlpha(), bg = sc.background; W.nightU.value = 0; r.setRenderTarget(rt); r.setClearColor(0, 0); r.clear(); r.render(sc, cm); const px = new Uint8Array(SZ * SZ * 4); r.readRenderTargetPixels(rt, 0, 0, SZ, SZ, px); r.setRenderTarget(null); r.setClearColor(oldC, oldA); W.nightU.value = night; rt.dispose(); sc.background = bg;
    const im = ctx.createImageData(SZ, SZ); for (let y = 0; y < SZ; y++) im.data.set(px.subarray((SZ - 1 - y) * SZ * 4, (SZ - y) * SZ * 4), y * SZ * 4); ctx.putImageData(im, bakeX, bakeY); tex.needsUpdate = true;
    const o = { u: uvOf(bakeX + .5, bakeY + .5, bakeX + SZ - .5, bakeY + SZ - .5), sx: half * 2, sy: half * 2, ox: -half, oy: -half * .25 - W0 * .32 }; bakeX += SZ; baked[key] = o; return o;
  }
  function spriteOf(b) {
    const i = MAP[b.t]; if (art && i != null) { const q = ISO_ART.cells[i], W0 = (b.w + b.d) / S2, k = (FIT[b.t] || 1.05) * (b.vis && b.sc ? Math.max(.8, b.sc * 1.2) : 1), sx = W0 * k, sy = sx * (q[3] - q[1]) / (q[2] - q[0]); return { u: uvOf(q[0], q[1], q[2], q[3]), sx, sy, ox: -sx * q[4], oy: -W0 * k / 4 }; } return bake(b.t, b.v);
  }

  function setup() {
    buildAtlas(); W.fixPitch = Math.PI / 6; W.cam.yaw = Math.PI / 4; const old = W.camera; W.camera = new THREE.OrthographicCamera(-10, 10, 10, -10, -500, 900); W.camera.position.copy(old.position);
    const pl = new THREE.PlaneGeometry(1, 1); pl.translate(.5, .5, 0); geo = new THREE.InstancedBufferGeometry(); geo.index = pl.index; geo.setAttribute('position', pl.attributes.position); geo.instanceCount = 0;
    const at = (n, k) => { const q = new THREE.InstancedBufferAttribute(new Float32Array(CAP * k), k); q.setUsage(THREE.DynamicDrawUsage); geo.setAttribute(n, q); return q; }; iA = at('iA', 3); iS = at('iS', 4); iU = at('iU', 4); iX = at('iX', 3);
    const mat = W.isoMat = new THREE.ShaderMaterial({ uniforms: { tex: { value: tex }, night: { value: 0 }, L: { value: 1 } }, transparent: true, depthTest: false, depthWrite: false, vertexShader: 'attribute vec3 iA;attribute vec4 iS,iU;attribute vec3 iX;varying vec2 vU,vQ;varying float vP,vG;void main(){vG=iX.z;vec4 c=viewMatrix*vec4(iA,1.);vec2 q=position.xy;c.xy+=iS.xy+q*iS.zw;gl_Position=projectionMatrix*c;vU=vec2(mix(iU.x,iU.z,iX.y>.5?1.-q.x:q.x),mix(iU.y,iU.w,q.y));vP=iX.x;vQ=q;}', fragmentShader: 'uniform sampler2D tex;uniform float night,L;varying vec2 vU,vQ;varying float vP,vG;void main(){vec4 t=texture2D(tex,vU);if(t.a<.03||vQ.y>vP)discard;vec3 c=t.rgb;float w=vG*smoothstep(.3,.52,c.r-c.b)*smoothstep(.78,.96,c.r);vec3 n=c*vec3(.3,.36,.56)+w*vec3(.92,.68,.34);c=mix(c*(.92+.08*L),n,night);if(vP<.999)c=mix(c,vec3(.95,.82,.55),.12);gl_FragColor=vec4(c,t.a);}' });
    mesh = new THREE.Mesh(geo, mat); mesh.frustumCulled = false; mesh.renderOrder = 3; W.scene.add(mesh); W.ring.renderOrder = 6;
    for (const q of [...W.treeMeshes, W.pBody, W.pHead, W.pLoad, W.carMesh, W.lampMesh, W.lampGlow, W.clouds]) if (q) q.visible = false; W.scene.fog.density = 0; W.renderer.shadowMap.enabled = false; W.waterU.sK.value = .2;
  }
  const init2 = W.init; W.init = function (cv, seed) { init2(cv, seed); setup(); };

  function staticList() {
    const L = [], z = new THREE.Vector3(), m = new THREE.Matrix4();
    if (treeU) W.treeAt.forEach((l, c) => { for (const e of l) { const sp = Math.floor(e / 100000), i = e % 100000; if (i % 3) continue; W.treeMeshes[sp].getMatrixAt(i, m); z.setFromMatrixPosition(m); const r = (i * 7919) % 100 / 100, s = 2 + r * .95; L.push({ k: z.x + z.z, x: z.x, y: Math.max(z.y, .05), z: z.z, u: treeU, ox: -s * .5, oy: -s * .05, sx: s, sy: s * (treeU[3] - treeU[1]) / (treeU[2] - treeU[0]) * (AW / AH), fl: i % 2, p: 1 }); } });
    for (const b of G.blds) { if (!b.done) continue; const sp = spriteOf(b); if (!sp) continue; const cx = b.x + b.w / 2, cz = b.z + b.d / 2, hk = TALL_K(b); L.push({ k: cx + cz, x: cx, y: Math.max(.04, W.h(cx, cz)), z: cz, u: sp.u, ox: sp.ox, oy: sp.oy, sx: sp.sx, sy: sp.sy * hk, p: 1, b, g: GLOW(b) }); }
    return L.sort((p, q) => p.k - q.k);
  }
  const GLOW = b => (b.t === 'farm' || b.t === 'bigfarm' || b.t === 'park' ? 0 : 1);
  const TALL_K = b => (W.heightK && MAP[b.t] != null && ['tower', 'mega', 'cbd', 'office', 'apt'].includes(b.t)) ? clamp(W.heightK(b), .78, 1.18) : 1;
  const push = (i, q) => { iA.array.set([q.x, q.y, q.z], i * 3); iS.array.set([q.ox, q.oy, q.sx, q.sy], i * 4); iU.array.set(q.u, i * 4); iX.array[i * 3] = q.p; iX.array[i * 3 + 1] = q.fl ? 1 : 0; iX.array[i * 3 + 2] = q.g || 0; };
  let visible = [];
  function sync() {
    const key = G.blds.length + ':' + G.blds.filter(b => b.done).length + ':' + W.treeLive + ':' + G.blds.reduce((q, b) => q + (b.done ? b.t.length * b.id : 0), 0); if (key !== statKey) { statKey = key; stat = staticList(); }
    const dyn = [], cam = W.cam, hh = cam.dist * .56 + 10, hw = hh * (innerWidth / innerHeight) + 10, inView = (x, z) => Math.abs((x - cam.x) - (z - cam.z)) / S2 < hw + 6 && Math.abs((x + z) - (cam.x + cam.z)) / S2 * .5 < hh + 12;
    for (const b of G.blds) { if (b.done) continue; const sp = spriteOf(b), cx = b.x + b.w / 2, cz = b.z + b.d / 2; if (!sp) continue; dyn.push({ k: cx + cz, x: cx, y: b.t === 'reclaim' ? .03 : Math.max(.04, W.h(cx, cz)), z: cz, u: sp.u, ox: sp.ox, oy: sp.oy, sx: sp.sx, sy: sp.sy * TALL_K(b), p: Math.max(.04, b.prog), b, g: GLOW(b) }); }
    if (cam.dist < 72) {
      W.agents.forEach((a, i) => { if (a.indoor || !inView(a.x, a.z)) return; const bob = a.moving ? Math.abs(Math.sin(G.time * 9 + i)) * .03 : 0, s = a.kid ? .34 : .46; dyn.push({ k: a.x + a.z, x: a.x, y: Math.max(W.h(a.x, a.z), .12) + bob, z: a.z, u: people[a.crew ? 8 : a.id % 8], ox: -s * .19, oy: -s * .08, sx: s * .38, sy: s, p: 1, fl: Math.sin(a.dir || 0) < 0 }); });
      (W.cars || []).forEach((q, i) => { const c = q.c, nx = q.n, x = c % N + .5 + ((nx % N) - (c % N)) * q.f, z = (c / N | 0) + .5 + ((nx / N | 0) - (c / N | 0)) * q.f; if (!inView(x, z)) return; dyn.push({ k: x + z, x, y: Math.max(W.h(x, z), .16), z, u: carU[i % carU.length], ox: -.34, oy: -.09, sx: .68, sy: .48, p: 1, fl: (nx % N) - (c % N) + (c / N | 0) - (nx / N | 0) > 0 }); });
    }
    dyn.sort((p, q) => p.k - q.k); let n = 0, d = 0; visible = [];
    /* ground shadows first */
    for (const q of stat) { if (!q.b || n > CAP * .15 || !inView(q.x, q.z)) continue; const W0 = (q.b.w + q.b.d) / S2; push(n++, { x: q.x, y: q.y, z: q.z, u: shadowU, ox: -W0 * .62 + .16, oy: -W0 * .36 - .06, sx: W0 * 1.24, sy: W0 * .72, p: 1 }); }
    for (let s = 0; s <= stat.length && n < CAP; s++) { const st = stat[s]; while (d < dyn.length && (!st || dyn[d].k <= st.k) && n < CAP) { push(n++, dyn[d]); if (dyn[d].b) visible.push(dyn[d]); d++; } if (st && inView(st.x, st.z)) { push(n++, st); if (st.b) visible.push(st); } }
    geo.instanceCount = n; for (const q of [iA, iS, iU, iX]) q.needsUpdate = true;
  }

  const render1 = W.render;
  W.render = function (t, dt) {
    if (!mesh) { render1(t, dt); return; } W.cam.yaw = Math.PI / 4; const hh = W.cam.dist * .56, asp = innerWidth / innerHeight, cm = W.camera; cm.left = -hh * asp; cm.right = hh * asp; cm.top = hh; cm.bottom = -hh; cm.updateProjectionMatrix();
    for (const k in W.arch) W.arch[k].im.visible = false; W.sites.forEach(q => { q.gr.visible = false; }); if (G.started) { W.isoMat.uniforms.night.value = W.nightU.value; W.isoMat.uniforms.L.value = W.waterU.L.value; sync(); } render1(t, dt);
  };
  W.project = function (x, y, z) { const v = new THREE.Vector3(x, y, z).project(W.camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight, Math.min(.5, v.z)]; };
  W.groundAt = function (sx, sy) {
    const cm = W.camera; cm.updateMatrixWorld(); const ex = new THREE.Vector3().setFromMatrixColumn(cm.matrixWorld, 0), ey = new THREE.Vector3().setFromMatrixColumn(cm.matrixWorld, 1), nx = sx / innerWidth * 2 - 1, ny = 1 - sy / innerHeight * 2;
    /* a tap on a tall building counts as that building, front-most first */
    const c0 = new THREE.Vector3(); for (let i = visible.length - 1; i >= 0; i--) { const q = visible[i]; c0.set(q.x, q.y, q.z).project(cm); const px = (nx - c0.x) * (cm.right - cm.left) / 2, py = (ny - c0.y) * (cm.top - cm.bottom) / 2; if (px > q.ox + q.sx * .12 && px < q.ox + q.sx * .88 && py > q.oy && py < q.oy + q.sy * .94) return [q.b.x + .5, q.b.z + .5]; }
    const o = cm.position.clone().add(ex.multiplyScalar(nx * (cm.right - cm.left) / 2)).add(ey.multiplyScalar(ny * (cm.top - cm.bottom) / 2)), d = new THREE.Vector3(); cm.getWorldDirection(d); const tt = (.25 - o.y) / d.y, x = o.x + d.x * tt, z = o.z + d.z * tt; return x >= 0 && z >= 0 && x < N && z < N ? [x, z] : null;
  };
})();
