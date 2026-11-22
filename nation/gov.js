'use strict';
/* ก่อร่างสร้างชาติ: laws, ministers and problems that grow into longer stories. */
const POSTS = { fin: ['คลัง', 1], int: ['มหาดไทย', 1], edu: ['ศึกษาธิการ', 2], hea: ['สาธารณสุข', 2], def: ['กลาโหม', 3], dip: ['ต่างประเทศ', 3] };
const LAW_N = { edu: 'การศึกษา', hq: 'สาธารณสุข', happy: 'ความสุข', trust: 'แรงสนับสนุน', unrest: 'ความไม่สงบ', crime: 'อาชญากรรม', corr: 'คอร์รัปชัน', gini: 'เหลื่อมล้ำ', pol: 'มลพิษ', rep: 'ชื่อเสียงโลก', prod: 'ผลผลิต', priv: 'การลงทุน', tech: 'เทคโนโลยี', tfr: 'อัตราเกิด', inM: 'คนย้ายเข้า', outM: 'คนย้ายออก', rev: 'รายได้ภาษี', infl: 'เงินเฟ้อ', food: 'อาหาร', forest: 'ป่าไม้', tension: 'ความตึงเครียด', army: 'กำลังทหาร' };
const LAW_BAD = { unrest: 1, crime: 1, corr: 1, gini: 1, pol: 1, infl: 1, tension: 1, outM: 1 };
/* name, group, stage, one-time cost (months of GDP), yearly-free upkeep (% of GDP), effects */
const LAWS = {
  freeschool: ['เรียนฟรีถึงมัธยม', 'สังคม', 1, .3, .7, { edu: .16, happy: 2, gini: -.012 }],
  forceschool: ['บังคับเด็กทุกคนเรียน', 'สังคม', 2, .15, .25, { edu: .1, unrest: 1.5 }],
  freehealth: ['รักษาฟรีถ้วนหน้า', 'สังคม', 2, .4, .9, { hq: 7, happy: 3, gini: -.012 }],
  pension: ['บำนาญผู้สูงอายุ', 'สังคม', 3, .3, .7, { happy: 2.5, trust: 2, gini: -.01 }],
  minwage: ['ค่าแรงขั้นต่ำ', 'สังคม', 2, .1, 0, { gini: -.025, happy: 2, priv: -.12, infl: .0006 }],
  babybonus: ['เงินอุดหนุนมีลูก', 'สังคม', 3, .2, .4, { tfr: .32, happy: 1 }],
  onechild: ['จำกัดจำนวนลูก', 'สังคม', 3, .1, .05, { tfr: -.8, unrest: 3, trust: -3 }],
  antidrug: ['ปราบยาเสพติดเด็ดขาด', 'สังคม', 2, .2, .15, { crime: -.025, rep: -.012 }],
  freezone: ['เขตเศรษฐกิจพิเศษ', 'เศรษฐกิจ', 3, .6, 0, { prod: .05, priv: .2, gini: .022 }],
  foreigninv: ['เปิดรับนักลงทุนต่างชาติ', 'เศรษฐกิจ', 2, .15, 0, { priv: .24, rep: .03, gini: .012 }],
  pricecap: ['คุมราคาสินค้า', 'เศรษฐกิจ', 2, .1, .12, { infl: -.0016, happy: 1.5, priv: -.14, food: -.04 }],
  landreform: ['ปฏิรูปที่ดินให้ชาวนา', 'เศรษฐกิจ', 1, .35, 0, { food: .1, gini: -.03, priv: -.06, trust: 2 }],
  research: ['ทุนวิจัยแห่งชาติ', 'เศรษฐกิจ', 4, .4, .45, { tech: .007, rep: .012 }],
  openlabor: ['เปิดรับแรงงานต่างชาติ', 'เศรษฐกิจ', 2, .05, 0, { inM: .4, tension: .012, gini: .008 }],
  closeborder: ['ปิดพรมแดน ห้ามคนออก', 'เศรษฐกิจ', 3, .2, .1, { outM: -.75, inM: -.5, rep: -.07, unrest: 2 }],
  forestlaw: ['เขตอนุรักษ์ป่า', 'สิ่งแวดล้อม', 2, .2, .08, { forest: .05, pol: -.018, priv: -.05 }],
  noburn: ['ห้ามเผาในที่โล่ง', 'สิ่งแวดล้อม', 1, .05, .04, { pol: -.016, happy: .5, food: -.015 }],
  carbontax: ['ภาษีคาร์บอน', 'สิ่งแวดล้อม', 4, .1, 0, { pol: -.035, rev: .025, priv: -.1, rep: .025 }],
  conscription: ['เกณฑ์ทหาร', 'อำนาจ', 3, .2, .2, { army: .3, prod: -.018, unrest: 1.5, tension: -.008 }],
  curfew: ['เคอร์ฟิวทั้งประเทศ', 'อำนาจ', 2, .05, .05, { crime: -.04, unrest: -3, happy: -5, prod: -.035 }],
  nomeeting: ['ห้ามชุมนุม', 'อำนาจ', 2, .05, .05, { unrest: -6, trust: -5, rep: -.05 }],
  censorship: ['ควบคุมสื่อ', 'อำนาจ', 2, .1, .08, { unrest: -4, trust: 1, rep: -.06, corr: .02 }],
  secretpolice: ['ตำรวจลับ', 'อำนาจ', 3, .4, .35, { unrest: -9, crime: -.02, trust: -6, rep: -.08, happy: -2 }],
  anticorrupt: ['ศาลพิเศษคดีโกง', 'อำนาจ', 3, .25, .12, { corr: -.04, trust: 3 }]
};
const LAW_GROUPS = ['สังคม', 'เศรษฐกิจ', 'สิ่งแวดล้อม', 'อำนาจ'];
/* strength of a law: the good part grows slowly, the bad part grows fast, so "very strong" always has a price */
const LAW_LV = ['ปิด', 'น้อย', 'กลาง', 'แรง', 'แรงมาก'], LV_GOOD = [0, .5, 1, 1.4, 1.75], LV_BAD = [0, .35, 1, 1.8, 2.9], LV_COST = [0, .6, 1, 1.5, 2.2];
const lawScale = (k, v, lv) => v * ((LAW_BAD[k] ? v > 0 : v < 0) ? LV_BAD[lv] : LV_GOOD[lv]);
function setLaw(S, id, lv) {
  const l = LAWS[id], old = +(S.laws[id] || 0); if (old === lv) return true; const base = l[3] * Math.max(S.gdp, 700), pay = Math.max(0, (LV_COST[lv] - LV_COST[old]) * base);
  if (S.treas < pay) { news('เงินคลังไม่พอ ต้องใช้ ' + fmt(pay) + ' บาท', 'bad'); return false; } S.treas -= pay; S.laws[id] = lv;
  if (lv < old) applyFx(S, { unrest: l[1] === 'อำนาจ' ? -.4 * (old - lv) : .6 * (old - lv) });
  news(lv ? 'กฎหมาย' + l[0] + ': ระดับ' + LAW_LV[lv] : 'ยกเลิกกฎหมาย: ' + l[0], lv > old ? 'good' : ''); recalcGov(S); return true;
}

function newCandidate() {
  const sex = Math.random() < .5 ? 1 : 0, roll = () => Math.round(2 + Math.random() * 8), q = { n: (sex ? pick(F_NAMES) : pick(M_NAMES)) + ' ' + pick(LAST_NAMES), sk: roll(), lo: roll(), gr: roll() };
  q.tag = q.sk >= 8 && q.gr >= 7 ? 'เก่งแต่โลภ' : q.sk >= 8 && q.lo <= 4 ? 'เก่งแต่ไว้ใจไม่ได้' : q.sk >= 8 ? 'คนเก่ง' : q.lo >= 8 && q.sk <= 4 ? 'ภักดีแต่ไม่เก่ง' : q.gr >= 8 ? 'ชอบเงิน' : q.lo >= 8 ? 'ผู้ภักดี' : q.gr <= 3 ? 'มือสะอาด' : 'คนทั่วไป'; return q;
}
function postOpen(S, p) { return (S.stageMax || 0) >= POSTS[p][1]; }
function ensureCands(S) { S.cands = S.cands || {}; S.gov = S.gov || {}; for (const p in POSTS) if (postOpen(S, p) && (!S.cands[p] || S.cands[p].length < 3)) { S.cands[p] = S.cands[p] || []; while (S.cands[p].length < 3) S.cands[p].push(newCandidate()); } }
/* every law and minister feeds one list of modifiers that the country model reads */
function recalcGov(S) {
  S.laws = S.laws || {}; S.gov = S.gov || {}; const L = {}, add = (k, v) => { L[k] = (L[k] || 0) + v; }; let up = 0;
  for (const id in S.laws) { const l = LAWS[id], lv = +S.laws[id]; if (!l || !lv) continue; up += l[4] * LV_COST[lv]; for (const k in l[5]) add(k, lawScale(k, l[5][k], lv)); }
  let gMax = 0, gWho = null, loDef = null;
  for (const p in POSTS) {
    const m = S.gov[p]; if (!postOpen(S, p)) continue; if (!m) { add('rev', -.006); add('unrest', .25); continue; } const s = m.sk - 5, g = m.gr - 4;
    up += .05; add('corr', Math.max(-.006, g * .004)); add('unrest', (5 - m.lo) * .25); if (m.gr > gMax) { gMax = m.gr; gWho = p; }
    if (p === 'fin') add('rev', s * .012); else if (p === 'int') { add('crime', -s * .006); add('unrest', -(m.lo - 5) * .4); } else if (p === 'edu') add('edu', s * .018); else if (p === 'hea') add('hq', s * .9); else if (p === 'def') { add('army', s * .04); add('unrest', (5 - m.lo) * .6); loDef = m.lo; } else if (p === 'dip') { add('rep', s * .005); add('tension', -s * .004); }
  }
  L.upkeep = up; S.lawMod = L; S.govStat = { gMax, gWho, loDef };
}
function govFire(S, who) { const p = who === 'graft' ? S.govStat && S.govStat.gWho : who; if (!p || !S.gov[p]) return; const m = S.gov[p]; S.gov[p] = null; S.cands = S.cands || {}; S.cands[p] = []; ensureCands(S); recalcGov(S); if (typeof news === 'function') news('ปลด' + m.n + ' ออกจากรัฐมนตรี' + POSTS[p][0], 'bad'); }
function govLoy(S, p) { const m = S.gov && S.gov[p]; if (m) { m.lo = Math.min(10, m.lo + 3); recalcGov(S); } }

/* ---------- stories: an answer today comes back months later ---------- */
const never = () => false;
E('bribe_leak', 'การเมือง', 0, never, 0, 'นักข่าวได้คลิปเงินใต้โต๊ะ', 'มีคลิปคุณรับเงินจากผู้รับเหมา และเขาขู่จะปล่อยในสัปดาห์นี้', [['จ่ายเงินปิดข่าว', { c: .5, corr: .02, next: [14, 'bribe_trial'] }], ['ออกมาขอโทษเอง', { tr: -6, corr: -.03, unrest: 3 }], ['สั่งจับนักข่าว', { unrest: 5, rep: -.06, next: [6, 'bribe_trial'] }]]);
E('bribe_trial', 'การเมือง', 0, never, 0, 'คดีโกงลุกลามถึงคนในรัฐบาล', 'หลักฐานชุดใหม่โผล่มา คนทั้งประเทศจับตาว่าคุณจะทำอย่างไร', [['ตั้งศาลพิเศษ สอบทุกคน', { c: .3, corr: -.05, tr: 6, unrest: -3 }], ['โยนความผิดให้รัฐมนตรี', { fire: 'graft', tr: -2, corr: -.01 }], ['ปิดคดี', { tr: -12, unrest: 10, corr: .04 }]]);
E('river_poison', 'สิ่งแวดล้อม', 0, never, 0, 'แม่น้ำเป็นพิษทั้งสาย', 'ปลาตายยกแม่น้ำ น้ำประปาเริ่มมีกลิ่น เด็กหลายคนป่วย', [['ปิดโรงงานจนกว่าจะแก้เสร็จ', { priv: -.6, pol: -.08, tr: 5 }], ['สร้างระบบบำบัดด้วยเงินรัฐ', { c: 1, pol: -.09 }], ['บอกว่าน้ำยังปลอดภัย', { sick: .04, tr: -8, next: [8, 'class_action'] }]]);
E('class_action', 'สิ่งแวดล้อม', 0, never, 0, 'ชาวบ้านทั้งลุ่มน้ำรวมตัวฟ้อง', 'ผลตรวจเลือดออกมาตรงกัน และองค์กรต่างชาติเริ่มสนใจคดีนี้', [['ชดเชยทุกครอบครัว', { c: 1.3, tr: 8, unrest: -6 }], ['เจรจาเป็นรายคน', { c: .5, tr: -2 }], ['ห้ามรายงานข่าว', { unrest: 9, rep: -.09, tr: -7 }]]);
E('famine', 'อาหาร', 0, never, 0, 'ความอดอยากเริ่มขึ้น', 'ยุ้งฉางว่างเปล่าหลายหมู่บ้าน ผู้คนเริ่มเดินเข้าเมืองเพื่อหาอาหาร', [['ซื้อข้าวฉุกเฉินทุกราคา', { c: 1.1, food: 1.6, tr: 4 }], ['ปันส่วนอาหารทั้งประเทศ', { food: .5, hp: -4, unrest: 3 }], ['ปิดข่าว รอฤดูหน้า', { food: -.5, sick: .03, pop: -.02, next: [3, 'hunger_march'] }]]);
E('hunger_march', 'ความมั่นคง', 0, never, 0, 'ขบวนคนหิวเดินเข้าเมืองหลวง', 'หลายพันคนถือหม้อเปล่าเดินมุ่งหน้าสู่ทำเนียบของคุณ', [['เปิดคลังแจกอาหาร', { c: .7, food: .9, unrest: -14, tr: 6 }], ['รับตัวแทนมาเจรจา', { unrest: -5, tr: 2 }], ['สั่งทหารขวาง', { unrest: 8, tr: -14, rep: -.09, next: [5, 'martyr'] }]]);
E('martyr', 'ความมั่นคง', 0, never, 0, 'นักศึกษาเสียชีวิตในการชุมนุม', 'ภาพสุดท้ายของเธอแพร่ไปทั่วโลก ผู้คนเริ่มเรียกเธอว่าวีรชน', [['ขอโทษและตั้งกรรมการสอบ', { tr: 5, unrest: -11, rep: .03 }], ['จ่ายเงินเยียวยาครอบครัว', { c: .2, unrest: -3 }], ['กล่าวหาว่าเป็นผู้ก่อการร้าย', { tr: -10, rep: -.08, unrest: 8, next: [4, 'general_strike'] }]]);
E('general_strike', 'ความมั่นคง', 0, never, 0, 'นัดหยุดงานทั่วประเทศ', 'ร้านปิด โรงงานหยุด รถไม่วิ่ง คนทั้งประเทศบอกว่าจะไม่ทำงานจนกว่าคุณจะยอม', [['ยอมปฏิรูปครั้งใหญ่', { tax: -3, tr: 12, unrest: -30, corr: -.02 }], ['ขึ้นค่าแรงทั่วประเทศ', { priv: -.7, gini: -.03, unrest: -16, infl: .012 }], ['ประกาศกฎอัยการศึก', { priv: -.6, unrest: 6, rep: -.12, tr: -12, next: [5, 'coup_attempt'] }]]);
E('coup_attempt', 'ความมั่นคง', 0, never, 0, 'รถถังเคลื่อนเข้าเมืองหลวง!', 'นายทหารกลุ่มหนึ่งยึดสถานีวิทยุและประกาศว่าจะล้มรัฐบาลของคุณคืนนี้', [['สั่งหน่วยที่ภักดีสู้กลับ', { c: .8, unrest: -18, pop: -.004, tr: -3 }], ['เจรจา แบ่งอำนาจให้กองทัพ', { c: .4, unrest: -9, corr: .05, bud: -.05 }], ['ออกทีวีขอให้ประชาชนช่วย', { unrest: 12, tr: 5 }]]);
E('investor_leaves', 'เศรษฐกิจ', 0, never, 0, 'บริษัทต่างชาติขู่ย้ายฐาน', 'พอหมดสิทธิภาษี เขาบอกว่าจะย้ายโรงงานไปประเทศอื่น คนนับพันอาจตกงาน', [['ต่อสิทธิภาษีให้', { priv: .2, tr: -3, gini: .012 }], ['ซื้อกิจการมาเป็นของรัฐ', { c: 1.2, priv: -.3, tr: 3 }], ['ปล่อยให้ไป', { priv: -.8, rep: -.015 }]]);
E('creditors', 'เศรษฐกิจ', 0, never, 0, 'เจ้าหนี้ต่างชาติมาทวงเงิน', 'เขาเสนอขอเช่าท่าเรือและเหมืองของประเทศ 99 ปีแทนการใช้หนี้', [['ยอมให้เช่า', { debt: -.45, rep: -.03, tr: -8, tension: .03 }], ['ตัดงบทุกกระทรวงเพื่อใช้หนี้', { debt: -.3, bud: -.12, unrest: 6 }], ['ไม่จ่าย', { rep: -.14, priv: -.7, tension: .08 }]]);
E('slum_fire', 'ภัยพิบัติ', 0, never, 0, 'ไฟไหม้สลัมกลางเมือง', 'บ้านสังกะสีไหม้เป็นแถวในชั่วโมงเดียว ผู้คนนับร้อยไม่มีที่อยู่', [['สร้างแฟลตให้ทุกคน', { c: 1, build: 'auto_house', tr: 7, unrest: -5 }], ['แจกเต็นท์และอาหาร', { c: .3, hp: -1 }], ['ยึดที่ให้นายทุนสร้างห้าง', { priv: .5, gini: .03, unrest: 11, tr: -8 }]]);
E('underground', 'การเมือง', 0, never, 0, 'หนังสือพิมพ์ใต้ดินแพร่ทั่วเมือง', 'ยิ่งปิดสื่อ คนยิ่งอยากอ่าน ใบปลิวด่ารัฐบาลโผล่ทุกตลาด', [['เปิดให้สื่อกลับมา', { tr: 5, unrest: -6, rep: .05 }], ['ตามจับคนพิมพ์', { c: .2, unrest: 2, rep: -.03 }], ['ปล่อยข่าวลวงกลับ', { tr: -4, corr: .012 }]]);
E('sea_dead', 'สิ่งแวดล้อม', 0, never, 0, 'ทะเลรอบเกาะเริ่มตาย', 'ปะการังขาวโพลน ปลาหายไป นักท่องเที่ยวและชาวประมงหายตามไปด้วย', [['ฟื้นฟูทะเลครั้งใหญ่', { c: 1, pol: -.06, rep: .05, tr: 3 }], ['ห้ามจับปลาชั่วคราว', { food: -.4, pol: -.03, unrest: 2 }], ['ถมต่อ เศรษฐกิจสำคัญกว่า', { priv: .3, pol: .05, rep: -.05, tr: -4 }]]);
E('minister_graft', 'การเมือง', 20, x => x.gMax >= 8, 4, 'รัฐมนตรีของคุณโกงงบ', 'สำนักตรวจเงินพบเงินหายจากกระทรวง และเส้นทางเงินไปถึงตัวรัฐมนตรี', [['ปลดและดำเนินคดี', { fire: 'graft', corr: -.03, tr: 3 }], ['ตักเตือนเป็นการภายใน', { corr: .012 }], ['ช่วยปิดข่าว', { corr: .03, later: [9, { tr: -8 }, 'ข่าวรัฐมนตรีโกงงบรั่วออกมา'] }]]);
E('minister_betray', 'ความมั่นคง', 100, x => x.loDef != null && x.loDef <= 3 && x.m > 36, 4, 'รัฐมนตรีกลาโหมแอบพบนายพล', 'สายลับรายงานว่าเขากำลังถามนายทหารว่าใครจะอยู่ข้างเขา ถ้าเกิดอะไรขึ้นกับคุณ', [['ปลดทันที', { fire: 'def', unrest: 4 }], ['ขึ้นเงินเดือนซื้อใจ', { c: .5, loy: 'def' }], ['เฝ้าดูไว้ก่อน', { unrest: 10, next: [5, 'coup_attempt'] }]]);
const chain = (id, o, m, nx) => { const e = EV.find(q => q.id === id); if (e && e.o[o]) e.o[o][1].next = [m, nx]; };
chain('corrupt', 2, 7, 'bribe_leak'); chain('factory_waste', 2, 8, 'river_poison'); chain('drought', 2, 4, 'famine'); chain('uprising', 2, 6, 'martyr'); chain('investor', 0, 34, 'investor_leaves'); chain('deficit', 2, 14, 'creditors'); chain('overpop', 2, 9, 'slum_fire'); chain('press', 2, 12, 'underground'); chain('coup_plot', 2, 4, 'coup_attempt'); chain('fishers', 2, 12, 'sea_dead'); chain('food_price', 2, 6, 'famine'); chain('strike', 2, 5, 'martyr');

/* ---------- government folder ---------- */
const lawChips = (m, up, lv) => { const shown = lv || 2, mark = k => { const f = Math.abs(lawScale(k, m[k], shown) / m[k]), a = m[k] > 0 ? '▲' : '▼'; return f > 1.6 ? a + a + a : f > 1.05 ? a + a : a; }; return '<div class="fx">' + Object.keys(m).map(k => { const bad = LAW_BAD[k], good = bad ? m[k] < 0 : m[k] > 0; return '<span class="' + (good ? 'g' : 'r') + '">' + LAW_N[k] + ' ' + mark(k) + '</span>'; }).join('') + (up ? '<span class="r">งบประจำ ' + (up * LV_COST[shown]).toFixed(2) + '% GDP</span>' : '') + '</div>'; };
const pips = (v, col) => '<i class="pips">' + Array.from({ length: 10 }, (_, i) => '<u style="background:' + (i < v ? col : '#e3d8c1') + '"></u>').join('') + '</i>';
UI.tab_gov = function () {
  const S = G.S; ensureCands(S); UI.govTab = UI.govTab || 'min'; let h = '<div class="chips"><button class="chip ' + (UI.govTab === 'min' ? 'on' : '') + '" data-a="gtab" data-v="min">รัฐมนตรี</button><button class="chip ' + (UI.govTab === 'law' ? 'on' : '') + '" data-a="gtab" data-v="law">กฎหมาย (' + Object.values(S.laws || {}).filter(Boolean).length + ')</button></div>';
  if (UI.govTab === 'min') {
    for (const p in POSTS) {
      const on = postOpen(S, p), m = S.gov[p]; h += '<h3>กระทรวง' + POSTS[p][0] + '</h3>'; if (!on) { h += '<p class="muted">เปิดเมื่อเป็น' + STAGES[POSTS[p][1]].n + '</p>'; continue; }
      if (m) h += '<div class="mincard"><div><b>' + esc(m.n) + '</b> <small>' + m.tag + '</small><div class="pipr">ฝีมือ ' + pips(m.sk, '#27825c') + '</div><div class="pipr">ภักดี ' + pips(m.lo, '#2d4a69') + '</div><div class="pipr">โลภ ' + pips(m.gr, '#b8392c') + '</div></div><button class="btn ghost" data-a="mfire" data-v="' + p + '">ปลด</button></div>';
      else h += '<p class="muted" style="color:var(--red)">ยังไม่มีรัฐมนตรี เลือกจากผู้สมัคร:</p>' + S.cands[p].map((c, i) => '<button class="mincard pick" data-a="mhire" data-v="' + p + ':' + i + '"><div><b>' + esc(c.n) + '</b> <small>' + c.tag + '</small><div class="pipr">ฝีมือ ' + pips(c.sk, '#27825c') + '</div><div class="pipr">ภักดี ' + pips(c.lo, '#2d4a69') + '</div><div class="pipr">โลภ ' + pips(c.gr, '#b8392c') + '</div></div></button>').join('');
    }
    return h + '<p class="muted" style="margin-top:7px">คนเก่งอาจโลภหรือไม่ภักดี ถ้ารัฐมนตรีกลาโหมไม่ภักดี อาจเกิดรัฐประหาร</p>';
  }
  const st = S.x.stage || 0; h += '<p class="muted">ยิ่งแรงยิ่งได้ผล แต่ผลเสียจะเพิ่มเร็วกว่า</p>';
  for (const g of LAW_GROUPS) { h += '<h3>' + g + '</h3>'; for (const id in LAWS) {
    const l = LAWS[id]; if (l[1] !== g) continue; const lv = +(S.laws || {})[id] || 0, open = l[2] <= st || lv > 0, base = l[3] * Math.max(S.gdp, 700);
    if (!open) { h += '<div class="lawc lock"><b>' + l[0] + '</b><small>เปิดเมื่อเป็น' + STAGES[l[2]].n + '</small></div>'; continue; }
    const next = lv < 4 ? (LV_COST[lv + 1] - LV_COST[lv]) * base : 0;
    h += '<div class="lawc ' + (lv ? 'lawon' : '') + '"><div class="lawt"><b>' + l[0] + '</b><small>' + (lv < 4 ? 'ขึ้นระดับถัดไป ' + fmt(next) + ' บาท' : 'แรงสุดแล้ว') + '</small></div>' + lawChips(l[5], l[4], lv) + '<div class="seg">' + LAW_LV.map((t, i) => { const pay = Math.max(0, (LV_COST[i] - LV_COST[lv]) * base); return '<button class="' + (i === lv ? 'on ' : '') + (i === 4 ? 'max ' : '') + '" data-a="lawlv" data-v="' + id + ':' + i + '" ' + (pay > S.treas ? 'disabled' : '') + '>' + t + '</button>'; }).join('') + '</div></div>';
  } }
  return h;
};
UI.govClick = function (a, v) {
  const S = G.S; if (a === 'gtab') UI.govTab = v;
  else if (a === 'mhire') { const [p, i] = v.split(':'), c = S.cands[p][+i]; S.gov[p] = c; S.cands[p] = []; ensureCands(S); recalcGov(S); news('แต่งตั้ง' + c.n + ' เป็นรัฐมนตรี' + POSTS[p][0], 'good'); }
  else if (a === 'mfire') { applyFx(S, { unrest: 1.5 }); govFire(S, v); }
  else if (a === 'lawlv') { const [id, lv] = v.split(':'); S.laws = S.laws || {}; setLaw(S, id, +lv); }
  UI.hud(); UI.render();
};
UI.init();
