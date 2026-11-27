// Class check of bag3d.html (owner 2026-11-28: KayKit classes + "คุณสมบัติคลาสคล้องกับไอเทมที่เราเชื่อมในกระเป๋า"). For every class:
//   - the title shows all 5 classes, picking one starts with its own bag and its own 3D body;
//   - CLASS LINKS: a test bag (class item kinds side by side / apart) gives the right number of links, the linked item really gets the class bonus
//     (damage / cooldown / crit / poison / life steal vs the same bag with the items apart) and the tiers switch on at 2 / 4 / 6 links;
//   - the bag draws one link marker per link; the swarm fight gets the class (address + numbers).
// python3 -m http.server 8000 ; node tools/qa/bag3d_class.js [out dir]   (exit 1 on a failure)
const { chromium } = require('playwright'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/bag3d_class'; fs.mkdirSync(out, { recursive: true }); let ok = true; const say = (n, v) => { console.log((v ? 'ok  ' : 'FAIL') + ' ' + n); if (!v) ok = false; };
  const b = await chromium.launch(), pg = await (await b.newContext({ viewport: { width: 844, height: 390 }, hasTouch: true })).newPage(), errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/bag3d.html?mute=1&t=' + Date.now()); await pg.waitForTimeout(1500); await pg.evaluate(() => localStorage.clear()); await pg.reload(); await pg.waitForTimeout(2500);
  const cards = await pg.evaluate(() => [...document.querySelectorAll('.ch')].map(e => e.dataset.k)); say('title shows the 5 classes: ' + cards.join(', '), cards.length === 5);
  await pg.screenshot({ path: out + '/title.png' });
  for (const cls of cards) {
    await pg.click(`.ch[data-k="${cls}"]`); await pg.waitForTimeout(300); await pg.click('#start'); await pg.waitForFunction(c => window.D3 && D3.hero && D3.cls === c, cls, { timeout: 15000 }).catch(() => {});
    const r = await pg.evaluate(cls => {
      const C = BAGCLS[cls], A = BAGKIND[C.link.a], B = BAGKIND[C.link.b], ids = Object.keys(IT).filter(k => !IT[k].tree && IT[k].r < 4), one = k => IT[k].sh.length === 1;
      const a = ids.find(k => A(IT[k]) && IT[k].dmg && !B(IT[k]) && IT[k].sh.length <= 2) || ids.find(k => A(IT[k]) && !B(IT[k])), bs = ids.filter(k => B(IT[k]) && !A(IT[k]) && one(k));
      const start = G.items.map(o => o.id), d3 = !!(D3.hero && D3.cls === cls);
      for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) G.open[x + ',' + y] = 1;   /* a big open bag for the test */
      const make = apart => { G.items = []; const w = give(a, 3, 2, 0), c = cellsOf(w), around = []; for (const [x, y] of c) for (const [p, q] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const X = x + p, Y = y + q; if (!c.some(e => e[0] === X && e[1] === Y) && !around.some(e => e[0] === X && e[1] === Y)) around.push([X, Y]); }
        bs.slice(0, 3).forEach((k, i) => { const [x, y] = apart ? [0, i * 2] : around[i]; give(k, x, y, 0); }); return w; };
      const H = HEROES[cls], f0 = (make(true), build(G.items.filter(o => o.bag), 100, H.aff, H.base)), w1 = make(false), f1 = build(G.items.filter(o => o.bag), 100, H.aff, H.base);
      draw(); const marks = document.querySelectorAll('#grid svg.links circle').length, rib = ($('#left .rib') || {}).textContent || '';
      const W0 = f0.its.find(q => q.d.id === a), W1 = f1.its.find(q => q.u === w1.u), P = C.link.per, n = f1.links.per.get(w1) || 0;
      const gain = []; if (W0 && W1) { if (P.dmg) gain.push(['dmg', W1.dmg / W0.dmg]); if (P.cd) gain.push(['cd', W0.cd / W1.cd]); if (P.crit) gain.push(['crit', W1.crit - W0.crit]); if (P.poi) gain.push(['poi', (W1.poi || 0) - (W0.poi || 0)]); if (P.ls) gain.push(['ls', (W1.ls || 0) - (W0.ls || 0)]); }
      /* tiers: a bag with 6+ links (two a-items, three b-items each) */
      G.items = []; const a2 = ids.filter(k => A(IT[k]) && !B(IT[k])).sort((p, q) => IT[p].sh.length - IT[q].sh.length); let tierN = 0, tiers = [];
      if (a2.length) { const busy = new Set(); for (const [x, y] of [[2, 1], [6, 1]]) { const w = give(a2[0], x, y, 0), c = cellsOf(w); c.forEach(([p, q]) => busy.add(p + ',' + q)); let k = 0;
          for (const [p, q] of c) for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) { const X = p + dx, Y = q + dy; if (k >= 3 || busy.has(X + ',' + Y) || X < 0 || Y < 0 || X >= GW || Y >= GH) continue; busy.add(X + ',' + Y); give(bs[k++ % bs.length], X, Y, 0); } }
        const f2 = build(G.items.filter(o => o.bag), 100, H.aff, H.base); tierN = f2.links.n; tiers = f2.links.tier.map(t => t[3]); }
      const hz = hordeCfg(build([], 100, H.aff, H.base), 1);
      return { start, d3, a, bs: bs.slice(0, 3), n0: f0.links.n, n1: f1.links.n, n, marks, rib, gain, per: P, tierN, tiers, cfgCls: hz.cls, cfgKind: hz.sk && hz.sk.kind, src: HZ.el ? HZ.el.src : '' };
    }, cls);
    say(`${cls}: starts with ${r.start.join(' + ')}, 3D body loaded`, r.start.length === 2 && r.d3);
    say(`${cls}: ${r.a} apart = ${r.n0} links, beside ${r.bs.join(', ')} = ${r.n1} links (${r.n} on it), ${r.marks} markers`, r.n0 === 0 && r.n1 >= 1 && r.marks === r.n1);
    const good = r.gain.length && r.gain.every(([c, v]) => c === 'dmg' || c === 'cd' ? v > 1 + (r.per[c] || 0) * r.n * .9 : v >= (r.per[c] || 0) * r.n * .9);
    say(`${cls}: the linked item gains ${r.gain.map(([c, v]) => c + ' ' + (c === 'dmg' || c === 'cd' ? 'x' + v.toFixed(2) : '+' + v.toFixed(2))).join(', ')}`, good);
    say(`${cls}: a 6-link bag has ${r.tierN} links, tiers on: ${r.tiers.join(',')}`, r.tierN >= 6 && r.tiers.every(Boolean));
    say(`${cls}: the swarm fight gets the class (${r.cfgCls}, skill ${r.cfgKind}) and loads ${r.src.replace(/^.*\//, '').slice(0, 60)}`, r.cfgCls === cls && r.cfgKind === BAGCLS_KIND(cls) && r.src.includes('cls=' + cls));
    await pg.screenshot({ path: `${out}/bag_${cls}.png` });
    await pg.evaluate(() => { localStorage.removeItem('bag.save'); }); await pg.goto('http://localhost:8000/bag3d.html?mute=1&t=' + Date.now()); await pg.waitForTimeout(2000);
  }
  function BAGCLS_KIND(c) { return { knight: 'bash', barbarian: 'spin', mage: 'meteor', ranger: 'fan', rogue: 'venom' }[c]; }
  say('no errors on the page', !errs.length); if (errs.length) console.log(errs.slice(0, 6).join('\n'));
  console.log(ok ? 'CLASSES OK' : 'CLASSES FAIL'); await b.close(); process.exit(ok ? 0 : 1);
})();
