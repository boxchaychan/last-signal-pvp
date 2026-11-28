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
/* ATTRIBUTES STR / AGI / INT (owner 2026-11-28: "เพิ่มเติมให้มีค่าสถานะในไอเทมด้วย str agi int โดยยึดตามหลักโมบ้า str บวกเลือด agi ตี int skill เวทย์แรง"),
   like a MOBA: every item carries a little of the three, scaled by its stars like its other numbers, and the bag's totals turn into:
     STR = life (+2 max life and +0.02 life regen a point)
     AGI = attack (+0.7 % damage of physical weapons and +0.4 % attack speed a point)
     INT = skill and magic (+2.5 % skill power, +0.8 % magic damage, skill comes 0.5 % sooner a point, at most 30 %)
   and the class's MAIN attribute also gives +0.5 % damage to everything a point (like a MOBA hero's primary attribute).
   [str, agi, int] by item id; ids not listed have none. */
const BAGATTRK = { str: { hp: 2, regen: .02 }, agi: { dmg: .007, haste: .004 }, int: { skill: .025, mdmg: .008, skcd: .005 }, main: .005 };   /* 2026-11-28: first numbers (2.5 / 1.5 % ...) gave bot bags +40-100 % damage by round 11 (40 points): too much */
const BAGATTRN = { str: ['STR', 'พลัง', '#ff6a5a', 'เลือด +2 / ฟื้นเลือด +0.02 ต่อแต้ม'], agi: ['AGI', 'ว่องไว', '#6ae86a', 'อาวุธกายภาพแรง +0.7% / ตีเร็ว +0.4% ต่อแต้ม'], int: ['INT', 'ปัญญา', '#5ab8ff', 'สกิลแรง +2.5% / เวทแรง +0.8% / สกิลเร็วขึ้น 0.5% ต่อแต้ม'] };
const BAGATTR = {
  dagger: [0, 2, 0], sword: [1, 2, 0], bow: [0, 3, 0], axe: [3, 1, 0], hammer: [4, 0, 0], wand: [0, 0, 3], poison: [0, 1, 2], bomb: [0, 0, 1],
  shield: [2, 0, 0], helm: [2, 0, 0], cactus: [2, 0, 0], feather: [0, 3, 0], apple: [1, 0, 0], meat: [2, 0, 0], juice: [0, 1, 0],
  stone: [0, 1, 0], glove: [0, 2, 0], clover: [0, 1, 0], ember: [0, 0, 2], frost: [0, 0, 2], heart: [2, 0, 0], star: [1, 1, 1], crown: [2, 2, 2],
  spear: [2, 2, 0], claw: [0, 3, 0], scythe: [2, 3, 0], shuriken: [0, 2, 0], club: [2, 0, 0], orb: [0, 0, 3], icestaff: [0, 0, 3], skull: [0, 0, 4],
  book: [0, 0, 3], meteor: [0, 0, 3], plate: [4, 0, 0], cloak: [0, 2, 1], ring: [1, 0, 2], wine: [1, 1, 0], fang: [1, 1, 0], hourglass: [0, 0, 3],
  flamesword: [2, 2, 2], venomknife: [0, 3, 1], frostbow: [0, 4, 2], bloodaxe: [4, 1, 0], thunderhammer: [6, 0, 1], archstaff: [0, 0, 6], vampclaw: [1, 4, 0],
  comet: [0, 0, 5], fortress: [5, 0, 0], spikeshield: [4, 0, 0], feast: [4, 0, 0], luckycoin: [0, 1, 0],
  twinblades: [0, 3, 0], rapier: [0, 2, 0], greatsword: [5, 1, 0], katana: [0, 4, 0], javelin: [1, 2, 0], chakram: [0, 3, 0], holytome: [1, 0, 3], voidorb: [0, 0, 5],
  buckler: [1, 0, 0], towershield: [3, 0, 0], boots: [0, 2, 0], amulet: [1, 0, 2], bread: [1, 0, 0], potion: [1, 0, 1], honey: [0, 1, 0], elixir: [2, 0, 2],
  furyrune: [1, 1, 0], venomgland: [0, 1, 0], thunderstone: [1, 0, 1], holyseal: [0, 0, 2], ragemask: [2, 0, 0], wardrum: [1, 1, 0], lantern: [0, 0, 2],
  stormblades: [0, 5, 0], luckrapier: [0, 4, 0], executioner: [6, 2, 0], frostlance: [2, 2, 2], divinetome: [1, 0, 5], parrybuckler: [2, 1, 0], honeybread: [1, 1, 0], soullantern: [0, 0, 4],
  p_blade: [0, 2, 0], p_hide: [2, 0, 0], p_plate: [2, 0, 0], p_feather: [0, 2, 0], p_crystal: [0, 0, 2], p_fang: [1, 1, 0], p_herb: [1, 0, 1],
  m_edge: [1, 4, 0], m_mail: [5, 0, 0], m_boots: [1, 3, 0], m_orb: [0, 0, 5], m_charm: [3, 0, 1], m_claws: [0, 4, 0],
  f_kingslayer: [2, 8, 0], f_bastion: [10, 0, 0], f_stormstep: [0, 8, 0], f_archmage: [0, 0, 10], f_bloodpact: [5, 3, 0], f_titan: [8, 2, 0], f_lichstaff: [2, 0, 8], f_godbow: [1, 8, 0],
};
/* the bag's totals: items = the bag, mul(o) = an item's star multiplier -> { str, agi, int } */
function bagAttrs(items, mul) { const t = { str: 0, agi: 0, int: 0 }; for (const o of items) { const a = BAGATTR[o.id]; if (!a) continue; const L = mul(o); t.str += a[0] * L; t.agi += a[1] * L; t.int += a[2] * L; } for (const k in t) t[k] = Math.round(t[k] * 10) / 10; return t; }
const BAGCLS = {
  knight: { main: 'str', n: 'อัศวินดำ', e: '⚔️', kk: 'Knight',   /* the body is the owner's Tripo DEMON KNIGHT (horde.html HEROES.kk_knight, portrait tools/art/cls_portraits.html); kk / wp / anim = the old KayKit knight, still used by ?fight=side and ?kk=knight */
    wp: [['sword_1handed', 'handslotr'], ['shield_round', 'handslotl']], col: ['#bfe0ff', '#2a4a7a'],
    r: 'แนวหน้า · ดาบใหญ่สองมือ', at: 'กายภาพ +10% · เกราะหนา', aff: { phy: 1.1 }, base: { hp: 84, armor: 1.5, critd: .05 }, start: ['sword', 'buckler'],
    anim: { idle: 'Idle', run: 'Running_A', melee: 'Melee_1H_Attack_Slice_Horizontal', shoot: 'Melee_1H_Attack_Chop', magic: 'Melee_1H_Attack_Chop', skill: ['Melee_Block_Attack'], hit: 'Melee_Block_Hit' },
    sk: { n: 'ดาบทมิฬทลายพสุธา', d: 'ฟาดดาบใหญ่ลงพื้น ศัตรูรอบตัวมึน 1 วิ และได้โล่กันดาเมจ', cd: 8, blk: 1, kind: 'bash', w: { ty: 'phy', stun: 1 }, h: [[.45, 1.4]] },
    link: { n: 'ดาบคู่เกราะ', a: 'w_phy', b: 'def', per: { dmg: .1 }, pd: 'แรง +10%', tiers: [[2, { armor: 2 }, 'เกราะ +2'], [4, { thorn: 3 }, 'สะท้อนดาเมจ +3'], [6, { hpm: .2 }, 'เลือดสูงสุด +20%']] } },
  barbarian: { main: 'str', n: 'นักรบขวานคลั่ง', e: '🪓', kk: 'Barbarian', wp: [['axe_2handed', 'handslotr']], col: ['#ffc89a', '#7a3a1a'],
    r: 'บุกตะลุย · ขวานสองมือ', at: 'กายภาพ +15% · เลือดหนา', aff: { phy: 1.15 }, base: { hp: 96, regen: .3, haste: -.05 }, start: ['club', 'meat'],
    anim: { idle: 'Melee_2H_Idle', run: 'Running_A', melee: 'Melee_2H_Attack_Chop', shoot: 'Melee_2H_Attack_Slice', magic: 'Melee_2H_Attack_Slice', skill: ['Melee_2H_Attack_Spinning'] },
    sk: { n: 'พายุขวานคลั่ง', d: 'หมุนขวานรอบตัว 3 รอบ ฟันทุกตัวที่อยู่ใกล้', cd: 8.5, kind: 'spin', w: { ty: 'phy' }, h: [[.3, .6], [.6, .6], [.9, .8, 1]] },
    link: { n: 'เลือดนักรบ', a: 'w_heavy', b: 'food', per: { dmg: .12, ls: .03 }, pd: 'แรง +12% ดูดเลือด +3%', tiers: [[2, { hpm: .12 }, 'เลือดสูงสุด +12%'], [4, { regen: .8 }, 'ฟื้นเลือด +0.8/วิ'], [6, { all: .15 }, 'ดาเมจทุกชิ้น +15%']] } },
  mage: { main: 'int', n: 'จอมเวทอัคคี', e: '🔮', kk: 'Mage', wp: [['staff', 'handslotr'], ['spellbook_open', 'handslotl']], col: ['#d8b8ff', '#4a2a7a'],
    r: 'ร่ายเวท · คทาและตำรา', at: 'เวท +20% · ต้านเวท', aff: { mag: 1.2 }, base: { hp: 62, mres: .15, sreg: .25 }, start: ['wand', 'apple'],
    anim: { idle: 'Idle', run: 'Running_A', melee: 'Melee_1H_Attack_Stab', shoot: 'Ranged_Magic_Summon', magic: 'Ranged_Magic_Summon', skill: ['Ranged_Magic_Summon'] },
    sk: { n: 'ฝนอุกกาบาต', d: 'อุกกาบาต 3 ลูกตกใส่กลุ่มศัตรู ติดไฟ', cd: 9, kind: 'meteor', w: { ty: 'mag', burn: 1.5 }, h: [[.5, .6], [.75, .6], [1, .8]] },
    link: { n: 'มนตร์เชื่อม', a: 'w_mag', b: 'boost', per: { dmg: .12, cd: .05 }, pd: 'แรง +12% ร่ายเร็ว +5%', tiers: [[2, { mres: .1 }, 'ต้านเวท +10%'], [4, { gmdmg: .15 }, 'เวททั้งหมด +15%'], [6, { haste: .12 }, 'โจมตีเร็ว +12%']] } },
  ranger: { main: 'agi', n: 'พรานธนูเงา', e: '🏹', kk: 'Ranger', wp: [['bow_withString', 'handslotl']], col: ['#c8f0b0', '#2a5a3a'],
    r: 'ยิงไกล · ธนู', at: 'กายภาพ +10% · คริติคอลสูง', aff: { phy: 1.1 }, base: { hp: 70, crit: .1, critd: .15 }, start: ['bow', 'apple'],
    anim: { idle: 'Ranged_Bow_Idle', run: 'Running_HoldingBow', melee: 'Melee_1H_Attack_Slice_Horizontal', shoot: 'Ranged_Bow_Release', magic: 'Ranged_Bow_Release', skill: ['Ranged_Bow_Draw_Up', 'Ranged_Bow_Release_Up'] },
    sk: { n: 'ฝนธนูพราน', d: 'ยิงธนูทะลุ 5 ดอกเป็นพัด ดอกกลางคริติคอล', cd: 7.5, kind: 'fan', w: { ty: 'phy' }, h: [[.45, .5], [.6, .5], [.75, .9, 1]] },
    link: { n: 'ตาเหยี่ยว', a: 'w_range', b: 'boost', per: { crit: .06, dmg: .06 }, pd: 'คริ +6% แรง +6%', tiers: [[2, { crit: .05 }, 'คริติคอล +5%'], [4, { critd: .3 }, 'แรงคริ +30%'], [6, { haste: .12 }, 'โจมตีเร็ว +12%']] } },
  rogue: { main: 'agi', n: 'นักฆ่าเงาพิษ', e: '🗡️', kk: 'Rogue_Hooded', wp: [['dagger', 'handslotr'], ['dagger', 'handslotl']], col: ['#c0ffb0', '#2a3a2a'],
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
if (typeof module !== 'undefined') module.exports = { BAGCLS, BAGKIND, BAGKN, bagLinks, BAGATTR, BAGATTRK, BAGATTRN, bagAttrs };
