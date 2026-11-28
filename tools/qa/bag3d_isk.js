// ITEM SIGNATURE SKILLS check (owner 2026-11-28 "ไอเทมมีสกิลเฉพาะ", "vfx สวยๆ"; list in bag3d/itemskills.js).
//   1. every item that fires (weapon, shield / food with a cooldown, start-of-fight item) has a skill, every effect sheet it names exists;
//   2. bag3d.html: the item info and the shop cards name the skill; in a duel the skills go off (counted) and add damage;
//   3. the swarm arena (horde.html?bag=1&map=arena): every skill kind is set off once with monsters around -> 2 frames each (arena_<kind>_*.png);
//   4. the side-view duel: every kind's big effect + its name label -> 3 frames each (duel_<kind>_*.png).
// python3 -m http.server 8000 ; node tools/qa/bag3d_isk.js [out=/tmp/bag3d_isk] [dsf 1]   then: python3 tools/qa/bag3d_isk_sheet.py <out>
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_isk', dsf = +(process.argv[3] || 1); fs.mkdirSync(out, { recursive: true }); let ok = true; const say = (n, v) => { console.log((v ? 'ok  ' : 'FAIL') + ' ' + n); if (!v) ok = false; };
  const { ITEMSK } = require(path.resolve(__dirname, '../../bag3d/itemskills.js'));
  const miss = [...new Set(Object.values(ITEMSK).flatMap(s => [s.pf, s.pf2]).filter(Boolean))].filter(p => !fs.existsSync(path.resolve(__dirname, '../../art/pvfx', p, 'sprite-sheet.png')));
  say('every effect sheet the skills name exists' + (miss.length ? ': missing ' + miss.join(', ') : ''), !miss.length);
  const b = await chromium.launch(), errs = [], watch = pg => { pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); };
  const ctx = await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: dsf }), shop = await ctx.newPage(); watch(shop);
  await shop.goto('http://localhost:8000/bag3d.html?mute=1&fight=side'); await shop.waitForTimeout(2000); await shop.evaluate(() => localStorage.clear()); await shop.reload(); await shop.waitForTimeout(2000); await shop.click('#start'); await shop.waitForTimeout(400);
  /* 1 + 2: coverage, item info, shop cards, the duel */
  const r = await shop.evaluate(() => {
    const fires = Object.keys(IT).filter(k => (IT[k].t === 'w' || IT[k].cd) && !IT[k].start && !IT[k].sp)   /* start-of-fight items fire once: no skill; the spell items of the redesign (sp: storm, stones, ball, skeletons ...) ARE skills, their move is the spell */, none = fires.filter(k => !iskOf(k, IT[k].base)), kinds = {};
    for (const k of fires) { const S = iskOf(k, IT[k].base); if (S && !kinds[S.k]) kinds[S.k] = k; }
    const info = desc({ id: 'sword', lv: 1, u: 1 }); G.shop = ['sword', 'bow', 'shield', 'apple', 'wand', 'feather', 'crown', 'axe'].map(id => ({ id })); draw(); const skn = (info.match(/class="iskt"/g) || []).length + (info.match(/class="iskl"/g) || []).length;
    /* the duel: a mid bag against a dummy, skills on and off */
    for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) G.open[x + ',' + y] = 1; G.items = []; for (const [id, x, y] of [['sword', 0, 0], ['bow', 2, 0], ['wand', 4, 0], ['shield', 6, 0], ['apple', 0, 3]]) give(id, x, y, 0);
    const H = HEROES[HK], mk = () => build(G.items.filter(o => o.bag), 120, H.aff, H.base); let fired = 0, dmgOn = 0, dmgOff = 0;
    const run = on => { const A = mk(), B = build([], 99999, H.aff, H.base); B.hp = B.max = 99999;   /* a training dummy: no armour or shield, so only the skills make the difference */ if (!on) for (const w of A.its) w.isk = 0; let T = 0; const ev = []; while (T < 30) { tick(A, B, .05, T, ev); for (const e of ev) if (e.k === 'isk' && e.s === 0) fired++; ev.length = 0; T += .05; } return 99999 - B.hp; };
    for (let i = 0; i < 6; i++) { dmgOn += run(true); dmgOff += run(false); }
    return { fires: fires.length, none, kinds, info: /สกิลเฉพาะ/.test(info), skn, fired: fired / 6, gain: dmgOn / dmgOff };
  });
  say(`${r.fires} items fire, all have a skill` + (r.none.length ? ' (none: ' + r.none.join(', ') + ')' : ''), !r.none.length);
  say(`${Object.keys(r.kinds).length} skill kinds in use: ${Object.keys(r.kinds).join(' ')}`, Object.keys(r.kinds).length >= 14);
  say(`item info names the skill (a tag on its first line + a line with what it does: ${r.skn} of 2)`, r.info && r.skn === 2);
  say(`duel: a 5-item bag sets off ${r.fired.toFixed(1)} skills in 30 s, damage x${r.gain.toFixed(2)} with them`, r.fired >= 4 && r.gain > 1.1 && r.gain < 1.5);
  await shop.screenshot({ path: out + '/shop.png' }); await shop.evaluate(() => { const o = give('sword', 3, 1, 0); draw(); say(desc(o)); }); await shop.waitForTimeout(150); await shop.screenshot({ path: out + '/info.png' }); await shop.click('#info'); await shop.waitForTimeout(200); await shop.screenshot({ path: out + '/info_pop.png' }); say('a tap on the info strip opens all of it', await shop.evaluate(() => $('#pop').style.display === 'flex' && /สกิลเฉพาะ/.test($('#pop div').textContent))); await shop.evaluate(() => closePop());
  /* 3: the swarm arena, every kind once */
  const ids = Object.values(r.kinds), cfg = await shop.evaluate(ids => { const H = HEROES[HK], its = []; let c0 = null;
    for (const id of ids) { G.items = []; give(id, 0, 0, 0); const f = build(G.items.filter(o => o.bag), 200, H.aff, Object.assign({}, H.base, { cls: null, sk: null })), c = BG.hordeCfg(f, 6);   /* no class: since the type shops (2026-11-28) a knight cannot use a bow or a wand, the test wants every skill kind */ c0 = c0 || c; its.push(...c.items.map(q => Object.assign(q, { cd: 99 }))); }
    return Object.assign(c0, { items: its, hp: 99999, round: 6, boss: false }); }, ids);
  const are = await ctx.newPage(); watch(are); await are.goto('http://localhost:8000/horde.html?bag=1&nopause=1&snd=0&map=arena&land=forest&cls=' + await shop.evaluate(() => HK));
  await are.waitForFunction(() => window.BAGAPI && BAGAPI.BAG.ready, null, { timeout: 60000 }); await are.evaluate(c => BAGAPI.start(c), cfg);
  await are.waitForFunction(() => GAME.G.state === 'play', null, { timeout: 60000 }); await are.waitForTimeout(7000);
  const kinds = await are.evaluate(() => BAGAPI.BAG.its.filter(W => W.isk).map(W => W.isk.k)); say(`arena: ${kinds.length} skill items ready (${kinds.join(' ')})`, kinds.length === ids.length);
  let used0 = await are.evaluate(() => BAGAPI.BAG.iskUsed || 0);
  for (let i = 0; i < kinds.length; i++) {
    await are.evaluate(i => { const B = BAGAPI.BAG, W = B.its.filter(W => W.isk)[i]; GAME.HERO.hp = GAME.HERO.max * .6; for (const m of GAME.MON) if (!m.dead && m.hp < 30) m.hp = m.max = 400; W.iskN = W.iskE - 1; bagIskUse(W); }, i);
    await are.waitForTimeout(380); await are.screenshot({ path: `${out}/arena_${kinds[i]}_0.png` }); await are.waitForTimeout(650); await are.screenshot({ path: `${out}/arena_${kinds[i]}_1.png` }); await are.waitForTimeout(900);
  }
  const used = await are.evaluate(() => BAGAPI.BAG.iskUsed || 0) - used0; say(`arena: ${used} of ${kinds.length} skills went off when set off`, used >= kinds.length - 1);
  /* the real loop sets them off by itself: a normal round with a normal bag */
  const auto = await are.evaluate(async () => { const B = BAGAPI.BAG; for (const W of B.its) { W.cd = 1.2; W.iskN = 0; } B.iskUsed = 0; await new Promise(r => setTimeout(r, 6000)); return B.iskUsed; }); say(`arena: ${auto} skills went off by themselves in 6 s`, auto >= 3);
  await are.close();
  /* 4: the duel, every kind's effect frozen and stepped */
  await shop.evaluate(() => { G.items = []; give('sword', 3, 1, 0); G.round = 4; draw(); $('#go').click(); }); await shop.waitForTimeout(2500);
  await shop.evaluate(() => { window.tick = () => { }; window.requestAnimationFrame = () => 0; $('#mybag').style.display = $('#fbag').style.display = 'none'; });
  for (const [k, id] of Object.entries(r.kinds)) {
    await shop.evaluate(([k, id]) => { const b = BT; b.px.length = 0; b.wp.length = 0; b.fx.length = 0; b.isl = []; b.sh = b.flash = b.punch = 0; b.eh = b.hh = 0; b.slow = 0; window.__t = 0; const it = { u: 99000, id, lv: 1 }, S = iskOf(id, IT[id].base);
      b.isl.push({ s: 0, n: S.n, c: '#' + S.c.toString(16).padStart(6, '0'), i: IT[id].i, t: 0 }); if (k === 'guard' || k === 'feast') castIskSelf(b, { s: 0, k: 'isk', kind: k, id, u: it.u }); if (k !== 'feast') { const dl = castIsk(b, { s: 0, k: 'hit', ik: k, u: it.u, big: 1, v: 40 }, it); b.fx.push({ x: .74, t: -dl, v: 40, c: '#ffd24a', big: 1, dx: 0 }); } }, [k, id]);
    for (const [i, t1] of [.14, .34, .62].entries()) {
      await shop.evaluate(t1 => { const b = BT; while (window.__t < t1 - 1e-6) { const dt = Math.min(1 / 60, t1 - window.__t); window.__t += dt; vfxStep(b, dt); for (const f of b.fx) f.t += dt; for (const f of b.isl) f.t += dt; for (const q of ['ha', 'ea', 'hh', 'eh', 'sh']) b[q] = Math.max(0, b[q] - dt); b.flash = Math.max(0, b.flash - dt * 2.2); } paint(performance.now() / 1000); }, t1);
      await shop.screenshot({ path: `${out}/duel_${k}_${i}.png`, clip: { x: 0, y: 0, width: 844, height: 300 } });
    }
  }
  fs.writeFileSync(out + '/kinds.json', JSON.stringify(r.kinds));
  say('no errors on the pages', !errs.length); if (errs.length) console.log([...new Set(errs)].slice(0, 8).join('\n'));
  console.log(ok ? 'ISK OK' : 'ISK FAIL'); await b.close(); process.exit(ok ? 0 : 1);
})();
