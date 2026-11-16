// Lookbook of the 2-star archer ("นักธนู ★★", owner 2026-11-16 "ลองเบลนเดอร์ใหม่ซักตัว เอาสวยๆ ลองทำนักธนู คิดซะว่า 2 ดาว"):
// the hooded Rogue (KayKit, teal tex_rogue_4) + Blender gear (art/tribe3d/gear/archer_gear.glb from tools/blender/archer_gear.py:
// bow in handslot.l, quiver on the hips, plume on the head, pad on upperarm.l) + bow moves from the KayKit Character Animations
// pack (art/incoming/kaykit/character_animations/Rig_Medium, same bone names as our characters). Not in the game yet.
//   python3 -m http.server 8000 ; node tools/art/archer_lookbook.js out.png [big] [pretty]   (pretty = smooth textures, soft shadows, rim light, anti-aliased)
const {chromium} = require('playwright'); const fs = require('fs');
const CFG = { local: { Bow: 1 }, bow: { p: [0, 0, 0], r: [0, 0, 0] }, quiver: { b: 'hips', p: [-0.36, 0.62, -0.1], r: [-0.35, 0, 0.32] }, plume: { p: [0.32, 1.98, -0.02], r: [0, 0, -0.55] }, pad: { b: 'upperarml', p: [0.3, 1.17, 0], r: [0, 0, -0.7] } };
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const res = await pg.evaluate(async (cfg) => {
    const ld = new THREE.GLTFLoader(), tl = new THREE.TextureLoader(), R = TB.renderer, A = 'art/incoming/kaykit/character_animations/Rig_Medium/';
    const [RH, GE, CR, MA] = await Promise.all(['art/tribe3d/people/Rogue_Hooded.glb', 'art/tribe3d/gear/archer_gear.glb', A + 'Rig_Medium_CombatRanged.glb', A + 'Rig_Medium_MovementAdvanced.glb'].map(u => ld.loadAsync(u)));
    const tex = n => tl.loadAsync(`art/tribe3d/people/tex_${n}.png`).then(t => { t.flipY = false; t.encoding = THREE.LinearEncoding; if (cfg.pretty) { t.magFilter = THREE.LinearFilter; t.minFilter = THREE.LinearMipmapLinearFilter; } return t; });
    const T3 = await tex('rogue_3'), T4 = await tex('rogue_4');
    const clips = [...CR.animations, ...MA.animations, ...GAME.PEOPLE.clips];
    const find = (root, n) => { let f = null; root.traverse(o => { if (o.name === n && !f) f = o; }); return f; };
    const gear = {}; GE.scene.traverse(o => { if (o.isMesh) { const mm = (Array.isArray(o.material) ? o.material : [o.material]).map(m => new THREE.MeshLambertMaterial({ color: m.color.clone().convertLinearToSRGB(), side: THREE.DoubleSide })); o.material = mm.length === 1 ? mm[0] : mm; } }); for (const c of GE.scene.children) { gear[c.name] = c; if (c.name !== 'Bow') c.traverse(o => { if (o.isMesh) o.geometry.rotateX(Math.PI / 2); }); }   // modelled with Blender +Y up; glTF turned that into -Z
    function body(tx, keep) { const r = THREE.SkeletonUtils.clone(RH.scene), drop = []; const m = new THREE.MeshLambertMaterial({ map: tx }); r.traverse(o => { if (o.isMesh) { if (o.isSkinnedMesh || keep.includes(o.name)) o.material = m; else drop.push(o); } }); drop.forEach(o => o.parent.remove(o)); r.updateMatrixWorld(true); return r; }
    function put(r, name, bone, pos, rot) { const g = gear[name].clone(); const bn = find(r, bone); if (cfg.local[name]) { g.position.set(...pos); g.rotation.set(...rot); bn.add(g); } else { r.updateMatrixWorld(true); g.position.set(...pos); g.rotation.set(...rot); r.add(g); g.updateMatrixWorld(true); bn.attach(g); } }
    function archer() { const r = body(T4, ['Rogue_Cape']);
      put(r, 'Bow', 'handslotl', cfg.bow.p, cfg.bow.r); put(r, 'Quiver', cfg.quiver.b || 'chest', cfg.quiver.p, cfg.quiver.r); put(r, 'Plume', 'head', cfg.plume.p, cfg.plume.r); put(r, 'Pad', cfg.pad.b || 'chest', cfg.pad.p, cfg.pad.r); return r; }
    const LIST = cfg.big ? [
      ['นักธนู ★★', 'ยืนพร้อม', archer, 'Ranged_Bow_Idle', -.5, .5],
      ['นักธนู ★★', 'ง้างธนู', archer, 'Ranged_Bow_Draw', -1.1, .95],
      ['นักธนู ★★', 'ด้านหลัง (กระบอกลูกธนู)', archer, 'Ranged_Bow_Idle', 2.5, .5],
    ] : [
      ['พรานหน้าไม้ ★', 'ตัวปัจจุบัน', () => body(T3, ['Rogue_Cape', '1H_Crossbow']), 'Idle', -.45, .4],
      ['นักธนู ★★', 'ยืนพร้อม', archer, 'Ranged_Bow_Idle', -.45, .5],
      ['นักธนู ★★', 'ง้างธนู (ด้านข้าง)', archer, 'Ranged_Bow_Draw', -1.4, .9],
      ['นักธนู ★★', 'ด้านหลัง', archer, 'Ranged_Bow_Idle', 2.7, .5],
      ['นักธนู ★★', 'วิ่ง', archer, 'Running_HoldingBow', -.6, .3],
    ];
    await document.fonts.load('800 20px Kanit');
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x6a5a48, cfg.pretty ? .62 : .75)); const dl = new THREE.DirectionalLight(0xfff0d8, cfg.pretty ? 1 : .9); dl.position.set(-6, 14, 12); sc.add(dl);
    if (cfg.pretty) { dl.castShadow = true; dl.shadow.mapSize.set(4096, 4096); Object.assign(dl.shadow.camera, { left: -14, right: 14, top: 8, bottom: -8, near: 1, far: 60 }); dl.shadow.radius = 4; dl.shadow.bias = -.0004; dl.target.position.set(3.6, 0, 0); sc.add(dl.target);
      const rim = new THREE.DirectionalLight(0xbfe0ff, .55); rim.position.set(8, 6, -14); sc.add(rim); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap; R.shadowMap.autoUpdate = true; }
    const gnd = new THREE.Mesh(new THREE.CircleGeometry(80, 40).rotateX(-Math.PI / 2), new THREE.MeshLambertMaterial({ color: cfg.pretty ? 0x7a9a5a : 0x6a8a4a })); gnd.receiveShadow = true; sc.add(gnd);
    const xs = [], miss = [];
    LIST.forEach(([, , mk, clip, ry, t], i) => { const r = mk(); r.position.x = i * 3.6; r.rotation.y = ry; if (cfg.pretty) r.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); xs.push(i * 3.6); const c = clips.find(c => c.name === clip); if (!c) miss.push(clip); else { const mx = new THREE.AnimationMixer(r); mx.clipAction(c).play(); mx.update(c.duration * t); } sc.add(r); });
    const W = 1800, H = cfg.big ? 1000 : 760, vw = 3.6 * LIST.length + (cfg.big ? -1.3 : .4), vh = vw * H / W, cx = 3.6 * (LIST.length - 1) / 2;
    const cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 400); cam.position.set(cx, 1.4 + 9, 30); cam.lookAt(cx, cfg.big ? 1.2 : 1.3, 0);
    const SS = cfg.pretty ? 2 : 1, rt = new THREE.WebGLRenderTarget(W * SS, H * SS, { samples: cfg.pretty ? 8 : 0 }); R.setRenderTarget(rt); R.setClearColor(0x2c2418, 1); R.clear(); R.render(sc, cam);
    const px = new Uint8Array(W * H * 4 * SS * SS); R.readRenderTargetPixels(rt, 0, 0, W * SS, H * SS, px); R.setRenderTarget(null); rt.dispose();
    const big = document.createElement('canvas'); big.width = W * SS; big.height = H * SS; const bg = big.getContext('2d'), id = bg.createImageData(W * SS, H * SS);
    for (let y = 0; y < H * SS; y++) id.data.set(px.subarray((H * SS - 1 - y) * W * SS * 4, (H * SS - y) * W * SS * 4), y * W * SS * 4); bg.putImageData(id, 0, 0);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H + 110; const g = cv.getContext('2d'); g.fillStyle = '#1c150c'; g.fillRect(0, 0, W, H + 110); g.imageSmoothingQuality = 'high'; g.drawImage(big, 0, 0, W, H); g.textAlign = 'center';
    LIST.forEach((u, i) => { const v = new THREE.Vector3(xs[i], 0, 0).project(cam), sx = (v.x + 1) / 2 * W; g.font = '800 34px Kanit'; g.fillStyle = i || cfg.big ? '#ffd27a' : '#c8c0b0'; g.fillText(u[0], sx, H + 44); g.font = '600 24px Kanit'; g.fillStyle = '#e8d8b8'; g.fillText(u[1], sx, H + 82); });
    return { url: cv.toDataURL('image/png'), miss };
  }, Object.assign({}, CFG, { big: process.argv.includes('big'), pretty: process.argv.includes('pretty') }));
  console.log('missing clips', res.miss.join(',') || 'none');
  fs.writeFileSync(process.argv[2], Buffer.from(res.url.split(',')[1], 'base64')); await b.close(); })();
