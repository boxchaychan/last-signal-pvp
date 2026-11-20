/* Checks for war.html "ศึกแม่ทัพ" (needs: python3 -m http.server 8000 in the repo).
   node tools/qa/war_check.js look <outPrefix> [extra query]   -> pictures: title, map, camp, prep, fight, end + console errors
   node tools/qa/war_check.js camp [tries]                     -> a bot plays the 20 stages (auto formation, buys upgrades evenly), prints tries per stage */
const { chromium } = require('playwright');
const MODE = process.argv[2] || 'look', ARG = process.argv[3] || 'war', EXTRA = process.argv[4] || '';
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }), p = await b.newPage({ viewport: { width: 900, height: 420 } });
  const errs = []; p.on('pageerror', e => errs.push('ERR ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });
  const ready = async () => { for (let i = 0; i < 120; i++) { await p.waitForTimeout(1000); const st = await p.evaluate(() => window.GAME && GAME.G.state).catch(() => 0); if (st && st !== 'load') return; } throw new Error('no load'); };
  if (MODE === 'look') {
    await p.addInitScript(() => localStorage.clear()); await p.goto('http://localhost:8000/war.html?snd=0' + EXTRA); await ready(); await p.waitForTimeout(1200);
    const shot = async n => { await p.waitForTimeout(700); await p.screenshot({ path: `${ARG}_${n}.png` }); };
    await shot('1title'); await p.evaluate(() => { GAME.G.state = 'map'; }); await shot('2map'); await p.evaluate(() => { GAME.G.state = 'camp'; }); await shot('3camp');
    await p.evaluate(() => { GAME.G.state = 'prep'; }); await shot('4prep'); await p.evaluate(() => GAME.startFight()); await p.waitForTimeout(500); await p.evaluate(() => GAME.sim(6)); await shot('5fight');
    await p.evaluate(() => GAME.sim(200)); await p.waitForTimeout(2500); await shot('6end'); console.log(JSON.stringify(await p.evaluate(() => ({ st: GAME.G.state, won: GAME.G.won, t: Math.round(GAME.G.t), info: GAME.info() }))));
  } else {
    await p.goto('http://localhost:8000/war.html?snd=0&norender=1'); await ready();
    const out = await p.evaluate(async (maxTry) => {
      const G = GAME.G, S = GAME.SAVE, rows = []; S.gold = 0; S.stars = {}; S.ulv = {}; S.glv = {}; S.form = null;
      const spend = () => { for (let k = 0; k < 200; k++) { const opts = []; for (const t in GAME.TYPES) if (GAME.typeOpen(t)) opts.push({ t, lv: S.ulv[t] || 1, c: GAME.upCost('u', S.ulv[t] || 1) }); for (const g of GAME.GKEYS) if (GAME.genOpen(g)) opts.push({ g, lv: S.glv[g] || 1, c: GAME.upCost('gen', S.glv[g] || 1) });
        const o = opts.filter(o => o.lv < 15).sort((a, b) => a.c - b.c)[0]; if (!o || o.c > S.gold) break; S.gold -= o.c; if (o.t) S.ulv[o.t] = o.lv + 1; else S.glv[o.g] = o.lv + 1; } };
      for (let s = 0; s < 20; s++) { let tries = 0, won = false, t = 0;
        while (!won && tries < maxTry) { tries++; await GAME.setupStage(s, true); await GAME.autoPlace(); GAME.startFight(); for (let i = 0; i < 5000 && G.state === 'fight'; i++) GAME.tickN(1 / 20); won = G.won; t = Math.round(G.t); spend(); }
        rows.push(`${s + 1}: tries ${tries} ${won ? 'WON' : 'LOST'} stars ${G.stars} t ${t}s gold ${S.gold} lv ${JSON.stringify(S.ulv)} gen ${JSON.stringify(S.glv)}`); if (!won) break; }
      return rows.join('\n'); }, +ARG || 6);
    console.log(out);
  }
  console.log(errs.slice(0, 12).join('\n')); await b.close();
})();
