// One unit template of tribe3d.html playing several moves side by side (checks a rig: arms, bow, braids, cape).
//   python3 -m http.server 8000 ; node tools/art/unit_lookbook.js out.png [template] [move:frac,...] [yaw]
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message)); pg.on('console', m => { if (/warn|error/.test(m.type())) console.log(m.text()); });
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const key = process.argv[3] || 'hunter3', moves = (process.argv[4] || 'Idle:.3,Walking_A:.25,Ranged_Bow_Draw:.8,Ranged_Bow_Release:.2,Cheer:.4,Hit_A:.3').split(',').map(s => s.split(':')), yaw = +(process.argv[5] || -.5);
  const url = await pg.evaluate(async ([key, moves, yaw]) => {
    const P = GAME.PEOPLE, R = TB.renderer, T = P.tpl[key]; if (!T) return null; const CL = T.clips || P.clips, W = 360 * moves.length, H = 620;
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x6a5a48, .8)); const k = new THREE.DirectionalLight(0xfff0d8, 1); k.position.set(-4, 8, 10); sc.add(k); const rim = new THREE.DirectionalLight(0xbfe0ff, .6); rim.position.set(6, 5, -8); sc.add(rim);
    moves.forEach(([clip, f], i) => { const o = THREE.SkeletonUtils.clone(T.root); o.scale.setScalar(2.6 / T.h);
      const c = CL.find(c => c.name === clip); if (c) { const mx = new THREE.AnimationMixer(o); mx.clipAction(c).play(); mx.update(c.duration * +f); }
      o.position.set(i * 3.2, 0, 0); o.rotation.y = yaw; sc.add(o); });
    const vw = 3.2 * moves.length, vh = vw * H / W, cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 200); cam.position.set(3.2 * (moves.length - 1) / 2, 1.6 + 2.5, 30); cam.lookAt(3.2 * (moves.length - 1) / 2, 1.6, 0);
    const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4 }); R.setRenderTarget(rt); R.setClearColor(0x2c4a7a, 1); R.clear(); R.render(sc, cam); const px = new Uint8Array(W * H * 4); R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H + 50; const g = cv.getContext('2d'), id = g.createImageData(W, H);
    for (let y = 0; y < H; y++) id.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4);
    g.fillStyle = '#1c150c'; g.fillRect(0, 0, W, H + 50); g.putImageData(id, 0, 50); g.font = '700 26px sans-serif'; g.fillStyle = '#ffd24a'; g.textAlign = 'center';
    moves.forEach(([clip], i) => g.fillText(clip, 180 + i * 360, 34)); return cv.toDataURL();
  }, [key, moves, yaw]);
  if (!url) { console.log('no template ' + key); process.exit(1); }
  fs.writeFileSync(process.argv[2], Buffer.from(url.split(',')[1], 'base64')); await b.close(); })();
