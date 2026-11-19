// guardtd.html smoke check before shipping: every tower at level 1 and level 4, the hero at Lv 12 casting all 4 skills, 6 waves with a boss.
// python3 -m http.server 8000 ; node tools/qa/guardtd_alltowers.js [archer|wing|demon|dark|hood] [circle (default)|maze|road]
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('http://localhost:8000/guardtd.html?snd=0&hero=' + (process.argv[2] || 'archer') + (process.argv[3] ? '&mode=' + process.argv[3] : '')); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 120000 }); await pg.waitForTimeout(800);
  const r = await pg.evaluate(async () => { const G = GAME.G; G.gold = 99999; const ks = ['archer', 'mage', 'bomb', 'knight']; GAME.PADS.slice(0, 8).forEach((p, i) => GAME.buildTower(p, ks[i % 4]));
    GAME.TOWERS.slice(4).forEach(t => { GAME.upgradeTower(t); GAME.upgradeTower(t); GAME.upgradeTower(t); }); const H = GAME.HERO; H.lv = 12; H.pts = 0; H.sk = [3, 3, 3, 3];
    const kinds = {}; for (let w = 0; w < 6; w++) { await GAME.startWave(); let g = 0; while ((G.queue.length || GAME.MON.length) && g++ < 600) { GAME.sim(.5); for (const m of GAME.MON) kinds[m.k] = 1; if (g % 4 === 0) { const m = GAME.MON.filter(q => !q.dead)[0]; for (let k = 0; k < 4; k++) { H.cdk[k] = 0; GAME.castSkill(k, m ? m.pos.clone() : new THREE.Vector3()); } } } G.build = 0; }
    return { wave: G.wave, lives: G.lives, kills: G.kills, towers: GAME.TOWERS.map(t => t.k[0] + t.lv).join(''), kinds: Object.keys(kinds).length }; });
  for (let i = 0; i < 20; i++) { await pg.evaluate(() => GAME.sim(.2)); await pg.waitForTimeout(50); }
  console.log(JSON.stringify(r)); console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].join('\n') : 'no errors'); await b.close(); })();
