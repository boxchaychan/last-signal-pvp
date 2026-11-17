// ★★ units: train ★ at a level-1 fort, upgrade the fort -> they turn ★★ (knight + crest shield + plume, archer with bow /
// quiver / plume, crimson shaman from hall 3); cards switch; a fight; villagers use the work moves. Screenshots + lineup.
//   python3 -m http.server 8000 ; node tools/qa/tribe3d_tiers.js <folder>
const {chromium} = require('playwright'); const fs = require('fs');
const out = process.argv[2];
(async () => { const b = await chromium.launch(); const errs = [], log = [];
  const pg = await (await b.newContext({ viewport: { width: 1280, height: 720 } })).newPage();
  pg.on('pageerror', e => errs.push('PAGEERR ' + e.message + ' ' + (e.stack || '').split('\n')[1])); pg.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
  try {
    await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready && TB.animalsReady, null, {timeout: 150000});
    log.push('templates: ' + await pg.evaluate(() => ['warrior2', 'hunter2', 'shaman2'].map(k => k + ':' + !!GAME.PEOPLE.tpl[k]).join(' ') + ' clips ' + GAME.PEOPLE.clips.length + ' portraits ' + Object.keys(GAME.PEOPLE.portrait).join(',')));
    const f = await pg.evaluate(() => { const G = GAME.G; GAME.cheat.res(5000); GAME.tryUpgrade(G.hall); const p = GAME.spot('fort'); GAME.startBuild('fort'); G.ghostAt = p; G.ghostOk = true; GAME.confirmBuild(); document.getElementById('gNo').dispatchEvent(new PointerEvent('pointerdown'));
      TB.hold = true; for (let t = 0; t < 30; t += .05) TB.step(.05); const f = GAME.forts()[0]; GAME.train(f, 2, 'warrior'); GAME.train(f, 2, 'hunter'); GAME.train(G.hall, 1, 'shaman'); for (let t = 0; t < 40; t += .05) TB.step(.05); return { x: f.x, z: f.z }; });
    log.push('before: ' + await pg.evaluate(() => GAME.G.sol.map(s => s.kind + s.tier).join(',')));
    await pg.evaluate(() => { const G = GAME.G; GAME.tryUpgrade(G.hall); GAME.tryUpgrade(GAME.forts()[0]); TB.step(.05); });
    log.push('after fort 2 + hall 3: ' + await pg.evaluate(() => GAME.G.sol.map(s => s.kind + s.tier + ':' + s.max).join(',')));
    await pg.evaluate(f => { GAME.select(GAME.forts()[0]); TB.camT.set(f.x, 0, f.z + 2); TB.zoomBy(2); TB.hold = true; for (let t = 0; t < 1.5; t += .05) TB.step(.05); TB.hold = false; }, f);
    await pg.waitForTimeout(1200); await pg.screenshot({ path: `${out}/tier_fort.png` });
    log.push('cards: ' + await pg.evaluate(() => [...document.querySelectorAll('#gSel .uc b')].map(e => e.textContent).join(' | ')));
    await pg.evaluate(() => GAME.select(null));
    // a fight: archers shoot with the bow move, villagers work with tools
    await pg.evaluate(f => { const G = GAME.G; GAME.cheat.night(); TB.hold = true; TB.step(.2); G.raid = null; for (let i = 0; i < 6; i++) GAME.spawnEnemy('wolf', f.x + 20 + (i % 3) * 2, f.z + (i / 3 | 0) * 3); }, f);
    let moves = new Set(); for (let i = 0; i < 30; i++) { await pg.evaluate(() => { for (let t = 0; t < .3; t += .05) TB.step(.05); TB.draw(); }); (await pg.evaluate(() => GAME.G.sol.map(s => s.cur))).forEach(m => moves.add(m)); }
    await pg.evaluate(f => { TB.camT.set(f.x + 10, 0, f.z); TB.draw(); }, f); await pg.screenshot({ path: `${out}/tier_fight.png` });
    log.push('fight moves: ' + [...moves].join(',') + ' | killed ' + await pg.evaluate(() => GAME.G.killed));
    await pg.evaluate(() => { GAME.G.t = 10; TB.hold = true; for (let t = 0; t < 15; t += .05) TB.step(.05); });
    log.push('villager moves: ' + await pg.evaluate(() => [...new Set(GAME.G.vill.map(v => v.cur))].join(',')));
    // lineup of all unit portraits
    const urls = await pg.evaluate(() => GAME.PEOPLE.portrait);
    await pg.setContent(`<body style="margin:0;background:#2c2418;display:flex;flex-wrap:wrap;width:1240px;gap:8px;padding:10px;font:800 14px sans-serif;color:#ffd27a">${['warrior', 'warrior2', 'warrior3', 'hunter', 'hunter2', 'hunter3', 'shaman', 'shaman2', 'shaman3', 'man', 'woman', 'chief'].map(k => `<div style="text-align:center"><img src="${urls[k]}" style="width:144px;height:168px;background:radial-gradient(circle at 50% 35%,#5a7a9a,#22344a 75%);border-radius:14px"><div>${k}</div></div>`).join('')}</body>`);
    await pg.setViewportSize({ width: 1260, height: 420 }); await pg.screenshot({ path: `${out}/tier_portraits.png` });
  } catch (e) { errs.push('TEST ' + e.message); }
  console.log(log.join('\n')); console.log('errors: ' + (errs.length ? '\n' + errs.slice(0, 8).join('\n') : 'none')); await b.close();
})();
