// Colours a unit template of tribe3d.html by its skin weights (one colour per bone) in rest + a few moves: to check a rig made by
// tools/blender/tripo_rig.py (bow on the hand, cape / braids off the arms).   node tools/qa/tripo_weights.js out.png handl,lowerarml,upperarml,handr,lowerarmr,upperarmr
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const url = await pg.evaluate((bones) => { const P = GAME.PEOPLE, R = TB.renderer, T = P.tpl.hunter3, W = 2000, H = 800;
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff, 0x888888, 1));
    const cols = [[1, .1, .1], [.1, .9, .1], [.2, .4, 1], [1, .9, .1], [1, .2, 1], [.1, 1, 1]];
    [['Rest', 0, 0], ['Idle', .3, 0], ['Ranged_Bow_Draw', .8, 0], ['Rest', 0, Math.PI / 2], ['Idle', .3, Math.PI / 2]].forEach(([clip, f, ry], i) => {
      const o = THREE.SkeletonUtils.clone(T.root); let m = null; o.traverse(x => { if (x.isSkinnedMesh) m = x; });
      const g = m.geometry.clone(), si = g.attributes.skinIndex, sw = g.attributes.skinWeight, names = m.skeleton.bones.map(b => b.name), C = new Float32Array(si.count * 3);
      for (let v = 0; v < si.count; v++) { let c = [.55, .55, .55]; for (let k = 0; k < 4; k++) { const n = names[si.getComponent ? si.getComponent(v, k) : [si.getX(v), si.getY(v), si.getZ(v), si.getW(v)][k]], w = [sw.getX(v), sw.getY(v), sw.getZ(v), sw.getW(v)][k], bi = bones.indexOf(n); if (bi >= 0 && w > .05) c = c.map((q, j) => q * (1 - w) + cols[bi][j] * w); } C.set(c, v * 3); }
      g.setAttribute('color', new THREE.BufferAttribute(C, 3)); m.geometry = g; m.material = new THREE.MeshLambertMaterial({ vertexColors: true });
      o.scale.setScalar(2.6 / T.h); const cl = T.clips.find(c => c.name === clip); if (cl) { const mx = new THREE.AnimationMixer(o); mx.clipAction(cl).play(); mx.update(cl.duration * f); }
      o.position.x = i * 3.2; o.rotation.y = ry; sc.add(o); });
    const vw = 16, vh = vw * H / W, cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 100); cam.position.set(6.4, 1.5 + 1, 30); cam.lookAt(6.4, 1.5, 0);
    const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4 }); R.setRenderTarget(rt); R.setClearColor(0x223344, 1); R.clear(); R.render(sc, cam); const px = new Uint8Array(W * H * 4); R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g2 = cv.getContext('2d'), id = g2.createImageData(W, H); for (let y = 0; y < H; y++) id.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4); g2.putImageData(id, 0, 0); return cv.toDataURL(); }, process.argv[3].split(','));
  fs.writeFileSync(process.argv[2], Buffer.from(url.split(',')[1], 'base64')); await b.close(); })();
