// each big part of a split GLB alone (front view) + the whole model. node tools/qa/glb_parts_grid.js <glb> <out.png> [count=10] [hide=i,j]
const { chromium } = require('playwright');
(async () => {
  const glb = process.argv[2], out = process.argv[3], N = +(process.argv[4] || 10), hide = (process.argv[5] || '').split(',').filter(Boolean).map(Number);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 2000, height: 900 } })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/__blank__'); await pg.setContent('<html><body style="margin:0"><canvas id="c" width="2000" height="900"></canvas></body></html>');
  await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/three.min.js' }); await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/GLTFLoader.js' });
  await pg.evaluate(async ([glb, N, hide]) => {
    const r = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true }); r.outputEncoding = THREE.sRGBEncoding; r.setClearColor(0xc8c8c8); r.setScissorTest(true);
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff, 0x888888, 1.1)); const d = new THREE.DirectionalLight(0xffffff, .8); d.position.set(1, 2, 3); sc.add(d);
    const g = (await new THREE.GLTFLoader().loadAsync(glb)).scene; sc.add(g); const box = new THREE.Box3().setFromObject(g), sz = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
    const parts = []; g.traverse(o => { if (o.isMesh) parts.push(o); }); parts.sort((a, b) => b.geometry.attributes.position.count - a.geometry.attributes.position.count); window.PN = parts.map(p => p.name + ':' + p.geometry.attributes.position.count);
    const H = sz.y * 1.05, cam = new THREE.OrthographicCamera(-H * .3, H * .3, H / 2, -H / 2, .01, 100); cam.position.set(c.x, c.y, c.z + 20); cam.lookAt(c);
    const tiles = [...Array(N).keys()].map(i => [i]).concat([['all']]); const tw = 2000 / tiles.length;
    tiles.forEach(([k], i) => { parts.forEach((p, j) => p.visible = k === 'all' ? !hide.includes(j) : j === k); r.setViewport(i * tw, 0, tw, 900); r.setScissor(i * tw, 0, tw, 900); cam.left = -H * .3; cam.right = H * .3; cam.top = H / 2 * 900 / 900; cam.updateProjectionMatrix(); r.render(sc, cam); });
  }, ['http://localhost:8000/' + glb, N, hide]); console.log(await pg.evaluate(() => PN.slice(0, 12).join(' ')));
  await pg.locator('#c').screenshot({ path: out }); console.log(errs.length ? errs.join('\n') : 'no errors'); await b.close();
})();
