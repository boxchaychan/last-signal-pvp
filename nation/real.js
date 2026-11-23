'use strict';
/* ก่อร่างสร้างชาติ: real causes. Rain fills the river, what you built decides how bad it gets, damage hits real buildings, and every fix must be paid for. */
const RAIN_N = [12, 20, 45, 85, 175, 190, 185, 215, 310, 240, 70, 18];
function rOf(S) { if (!S.r) S.r = { y: 1, rain: 40, norm: 40, storm: 0, river: .2, bank: 150, res: 0, soil: .8, garb: 0, p: {}, cool: {}, n: {}, dmg: {}, plans: [], hit: [], floodM: -9, fireM: -9, slideM: -9, stormM: -9 }; return S.r; }
const waitOf = b => { const r = G.S && G.S.r, d = r && r.dmg[b.id]; return !!(d && d.w); };
const rCost = b => Math.max(30, Math.round((BT[b.t] ? BT[b.t].c : 100) * .42));
const baseOf = S => Math.max(S.gdp, 700);

/* ---------- where a building stands: near the river and low down floods first ---------- */
function lowOf(b) {
  if (b._lo != null) return b._lo; let dw = 9;
  for (let p = -6; p < b.w + 6; p++) for (let q = -6; q < b.d + 6; q++) { const x = b.x + p, z = b.z + q; if (!inMap(x, z) || W.T[ci(x, z)] !== 1) continue; const dx = p < 0 ? -p : p >= b.w ? p - b.w + 1 : 0, dz = q < 0 ? -q : q >= b.d ? q - b.d + 1 : 0, dd = Math.hypot(dx, dz); if (dd < dw) dw = dd; }
  return b._lo = Math.max(0, W.h(b.x + b.w / 2, b.z + b.d / 2)) * .6 + dw * .045;
}
function ruin(b, closed) {
  const r = G.S.r, k = G.S.k; if (!b.done || b.t === 'hall' || !BT[b.t] || r.dmg[b.id]) return false; const l = {}, f = b.vis ? .4 : 1;
  for (const q in BT[b.t].g) { const a = Math.min(k[q] || 0, BT[b.t].g[q] * f); k[q] = (k[q] || 0) - a; l[q] = a; }
  r.dmg[b.id] = closed ? { w: 1, l, c: 1 } : { w: 1, l }; W.removeInstance(b); b.done = false; b.prog = .32; b.vis = 1; W.addSite(b); W.siteProgress(b, .32); if (W.ruinLook) W.ruinLook(b, true); return true;
}
function startRepair(id) { const d = G.S.r.dmg[id]; if (!d) return; d.w = 0; const b = G.byId.get(+id); if (b && W.ruinLook) W.ruinLook(b, false); }
function ruins(S, pubOnly) { const L = []; for (const id in S.r.dmg) { const b = G.byId.get(+id); if (!b) { delete S.r.dmg[id]; continue; } if (S.r.dmg[id].w && !S.r.dmg[id].c && (!pubOnly || b.pub)) L.push(b); } return L; }

/* ---------- weather and water, every month ---------- */
function weather(S, r, x) {
  const mo = (S.m - 1) % 12; if (mo === 0) r.y = clamp(1 + (r.y - 1) * .4 + (Math.random() + Math.random() - 1) * .62, .52, 1.7);
  let rain = RAIN_N[mo] * r.y * (1 + ((S.g && S.g.rain) || 0)) * (.74 + Math.random() * .52); r.storm = 0;
  if (mo >= 5 && mo <= 10 && Math.random() < .03 + Math.max(0, r.y - 1) * .07) { r.storm = 1 + Math.random(); rain *= 1.45 + r.storm * .55; }
  r.rain = rain; r.norm = RAIN_N[mo]; r.paved = clamp((G.blds.length + W.roadCount * .3) / 900); r.runoff = .24 + .5 * (1 - x.forest) + .22 * r.paved;
  let flow = rain * r.runoff; const cap = S.k.hold || 0, take = Math.min(flow * .85, Math.max(0, cap - r.res)); if (take > 0) { r.res += take; flow -= take; }
  const use = Math.min(r.res, rain < 120 ? Math.max(18, cap * .14) : cap * .02); r.res -= use;
  r.bank = 150 + Math.min(10, S.k.levee || 0) * 34; r.river = clamp((r.river * r.bank * .3 + flow) / r.bank, 0, 2.4);
  r.soil += (clamp((rain + use) / (r.norm + 18)) - r.soil) * .35; if (mo >= 4 && mo <= 9 && r.soil < .62 && !(cap > 0 && r.res > cap * .45)) S.drought = Math.max(S.drought, (.62 - r.soil) * 1.6);
  const over = Math.max(0, x.pop - S.k.trash - 26); r.garb = over > 0 ? r.garb + over * .035 : Math.max(0, r.garb - x.pop * .05 - 1);
}
function disasters(S, r, x) {
  const mo = (S.m - 1) % 12, wood = G.blds.filter(b => b.done && (b.t === 'hut' || b.t === 'house')), hit = (id, L, why, sev) => { const done = L.filter(b => ruin(b)); if (!done.length) return false; r.hit.push({ id, ids: done.map(b => b.id), why, sev, at: [done[0].x, done[0].z] }); assignJobs(); return true; };
  if (r.river > 1 && S.m >= 12 && S.m - r.floodM >= 5) {
    const sev = r.river - 1, reach = .09 + sev * .72, all = G.blds.filter(b => b.done && b.t !== 'hall' && b.t !== 'levee' && b.t !== 'reservoir'), L = all.filter(b => lowOf(b) < reach).sort((p, q) => lowOf(p) - lowOf(q)).slice(0, Math.max(3, Math.min(42, Math.floor(all.length * .45)))); r.floodM = S.m;
    if (!L.length) news('ฝนหนัก แม่น้ำล้นตลิ่ง แต่ยังไม่มีอาคารในแนวน้ำ', 'good');
    else if (hit('flood', L, ['ฝนเดือนนี้ ' + Math.round(r.rain) + ' มม. (ปกติ ' + r.norm + ')', x.forest < .8 ? 'ป่าถูกถางเหลือ ' + pct(x.forest) + ' น้ำจึงไหลลงแม่น้ำเร็ว' : 'ป่ายังดี แต่ฝนมากเกินที่ดินจะรับไหว', S.k.levee ? 'คันกั้นน้ำ ' + S.k.levee + ' จุด ยังรับไม่พอ' : 'ยังไม่มีคันกั้นน้ำ', S.k.hold ? 'อ่างเก็บน้ำเต็มแล้ว' : 'ไม่มีอ่างหรือเขื่อนเก็บน้ำ', 'มีอาคารสร้างอยู่ในแนวน้ำ ' + L.length + ' หลัง'], sev)) { G.floodT = 7 + sev * 12; { const p0 = S.x.pop, dead = p0 * Math.min(.012, sev * .008); S.life = S.life || { dc: {} }; S.life.dc.disaster = (S.life.dc.disaster || 0) + dead; } applyFx(S, { food: -Math.min(.8, .12 + sev * .5), sick: .008 + sev * .03, pop: -Math.min(.018, sev * .012), hp: -2 - sev * 4 }); return; }
  }
  if (r.storm && S.m >= 18 && S.m - r.stormM >= 14 && wood.length) { r.stormM = S.m; const L = wood.sort(() => Math.random() - .5).sort((p, q) => (p.t === 'hut' ? 0 : 1) - (q.t === 'hut' ? 0 : 1)).slice(0, Math.min(12, Math.ceil(wood.length * .1 * r.storm))); if (L.length < 3) { const n = L.filter(b => ruin(b)).length; if (n) { assignJobs(); news('พายุพัดบ้านเสียหาย ' + n + ' หลัง เจ้าของกำลังซ่อม', 'bad'); } } else if (hit('storm', L, ['พายุเข้า ฝน ' + Math.round(r.rain) + ' มม. ในเดือนเดียว', 'บ้านไม้และกระท่อมมี ' + wood.length + ' หลัง ทนลมไม่ไหว'], r.storm)) { applyFx(S, { hp: -3 }); return; } }
  if (x.forest < .62 && r.rain > 260 && S.m >= 24 && S.m - r.slideM >= 30 && Math.random() < .35) { const L = G.blds.filter(b => b.done && b.t !== 'hall' && W.h(b.x + b.w / 2, b.z + b.d / 2) > .55).slice(0, 4); if (L.length) { r.slideM = S.m; if (hit('slide', L, ['ฝน ' + Math.round(r.rain) + ' มม. บนเขาที่ป่าถูกถาง', 'ป่าเหลือ ' + pct(x.forest) + ' ไม่มีรากไม้ยึดดิน', 'มีอาคารบนที่ลาดชัน ' + L.length + ' หลัง'], 1)) { applyFx(S, { pop: -.004, hp: -3 }); return; } } }
  if ((mo >= 11 || mo <= 3) && r.rain < 80 && r.soil < .9 && S.m >= 20 && S.m - r.fireM >= 18 && wood.length >= 8) { const fire = S.k.fire || 0, p = clamp(.02 + wood.length * .0016, 0, .16) / (1 + fire * 1.2); if (Math.random() < p) { r.fireM = S.m; const s = pick(wood), L = wood.filter(b => Math.hypot(b.x - s.x, b.z - s.z) < 7).slice(0, Math.max(1, Math.ceil((3 + wood.length / 18) / (1 + fire)))); hit('fire', L, ['หน้าแล้ง อากาศแห้ง ฝนแทบไม่ตก', 'บ้านไม้ ' + wood.length + ' หลังปลูกติดกัน ไฟลามเร็ว', fire ? 'สถานีดับเพลิง ' + fire + ' แห่ง ไปถึงช้า' : 'ยังไม่มีสถานีดับเพลิง'], 1); } }
}
function repairTick(S, r) { let n = 0; const most = 2 + (S.x.stage || 0); for (const b of ruins(S)) { if (b.pub) continue; const c = rCost(b); if (S.priv < c * 1.5) break; S.priv -= c; startRepair(b.id); if (++n >= most) break; } }
function plansTick(S, r) { for (let i = r.plans.length - 1; i >= 0; i--) { const p = r.plans[i], pay = Math.min(p.per, S.treas, S.debt); S.treas -= pay; S.debt -= pay; if (S.m >= p.m) { if (p.k === 'tax') S.tax.inc = Math.max(0, S.tax.inc - p.d); else S.bud[p.k] = clamp(S.bud[p.k] + p.d, 0, 2); r.plans.splice(i, 1); news('มาตรการหาเงิน 12 เดือนสิ้นสุดแล้ว'); } } }
function realMonth(S) {
  const r = rOf(S), x = S.x; if (!x.pop) return; weather(S, r, x); plansTick(S, r); repairTick(S, r); disasters(S, r, x); econMonth(S);
  for (const id in RI) { const v = RI[id].g(S, x, r) || 0; r.p[id] = (r.p[id] || 0) + (v - (r.p[id] || 0)) * .4; }
}

/* ---------- where the money comes from ---------- */
function moneyWays(c) {
  const S = G.S, gdp = Math.max(S.gdp, 200), y = gdp * 12, L = [{ f: 'treas', n: 'ใช้เงินคลัง', d: S.treas >= c ? 'เหลือ ' + fmt(S.treas - c) : 'มีแค่ ' + fmt(S.treas), ok: S.treas >= c }];
  L.push({ f: 'loan', n: 'กู้เงิน', d: 'ดอกเบี้ย ' + fmt(c * .0035) + '/เดือน หนี้เพิ่ม', ok: S.debt + c <= Math.max(gdp * 18, 1600) });
  const pts = c / (y * .62 / 100 * .75); const levyOK = pts <= 8 && S.tax.inc + pts <= 45; L.push({ f: 'levy', n: 'ขึ้นภาษี 12 เดือน', d: levyOK ? 'ภาษีเงินได้ +' + pts.toFixed(1) + '% คนไม่พอใจ' : 'เงินก้อนนี้ใหญ่เกินกว่าภาษีจะเก็บทัน', ok: levyOK });
  Object.keys(BUDGET_N).map(k => ({ k, v: S.bud[k] * BUDGET_N[k][1] })).sort((p, q) => q.v - p.v).slice(0, 2).forEach(q => { const d = c / (y * BUDGET_N[q.k][1] / 100), ok = d <= S.bud[q.k] * .6; L.push({ f: 'cut:' + q.k, n: 'ตัดงบ' + BUDGET_N[q.k][0], d: ok ? 'ลด ' + Math.round(d * 100) + ' จุด นาน 12 เดือน' : 'งบนี้มีไม่พอให้ตัด', ok }); });
  L.push({ f: 'print', n: 'พิมพ์เงินเพิ่ม', d: 'ไม่ต้องจ่ายคืน แต่ของแพงทั้งประเทศ', ok: c / y < .6 }); return L;
}
function takeMoney(f, c) {
  const S = G.S, r = rOf(S), gdp = Math.max(S.gdp, 200), y = gdp * 12;
  if (f === 'treas') S.treas -= c; else if (f === 'loan') S.debt += c;
  else if (f === 'levy') { const d = c / (y * .62 / 100 * .75); S.tax.inc += d; S.debt += c; r.plans.push({ k: 'tax', d, per: c / 12, m: S.m + 12 }); applyFx(S, { tr: -2, unrest: Math.min(6, d * .8) }); }
  else if (f.indexOf('cut:') === 0) { const k = f.slice(4), d = c / (y * BUDGET_N[k][1] / 100); S.bud[k] = Math.max(0, S.bud[k] - d); S.debt += c; r.plans.push({ k, d, per: c / 12, m: S.m + 12 }); applyFx(S, { tr: -1 }); }
  else if (f === 'print') applyFx(S, { infl: clamp(c / y * .16, .002, .05) });
  UI.dirty = true;
}
UI.payFor = function (c, label, done, back) {
  const S = G.S, L = moneyWays(c), any = L.some(q => q.ok);
  openModal('<span class="cat">เอาเงินจากไหน</span><h1>' + esc(label) + '</h1><div class="bd">ต้องใช้ <b>' + fmt(c) + '</b> บาท · ในคลังมี ' + fmt(S.treas) + ' · หนี้ ' + fmt(S.debt) + (any ? '' : '<br><b style="color:var(--red)">ตอนนี้หาเงินก้อนนี้ไม่ได้เลย ต้องเลือกทางที่ถูกกว่า</b>') + '</div><div class="payg">' + L.map(q => '<button class="fund" data-f="' + q.f + '" ' + (q.ok ? '' : 'disabled') + '><b>' + q.n + '</b><small>' + q.d + '</small></button>').join('') + '</div><button class="btn ghost" style="width:100%;margin-top:6px" id="payBack">กลับไปเลือกทางอื่น</button>', 'var(--gold)');
  $('payBack').onclick = () => back(); $('modal').onclick = e => { const q = e.target.closest('[data-f]'); if (!q || q.disabled) return; $('modal').onclick = null; takeMoney(q.dataset.f, c); closeModal(); done(); UI.hud(); };
};
function payOr(c, label, done, back) { const S = G.S; if (c <= 0) { closeModal(); done(); return; } if (S.treas >= c && c <= S.treas * .4) { S.treas -= c; closeModal(); done(); return; } UI.payFor(c, label, done, back); }

/* ---------- ordering what a problem really needs; levees and reservoirs go by the river ---------- */
function fixPlan(list, key, gap) { const st = G.S.x.stage || 0; let t = null; for (const q of list) { if (BT[q].st > st) continue; t = q; if ((BT[q].g[key] || 0) >= gap) break; } if (!t) return null; const n = clamp(Math.ceil(gap / (BT[t].g[key] || 1)), 1, 6); return { t, n, c: BT[t].c * n }; }
function riverSpot(c, t) {
  const d = BT[t], w = d.s[0], h = d.s[1]; let best = null, bs = -1e9;
  for (let z = Math.max(1, c.z - 36 | 0); z < Math.min(N - h - 1, c.z + 36); z++) for (let x = Math.max(1, c.x - 36 | 0); x < Math.min(N - w - 1, c.x + 36); x++) {
    let dw = 9; for (let p = -4; p < w + 4; p += 2) for (let q = -4; q < h + 4; q += 2) if (inMap(x + p, z + q) && W.T[ci(x + p, z + q)] === 1) dw = Math.min(dw, Math.hypot(p < 0 ? p : Math.max(0, p - w), q < 0 ? q : Math.max(0, q - h))); if (dw > 5) continue;
    const s = -Math.hypot(x - c.x, z - c.z) - dw * 3; if (s <= bs || !W.canPlace(x, z, w, h, true)) continue; const door = W.doorFor(x, z, w, h, c.x, c.z); if (door) { bs = s; best = { x, z, w, d: h, door }; }
  } return best;
}
const findSpot1 = W.findSpot; W.findSpot = function (c, t, R0) { if (t === 'levee' || t === 'reservoir') { const s = riverSpot(c, t); if (s) return s; } return findSpot1(c, t, R0); };
function orderBuild(t, n) { const S = G.S; let made = 0, idx = 0, top = -1; G.cities.forEach((c, i) => { if (c.n > top) { top = c.n; idx = i; } }); for (let i = 0; i < n; i++) { const sp = W.findSpot(G.cities[idx], t); if (!sp) break; makeB(t, sp, idx, { fund: 'treas', urgent: true }); made++; } if (made < n) { S.treas += BT[t].c * (n - made); news('ไม่มีที่สร้าง' + BT[t].n + ' คืนเงิน ' + fmt(BT[t].c * (n - made))); } else news('อนุมัติแล้ว ชาวเมืองกำลังไปสร้าง' + BT[t].n, 'good'); }

/* ---------- problems that grow from the state of the country ---------- */
const O = (n, d, c, fx, cool, more) => Object.assign({ n, d, c: Math.round(c || 0), fx: fx || {}, cool: cool || 8 }, more);
const fixO = (list, key, gap, d, cool) => { const p = fixPlan(list, key, Math.max(1, gap)); return p ? O('สร้าง' + BT[p.t].n + (p.n > 1 ? ' ' + p.n + ' แห่ง' : ''), d, p.c, {}, cool || 16, { b: [p.t, p.n] }) : null; };
const L_WATER = ['well', 'waterworks', 'dam'], L_POWER = ['gen', 'coal', 'solar', 'nuclear'], L_HOSP = ['clinic', 'hospital', 'medcenter'], L_SCHOOL = ['school', 'hischool', 'univ'], L_SAFE = ['police', 'policehq'], L_TRASH = ['trash', 'recycle'], L_HOLD = ['reservoir', 'dam'];
const RI = {
  water: { cat: 'น้ำ', n: 'น้ำสะอาด', fix: L_WATER, key: 'water', g: (S, x, r) => x.m < 3 ? 0 : (1 - x.cleanW) * 1.55 + (r.soil < .5 ? .2 : 0), line: (S, x) => 'น้ำพอสำหรับ ' + fmt(S.k.water) + ' จาก ' + fmt(x.pop) + ' คน', t: 'น้ำสะอาดไม่พอ', b: (S, x) => 'ราว ' + fmt(Math.max(1, x.pop - S.k.water)) + ' คนต้องตักน้ำจากลำธารมาดื่ม เริ่มมีคนท้องเสีย', why: (S, x, r) => ['มีคน ' + fmt(x.pop) + ' แต่น้ำสะอาดพอแค่ ' + fmt(S.k.water) + ' คน', r.soil < .6 ? 'ฝนน้อย น้ำในบ่อลดลง' : 'เมืองโตเร็วกว่าระบบน้ำ'],
    o: (S, x) => [fixO(L_WATER, 'water', x.pop - S.k.water, 'แก้ได้ถาวร แต่ต้องรอสร้างหลายเดือน'), O('ซื้อน้ำมาแจก', 'ได้น้ำทันที แต่หมดแล้วต้องซื้อใหม่', baseOf(S) * .3, { sick: -.012 }, 7), O('แบ่งเวลาใช้น้ำ', 'ไม่เสียเงิน แต่คนลำบาก ปัญหายังอยู่', 0, { hp: -4, tr: -2 }, 5)] },
  hosp: { cat: 'สุขภาพ', n: 'หมอและเตียง', fix: L_HOSP, key: 'hosp', g: (S, x) => x.m < 5 ? 0 : (1 - x.hospCov) * 1.15 * clamp(x.sick / .045), line: (S, x) => 'ดูแลได้ ' + fmt(S.k.hosp) + ' จาก ' + fmt(x.pop) + ' คน · ป่วย ' + pct(x.sick), t: 'คนป่วยไม่มีที่รักษา', b: (S, x) => 'ตอนนี้มีคนป่วยราว ' + fmt(x.pop * x.sick) + ' คน หลายคนต้องนอนรอที่บ้าน', why: (S, x) => ['หมอและเตียงรองรับได้ ' + pct(x.hospCov) + ' ของคน', 'คนป่วย ' + pct(x.sick) + (x.cleanW < .8 ? ' เพราะน้ำไม่สะอาด' : x.clean < .8 ? ' เพราะขยะและยุง' : '')],
    o: (S, x) => [fixO(L_HOSP, 'hosp', x.pop - S.k.hosp, 'รักษาได้ระยะยาว แต่แพงและรอสร้าง'), O('จ้างหมอจากนอกเมือง', 'ช่วยได้เร็ว ต้องจ่ายแพงและอยู่ไม่นาน', baseOf(S) * .35, { hq: 4, sick: -.01 }, 8), O('ให้ใช้ยาพื้นบ้าน', 'ไม่เสียเงิน แต่บางคนอาการหนักขึ้น', 0, { sick: .012, tr: -3 }, 6)] },
  school: { cat: 'การศึกษา', n: 'ที่เรียน', fix: L_SCHOOL, key: 'school', g: (S, x) => x.m < 8 ? 0 : (1 - x.schoolCov) * 1.1 * clamp(x.kids / 9), line: (S, x) => 'รับเด็กได้ ' + fmt(S.k.school) + ' คน · เด็ก ' + fmt(x.kids), t: 'เด็กไม่มีที่เรียน', b: (S, x) => 'เด็ก ' + fmt(x.kids) + ' คน แต่ได้เรียนแค่ ' + pct(x.schoolCov) + ' ที่เหลือต้องไปช่วยงานบ้าน', why: (S, x) => ['ที่เรียนรับได้ ' + fmt(S.k.school) + ' คน', 'ถ้าไม่เรียน โตมาได้งานรายได้ต่ำ'],
    o: (S, x) => [fixO(L_SCHOOL, 'school', x.kids * 1.2 - S.k.school, 'ลงทุนวันนี้ อีกหลายปีกว่าจะเห็นผล'), O('ให้ผู้ใหญ่ช่วยสอน', 'ถูก แต่คุณภาพต่ำ และเสียคนทำงาน', baseOf(S) * .08, { edu: .05, priv: -.04 }, 9), O('ยังไม่ลงทุน', 'เก็บเงินไว้ก่อน แต่คนรุ่นนี้เสียโอกาส', 0, { edu: -.05, tr: -2 }, 8)] },
  power: { cat: 'ไฟฟ้า', n: 'ไฟฟ้า', fix: L_POWER, key: 'power', g: (S, x) => x.pop < 40 ? 0 : (1 - x.pw) * 1.3 * clamp((x.pop - 25) / 60), line: (S, x) => 'ไฟพอ ' + pct(x.pw) + ' ของความต้องการ', t: 'ไฟดับเป็นแถบ', b: (S, x) => 'ไฟฟ้าผลิตได้แค่ ' + pct(x.pw) + ' ของที่ใช้ ร้านค้าและโรงงานต้องหยุดเป็นช่วงๆ', why: (S, x) => ['บ้านและโรงงานใช้ไฟมากกว่าที่ผลิตได้', 'โรงงานมีคนทำงาน ' + fmt(x.E_ind) + ' คน'],
    o: (S, x) => [fixO(L_POWER, 'power', (x.pop * .7 + x.E_ind * .6 + x.E_tech) - S.k.power, 'ไฟพอระยะยาว ถ้าเป็นถ่านหินอากาศจะเสีย'), O('ดับไฟหมุนเวียน', 'ไม่เสียเงิน แต่เศรษฐกิจสะดุด', 0, { priv: -.12, hp: -3 }, 6), O('ซื้อไฟจากเพื่อนบ้าน', 'ได้ทันที แต่เป็นค่าใช้จ่ายทุกปี', baseOf(S) * .4, { priv: .03 }, 9)] },
  trash: { cat: 'ขยะ', n: 'ขยะ', fix: L_TRASH, key: 'trash', g: (S, x, r) => r.garb / (x.pop * .25 + 8), line: (S, x, r) => 'ขยะค้าง ' + fmt(r.garb) + ' ตัน · จัดการได้ ' + fmt(S.k.trash) + ' คน', t: 'ขยะล้นเมือง', b: (S, x, r) => 'ขยะค้าง ' + fmt(r.garb) + ' ตัน หนูและยุงเพิ่มขึ้น น้ำขังในกองขยะ', why: (S, x) => ['คน ' + fmt(x.pop) + ' คน แต่ระบบขยะรับได้ ' + fmt(S.k.trash + 26) + ' คน', 'ยิ่งเมืองโต ขยะยิ่งเพิ่มทุกเดือน'],
    o: (S, x) => [fixO(L_TRASH, 'trash', x.pop - S.k.trash, 'แก้ที่ต้นเหตุ แต่ใช้เงินและที่ดิน', 14), O('เผากลางแจ้ง', 'ถูกและเร็ว แต่อากาศเสีย', baseOf(S) * .05, { pol: .04, sick: .006 }, 7, { garb: .4 }), O('ขนไปทิ้งนอกเมือง', 'เมืองสะอาดขึ้น แต่ป่าและน้ำเสีย', baseOf(S) * .14, { pol: .02, forest: -.008 }, 8, { garb: .5 })] },
  house: { cat: 'ที่อยู่', n: 'ที่อยู่อาศัย', g: (S, x) => x.pop < 20 ? 0 : (1 - x.houseRatio) * 4.2, line: (S, x) => 'บ้านพอ ' + pct(clamp(x.houseRatio)) + ' ของคน', t: 'คนล้นบ้าน เริ่มเกิดสลัม', b: (S, x) => 'บ้านรองรับได้ ' + pct(clamp(x.houseRatio)) + ' ของคน หลายครอบครัวอยู่รวมกัน', why: (S, x) => ['คนเพิ่มเร็วกว่าบ้าน', 'เอกชนมีเงินสร้างบ้าน ' + fmt(S.priv)],
    o: (S, x) => { const t = tierPick(HOME_T, x.stage, x.pop * .05, 'house'), n = clamp(Math.ceil((x.pop - S.k.house) / BT[t].g.house), 1, 6); return [O('สร้างบ้านราคาถูก ' + n + ' หลัง', 'คนมีที่อยู่ แต่รัฐจ่ายเอง', BT[t].c * n, { hp: 2 }, 14, { b: [t, n] }), O('จำกัดคนย้ายเข้า', 'ไม่เสียเงิน แต่เศรษฐกิจโตช้าลง', 0, { pop: -.008, rep: -.01 }, 10), O('ปล่อยให้แออัด', 'ไม่เสียเงิน แต่โรคและอาชญากรรมตามมา', 0, { crime: .03, sick: .012, tr: -3, next: [9, 'slum_fire'] }, 9)]; } },
  jobs: { cat: 'เศรษฐกิจ', n: 'งาน', g: (S, x) => x.pop < 25 ? 0 : x.u / .14, line: (S, x) => 'ตกงาน ' + pct(x.u), t: 'คนตกงานเพิ่มขึ้น', b: (S, x) => 'มีคนว่างงาน ' + fmt(x.LF * x.u) + ' คน หลายครอบครัวเริ่มเลื่อนการมีลูกและคิดย้ายออก', why: (S, x) => ['คนทำงานได้ ' + fmt(x.LF) + ' คน มีงาน ' + fmt(x.emp), 'เอกชนมีเงินลงทุน ' + fmt(S.priv)],
    o: S => [O('จ้างคนซ่อมถนนและขุดคลอง', 'มีงานทันที แต่หมดเงินแล้วงานก็หมด', baseOf(S) * .6, { hp: 4, road: .03 }, 10), O('ลดภาษีธุรกิจ 3%', 'ธุรกิจลงทุนเพิ่ม แต่รัฐเก็บเงินได้น้อยลง', 0, { corp: 1, priv: .3 }, 12, { corp: -3 }), O('ให้ตลาดปรับตัวเอง', 'ไม่เสียเงิน แต่คนจนลำบากและอาชญากรรมขึ้น', 0, { crime: .02, tr: -4 }, 7)] },
  food: { cat: 'อาหาร', n: 'อาหาร', g: (S, x) => (1.2 - x.foodMonths) / .6 + x.hunger * 5, line: (S, x) => 'ข้าวในยุ้งพอ ' + x.foodMonths.toFixed(1) + ' เดือน', t: 'อาหารกำลังจะหมด', b: (S, x) => 'ยุ้งฉางเหลือพอกินอีก ' + x.foodMonths.toFixed(1) + ' เดือน ราคาข้าวเริ่มพุ่ง', why: (S, x, r) => ['ผลิตได้ ' + fmt(x.foodOut) + ' คนกิน ' + fmt(x.pop) + ' ต่อเดือน', r.soil < .6 ? 'ฝนน้อย ผลผลิตตก' : 'นาไม่พอกับคนที่เพิ่มขึ้น'],
    o: (S, x) => [O('นำเข้าข้าวฉุกเฉิน', 'อิ่มทันที แต่แพงตามราคาตลาด', Math.max(baseOf(S) * .5, x.pop * S.pFood * .6), { food: 1.6 }, 8), O('ปันส่วนอาหาร', 'ไม่เสียเงิน แต่ทุกคนหิวและไม่พอใจ', 0, { food: .5, hp: -5, unrest: 3 }, 6), O('ปล่อยให้ราคาขึ้น', 'คนมีเงินยังซื้อได้ คนจนอดก่อน', 0, { gini: .012, infl: .012, tr: -3, next: [4, 'famine'] }, 8)] },
  drought: { cat: 'ภัยธรรมชาติ', n: 'ความชื้นในดิน', fix: L_HOLD, key: 'hold', g: (S, x, r) => { const mo = (S.m - 1) % 12; return mo < 4 || mo > 9 || x.pop < 15 || r.rain > r.norm * .9 || (S.k.hold > 0 && r.res > S.k.hold * .45) ? 0 : (.62 - r.soil) / .28; }, line: (S, x, r) => 'ดินชื้น ' + pct(r.soil) + ' · อ่างเก็บน้ำ ' + fmt(r.res), t: 'ภัยแล้ง นาเริ่มแห้ง', b: (S, x, r) => 'ฝนเดือนนี้ ' + Math.round(r.rain) + ' มม. จากปกติ ' + r.norm + ' ข้าวในนาเริ่มเหี่ยว', why: (S, x, r) => ['ปีนี้ฝนน้อยกว่าปกติ ' + Math.max(0, Math.round((1 - r.y) * 100)) + '%', S.k.hold ? 'น้ำในอ่างเหลือ ' + fmt(r.res) : 'ไม่มีอ่างเก็บน้ำไว้ใช้หน้าแล้ง'],
    o: (S, x) => [fixO(L_HOLD, 'hold', 60, 'เก็บน้ำไว้ใช้ปีต่อไป แต่ปีนี้ยังไม่ทัน', 18), O('ซื้ออาหารสำรอง', 'กันคนอด แต่ไม่ได้แก้เรื่องน้ำ', baseOf(S) * .5, { food: 1 }, 7), O('ให้ชาวนาใช้น้ำก่อน', 'รักษานาไว้ได้ แต่เมืองขาดน้ำ', 0, { drought: .2, hp: -3, sick: .008 }, 6)] },
  smog: { cat: 'สิ่งแวดล้อม', n: 'อากาศ', g: (S, x) => x.P / .34, line: (S, x) => 'มลพิษ ' + pct(x.P), t: 'ฝุ่นพิษปกคลุมเมือง', b: (S, x) => 'มลพิษ ' + pct(x.P) + ' เด็กต้องหยุดเรียน คนไข้ทางเดินหายใจเพิ่มขึ้น', why: (S, x) => ['โรงงานมีสัดส่วนสูง ' + pct(x.dirtyShare), S.k.power && x.k.dirty > 800 ? 'โรงไฟฟ้าถ่านหินปล่อยควัน' : 'รถและการเผาขยะเพิ่มขึ้น', 'ป่าเหลือ ' + pct(x.forest)],
    o: S => [O('สั่งโรงงานติดเครื่องกรอง', 'อากาศดีขึ้น แต่ธุรกิจเสียเงินและลดคน', 0, { pol: -.07, priv: -.4 }, 12), O('รัฐอุดหนุนพลังงานสะอาด', 'แก้ระยะยาว แต่แพงมาก', baseOf(S) * 1.1, { pol: -.08, tech: .008 }, 18), O('แจกหน้ากาก', 'ถูก แต่แก้ไม่ถึงต้นเหตุ', baseOf(S) * .08, { sick: .008, tr: -3 }, 7)] },
  riverpol: { cat: 'สิ่งแวดล้อม', n: 'น้ำในแม่น้ำ', g: (S, x) => x.dirtyShare / .22, line: (S, x) => 'น้ำเสียโรงงาน ' + pct(x.dirtyShare), t: 'โรงงานปล่อยน้ำเสียลงแม่น้ำ', b: () => 'ปลาตายลอยเป็นแพ ชาวบ้านปลายน้ำเริ่มเป็นผื่น', why: (S, x) => ['โรงงานมีคนทำงาน ' + fmt(x.E_ind) + ' คน', 'ยังไม่มีระบบบำบัดน้ำเสียรวม'],
    o: S => [O('บังคับให้โรงงานบำบัดเอง', 'รัฐไม่จ่าย แต่โรงงานขึ้นราคาและลดคน', 0, { pol: -.05, priv: -.35 }, 14), O('รัฐสร้างระบบบำบัด', 'น้ำสะอาดขึ้น แต่ใช้เงินภาษี', baseOf(S) * .7, { pol: -.06 }, 18), O('ปล่อยไว้เพื่อรักษางาน', 'เศรษฐกิจเดินต่อ แต่แม่น้ำจะเน่า', 0, { pol: .05, sick: .012, tr: -4, next: [8, 'river_poison'] }, 10)] },
  traffic: { cat: 'เมือง', n: 'จราจร', g: (S, x) => x.cong / .42, line: (S, x) => 'รถติด ' + pct(x.cong) + ' · ถนน ' + fmt(S.k.roadC) + ' ช่อง', t: 'รถติดทั้งเมือง', b: (S, x) => 'คนเสียเวลาบนถนนหลายชั่วโมง ความแออัด ' + pct(x.cong), why: (S, x) => ['รถเพิ่มตามรายได้ แต่ถนนมีแค่ ' + fmt(S.k.roadC) + ' ช่อง', 'ยังไม่มีขนส่งมวลชน'],
    o: S => [O('ลงทุนรถไฟฟ้า', 'แก้ได้จริง แต่แพงและใช้เวลา', baseOf(S) * 1.6, { cong: -.25, pol: -.02 }, 24), O('ตัดถนนเพิ่ม', 'ถูกกว่า แต่รถจะเพิ่มตามอีก', baseOf(S) * .6, { cong: -.08, pol: .02 }, 12), O('เก็บค่าเข้าเมือง', 'รัฐได้เงิน แต่คนจนเดือดร้อน', 0, { c: -.1, cong: -.14, tr: -3, gini: .006 }, 12)] },
  crime: { cat: 'ความปลอดภัย', n: 'ความปลอดภัย', fix: L_SAFE, key: 'safe', g: (S, x) => x.crime / .19, line: (S, x) => 'อาชญากรรม ' + pct(x.crime) + ' · ตกงาน ' + pct(x.u), t: 'อาชญากรรมเพิ่มขึ้น', b: (S, x) => 'ขโมยและจี้ปล้นเพิ่มขึ้น อาชญากรรม ' + pct(x.crime), why: (S, x) => ['คนตกงาน ' + pct(x.u) + ' ช่องว่างรวยจน ' + x.gini.toFixed(2), 'ตำรวจดูแลได้ ' + pct(x.safeCov) + ' ของคน'],
    o: (S, x) => [fixO(L_SAFE, 'safe', x.pop - S.k.safe, 'คุมได้ดีขึ้น แต่ไม่ได้แก้ความจน', 14), O('สร้างงานในย่านยากจน', 'แก้ที่ต้นเหตุ แต่แพงและช้า', baseOf(S) * .55, { crime: -.035, hp: 2 }, 14), O('เพิ่มโทษและตั้งด่าน', 'ถูก แต่คนเริ่มกลัวรัฐ', baseOf(S) * .06, { crime: -.015, tr: -3, unrest: 2 }, 8)] }
};
const HIT_T = { flood: ['ภัยธรรมชาติ', 'น้ำท่วม!', 'แม่น้ำล้นตลิ่งเข้าเมือง'], storm: ['ภัยธรรมชาติ', 'พายุถล่ม', 'ลมแรงพัดหลังคาและกำแพงพัง'], slide: ['ภัยธรรมชาติ', 'ดินถล่ม', 'ภูเขาที่ถูกถางป่าไหลลงมาทับบ้าน'], fire: ['ภัยพิบัติ', 'ไฟไหม้ชุมชน', 'ไฟลามจากบ้านหลังหนึ่งไปทั้งแถว'] };
function hitOptions(S, h) {
  const x = S.x, L = h.ids.map(i => G.byId.get(i)).filter(Boolean), all = L.reduce((p, b) => p + rCost(b), 0), pub = L.filter(b => b.pub).reduce((p, b) => p + rCost(b), 0), out = [O('รัฐจ่ายซ่อมให้ทั้งหมด', 'คนรักคุณ แต่เงินก้อนใหญ่ และเหตุเดิมเกิดซ้ำได้', all, { tr: 3 }, 0, { rep: 'all', ids: h.ids })];
  if (pub) out.push(O('ซ่อมแค่ของส่วนรวม', 'ประหยัด แต่คนจนซ่อมบ้านเองไม่ไหว', pub, { gini: .008, tr: -2 }, 0, { rep: 'pub', ids: h.ids }));
  if (h.id === 'flood') { const lv = BT.levee.c * 2, ho = fixPlan(L_HOLD, 'hold', 60); out.push(O('ซ่อม + สร้างคันกั้นน้ำ 2 จุด', 'แพงสุด แต่ฝนแบบนี้จะท่วมยากขึ้น', all + lv, { tr: 2 }, 0, { rep: 'all', ids: h.ids, b: ['levee', 2] })); if (ho) out.push(O('สร้าง' + BT[ho.t].n + 'เก็บน้ำ', 'แก้ต้นเหตุระยะยาว แต่บ้านยังต้องซ่อมเอง', ho.c, { tr: -1 }, 0, { b: [ho.t, ho.n] })); if (x.forest < .75) out.push(O('ปลูกป่าต้นน้ำคืน', 'ลดน้ำป่าในอีกหลายปี แต่ตอนนี้ไม่ช่วยใคร', baseOf(S) * .5, { forest: .05, tr: -2 })); }
  if (h.id === 'fire') { const f = fixPlan(['firest'], 'fire', 1); if (f) out.push(O('ซ่อม + ตั้งสถานีดับเพลิง', 'ไฟครั้งหน้าลามน้อยลง แต่ต้องจ่ายสองก้อน', all + f.c, { tr: 2 }, 0, { rep: 'all', ids: h.ids, b: ['firest', 1] })); }
  if (h.id === 'slide') out.push(O('ปลูกป่าบนเขาคืน', 'กันดินถล่มระยะยาว แต่บ้านยังต้องซ่อมเอง', baseOf(S) * .45, { forest: .05 }));
  out.push(O('ให้ชาวบ้านซ่อมกันเอง', 'ไม่เสียเงิน แต่ช้า คนโกรธและบางคนย้ายออก', 0, { tr: -6, unrest: 3, pop: -.005 })); return out;
}

/* ---------- the card: cause first, no best answer on top, and you must find the money ---------- */
const shuffled = l => { const a = l.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.random() * (i + 1) | 0; [a[i], a[j]] = [a[j], a[i]]; } return a; };
const causeBox = L => L && L.length ? '<div class="cause"><b>สาเหตุ</b>' + L.map(q => '<span>' + q + '</span>').join('') + '</div>' : '';
function applyO(S, card, o) {
  const fx = Object.assign({}, o.fx); delete fx.corp; if (Object.keys(fx).length) applyFx(S, fx); const r = S.r; if (o.corp) S.tax.corp = clamp(S.tax.corp + o.corp, 0, 45); if (o.garb) r.garb *= o.garb;
  if (o.rep) for (const i of o.ids) { const b = G.byId.get(i); if (b && r.dmg[i] && (o.rep === 'all' || b.pub)) startRepair(i); } if (o.b) orderBuild(o.b[0], o.b[1]); if (o.econ) econAct(S, o.econ[0], o.econ[1]); if (o.inv) investAct(S, o.inv[0], o.inv[1]);
  /* the same problem comes back only if it is still there, and each time it waits longer so other things can happen */
  if (card.id) { const n = r.n[card.id] || 0; r.cool[card.id] = S.m + Math.round((o.cool || 8) * (1 + Math.min(4, n) * .7)); r.p[card.id] = .5; r.n[card.id] = n + 1; } news('ตัดสินใจ: ' + o.n); UI.dirty = true;
}
UI.showCard = function (card) {
  const S = G.S, list = card.list || (card.list = shuffled(card.o.filter(Boolean)));
  openModal('<span class="cat">' + card.cat + '</span><span class="dt">' + dateOf(S.m) + '</span><h1>' + card.t + '</h1><div class="bd">' + card.b + '</div>' + causeBox(card.why) + list.map((o, i) => '<button class="opt" data-o="' + i + '"><b>' + o.n + '</b><small>' + o.d + '</small><div class="fx">' + (o.c > 0 ? '<span class="' + (o.c > S.treas ? 'r' : 'n') + '">ใช้เงิน ' + fmt(o.c) + (o.c > S.treas ? ' · เงินคลังไม่พอ' : '') + '</span>' : '<span>ไม่ใช้เงิน</span>') + '</div></button>').join(''));
  $('modal').onclick = v => { const q = v.target.closest('[data-o]'); if (!q) return; $('modal').onclick = null; const o = list[+q.dataset.o]; payOr(o.c, o.n, () => applyO(S, card, o), () => UI.showCard(card)); };
};
const nthOf = (r, id) => r.n[id] ? ' (ครั้งที่ ' + (r.n[id] + 1) + ')' : '';
function showHit(S, h) { const T = HIT_T[h.id], L = h.ids.map(i => G.byId.get(i)).filter(Boolean), cost = L.reduce((p, b) => p + rCost(b), 0), count = {}; L.forEach(b => { count[BT[b.t].n] = (count[BT[b.t].n] || 0) + 1; }); W.fly(h.at[0], h.at[1], 26); UI.showCard({ cat: T[0], t: T[1] + nthOf(S.r, h.id), b: T[2] + ' เสียหาย: ' + Object.keys(count).slice(0, 4).map(q => q + ' ' + count[q]).join(' · ') + ' รวมค่าซ่อม ' + fmt(cost) + ' บาท', why: h.why, o: hitOptions(S, h), id: 'hit_' + h.id }); }
function showInc(S, id) { const q = RI[id], x = S.x, r = S.r; UI.showCard({ id, cat: q.cat, t: q.t + nthOf(r, id), b: q.b(S, x, r), why: q.why(S, x, r), o: q.o(S, x, r) }); }

/* old story events stay only when something real is behind them */
['dirty_water', 'water_short', 'drought', 'food_price', 'sick_child', 'dengue', 'doctor_short', 'no_school', 'jobless', 'factory_waste', 'smog', 'trash_mountain', 'overpop', 'traffic', 'flood', 'storm', 'fire', 'thief', 'neighbor_fight'].forEach(id => { const e = EV.find(q => q.id === id); if (e) e.when = () => false; });
const setWhen = (id, f) => { const e = EV.find(q => q.id === id); if (e) e.when = f; }; EV.find(q => q.id === 'festival').cd = 9;
setWhen('corrupt', x => x.corr > .09 && G.blds.some(b => !b.done && b.pub && BT[b.t].c >= 800)); setWhen('pest', x => x.E_ag > 6 && G.S.r && G.S.r.rain > 170 && G.S.r.soil > .8); setWhen('pandemic', x => x.m > 96 && x.k.port + x.k.air > 0); setWhen('migrants', x => x.m > 30 && x.tension > .22); setWhen('river_dispute', x => x.m > 40 && G.S.r && G.S.r.soil < .6); setWhen('festival', x => x.happy > 62 && x.foodMonths > 2.2 && (x.m % 12 === 11 || x.m % 12 === 0));
const WHY = {
  corrupt: x => ['มีโครงการรัฐกำลังก่อสร้าง', 'คอร์รัปชันในระบบ ' + pct(x.corr)], pest: () => ['ฝนชุกและดินชื้น แมลงจึงระบาด'], pandemic: x => ['มีท่าเรือหรือสนามบินรับคนจากต่างประเทศ'], migrants: x => ['ความตึงเครียดในภูมิภาค ' + pct(x.tension)], river_dispute: () => ['ฝนน้อย ทุกประเทศจึงแย่งน้ำ'], rice_crash: x => ['ข้าวเหลือในยุ้ง ' + x.foodMonths.toFixed(1) + ' เดือน ผลผลิตล้นตลาด'], tax_protest: x => ['ภาระภาษีรวม ' + Math.round(x.taxLoad) + '%'], deficit: x => ['หนี้ ' + pct(x.debtRatio) + ' ของรายได้ประเทศต่อปี'], debt_crisis: x => ['หนี้ ' + pct(x.debtRatio) + ' ของรายได้ประเทศต่อปี'], inflation: x => ['ของแพงขึ้น ' + (x.infl * 1200).toFixed(0) + '% ต่อปี'], strike: x => ['ช่องว่างรวยจน ' + x.gini.toFixed(2) + ' · ภาษี ' + Math.round(x.taxLoad) + '%'], inequal: x => ['ช่องว่างรวยจน ' + x.gini.toFixed(2)], loan_shark: x => ['ช่องว่างรวยจน ' + x.gini.toFixed(2)], old_society: x => ['คนสูงอายุ ' + pct(x.oldShare)], low_birth: x => ['เด็กเกิด ' + x.tfr.toFixed(1) + ' คนต่อแม่หนึ่งคน'], child_labor: x => ['รายได้ต่อคน ' + fmt(x.gdpPc) + ' · ได้เรียน ' + pct(x.schoolCov)], brain_drain: x => ['เรียนเฉลี่ย ' + x.eduY.toFixed(1) + ' ปี แต่รายได้ต่อคนแค่ ' + fmt(x.gdpPc)], skills_gap: x => ['ตกงาน ' + pct(x.u) + ' แต่เรียนเฉลี่ยแค่ ' + x.eduY.toFixed(1) + ' ปี'], housing_bubble: x => ['บ้านพอ ' + pct(clamp(x.houseRatio)) + ' ของคน'], deforest: x => ['ป่าเหลือ ' + pct(x.forest)], too_many_factories: x => ['โรงงานสกปรกมีสัดส่วน ' + pct(x.dirtyShare)], fishers: x => ['ถมทะเลแล้ว ' + x.land + ' ครั้ง'], land_sink: x => ['ถมทะเลแล้ว ' + x.land + ' ครั้ง'], drugs: x => ['ตกงาน ' + pct(x.u) + ' · อาชญากรรม ' + pct(x.crime)], mental: x => ['ความสุขเฉลี่ย ' + Math.round(x.happy)], coup_plot: x => ['ความไม่สงบ ' + Math.round(x.unrest) + '%'], uprising: x => ['ความไม่สงบ ' + Math.round(x.unrest) + '%'], sanctions: x => ['ชื่อเสียงโลกเหลือ ' + pct(x.rep)], press: x => ['ความเชื่อใจรัฐบาล ' + Math.round(x.trust)], border_crisis: x => ['ความตึงเครียดชายแดน ' + pct(x.tension)], invasion: x => ['ความตึงเครียดชายแดน ' + pct(x.tension)], bandits: x => ['ไม่มีกองทัพ ตำรวจดูแลได้ ' + pct(x.safeCov)], trade_war: x => ['ประเทศพึ่งการค้าผ่านท่าเรือ'], investor: x => ['ชื่อเสียงโลก ' + pct(x.rep) + ' · ความเชื่อใจ ' + Math.round(x.trust)], grant: x => ['เงินคลังน้อย องค์กรโลกจึงเสนอช่วย'], festival: x => ['เก็บเกี่ยวเสร็จ ข้าวเหลือ ' + x.foodMonths.toFixed(1) + ' เดือน']
};
/* no free lunch: an answer with no downside at least costs money to carry out */
for (const e of EV) for (const o of e.o) { const f = o[1]; let bad = !!(f.next || f.later || f.fire || f.geo || f.war || f.bud || f.tax); for (const k in f) { const v = f[k]; if (k === 'c') { if (v > 0) bad = true; } else if (FX_BAD[k] ? v > 0 : ['tr', 'hp', 'priv', 'rep', 'food', 'edu', 'hq', 'forest', 'pop', 'tech', 'road'].includes(k) && v < 0) bad = true; } if (!bad) f.c = (f.c || 0) + .12; }
UI.showEvent = function (e) {
  const S = G.S, why = e.why || (WHY[e.id] ? WHY[e.id](S.x, S) : null), idx = shuffled(e.o.map((_, i) => i)), price = o => o[1].c > 0 ? Math.round(o[1].c * baseOf(S)) : 0;
  const line = o => { const g = [], b = []; for (const k in o[1]) { if (k === 'c') { if (o[1].c < 0) g.push('เงิน'); continue; } const name = FX_N[k]; if (!name) continue; const v = o[1][k]; ((FX_BAD[k] ? v < 0 : v > 0) ? g : b).push(name); } const c = price(o); return '<div class="fx">' + (c ? '<span class="' + (c > S.treas ? 'r' : 'n') + '">ใช้เงิน ' + fmt(c) + (c > S.treas ? ' · เงินคลังไม่พอ' : '') + '</span>' : '<span>ไม่ใช้เงิน</span>') + (g.length ? '<span class="g">ได้ ' + g.slice(0, 2).join(' ') + '</span>' : '') + (b.length ? '<span class="r">เสีย ' + b.slice(0, 2).join(' ') + '</span>' : '') + '</div>'; };
  const draw = () => { openModal('<span class="cat">' + e.cat + '</span><span class="dt">' + dateOf(S.m) + '</span><h1>' + e.t + '</h1><div class="bd">' + e.b + '</div>' + causeBox(why) + idx.map(i => '<button class="opt" data-o="' + i + '"><b>' + e.o[i][0] + '</b>' + line(e.o[i]) + '</button>').join(''));
    $('modal').onclick = v => { const q = v.target.closest('[data-o]'); if (!q) return; $('modal').onclick = null; const o = e.o[+q.dataset.o], c = price(o), fx = Object.assign({}, o[1]); if (c) delete fx.c; payOr(c, o[0], () => { answerEvent(e, [o[0], fx]); news('ตัดสินใจ: ' + o[0]); UI.hud(); }, draw); }; };
  draw();
};
/* the next card comes from what is really happening, the worst first */
function realNext(S) {
  if (G.modal) return; const r = rOf(S); S.queue = S.queue || []; const due = S.queue.findIndex(q => q.m <= S.m); if (due >= 0) { const q = S.queue.splice(due, 1)[0], ev = EV.find(e => e.id === q.id); if (ev) { S.lastEv[ev.id] = S.m; S.evM = S.m; UI.showEvent(ev); return; } }
  if (r.hit.length) { S.evM = S.m; showHit(S, r.hit.shift()); return; } if (S.m - S.evM < 6) return;
  let best = null, bs = 1; for (const id in RI) { const p = r.p[id] || 0; if (p >= bs && S.m >= (r.cool[id] || 0)) { bs = p; best = id; } } if (best) { S.evM = S.m; showInc(S, best); return; }
  if (S.m - S.evM < 18) return; const L = eligible(); if (!L.length) return; L.sort((p, q) => (S.lastEv[p.id] != null ? 1 : 0) - (S.lastEv[q.id] != null ? 1 : 0) || Math.random() - .5); const e = L[0]; S.lastEv[e.id] = S.m; S.evM = S.m; UI.showEvent(e);
}

/* ---------- watch list: see it coming and act before it breaks ---------- */
DOCK.splice(3, 0, ['risk', 'เฝ้าระวัง']); TITLES.risk = 'สถานการณ์จริง'; IC.risk = svg('<path d="M12 2L1 21h22zM11 9h2v6h-2zm0 8h2v2h-2z"/>');
UI.tab_risk = function () {
  const S = G.S, x = S.x, r = rOf(S), col = v => v >= 1 ? '#b8392c' : v >= .7 ? '#d29a2e' : '#27825c', rows = Object.keys(RI).map(id => ({ id, v: r.p[id] || 0 })).sort((p, q) => q.v - p.v), R = ruins(S), cost = R.reduce((p, b) => p + rCost(b), 0);
  let h = '<h3>' + TH_M[(S.m - 1 + 12) % 12] + ' · ฝน ' + Math.round(r.rain) + ' มม. (ปกติ ' + r.norm + ')</h3><div class="bar"><span>แม่น้ำเทียบตลิ่ง</span><i><u style="width:' + Math.round(clamp(r.river) * 100) + '%;background:' + col(r.river) + '"></u></i><b>' + pct(r.river) + '</b></div><p class="muted">น้ำไหลลงแม่น้ำ ' + pct(r.runoff || .3) + ' ของฝน เพราะป่าเหลือ ' + pct(x.forest || 1) + ' · คันกั้นน้ำ ' + (S.k.levee || 0) + ' · อ่างเก็บน้ำ ' + fmt(r.res) + '/' + fmt(S.k.hold || 0) + '</p>';
  if (R.length) h += '<h3>อาคารพังรอซ่อม ' + R.length + ' หลัง</h3><button class="btn gold" style="width:100%" data-a="rrep">ซ่อมทั้งหมด ' + fmt(cost) + ' บาท</button>';
  h += '<h3>ระบบของประเทศ</h3>' + rows.map(q => { const d = RI[q.id], fix = d.fix && q.v >= .55 ? fixPlan(d.fix, d.key, Math.max(1, d.key === 'hold' ? 60 : (d.key === 'school' ? x.kids * 1.2 : x.pop) - (S.k[d.key] || 0))) : null; return '<div class="bar"><span>' + d.n + '</span><i><u style="width:' + Math.round(clamp(q.v) * 100) + '%;background:' + col(q.v) + '"></u></i><b>' + (q.v >= 1 ? 'วิกฤต' : q.v >= .7 ? 'เสี่ยง' : 'ปกติ') + '</b></div><p class="muted" style="margin:-2px 0 3px">' + d.line(S, x, r) + (fix ? ' <button class="chip" data-a="rfix" data-v="' + fix.t + '">สั่งสร้าง' + BT[fix.t].n + '</button>' : '') + '</p>'; }).join('');
  return h;
};
const sheetClick0 = UI.sheetClick;
UI.sheetClick = function (e) {
  const q = e.target.closest('[data-a]'); if (q && q.dataset.a === 'rfix') { UI.closeSheet(); proposeBuild(q.dataset.v); return; }
  if (q && q.dataset.a === 'rrep') { const S = G.S, R = ruins(S), c = R.reduce((p, b) => p + rCost(b), 0); UI.closeSheet(); payOr(c, 'ซ่อมอาคาร ' + R.length + ' หลัง', () => { R.forEach(b => startRepair(b.id)); news('ส่งช่างไปซ่อม ' + R.length + ' หลัง', 'good'); }, () => closeModal()); return; }
  sheetClick0(e);
};
const hud0 = UI.hud; UI.hud = function () { hud0(); const S = G.S, r = S.r; if (!r) return; const n = Object.keys(RI).filter(id => (r.p[id] || 0) >= .7).length, R = Object.values(r.dmg).filter(d => !d.c).length; $('goal').insertAdjacentHTML('beforeend', '<small class="wx">ฝน ' + Math.round(r.rain) + ' มม. · แม่น้ำ ' + pct(r.river) + (n ? ' · เสี่ยง ' + n + ' เรื่อง' : '') + (R ? ' · พัง ' + R + ' หลัง' : '') + '</small>'); };

/* ---------- rain you can see ---------- */
(function () {
  const c = document.createElement('canvas'); c.id = 'rainC'; document.body.appendChild(c); const g = c.getContext('2d'); let w = 0, h = 0, clear = true, last = 0;
  const D = Array.from({ length: 110 }, () => [Math.random(), Math.random(), .6 + Math.random() * .8]);
  function draw(t) {
    requestAnimationFrame(draw); if (t - last < 40) return; const dt = Math.min(.1, (t - last) / 1000); last = t; const S = G.S, r = S && S.r, on = G.started && r ? clamp((r.rain - 110) / 260) : 0; if (!on) { if (!clear) { g.clearRect(0, 0, w, h); clear = true; } return; }
    if (w !== innerWidth || h !== innerHeight) { w = c.width = innerWidth; h = c.height = innerHeight; } g.clearRect(0, 0, w, h); clear = false; g.fillStyle = 'rgba(38,58,84,' + (on * .2).toFixed(3) + ')'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(214,232,246,' + (.24 + on * .3).toFixed(3) + ')'; g.lineWidth = 1.2; g.beginPath(); const n = Math.round(30 + on * 80);
    for (let i = 0; i < n; i++) { const q = D[i]; q[1] += dt * 1.5 * q[2]; if (q[1] > 1) { q[1] -= 1; q[0] = Math.random(); } const x = q[0] * (w + 60) - 30, y = q[1] * h; g.moveTo(x, y); g.lineTo(x - 4, y + 15 * q[2]); } g.stroke();
  }
  requestAnimationFrame(draw);
})();
