'use strict';
/* CLASSES OF THE BACKPACK GAME (owner 2026-11-28: "เอาเกมส์กระเป๋าทำต่อ ละเอาพวกโมเดล KayKit มาใช้ เป็นแบ่งตามคลาส ละให้มอนวิ่งมารุมตามรอบ",
   then "เอาให้คุณสมบัติคลาสคล้องกับไอเทมที่เราเชื่อมในกระเป๋า"). Shared by bag3d.html (shop, bag, stats, side-view duel) and horde.html?bag=1
   (the swarm fight, bag3d/arena.js).
   - Each class = one free KayKit Adventurers 2.0 body (CC0, art/tribe3d/people/) holding its own KayKit weapons, its own moves
     (art/grind3d/hero_anims.glb clips, same skeleton), its own skill and starting bag.
   - CLASS LINKS: a class has a pair of item KINDS (a = the items that gain, b = the items they link with). Every a-item that touches
     b-items in the bag (side by side) gets `per` once for each b-item it touches (at most 3), and the number of links of the whole bag
     opens the class TIERS (2 / 4 / 6 links), like a set bonus. The bag draws a line for every link. */
const BAGKIND = {
  w_phy: d => d.t === 'w' && d.ty !== 'mag',
  w_heavy: d => d.t === 'w' && d.ty !== 'mag' && d.cd >= 2.2,
  w_mag: d => (d.t === 'w' || d.start) && d.ty === 'mag',
  w_range: d => d.t === 'w' && BAGRANGED.has(d.base || d.id) || d.t === 'w' && BAGRANGED.has(d.id),
  w_fast: d => d.t === 'w' && d.cd <= 1.35,
  def: d => d.t === 'd',
  food: d => d.t === 'f' || ['ragemask', 'wardrum'].includes(d.id),
  boost: d => d.t === 'g',
  venom: d => d.t !== 'w' && !!(d.poi || d.adj && (d.adj.poi || d.adj.crit) || d.dodge || d.id === 'cloak' || d.id === 'skull'),
};
const BAGRANGED = new Set(['bow', 'frostbow', 'f_godbow', 'javelin', 'shuriken', 'chakram', 'axe', 'bloodaxe']);
const BAGKN = { w_phy: 'อาวุธกายภาพ', w_heavy: 'อาวุธหนัก (ตีช้า)', w_mag: 'อาวุธเวท', w_range: 'อาวุธยิง / ขว้าง', w_fast: 'อาวุธเร็ว', def: 'เกราะ / โล่', food: 'อาหาร / ของคลั่ง', boost: 'เครื่องเสริม', venom: 'ของพิษ / คริ / หลบ' };
const BAGCLS = {
  knight: { n: 'อัศวินโล่เหล็ก', e: '🛡️', kk: 'Knight', wp: [['sword_1handed', 'handslotr'], ['shield_round', 'handslotl']], col: ['#bfe0ff', '#2a4a7a'],
    r: 'แนวหน้า · ดาบและโล่', at: 'กายภาพ +10% · เกราะหนา', aff: { phy: 1.1 }, base: { hp: 84, armor: 1.5, critd: .05 }, start: ['sword', 'buckler'],
    anim: { idle: 'Idle', run: 'Running_A', melee: 'Melee_1H_Attack_Slice_Horizontal', shoot: 'Melee_1H_Attack_Chop', magic: 'Melee_1H_Attack_Chop', skill: ['Melee_Block_Attack'], hit: 'Melee_Block_Hit' },
    sk: { n: 'โล่ทลายพสุธา', d: 'กระแทกโล่ใส่ศัตรูรอบตัว มึน 1 วิ และได้โล่กันดาเมจ', cd: 8, blk: 1, kind: 'bash', w: { ty: 'phy', stun: 1 }, h: [[.45, 1.4]] },
    link: { n: 'ดาบคู่เกราะ', a: 'w_phy', b: 'def', per: { dmg: .1 }, pd: 'แรง +10%', tiers: [[2, { armor: 2 }, 'เกราะ +2'], [4, { thorn: 3 }, 'สะท้อนดาเมจ +3'], [6, { hpm: .2 }, 'เลือดสูงสุด +20%']] } },
  barbarian: { n: 'นักรบขวานคลั่ง', e: '🪓', kk: 'Barbarian', wp: [['axe_2handed', 'handslotr']], col: ['#ffc89a', '#7a3a1a'],
    r: 'บุกตะลุย · ขวานสองมือ', at: 'กายภาพ +15% · เลือดหนา', aff: { phy: 1.15 }, base: { hp: 96, regen: .3, haste: -.05 }, start: ['club', 'meat'],
    anim: { idle: 'Melee_2H_Idle', run: 'Running_A', melee: 'Melee_2H_Attack_Chop', shoot: 'Melee_2H_Attack_Slice', magic: 'Melee_2H_Attack_Slice', skill: ['Melee_2H_Attack_Spinning'] },
    sk: { n: 'พายุขวานคลั่ง', d: 'หมุนขวานรอบตัว 3 รอบ ฟันทุกตัวที่อยู่ใกล้', cd: 8.5, kind: 'spin', w: { ty: 'phy' }, h: [[.3, .6], [.6, .6], [.9, .8, 1]] },
    link: { n: 'เลือดนักรบ', a: 'w_heavy', b: 'food', per: { dmg: .12, ls: .03 }, pd: 'แรง +12% ดูดเลือด +3%', tiers: [[2, { hpm: .12 }, 'เลือดสูงสุด +12%'], [4, { regen: .8 }, 'ฟื้นเลือด +0.8/วิ'], [6, { all: .15 }, 'ดาเมจทุกชิ้น +15%']] } },
  mage: { n: 'จอมเวทอัคคี', e: '🔮', kk: 'Mage', wp: [['staff', 'handslotr'], ['spellbook_open', 'handslotl']], col: ['#d8b8ff', '#4a2a7a'],
    r: 'ร่ายเวท · คทาและตำรา', at: 'เวท +20% · ต้านเวท', aff: { mag: 1.2 }, base: { hp: 62, mres: .15, sreg: .25 }, start: ['wand', 'apple'],
    anim: { idle: 'Idle', run: 'Running_A', melee: 'Melee_1H_Attack_Stab', shoot: 'Ranged_Magic_Summon', magic: 'Ranged_Magic_Summon', skill: ['Ranged_Magic_Summon'] },
    sk: { n: 'ฝนอุกกาบาต', d: 'อุกกาบาต 3 ลูกตกใส่กลุ่มศัตรู ติดไฟ', cd: 9, kind: 'meteor', w: { ty: 'mag', burn: 1.5 }, h: [[.5, .6], [.75, .6], [1, .8]] },
    link: { n: 'มนตร์เชื่อม', a: 'w_mag', b: 'boost', per: { dmg: .12, cd: .05 }, pd: 'แรง +12% ร่ายเร็ว +5%', tiers: [[2, { mres: .1 }, 'ต้านเวท +10%'], [4, { gmdmg: .15 }, 'เวททั้งหมด +15%'], [6, { haste: .12 }, 'โจมตีเร็ว +12%']] } },
  ranger: { n: 'พรานธนูเงา', e: '🏹', kk: 'Ranger', wp: [['bow_withString', 'handslotl']], col: ['#c8f0b0', '#2a5a3a'],
    r: 'ยิงไกล · ธนู', at: 'กายภาพ +10% · คริติคอลสูง', aff: { phy: 1.1 }, base: { hp: 70, crit: .1, critd: .15 }, start: ['bow', 'apple'],
    anim: { idle: 'Ranged_Bow_Idle', run: 'Running_HoldingBow', melee: 'Melee_1H_Attack_Slice_Horizontal', shoot: 'Ranged_Bow_Release', magic: 'Ranged_Bow_Release', skill: ['Ranged_Bow_Draw_Up', 'Ranged_Bow_Release_Up'] },
    sk: { n: 'ฝนธนูพราน', d: 'ยิงธนูทะลุ 5 ดอกเป็นพัด ดอกกลางคริติคอล', cd: 7.5, kind: 'fan', w: { ty: 'phy' }, h: [[.45, .5], [.6, .5], [.75, .9, 1]] },
    link: { n: 'ตาเหยี่ยว', a: 'w_range', b: 'boost', per: { crit: .06, dmg: .06 }, pd: 'คริ +6% แรง +6%', tiers: [[2, { crit: .05 }, 'คริติคอล +5%'], [4, { critd: .3 }, 'แรงคริ +30%'], [6, { haste: .12 }, 'โจมตีเร็ว +12%']] } },
  rogue: { n: 'นักฆ่าเงาพิษ', e: '🗡️', kk: 'Rogue_Hooded', wp: [['dagger', 'handslotr'], ['dagger', 'handslotl']], col: ['#c0ffb0', '#2a3a2a'],
    r: 'ลอบสังหาร · มีดคู่', at: 'ตีเร็ว · คริติคอล · พิษ', aff: { phy: 1.05, mag: 1.05 }, base: { hp: 64, haste: .1, crit: .08 }, start: ['dagger', 'venomgland'],
    anim: { idle: 'Idle_B', run: 'Running_A', melee: 'Melee_1H_Attack_Stab', shoot: 'Melee_1H_Attack_Slice_Diagonal', magic: 'Melee_1H_Attack_Stab', skill: ['Dodge_Forward', 'Melee_1H_Attack_Stab'] },
    sk: { n: 'เงาพิษพันคม', d: 'พุ่งแทงศัตรูใกล้ตัว 5 ตัว ติดพิษ', cd: 7, kind: 'venom', w: { ty: 'phy', poi: 2 }, h: [[.3, .35], [.42, .35], [.54, .35], [.66, .35], [.8, .6, 1]] },
    link: { n: 'พิษในเงา', a: 'w_fast', b: 'venom', per: { cd: .08, poi: 1 }, pd: 'ตีเร็ว +8% พิษ +1', tiers: [[2, { dodge: .06 }, 'หลบ +6%'], [4, { crit: .08 }, 'คริติคอล +8%'], [6, { critd: .4 }, 'แรงคริ +40%']] } },
};
/* the links of a bag: cellsOf(o) gives an item's cells, def(id) its table entry. -> { pairs: [[a, b]], per: Map(a -> n), n, tier: [[need, bonus, text, on]] } */
function bagLinks(cls, items, cellsOf, def) {
  const C = BAGCLS[cls], out = { pairs: [], per: new Map(), n: 0, tier: [] }; if (!C) return out; const A = BAGKIND[C.link.a], B = BAGKIND[C.link.b], m = {};
  for (const o of items) for (const [x, y] of cellsOf(o)) m[x + ',' + y] = o;
  for (const o of items) { const d = def(o.id); if (!A(d)) continue; const s = new Set();
    for (const [x, y] of cellsOf(o)) for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const t = m[(x + a) + ',' + (y + b)]; if (t && t !== o && B(def(t.id))) s.add(t); }
    const ns = [...s].slice(0, 3); if (ns.length) { out.per.set(o, ns.length); for (const t of ns) out.pairs.push([o, t]); } }
  out.n = out.pairs.length; out.tier = C.link.tiers.map(([need, bon, txt]) => [need, bon, txt, out.n >= need]); return out;
}
if (typeof module !== 'undefined') module.exports = { BAGCLS, BAGKIND, BAGKN, bagLinks };
