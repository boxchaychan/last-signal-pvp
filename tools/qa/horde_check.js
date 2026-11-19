// horde.html "ฝ่าฝูงอสูร" (3D horde survival). look = screenshots of the title, the shop, the missions, a fight with a shrine, the level-up cards, a boss, the result;
// bot = the built-in simple player (?bot=1) plays a whole run with the game logic only (?norender=1) and prints how it went.
// python3 -m http.server 8000 ; node tools/qa/horde_check.js look [out=/tmp/horde] [hero=archer] [map=forest]  |  node tools/qa/horde_check.js bot [hero] [map] [seconds=600]
const { chromium } = require('playwright');
(async () => {
  const what = process.argv[2] || 'look', b = await chromium.launch(), errs = [];
  if (what === 'look') {
    const out = process.argv[3] || '/tmp/horde', hero = process.argv[4] || 'archer', map = process.argv[5] || 'forest'; require('fs').mkdirSync(out, { recursive: true });
    const pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 2 })).newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    await pg.goto(`http://localhost:8000/horde.html?snd=0&nopause=1&unlock=1&god=1&q=0&hero=${hero}&map=${map}`, { waitUntil: 'domcontentloaded', timeout: 120000 }); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'title', null, { timeout: 180000 });
    await pg.waitForTimeout(2500); await pg.screenshot({ path: `${out}/1_title.png` });
    await pg.evaluate(() => { GAME.SAVE.coins = 900; GAME.G.state = 'shop'; }); await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/2_shop.png` });
    await pg.evaluate(() => { GAME.SAVE.mk = {}; GAME.MAPS[GAME.MAPK].mobs.flat().slice(0, 13).forEach((k, i) => { GAME.SAVE.mk[k] = 12 + i * 37; }); GAME.SAVE.mk[GAME.MAPS[GAME.MAPK].boss[0]] = 2; GAME.G.state = 'codex'; GAME.CODEX.map = Object.keys(GAME.MAPS).indexOf(GAME.MAPK); }); await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/2c_codex.png` });
    await pg.evaluate(() => { GAME.SAVE.kills = 2600; GAME.SAVE.runs = 7; GAME.SAVE.evos = 1; GAME.G.state = 'quest'; }); await pg.waitForTimeout(500); await pg.screenshot({ path: `${out}/2b_quest.png` });
    await pg.evaluate(() => { GAME.G.state = 'title'; GAME.startRun(); }); await pg.waitForFunction(() => GAME.G.state === 'relic', null, { timeout: 120000 }); await pg.waitForTimeout(1200); await pg.screenshot({ path: `${out}/2d_relic.png` });
    await pg.evaluate(() => { GAME.BOT.on = true; }); await pg.waitForFunction(() => GAME.G.state === 'play', null, { timeout: 120000 });
    await pg.evaluate(() => GAME.sim(25)); await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/3_start.png` });
    const r1 = await pg.evaluate(async () => { const G = GAME.G; for (const k of ['orb', 'fire', 'bolt', 'frost', 'aura']) if (!G.weps.some(w => w.k === k) && G.weps.length < 6) GAME.addWeapon(k); for (let i = 0; i < 12 && G.state === 'play' && G.t < 200; i++) { GAME.sim(15); await new Promise(r => setTimeout(r, 30)); } return { t: G.t, lv: G.lv, alive: GAME.aliveN(), kills: G.kills, state: G.state, hp: GAME.HERO.hp }; });
    await pg.evaluate(() => { GAME.spawnShrine(); const sh = GAME.SHRINES[0]; if (sh) { sh.x = GAME.HERO.pos.x + 2.5; sh.z = GAME.HERO.pos.z - 1.5; sh.g.position.set(sh.x, 0, sh.z); } GAME.G.rage = 12; }); await pg.waitForTimeout(1500); await pg.screenshot({ path: `${out}/4_crowd.png` }); const play = await pg.evaluate(() => GAME.info());
    await pg.evaluate(() => { GAME.BOT.on = false; GAME.G.pend = 1; }); await pg.waitForFunction(() => GAME.G.state === 'levelup', null, { timeout: 20000 }).catch(() => { }); await pg.waitForTimeout(900); await pg.screenshot({ path: `${out}/5_cards.png` });
    await pg.evaluate(() => { GAME.G.cardT = 1; GAME.pickCard(0); GAME.openChest(); }); await pg.waitForTimeout(1600); await pg.screenshot({ path: `${out}/6_chest.png` });
    await pg.evaluate(() => { GAME.G.state = 'play'; GAME.BOT.on = true; GAME.spawnBoss(1); }); await pg.waitForTimeout(3500); await pg.screenshot({ path: `${out}/7_boss.png` });
    await pg.evaluate(() => { GAME.G.state = 'pause'; }); await pg.waitForTimeout(400); await pg.screenshot({ path: `${out}/8_pause.png` });
    await pg.evaluate(() => { GAME.G.state = 'play'; GAME.finishRun(); }); await pg.waitForTimeout(1600); await pg.screenshot({ path: `${out}/9_end.png` });
    console.log(JSON.stringify({ r1, play, title: await pg.evaluate(() => { GAME.toTitle(); return new Promise(r => setTimeout(() => r(GAME.info()), 1500)); }) }));
  } else {
    const hero = process.argv[3] || 'archer', map = process.argv[4] || 'forest', secs = +(process.argv[5] || 600);
    const pg = await b.newPage(); pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    await pg.goto(`http://localhost:8000/horde.html?snd=0&norender=1&nopause=1&bot=1&unlock=1&hero=${hero}&map=${map}&go=1`, { waitUntil: 'domcontentloaded', timeout: 120000 }); await pg.waitForFunction(() => window.GAME && GAME.G.state === 'play', null, { timeout: 180000 });
    const res = await pg.evaluate(async (secs) => { const G = GAME.G, out = []; let peak = 0, guard = 0;
      while (G.t < secs && guard++ < 4000 && (G.state === 'play' || G.state === 'levelup' || G.state === 'chest')) { GAME.sim(5); peak = Math.max(peak, GAME.aliveN()); if (guard % 6 === 0) { out.push(`${Math.round(G.t)}s lv${G.lv} hp${Math.round(GAME.HERO.hp)}/${GAME.HERO.max} a${GAME.aliveN()} k${G.kills}`); await new Promise(r => setTimeout(r, 0)); } }
      return { out, state: G.state, t: Math.round(G.t), lv: G.lv, kills: G.kills, peak, won: G.won, res: G.result, weps: G.weps.map(w => w.k + w.lv + (w.evo ? '*' : '')), pas: G.pas.map(p => p.k + p.lv), dmg: Object.entries(GAME.STATS).map(([k, v]) => k + ':' + Math.round(v / 1000) + 'k').join(' '), taken: G.taken, boss: G.bossKills }; }, secs);
    console.log(`${hero} @ ${map}: ${res.state} t=${res.t}s lv${res.lv} kills ${res.kills} peak ${res.peak} bosses ${res.boss} won=${res.won} taken ${res.taken}`); console.log(res.out.join(' | ')); console.log('weapons', res.weps.join(' '), '| passives', res.pas.join(' ')); console.log('damage', res.dmg); if (res.res) console.log('result', JSON.stringify(res.res));
  }
  if (errs.length) console.log('ERRORS:\n' + [...new Set(errs)].slice(0, 12).join('\n')); else console.log('no errors'); await b.close();
})();
