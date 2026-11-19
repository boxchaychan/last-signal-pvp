// guardtd.html MAZE mode check (owner 2026-11-19 "เล่นคล้ายๆ green td"): screenshots of the field, a wall line with the route arrows, the build
// menu (blue = the way with a tower there, red = would close the way), a wave walking the maze; then checks that no tower can close the way.
// python3 -m http.server 8000 ; node tools/qa/guardtd_maze.js [out=/tmp/maze] [hero=archer]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '/tmp/maze', hero = process.argv[3] || 'archer'; require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = []; const pg = await (await b.newContext({ viewport: { width: 844, height: 390 } })).newPage();
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('http://localhost:8000/guardtd.html?snd=0&mode=maze&hero=' + hero); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 120000 });
  await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/m1_start.png` });
  // a wall line with a gap: the arrows must go round it
  const r1 = await pg.evaluate(() => { const G = GAME.G; G.gold = 99999; const P = (i, j) => GAME.PADAT[GAME.cId(i, j)]; let ok = 0;
    for (let j = 1; j <= 7; j++) ok += GAME.buildTower(P(4, j), 'wall') ? 1 : 0; for (let j = 2; j <= 8; j++) ok += GAME.buildTower(P(11, j), 'wall') ? 1 : 0;
    GAME.buildTower(P(4, 4), 'archer'); GAME.buildTower(P(11, 5), 'mage'); GAME.buildTower(P(5, 7), 'bomb'); GAME.buildTower(P(10, 2), 'knight');
    const D = GAME.DIST[GAME.SPC[0]]; return { walls: ok, dist: +D.toFixed(1) }; });
  await pg.waitForTimeout(600); await pg.screenshot({ path: `${out}/m2_walls.png` });
  // menu on a free tile (blue preview) and on a tile that would close the way (red)
  const r2 = await pg.evaluate(() => { const P = (i, j) => GAME.PADAT[GAME.cId(i, j)]; const p = P(7, 3); const [x, y] = GAME.toScreen(p.c.x, .1, p.c.z); GAME.tap(x, y); return { menu: !!GAME.G.menu }; });
  await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/m3_menu_ok.png` });
  const r3 = await pg.evaluate(() => { GAME.G.menu = null; const P = (i, j) => GAME.PADAT[GAME.cId(i, j)]; const p = P(4, 8); const [x, y] = GAME.toScreen(p.c.x, .1, p.c.z); GAME.tap(x, y); const can = GAME.canBuild(p), built = GAME.buildTower(p, 'wall'); return { canCloseGap: can, built }; });
  await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/m4_menu_bad.png` });
  // a wave walks the maze
  await pg.evaluate(async () => { GAME.G.menu = null; await GAME.startWave(); GAME.sim(9); });
  await pg.waitForTimeout(600); await pg.screenshot({ path: `${out}/m5_wave.png` });
  // random building never closes the way
  const r4 = await pg.evaluate(async () => { const G = GAME.G; let tries = 0, built = 0; for (let k = 0; k < 600; k++) { const p = GAME.PADS[Math.random() * GAME.PADS.length | 0]; if (p.tower) continue; tries++; if (GAME.buildTower(p, 'wall')) built++; }
    GAME.flow(); const open = GAME.SPC.some(c => GAME.DIST[c] < 1e8); let stuck = 0; for (const m of GAME.MON) if (!m.dead && !m.fly && GAME.DIST[m.tgt] >= 1e8) stuck++;
    let g = 0; while ((G.queue.length || GAME.MON.length) && g++ < 900) GAME.sim(.5); return { tries, built, open, stuck, left: GAME.MON.length, wave: G.wave, lives: G.lives, kills: G.kills }; });
  await pg.waitForTimeout(300); await pg.screenshot({ path: `${out}/m6_full.png` });
  console.log(JSON.stringify({ r1, r2, r3, r4, info: await pg.evaluate(() => GAME.info()) }));
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].join('\n') : 'no errors'); await b.close();
})();
