// The owner's design picture next to the 3D hero of tribe3d.html: the same 3/4 view big, then side / back / a sword swing, straight from the game's template.
//   python3 -m http.server 8000 ; node tools/art/hero_lookbook.js out.png [yaw]
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const url = await pg.evaluate(async (yaw) => {
    const P = GAME.PEOPLE, R = TB.renderer, T = P.tpl.hero; if (!T) return null;
    const shoot = (views, W, H, vw, cy) => {
      const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x6a5a48, .72)); const k = new THREE.DirectionalLight(0xfff0d8, 1); k.position.set(-4, 8, 10); sc.add(k); const rim = new THREE.DirectionalLight(0xbfe0ff, .7); rim.position.set(6, 5, -8); sc.add(rim);
      views.forEach(([ry, clip, f, x], i) => { const o = THREE.SkeletonUtils.clone(T.root); o.scale.setScalar(3 / T.h);
        const c = P.clips.find(c => c.name === clip); const mx = new THREE.AnimationMixer(o); mx.clipAction(c).play(); mx.update(c.duration * f);
        o.position.set(x, 0, 0); o.rotation.y = ry; sc.add(o); });
      const vh = vw * H / W, cx = views.reduce((a, v) => a + v[3], 0) / views.length, cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 200); cam.position.set(cx, cy + 3, 30); cam.lookAt(cx, cy, 0);
      const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4 }); R.setRenderTarget(rt); R.setClearColor(0x2c4a7a, 1); R.clear(); R.render(sc, cam); const px = new Uint8Array(W * H * 4); R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null); rt.dispose();
      const id = new ImageData(W, H); for (let y = 0; y < H; y++) id.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4); return id;
    };
    const H = 1000, big = shoot([[yaw, 'Idle', .3, 0]], 1000, H, 4.6, 1.75), row = shoot([[Math.PI / 2, 'Idle', .3, 0], [Math.PI + .35, 'Idle', .3, 3.4], [-.5, '1H_Melee_Attack_Slice_Diagonal', .42, 6.8]], 1500, H, 10.4, 1.75);
    const ref = new Image(); ref.src = 'art/incoming/tribe3d/hero_ref.png'; await ref.decode();
    const RW = Math.round(H * ref.width / ref.height), cv = document.createElement('canvas'); cv.width = RW + 1000 + 1500; cv.height = H + 70; const g = cv.getContext('2d');
    g.fillStyle = '#1c150c'; g.fillRect(0, 0, cv.width, cv.height); g.drawImage(ref, 0, 70, RW, H); g.putImageData(big, RW, 70); g.putImageData(row, RW + 1000, 70);
    await document.fonts.load('800 20px Kanit'); g.font = '800 44px Kanit'; g.textAlign = 'center'; g.fillStyle = '#ffd24a';
    g.fillText('แบบที่ส่งมา', RW / 2, 52); g.fillText('3D ในเกม', RW + 500, 52); g.fillText('ข้าง / หลัง / ท่าฟัน', RW + 1750, 52);
    return cv.toDataURL();
  }, +(process.argv[3] || .4));
  if (!url) { console.log('no hero template'); process.exit(1); }
  fs.writeFileSync(process.argv[2], Buffer.from(url.split(',')[1], 'base64')); await b.close(); })();
