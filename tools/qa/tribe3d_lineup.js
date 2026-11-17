// All units ★ next to ★★ (warrior, hunter / archer, shaman) standing in the game itself, pretty mode, labels; for the owner.
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_lineup.js out.png
const {chromium} = require('playwright');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&gfx=2'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && TB.animalsReady, null, {timeout: 150000});
  const res = await pg.evaluate(() => {
    const G = GAME.G; GAME.cheat.res(99999); TB.hold = true; const run = s => { for (let t = 0; t < s; t += .05) TB.step(.05); };
    GAME.tryUpgrade(G.hall); const q = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = q; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); run(30);
    const f = GAME.forts()[0];
    for (const [fl, hl] of [[1, 2], [2, 3], [3, 5]]) {   // train each tier by setting the levels for a moment, then free the units from promotion
      f.lv = fl; G.hall.lv = hl; GAME.train(f, 1, 'warrior'); GAME.train(f, 1, 'hunter'); GAME.train(G.hall, 1, 'shaman'); run(20); for (const s of G.sol) s.fort = null; }
    G.t = 12; G.enemies.length = 0;
    const order = [['warrior', 1], ['warrior', 2], ['warrior', 3], ['hunter', 1], ['hunter', 2], ['hunter', 3], ['shaman', 1], ['shaman', 2], ['shaman', 3]];
    const h = G.hall, cx = VX + 2, cz = VZ + 9, out = [], face = Math.atan2(TOC.x, TOC.z);
    order.forEach(([k, t], i) => { const s = G.sol.find(u => u.kind === k && (u.tier || 1) === t && !u.used); if (!s) return; s.used = true;
      const off = -19.5 + i * 4.3 + Math.floor(i / 3) * 1.4; s.x = cx + R.x * off; s.z = cz + R.z * off; s.g.position.set(s.x, groundY(s.x, s.z), s.z); s.g.rotation.y = face + .35; out.push(s); });   // in a row across the screen, facing the camera
    for (const v of G.vill) { v.x = h.x - 30; v.z = h.z - 30; v.g.position.set(v.x, groundY(v.x, v.z), v.z); } if (G.chief) G.chief.g.visible = false;
    TB.camT.set(cx, 0, cz); TB.zoomBy(3); document.getElementById('hud').style.display = 'none'; document.getElementById('gOv').style.display = 'none';
    TB.draw();
    const lab = (s, i) => { const v = new THREE.Vector3(s.x, groundY(s.x, s.z), s.z).project(cam), rc = document.querySelector('canvas').getBoundingClientRect(); return [(v.x + 1) / 2 * rc.width + rc.left, (1 - v.y) / 2 * rc.height + rc.top]; };
    const names = { warrior: ['นักรบ', 'นักรบ', 'นักรบ'], hunter: ['พรานหน้าไม้', 'นักธนู', 'นักธนู'], shaman: ['หมอผี', 'หมอผี', 'หมอผี'] };
    out.forEach(s => { const [x, y] = lab(s); const d = document.createElement('div'); d.innerHTML = names[s.kind][(s.tier || 1) - 1] + '<br>' + '★'.repeat(s.tier || 1);
      Object.assign(d.style, { position: 'fixed', left: x + 'px', top: (y + 34) + 'px', transform: 'translateX(-50%)', font: '800 17px Kanit, sans-serif', lineHeight: '1.15', textAlign: 'center', color: s.tier > 2 ? '#e8a8ff' : s.tier > 1 ? '#ffd24a' : '#ffffff', textShadow: '0 2px 0 #140c06, 0 -1px 0 #140c06, 2px 0 0 #140c06, -2px 0 0 #140c06', zIndex: 9, whiteSpace: 'nowrap' }); document.body.appendChild(d); });
    const t = document.createElement('div'); t.textContent = '★ ปกติ · ★★ ป้อมขั้น 2 · ★★★ ป้อมขั้น 3 (หมอผี: โถงขั้น 3 / 5)'; Object.assign(t.style, { position: 'fixed', left: '50%', top: '14px', transform: 'translateX(-50%)', font: '800 20px Kanit, sans-serif', color: '#fff', background: '#20140acc', padding: '4px 16px', borderRadius: '10px', zIndex: 9 }); document.body.appendChild(t);
    return out.map(s => s.kind + (s.tier || 1)).join(',');
  });
  console.log('placed', res); await pg.waitForTimeout(600); await pg.screenshot({ path: process.argv[2] }); await b.close(); })();
