'use strict';
/* ก่อร่างสร้างชาติ: the working economy. Three skill levels, wages, resources, production chains, trade and profit. No DOM here, so the future forecast can run it. */
const JOB_MIX = { ag: [1, 0, 0], svc: [.62, .3, .08], ind: [.5, .42, .08], pub: [.25, .45, .3], tech: [0, .15, .85] };
const SKILL_N = ['ไร้ฝีมือ', 'ช่าง', 'คนเรียนสูง'];
const MIN_WAGE = [0, .92, 1.02, 1.16, 1.34];
const IND_V = { mine: 300, mill: 240, saw: 270, lum: 250, steel: 430, gen: 330, mach: 560 };
function econNew() { return { w: [1, 1, 1], wage: 1, wg: 0, mul: 1, margin: .45, lossM: 0, ore: 0, oreMax: 0, seeded: 0, px: { ore: 1, steel: 1, goods: 1, mach: 1, food: 1 }, tariff: 0, sub: 0, subM: 0, train: 0, temp: null, vm: 0, vh: 0, idle: 0, L: [0, 0, 0], D: [0, 0, 0], lim: {}, flow: {} }; }

/* who can fill which job: better-trained people can step down, the untrained can only help as apprentices */
function laborMatch(S, LF, J) {
  const e = S.e, h = clamp((S.eduY - 8) / 9, 0, .5), m = Math.min(clamp((S.eduY - 3.2) / 8, 0, .62), .95 - h), T = Math.min(e.train || 0, LF * Math.max(0, 1 - h - m)), Lh = LF * h, Lm = LF * m + T, Ll = Math.max(0, LF - Lh - Lm), D = [0, 0, 0];
  for (const q in JOB_MIX) for (let i = 0; i < 3; i++) D[i] += (J[q] || 0) * JOB_MIX[q][i];
  let Eh = Math.min(D[2], Lh), sH = Lh - Eh, Em = Math.min(D[1], Lm), sM = Lm - Em; const mH = Math.min(D[1] - Em, sH); Em += mH; sH -= mH;
  let El = Math.min(D[0], Ll), sL = Ll - El; const lU = Math.min(D[0] - El, sM + sH); El += lU; const left = Math.max(0, sM + sH - lU);
  const appr = Math.min((D[1] - Em) * .7, sL); sL -= appr; const apH = Math.min((D[2] - Eh) * .3, left); const temp = Math.min(e.temp ? e.temp.n : 0, sL); sL -= temp;
  const fl = D[0] > 0 ? El / D[0] : 1, fm = D[1] > 0 ? (Em + appr * .6) / D[1] : 1, fh = D[2] > 0 ? (Eh + apH * .6) / D[2] : 1, fit = q => JOB_MIX[q][0] * fl + JOB_MIX[q][1] * fm + JOB_MIX[q][2] * fh, jobs = D[0] + D[1] + D[2], emp = Math.min(LF, El + Em + appr + Eh + apH + temp);
  return { ag: J.ag * fl, svc: J.svc * fit('svc'), ind: J.ind * fit('ind'), pub: J.pub * fit('pub') + temp, tech: J.tech * fit('tech'), emp, fill: jobs > 0 ? clamp((emp - temp) / jobs) : 0, L: [Ll, Lm, Lh], D, T: (() => { const Am = Lm + Math.max(0, Lh - D[2]), Al = Ll + Math.max(0, Am - D[1]); return [D[0] / (Al + .5), D[1] / (Am + .5), D[2] / (Lh + .5)]; })(), vm: Math.max(0, D[1] - Em - appr), vh: Math.max(0, D[2] - Eh - apH), idle: sL };
}

/* one month of industry: dig, process, make, sell, and see whether anyone made a profit */
function econStep(S, c) {
  const e = S.e, k = S.k, M = c.M, rand = !!S.stats, px = e.px;
  e.L = M.L; e.D = M.D; e.vm = M.vm; e.vh = M.vh; e.idle = M.idle; e.train = (e.train || 0) * .992;
  for (let i = 0; i < 3; i++) e.w[i] += (clamp(1 + ((M.D[i] > .5 ? M.T[i] : 1) - 1) * .6, .72, 1.4) - e.w[i]) * .04;
  const lawW = MIN_WAGE[+((S.laws || {}).minwage || 0)] || 0; if (e.w[0] < lawW) e.w[0] = lawW; if (e.floor && e.w[0] < e.floor) e.w[0] = e.floor; e.floor = (e.floor || 0) * .995;
  const old = e.wage, tot = M.D[0] + M.D[1] + M.D[2] || 1; e.wage = (e.w[0] * M.D[0] + e.w[1] * M.D[1] * 1.5 + e.w[2] * M.D[2] * 2.4) / (M.D[0] + M.D[1] * 1.5 + M.D[2] * 2.4 || 1); e.wg = e.wage - old; e.tot = tot;
  if (rand) for (const q in px) px[q] = clamp(px[q] + (1 - px[q]) * .03 + (Math.random() - .5) * .055, .62, 1.45);
  const ind = c.E.ind, f = ind / Math.max(1, k.ind), W0 = { mine: (k.ore || 0) * f, mill: (k.mill || 0) * f, saw: (k.saw || 0) * f, lum: (k.wood || 0) * f, steel: (k.steelJ || 0) * f, mach: (k.mach || 0) * f }; let spec = 0; for (const q in W0) spec += W0[q];
  if (spec > ind && spec > 0) for (const q in W0) W0[q] *= ind / spec; const gen = Math.max(0, ind - Math.min(spec, ind)), partners = (S.world || []).filter(q => q.trade).length, tc = .1 + .2 * Math.min(k.port || 0, 4) + .05 * Math.min(k.air || 0, 3) + .04 * partners;
  let room = tc * (ind + 8), cost = 0; const buy = (need, have, key, unit) => { const miss = Math.max(0, need - have), got = Math.min(miss, room); room -= got; cost += got * px[key] * unit * (1 + (e.tariff || 0) / 100); return { fit: need > 0 ? clamp((have + got) / need) : 1, got }; };
  const oreOut = Math.min(W0.mine * 1.1, e.ore); e.ore = Math.max(0, e.ore - oreOut);
  const woodOut = (W0.lum + W0.saw * .6) * 1.5 * (.3 + .7 * c.forest), timber = Math.min(W0.saw * .9, woodOut), woodLeft = Math.max(0, woodOut - timber); S.forestAdj += (S.forestAdj < 0 ? .00016 : 0) - Math.min(.0012, woodOut * 1.6e-6);
  const riceNeed = W0.mill * 3, rice = Math.min(riceNeed, Math.max(0, S.food - c.pop * 1.6)); S.food -= rice; const millFit = riceNeed > 0 ? rice / riceNeed : 1;
  const steelNeed = W0.steel, oreB = buy(steelNeed, oreOut, 'ore', 120), steelOut = steelNeed * oreB.fit, oreSold = Math.max(0, oreOut - steelNeed);
  const machNeed = W0.mach * .7, machS = Math.min(machNeed, steelOut), machB = buy(machNeed, machS, 'steel', 180), steelLeft = Math.max(0, steelOut - machS);
  const partNeed = gen * .25, partHave = timber + woodLeft * .6 + steelLeft * .7, partB = buy(partNeed, partHave, 'goods', 110);
  const wFit = clamp((k.water + 14) / (c.pop + k.ind * .35 + 1), .6, 1), gross = (W0.mine * IND_V.mine * px.ore * (W0.mine > 0 ? clamp(oreOut / (W0.mine * 1.1)) : 1) + W0.mill * IND_V.mill * px.food * (.45 + .55 * millFit) + W0.saw * IND_V.saw * (.3 + .7 * (W0.saw > 0 ? clamp(timber / (W0.saw * .9)) : 1)) + W0.lum * IND_V.lum + W0.steel * IND_V.steel * px.steel * (.25 + .75 * oreB.fit) + gen * IND_V.gen * px.goods * (.5 + .5 * partB.fit) + W0.mach * IND_V.mach * px.mach * (.25 + .75 * machB.fit)) * wFit;
  const units = gross / 330, wg = clamp(1.25 - (e.wage - 1) * .6, .5, 1.3), dom = c.pop * .32 * (.45 + clamp(c.gdpPc / 1400)) * (1 + (e.tariff || 0) * .012), expRoom = tc * (ind + 8) * 1.6 * wg, sold = units > 0 ? clamp((dom + expRoom) / units, .3, 1) : 1, exp = Math.max(0, Math.min(units * sold - Math.min(dom, units), expRoom));
  const pot = Math.max(1, (W0.mine * IND_V.mine + W0.mill * IND_V.mill + W0.saw * IND_V.saw + W0.lum * IND_V.lum + W0.steel * IND_V.steel + gen * IND_V.gen + W0.mach * IND_V.mach)), val = Math.max(0, gross * sold - cost), base = Math.max(1, ind * 330); e.mul = ind > .5 ? clamp(val / base, .22, 1.7) : 1;
  if (e.subM && S.m >= e.subM) { e.sub = 0; e.subM = 0; } const subPay = c.gdp * (e.sub || 0) / 100; if (subPay > 0) S.treas -= subPay; if (cost > 0 && e.tariff) S.treas += cost * e.tariff / (100 + e.tariff);
  e.margin = (ind > .5 ? val / pot : 1) - .55 * e.wage + Math.min(.4, subPay / pot); e.lossM = e.margin < -.02 ? (e.lossM || 0) + 1 : Math.max(0, (e.lossM || 0) - .6);
  e.flow = { ore: oreOut, oreImp: oreB.got, oreSold, timber, wood: woodOut, rice, steel: steelOut, gen, mach: W0.mach * machB.fit, partFit: partB.fit, steelFit: oreB.fit, machFit: machB.fit, millFit, sold, exp: exp * 330, imp: cost, tc, partners };
  e.lim = { power: c.pw < .8 ? 1 - c.pw : 0, water: wFit < .95 ? 1 - wFit : 0, input: ind > 2 ? 1 - (gen * partB.fit + W0.steel * oreB.fit + W0.mach * machB.fit + W0.mill * millFit + 1) / (gen + W0.steel + W0.mach + W0.mill + 1) : 0, sales: 1 - sold, skill: M.D[1] + M.D[2] > 0 ? (M.vm + M.vh) / (M.D[1] + M.D[2]) : 0, wage: Math.max(0, e.wage - 1.15) };
}
const econInvest = e => clamp(.35 + e.margin * 1.45, .25, 1.35);

/* which factory private money wants next, following what the chain is short of */
function econPick(S, st) {
  const x = S.x, k = S.k, e = S.e; if (!e || (e.margin < -.05 && Math.random() < .7)) return null; const ind = k.ind || 0, tooFewSkilled = (e.vm + e.vh) > (x.LF || 5) * .05;
  if (BT.ricemill.st <= st && (x.foodMonths || 0) > 2.4 && (k.mill || 0) * 3 < Math.max(0, (x.foodOut || 0) - (x.pop || 0)) && Math.random() < .55) return 'ricemill';
  if (BT.sawmill.st <= st && (x.forest || 1) > .5 && (k.saw || 0) < ind * .2 + 3 && Math.random() < .6) return 'sawmill'; if (tooFewSkilled) return null;
  if (BT.mine.st <= st && e.ore > 0 && (k.ore || 0) < ind * .12 + 8 && Math.random() < .6) return 'mine';
  if (BT.steel.st <= st && (k.steelJ || 0) < ind * .2 && (e.ore > 0 || k.port > 0)) return 'steel';
  if (BT.machine.st <= st && (k.mach || 0) < ind * .14 && (k.steelJ || 0) > 0 && (x.eduY || 0) > 6.5) return 'machine'; return null;
}
/* nationwide growth keeps the same mix of industries */
function econSpread(k, add, st) { if (st >= 2) k.ore = (k.ore || 0) + add * .1; k.mill = (k.mill || 0) + add * .08; k.saw = (k.saw || 0) + add * .06; if (st >= 4) k.steelJ = (k.steelJ || 0) + add * .16; if (st >= 5) k.mach = (k.mach || 0) + add * .12; }
