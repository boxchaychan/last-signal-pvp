// GLB checks (run python3 -m http.server 8000 first). node tools/qa/<this> <glb path from repo root> <out.png>
const { chromium } = require('playwright');
(async () => {
  const glb = process.argv[2], out = process.argv[3];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 2000, height: 1000 } })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/__blank__'); await pg.setContent('<html><body style="margin:0"><canvas id="c" width="2000" height="1000"></canvas></body></html>');
  await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/three.min.js' }); await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/GLTFLoader.js' });
  await pg.evaluate(async glb => {
    const r = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true }); r.outputEncoding = THREE.sRGBEncoding; r.setClearColor(0xc8c8c8); r.setScissorTest(true);
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff, 0x9a8a80, .42)); const d = new THREE.DirectionalLight(0xffffff, .62); d.position.set(.6, 1.2, 1.5); sc.add(d);
    const g = (await new THREE.GLTFLoader().loadAsync(glb)).scene; sc.add(g);
    const SKIN = 0xf0b48c, HAIR = 0x7a3e22, TOP = 0x9a9aa2, SHORT = 0x3c3c44, RED = 0xd8342c, DARK = 0x2a1810, WHITE = 0xffffff, BROW = 0x5a3020;
    const C = { 0: SKIN, 1: HAIR, 2: SKIN, 3: SKIN, 4: SKIN, 8: SKIN, 5: TOP, 6: SHORT, 7: TOP, 9: HAIR, 10: DARK, 11: DARK, 12: 0xc0605a, 21: BROW, 23: BROW, 26: RED, 27: RED, 28: RED, 29: RED, 30: 0xb01818, 31: 0xb01818, 32: DARK, 33: DARK, 34: WHITE, 35: WHITE };
    const grad = new THREE.DataTexture(new Uint8Array([90, 90, 90, 255, 190, 190, 190, 255, 255, 255, 255, 255]), 3, 1); grad.minFilter = grad.magFilter = THREE.NearestFilter; grad.needsUpdate = true;
    g.traverse(o => { if (!o.isMesh) return; const k = +o.name.replace('tripo_part_', ''); o.material = new THREE.MeshToonMaterial({ color: C[k] !== undefined ? C[k] : HAIR, gradientMap: grad }); });
    const box = new THREE.Box3().setFromObject(g), sz = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
    const H = sz.y * 1.06, cam = new THREE.OrthographicCamera(-1, 1, 1, -1, .01, 100);
    const views = [[0, 0, c.y, H], [Math.PI / 2, 1, c.y, H], [Math.PI, 2, c.y, H], [0, 3, .77, .32]];
    views.forEach(([a, i, cy, h]) => { cam.position.set(c.x + Math.sin(a) * 10, cy, c.z + Math.cos(a) * 10); cam.lookAt(c.x, cy, c.z); cam.left = -h * .25; cam.right = h * .25; cam.top = h / 2; cam.bottom = -h / 2; cam.updateProjectionMatrix();
      r.setViewport(i * 500, 0, 500, 1000); r.setScissor(i * 500, 0, 500, 1000); r.render(sc, cam); });
  }, 'http://localhost:8000/' + glb);
  await pg.locator('#c').screenshot({ path: out }); console.log(errs.length ? errs.join('\n') : 'no errors'); await b.close();
})();
