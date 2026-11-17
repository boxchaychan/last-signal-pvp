// Render groups of a Tripo split model's parts (front + side) to find which part numbers make a helmet, pads, ... (tools/blender/tripo_gear.py).
//   python3 -m http.server 8000 ; node tools/art/tripo_part_view.js /art/incoming/grind3d/knight/knight_raw.glb out.png "all:;helmet:3,111,141,142;pads:6,7" [front|side|both]
const { chromium } = require('playwright');
(async () => {
  const [url, out, sets, views = 'both'] = process.argv.slice(2);
  const html = `<html><body style="margin:0;background:#333"><script src="/vendor/threejs/three.min.js"></script><script src="/vendor/threejs/GLTFLoader.js"></script>
  <script>
  window.go = async (url, sets, views) => {
    const gl = await new THREE.GLTFLoader().loadAsync(url); const R = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); R.setSize(300, 300); R.outputEncoding = THREE.sRGBEncoding;
    const sc = new THREE.Scene(); sc.background = new THREE.Color(0x8899aa); sc.add(new THREE.HemisphereLight(0xffffff, 0x666666, 1.1)); const d = new THREE.DirectionalLight(0xffffff, .8); d.position.set(1, 2, 3); sc.add(d); sc.add(gl.scene);
    const parts = []; gl.scene.traverse(o => { if (o.isMesh) { const m = o.name.match(/(\\d+)$/) || (o.parent && o.parent.name.match(/(\\d+)$/)); o.userData.n = m ? +m[1] : -1; parts.push(o); } });
    const box = new THREE.Box3().setFromObject(gl.scene), c = box.getCenter(new THREE.Vector3()), sz = box.getSize(new THREE.Vector3());
    const V = views === 'both' ? ['front', 'side'] : [views]; const cv = document.createElement('canvas'); cv.width = 300 * sets.length; cv.height = 300 * V.length + 24; const x = cv.getContext('2d'); x.fillStyle = '#222'; x.fillRect(0, 0, cv.width, cv.height);
    sets.forEach(([lab, ids, zoom], i) => {
      let bb = new THREE.Box3(); for (const o of parts) { o.visible = !ids.length || ids.includes(o.userData.n); if (o.visible) bb.expandByObject(o); }
      const cc = bb.getCenter(new THREE.Vector3()), s = Math.max(...bb.getSize(new THREE.Vector3()).toArray()) * .62;
      const cam = new THREE.OrthographicCamera(-s, s, s, -s, .01, 100);
      V.forEach((v, j) => { cam.position.copy(cc).add(v === 'front' ? new THREE.Vector3(0, 0, 10) : new THREE.Vector3(10, 0, 0)); cam.lookAt(cc); R.render(sc, cam); x.drawImage(R.domElement, i * 300, 24 + j * 300); });
      x.fillStyle = '#fff'; x.font = '16px sans-serif'; x.fillText(lab, i * 300 + 6, 18);
    });
    return cv.toDataURL();
  };
  </script></body></html>`;
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.route('http://localhost:8000/__view.html', r => r.fulfill({ body: html, contentType: 'text/html' }));
  pg.on('console', m => { if (m.type() === 'error') console.log('ERR', m.text()); });
  await pg.goto('http://localhost:8000/__view.html');
  const S = sets.split(';').map(s => { const [l, ids] = s.split(':'); return [l, ids ? ids.split(',').filter(Boolean).map(Number) : []]; });
  const data = await pg.evaluate(([u, s, v]) => go(u, s, v), [url, S, views]);
  require('fs').writeFileSync(out, Buffer.from(data.split(',')[1], 'base64')); await b.close();
})();
