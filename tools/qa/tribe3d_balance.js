// Balance run for tribe3d.html: a simple "player" builds every morning (towers first, then huts / farms / walls / an outpost
// when affordable), the game runs at full speed for N days; prints the state at each dawn. One browser, headless.
//   node tools/qa/tribe3d_balance.js [days, default 12]        SKILLS=1 node ... = with the chief's skills
const {chromium} = require('playwright');
const DAYS = +(process.argv[2] || 12), SKILLS = !!process.env.SKILLS;   // SKILLS=1: the player also throws each ready skill at the thickest pack
(async () => { const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({viewport: {width: 844, height: 390}}); const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push(e.message + (e.stack || '').split('\n')[1]));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1'); await pg.waitForFunction(() => window.GAME && GAME.on && TB.animalsReady, null, {timeout: 90000});
  for (let d = 0; d < DAYS; d++) {
    const r = await pg.evaluate((SK) => {
      const G = GAME.G, BT = GAME.BT, can = c => Object.entries(c).every(([k, v]) => G.res[k] >= v), plan = ['tower', 'hut', 'farm', 'tower', 'wall', 'wall', 'hut', 'fire', 'outpost', 'tower'];
      let built = [];
      for (const t of plan) { if (!can(BT[t].cost)) continue; const p = GAME.spot(t); if (!p) continue; GAME.startBuild(t); G.ghostAt = p; G.ghostOk = true; GAME.confirmBuild(); built.push(t); }
      if (GAME.G.mode) { /* leave build mode */ }
      TB.hold = true; const start = G.day; let guard = 0;
      let casts = 0; while (G.day === start && !G.over && guard++ < 6000) { TB.step(.05); if (SK && guard % 20 === 0 && GAME.isNight() && GAME.autoCast()) casts++; }
      return { casts, day: G.day, over: G.over, built: built.join('+'), vill: G.vill.length, hall: Math.round(G.hall.hp), b: G.buildings.length, killed: G.killed, res: Object.values(G.res).map(Math.round).join('/') };
    }, SKILLS);
    console.log(JSON.stringify(r)); if (r.over) break;
  }
  console.log('errors', errs.slice(0, 5).join(' | ') || 'none'); await b.close(); })();
