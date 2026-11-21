// every part (biggest first) alone in its own full-body tile, labelled, front view: node tools/qa/glb_parts_sheet.js <glb> <out.png> [count=24] [cols=8]
const { chromium } = require('playwright');
(async () => {
  const glb = process.argv[2], out = process.argv[3], N = +(process.argv[4] || 24), C = +(process.argv[5] || 8), TW = 220, TH = 360, R = Math.ceil(N / C);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: TW * C, height: TH * R } })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8000/__blank__'); await pg.setContent(`<html><body style="margin:0;position:relative"><canvas id="c" width="${TW * C}" height="${TH * R}"></canvas><div id="l"></div></body></html>`);
  await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/three.min.js' }); await pg.addScriptTag({ url: 'http://localhost:8000/vendor/threejs/GLTFLoader.js' });
  await pg.evaluate(async ([glb, N, C, TW, TH]) => {
    const r = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true }); r.outputEncoding = THREE.sRGBEncoding; r.setClearColor(0xd0d0d0); r.setScissorTest(true);
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff, 0x888888, 1.1)); const d = new THREE.DirectionalLight(0xffffff, .8); d.position.set(1, 2, 3); sc.add(d);
    const g = (await new THREE.GLTFLoader().loadAsync(glb)).scene; sc.add(g); const box = new THREE.Box3().setFromObject(g), sz = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
    const parts = []; g.traverse(o => { if (o.isMesh) parts.push(o); }); parts.sort((a, b) => b.geometry.attributes.position.count - a.geometry.attributes.position.count);
    const H = sz.y * 1.04, cam = new THREE.OrthographicCamera(-H * TW / TH / 2, H * TW / TH / 2, H / 2, -H / 2, .01, 100); cam.position.set(c.x, c.y, c.z + 20); cam.lookAt(c); cam.updateProjectionMatrix();
    const L = document.getElementById('l'); const H0 = TH * Math.ceil(N / C);
    parts.slice(0, N).forEach((p, i) => { parts.forEach(q => q.visible = q === p); const x = (i % C) * TW, y = Math.floor(i / C) * TH; r.setViewport(x, H0 - y - TH, TW, TH); r.setScissor(x, H0 - y - TH, TW, TH); r.render(sc, cam);
      const t = document.createElement('div'); t.textContent = p.name.replace('tripo_part_', '#') + ' (' + p.geometry.attributes.position.count + ')'; Object.assign(t.style, { position: 'absolute', left: x + 4 + 'px', top: y + 2 + 'px', font: 'bold 15px sans-serif', color: '#a00' }); L.appendChild(t); });
  }, ['http://localhost:8000/' + glb, N, C, TW, TH]);
  await pg.screenshot({ path: out }); console.log(errs.length ? errs.join('\n') : 'no errors'); await b.close();
})();
