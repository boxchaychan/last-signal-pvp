// The ★ / ★★ / ★★★ units of tribe3d.html side by side, big and pretty (front 3/4 and back), straight from the game's templates.
//   python3 -m http.server 8000 ; node tools/art/tiers_lookbook.js out.png
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const url = await pg.evaluate(async () => {
    const P = GAME.PEOPLE, R = TB.renderer, W = 2000, H = 1500, rowsK = ['warrior', 'hunter', 'shaman'], names = { warrior: ['นักรบ', 'นักรบ', 'นักรบ'], hunter: ['พรานหน้าไม้', 'นักธนู', 'นักธนู'], shaman: ['หมอผี', 'หมอผี', 'หมอผี'] };
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x6a5a48, .72)); const k = new THREE.DirectionalLight(0xfff0d8, 1); k.position.set(-4, 8, 10); sc.add(k); const rim = new THREE.DirectionalLight(0xbfe0ff, .7); rim.position.set(6, 5, -8); sc.add(rim);
    const pose = { warrior: 'Idle', hunter: 'Idle', shaman: 'Idle' };
    rowsK.forEach((kind, r) => { for (let t = 1; t <= 3; t++) for (const back of [0, 1]) {
      const key = t === 1 ? kind : kind + t, T = P.tpl[key]; if (!T) continue; const o = THREE.SkeletonUtils.clone(T.root); o.scale.setScalar(2.4 / T.h * (t === 3 ? 1.12 : t === 2 ? 1.06 : 1));
      o.traverse(m => { if (m.isSkinnedMesh) { m.material = m.material.clone(); if (m.material.map) { m.material.map = m.material.map.clone(); m.material.map.magFilter = THREE.LinearFilter; m.material.map.needsUpdate = true; } } });
      const c = P.clips.find(c => c.name === (t > 1 && kind === 'hunter' ? 'Ranged_Bow_Idle' : pose[kind])); const mx = new THREE.AnimationMixer(o); mx.clipAction(c).play(); mx.update(.5);
      o.position.set((t - 1) * 6.6 + back * 2.9, 0, r * -4.6 + r * 0); o.position.y = (2 - r) * 3.9; o.rotation.y = back ? Math.PI + .4 : -.4; sc.add(o); } });
    const vw = 19.5, vh = vw * H / W, cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 200); cam.position.set(8.0, 5.3 + 4, 30); cam.lookAt(8.0, 5.3, 0);
    const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4 }); R.setRenderTarget(rt); R.setClearColor(0x2a3646, 1); R.clear(); R.render(sc, cam); const px = new Uint8Array(W * H * 4); R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H + 80; const g = cv.getContext('2d'), id = g.createImageData(W, H); for (let y = 0; y < H; y++) id.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4);
    g.fillStyle = '#1c150c'; g.fillRect(0, 0, W, H + 80); g.putImageData(id, 0, 80); await document.fonts.load('800 20px Kanit'); g.textAlign = 'center';
    ['★', '★★', '★★★'].forEach((s, t) => { const v = new THREE.Vector3(t * 6.6 + 1.45, 0, 0).project(cam), x = (v.x + 1) / 2 * W; g.font = '800 56px Kanit'; g.fillStyle = ['#ffffff', '#ffd24a', '#e8a8ff'][t]; g.fillText(s, x, 62); });
    rowsK.forEach((kind, r) => { names[kind].forEach((n, t) => { const v = new THREE.Vector3(t * 6.6 + 1.45, (2 - r) * 3.9 + .05, 0).project(cam), x = (v.x + 1) / 2 * W, y = (1 - v.y) / 2 * H + 80; g.font = '800 30px Kanit'; g.fillStyle = ['#ffffff', '#ffd24a', '#e8a8ff'][t]; g.lineWidth = 6; g.strokeStyle = '#140c06'; g.strokeText(n, x, y + 30); g.fillText(n, x, y + 30); }); });
    return cv.toDataURL();
  });
  fs.writeFileSync(process.argv[2], Buffer.from(url.split(',')[1], 'base64')); await b.close(); })();
