// front / side / back of a GLB with some parts hidden: node tools/qa/glb_turnaround_hide.js <glb> <out.png> "<part numbers, comma separated>"
const { chromium } = require('playwright');
(async () => {
  const glb = process.argv[2], out = process.argv[3];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 1800, height: 1000 } })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/__blank__'); await pg.setContent('<html><body style="margin:0;background:#c8c8c8"><canvas id="c" width="1800" height="1000"></canvas></body></html>');
  await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/three.min.js' }); await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/GLTFLoader.js' }); await pg.evaluate(h => { window.HIDE = h; }, (process.argv[4] || '').split(',').filter(Boolean).map(Number));
  const info = await pg.evaluate(async glb => {
    const r = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true }); r.outputEncoding = THREE.sRGBEncoding; r.setClearColor(0xc8c8c8);
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff, 0x888888, 1.1)); const d = new THREE.DirectionalLight(0xffffff, .8); d.position.set(1, 2, 3); sc.add(d);
    const g = (await new THREE.GLTFLoader().loadAsync(glb)).scene; const HIDE = (window.HIDE || []); g.traverse(o => { if (o.isMesh && HIDE.includes(+o.name.split('_').pop())) o.visible = false; }); const box = new THREE.Box3().setFromObject(g), sz = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
    const H = sz.y * 1.08, W = H * 1.5, cam = new THREE.OrthographicCamera(-W / 2, W / 2, H / 2, -H / 2, .01, 100);
    const views = [[0, 'front'], [Math.PI / 2, 'side'], [Math.PI, 'back']]; r.setScissorTest(true);
    views.forEach(([a, n], i) => { const p = new THREE.Group(); sc.add(p); g.position.set(-c.x, -c.y, -c.z); p.add(g); p.rotation.y = -a; cam.position.set(0, 0, 10); cam.lookAt(0, 0, 0);
      r.setViewport(i * 600, 0, 600, 1000); r.setScissor(i * 600, 0, 600, 1000); cam.left = -H * .3; cam.right = H * .3; cam.updateProjectionMatrix(); r.render(sc, cam); sc.remove(p); });
    return { size: [sz.x, sz.y, sz.z].map(v => +v.toFixed(2)) };
  }, 'http://localhost:8000/' + glb);
  console.log(JSON.stringify(info)); await pg.locator('#c').screenshot({ path: out }); console.log(errs.length ? errs.join('\n') : 'no errors'); await b.close();
})();
