'use strict';
/* ก่อร่างสร้างชาติ: who dies, at what age and from what. Life expectancy is worked out from these death rates, not guessed. */
const DEATH_N = { age: 'ชราภาพ', ncd: 'หัวใจ เบาหวาน มะเร็ง', infect: 'ติดเชื้อ ท้องร่วง', air: 'มลพิษทางอากาศ', water: 'น้ำเสียและสารพิษ', hunger: 'อดอาหาร', baby: 'ทารกและเด็กเล็ก', accident: 'อุบัติเหตุและงานอันตราย', crime: 'ถูกทำร้าย', war: 'สงคราม', disaster: 'ภัยพิบัติ' };
const DEATH_FIX = { ncd: 'เพิ่มหมอ โรงพยาบาล และรายได้', infect: 'น้ำสะอาด ขยะ และสถานีอนามัย', air: 'ลดโรงงานสกปรก ถ่านหิน และรถติด', water: 'บำบัดน้ำเสียและจัดการขยะ', hunger: 'เพิ่มไร่นาหรือสำรองอาหาร', baby: 'น้ำสะอาด หมอ และอาหาร', accident: 'กฎความปลอดภัยและถนนที่ดี', crime: 'ลดคนตกงานและเพิ่มตำรวจ', war: 'หลีกเลี่ยงสงคราม', disaster: 'คันกั้นน้ำ อ่างเก็บน้ำ และสถานีดับเพลิง' };
function hazards(R, i) {
  const B = .00032 * Math.exp(.092 * i) * R.care, share = i >= 35 ? clamp(.25 + .5 * R.inc) * clamp((i - 30) / 25) : 0, H = { age: B * (1 - share), ncd: B * share };
  const ageW = i < 5 ? 1.7 : i >= 60 ? 1.7 : .28; H.infect = (R.sick * .18 + R.epi * .6) * ageW * (1 - R.hq / 130);
  H.air = Math.pow(R.Pa, 1.25) * .05 * (i >= 50 ? Math.exp((i - 50) * .055) : i < 5 ? .7 : .12) * (1 - R.hq * .004);
  H.water = Math.pow(R.Pw, 1.2) * .03 * (i < 5 ? 3 : i >= 60 ? 1.3 : .25) * (1 - R.hq * .005); H.hunger = R.hunger * .16 * (i < 5 || i >= 65 ? 2 : .6);
  H.baby = i === 0 ? R.imr : i < 5 ? R.imr * .08 : 0; H.accident = i >= 15 && i < 65 ? .0005 + .0016 * R.ind + .0012 * R.cong : .0002; H.crime = i >= 15 && i < 45 ? R.crime * .003 : 0; H.war = R.war && i >= 18 && i < 42 ? .012 * R.armyK : 0;
  return H;
}
const hazardSum = (R, i) => { const H = hazards(R, i); let s = 0; for (const q in H) s += H[q]; return s; };
function lifeRates(S, c) {
  const inc = clamp(Math.log((c.gdpPc + 1) / 120) / Math.log(20)), hq = S.hq, care = clamp(1.55 - hq * .0105 - .15 * inc, .42, 1.6), Pa = clamp(S.P * 1.15 + c.cong * .08), Pw = clamp(c.dirtyShare * 1.1 + (1 - c.clean) * .28 + (1 - c.cleanW) * .16), imr = clamp(.008 + .05 * (1 - c.cleanW) + .05 * Math.pow(1 - hq / 100, 2) + .08 * S.hunger, .002, .25);
  const R = { inc, care, Pa, Pw, imr, hq, sick: S.sick, epi: S.epi, hunger: S.hunger, cong: c.cong, crime: S.crime, ind: c.indE / Math.max(1, c.LF), war: S.war > 0, armyK: 1 - .6 * Math.min(1, S.k.army + S.bud.defense * .4 + ((S.lawMod || {}).army || 0)) };
  let l = 1, e0 = 0; for (let i = 0; i < 91; i++) { const q = Math.min(.95, hazardSum(R, i)); e0 += l * (1 - q * .5); l *= 1 - q; } R.e0 = clamp(e0 + l * 2, 20, 95); return R;
}
function lifeStep(S, R, pop) {
  const a = S.age, T = {}; let died = 0;
  for (let i = 0; i < 91; i++) { const H = hazards(R, i); let s = 0; for (const q in H) s += H[q]; const d = a[i] * Math.min(.5, s) / 12; a[i] -= d; died += d; if (s > 0) for (const q in H) T[q] = (T[q] || 0) + d * H[q] / s; }
  const L = S.life || (S.life = { dc: {} }); for (const q in T) L.dc[q] = (L.dc[q] || 0) * .94 + T[q] * 12 * .06; L.dc.disaster = (L.dc.disaster || 0) * .94; L.e0 = R.e0; L.imr = R.imr; L.Pa = R.Pa; L.Pw = R.Pw; L.R = { inc: R.inc, care: R.care, Pa: R.Pa, Pw: R.Pw, imr: R.imr, hq: R.hq, sick: R.sick, epi: R.epi, hunger: R.hunger, cong: R.cong, crime: R.crime, ind: R.ind, war: R.war, armyK: R.armyK }; L.dr = died * 12 / Math.max(pop, 1) * 1000; return died;
}
