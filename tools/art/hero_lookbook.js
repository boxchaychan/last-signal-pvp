// The owner's design picture next to the 3D hero of tribe3d.html (front 3/4, side, back, a sword swing), straight from the game's template.
//   python3 -m http.server 8000 ; node tools/art/hero_lookbook.js out.png
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const url = await pg.evaluate(async () => {
    const P = GAME.PEOPLE, R = TB.renderer, W = 2400, H = 1100, T = P.tpl.hero; if (!T) return null;
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x6a5a48, .72)); const k = new THREE.DirectionalLight(0xfff0d8, 1); k.position.set(-4, 8, 10); sc.add(k); const rim = new THREE.DirectionalLight(0xbfe0ff, .7); rim.position.set(6, 5, -8); sc.add(rim);
    const views = [[-.45, 'Idle', .3], [Math.PI / 2, 'Idle', .3], [Math.PI + .35, 'Idle', .3], [-.6, '1H_Melee_Attack_Slice_Diagonal', .42]];
    views.forEach(([ry, clip, f], i) => { const o = THREE.SkeletonUtils.clone(T.root); o.scale.setScalar(3 / T.h);
      o.traverse(m => { if (m.isSkinnedMesh) { m.material = m.material.clone(); if (m.material.map) { m.material.map = m.material.map.clone(); m.material.map.magFilter = THREE.LinearFilter; m.material.map.needsUpdate = true; } } });
      const c = P.clips.find(c => c.name === clip); const mx = new THREE.AnimationMixer(o); mx.clipAction(c).play(); mx.update(c.duration * f);
      o.position.set(i * 3.6, 0, 0); o.rotation.y = ry; sc.add(o); });
    const vw = 14.6, vh = vw * H / W, cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 200); cam.position.set(5.4, 2.0 + 2.5, 30); cam.lookAt(5.4, 2.0, 0);
    const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4 }); R.setRenderTarget(rt); R.setClearColor(0x2c4a7a, 1); R.clear(); R.render(sc, cam); const px = new Uint8Array(W * H * 4); R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null);
    const ref = new Image(); ref.src = 'art/incoming/tribe3d/hero_ref.png'; await ref.decode();
    const RW = Math.round(H * .9 * ref.width / ref.height), cv = document.createElement('canvas'); cv.width = W + RW; cv.height = H + 70; const g = cv.getContext('2d'), id = g.createImageData(W, H);
    for (let y = 0; y < H; y++) id.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4);
    g.fillStyle = '#1c150c'; g.fillRect(0, 0, cv.width, cv.height); g.drawImage(ref, 0, 70 + H * .05, RW, H * .9); g.putImageData(id, RW, 70);
    await document.fonts.load('800 20px Kanit'); g.font = '800 44px Kanit'; g.textAlign = 'center'; g.fillStyle = '#ffd24a';
    g.fillText('แบบที่ส่งมา', RW / 2, 52); g.fillText('3D ในเกม (หน้า / ข้าง / หลัง / ฟัน)', RW + W / 2, 52);
    return cv.toDataURL();
  });
  if (!url) { console.log('no hero template'); process.exit(1); }
  fs.writeFileSync(process.argv[2], Buffer.from(url.split(',')[1], 'base64')); await b.close(); })();
