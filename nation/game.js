'use strict';
/* ก่อร่างสร้างชาติ: joins the country model to the 3D world: buildings, workers, cities, problems, elections, saves. */
const SAVE_KEY = 'nation_save_v1', SCORE_KEY = 'nation_scores_v1', MAX_BLDS = MOBILE ? 620 : 1150;
const G = { S: null, blds: [], byId: new Map(), nextId: 1, cities: [], speed: 1, time: 0, dayT: 18, dayF: .15, sub: 0, seed: 0, prop: null, modal: false, over: false, news: [], pfBudget: 0, sel: null, started: false, abstract: 0 };
const JOB_N = { farm: 'ชาวนา', bigfarm: 'เกษตรกร', lumber: 'คนตัดไม้', shop: 'พ่อค้าแม่ค้า', market: 'แม่ค้าในตลาด', workshop: 'ช่างในโรงงานเล็ก', factory: 'พนักงานโรงงาน', plant: 'วิศวกรนิคม', office: 'พนักงานออฟฟิศ', cbd: 'นักธุรกิจ', techpark: 'นักพัฒนาเทคโนโลยี', school: 'ครู', hischool: 'ครูมัธยม', univ: 'อาจารย์', clinic: 'พยาบาล', hospital: 'หมอ', medcenter: 'แพทย์เฉพาะทาง', police: 'ตำรวจ', policehq: 'ตำรวจ', base: 'ทหาร', trash: 'พนักงานเก็บขยะ', recycle: 'พนักงานรีไซเคิล', waterworks: 'ช่างประปา', dam: 'ช่างเขื่อน', coal: 'ช่างไฟฟ้า', solar: 'ช่างไฟฟ้า', nuclear: 'วิศวกรนิวเคลียร์', port: 'คนท่าเรือ', airport: 'พนักงานสนามบิน', parliament: 'ข้าราชการ' };
const SHIRTS = [0xd9534f, 0x3f8fd8, 0xf0b93a, 0x3fae6e, 0x8e6bbf, 0xe07b39, 0xf2f0e6, 0x2f9fa8, 0xc9577f], SKINS = [0xf1c9a5, 0xe0ac7c, 0xc98f62, 0xa96f47];
const CITY_NAMES = ['นครธารา', 'เมืองพนา', 'บูรพานคร', 'ศรีสมุทร', 'อุดรธานินทร์', 'ทักษิณบุรี', 'เวียงทอง', 'เมืองแก้ว', 'ภูผานคร'];
const fmt = n => { const a = Math.abs(n), s = n < 0 ? '-' : ''; if (a >= 1e12) return s + (a / 1e12).toFixed(2) + ' ล้านล้าน'; if (a >= 1e9) return s + (a / 1e9).toFixed(2) + ' พันล้าน'; if (a >= 1e6) return s + (a / 1e6).toFixed(2) + ' ล้าน'; return s + Math.round(a).toLocaleString('en-US'); };
const dateOf = m => TH_M[m % 12] + ' ปีที่ ' + (Math.floor(m / 12) + 1);
const pick = l => l[Math.random() * l.length | 0];

function news(t, kind = '') { G.news.unshift({ t, kind, m: G.S ? G.S.m : 0 }); G.news.length = Math.min(G.news.length, 40); if (window.UI) UI.toast(t, kind); }

/* ---------- buildings ---------- */
function makeB(t, spot, city, opt = {}) {
  const def = BT[t] || { s: [3, 3] }, door = spot.door, b = { id: G.nextId++, t, v: opt.v != null ? opt.v : Math.random() * 6 | 0, x: spot.x, z: spot.z, w: spot.w, d: spot.d, rot: door[2], door: [door[0], door[1]], city, prog: 0, done: false, pub: !def.auto, fund: opt.fund || 'priv', urgent: !!opt.urgent };
  G.blds.push(b); G.byId.set(b.id, b); W.occupy(b); const C = G.cities[city]; if (C) C.n++;
  if (opt.instant) finish(b, true); else W.addSite(b);
  return b;
}
function addGive(t, f = 1) { const g = (BT[t] || {}).g; if (g) for (const q in g) G.S.k[q] = (G.S.k[q] || 0) + g[q] * f; }
const RECLAIM_R = 7.5, RECLAIM_BASE = BT.reclaim.c;
function reclaimPrice() { BT.reclaim.c = Math.round(RECLAIM_BASE * (1 + (G.S.landBonus || 0) * .45)); BT.reclaim.m = 40 + (G.S.landBonus || 0) * 12; }
function finishReclaim(b) {
  const S = G.S, cx = b.x + 1.5, cz = b.z + 1.5; W.reclaim(cx, cz, RECLAIM_R); W.removeSite(b);
  for (let a = b.x; a < b.x + b.w; a++) for (let c = b.z; c < b.z + b.d; c++) W.occ[ci(a, c)] = 0; W.reserved[ci(b.door[0], b.door[1])] = 0;
  G.blds.splice(G.blds.indexOf(b), 1); G.byId.delete(b.id); const C = G.cities[b.city]; if (C) C.n = Math.max(0, C.n - 1); if (!S.reclaims) S.reclaims = []; S.reclaims.push([cx, cz]); S.landBonus = (S.landBonus || 0) + 1; applyFx(S, BT.reclaim.fx); reclaimPrice();
  for (const a of W.agents) if (a.site === b.id) { a.site = 0; a.path = null; a.wait = .2; a.moving = false; a.carry = 0; } if (G.sel && G.sel.b === b && window.UI) UI.closeSheet(); news('ถมทะเลสำเร็จ เกาะใหญ่ขึ้นแล้ว!', 'good'); if (window.UI) UI.dirty = true;
}
function finish(b, quiet) {
  if (b.t === 'reclaim') { finishReclaim(b); return; }
  b.done = true; b.prog = 1; W.removeSite(b); W.placeInstance(b); const wasVis = b.vis; if (!wasVis) addGive(b.t); const def = BT[b.t]; if (wasVis) { for (const a of W.agents) if (a.site === b.id) { a.site = 0; a.path = null; a.wait = .2; a.moving = false; a.carry = 0; } return; }
  if (def && def.fx && !quiet) applyFx(G.S, def.fx);
  connectDoor(b);
  if (!quiet && b.pub && def) { news('สร้าง' + def.n + 'เสร็จแล้ว', 'good'); if (window.UI) UI.dirty = true; }
  for (const a of W.agents) if (a.site === b.id) { a.site = 0; a.path = null; a.wait = .2; a.moving = false; a.carry = 0; }
  if (!quiet) assignJobs();
}
/* a new door gets a worn path to the town, so roads link up by themselves */
function connectDoor(b) { const C = G.cities[b.city]; if (!C || (b.t === 'hall')) return; const p = W.path(b.door[0], b.door[1], C.door[0], C.door[1], 1400); if (p) { const w = 7.2 * (1 + (G.S.x.stage || 0) * 1.25); for (const c of p) W.walkOn(c % N, c / N | 0, w); } }
function homes() { return G.blds.filter(b => b.done && BT[b.t] && BT[b.t].g.house); }
function workplaces() { return G.blds.filter(b => b.done && JOB_N[b.t]); }

/* who builds, and how fast: this is the list shown to the player */
function buildFactors(b) {
  const S = G.S, x = S.x, def = BT[b.t], pop = x.pop || 10, LF = x.LF || 5, free = LF * clamp(.46 - Math.log10(pop + 1) * .055, .06, .46) + LF * (x.u || 0) * .6;
  const act = G.blds.filter(q => !q.done).sort((p, q) => (q.urgent - p.urgent) || (p.id - q.id)); let left = Math.max(1.5, free), w = 0;
  for (const q of act) { const n = Math.min(BT[q.t].mw * (q.fund === 'labor' ? 1.3 : 1), left); if (q === b) { w = n; break; } left -= n; if (left <= .05) break; }
  const skill = .72 + .4 * clamp((x.eduY || 2) / 10) + (S.tech - 1) * .06, mood = clamp(.5 + .65 * (x.happy || 60) / 100, .4, 1.1), rainy = S.m % 12 >= 5 && S.m % 12 <= 9, weather = (rainy ? .86 : 1) * (1 - S.drought * .1), road = .78 + .32 * S.road, crowd = w > 1 ? Math.pow(w, .88) / w : 1, mat = S.mat > 0 || b.matOK ? 1 : 0;
  return { w, skill, mood, weather, road, crowd, mat, rainy, sp: w * crowd * skill * mood * weather * road * mat * (b.fund === 'labor' ? .82 : 1) * (b.urgent ? 1.12 : 1) };
}
function stepSites(dtM) {
  const S = G.S; for (const b of G.blds) {
    if (b.done) continue; const def = BT[b.t]; b.f = buildFactors(b); const dp = b.vis ? dtM / 5 : b.f.sp * dtM / def.wk, use = b.vis ? 0 : dp * def.m; b.matOK = true;
    if (use > 0 && S.mat < use) { const miss = use - S.mat, cost = miss * 24, payer = b.pub ? 'treas' : 'priv'; if (S[payer] >= cost) { S[payer] -= cost; S.mat += miss; } else { b.matOK = false; b.f.mat = 0; b.f.sp = 0; continue; } }
    S.mat = Math.max(0, S.mat - use); b.prog = Math.min(1, b.prog + dp); W.siteProgress(b, b.prog); if (b.t === 'reclaim') { const st = Math.floor(b.prog * 4); if (st > (b.rs || 0) && st < 4) { b.rs = st; W.reclaim(b.x + 1.5, b.z + 1.5, RECLAIM_R * st / 4); } } if (b.prog >= 1) finish(b);
  }
}
function placeAuto(t, payer) {
  const S = G.S, def = BT[t]; if (S[payer] < def.c) return false; S[payer] -= def.c;
  const weights = G.cities.map(c => Math.max(1, c.n)), tot = weights.reduce((p, q) => p + q, 0); let r = Math.random() * tot, cIdx = 0; for (let i = 0; i < weights.length; i++) { r -= weights[i]; if (r <= 0) { cIdx = i; break; } }
  const A = W.arch[t + 0]; const noRoom = G.blds.length >= MAX_BLDS || (A && A.list.length > MAX_INST - 8);
  const spot = noRoom ? null : W.findSpot(G.cities[cIdx], t);
  if (!spot) { addGive(t); G.abstract++; return true; }
  makeB(t, spot, cIdx, { fund: payer === 'priv' ? 'priv' : 'treas' }); return true;
}
function autoGrowth() {
  const S = G.S, active = G.blds.filter(b => !b.done && !b.vis).length, cap = 3 + Math.ceil(Math.pow(S.x.pop, .3));
  if (active < cap) for (const t of autoPlan(S).slice(0, cap - active)) placeAuto(t, 'priv');
  if (active < cap + 3) for (const t of ministryPlan(S).slice(0, 3)) placeAuto(t, 'treas');
  /* old huts in the middle turn into proper houses when people can afford it */
  if (S.x.stage >= 2 && S.priv > 900 && Math.random() < .6) { const h = G.blds.find(b => b.t === 'hut' && b.done); if (h) { S.priv -= 300; W.removeInstance(h); addGive('hut', -1); h.t = 'house'; h.done = false; h.prog = 0; h.pub = false; W.addSite(h); } }
}
/* the old low-rise middle of a growing city is rebuilt taller */
const RANK = { hut: 0, house: 1, row: 2, apt: 3, tower: 4, mega: 5, shop: 1, market: 2, workshop: 2, office: 4, cbd: 5, farm: 0, bigfarm: 1 };
function redevelop() {
  const S = G.S, st = S.x.stage; if (st < 3 || G.blds.filter(b => !b.done && b.vis).length >= 8) return;
  const best = st >= 7 ? 5 : st >= 5 ? 4 : st >= 4 ? 3 : 2, L = [];
  for (const b of G.blds) { if (!b.done || b.pub || RANK[b.t] == null) continue; const C = G.cities[b.city], R = Math.sqrt(C.n + 1) * 1.8 + 6, ratio = Math.hypot(b.x + b.w / 2 - C.x, b.z + b.d / 2 - C.z) / R, farm = b.t === 'farm' || b.t === 'bigfarm'; if (farm && (st < 5 || ratio > .42)) continue; const want = Math.max(0, best - (ratio < .34 ? 0 : ratio < .62 ? 1 : ratio < .9 ? 2 : 3)); if (want > RANK[b.t]) L.push([ratio - (want - RANK[b.t]) * .1, b, want]); }
  L.sort((p, q) => p[0] - q[0]);
  for (const [, b, want] of L.slice(0, Math.min(5, st - 1))) {
    const biz = ['shop', 'market', 'workshop', 'office'].includes(b.t) || ((b.t === 'farm' || b.t === 'bigfarm') && b.id % 3 === 0), t = biz ? (want >= 5 && st >= 6 ? 'cbd' : want >= 3 && st >= 4 ? 'office' : null) : HOME_T[Math.min(want, 5)]; if (!t || t === b.t || BT[t].st > st) continue;
    W.removeInstance(b); b.t = t; b.v = Math.random() * 6 | 0; b.vis = 1; b.done = false; b.prog = 0; b.sc = Math.min(1, b.w / BT[t].s[0], b.d / BT[t].s[1]); W.paintPad(b); W.addSite(b);
  }
}
function maybeNewCity() {
  const S = G.S, marks = [3000, 20000, 90000, 400000, 1500000, 4000000, 9000000, 18000000]; if (G.cities.length > marks.length || S.x.pop < marks[G.cities.length - 1]) return;
  let best = null, bs = -1e9;
  for (let i = 0; i < 1400; i++) {
    const x = 8 + Math.random() * (N - 16) | 0, z = 8 + Math.random() * (N - 16) | 0; if (!W.canPlace(x, z, 3, 3)) continue; const dd = Math.min(...G.cities.map(c => Math.hypot(c.x - x, c.z - z))); if (dd < 26) continue; let flat = 0, w = 0;
    for (let a = -8; a <= 8; a += 2) for (let b = -8; b <= 8; b += 2) { if (!inMap(x + a, z + b)) continue; const t = W.T[ci(x + a, z + b)]; if (t === 3 || t === 4) flat++; else if (t === 1) w++; }
    const s = flat + Math.min(w, 5) * 2 - dd * .12; if (s > bs) { bs = s; best = { x, z }; }
  }
  if (!best) return; const door = W.doorFor(best.x, best.z, 3, 3, best.x - 3, best.z); if (!door) return;
  const idx = G.cities.length, C = { x: best.x + 1.5, z: best.z + 1.5, n: 0, name: CITY_NAMES[(idx - 1) % CITY_NAMES.length], door: [door[0], door[1]] }; G.cities.push(C);
  makeB('hall', { x: best.x, z: best.z, w: 3, d: 3, door }, idx, { instant: true, v: 0 });
  const from = G.cities[nearestCity(C, idx)], p = W.path(from.door[0], from.door[1], door[0], door[1], 24000); if (p) for (const c of p) { W.wear[c] = Math.max(W.wear[c], 70); if (!W.road[c]) { W.road[c] = 1; W.paintRoad(c % N, c / N | 0); } }
  news('เกิดเมืองใหม่: ' + C.name + ' รัฐบาลต้องจ้างคนสร้างทางหลวงเชื่อมเมือง', 'good');
}
function nearestCity(C, skip) { let b = 0, d = 1e9; G.cities.forEach((c, i) => { if (i === skip) return; const q = Math.hypot(c.x - C.x, c.z - C.z); if (q < d) { d = q; b = i; } }); return b; }

/* ---------- roads: people wear a trail, the government pays crews to build the real road ---------- */
const ROAD_COST = [0, 0, 6, 22, 70];
function roadTarget(c) { const w = W.wear[c], q = G.S.road, st = G.S.x.stage || 0; return w >= 150 && st >= 3 && q > .5 ? 4 : w >= 55 && st >= 2 && q > .4 ? 3 : w >= 7 ? 2 : 0; }
function planRoads() {
  const L = []; for (let c = 0; c < N * N; c++) { if (W.wear[c] < 7 || W.occ[c] || W.T[c] === 0 || roadTarget(c) <= W.road[c]) continue; const x = c % N, z = c / N | 0; let adj = 0; for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (inMap(x + a, z + b) && W.road[ci(x + a, z + b)] >= 2) adj = 1; const d = Math.min(...G.cities.map(q => Math.hypot(q.x - x, q.z - z))); L.push([W.wear[c] * (adj ? 2.4 : 1) - d * .4, c]); }
  L.sort((p, q) => q[0] - p[0]); const busy = new Set(W.agents.filter(a => a.crew).map(a => a.crew - 1)); G.roadQ = L.slice(0, 70).map(q => q[1]).filter(c => !busy.has(c));
}
function finishRoad(c) { const S = G.S, t = Math.max(2, W.road[c] + 1); if (roadTarget(c) < t || W.occ[c]) return true; const cost = ROAD_COST[t] * Math.sqrt(S.tech); if (S.roadFund < cost) return false; S.roadFund -= cost; W.setRoad(c, t); G.roadDone = (G.roadDone || 0) + 1; return true; }
function roadMonth() {
  const S = G.S, x = S.x; if (!G.roadQ || G.roadQ.length < 12 || S.m % 4 === 0) planRoads(); const has = G.roadQ.length > 0, need = G.roadQ.reduce((q, c) => q + ROAD_COST[Math.max(2, W.road[c] + 1)] * Math.sqrt(S.tech), 0), pay = has ? Math.max(0, Math.min(S.treas, (x.rev || 0) * S.roadPct / 100, need - S.roadFund)) : 0; S.treas -= pay; S.roadFund += pay;
  G.crewN = has ? clamp(Math.ceil(S.roadFund / 13), 0, Math.min(8, Math.ceil((x.LF || 5) * .4))) : 0;
  const jobs = has ? Math.min((x.LF || 5) * .08, pay / 170) : 0; S.k.pub = Math.max(0, S.k.pub + jobs - (S.crewJobs || 0)); S.crewJobs = jobs; G.roadPaid = pay;
  let n = 0; const extra = Math.min(60, Math.floor(x.pop / 120)); while (G.roadQ.length > G.crewN + 2 && n++ < extra) { const c = G.roadQ.pop(); if (!finishRoad(c)) { G.roadQ.push(c); break; } }
}

/* ---------- people on the map ---------- */
function newAgent(age, opt = {}) {
  const sex = opt.sex != null ? opt.sex : Math.random() < .5 ? 0 : 1, last = opt.last || pick(LAST_NAMES);
  const a = { id: G.nextId++, name: (sex ? pick(F_NAMES) : pick(M_NAMES)) + ' ' + last, sex, age, kid: age < 15, shirt: pick(SHIRTS), skin: pick(SKINS), home: 0, job: 0, site: 0, x: 0, z: 0, path: null, pi: 0, wait: Math.random() * 2, moving: false, carry: 0, indoor: false, dir: 0 };
  W.agents.push(a); return a;
}
function placeAgent(a, b) { const d = b ? b.door : G.cities[0].door; a.x = d[0] + .3 + Math.random() * .4; a.z = d[1] + .3 + Math.random() * .4; }
function assignJobs() {
  const adults = W.agents.filter(a => !a.kid && a.age < 66), P = workplaces(), x = G.S.x, u = x.u || 0; if (!P.length) return;
  const weightOf = b => { const g = BT[b.t].g; return (g.ag || 0) + (g.ind || 0) + (g.svc || 0) + (g.pub || 0) + (g.tech || 0); }; const tot = P.reduce((q, b) => q + weightOf(b), 0);
  adults.forEach((a, i) => {
    if (a.job && G.byId.has(a.job) && JOB_N[G.byId.get(a.job).t] && Math.random() > .15) { return; }
    if (i / Math.max(adults.length, 1) < u) { a.job = 0; return; }
    let r = Math.random() * tot; for (const b of P) { r -= weightOf(b); if (r <= 0) { a.job = b.id; break; } }
  });
}
function syncAgents() {
  const pop = Math.round(G.S.x.pop), want = Math.min(MAX_AGENTS, pop), H = homes();
  while (W.agents.length < want) {
    const r = Math.random(), age = r < .3 ? Math.random() * 15 : r < .9 ? 15 + Math.random() * 45 : 60 + Math.random() * 25, a = newAgent(age), h = H.length ? pick(H) : null; a.home = h ? h.id : 0; placeAgent(a, h);
    if (pop <= 60) news((age < 1 ? 'มีเด็กเกิดใหม่: ' : 'คนใหม่ย้ายเข้าเมือง: ') + a.name, 'good');
  }
  while (W.agents.length > want) { const i = Math.random() * W.agents.length | 0, a = W.agents[i]; if (pop <= 60) news(a.name + (a.age > 58 ? ' เสียชีวิตแล้ว' : ' ย้ายออกจากเมือง'), 'bad'); if (G.sel && G.sel.a === a) { G.sel = null; W.ring.visible = false; if (window.UI) UI.closeSheet(); } W.agents.splice(i, 1); }
  for (const a of W.agents) { a.age += 1 / 12; a.kid = a.age < 15; if (a.home && !G.byId.has(a.home)) a.home = 0; if (!a.home && H.length) a.home = pick(H).id; }
}
function agentGo(a, c, then) {
  if (G.pfBudget <= 0) { a.wait = .15; return; } G.pfBudget--; const p = W.path(a.x, a.z, c[0], c[1], 1100);
  if (!p) { a.wait = 1 + Math.random() * 2; a.then = null; return; } if (!p.length) { a.then = then; arrive(a); return; } a.path = p; a.pi = 0; a.moving = true; a.then = then; a.indoor = false;
}
function arrive(a) {
  a.path = null; a.moving = false; const t = a.then; a.then = null;
  if (t === 'home') { a.indoor = true; a.wait = 4 + Math.random() * 4; }
  else if (t === 'work') { const b = G.byId.get(a.job); a.indoor = !!b && !/farm|lumber|park|market/.test(b.t); a.wait = 5 + Math.random() * 7; }
  else if (t === 'school') { a.indoor = true; a.wait = 7 + Math.random() * 5; }
  else if (t === 'tree') { a.wait = 2.2; a.then = 'chop'; const c = a.tree; if (c != null && Math.random() < .22) { W.clearTrees(c % N, c / N | 0, 1, 1); } a.carry = 0x9a6b3f; const b = G.byId.get(a.job); a.after = b ? [b.door[0], b.door[1]] : null; }
  else if (t === 'store') { a.carry = 0xb89a6c; a.wait = .5; a.then = 'haul'; }
  else if (t === 'road') { a.wait = 1.7; a.then = 'paved'; a.carry = 0x8f8a7c; }
  else if (t === 'site') { a.carry = 0; a.wait = 2.2 + Math.random() * 2; }
  else a.wait = 1.5 + Math.random() * 3;
}
function nearTree(a) { for (let i = 0; i < 40; i++) { const r = 2 + Math.random() * 13, t = Math.random() * 6.28, x = Math.round(a.x + Math.cos(t) * r), z = Math.round(a.z + Math.sin(t) * r); if (inMap(x, z) && W.treeAt.has(ci(x, z)) && !W.occ[ci(x, z)]) return [x, z]; } return null; }
function think(a) {
  const night = G.dayF > .68 || G.dayF < .02, H = a.home && G.byId.get(a.home); a.indoor = false;
  if (a.then === 'paved') { a.then = null; const c = a.crew - 1; a.crew = 0; a.crewTry = 0; if (!finishRoad(c) && G.roadQ) G.roadQ.push(c); }
  if (a.crew) { if (++a.crewTry > 4) { if (G.roadQ) G.roadQ.push(a.crew - 1); a.crew = 0; a.crewTry = 0; } else { const c = a.crew - 1; agentGo(a, [c % N, c / N | 0], 'road'); return; } }
  if (!a.kid && !night && a.age < 60 && G.roadQ && G.roadQ.length && (!a.job || Math.random() < .55) && W.agents.filter(q => q.crew).length < (G.crewN || 0)) { const c = G.roadQ.shift(); a.crew = c + 1; a.crewTry = 0; agentGo(a, [c % N, c / N | 0], 'road'); return; }
  if (a.then === 'chop') { a.then = null; if (a.after) { agentGo(a, a.after, 'drop'); return; } a.carry = 0; }
  if (a.then === 'haul') { a.then = null; const b = G.byId.get(a.site); if (b && !b.done) { agentGo(a, b.door, 'site'); return; } a.carry = 0; a.site = 0; }
  a.carry = a.then === 'drop' ? 0 : a.carry; if (!a.moving) a.carry = 0;
  if (night && H) { agentGo(a, H.door, 'home'); return; }
  if (a.kid) { const s = G.blds.find(b => b.done && /school|univ/.test(b.t)); if (s && a.age >= 6 && Math.random() < .7) agentGo(a, s.door, 'school'); else wander(a, H ? H.door : G.cities[0].door, 3); return; }
  const act = G.blds.filter(b => !b.done);
  if (act.length && (!a.job || Math.random() < .42) && a.age < 66) {
    const counts = act.map(b => W.agents.filter(q => q.site === b.id).length), best = act.reduce((p, b, i) => { const s = (BT[b.t].mw - counts[i]) + (b.urgent ? 6 : 0); return s > p.s ? { s, b } : p; }, { s: -99, b: null });
    if (best.b && best.s > 0) { a.site = best.b.id; if (Math.random() < .45) agentGo(a, G.cities[best.b.city].door, 'store'); else agentGo(a, best.b.door, 'site'); return; }
  } else a.site = 0;
  if (a.job) { const b = G.byId.get(a.job); if (b && b.done) { if (b.t === 'lumber') { const t = nearTree(a); if (t) { a.tree = ci(t[0], t[1]); agentGo(a, t, 'tree'); return; } } if (Math.random() < .86) { agentGo(a, b.door, 'work'); return; } } else a.job = 0; }
  const r = Math.random();
  if (r < .34) { const w = G.blds.find(b => b.done && b.t === 'well'); if (w) { agentGo(a, w.door, 'visit'); return; } }
  if (r < .7) { const q = G.blds.filter(b => b.done && /shop|market|park/.test(b.t)); if (q.length) { agentGo(a, pick(q).door, 'visit'); return; } }
  wander(a, H ? H.door : G.cities[0].door, 5);
}
function wander(a, c, r) { for (let i = 0; i < 6; i++) { const x = Math.round(c[0] + (Math.random() - .5) * r * 2), z = Math.round(c[1] + (Math.random() - .5) * r * 2); if (inMap(x, z) && W.T[ci(x, z)] >= 2 && !W.occ[ci(x, z)]) { agentGo(a, [x, z], 'visit'); return; } } a.wait = 2; }
function stepAgents(dt) {
  const q = G.S.road, wt = Math.min(10, Math.sqrt(Math.max(1, G.S.x.pop / Math.max(W.agents.length, 1))));
  for (const a of W.agents) {
    if (a.path) {
      const c = a.path[a.pi], tx = c % N + .5, tz = (c / N | 0) + .5, dx = tx - a.x, dz = tz - a.z, d = Math.hypot(dx, dz), rt = W.road[c], sp = (a.kid ? 1.25 : 1.5) * (1 + rt * .12) * dt;
      if (d <= sp) { a.x = tx; a.z = tz; W.walkOn(c % N, c / N | 0, wt * .28, q); if (++a.pi >= a.path.length) arrive(a); } else { a.x += dx / d * sp; a.z += dz / d * sp; a.dir = Math.atan2(dx, dz); }
    } else { a.wait -= dt; if (a.wait <= 0) think(a); }
  }
}

/* ---------- problems ---------- */
function eligible() {
  const S = G.S, x = S.x; return EV.filter(e => x.pop >= e.p && S.m >= (S.lastEv[e.id] != null ? S.lastEv[e.id] + e.cd * 12 : 0) && (() => { try { return e.when(x); } catch (q) { return false; } })());
}
function nextProblem() {
  const S = G.S, gap = S.m < 24 ? 3 : clamp(5 - S.x.stage * .25, 3, 5); if (G.modal || S.m - S.evM < gap) return;
  const L = eligible(); if (!L.length) return; L.sort((p, q) => (S.lastEv[p.id] != null ? 1 : 0) - (S.lastEv[q.id] != null ? 1 : 0) || Math.random() - .5); const e = L[0]; S.lastEv[e.id] = S.m; S.evM = S.m; UI.showEvent(e);
}
function answerEvent(e, o) {
  const S = G.S, fx = o[1], plain = {}; for (const q in fx) if (q !== 'build') plain[q] = fx[q]; applyFx(S, plain); S.x.pop && (S.x.trust = S.trust); UI.dirty = true;
  if (fx.build === 'auto_house') { for (let i = 0; i < 3; i++) { const t = tierPick(HOME_T, S.x.stage, S.x.pop * .05, 'house'); S.priv += BT[t].c; placeAuto(t, 'priv'); } }
  else if (fx.build) { const t = bestOfCat(fx.build); if (t) setTimeout(() => proposeBuild(t, true), 180); }
}
function bestOfCat(t) { const st = G.S.x.stage; if (BT[t].st <= st) return t; const c = BT[t].cat; const L = PUBLIC_ORDER.filter(q => BT[q].cat === c && BT[q].st <= st); return L[L.length - 1] || null; }

/* ---------- ordering a public project: the people choose the place, you approve the money ---------- */
function proposeBuild(t, urgent) {
  let idx = 0, bs = 1e9; G.cities.forEach((c, i) => { const q = Math.hypot(c.x - W.cam.tx, c.z - W.cam.tz); if (q < bs) { bs = q; idx = i; } });
  const land = t === 'reclaim', spot = land ? W.findCoast(G.cities[idx]) : W.findSpot(G.cities[idx], t); if (!spot) { news(land ? 'ไม่มีชายฝั่งที่ถมได้ใกล้เมืองนี้แล้ว' : 'ไม่มีที่เหมาะสำหรับ' + BT[t].n, 'bad'); return; }
  const cx = spot.x + spot.w / 2, cz = spot.z + spot.d / 2, H = homes().filter(b => Math.hypot(b.x - cx, b.z - cz) < 9).length, why = [];
  if (land) { why.push('ชายฝั่งใกล้เมือง'); why.push(W.h(cx, cz) > -.9 ? 'น้ำตื้น ถมง่าย' : 'น้ำค่อนข้างลึก'); if (H) why.push('ใกล้บ้าน ' + H + ' หลัง'); } else { if (H) why.push('ใกล้บ้าน ' + H + ' หลัง'); if (W.h(cx, cz) > .28) why.push('ที่สูง น้ำไม่ท่วม'); else why.push('ที่ราบ สร้างง่าย'); if (spot.rw) why.push('ใกล้แหล่งน้ำ'); if (W.road[ci(spot.door[0], spot.door[1])] >= 1) why.push('ติดทางเดิน'); }
  G.prop = { t, spot, city: idx, why, urgent: !!urgent }; W.ring.visible = true; W.ring.scale.setScalar(land ? RECLAIM_R : Math.max(spot.w, spot.d) * .85); W.ring.position.set(cx, Math.max(.16, W.h(cx, cz) + .18), cz); W.fly(cx, cz, land ? Math.max(30, Math.min(W.cam.tDist, 44)) : Math.min(W.cam.tDist, 24)); UI.showProposal(G.prop);
}
const FUNDS = {
  treas: ['ใช้เงินคลัง', 'จ่ายเต็ม สร้างได้ทันที'],
  labor: ['ลงแขกช่วยกัน', 'จ่าย 35% ชาวเมืองมาช่วย แต่ช้ากว่าและงานอื่นชะงัก'],
  loan: ['กู้เงิน', 'ได้ทันที แต่เป็นหนี้และมีดอกเบี้ย'],
  grant: ['ขอทุนต่างประเทศ', 'ฟรี แต่รอหลายเดือน และอาจถูกปฏิเสธ'],
  ppp: ['ให้เอกชนลงทุน', 'รัฐไม่จ่าย แต่ประชาชนจ่ายค่าบริการและเหลื่อมล้ำขึ้น']
};
function fundOK(t, f) { const S = G.S, c = BT[t].c; if (f === 'treas') return S.treas >= c; if (f === 'labor') return S.treas >= c * .35 && c <= 3000; if (f === 'loan') return S.debt + c <= Math.max(S.gdp * 18, 1600); if (f === 'grant') return !S.grantWait; if (f === 'ppp') return S.priv >= c * .7 && ['water', 'power', 'life', 'clean', 'land'].includes(BT[t].cat); return false; }
function approve(f) {
  const P = G.prop, S = G.S; if (!P || !fundOK(P.t, f)) return; const c = BT[P.t].c;
  if (f === 'treas') S.treas -= c; else if (f === 'labor') { S.treas -= c * .35; S.mods.push({ v: -1.5, u: S.m + 3 }); } else if (f === 'loan') S.debt += c; else if (f === 'ppp') { S.priv -= c * .7; applyFx(S, { hp: -2, gini: .006 }); }
  else if (f === 'grant') { S.grantWait = { t: P.t, m: S.m + 4 + (Math.random() * 5 | 0) }; news('ส่งคำขอทุนสร้าง' + BT[P.t].n + ' แล้ว รอผลหลายเดือน'); cancelProp(); return; }
  const b = makeB(P.t, P.spot, P.city, { fund: f, urgent: P.urgent }); news('อนุมัติ: ' + BT[P.t].n + ' ชาวเมืองกำลังไปสร้าง'); cancelProp(); UI.dirty = true; return b;
}
function cancelProp() { G.prop = null; if (!G.sel) W.ring.visible = false; UI.closeProposal(); }

/* ---------- the throne: no elections, but a ruler can still fall ---------- */
function throneCheck() {
  const S = G.S, u = S.unrest || 0;
  if (u >= 100) { const army = S.bud.defense < .3; UI.showEnd(army ? 'กองทัพก่อรัฐประหาร' : 'ประชาชนลุกฮือโค่นล้มคุณ', army ? 'ทหารไม่พอใจจนยึดอำนาจจากคุณ' : 'ผู้คนทนไม่ไหวและบุกเข้าทำเนียบ ยุคของคุณจบลงแล้ว'); return; }
  if (u >= 75 && !S.warn75) { S.warn75 = 1; news('บัลลังก์สั่นคลอน! ถ้าความไม่สงบถึง 100% คุณจะถูกโค่นล้ม', 'bad'); }
  if (u < 60) S.warn75 = 0;
}

/* ---------- scores ---------- */
function loadScores() { try { return JSON.parse(localStorage.getItem(SCORE_KEY)) || []; } catch (e) { return []; } }
function saveScore() { const S = G.S, x = S.x, L = loadScores().filter(q => q.id !== G.seed), e = { id: G.seed, n: S.name, score: Math.max(S.best, x.score || 0), st: S.stageMax, y: Math.floor(S.m / 12), pop: Math.round(x.pop || 0), me: 1 }; L.push(e); L.sort((p, q) => q.score - p.score); try { localStorage.setItem(SCORE_KEY, JSON.stringify(L.slice(0, 30))); } catch (q) {} }
function ranking() { const S = G.S, y = S ? S.m / 12 : 0, L = RIVALS.map(r => ({ n: r[0], score: Math.round(r[1] + r[2] * y), rival: 1 })), past = loadScores().filter(q => !S || q.id !== G.seed); past.forEach(q => L.push({ n: q.n + (q.friend ? ' (เพื่อน)' : ' (เกมก่อน)'), score: q.score, past: 1 })); if (S) L.push({ n: S.name, score: S.x.score || 0, me: 1 }); return L.sort((p, q) => q.score - p.score); }
function shareLink() { const S = G.S, q = { n: S.name, s: Math.max(S.best, S.x.score || 0), st: S.stageMax, y: Math.floor(S.m / 12) }; const code = btoa(unescape(encodeURIComponent(JSON.stringify(q)))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); return location.origin + location.pathname + '?vs=' + code; }
function readFriend() { try { const c = new URLSearchParams(location.search).get('vs'); if (!c) return; const o = JSON.parse(decodeURIComponent(escape(atob(c.replace(/-/g, '+').replace(/_/g, '/'))))); if (typeof o.s !== 'number' || !isFinite(o.s) || o.s < 0 || o.s > 1e6) return; const name = String(o.n || 'เพื่อน').slice(0, 24), L = loadScores().filter(q => !(q.friend && q.n === name)); L.push({ id: 'f' + name, n: name, score: Math.round(o.s), st: clamp(o.st | 0, 0, 9), y: o.y | 0, friend: 1 }); L.sort((p, q) => q.score - p.score); localStorage.setItem(SCORE_KEY, JSON.stringify(L.slice(0, 30))); G.friend = name; } catch (e) {} }

/* ---------- save / load ---------- */
function saveGame() {
  if (!G.S || G.over) return; try {
    const roads = []; for (let i = 0; i < N * N; i++) if (W.road[i] || W.wear[i] > 1) roads.push(i, W.road[i], Math.round(W.wear[i]));
    localStorage.setItem(SAVE_KEY, JSON.stringify({ S: G.S, seed: G.seed, nextId: G.nextId, cities: G.cities, roads, blds: G.blds.map(b => [b.id, b.t, b.v, b.x, b.z, b.w, b.d, b.rot, b.door[0], b.door[1], b.city, +b.prog.toFixed(3), b.done ? 1 : 0, b.pub ? 1 : 0, b.fund, b.urgent ? 1 : 0, b.vis ? 1 : 0, b.sc || 1]), ppl: W.agents.map(a => [a.name, a.sex, +a.age.toFixed(1), a.shirt, a.skin]) }));
  } catch (e) {}
}
function hasSave() { try { return !!localStorage.getItem(SAVE_KEY); } catch (e) { return false; } }
function loadGame() {
  let D; try { D = JSON.parse(localStorage.getItem(SAVE_KEY)); } catch (e) { return false; } if (!D || !D.S || D.S.v !== 1) return false;
  G.seed = D.seed; W.init(document.getElementById('cv'), G.seed); G.S = D.S; G.nextId = D.nextId; G.cities = D.cities; G.cities.forEach(c => { c.n = 0; }); const keep = { ...G.S.k }; for (const r of G.S.reclaims || []) W.reclaim(r[0], r[1], RECLAIM_R);
  for (const r of D.blds) { const b = { id: r[0], t: r[1], v: r[2], x: r[3], z: r[4], w: r[5], d: r[6], rot: r[7], door: [r[8], r[9]], city: r[10], prog: r[11], done: !!r[12], pub: !!r[13], fund: r[14], urgent: !!r[15], vis: r[16] ? 1 : 0, sc: r[17] || 1 }; G.blds.push(b); G.byId.set(b.id, b); W.occupy(b); G.cities[b.city].n++; if (b.done) W.placeInstance(b); else { W.addSite(b); W.siteProgress(b, b.prog); } }
  G.S.k = keep; reclaimPrice(); for (const b of G.blds) if (b.t === 'reclaim' && b.prog > 0) { b.rs = Math.min(3, Math.floor(b.prog * 4)); if (b.rs) W.reclaim(b.x + 1.5, b.z + 1.5, RECLAIM_R * b.rs / 4); } for (let i = 0; i < D.roads.length; i += 3) { W.road[D.roads[i]] = D.roads[i + 1]; W.wear[D.roads[i]] = D.roads[i + 2]; if (D.roads[i + 1] >= 2) W.roadCount++; } for (let i = 0; i < D.roads.length; i += 3) if (D.roads[i + 1]) W.paintRoad(D.roads[i] % N, D.roads[i] / N | 0);
  const H = homes(); for (const p of D.ppl) { const a = newAgent(p[2], { sex: p[1] }); a.name = p[0]; a.shirt = p[3]; a.skin = p[4]; const h = H.length ? pick(H) : null; a.home = h ? h.id : 0; placeAgent(a, h); }
  assignJobs(); W.fly(G.cities[0].x, G.cities[0].z, 28); W.needShadow = true; return true;
}
function newGame(name) {
  try { localStorage.removeItem(SAVE_KEY); } catch (e) {}
  G.seed = (Date.now() ^ (Math.random() * 1e9)) >>> 0; const q = new URLSearchParams(location.search).get('seed'); if (q) G.seed = +q >>> 0;
  W.init(document.getElementById('cv'), G.seed); const S = G.S = newState(name), st = W.start; reclaimPrice();
  let hs = null; for (let r = 0; r < 18 && !hs; r++) for (let i = 0; i < 40 && !hs; i++) { const x = st.x + Math.round((Math.random() - .5) * r * 2), z = st.z + Math.round((Math.random() - .5) * r * 2); if (W.canPlace(x, z, 3, 3)) { const door = W.doorFor(x, z, 3, 3, x, z + 9); if (door) hs = { x, z, w: 3, d: 3, door }; } }
  if (!hs) hs = { x: st.x, z: st.z, w: 3, d: 3, door: [st.x + 1, st.z + 3, 0] };
  G.cities = [{ x: hs.x + 1.5, z: hs.z + 1.5, n: 0, name: name, door: [hs.door[0], hs.door[1]] }];
  makeB('hall', hs, 0, { instant: true, v: 0 });
  for (const t of ['hut', 'hut', 'hut', 'farm', 'lumber']) { const sp = W.findSpot(G.cities[0], t, 7); if (sp) makeB(t, sp, 0, { instant: true }); else addGive(t); }
  const fam = [[62, 1], [41, 0], [38, 1], [12, 1], [9, 0], [34, 0], [31, 1], [6, 0], [27, 0], [3, 1]], H = homes(), lasts = [pick(LAST_NAMES), pick(LAST_NAMES), pick(LAST_NAMES)], who = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2];
  fam.forEach((f, i) => { const a = newAgent(f[0], { sex: f[1], last: lasts[who[i]] }), h = H[who[i]] || H[0]; a.home = h ? h.id : 0; placeAgent(a, h); });
  stepModel(S); S.m = 0; S.month = { born: 0, died: 0, inM: 0, outM: 0, noKid: 0 }; assignJobs(); W.fly(hs.x + 1.5, hs.z + 1.5, 24); W.needShadow = true;
}

/* ---------- monthly + per-frame clock ---------- */
function monthTick() {
  const S = G.S; S.k.roadC = W.roadCount; S.forestBase = clamp(W.treeLive / W.treeTotal); S.month = { born: 0, died: 0, inM: 0, outM: 0, noKid: 0 };
  const before = S.x.stage, x = stepModel(S); nationalWorks(S); roadMonth();
  for (let i = S.later.length - 1; i >= 0; i--) { const q = S.later[i]; if (q.m <= S.m) { applyFx(S, q.fx); if (q.news) news(q.news, q.fx.tr < 0 || q.fx.food < 0 ? 'bad' : 'good'); if (q.vis === 'flood') G.floodT = 14; S.later.splice(i, 1); } }
  if (S.grantWait && S.m >= S.grantWait.m) { const t = S.grantWait.t, ok = Math.random() < clamp(.42 + S.rep * .7 + (x.trust - 50) * .006, .15, .95); S.grantWait = null; if (ok) { S.treas += BT[t].c; news('ได้รับทุนสร้าง' + BT[t].n + ' แล้ว! สั่งสร้างได้เลย', 'good'); } else news('คำขอทุนสร้าง' + BT[t].n + ' ถูกปฏิเสธ', 'bad'); }
  autoGrowth(); redevelop(); if (S.m % 6 === 0) { maybeNewCity(); } syncAgents(); if (S.m % 3 === 0) assignJobs();
  if (S.m % 3 === 0) { S.hist.push([S.m, Math.round(x.pop), Math.round(x.idx), Math.round(x.gdpPc), Math.round(x.happy), x.score]); if (S.hist.length > 260) S.hist.splice(0, 2).length; }
  if (x.stage > before && x.stage === S.stageMax) UI.showStage(x.stage);
  if (x.pop < 1.2) { UI.showEnd('ประเทศร้างผู้คน', 'ไม่เหลือใครอยู่ในประเทศแล้ว'); return; }
  throneCheck(); if (!G.over) nextProblem();
  if (S.m % 4 === 0) { saveGame(); saveScore(); } UI.dirty = true;
}
function tick(dt) {
  if (!G.started || G.over) return; G.dayT += dt; G.dayF = (G.dayT % 84) / 84; G.pfBudget = 9;
  const run = !G.modal && !G.prop && G.speed > 0;
  if (run) {
    const sim = dt * G.speed; stepSites(sim / MONTH_S); G.sub += sim; let guard = 0; while (G.sub >= MONTH_S && guard++ < 4 && !G.over) { G.sub -= MONTH_S; monthTick(); if (G.modal || G.prop) break; }
    stepAgents(Math.min(.25, dt * Math.min(G.speed, 4)));
  }
}
