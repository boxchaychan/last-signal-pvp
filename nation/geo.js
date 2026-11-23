'use strict';
/* ก่อร่างสร้างชาติ: provinces inside the country, neighbour countries, trade, alliances and real wars. */
const PROV_T = { farm: ['เกษตร', { food: .05 }], ind: ['อุตสาหกรรม', { prod: .012 }], sea: ['ท่องเที่ยว', { rev: .012, rep: .006 }], mine: ['เหมืองแร่', { priv: .06 }] };

/* ---------- provinces: every city is one, with its own wealth and anger ---------- */
function provType(c) { let river = 0, sea = 0, hill = 0, plain = 0; for (let a = -12; a <= 12; a += 2) for (let b = -12; b <= 12; b += 2) { const x = Math.round(c.x) + a, z = Math.round(c.z) + b; if (!inMap(x, z)) continue; const t = W.T[ci(x, z)]; if (t === 0) sea++; else if (t === 1) river++; else if (t >= 5) hill++; else plain++; } return hill > 26 ? 'mine' : sea > 34 ? 'sea' : river > 7 ? 'farm' : plain > 80 ? 'ind' : 'farm'; }
function provs(S) { S.prov = S.prov || []; G.cities.forEach((c, i) => { if (!S.prov[i]) S.prov[i] = { w: i ? .36 : .6, un: S.unrest || 6, type: provType(c), inv: 0, troops: 0 }; }); return S.prov; }
function provShare(i) { const tot = G.cities.reduce((q, c) => q + Math.max(1, c.n), 0) || 1; return Math.max(1, G.cities[i].n) / tot; }
function provTick(S) {
  const P = provs(S), avg = P.reduce((q, p, i) => q + p.w * provShare(i), 0);
  P.forEach((p, i) => {
    const sh = provShare(i), tgt = clamp(.3 + Math.sqrt(sh) * .34 + (i ? 0 : .12) + p.inv * .5 + clamp(Math.log10(S.x.gdpPc + 10) / 4) * .22); p.w += (tgt - p.w) * .012; p.inv *= .985; p.troops *= .97;
    const t = clamp((S.unrest || 0) + (avg - p.w) * 95 + (i ? 5 : -2) - p.troops * 22 - p.inv * 14, 0, 100); p.un += (t - p.un) * .07;
  });
  if (!G.modal && S.m - (S.sepM || -99) > 30) { const i = P.findIndex((p, q) => q > 0 && p.un > 72); if (i > 0) { S.sepM = S.m; S.evM = S.m; const n = G.cities[i].name; UI.showEvent({ cat: 'จังหวัด', t: n + ' ประกาศจะแยกตัว', b: 'คนใน' + n + ' บอกว่าเมืองหลวงรวยอยู่ฝ่ายเดียว และพวกเขาถูกทอดทิ้งมานาน', o: [['ลงทุนพัฒนาจังหวัดนี้ครั้งใหญ่', { c: 1, geo: ['pinv', i, .5] }], ['ให้ปกครองตนเองบางส่วน', { tr: 2, corr: .006, geo: ['pcalm', i, 34] }], ['ส่งทหารเข้าควบคุม', { c: .3, tr: -6, rep: -.05, geo: ['ptroop', i, 1] }]] }); } }
}

/* ---------- neighbour countries ---------- */
function worldOf(S) { if (!S.world) S.world = RIVALS.slice(0, 6).map(r => ({ n: r[0], pow: 16 + r[1] / 42, eco: r[1], rel: Math.round(-14 + Math.random() * 44), trade: 0, ally: 0, sanc: 0 })); return S.world; }
function myPower(S) { const x = S.x, L = S.lawMod || {}; return (Math.log10(x.pop + 10) * 12 + Math.log10(x.gdp + 10) * 8) * (.5 + Math.min(1.8, S.bud.defense) * .9 + .3 * Math.min(S.k.army || 0, 3) + (L.army || 0)) * Math.sqrt(S.tech); }
function allyPower(S, skip) { return worldOf(S).reduce((q, c, i) => q + (c.ally && i !== skip ? c.pow * .35 : 0), 0); }
function geoMods(S, add) {
  if (!S.world) return; let tr = 0; for (const c of S.world) { if (c.trade) tr++; if (c.ally) { add('tension', -.018); add('army', .05); } if (c.rel <= -62) add('prod', -.008); } if (tr) { add('prod', Math.min(.07, tr * .014)); add('priv', tr * .03); }
  if (S.prov && typeof G !== 'undefined' && G.cities.length) S.prov.forEach((p, i) => { if (!G.cities[i]) return; const m = PROV_T[p.type][1]; for (const k in m) add(k, m[k] * p.w); if (p.un > 52) add('unrest', (p.un - 52) * .07 * provShare(i)); });
}
function startWar(S, i) { const c = worldOf(S)[i]; c.trade = 0; c.ally = 0; c.rel = -100; S.front = { c: i, f: 0, m: S.m }; S.war = Math.max(S.war, 2); recalcGov(S); }
function endWar(S, how) {
  const F = S.front; if (!F) return; const c = S.world[F.c]; S.front = null; S.war = 0;
  if (how === 'win') { const pay = Math.max(S.gdp, 700) * 3; S.treas += pay; S.landBonus = (S.landBonus || 0) + 1; c.pow *= .68; c.rel = -45; applyFx(S, { tr: 8, rep: -.03, unrest: -8 }); UI.showEvent({ cat: 'สงคราม', t: 'คุณชนะสงครามกับ' + c.n + '!', b: 'ได้ค่าปฏิกรรมสงคราม ' + fmt(pay) + ' บาท และดินแดนใหม่สำหรับคนของคุณ', o: [['ประกาศชัยชนะ', { hp: 5 }], ['ยื่นมือคืนดี', { rep: .05, geo: ['rel', F.c, 25] }]] }); }
  else if (how === 'lose') { c.rel = -55; applyFx(S, { pop: -.08, unrest: 24, tr: -14, debt: .6, rep: -.04 }); UI.showEvent({ cat: 'สงคราม', t: 'คุณแพ้สงครามให้' + c.n, b: 'เสียคนและเงินจำนวนมาก ประชาชนเริ่มถามว่าใครต้องรับผิดชอบ', o: [['ยอมรับเงื่อนไขสันติภาพ', { c: .6, unrest: -6 }], ['ปลดรัฐมนตรีกลาโหม', { fire: 'def', unrest: -3 }], ['สาบานว่าจะล้างแค้น', { tr: 3, tension: .1, unrest: 3 }]] }); }
  else { c.rel = Math.max(c.rel, -32); news('สงบศึกกับ' + c.n + ' แล้ว', 'good'); } recalcGov(S);
}
function worldTick(S) {
  const W2 = worldOf(S), x = S.x; if (S.war > 0 && !S.front) { let e = 0; W2.forEach((c, i) => { if (c.rel < W2[e].rel) e = i; }); startWar(S, e); }
  const F = S.front; if (F) { const c = W2[F.c], me = myPower(S) + allyPower(S, F.c), th = c.pow; F.f = clamp(F.f + (me - th) / (me + th) * 15 + (Math.random() - .5) * 8, -100, 100); S.war = Math.max(S.war, 2); S.treas -= S.gdp * .05; if (S.treas < 0) { S.debt += -S.treas * 1.02; S.treas = 0; } if (F.f >= 100) endWar(S, 'win'); else if (F.f <= -100) endWar(S, 'lose'); }
  const mine = myPower(S); W2.forEach(c => { c.pow *= 1.0024; c.rel = clamp(c.rel + (c.trade ? .1 : 0) + (c.ally ? .12 : 0) + (c.rel < 0 ? .05 : -.02) + (S.rep - .35) * .08 - clamp((mine / c.pow - 1) * .05, 0, .12), -100, 100); });
  if (G.modal || S.front || x.pop < 150 || S.m - (S.dipM || 0) < 26 || Math.random() > .42) return; S.dipM = S.m; S.evM = S.m;
  const i = Math.random() * W2.length | 0, c = W2[i];
  if (c.rel < -30 && x.pop > 1500 && c.pow > myPower(S) * .62 && Math.random() < .75) UI.showEvent({ cat: 'สงคราม', t: c.n + ' ประกาศสงครามกับเรา!', b: 'กองทัพของเขาเคลื่อนมาที่ชายฝั่ง กำลังรบ ' + Math.round(c.pow) + ' ต่อของเรา ' + Math.round(myPower(S)), why: ['ความสัมพันธ์กับเขาตกถึง ' + Math.round(c.rel), 'เขาเห็นว่ากองทัพของเราอ่อนกว่า'], o: [['สู้เต็มกำลัง', { c: .5, tr: 5, geo: ['war', i] }], ['ยอมจ่ายค่าไถ่', { c: 1.5, tr: -8, geo: ['rel', i, 18] }], ['เจรจาขอเวลา', { c: .3, unrest: 3, geo: ['rel', i, 9] }]] });
  else if (c.ally) { const o = W2.findIndex(q => q !== c); UI.showEvent({ cat: 'ต่างประเทศ', t: 'พันธมิตร ' + c.n + ' ขอความช่วยเหลือ', b: 'เขากำลังมีปัญหากับ ' + W2[o].n + ' และถามว่าคุณจะอยู่ข้างเขาไหม', o: [['ส่งทหารช่วย', { c: .5, pop: -.002, geo: ['rel2', i, 16, o, -18] }], ['ส่งเงินช่วย', { c: .35, geo: ['rel', i, 8] }], ['ไม่ยุ่ง', { geo: ['rel', i, -16] }]] }); }
  else if (!c.trade && c.rel > -6 && (x.foodMonths > 2.6 || x.E_ind > x.LF * .16)) UI.showEvent({ cat: 'ต่างประเทศ', t: c.n + ' เสนอทำการค้า', b: 'เขาอยากซื้อสินค้าของเรา แต่ขอให้ลดภาษีนำเข้าให้', why: [x.foodMonths > 2.6 ? 'เรามีข้าวเหลือ ' + x.foodMonths.toFixed(1) + ' เดือน' : 'โรงงานของเราผลิตเกินใช้เอง', 'ถ้าเปิดตลาด ของนอกจะมาแข่งกับคนในประเทศ'], o: [['ลงนามเลย', { priv: .15, gini: .006, tr: -1, geo: ['deal', i] }], ['ต่อรองให้เราได้เปรียบ', { geo: ['rel', i, -3] }], ['ปฏิเสธ', { geo: ['rel', i, -9] }]] });
  else if (c.rel < -30) UI.showEvent({ cat: 'ความมั่นคง', t: 'เรือของ' + c.n + ' รุกล้ำน่านน้ำ', b: 'ชาวประมงของเราถูกไล่ และคนทั้งประเทศรอดูว่าคุณจะตอบโต้อย่างไร', why: ['ความสัมพันธ์กับเขาตกถึง ' + Math.round(c.rel)], o: [['ส่งเรือรบไปเผชิญหน้า', { c: .3, tr: 4, tension: .04, geo: ['rel', i, -10] }], ['ประท้วงทางการทูต', { c: .05, geo: ['rel', i, 3] }], ['เงียบไว้', { tr: -5 }]] });
}
function geoFx(S, v) {
  const P = provs(S), W2 = worldOf(S), k = v[0]; if (k === 'pinv') { P[v[1]].inv += v[2]; P[v[1]].w = clamp(P[v[1]].w + v[2] * .3); P[v[1]].un = clamp(P[v[1]].un - 26, 0, 100); } else if (k === 'pcalm') P[v[1]].un = clamp(P[v[1]].un - v[2], 0, 100); else if (k === 'ptroop') { P[v[1]].troops += v[2]; P[v[1]].un = clamp(P[v[1]].un - 18, 0, 100); }
  else if (k === 'rel') W2[v[1]].rel = clamp(W2[v[1]].rel + v[2], -100, 100); else if (k === 'rel2') { W2[v[1]].rel = clamp(W2[v[1]].rel + v[2], -100, 100); W2[v[3]].rel = clamp(W2[v[3]].rel + v[4], -100, 100); } else if (k === 'deal') { W2[v[1]].trade = 1; W2[v[1]].rel = clamp(W2[v[1]].rel + 8, -100, 100); recalcGov(S); } else if (k === 'war') startWar(S, v[1]);
}
/* ---------- big crises: they hit first, then you choose how to respond ---------- */
const CRISES = [
  { t: 'ราคาน้ำมันโลกพุ่ง', b: 'ค่าขนส่งและค่าไฟขึ้นทั้งประเทศภายในสัปดาห์เดียว ร้านค้าเริ่มขึ้นราคา', hit: { unrest: 13, infl: .018, priv: -.3 }, o: [['อุดหนุนราคาพลังงาน', { c: 1.2, unrest: -10 }], ['ปล่อยราคาตามจริง', { infl: .01, unrest: 5 }], ['เร่งพลังงานสะอาด', { c: .8, tech: .012, pol: -.025, unrest: -4 }]] },
  { t: 'ธนาคารใหญ่ล้ม', b: 'ผู้คนแห่ถอนเงินจนตู้เงินว่าง ธุรกิจจ่ายเงินเดือนไม่ได้', hit: { unrest: 15, priv: -.7, tr: -5 }, o: [['ใช้เงินรัฐอุ้มธนาคาร', { c: 1.6, unrest: -11, gini: .015 }], ['ค้ำประกันเฉพาะเงินฝากประชาชน', { c: .9, unrest: -8 }], ['ปล่อยให้ล้ม', { priv: -.4, unrest: 7 }]] },
  { t: 'ข้าวยากหมากแพงทั่วโลก', b: 'ประเทศผู้ส่งออกหยุดขายอาหาร ราคาข้าวในตลาดเพิ่มเท่าตัว', hit: { unrest: 12, food: -.8, infl: .012 }, o: [['ซื้อสำรองทุกราคา', { c: 1.2, food: 1.5, unrest: -9 }], ['ปันส่วนอาหาร', { food: .4, unrest: -2, hp: -4 }], ['ห้ามส่งออกและคุมราคา', { priv: -.3, unrest: -4, rep: -.03 }]] },
  { t: 'คนรุ่นใหม่ลุกขึ้นทั้งประเทศ', b: 'นักศึกษาและคนทำงานรุ่นใหม่ออกมาเรียกร้องเสรีภาพและอนาคตที่ดีกว่า', hit: { unrest: 18, tr: -6 }, o: [['เปิดเวทีและปฏิรูปบางส่วน', { c: .4, tr: 7, unrest: -14, corr: -.012 }], ['สร้างงานและทุนให้คนรุ่นใหม่', { c: 1, edu: .08, unrest: -11 }], ['ปราบให้เด็ดขาด', { unrest: -10, tr: -13, rep: -.1, next: [6, 'martyr'] }]] },
  { t: 'ค่าเงินดิ่งเหว', b: 'นักเก็งกำไรทิ้งเงินของเรา ของนำเข้าแพงขึ้นทันที และหนี้ต่างประเทศบวมขึ้น', hit: { unrest: 11, infl: .025, debt: .25, rep: -.03 }, o: [['ใช้ทุนสำรองพยุงค่าเงิน', { c: 1.4, infl: -.016, unrest: -6 }], ['ขึ้นดอกเบี้ยแรงๆ', { infl: -.02, priv: -.6, unrest: 2 }], ['ขอกู้กองทุนโลก', { debt: .5, bud: -.08, unrest: 3, rep: .01 }]] },
  { t: 'ผู้อพยพหลั่งไหลเข้าประเทศ', b: 'สงครามในภูมิภาคทำให้คนนับหมื่นมาถึงชายฝั่งของเรา งานและบ้านเริ่มไม่พอ', hit: { unrest: 9, pop: .025, crime: .012 }, o: [['ตั้งศูนย์พักและหางานให้', { c: .9, rep: .05, unrest: -7 }], ['รับเฉพาะคนมีฝีมือ', { c: .3, rep: -.01, edu: .03, unrest: -3 }], ['ผลักดันออกทั้งหมด', { rep: -.09, pop: -.02, unrest: -3 }]] }
];
function crisisTick(S) {
  if (S.nextCrisis == null) S.nextCrisis = 120 + Math.random() * 40 | 0; if (G.modal || S.m < S.nextCrisis || S.x.pop < 40) return;
  const c = CRISES[Math.random() * CRISES.length | 0]; S.nextCrisis = S.m + 62 + Math.random() * 62 - (S.x.stage || 0) * 3 | 0; applyFx(S, c.hit); S.evM = S.m; UI.showEvent({ cat: 'วิกฤตใหญ่', t: c.t, b: c.b, o: c.o, why: ['เหตุนี้มาจากนอกประเทศ คุณคุมไม่ได้ แต่เลือกวิธีรับมือได้'] });
}
/* every so often a neighbour turns aggressive, sized to be a real threat to you */
function aggressorTick(S) {
  const x = S.x; if (x.pop < 2500) return; if (S.nextAgg == null) S.nextAgg = S.m + 40 + Math.random() * 50 | 0; if (S.m < S.nextAgg || S.front) return; S.nextAgg = S.m + 100 + Math.random() * 80 | 0;
  const L = S.world.filter(c => !c.ally); if (!L.length) return; const c = L[Math.random() * L.length | 0]; c.rel = Math.min(c.rel, -48); c.trade = 0; c.pow = Math.max(c.pow, myPower(S) * (.78 + Math.random() * .5)); recalcGov(S); news(c.n + ' เริ่มสะสมอาวุธและขู่เรา', 'bad');
}
function geoTick(S) { provTick(S); worldOf(S); aggressorTick(S); worldTick(S); }

/* ---------- folders ---------- */
const bar2 = (l, v, col, t) => '<div class="bar"><span>' + l + '</span><i><u style="width:' + Math.round(clamp(v) * 100) + '%;background:' + col + '"></u></i><b>' + t + '</b></div>';
const WHY_N = { wage: ['ค่าแรงต่ำจนอยู่ไม่ได้', 'ขึ้นค่าแรงขั้นต่ำ หรือฝึกคนให้มีฝีมือ'], neglect: ['บริการรัฐไม่ทั่วถึง', 'สร้างน้ำ หมอ โรงเรียน และไฟฟ้าให้พอ'], trust: ['คนไม่สนับสนุนคุณ', 'แก้ปัญหาให้ประชาชนและลดการโกง'], mood: ['คนไม่มีความสุข', 'ดูงาน อาหาร บ้าน และบริการรัฐ'], hunger: ['คนอดอาหาร', 'เพิ่มไร่นาหรือนำเข้าอาหาร'], jobs: ['คนตกงาน', 'ดึงการลงทุนและสร้างงาน'], prices: ['ของแพง', 'ลดการขาดดุลหรือคุมราคา'], war: ['สงคราม', 'เจรจาสงบศึกหรือเอาชนะให้เร็ว'], army: ['ทหารไม่พอใจ', 'เพิ่มงบกลาโหม'], tax: ['ภาษีสูงเกินไป', 'ลดภาษีหรือใช้จ่ายให้น้อยลง'], corr: ['คอร์รัปชัน', 'เพิ่มงบปราบโกงหรือออกกฎหมาย'], free: ['คนมีการศึกษาเรียกร้องเสรีภาพ', 'เปิดสื่อ ลดการกดขี่ เพิ่มคุณภาพชีวิต'], age: ['ครองอำนาจมานาน คนเริ่มเบื่อ', 'ตั้งทายาทหรือสร้างผลงานใหม่'] };
function throneWhy() {
  const S = G.S, u = S.unrest || 0, L = Object.entries(S.unWhy || {}).filter(q => q[1] >= 1).sort((p, q) => q[1] - p[1]).slice(0, 4), col = u > 65 ? '#b8392c' : u > 40 ? '#d29a2e' : '#27825c';
  return '<div class="lawc"><div class="lawt"><b>บัลลังก์ของคุณ</b><small>ถึง 100% = ถูกโค่นล้ม</small></div>' + bar2('ความไม่สงบ', u / 100, col, Math.round(u) + '%') + (L.length ? L.map(q => '<div class="whyr"><b>' + WHY_N[q[0]][0] + ' +' + Math.round(q[1]) + '</b><span>' + WHY_N[q[0]][1] + '</span></div>').join('') : '<p class="muted">ตอนนี้ยังไม่มีเรื่องน่ากังวล</p>') + '</div>';
}
const countryBase = UI.tab_country;
UI.tab_country = function () {
  UI.ctab = UI.ctab || 'all'; let h = '<div class="chips"><button class="chip ' + (UI.ctab === 'all' ? 'on' : '') + '" data-a="ctab" data-v="all">ภาพรวม</button><button class="chip ' + (UI.ctab === 'prov' ? 'on' : '') + '" data-a="ctab" data-v="prov">จังหวัด (' + G.cities.length + ')</button><button class="chip ' + (UI.ctab === 'life' ? 'on' : '') + '" data-a="ctab" data-v="life">สุขภาพและการตาย</button></div>'; if (UI.ctab === 'life') return h + UI.tab_life(); if (UI.ctab === 'all') return h + throneWhy() + countryBase();
  const S = G.S, P = provs(S), base = Math.max(S.gdp, 700), st = S.x.stage || 0;
  P.forEach((p, i) => { const c = G.cities[i]; if (!c) return; const sh = provShare(i), col = p.un > 65 ? '#b8392c' : p.un > 40 ? '#d29a2e' : '#27825c'; h += '<div class="lawc"><div class="lawt"><b>' + esc(c.name) + (i ? '' : ' (เมืองหลวง)') + '</b><small>' + PROV_T[p.type][0] + ' · ' + fmt(S.x.pop * sh) + ' คน</small></div>' + bar2('ความมั่งคั่ง', p.w, '#2d8fa8', Math.round(p.w * 100)) + bar2('ความไม่พอใจ', p.un / 100, col, Math.round(p.un) + '%') + '<div class="seg s4"><button data-a="pact" data-v="inv:' + i + '" ' + (S.treas < base * .4 ? 'disabled' : '') + '>ลงทุน ' + fmt(base * .4) + '</button><button data-a="pact" data-v="aid:' + i + '" ' + (S.treas < base * .15 ? 'disabled' : '') + '>ช่วยเหลือ ' + fmt(base * .15) + '</button><button data-a="pact" data-v="troop:' + i + '" ' + (S.treas < base * .1 ? 'disabled' : '') + '>ส่งทหาร</button><button data-a="pact" data-v="go:' + i + '">ไปดู</button></div></div>'; });
  const cost = base * 1.5 + 1500; h += '<button class="btn gold" style="width:100%" data-a="newcity" ' + (st < 2 || S.treas < cost || G.cities.length >= 9 ? 'disabled' : '') + '>ก่อตั้งเมืองใหม่ ' + fmt(cost) + ' บาท</button><p class="muted" style="margin-top:5px">' + (st < 2 ? 'ตั้งเมืองใหม่ได้เมื่อเป็นตำบล' : 'จังหวัดที่ถูกทอดทิ้งจะไม่พอใจ และอาจประกาศแยกตัว') + '</p>'; return h;
};
UI.tab_world = function () {
  UI.wtab = UI.wtab || 'news'; let h = '<div class="chips"><button class="chip ' + (UI.wtab === 'news' ? 'on' : '') + '" data-a="wtab" data-v="news">สถานการณ์โลก</button><button class="chip ' + (UI.wtab === 'map' ? 'on' : '') + '" data-a="wtab" data-v="map">เพื่อนบ้าน</button><button class="chip ' + (UI.wtab === 'rank' ? 'on' : '') + '" data-a="wtab" data-v="rank">อันดับโลก</button></div>'; if (UI.wtab === 'news') return h + UI.worldNews(); if (UI.wtab === 'rank') return h + UI.tab_rank();
  const S = G.S, W2 = worldOf(S), me = myPower(S), base = Math.max(S.gdp, 700), F = S.front, relC = r => r > 45 ? '#27825c' : r > 5 ? '#6fa86f' : r > -30 ? '#c79a3a' : '#b8392c';
  let map = '<svg class="wmap" viewBox="0 0 360 150" role="img" aria-label="แผนที่ความสัมพันธ์"><rect width="360" height="150" rx="7" fill="#1d6f8f"/>'; const pos = W2.map((_, i) => { const a = -2.6 + i * (5.2 / (W2.length - 1 || 1)); return [180 + Math.cos(a) * 142, 75 + Math.sin(a) * 54]; });
  W2.forEach((c, i) => { const p = pos[i], war = F && F.c === i; if (war || c.trade || c.ally) map += '<line x1="180" y1="75" x2="' + p[0].toFixed(0) + '" y2="' + p[1].toFixed(0) + '" stroke="' + (war ? '#ff5a45' : c.ally ? '#f5cf73' : '#a8e6c0') + '" stroke-width="' + (war ? 3 : 2) + '" ' + (c.trade && !c.ally && !war ? 'stroke-dasharray="5 4"' : '') + '/>'; });
  map += '<ellipse cx="180" cy="75" rx="30" ry="19" fill="#7fb85a" stroke="#f0dfa8" stroke-width="2"/><text x="180" y="79" text-anchor="middle" font-size="11" font-weight="800" fill="#14263a">เรา</text>'; W2.forEach((c, i) => { const p = pos[i], r = 8 + Math.min(11, c.pow / 11); map += '<circle cx="' + p[0].toFixed(0) + '" cy="' + p[1].toFixed(0) + '" r="' + r.toFixed(0) + '" fill="' + relC(c.rel) + '" stroke="#fff" stroke-width="1.500"/><text x="' + p[0].toFixed(0) + '" y="' + (p[1] + 3.5).toFixed(0) + '" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">' + (i + 1) + '</text>'; }); map += '</svg>'; h += map;
  h += '<div class="kv"><span>กำลังรบของเรา</span><b>' + Math.round(me) + (allyPower(S, -1) ? ' + พันธมิตร ' + Math.round(allyPower(S, -1)) : '') + '</b></div>';
  if (F) { const c = W2[F.c], pct2 = (F.f + 100) / 2; h += '<div class="warbox"><b>กำลังรบกับ ' + c.n + '</b><div class="front"><u style="width:' + pct2 + '%"></u></div><div class="frontl"><span>เราแพ้</span><span>แนวหน้า ' + (F.f >= 0 ? '+' : '') + Math.round(F.f) + '</span><span>เราชนะ</span></div><button class="btn ghost" style="width:100%" data-a="wact" data-v="peace:' + F.c + '" ' + (F.f < -35 ? 'disabled' : '') + '>' + (F.f < -35 ? 'เขาไม่ยอมเจรจาตอนนี้' : 'เจรจาสงบศึก') + '</button></div>'; }
  W2.forEach((c, i) => { const atWar = F && F.c === i, btn = (k, t, off) => '<button data-a="wact" data-v="' + k + ':' + i + '" ' + (off ? 'disabled' : '') + '>' + t + '</button>'; h += '<div class="lawc"><div class="lawt"><b>' + (i + 1) + '. ' + c.n + '</b><small>กำลัง ' + Math.round(c.pow) + (c.ally ? ' · พันธมิตร' : c.trade ? ' · คู่ค้า' : '') + '</small></div>' + bar2('ความสัมพันธ์', (c.rel + 100) / 200, relC(c.rel), Math.round(c.rel)) + '<div class="seg s4">' + btn('gift', 'ส่งของขวัญ', atWar || S.treas < base * .25) + btn('trade', c.trade ? 'เลิกค้า' : 'ทำการค้า', atWar || (!c.trade && c.rel < -5)) + btn('ally', c.ally ? 'เลิกพันธมิตร' : 'พันธมิตร', atWar || (!c.ally && (c.rel < 45 || !c.trade))) + btn('war', 'ประกาศสงคราม', !!F) + '</div></div>'; });
  return h;
};
UI.geoClick = function (a, v) {
  const S = G.S, base = Math.max(S.gdp, 700); if (a === 'ctab') UI.ctab = v; else if (a === 'wtab') UI.wtab = v;
  else if (a === 'newcity') { const cost = base * 1.5 + 1500; if (S.treas >= cost && G.cities.length < 9) { const n = G.cities.length; maybeNewCity(true); if (G.cities.length > n) S.treas -= cost; else news('ไม่มีพื้นที่ราบพอสำหรับเมืองใหม่ ลองถมทะเลก่อน', 'bad'); } }
  else if (a === 'pact') { const [k, q] = v.split(':'), i = +q; if (k === 'go') { W.fly(G.cities[i].x, G.cities[i].z, 34); UI.closeSheet(); return; } const c = k === 'inv' ? .4 : k === 'aid' ? .15 : .1; if (S.treas < base * c) return; S.treas -= base * c; if (k === 'inv') geoFx(S, ['pinv', i, .22]); else if (k === 'aid') geoFx(S, ['pcalm', i, 14]); else { geoFx(S, ['ptroop', i, .7]); applyFx(S, { tr: -1.5 }); } }
  else if (a === 'wact') { const [k, q] = v.split(':'), i = +q, c = worldOf(S)[i];
    if (k === 'gift') { if (S.treas >= base * .25) { S.treas -= base * .25; c.rel = clamp(c.rel + 12, -100, 100); } } else if (k === 'trade') { if (c.trade) { c.trade = 0; c.ally = 0; c.rel -= 8; } else if (c.rel >= -5) { c.trade = 1; c.rel += 4; news('ลงนามการค้ากับ' + c.n, 'good'); } recalcGov(S); }
    else if (k === 'ally') { if (c.ally) { c.ally = 0; c.rel -= 25; } else if (c.rel >= 45 && c.trade) { c.ally = 1; news(c.n + ' เป็นพันธมิตรแล้ว', 'good'); } recalcGov(S); }
    else if (k === 'war') { if (!S.front) { if (UI.warArm !== i) { UI.warArm = i; news('กด "ประกาศสงคราม" อีกครั้งเพื่อยืนยันกับ ' + c.n, 'bad'); return; } UI.warArm = null; startWar(S, i); applyFx(S, { rep: -.06, tension: .05 }); worldOf(S).forEach(q => { if (q !== c) q.rel = clamp(q.rel - 6, -100, 100); }); news('ประกาศสงครามกับ ' + c.n + '!', 'bad'); } }
    else if (k === 'peace' && S.front && S.front.f >= -35) { if (S.front.f < 0) applyFx(S, { c: .6 }); endWar(S, 'peace'); } }
  UI.hud(); UI.render();
};
UI.init();
