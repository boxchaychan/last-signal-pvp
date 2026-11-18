// Render groups of a Tripo split model's parts (front + side) to find which part numbers make a helmet, pads, ... (tools/blender/tripo_gear.py).
//   python3 -m http.server 8000 ; node tools/art/tripo_part_view.js /art/incoming/grind3d/knight/knight_raw.glb out.png "all:;helmet:3,111,141,142;pads:6,7" [front|side|both] [tile px] [grid]
//   grid = lines every 0.05 model units with their heights / x / z, for finding the joints of a new model (tools/blender/tripo_parts_rig.py J)
const { chromium } = require('playwright');
(async () => {
  const [url, out, sets, views = 'both', TS = '300', grid = ''] = process.argv.slice(2);
  const html = `<html><body style="margin:0;background:#333"><script src="/vendor/threejs/three.min.js"></script><script src="/vendor/threejs/GLTFLoader.js"></script>
  <script>
  window.go = async (url, sets, views, T, grid) => {
    const gl = await new THREE.GLTFLoader().loadAsync(url); const R = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); R.setSize(T, T); R.outputEncoding = THREE.sRGBEncoding;
    const sc = new THREE.Scene(); sc.background = new THREE.Color(0x8899aa); sc.add(new THREE.HemisphereLight(0xffffff, 0x666666, 1.1)); const d = new THREE.DirectionalLight(0xffffff, .8); d.position.set(1, 2, 3); sc.add(d); sc.add(gl.scene);
    const parts = []; gl.scene.traverse(o => { if (o.isMesh) { const m = o.name.match(/(\\d+)$/) || (o.parent && o.parent.name.match(/(\\d+)$/)); o.userData.n = m ? +m[1] : -1; parts.push(o); } });
    const box = new THREE.Box3().setFromObject(gl.scene), c = box.getCenter(new THREE.Vector3()), sz = box.getSize(new THREE.Vector3());
    const V = views === 'both' ? ['front', 'side'] : [views]; const cv = document.createElement('canvas'); cv.width = T * sets.length; cv.height = T * V.length + 24; const x = cv.getContext('2d'); x.fillStyle = '#222'; x.fillRect(0, 0, cv.width, cv.height);
    sets.forEach(([lab, ids, zoom], i) => {
      let bb = new THREE.Box3(); for (const o of parts) { o.visible = !ids.length || ids.includes(o.userData.n); if (o.visible) bb.expandByObject(o); }
      const cc = bb.getCenter(new THREE.Vector3()), s = Math.max(...bb.getSize(new THREE.Vector3()).toArray()) * .62;
      const cam = new THREE.OrthographicCamera(-s, s, s, -s, .01, 100);
      V.forEach((v, j) => { cam.position.copy(cc).add(v === 'front' ? new THREE.Vector3(0, 0, 10) : new THREE.Vector3(10, 0, 0)); cam.lookAt(cc); R.render(sc, cam); x.drawImage(R.domElement, i * T, 24 + j * T);
        if (grid) { x.save(); x.font = '11px sans-serif'; const k = T / (2 * s), oy = 24 + j * T;
          for (let g = Math.ceil((cc.y - s) / .05) * .05; g < cc.y + s; g += .05) { const yy = oy + (cc.y + s - g) * k; x.strokeStyle = 'rgba(255,255,0,.35)'; x.beginPath(); x.moveTo(i * T, yy); x.lineTo(i * T + T, yy); x.stroke(); x.fillStyle = '#ff0'; x.fillText(g.toFixed(2), i * T + 2, yy - 2); }
          const h0 = v === 'front' ? cc.x : -cc.z, sg = v === 'front' ? 1 : -1;   // side view: screen right = -z (front of the model faces left)
          for (let g = Math.ceil((h0 - s) / .05) * .05; g < h0 + s; g += .05) { const xx = i * T + (g - h0 + s) * k; x.strokeStyle = 'rgba(0,255,255,.3)'; x.beginPath(); x.moveTo(xx, oy); x.lineTo(xx, oy + T); x.stroke(); x.fillStyle = '#0ff'; x.fillText((sg * g).toFixed(2), xx + 2, oy + T - 4); }
          x.restore(); } });
      x.fillStyle = '#fff'; x.font = '16px sans-serif'; x.fillText(lab, i * T + 6, 18);
    });
    return cv.toDataURL();
  };
  </script></body></html>`;
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.route('http://localhost:8000/__view.html', r => r.fulfill({ body: html, contentType: 'text/html' }));
  pg.on('console', m => { if (m.type() === 'error') console.log('ERR', m.text()); });
  await pg.goto('http://localhost:8000/__view.html');
  const S = sets.split(';').map(s => { const [l, ids] = s.split(':'); return [l, ids ? ids.split(',').filter(Boolean).map(Number) : []]; });
  const data = await pg.evaluate(([u, s, v, t, g]) => go(u, s, v, t, g), [url, S, views, +TS, grid]);
  require('fs').writeFileSync(out, Buffer.from(data.split(',')[1], 'base64')); await b.close();
})();
