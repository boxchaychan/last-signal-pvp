// The ★★★ warrior = the owner's Tripo demon knight (art/tribe3d/people/demon_knight.glb): three of them fight a night pack; moves, kills, errors, a picture.
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_knight.js [out_dir] [mix|old]   (mix = the KayKit knight wearing the demon knight's helmet + pads)
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const out = process.argv[2] || '.'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1280, height: 720 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (/error/.test(m.type()) || /demon knight|knight mix/.test(m.text())) errs.push(m.text()); });
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0' + (process.argv[3] ? '&knight=' + process.argv[3] : '')); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const res = await pg.evaluate(() => {
    const G = GAME.G, T = GAME.PEOPLE.tpl.warrior3; let n = 0; T.root.traverse(o => { if (o.isSkinnedMesh) n++; });
    GAME.cheat.res(99999); TB.hold = true; const run = s => { for (let t = 0; t < s; t += .05) TB.step(.05); };
    GAME.tryUpgrade(G.hall); const q = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = q; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown')); run(30);
    const f = GAME.forts()[0]; f.lv = 3; G.hall.lv = 5; for (let i = 0; i < 3; i++) GAME.train(f, 1, 'warrior'); run(25);
    const ks = G.sol.filter(s => s.kind === 'warrior' && s.tier === 3);
    GAME.cheat.night(); TB.step(.2); G.raid = null; for (let i = 0; i < 6; i++) GAME.spawnEnemy(i % 2 ? 'wolf' : 'tribal', f.x + 14 + (i % 3) * 2, f.z + (i / 3 | 0) * 3);
    const moves = new Set(); for (let t = 0; t < 30; t += .05) { TB.step(.05); for (const s of ks) moves.add(s.cur); }
    TB.camT.set(f.x + 8, 0, f.z); TB.zoomBy(3); TB.hold = false;
    return { tplMeshes: n, tplH: +T.h.toFixed(2), knights: ks.length, moves: [...moves].join(','), killed: G.killed, alive: G.enemies.filter(e => !e.dead).length, hp: ks.map(s => Math.round(s.hp / s.max * 100)).join(',') };
  });
  await pg.waitForTimeout(1200); await pg.screenshot({ path: out + '/knight_fight.png' });
  console.log(JSON.stringify(res)); console.log('errors:', errs.length ? errs.join(' | ') : 'none'); await b.close(); })();
