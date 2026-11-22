'use strict';
/* ก่อร่างสร้างชาติ: the country model. No DOM and no 3D here, so the future forecast and balance tests can run it alone. */
const clamp = (v, a = 0, b = 1) => v < a ? a : v > b ? b : v;
const HOME_T = ['hut', 'house', 'row', 'apt', 'tower', 'mega'];
const K_ZERO = () => ({ house: 0, ag: 0, ind: 0, svc: 0, tech: 0, pub: 0, matp: 0, dirty: 0, water: 0, power: 0, school: 0, hosp: 0, safe: 0, trash: 0, park: 0, port: 0, air: 0, admin: 0, army: 0, rnd: 0, roadC: 0 });

function newState(name) {
  const age = new Array(91).fill(0);
  [62, 41, 38, 34, 31, 27, 12, 9, 6, 3].forEach(a => { age[a] += 1; });
  return {
    v: 1, name, m: 0, age, eduY: 2.4, hq: 18, sick: .035, tech: 1, treas: 2600, debt: 0, priv: 900, mat: 34, food: 42,
    tax: { inc: 5, corp: 10, vat: 5 }, bud: { edu: .7, health: .7, safety: .5, infra: .7, welfare: .4, env: .4, defense: .2, rnd: .1, admin: .5 },
    k: K_ZERO(), P: .03, crime: .05, gini: .3, corr: .08, trust: 62, happy: 60, cpi: 1, pFood: 40, infl: .002, inflShock: 0, road: .35, hunger: 0, epi: 0,
    war: 0, tension: .05, rep: .3, drought: 0, tfrAdd: 0, transit: 0, forestBase: 1, forestAdj: 0, adj: { pol: 0, crime: 0, corr: 0, gini: 0, hq: 0 }, mods: [], later: [],
    gdp: 700, x: {}, hist: [], stats: { born: 0, died: 0, inM: 0, outM: 0, noKid: 0 }, month: { born: 0, died: 0, inM: 0, outM: 0, noKid: 0 }, reclaims: [], landBonus: 0, roadPct: 20, roadFund: 0, crewJobs: 0, best: 0, lastEv: {}, evM: 0, term: 1, nextVote: 48, promise: null, stageMax: 0
  };
}

function ageGroups(a) {
  let kids = 0, work = 0, old = 0, fem = 0, stu = 0;
  for (let i = 0; i < 91; i++) { const v = a[i]; if (i < 15) kids += v; else if (i < 65) work += v; else old += v; if (i >= 15 && i < 45) fem += v * .5; if (i >= 6 && i < 23) stu += v; }
  return { kids, work, old, fem, stu, pop: Math.max(.01, kids + work + old) };
}

function devIndex(x) {
  const inc = clamp(Math.log((x.gdpPc + 20) / 100) / Math.log(3200 / 100), .02, 1), edu = clamp(x.eduY / 14, .04, 1), hl = clamp((x.LE - 40) / 45, .04, 1);
  const env = clamp(1 - x.P * 1.1, .1, 1), stab = clamp((1 - x.crime * 1.2) * (.45 + x.trust / 180) * (1 - clamp(x.debtRatio - .9) * .4), .1, 1);
  return 1000 * Math.pow(inc, .32) * Math.pow(edu, .24) * Math.pow(hl, .24) * Math.pow(env, .09) * Math.pow(stab, .11);
}
const scoreOf = x => Math.round(x.idx * (1 + Math.log10(Math.max(x.pop, 1))) * (1 + x.stage * .08));
function stageOf(pop, idx) { let s = 0; for (let i = 0; i < STAGES.length; i++) if (pop >= STAGES[i].p && idx >= STAGES[i].i) s = i; return s; }

/* One game month for the whole country. */
function stepModel(S) {
  const a = S.age, k = S.k, b = S.bud, t = S.tax, G0 = ageGroups(a), pop = G0.pop, m = S.stats && S.month;
  const LF = Math.max(.5, G0.work * .82 + G0.old * .06), skill = clamp((S.eduY - 5) / 9);
  const dem = clamp(.955 + .04 * Math.sin(S.m / 31) + .022 * Math.sin(S.m / 9.7) + (S.shock || 0), .6, 1.05); S.shock = (S.shock || 0) * .95;
  const techE = Math.min(k.tech, LF * skill), oth = k.ag + (k.ind + k.svc) * dem + k.pub, othE = Math.min(oth, LF - techE), fill = oth > 0 ? othE / oth : 0;
  const E = { ag: k.ag * fill, ind: k.ind * dem * fill, svc: k.svc * dem * fill, pub: k.pub * fill };
  const emp = techE + othE, u = clamp(1 - emp / LF);
  const pw = clamp(k.power / (pop * .7 + E.ind * .6 + techE + 1)), cleanW = clamp(k.water / pop), wr = clamp((k.water + 14) / (pop + 1)), clean = clamp((k.trash + 26) / (pop + 1));
  const safeCov = clamp((k.safe + 22) / (pop + 1)), hospCov = clamp(k.hosp / (pop + 1)), schoolCov = clamp(k.school / (G0.stu + 1)), houseRatio = k.house / pop, parkCov = clamp((k.park + 8) / (pop + 1));
  const dirtyShare = k.dirty * fill / (pop + 30), prevPc = S.gdp / pop, car = pop * clamp(prevPc / 1300);
  const cong = clamp(car / (k.roadC * 42 + 180) - .5 - S.transit);
  const trade = 1 + .05 * Math.min(k.port, 4) + .05 * Math.min(k.air, 3) + .08 * (S.rep - .35), pwF = .74 + .26 * pw;
  const prod = (.62 + S.eduY / 11) * S.tech * (.72 + .28 * S.road) * (1 - cong * .16) * (1 - S.sick * .7) * (S.war > 0 ? .85 : 1) * trade;
  const gdp = Math.max(1, prod * (E.ag * 190 + (E.ind * 330 + E.svc * 270 + techE * 950) * pwF + E.pub * 240)), gdpPc = gdp / pop;
  const eff = 1 - S.corr * .7;
  /* government money */
  const rev = gdp * (.62 * t.inc + .38 * t.corp + .7 * t.vat) / 100 * (1 - S.corr * .55) * (.72 + .28 * S.trust / 100);
  let spend = 0; for (const q in BUDGET_N) spend += gdp * b[q] * BUDGET_N[q][1] / 100;
  const debtRatio0 = S.debt / Math.max(gdp * 12, 1), interest = S.debt * (.0035 + .012 * Math.max(0, debtRatio0 - .6));
  S.treas += rev - spend - interest;
  if (S.treas > gdp * 3 && S.debt > 0) { const pay = Math.min(S.debt, (S.treas - gdp * 3) * .3); S.debt -= pay; S.treas -= pay; }
  if (S.treas < 0) { S.debt += -S.treas * 1.02; S.treas = 0; S.trust -= .4; }
  S.priv += gdp * .38 * (1 - t.corp / 100) * .46 + gdp * .018 * S.rep;
  /* food + materials */
  const yieldF = (1 + (S.tech - 1) * .4) * (.72 + .28 * wr) * (1 - S.drought * .55) * (1 - S.P * .25), foodOut = E.ag * 3.2 * yieldF;
  S.food += foodOut - pop; let hungerNow = 0;
  if (S.food < 0) { const miss = -S.food, can = gdp * .35 / (S.pFood * 1.6), got = Math.min(miss, can); hungerNow = (miss - got) / pop; S.priv = Math.max(0, S.priv - got * S.pFood * .6); S.food = 0; }
  S.food = Math.min(S.food, pop * 5 + 40); S.hunger += (hungerNow - S.hunger) * .5; S.drought *= .93;
  const foodMonths = S.food / pop; S.pFood += (40 * clamp(1.6 / (foodMonths + .4), .7, 3) - S.pFood) * .3;
  S.mat = Math.min(S.mat + k.matp * fill, 3000 + pop * 2);
  /* prices */
  const defGDP = (spend + interest - rev) / gdp, press = .0015 + Math.max(0, defGDP) * .012 + S.hunger * .02 + Math.max(0, 1 - houseRatio) * .003 + (S.war > 0 ? .006 : 0) + Math.max(0, .05 - u) * .02;
  S.infl += (press + S.inflShock - S.infl) * .18; S.inflShock *= .85; S.cpi *= 1 + S.infl;
  /* slow things that build a country */
  for (const q in S.adj) S.adj[q] *= .975;
  S.eduY += (1 + 13.6 * schoolCov * clamp((b.edu * eff + .25) / 1.1) - S.eduY) * .012;
  S.hq += (clamp(14 + 84 * hospCov * clamp((b.health * eff + .3) / 1.15) + S.adj.hq, 5, 99) - S.hq) * .05;
  S.road += (clamp(.3 + .55 * Math.min(1.25, b.infra * eff)) - S.road) * .025;
  S.epi = Math.max(0, S.epi * .9);
  S.sick += (clamp((.015 + .08 * (1 - cleanW) + .05 * (1 - clean) + .08 * S.P + .1 * S.hunger + Math.max(0, .85 - houseRatio) * .08) * (1 - S.hq / 160) + S.epi, .002, .6) - S.sick) * .25;
  const forest = clamp(S.forestBase + S.forestAdj);
  S.P += (clamp(.02 + dirtyShare * .85 + (1 - clean) * .12 + clamp(car / (pop + 1)) * .1 - .12 * Math.min(1.4, b.env * eff) - .1 * (forest - .5) - parkCov * .03 + S.adj.pol, .005, .95) - S.P) * .035;
  S.gini += (clamp(.3 + .22 * (k.ind + k.tech * 1.2) / (LF + 5) * .45 - .12 * Math.min(1.4, b.welfare) + .16 * S.corr + .05 * Math.log(S.tech) + S.adj.gini, .18, .75) - S.gini) * .025;
  S.corr += (clamp(.055 + .022 * Math.log10(pop + 1) - .09 * b.admin - .04 * Math.min(1, k.admin) + S.adj.corr, .01, .8) - S.corr) * .025;
  S.crime += (clamp(.03 + .55 * u + .25 * Math.max(0, S.gini - .3) + .25 * S.hunger + .1 * (1 - safeCov) - .08 * Math.min(1.5, b.safety * eff) * safeCov + S.adj.crime, .005, .9) - S.crime) * .06;
  const taxLoad = t.inc + t.corp * .35 + t.vat * 1.1;
  const LE = clamp(44 + .36 * S.hq + 8 * clamp(Math.log((gdpPc + 1) / 120) / Math.log(20)) - 22 * S.P - 35 * S.hunger - 30 * S.epi - (S.war > 0 ? 3 : 0), 25, 90);
  /* happiness */
  S.mods = S.mods.filter(q => q.u > S.m); const modSum = S.mods.reduce((q, r) => q + r.v, 0);
  const hapT = 100 * (.17 * clamp(1 - u * 3) + .14 * clamp(1 - S.hunger * 4) * clamp(foodMonths + .55) + .1 * clamp(.35 + .65 * cleanW) + .12 * clamp(.2 + .8 * S.hq / 75) + .08 * clamp(.3 + .7 * schoolCov) + .09 * clamp(1 - S.crime * 2.4) + .1 * clamp(houseRatio - .15) + .07 * clamp(Math.log((gdpPc + 20) / 90) / Math.log(18)) + .05 * clamp(1 - S.P * 2) + .04 * parkCov + .04 * clamp(S.road)) + modSum - Math.max(0, taxLoad - 25) * .8 - Math.max(0, S.infl - .006) * 900 - (S.war > 0 ? 9 : 0);
  S.happy += (clamp(hapT, 3, 99) - S.happy) * .12;
  const debtRatio = S.debt / Math.max(gdp * 12, 1);
  S.trust += (clamp(24 + .68 * S.happy - 46 * S.corr - 8 * clamp(debtRatio - 1) + .14 * (S.rep * 100 - 30), 3, 98) - S.trust) * .05;
  S.rep = clamp(S.rep + (.45 * (S.trust / 100) + .15 * clamp(gdpPc / 1800) - .03 * (S.war > 0) - S.rep) * .006, .01, 1);
  S.tech *= 1 + (.004 + .022 * clamp(S.eduY / 12) * (1 - S.corr) + .018 * Math.min(1.6, b.rnd * eff) + .012 * Math.min(k.rnd, 2) + .05 * techE / Math.max(LF, 1) + .003 * Math.min(k.port + k.air, 4)) / 12 * (S.war > 0 ? .4 : 1) / (1 + S.tech / 9);
  S.tension = clamp(S.tension + (.05 + .02 * clamp(Math.log10(pop + 1) / 7) - .03 * Math.min(1.5, b.defense) - S.tension) * .012 + (S.war > 0 ? -.002 : 0), 0, 1);
  if (S.war > 0) S.war--;
  /* people: born, die, move */
  const mult = clamp((90 - LE) / 30, .12, 3); let died = 0;
  for (let i = 0; i < 91; i++) { const q = Math.min(.5, (.00045 * Math.exp(.088 * i) + (i < 2 ? .035 : 0)) * mult + (S.war > 0 && i >= 18 && i < 42 ? .012 * (1 - .6 * Math.min(1, k.army + b.defense * .4)) : 0)); const d = a[i] * q / 12; a[i] -= d; died += d; }
  const tfrBase = 1.45 + 4.1 * Math.exp(-S.eduY / 4.2), econ = clamp(1 - u * 1.7) * clamp(.45 + .55 * houseRatio / 1.02) * clamp(1 - S.hunger * 2.4) * (S.war > 0 ? .75 : 1) * clamp(.7 + .5 * gdpPc / 240, .55, 1.05) * (1 + (b.welfare - .6) * .12);
  const tfr = Math.max(.25, (tfrBase + S.tfrAdd) * econ), born = G0.fem * tfr / 30 / 12, noKid = Math.max(0, G0.fem * (tfrBase - tfr) / 30 / 12);
  const A = .28 + .45 * clamp(Math.log((gdpPc + 40) / 300), -1, 1) - 1.5 * Math.max(0, u - .06) + .25 * (safeCov - .7) + .25 * (hospCov - .5) + .15 * (schoolCov - .5) + .35 * clamp(houseRatio - 1, -.6, .2) + .35 * (S.happy - 55) / 45 - .9 * S.crime - .6 * S.P - 1.5 * S.hunger - (S.war > 0 ? .5 : 0);
  const room = clamp((k.house * 1.1 - pop) / (pop * .05 + 2), .07, 1), inM = Math.max(0, A + (pop < 120 ? .12 : 0)) * (.85 + pop * .016 / (1 + pop / 3e6)) * clamp(1 - pop / (1.1e8 + (S.landBonus || 0) * 1.5e6)) * room, outM = Math.max(0, -A) * pop * .024 + pop * Math.max(0, u - .2) * .022;
  for (let i = 90; i > 0; i--) { const mv = a[i - 1] / 12; a[i] += mv; a[i - 1] -= mv; }
  a[0] += born;
  for (let i = 20; i < 40; i++) a[i] += inM * .65 / 20;
  for (let i = 0; i < 15; i++) a[i] += inM * .35 / 15;
  let mvb = 0; for (let i = 18; i < 46; i++) mvb += a[i];
  if (mvb > 0) { const f = Math.min(.5, outM / mvb); for (let i = 18; i < 46; i++) a[i] *= 1 - f; }
  if (S.month) { const q = S.month; q.born += born; q.died += died; q.inM += inM; q.outM += Math.min(outM, mvb * .5); q.noKid += noKid; const r = S.stats; r.born += born; r.died += died; r.inM += inM; r.outM += Math.min(outM, mvb * .5); r.noKid += noKid; }
  S.gdp = gdp; S.m++;
  const G1 = ageGroups(a);
  const x = S.x = { m: S.m, pop: G1.pop, kids: G1.kids, work: G1.work, old: G1.old, oldShare: G1.old / G1.pop, LF, emp, u, gdp, gdpPc, E_ag: E.ag, E_ind: E.ind, E_svc: E.svc, E_pub: E.pub, E_tech: techE, cleanW, clean, wr, pw, safeCov, hospCov, schoolCov, houseRatio, parkCov, foodMonths, foodOut, dirtyShare, cong, eduY: S.eduY, hq: S.hq, sick: S.sick, P: S.P, crime: S.crime, gini: S.gini, corr: S.corr, trust: S.trust, happy: S.happy, infl: S.infl, tech: S.tech, debtRatio, taxLoad, k, tfr, rep: S.rep, tension: S.tension, forest, army: k.army, treas: S.treas, rev, spend, interest, LE, A, war: S.war, hunger: S.hunger };
  x.land = S.landBonus || 0; x.idx = devIndex(x); x.stage = stageOf(x.pop, x.idx); x.score = scoreOf(x); S.best = Math.max(S.best, x.score); S.stageMax = Math.max(S.stageMax, x.stage);
  return x;
}

function applyFx(S, fx) {
  const base = Math.max(S.gdp, 700), pop = ageGroups(S.age).pop;
  for (const q in fx) {
    const v = fx[q];
    if (q === 'c') S.treas -= v * base; else if (q === 'tr') S.trust = clamp(S.trust + v, 0, 100); else if (q === 'hp') S.mods.push({ v, u: S.m + 12 });
    else if (q === 'pol' || q === 'crime' || q === 'corr' || q === 'gini') S.adj[q] += v * 1.6;
    else if (q === 'hq') S.adj.hq += v; else if (q === 'edu') S.eduY = clamp(S.eduY + v * 3, 0, 16); else if (q === 'sick') S.sick = clamp(S.sick + v, 0, .6);
    else if (q === 'food') S.food = Math.max(0, S.food + v * pop); else if (q === 'mat') S.mat = Math.max(0, S.mat + v); else if (q === 'rep') S.rep = clamp(S.rep + v);
    else if (q === 'infl') S.inflShock += v; else if (q === 'tech') S.tech += v; else if (q === 'tension') S.tension = clamp(S.tension + v); else if (q === 'forest') S.forestAdj += v;
    else if (q === 'priv') { S.priv = Math.max(0, S.priv + v * base); if (v < 0) S.shock = (S.shock || 0) + v * .12; } else if (q === 'war') S.war = Math.max(S.war, v); else if (q === 'epi') S.epi = Math.max(0, S.epi + v); else if (q === 'drought') S.drought = Math.max(S.drought, v);
    else if (q === 'road') S.road = clamp(S.road + v); else if (q === 'cong') S.transit -= v; else if (q === 'tfr') S.tfrAdd += v;
    else if (q === 'tax') { S.tax.inc = clamp(S.tax.inc + v, 0, 45); S.tax.vat = clamp(S.tax.vat + v, 0, 25); }
    else if (q === 'bud') { for (const r in S.bud) S.bud[r] = clamp(S.bud[r] * (1 + v), 0, 2); }
    else if (q === 'debt') { if (v < 0) S.debt *= Math.max(0, 1 + v); else { const n = v * base * 6; S.debt += n; S.treas += n * .5; } }
    else if (q === 'pop') { const f = clamp(1 + v, .4, 1.3); for (let i = 15; i < 50; i++) S.age[i] *= f; }
    else if (q === 'later') S.later.push({ m: S.m + v[0], fx: v[1], news: v[2], vis: v[3] || '' });
  }
}

/* What private people want to build next (they pay with private money). The same logic runs in the future forecast. */
function tierPick(list, st, need, key) { let best = null; for (const t of list) { if (BT[t].st > st) continue; best = t; if (BT[t].g[key] >= need) break; } return best; }
function autoPlan(S) {
  const x = S.x, st = x.stage || 0, out = [], pop = x.pop || 10; let money = S.priv;
  const want = (t, n = 1) => { for (let i = 0; i < n; i++) { if (t && BT[t].c <= money) { out.push(t); money -= BT[t].c; } } };
  const maxN = Math.ceil(1 + Math.pow(pop, .36));
  if ((x.houseRatio || 0) < 1.14) { const need = pop * 1.18 - S.k.house, t = tierPick(HOME_T, st, need * .55, 'house'); want(t, Math.min(maxN, Math.ceil(need / BT[t].g.house))); }
  const foodNeed = pop * 1.08 - (x.foodOut || 0);
  if (foodNeed > 0 && (x.foodMonths || 0) < 3) { const t = tierPick(['farm', 'bigfarm'], st, foodNeed / 3, 'ag'); want(t, Math.min(maxN, Math.ceil(foodNeed / 3 / BT[t].g.ag))); }
  if (S.mat < 16 + pop * .03 && S.k.matp < pop * .25 + 2) want(tierPick(['lumber', 'workshop', 'factory', 'plant'], st, pop * .01, 'matp'));
  const free = (S.k.ag + S.k.ind + S.k.svc + S.k.pub + S.k.tech) - (x.LF || 5);
  if (free < (x.LF || 5) * .03) {
    const need = (x.LF || 5) * 1.05 - (S.k.ag + S.k.ind + S.k.svc + S.k.pub + S.k.tech);
    const skilled = (x.eduY || 0) > 7 && st >= 6 && S.k.tech < (x.LF || 5) * clamp(((x.eduY || 0) - 5) / 9) * .6;
    let list = ['shop', 'market', 'office', 'cbd'], key = 'svc';
    if (skilled) { list = ['techpark']; key = 'tech'; } else if (st >= 2 && S.k.ind < S.k.svc * .9) { list = ['workshop', 'factory', 'plant']; key = 'ind'; }
    const t = tierPick(list, st, need * .55, key); if (t) want(t, Math.min(maxN, Math.ceil(need / BT[t].g[key])));
  }
  return out.slice(0, maxN + 2);
}
/* Ministries take over public building when the country is too big to order by hand. */
function ministryPlan(S) {
  const x = S.x, st = x.stage || 0, pop = x.pop || 0, out = []; if (st < 3) return out; let money = S.treas * .7;
  const chk = (ok, list, key, need) => { if (ok) return; const t = tierPick(list, st, need, key); if (!t) return; const n = Math.min(12, Math.ceil(Math.max(1, need) / BT[t].g[key])); for (let i = 0; i < n && BT[t].c <= money; i++) { out.push(t); money -= BT[t].c; } };
  chk(x.cleanW > .96, ['well', 'waterworks', 'dam'], 'water', pop - S.k.water); chk(x.pw > .9, ['gen', 'coal', 'solar', 'nuclear'], 'power', pop * .7 - S.k.power);
  chk(x.hospCov > .92 || S.bud.health < .4, ['clinic', 'hospital', 'medcenter'], 'hosp', pop - S.k.hosp); chk(x.schoolCov > .9 || S.bud.edu < .4, ['school', 'hischool', 'univ'], 'school', (x.kids || 0) * 1.2 - S.k.school);
  chk(x.safeCov > .9 || S.bud.safety < .3, ['police', 'policehq'], 'safe', pop - S.k.safe); chk(x.clean > .92, ['trash', 'recycle'], 'trash', pop - S.k.trash);
  return out.slice(0, 24);
}

/* From state level up, ministries also run nationwide programmes that do not each need a building on the map. */
function nationalWorks(S) {
  const x = S.x; if ((x.stage || 0) < 5) return; const k = S.k, pop = x.pop;
  for (const [key, need, unit, bud] of [['water', pop, 6, 'infra'], ['power', pop * .85, 8, 'infra'], ['hosp', pop, 14, 'health'], ['school', (x.kids + pop * .08) * 1.15, 30, 'edu'], ['safe', pop, 6, 'safety'], ['trash', pop, 6, 'env']]) {
    if (S.bud[bud] < .35) continue; const gap = need * 1.03 - k[key]; if (gap <= 0) continue;
    const add = Math.min(gap, k[key] * .05 + need * .012), cost = add * unit * Math.sqrt(S.tech); if (cost <= S.treas * .3) { k[key] += add; S.treas -= cost; }
  }
  /* private companies and home builders at national scale */
  const jobs = k.ag + k.ind + k.svc + k.pub + k.tech, jobGap = x.LF * 1.05 - jobs, unit = 34 * Math.sqrt(S.tech);
  if (jobGap > 0) { const add = Math.min(jobGap, jobs * .03), cost = add * unit; if (cost <= S.priv * .5) { const tc = clamp((x.eduY - 6) / 10) * .35, ic = .3 - clamp(S.tech / 12) * .12; k.tech += add * tc; k.ind += add * ic; k.dirty += add * ic * .7; k.svc += add * (1 - tc - ic); S.priv -= cost; } }
  const homeGap = pop * 1.12 - k.house; if (homeGap > 0) { const add = Math.min(homeGap, k.house * .03), cost = add * unit * .6; if (cost <= S.priv * .5) { k.house += add; S.priv -= cost; } }
}

/* The future: run a copy of the country forward, with private people and ministries acting, and no surprise events. */
const WHATIF = {
  none: ['ปล่อยไปแบบนี้', null],
  factory: ['โรงงานเพิ่มเท่าตัว', C => { C.k.ind *= 2; C.k.dirty = C.k.dirty * 2 + 60; C.k.matp *= 2; }],
  tax: ['ขึ้นภาษี +8%', C => { C.tax.inc += 4; C.tax.vat += 4; }],
  debt: ['กู้เงินเพิ่มมหาศาล', C => { const n = Math.max(C.gdp, 700) * 36; C.debt += n; C.treas += n * .75; }],
  noedu: ['ตัดงบการศึกษา', C => { C.bud.edu = .1; }],
  nohealth: ['ตัดงบสาธารณสุข', C => { C.bud.health = .1; }],
  babies: ['คนมีลูกเยอะมาก', C => { C.tfrAdd += 2.2; }],
  noenv: ['ไม่ดูแลสิ่งแวดล้อม', C => { C.bud.env = 0; C.adj.pol += .2; C.forestAdj -= .2; }],
  welfare: ['สวัสดิการเต็มที่', C => { C.bud.welfare = 1.6; C.bud.health = Math.max(C.bud.health, 1.2); }]
};
function forecast(S, years, patchKey) {
  const C = JSON.parse(JSON.stringify(S)); C.month = null; C.stats = null; C.later = []; C.hist = [];
  const patch = WHATIF[patchKey || 'none'][1]; if (patch) patch(C); if (!C.x.pop) stepModel(C);
  const pts = [], warn = {}, mark = (id, cond, txt) => { if (cond && !warn[id]) warn[id] = { y: Math.max(.1, (C.m - S.m) / 12), t: txt }; };
  for (let i = 0; i < years * 12; i++) {
    const x = stepModel(C); nationalWorks(C);
    for (const q of [...autoPlan(C), ...ministryPlan(C)]) { const d = BT[q]; if (BT[q].auto) C.priv -= d.c; else C.treas -= d.c; C.mat = Math.max(0, C.mat - d.m); for (const g in d.g) C.k[g] = (C.k[g] || 0) + d.g[g]; if (d.g.house) C.forestBase = Math.max(.2, C.forestBase - .00015); }
    if (i % 3 === 2) pts.push({ y: (i + 1) / 12, pop: x.pop, gdpPc: x.gdpPc, idx: x.idx, u: x.u, P: x.P, debt: x.debtRatio, happy: x.happy, old: x.oldShare, score: x.score });
    mark('water', x.cleanW < .7 && x.pop > 20, 'น้ำสะอาดไม่พอ'); mark('food', x.hunger > .05, 'เริ่มมีคนอดอาหาร'); mark('jobs', x.u > .2, 'คนตกงานเกิน 20%'); mark('home', x.houseRatio < .85, 'ที่อยู่อาศัยไม่พอ เกิดสลัม');
    mark('smog', x.P > .4, 'มลพิษถึงระดับอันตราย'); mark('debt', x.debtRatio > 1, 'หนี้เกิน GDP เสี่ยงวิกฤต'); mark('old', x.oldShare > .2, 'เข้าสู่สังคมสูงวัย แรงงานลด'); mark('crime', x.crime > .28, 'อาชญากรรมพุ่ง');
    mark('doctor', x.hospCov < .5 && x.pop > 60, 'หมอและเตียงไม่พอ'); mark('school', x.schoolCov < .5 && x.pop > 40, 'เด็กครึ่งหนึ่งไม่ได้เรียน'); mark('infl', x.infl > .018, 'เงินเฟ้อสูง ของแพง'); mark('traffic', x.cong > .4, 'รถติดหนักทั้งเมือง');
    mark('gap', x.gini > .48, 'ช่องว่างรวยจนกว้างมาก'); mark('leave', x.A < -.15, 'คนเริ่มย้ายออกจากประเทศ'); mark('birth', x.tfr < 1.5 && x.pop > 500, 'เด็กเกิดน้อยเกินไป'); mark('power', x.pw < .6 && x.pop > 100, 'ไฟฟ้าไม่พอ');
  }
  return { pts, warn: Object.values(warn).sort((p, q) => p.y - q.y), end: C.x };
}
if (typeof module !== 'undefined') module.exports = { nationalWorks, newState, stepModel, applyFx, autoPlan, ministryPlan, forecast, ageGroups };
