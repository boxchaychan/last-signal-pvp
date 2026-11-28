// STR / AGI / INT check of bag3d.html (owner 2026-11-28: "ค่าสถานะในไอเทม str agi int ยึดตามหลักโมบ้า str บวกเลือด agi ตี int skill เวทย์แรง").
// The same bag is built with an item's attributes switched off and on (BAGATTR in bag3d/classes.js), so only the attributes make the difference:
//   STR -> max life and regen; AGI -> physical weapon damage and attack speed; INT -> magic damage, skill power, skill cooldown;
//   the class's main attribute adds damage to everything; stars scale the attributes; the cards / item info / stats bar show them.
// python3 -m http.server 8000 ; node tools/qa/bag3d_attr.js [out dir]   (exit 1 on a failure)
const { chromium } = require('playwright'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_attr'; fs.mkdirSync(out, { recursive: true }); let ok = true; const say = (n, v) => { console.log((v ? 'ok  ' : 'FAIL') + ' ' + n); if (!v) ok = false; };
  const b = await chromium.launch(), pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, hasTouch: true })).newPage(), errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/bag3d.html?mute=1&t=' + Date.now()); await pg.waitForTimeout(1500); await pg.evaluate(() => localStorage.clear()); await pg.reload(); await pg.waitForTimeout(2000); await pg.click('#start'); await pg.waitForTimeout(600);
  const r = await pg.evaluate(() => {
    const K = BAGATTRK, near = (a, b, e = 1e-6) => Math.abs(a - b) <= e * Math.max(1, Math.abs(b));
    const run = (cls, list, id) => { const H = HEROES[cls]; G.items = []; for (const [k, x, y, lv] of list) { const o = give(k, x, y, 0); o.lv = lv || 1; } const mine = G.items.filter(o => o.bag);
      const keep = BAGATTR[id]; BAGATTR[id] = [0, 0, 0]; const f0 = build(mine, 100, H.aff, H.base); BAGATTR[id] = keep; const f1 = build(mine, 100, H.aff, H.base); return { f0, f1, H }; };
    for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) G.open[x + ',' + y] = 1;
    const o = {};
    /* STR: the knight (main STR) with plate armour (STR 4) beside a sword */
    { const { f0, f1 } = run('knight', [['plate', 0, 0], ['sword', 3, 0]], 'plate'), w0 = f0.its.find(w => w.d.id === 'sword'), w1 = f1.its.find(w => w.d.id === 'sword');
      o.str = { at: f1.at.str, hp: f1.max - f0.max, regen: +(f1.regen - f0.regen).toFixed(3), sword: +(w1.dmg / w0.dmg).toFixed(4), want: { hp: Math.round(4 * K.str.hp), regen: 4 * K.str.regen, sword: 1 + 4 * K.main } }; }
    /* STR at two stars: 4 x 1.55 */
    { const { f1 } = run('knight', [['plate', 0, 0, 2], ['sword', 3, 0]], 'plate'); o.star = { at: f1.at.str, want: Math.round((4 * LM[2] + 1) * 10) / 10 };   /* + the sword's 1 */ }
    /* AGI: the ranger (main AGI) with a bow (AGI 3) */
    { const { f0, f1 } = run('ranger', [['bow', 0, 0]], 'bow'), w0 = f0.its.find(w => w.d.id === 'bow'), w1 = f1.its.find(w => w.d.id === 'bow');
      o.agi = { at: f1.at.agi, dmg: +(w1.dmg / w0.dmg).toFixed(4), haste: +(f1.haste - f0.haste).toFixed(4), want: { dmg: (1 + 3 * K.agi.dmg) * (1 + 3 * K.main), haste: 3 * K.agi.haste } }; }
    /* INT: the mage (main INT) with a fire wand (INT 3) */
    { const { f0, f1 } = run('mage', [['wand', 0, 0]], 'wand'), w0 = f0.its.find(w => w.d.id === 'wand'), w1 = f1.its.find(w => w.d.id === 'wand');
      o.int = { at: f1.at.int, dmg: +(w1.dmg / w0.dmg).toFixed(4), pw: +(f1.pw / f0.pw).toFixed(4), cd: +(f1.sk.cd / f0.sk.cd).toFixed(4), want: { dmg: (1 + 3 * K.int.mdmg) * (1 + 3 * K.main), pw: 1 + 3 * K.int.skill, cd: 1 - 3 * K.int.skcd } }; }
    /* a non-main attribute gives no main bonus: the knight with the lightning ball (a spell item, INT 3; spells count INT .03 a point; since the type shops a knight cannot use a wand) */
    { const { f0, f1 } = run('knight', [['sp_ball', 0, 0]], 'sp_ball'), w0 = f0.its.find(w => w.d.id === 'sp_ball'), w1 = f1.its.find(w => w.d.id === 'sp_ball'); o.off = { dmg: +(w1.dmg / w0.dmg).toFixed(4), want: 1 + 3 * .03 }; }
    /* the UI: a bag, the stats bar, a shop card with chips, the item info */
    G.items = []; give('plate', 2, 1, 0); give('sword', 4, 1, 0); give('wand', 5, 1, 0); G.shop = [{ id: 'plate' }, { id: 'bow' }, { id: 'wand' }, { id: 'crown' }, { id: 'pig' }, { id: 'feather' }, { id: 'katana' }, { id: 'book' }]; draw();
    const st = [...document.querySelectorAll('#stats .at')].map(e => e.textContent.trim()), chips = document.querySelectorAll('#shop .atc i').length, info = desc(G.items[0]);
    return { o, st, chips, info: /STR \+4/.test(info), ok: { near } };
  });
  const o = r.o, close = (a, b, e = 1e-3) => Math.abs(a - b) <= e * Math.max(1, Math.abs(b));
  say(`STR: plate armour STR 4 (bag ${o.str.at} with the sword's 1) -> life +${o.str.hp} (want ${o.str.want.hp}), regen +${o.str.regen} (want ${o.str.want.regen}), the knight's sword x${o.str.sword} from his main STR (want x${o.str.want.sword})`, o.str.at === 5 && o.str.hp === o.str.want.hp && close(o.str.regen, o.str.want.regen) && close(o.str.sword, o.str.want.sword));
  say(`stars: plate ★★ = STR ${o.star.at} (want ${o.star.want})`, close(o.star.at, o.star.want));
  say(`AGI: bow AGI ${o.agi.at} -> bow damage x${o.agi.dmg} (want x${o.agi.want.dmg.toFixed(4)}), attack speed +${o.agi.haste} (want +${o.agi.want.haste})`, o.agi.at === 3 && close(o.agi.dmg, o.agi.want.dmg) && close(o.agi.haste, o.agi.want.haste));
  say(`INT: wand INT ${o.int.at} -> magic x${o.int.dmg} (want x${o.int.want.dmg.toFixed(4)}), skill power x${o.int.pw} (want x${o.int.want.pw} or a little more: it is built from the weapon damage INT raised), skill cooldown x${o.int.cd} (want x${o.int.want.cd})`, o.int.at === 3 && close(o.int.dmg, o.int.want.dmg) && o.int.pw >= o.int.want.pw - 1e-3 && o.int.pw <= o.int.want.pw * o.int.dmg + 1e-3 && close(o.int.cd, o.int.want.cd));
  say(`not the main attribute: the knight's lightning ball x${o.off.dmg} (want x${o.off.want}, no main bonus)`, close(o.off.dmg, o.off.want));
  say(`stats bar shows ${r.st.join(' | ')}`, r.st.length === 3 && /★STR/.test(r.st[0]));
  say(`shop cards show ${r.chips} attribute chips, item info shows STR +4`, r.chips >= 8 && r.info);
  await pg.screenshot({ path: out + '/bag.png' });
  await pg.evaluate(() => { sel = G.items[0]; say(desc(G.items[0])); }); await pg.waitForTimeout(200); await pg.screenshot({ path: out + '/info.png' });
  say('no errors on the page', !errs.length); if (errs.length) console.log(errs.slice(0, 6).join('\n'));
  console.log(ok ? 'ATTRS OK' : 'ATTRS FAIL'); await b.close(); process.exit(ok ? 0 : 1);
})();
