'use strict';
/* ITEM SKILLS (owner 2026-11-28: "กลับไปเกมส์กระเป๋า ภาพยังไม่สวยเลย vfx สวยๆ บ้าง ไอเทมมีสกิลเฉพาะ"): every weapon, shield and food of the
   backpack game has its OWN named skill. It goes off every `every` uses of that item (default by speed: fast 6, medium 4, slow 3), on top of its
   normal hit, with a big effect made of the CC0 pixel effects in art/pvfx (PVFX Foundry) + the 3D arena's own glows, rings and decals.
   Shared by bag3d.html (item info, side-view duel) and horde.html?bag=1 (bag3d/arena.js plays the kinds).
   kinds (what the skill does in the swarm; the duel turns each into one big hit, see BAGISK_DUEL):
     meteor  n meteors fall on the thickest groups            thunder  lightning strikes jump between n monsters (stun)
     nova    a blast ring round the champion                   pillar   n beams of light / fire on groups, 3 ticks each
     spikes  a line of spikes erupts toward the target        tornado  a whirlwind runs through the horde and drags them
     blades  blades spin round the champion for a while       rain     a rain of strikes over an area
     void    a black hole pulls monsters in, then bursts      quake    the ground cracks round the champion (stun)
     blood   bites the n nearest and heals the champion       frost    a blizzard freezes an area
     poison  a toxic cloud that keeps poisoning               crit     one huge critical strike on the strongest monster
     guard   (shields) a big shield bubble + a thorn pulse    feast    (food) heals over time in a green aura
   c = colour of the 3D glows / rings, pf = the main pixel effect, pf2 = a second one. */
const ITEMSK = {
  dagger: { n: 'พายุมีดเงา', d: 'ใบมีดเงาหมุนรอบตัวฟันทุกตัวที่เข้าใกล้', k: 'blades', c: 0xcda0ff, pf: 'melee/shadow-claw', dur: 1.6 },
  venomknife: { n: 'หมอกพิษมรณะ', d: 'ปล่อยหมอกพิษกลางฝูงมอน พิษสะสมไม่หยุด', k: 'poison', c: 0x8cff5a, pf: 'nature/poison-cloud', pf2: 'nature/acid-splash' },
  sword: { n: 'ใบมีดพายุรัตติกาล', d: 'ดาบเงาหมุนรอบตัว ฟันซ้ำทุกตัวรอบ ๆ', k: 'blades', c: 0x96c8ff, pf: 'melee/sword-combo', dur: 2.2 },
  flamesword: { n: 'อุกกาบาตอัคนี', d: 'เรียกอุกกาบาตไฟ 2 ลูกถล่มกลุ่มมอน ติดไฟ', k: 'meteor', c: 0xff8228, pf: 'fire/meteor-strike', pf2: 'fire/ground-flames', count: 2, burn: 2 },
  katana: { n: 'ฟันลมพันคม', d: 'คมลมนับสิบฟาดลงทั่วบริเวณ', k: 'rain', c: 0xaaffeb, pf: 'wind/wind-gust', pf2: 'impacts/hit-spark', count: 12 },
  greatsword: { n: 'ปฐพีแยก', d: 'ปักดาบลงพื้น แผ่นดินแตกรอบตัว มอนมึน', k: 'quake', c: 0xaa6eff, pf: 'impacts/ground-slam', pf2: 'impacts/rock-shatter' },
  executioner: { n: 'ประหารหัวขาด', d: 'ฟันตัวที่แข็งที่สุดครั้งเดียว แรง 4 เท่า คริติคอลแน่นอน', k: 'crit', c: 0xff4646, pf: 'melee/axe-smear', pf2: 'impacts/blood-splat', mul: 4 },
  twinblades: { n: 'คู่ใบมีดจันทรา', d: 'ใบมีดคู่หมุนรอบตัวยาว ๆ', k: 'blades', c: 0xcdb9ff, pf: 'melee/sword-combo', dur: 2.6 },
  stormblades: { n: 'พายุใบมีดสายฟ้า', d: 'สายฟ้าฟาดลง 6 ตัว กระโดดต่อกัน มอนมึน', k: 'thunder', c: 0x96e6ff, pf: 'lightning/lightning-strike', pf2: 'lightning/static-burst', count: 6 },
  rapier: { n: 'แทงจุดตาย', d: 'แทงตัวที่แข็งที่สุด แรง 3 เท่า คริติคอลแน่นอน', k: 'crit', c: 0xebf0ff, pf: 'impacts/crit-hit', mul: 3 },
  luckrapier: { n: 'โชคชะตาคริติคอล', d: 'แทงตัวที่แข็งที่สุด แรง 3.5 เท่า คริติคอลแน่นอน', k: 'crit', c: 0xb4ff96, pf: 'impacts/crit-hit', pf2: 'ui/star-burst-pickup', mul: 3.5 },
  spear: { n: 'หอกพสุธา', d: 'หนามหินพุ่งเป็นแนวยาวไปหาศัตรู', k: 'spikes', c: 0xffdc8c, pf: 'nature/earth-spike' },
  frostlance: { n: 'หอกน้ำแข็งพันปี', d: 'หนามน้ำแข็งพุ่งเป็นแนว มอนที่โดนแข็งค้าง', k: 'spikes', c: 0x96dcff, pf: 'ice/ice-spike', frz: 1.2 },
  javelin: { n: 'ฝนหอก', d: 'หอกนับสิบตกลงทั่วบริเวณ', k: 'rain', c: 0xffe6aa, pf: 'projectiles/arrow-impact', count: 10 },
  axe: { n: 'ขวานพายุหมุน', d: 'พายุหมุนวิ่งฝ่าฝูงมอน ลากมอนเข้าหากัน', k: 'tornado', c: 0xffaa64, pf: 'wind/whirlwind' },
  bloodaxe: { n: 'ขวานกระหายเลือด', d: 'ฟาด 5 ตัวที่ใกล้ที่สุด ดูดเลือดกลับมา', k: 'blood', c: 0xff3c3c, pf: 'impacts/blood-splat', count: 5 },
  hammer: { n: 'ทุบปฐพี', d: 'ทุบพื้นจนสั่น มอนรอบตัวกระเด็นและมึน', k: 'quake', c: 0xffdc96, pf: 'impacts/ground-slam', pf2: 'impacts/rock-shatter' },
  thunderhammer: { n: 'ค้อนเทพสายฟ้า', d: 'ฟ้าผ่า 7 ตัว กระโดดต่อกัน มอนมึน', k: 'thunder', c: 0xbeb4ff, pf: 'lightning/lightning-strike', pf2: 'lightning/static-burst', count: 7 },
  club: { n: 'กระบองแผ่นดินไหว', d: 'ทุบพื้นรอบตัว มอนมึน', k: 'quake', c: 0xf0c88c, pf: 'impacts/ground-slam' },
  claw: { n: 'กรงเล็บล่าเหยื่อ', d: 'ข่วน 4 ตัวที่ใกล้ที่สุด ดูดเลือด', k: 'blood', c: 0xff8c50, pf: 'melee/shadow-claw', count: 4 },
  vampclaw: { n: 'อสูรดูดเลือด', d: 'ข่วน 6 ตัวที่ใกล้ที่สุด ดูดเลือดกลับมามาก', k: 'blood', c: 0xff326e, pf: 'impacts/blood-splat', count: 6, heal: .45 },
  scythe: { n: 'เคียวเก็บวิญญาณ', d: 'หลุมดำดูดมอนเข้าหากันแล้วระเบิด', k: 'void', c: 0xb46eff, pf: 'shadow/void-implosion', pf2: 'shadow/curse' },
  shuriken: { n: 'ฝนดาวกระจาย', d: 'ดาวกระจายนับสิบโปรยทั่วบริเวณ', k: 'rain', c: 0xdce6ff, pf: 'impacts/hit-spark', count: 14 },
  chakram: { n: 'จักรเพลิงหมุน', d: 'ทอร์นาโดไฟวิ่งฝ่าฝูงมอน ติดไฟ', k: 'tornado', c: 0xff9632, pf: 'fire/fire-tornado', burn: 1.5 },
  bow: { n: 'ฝนธนู', d: 'ลูกธนูนับสิบตกลงใส่กลุ่มมอน', k: 'rain', c: 0xfff0c8, pf: 'projectiles/arrow-impact', count: 12 },
  frostbow: { n: 'ศรพายุหิมะ', d: 'พายุหิมะกลางฝูง มอนแข็งค้าง', k: 'frost', c: 0x96e1ff, pf: 'ice/blizzard', pf2: 'ice/freeze-encase' },
  f_godbow: { n: 'ศรเทพทะลุฟ้า', d: 'ลำแสงสวรรค์ 3 ลำผ่ากลางกลุ่มมอน', k: 'pillar', c: 0xffe178, pf: 'holy/divine-beam', count: 3 },
  wand: { n: 'อุกกาบาตเพลิง', d: 'อุกกาบาตไฟ 1 ลูกถล่มกลุ่มมอน ติดไฟ', k: 'meteor', c: 0xff8228, pf: 'fire/meteor-strike', pf2: 'fire/ground-flames', count: 1, burn: 2 },
  archstaff: { n: 'ฝนอุกกาบาตจอมเวท', d: 'อุกกาบาต 3 ลูกถล่มกลุ่มมอน ติดไฟ', k: 'meteor', c: 0xff5a1e, pf: 'fire/meteor-strike', pf2: 'fire/lava-burst', count: 3, burn: 3 },
  icestaff: { n: 'พายุหิมะ', d: 'พายุหิมะกลางฝูง มอนแข็งค้าง', k: 'frost', c: 0x96dcff, pf: 'ice/blizzard', pf2: 'ice/frost-nova' },
  orb: { n: 'สายฟ้าลูกโซ่', d: 'สายฟ้ากระโดด 5 ตัว มอนมึน', k: 'thunder', c: 0xbeb4ff, pf: 'lightning/lightning-strike', pf2: 'lightning/static-burst', count: 5 },
  poison: { n: 'หมอกพิษแม่มด', d: 'หมอกพิษกลางฝูง พิษสะสม', k: 'poison', c: 0x82ff5a, pf: 'nature/poison-cloud', pf2: 'nature/spore-burst' },
  skull: { n: 'คำสาปวิญญาณ', d: 'หลุมคำสาปดูดมอนแล้วระเบิด ติดพิษและไฟ', k: 'void', c: 0xaa6eff, pf: 'shadow/curse', pf2: 'shadow/void-implosion' },
  holytome: { n: 'ทัณฑ์สวรรค์', d: 'เสาแสงศักดิ์สิทธิ์ 2 ต้นลงกลางกลุ่มมอน', k: 'pillar', c: 0xffeb96, pf: 'holy/holy-smite', count: 2 },
  divinetome: { n: 'ลำแสงเทพเจ้า', d: 'ลำแสงสวรรค์ 3 ลำลงกลางกลุ่มมอน', k: 'pillar', c: 0xfff5be, pf: 'holy/divine-beam', pf2: 'holy/holy-smite', count: 3 },
  voidorb: { n: 'หลุมดำ', d: 'หลุมดำดูดมอนทั้งฝูงแล้วระเบิด', k: 'void', c: 0x9650ff, pf: 'shadow/void-implosion', pf2: 'explosions/implosion' },
  f_lichstaff: { n: 'คลื่นวิญญาณลิช', d: 'คลื่นวิญญาณระเบิดรอบตัว ติดพิษ', k: 'nova', c: 0x78ffa0, pf: 'shadow/shadow-tendrils', pf2: 'explosions/arcane-burst', poi: 3 },
  /* shields and food: on the champion */
  shield: { n: 'โล่ศักดิ์สิทธิ์', d: 'โล่ฟองแสงกันดาเมจก้อนใหญ่ สะท้อนหนามรอบตัว', k: 'guard', c: 0x8fc8ff, pf: 'holy/shield-bubble' },
  buckler: { n: 'โล่ปัดป้อง', d: 'โล่กันดาเมจ สะท้อนหนามรอบตัว', k: 'guard', c: 0x8fc8ff, pf: 'holy/barrier-block' },
  towershield: { n: 'ป้อมโล่หอคอย', d: 'โล่กันดาเมจก้อนใหญ่มาก', k: 'guard', c: 0x9fd8ff, pf: 'holy/shield-bubble' },
  fortress: { n: 'ป้อมปราการ', d: 'โล่ฟองแสงก้อนใหญ่ สะท้อนหนามแรง', k: 'guard', c: 0xbfe4ff, pf: 'holy/shield-bubble' },
  spikeshield: { n: 'โล่หนามคลั่ง', d: 'หนามเหล็กระเบิดรอบตัว + โล่', k: 'guard', c: 0xffc08a, pf: 'impacts/shockwave-ring', thorn: 2 },
  parrybuckler: { n: 'ปัดคืนสวนกลับ', d: 'โล่ + สวนกลับรอบตัว', k: 'guard', c: 0xffe08a, pf: 'impacts/parry', thorn: 1.5 },
  apple: { n: 'ผลไม้ฟื้นชีพ', d: 'ฟื้นเลือดต่อเนื่อง', k: 'feast', c: 0x9fe870, pf: 'nature/bloom-heal' },
  meat: { n: 'มื้อนักรบ', d: 'ฟื้นเลือดต่อเนื่องก้อนใหญ่', k: 'feast', c: 0x9fe870, pf: 'holy/regen-aura' },
  wine: { n: 'ไวน์ชุ่มชื่น', d: 'ฟื้นเลือดต่อเนื่อง', k: 'feast', c: 0xff8ab0, pf: 'holy/regen-aura' },
  bread: { n: 'ขนมปังอุ่น', d: 'ฟื้นเลือดต่อเนื่อง', k: 'feast', c: 0xffd890, pf: 'nature/bloom-heal' },
  potion: { n: 'ยาเลือดเข้มข้น', d: 'ฟื้นเลือดต่อเนื่องก้อนใหญ่', k: 'feast', c: 0xff6a7a, pf: 'holy/holy-heal' },
  honey: { n: 'น้ำผึ้งทอง', d: 'ฟื้นเลือดต่อเนื่อง', k: 'feast', c: 0xffd84a, pf: 'nature/bloom-heal' },
  elixir: { n: 'ยาอายุวัฒนะ', d: 'ฟื้นเลือดต่อเนื่องก้อนใหญ่มาก', k: 'feast', c: 0xffeb96, pf: 'holy/resurrect' },
  feast: { n: 'งานเลี้ยงชัยชนะ', d: 'ฟื้นเลือดต่อเนื่องก้อนใหญ่มาก', k: 'feast', c: 0x9fe870, pf: 'holy/regen-aura' },
  honeybread: { n: 'ขนมปังน้ำผึ้ง', d: 'ฟื้นเลือดต่อเนื่อง', k: 'feast', c: 0xffd84a, pf: 'nature/bloom-heal' },
};
/* a skill at the side-view duel (one enemy): x the item's damage, or x its block / heal */
const BAGISK_DUEL = { meteor: 1.4, thunder: 1.2, nova: 1.2, pillar: 1.4, spikes: 1.4, tornado: 1.2, blades: 1.2, rain: 1.2, void: 1.3, quake: 1.2, blood: 1.2, frost: 1.1, poison: 1, crit: .4, guard: 2, feast: 2 };   /* the duel: the skill is ONE extra blow of (item damage x this); crit = a sure crit of x (its mul x this) */
/* how many uses of the item set the skill off */
function iskEvery(S, d) { return S.every || (d && d.cd ? (d.cd <= 1.25 ? 6 : d.cd <= 2.25 ? 4 : 3) : 4); }
/* the skill of an item id (an item made from another one with no skill of its own uses its base's) */
function iskOf(id, base) { return ITEMSK[id] || (base && ITEMSK[base]) || null; }
const ISKN = { meteor: 'อุกกาบาต', thunder: 'สายฟ้าลูกโซ่', nova: 'ระเบิดรอบตัว', pillar: 'เสาแสง', spikes: 'หนามพุ่ง', tornado: 'พายุหมุน', blades: 'ใบมีดหมุน', rain: 'ฝนโจมตี', void: 'หลุมดำ', quake: 'แผ่นดินไหว', blood: 'ดูดเลือด', frost: 'แช่แข็ง', poison: 'หมอกพิษ', crit: 'คริติคอลใหญ่', guard: 'โล่', feast: 'ฟื้นเลือด' };
if (typeof module !== 'undefined') module.exports = { ITEMSK, BAGISK_DUEL, iskEvery, iskOf, ISKN };
