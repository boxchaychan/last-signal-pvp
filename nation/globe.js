'use strict';
/* ก่อร่างสร้างชาติ: the world keeps moving by itself. Trouble starts abroad, shows signals first, and hits prices and markets whether or not you answer. Prepare early and it costs less. */
const GE0 = { oil: 1, food: 1, rate: 3, dem: 1, ship: 1, parts: 1, fear: 0 };
const G_STAGE = ['สัญญาณเตือน', 'กำลังลุกลาม', 'รุนแรงเต็มที่', 'เริ่มคลี่คลาย'], G_K = [.1, .55, 1, .35];
const WORLD_EV = [
  { id: 'oilwar', n: 'สงครามในแหล่งน้ำมันโลก', sig: 'กองทัพสองฝ่ายเผชิญหน้ากันใกล้แหล่งน้ำมัน', hit: 'น้ำมัน ค่าไฟ และค่าขนส่งแพงขึ้น', fx: { oil: .85, ship: .2, fear: .18 }, len: [10, 22], prep: 'oil' },
  { id: 'strait', n: 'เส้นทางเดินเรือหลักถูกปิด', sig: 'เรือสินค้าถูกโจมตีในช่องแคบ บริษัทเรือเริ่มเลี่ยงเส้นทาง', hit: 'ค่าระวางเรือพุ่ง ของนำเข้าช้าและแพง', fx: { ship: 1.15, oil: .18 }, len: [6, 14], prep: 'parts' },
  { id: 'ratehike', n: 'ธนาคารกลางใหญ่ขึ้นดอกเบี้ย', sig: 'เงินเฟ้อในประเทศมหาอำนาจสูงเกินเป้า', hit: 'ดอกเบี้ยหนี้สูงขึ้น เงินทุนไหลออก', fx: { rate: 3.5, fear: .28, dem: -.06 }, len: [18, 36], prep: 'fx' },
  { id: 'bubble', n: 'ฟองสบู่การเงินโลกแตก', sig: 'ราคาหุ้นและอสังหาในหลายประเทศสูงผิดปกติ', hit: 'คำสั่งซื้อหาย ธุรกิจปลดคน เงินทุนหนี', fx: { dem: -.28, fear: .5, rate: -.8 }, len: [14, 30], prep: 'fx' },
  { id: 'pandemic', n: 'โรคอุบัติใหม่ระบาดทั่วโลก', sig: 'พบผู้ป่วยโรคปอดแปลกๆ ในต่างประเทศ', hit: 'การค้าสะดุด และเชื้อเข้าประเทศผ่านท่าเรือกับสนามบิน', fx: { dem: -.18, ship: .4, fear: .22, epi: 1 }, len: [14, 30], prep: 'med' },
  { id: 'elnino', n: 'เอลนีโญรุนแรง', sig: 'น้ำทะเลแปซิฟิกอุ่นผิดปกติ', hit: 'ฝนน้อย ข้าวทั่วโลกแพง', fx: { food: .35, rain: -.38 }, len: [10, 18], prep: 'food' },
  { id: 'lanina', n: 'ลานีญาฝนหนักทั้งภูมิภาค', sig: 'นักอุตุฯ เตือนว่าปีนี้ฝนจะมากกว่าปกติ', hit: 'แม่น้ำสูง เสี่ยงน้ำท่วม', fx: { rain: .42, food: .12 }, len: [8, 16], prep: 'food' },
  { id: 'foodban', n: 'ประเทศผู้ส่งออกห้ามส่งออกอาหาร', sig: 'ผลผลิตธัญพืชโลกต่ำ หลายประเทศเริ่มกักตุน', hit: 'ราคาอาหารโลกพุ่ง ประเทศที่ซื้ออาหารเดือดร้อน', fx: { food: .75 }, len: [6, 14], prep: 'food' },
  { id: 'tradewar', n: 'สงครามการค้าของมหาอำนาจ', sig: 'มหาอำนาจขู่ตั้งกำแพงภาษีใส่กัน', hit: 'ส่งออกยากขึ้น แต่บางบริษัทหาฐานผลิตใหม่', fx: { dem: -.12, ship: .15, shift: .1 }, len: [24, 48], prep: 'market' },
  { id: 'chips', n: 'ชิปและชิ้นส่วนขาดตลาด', sig: 'โรงงานชิปหลักประกาศลดการผลิต', hit: 'โรงงานเครื่องจักรและประกอบสินค้าต้องหยุดเป็นช่วง', fx: { parts: .75 }, len: [12, 26], prep: 'parts' },
  { id: 'fert', n: 'ปุ๋ยและพลังงานแพงทั่วโลก', sig: 'ก๊าซธรรมชาติแพงขึ้น โรงงานปุ๋ยลดกำลังผลิต', hit: 'ต้นทุนชาวนาสูง ข้าวแพง', fx: { food: .3, oil: .25 }, len: [8, 16], prep: 'food' },
  { id: 'refugee', n: 'คลื่นผู้ลี้ภัยในภูมิภาค', sig: 'การสู้รบในประเทศใกล้เคียงรุนแรงขึ้น', hit: 'คนหนีตายเข้าประเทศ งานและบ้านตึงตัว', fx: { refugee: 1, fear: .1 }, len: [8, 18], prep: 'med' },
  { id: 'lowcost', n: 'ประเทศค่าแรงต่ำเปิดรับนักลงทุน', sig: 'เพื่อนบ้านเซ็นข้อตกลงการค้าและเสนอที่ดินฟรี', hit: 'โรงงานที่หาแรงงานถูกเริ่มพิจารณาย้ายฐาน', fx: { rival: .16 }, len: [60, 120], prep: 'skill' },
  { id: 'robot', n: 'AI และหุ่นยนต์แทนแรงงาน', sig: 'บริษัทใหญ่ทั่วโลกเริ่มเปลี่ยนสายการผลิตเป็นอัตโนมัติ', hit: 'งานใช้แรงงานลดลง ต้องการคนมีทักษะมากขึ้น', fx: { auto: .25 }, len: [60, 100], prep: 'skill' },
  { id: 'misinfo', n: 'ข่าวปลอมและความแตกแยกทั่วโลก', sig: 'แพลตฟอร์มออนไลน์เต็มไปด้วยคลิปปลอม', hit: 'คนเชื่อรัฐน้อยลง ความไม่สงบเพิ่มขึ้น', fx: { unrest: .1 }, len: [18, 36], prep: 'skill' }
];
function globeOf(S) { if (!S.g) S.g = { oil: 1, food: 1, rate: 3, dem: 1, ship: 1, parts: 1, fear: 0, rain: 0, rival: 0, shift: 0, auto: 0, epiK: 0, unrestK: 0, refugee: 0, on: [], next: 16 + Math.random() * 14 | 0, log: [], fix: 0, st: { oil: 0, fx: 0, med: 0, parts: 0, market: 0 }, e: Object.assign({}, GE0) }; return S.g; }
const gNews = (t, k) => { if (typeof news === 'function') news(t, k); };
function globeMonth(S) {
  const g = globeOf(S), x = S.x;
  if (S.m >= g.next && g.on.length < 2) { const e = pickStory(S, g); g.next = S.m + (e ? 34 + Math.random() * 40 : 8 + Math.random() * 8) | 0; if (e) { g.on.push({ id: e.id, st: 0, left: 4 + Math.random() * 6 | 0, len: e.len[0] + Math.random() * (e.len[1] - e.len[0]) | 0, real: Math.random() > .26 }); gNews('สัญญาณโลก: ' + e.sig); } }
  const T = { oil: 0, food: 0, rate: 0, dem: 0, ship: 0, parts: 0, fear: 0, rain: 0, rival: 0, shift: 0, auto: 0, epi: 0, unrest: 0, refugee: 0 };
  for (let i = g.on.length - 1; i >= 0; i--) {
    const q = g.on[i], d = WORLD_EV.find(v => v.id === q.id); if (!d) { g.on.splice(i, 1); continue; } if (q.st < 2) { const no = whyNot(S, d); if (no) { gNews(d.n + ' ไม่เกิดกับเรา เพราะ' + no, 'good'); g.on.splice(i, 1); continue; } } if (--q.left <= 0) {
      if (q.st === 0 && !q.real) { gNews('สัญญาณนี้ซาลงแล้ว ยังไม่เกิด' + d.n, 'good'); g.on.splice(i, 1); continue; }
      q.st++; if (q.st > 3) { gNews('โลกคลี่คลาย: ' + d.n, 'good'); g.on.splice(i, 1); histEnd(S, q, d); continue; } if (q.st === 2) histHit(S, q, d);
      q.left = Math.max(2, Math.round(q.len * [0, .3, .45, .25][q.st])); if (q.st === 1) gNews('ข่าวโลก: ' + d.n + ' กำลังลุกลาม ' + d.hit, 'bad');
    }
    const k = G_K[q.st]; for (const f in d.fx) T[f] += d.fx[f] * k;
  }
  const ease = (f, base) => { g[f] += (base + T[f] - g[f]) * .25; }; ease('oil', 1); ease('food', 1); ease('rate', 3); ease('dem', 1); ease('ship', 1); ease('parts', 1); ease('fear', 0); ease('rain', 0); ease('shift', 0); g.rival += (T.rival - g.rival) * .05; g.auto += (T.auto - g.auto) * .03; g.epiK = T.epi; g.unrestK = T.unrest; g.refugee = T.refugee; g.rate = Math.max(.8, g.rate); g.dem = clamp(g.dem, .4, 1.1); g.fear = clamp(g.fear);
  /* what you prepared absorbs the shock, then runs out */
  const st = g.st; let oilCut = 0, partCut = 0; if (g.oil > 1.1 && st.oil > 0) { oilCut = .72; st.oil = Math.max(0, st.oil - 1); } if ((g.parts > 1.1 || g.ship > 1.25) && st.parts > 0) { partCut = .7; st.parts = Math.max(0, st.parts - 1); } const fx = st.fx, mk = st.market; if (g.fear > .05 && fx > 0) st.fx = Math.max(0, fx - .012); st.med *= .996; st.market *= .998; g.fix *= .994;
  g.e = { oil: 1 + (g.oil - 1) * (1 - oilCut), food: g.food, rate: 3 + (g.rate - 3) * (1 - g.fix), dem: 1 + (g.dem - 1) * (1 - mk * .55), ship: 1 + (g.ship - 1) * (1 - partCut) * (1 - mk * .4), parts: 1 + (g.parts - 1) * (1 - partCut), fear: g.fear * (1 - fx * .75) };
  /* things that reach people directly */
  if (g.epiK > .2) { const door = 1 + Math.min(S.k.port || 0, 3) * .5 + Math.min(S.k.air || 0, 2) * .8; S.epi = clamp(S.epi + .006 * g.epiK * door * (1 - st.med * .8), 0, .12); }
  if (g.refugee > .2 && x.pop > 60) applyFx(S, { pop: .0035 * g.refugee, crime: .0015 * g.refugee, tension: .0006 }); if (g.unrestK > 0) S.unrestAdj = (S.unrestAdj || 0) + g.unrestK * .5;
  if (g.auto > .03 && (x.stage || 0) >= 4) { const f = 1 - .0009 * g.auto; S.k.ind *= f; S.k.svc *= f; S.tech += .00006 * g.auto; }
}
const G_PREP = {
  oil: { n: 'สำรองน้ำมัน 6 เดือน', d: 'ราคาน้ำมันโลกพุ่งแล้วไม่กระทบเต็มๆ', cost: (S, g) => Math.max(S.gdp, 500) * .22 * g.oil, ok: g => g.st.oil < 12, val: g => g.st.oil.toFixed(0) + ' เดือน' },
  food: { n: 'สำรองข้าวเพิ่ม 3 เดือน', d: 'ซื้อตอนราคาปกติถูกกว่าตอนขาดตลาดมาก', cost: (S, g) => Math.max(S.x.pop, 10) * 3 * S.pFood * .5 * g.food, ok: (g, S) => S.x.foodMonths < 4.6, val: (g, S) => S.x.foodMonths.toFixed(1) + ' เดือน' },
  fx: { n: 'เพิ่มทุนสำรอง', d: 'กันเงินทุนไหลออกตอนโลกตื่นตระหนก', cost: S => Math.max(S.gdp, 500) * 1.1, ok: g => g.st.fx < .95, val: g => pct(g.st.fx) },
  debt: { n: 'แปลงหนี้เป็นดอกเบี้ยคงที่', d: 'เสียค่าธรรมเนียมตอนนี้ แต่ดอกเบี้ยโลกขึ้นไม่กระทบ', cost: S => Math.max(50, S.debt * .025), ok: (g, S) => S.debt > 100 && g.fix < .9, val: g => pct(g.fix) },
  med: { n: 'ตั้งระบบเฝ้าระวังโรค', d: 'ตรวจเจอเร็ว มีหน้ากาก ยา และเตียงสำรอง', cost: S => Math.max(S.gdp, 500) * .4, ok: g => g.st.med < .95, val: g => pct(g.st.med) },
  parts: { n: 'สำรองชิ้นส่วน 6 เดือน', d: 'โรงงานเดินต่อได้ตอนเรือและชิปขาด', cost: (S, g) => Math.max(S.gdp, 500) * .3 * Math.max(g.ship, g.parts), ok: g => g.st.parts < 12, val: g => g.st.parts.toFixed(0) + ' เดือน' },
  market: { n: 'กระจายตลาดและคู่ค้า', d: 'ไม่พึ่งลูกค้าประเทศเดียว ค่อยๆ หมดผลถ้าไม่ลงทุนต่อ', cost: S => Math.max(S.gdp, 500) * .6, ok: g => g.st.market < .95, val: g => pct(g.st.market) }
};
function globePrep(S, k) { const g = globeOf(S), st = g.st; if (k === 'oil') st.oil = Math.min(12, st.oil + 6); else if (k === 'food') S.food += Math.max(S.x.pop, 10) * 3; else if (k === 'fx') st.fx = Math.min(1, st.fx + .3); else if (k === 'debt') g.fix = Math.min(1, g.fix + .4); else if (k === 'med') st.med = Math.min(1, st.med + .45); else if (k === 'parts') st.parts = Math.min(12, st.parts + 6); else if (k === 'market') st.market = Math.min(1, st.market + .35); }
