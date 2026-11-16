// All units ★ next to ★★ (warrior, hunter / archer, shaman) standing in the game itself, pretty mode, labels; for the owner.
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_lineup.js out.png
const {chromium} = require('playwright');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&gfx=2'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && TB.animalsReady, null, {timeout: 150000});
  const res = await pg.evaluate(() => {
    const G = GAME.G; GAME.cheat.res(9000); TB.hold = true; const run = s => { for (let t = 0; t < s; t += .05) TB.step(.05); };
    GAME.tryUpgrade(G.hall);   // hall 2
    const mk = () => { const q = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = q; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); };
    mk(); run(30); GAME.tryUpgrade(G.hall); mk(); run(30);   // hall 3 allows the 2nd fort
    const [f1, f2] = GAME.forts();
    GAME.train(f1, 1, 'warrior'); GAME.train(f1, 1, 'hunter'); run(15);
    G.hall.lv = 2; GAME.train(G.hall, 1, 'shaman'); run(10); G.hall.lv = 3;          // a ★ shaman (trained as if the hall were level 2)
    for (const s of G.sol) s.fort = null;                                              // keep the ★ ones ★ (promotion only touches a fort's own units)
    GAME.tryUpgrade(f2); GAME.train(f2, 1, 'warrior'); GAME.train(f2, 1, 'hunter'); GAME.train(G.hall, 1, 'shaman'); run(20);
    G.t = 12; G.enemies.length = 0;
    const order = [['warrior', 1], ['warrior', 2], ['hunter', 1], ['hunter', 2], ['shaman', 1], ['shaman', 2]];
    const h = G.hall, cx = VX + 2, cz = VZ + 9, out = [], face = Math.atan2(TOC.x, TOC.z);
    order.forEach(([k, t], i) => { const s = G.sol.find(u => u.kind === k && (u.tier || 1) === t && !u.used); if (!s) return; s.used = true;
      const off = -13.4 + i * 4.6 + Math.floor(i / 2) * 1.6; s.x = cx + R.x * off; s.z = cz + R.z * off; s.g.position.set(s.x, groundY(s.x, s.z), s.z); s.g.rotation.y = face + .35; out.push(s); });   // in a row across the screen, facing the camera
    for (const v of G.vill) { v.x = h.x - 30; v.z = h.z - 30; v.g.position.set(v.x, groundY(v.x, v.z), v.z); } if (G.chief) G.chief.g.visible = false;
    TB.camT.set(cx, 0, cz); TB.zoomBy(3); TB.zoomBy(1); document.getElementById('hud').style.display = 'none'; document.getElementById('gOv').style.display = 'none';
    TB.draw();
    const lab = (s, i) => { const v = new THREE.Vector3(s.x, groundY(s.x, s.z), s.z).project(cam), rc = document.querySelector('canvas').getBoundingClientRect(); return [(v.x + 1) / 2 * rc.width + rc.left, (1 - v.y) / 2 * rc.height + rc.top]; };
    const names = { warrior: ['นักรบ', 'นักรบ'], hunter: ['พรานหน้าไม้', 'นักธนู'], shaman: ['หมอผี', 'หมอผี'] };
    out.forEach(s => { const [x, y] = lab(s); const d = document.createElement('div'); d.innerHTML = names[s.kind][(s.tier || 1) - 1] + '<br>' + ((s.tier || 1) > 1 ? '★★' : '★');
      Object.assign(d.style, { position: 'fixed', left: x + 'px', top: (y + 34) + 'px', transform: 'translateX(-50%)', font: '800 17px Kanit, sans-serif', lineHeight: '1.15', textAlign: 'center', color: s.tier > 1 ? '#ffd24a' : '#ffffff', textShadow: '0 2px 0 #140c06, 0 -1px 0 #140c06, 2px 0 0 #140c06, -2px 0 0 #140c06', zIndex: 9, whiteSpace: 'nowrap' }); document.body.appendChild(d); });
    const t = document.createElement('div'); t.textContent = '★ ปกติ  ·  ★★ หลังอัปเกรดป้อมเป็นขั้น 2 (หมอผี: โถงขั้น 3)'; Object.assign(t.style, { position: 'fixed', left: '50%', top: '14px', transform: 'translateX(-50%)', font: '800 20px Kanit, sans-serif', color: '#fff', background: '#20140acc', padding: '4px 16px', borderRadius: '10px', zIndex: 9 }); document.body.appendChild(t);
    return out.map(s => s.kind + (s.tier || 1)).join(',');
  });
  console.log('placed', res); await pg.waitForTimeout(600); await pg.screenshot({ path: process.argv[2] }); await b.close(); })();
