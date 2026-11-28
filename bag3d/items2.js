'use strict';
/* THE BIG ITEM REDESIGN OF THE BACKPACK GAME (talked through with the owner 2026-11-28, built on "ทำเลย"; notes: BAG 3D: BIG ITEM DESIGN in
   docs/action-game.md). Item MECHANICS follow the MOBA genre (owner: "เอาคุณสมบัติไอเทมแบบ Dota มาเลย ... คนละรูป"): names, pictures, texts and numbers
   are our own. Loaded by bag3d.html after bag3d/classes.js; bag3d.html merges IT2 into its item table IT.
   - three TYPES of champion: melee physical (mel), ranged physical (rng), magic (mag). An item's `cl` says which types may use it
     ('' / missing = everyone); the shop only shows what the champion's type can use.
   - MATERIALS (t 'm', mat): cheap, kept in a pouch (no bag cells), only for crafting.
   - CRAFTED items (`from` + `fee`): made with the "ประกอบ" button from a basic item + materials, paying only for the missing pieces.
   - a weapon's own mechanic is `x`, a whole-bag mechanic is `gx` (the same kind never stacks: the biggest one counts).
   - SPELL items (sp): everyone can use them, their power counts INT much more than other magic (a mage hits far harder).
   - BOOTS (boot): only one pair works.
   - ELEMENTS (el: f fire, i ice, l lightning, p poison): a weapon with an element lays a stack of it on every hit; a weapon with two elements
     alternates; five stacks of one = its big effect; two different elements meeting = a REACTION (bag3d/arena.js BAGEL). */
const BAGTYPE = { knight: 'mel', barbarian: 'mel', rogue: 'mel', ranger: 'rng', mage: 'mag', archer: 'rng', wing: 'mel', demon: 'mel', dark: 'mel', hood: 'mag', wolf: 'rng' };
const BAGTYPEN = { mel: ['ประชิด', '#ff8a6a', 'ui_mel', 'อาวุธประชิดและของสายประชิด'], rng: ['ยิงไกล', '#8ae07a', 'ui_rng', 'ธนู ของขว้าง และของสายยิง'], mag: ['เวท', '#c09cff', 'ui_mag', 'คทา ตำรา และของสายเวท'] };
const BAGRNG2 = new Set(['bow', 'frostbow', 'f_godbow', 'javelin', 'frostlance', 'shuriken', 'chakram']);
const ELN = { f: ['ไฟ', '#ff7a3a', 'el_f'], i: ['น้ำแข็ง', '#7ad0ff', 'el_i'], l: ['สายฟ้า', '#ffe14a', 'el_l'], p: ['พิษ', '#8ae05a', 'el_p'] };
/* reactions: shown in the help of the elements tome and in the fight (the numbers live in bag3d/arena.js BAGEL) */
const ELREACT = [['f', 'i', 'เปียกโชก', 'ติดสถานะเปียก 5 วิ'], ['w', 'l', 'ช็อตหนัก', 'ตัวที่เปียกโดนสายฟ้า: แรง x2 มึน และลามไปตัวที่เปียกรอบๆ'], ['f', 'l', 'โอเวอร์โหลด', 'ระเบิดเป็นวง กระเด็น'], ['i', 'l', 'แตกสลาย', 'ดาเมจก้อนใหญ่ เกราะแตก (โดนแรงขึ้น 20%)'],
  ['f', 'p', 'แก๊สระเบิด', 'ระเบิดพิษเป็นวง ติดไฟ'], ['i', 'p', 'พิษเยือกแข็ง', 'ช้าลงมากและพิษไม่หาย'], ['l', 'p', 'พิษลามทุ่ง', 'พิษกระจายไปตัวรอบๆ']];
const EL5 = { f: ['ลุกโชน', 'ระเบิดไฟรอบตัวมัน'], i: ['แช่แข็ง', 'แข็งค้าง 1.5 วิ'], l: ['ฟ้าผ่า', 'ฟ้าผ่าลงมาแล้วกระโดดต่อ'], p: ['กัดกร่อน', 'เกราะแตก พิษแรงขึ้น'] };
/* old items: who may use them, their elements */
const CLX = { stone: 'mel rng', fang: 'mel rng', book: 'mag', m_orb: 'mag', f_archmage: 'mag', f_lichstaff: 'mag', f_godbow: 'rng' };
const ELX = { wand: 'f', flamesword: 'f', archstaff: 'f', chakram: 'f', meteor: 'f', comet: 'f', bomb: 'f', icestaff: 'i', frostbow: 'i', frostlance: 'i', orb: 'l', thunderhammer: 'l', stormblades: 'l', poison: 'p', venomknife: 'p', skull: 'pf', f_lichstaff: 'fp' };
const ELADJ = { ember: 'f', frost: 'i', thunderstone: 'l', venomgland: 'p' };
const MATS = ['p_wood', 'p_feather', 'p_plate', 'p_hide', 'p_blade', 'p_fang', 'p_crystal', 'p_cloth', 'p_soul', 'p_herb'];
const MATD = 'วัสดุ: ใช้ประกอบของ (เก็บในถุงวัสดุ ไม่กินช่องกระเป๋า)';
const IT2 = {
  /* ---- materials */
  p_wood: { n: 'ไม้เนื้อแข็ง', sh: 'S1', c: 2, r: 1, t: 'm', mat: 1, d: MATD }, p_cloth: { n: 'ผ้าทอเวท', sh: 'S1', c: 2, r: 1, t: 'm', mat: 1, d: MATD }, p_soul: { n: 'ดวงวิญญาณ', sh: 'S1', c: 2, r: 1, t: 'm', mat: 1, d: MATD },
  /* ---- SHOOTING (ranged champions only) */
  b_spread: { n: 'ธนูสามศร', sh: 'V3', c: 13, r: 2, t: 'w', cl: 'rng', dmg: 5, cd: 1.6, sta: .9, crit: .15, base: 'bow', from: ['bow', 'p_wood', 'p_feather'], fee: 3, x: { multi: 3 }, d: 'ยิงทีละ 3 ดอก (ดอกเสริมแรง 40%)' },
  b_thunder: { n: 'ธนูอสนี', sh: 'V3', c: 13, r: 2, t: 'w', cl: 'rng', dmg: 7, cd: 1.5, sta: .8, crit: .2, base: 'bow', el: 'l', from: ['bow', 'p_crystal', 'p_blade'], fee: 3, x: { chain: [.1, 5, .7] }, d: '10% ลูกธนูกลายเป็นสายฟ้า กระโดดต่อ 5 ตัว' },
  b_double: { n: 'ธนูคู่แฝด', sh: 'V3', c: 13, r: 2, t: 'w', cl: 'rng', dmg: 7, cd: 1.5, sta: .8, crit: .2, base: 'bow', from: ['bow', 'p_feather', 'p_fang'], fee: 3, x: { twice: .2 }, d: '20% ยิงซ้ำอีกครั้งทันที' },
  a_pierce: { n: 'ศรเจาะเกราะ', sh: 'S1', c: 7, r: 2, t: 'g', cl: 'rng', from: ['p_blade', 'p_wood'], fee: 3, gx: { apierce: 1 }, d: 'ลูกธนูและของขว้างทุกชิ้นทะลุศัตรูเป็นแนว (ดวล: ทะลุเกราะและโล่ 50%)' },
  quiver: { n: 'ซองธนูนักล่า', sh: 'V2', c: 7, r: 2, t: 'g', cl: 'rng', from: ['p_hide', 'p_feather'], fee: 3, adj: { arrow: 1 }, d: 'ธนูที่ติดกัน ยิงเพิ่ม +1 ดอก (ธนูหนึ่งคันเพิ่มได้สูงสุด +4)' },
  b_rapid: { n: 'ธนูลมกรด', sh: 'V3', c: 13, r: 2, t: 'w', cl: 'rng', dmg: 5, cd: 1.4, sta: .7, crit: .15, base: 'bow', from: ['bow', 'p_feather', 'p_wood'], fee: 3, x: { rapid: [.1, 5] }, d: 'ยิงเป้าเดิมซ้ำ เร็วขึ้น +10% ต่อครั้ง (สูงสุด 5 ชั้น) เปลี่ยนเป้าแล้วเริ่มใหม่' },
  b_charge: { n: 'ธนูสะสมพลัง', sh: 'V3', c: 13, r: 2, t: 'w', cl: 'rng', dmg: 8, cd: 1.7, sta: .9, crit: .1, base: 'bow', from: ['bow', 'p_crystal', 'p_wood'], fee: 3, x: { nth: [6, 'crit'] }, d: 'ทุกดอกที่ 6 คริติคอลแน่นอน ทะลุทั้งแนว' },
  b_shock: { n: 'ธนูช็อต', sh: 'V3', c: 13, r: 2, t: 'w', cl: 'rng', dmg: 6, cd: 1.5, sta: .8, crit: .15, base: 'bow', from: ['bow', 'p_fang', 'p_crystal'], fee: 3, x: { jolt: [.25, .4] }, d: '25% ทำให้ศัตรูกระตุกชะงักชั่วครู่' },
  /* ---- MELEE (melee champions only) */
  s_spin: { n: 'ดาบวงพายุ', sh: 'V2', c: 12, r: 2, t: 'w', cl: 'mel', dmg: 9, cd: 1.8, sta: 1, base: 'sword', from: ['sword', 'p_blade', 'p_hide'], fee: 3, x: { spin: .15 }, d: '15% หมุนฟันทุกตัวรอบตัว' },
  s_double: { n: 'ดาบสองจังหวะ', sh: 'V2', c: 12, r: 2, t: 'w', cl: 'mel', dmg: 9, cd: 1.8, sta: 1, base: 'sword', from: ['sword', 'p_blade', 'p_feather'], fee: 3, x: { twice: .2 }, d: '20% ฟันซ้ำอีกครั้งทันที' },
  h_bash: { n: 'ค้อนกระแทกมึน', sh: 'V2', c: 11, r: 2, t: 'w', cl: 'mel', dmg: 12, cd: 2.4, sta: 1.4, base: 'club', from: ['club', 'p_plate', 'p_hide'], fee: 3, x: { bash: [.15, 1] }, d: '15% ทำให้ศัตรูมึน 1 วิ' },
  s_ramp: { n: 'ดาบกระหายศึก', sh: 'V2', c: 12, r: 2, t: 'w', cl: 'mel', dmg: 8, cd: 1.6, sta: 1, base: 'sword', from: ['sword', 'p_fang', 'p_blade'], fee: 3, x: { ramp: [.08, 5] }, d: 'ตีเป้าเดิมซ้ำ แรงขึ้น +8% ต่อครั้ง (สูงสุด 5 ชั้น)' },
  s_wave: { n: 'ดาบคลื่นสังหาร', sh: 'V2', c: 12, r: 2, t: 'w', cl: 'mel', dmg: 9, cd: 1.8, sta: 1, base: 'sword', from: ['sword', 'p_crystal', 'p_blade'], fee: 3, x: { nth: [4, 'wave'] }, d: 'ทุกครั้งที่ 4 ปล่อยคลื่นดาบยาวไปข้างหน้า' },
  s_dash: { n: 'ดาบพุ่งทะยาน', sh: 'S1', c: 10, r: 2, t: 'w', cl: 'mel', dmg: 8, cd: 3, sta: .6, base: 'dagger', mv: 'leapcut', from: ['dagger', 'p_feather', 'p_blade'], fee: 3, d: 'กระโจนเข้าหาศัตรูที่อยู่ไกล แล้วฟันเป็นวง' },
  g_counter: { n: 'ปลอกแขนสวนกลับ', sh: 'S1', c: 8, r: 2, t: 'd', cl: 'mel', armor: .5, from: ['p_plate', 'p_fang'], fee: 4, gx: { counter: .25 }, d: '25% สวนกลับเมื่อโดนตี · เกราะ +0.5' },
  blinkdagger: { n: 'มีดพริบตา', sh: 'S1', c: 11, r: 3, t: 'w', cl: 'mel', dmg: 9, cd: 6, sta: .5, base: 'dagger', mv: 'blinkstab', from: ['dagger', 'p_crystal', 'p_cloth'], fee: 3, d: 'ทุก 6 วิ วาร์ปไปหลังศัตรูตัวแข็งสุดแล้วแทง คริติคอลแน่นอน' },
  /* ---- MAGIC (mages only) */
  t_multi: { n: 'ตำราร่ายซ้ำ', sh: 'H2', c: 11, r: 3, t: 'g', cl: 'mag', from: ['book', 'p_crystal', 'p_cloth'], fee: 3, gx: { multicast: .2 }, adj: { mdmg: .15 }, d: 'อาวุธเวททุกชิ้น 20% ร่ายซ้ำทันที · อาวุธเวทที่ติดกันแรงขึ้น 15%' },
  st_blast: { ty: 'mag', n: 'คทาระเบิดเพลิง', sh: 'V2', c: 13, r: 2, t: 'w', cl: 'mag', dmg: 7, cd: 2, sta: 1, burn: 1.5, base: 'wand', el: 'f', mv: 'blast', from: ['wand', 'p_crystal', 'p_wood'], fee: 3, d: 'ลูกไฟระเบิดเป็นวงกว้าง ติดไฟ 1.5' },
  st_beam: { ty: 'mag', n: 'คทาลำแสง', sh: 'V2', c: 13, r: 2, t: 'w', cl: 'mag', dmg: 9, cd: 2.2, sta: 1, base: 'wand', mv: 'beam', from: ['wand', 'p_crystal', 'p_crystal'], fee: 3, d: 'ยิงลำแสงทะลุศัตรูทั้งแนว' },
  o_soul: { n: 'ลูกแก้ววิญญาณ', sh: 'S1', c: 9, r: 2, t: 'g', cl: 'mag', from: ['p_soul', 'p_crystal'], fee: 4, gx: { soul: .15 }, d: 'ดาเมจเวท 15% กลับมาเป็นเลือด' },
  st_spirit: { ty: 'mag', n: 'คทาภูตพราย', sh: 'V2', c: 13, r: 2, t: 'w', cl: 'mag', dmg: 6, cd: 1.9, sta: 1, base: 'wand', from: ['wand', 'p_soul', 'p_wood'], fee: 3, x: { nth: [3, 'spirit'] }, d: 'ทุกครั้งที่ 3 ภูตพรายพุ่งตามล่าศัตรู' },
  g_mpierce: { n: 'ศิลาเจาะมนตร์', sh: 'S1', c: 8, r: 2, t: 'g', cl: 'mag', from: ['p_crystal', 'p_blade'], fee: 4, gx: { mpierce: .3 }, d: 'เวททะลุการต้านเวท 30% · บอสและหัวหน้าฝูงโดนเวทแรงขึ้น 15%' },
  t_haste: { n: 'ตำราเร่งเวท', sh: 'H2', c: 11, r: 3, t: 'g', cl: 'mag', from: ['book', 'p_feather', 'p_cloth'], fee: 3, gx: { skcd: .2 }, adj: { cd: .1 }, d: 'สกิลแชมเปี้ยนมาเร็วขึ้น 20% · อาวุธที่ติดกันเร็วขึ้น 10%' },
  /* ---- SPELL ITEMS (everyone; power from INT) */
  sp_storm: { ty: 'mag', sp: 1, n: 'ศิลาพายุผลัก', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 4, cd: 6, sta: .5, mv: 'storm', from: ['p_feather', 'p_crystal'], fee: 4, d: 'พายุหมุนรอบตัว ผลักศัตรูกระเด็นออกไป' },
  sp_stones: { ty: 'mag', sp: 1, n: 'ศิลาพิทักษ์', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 3, cd: 9, sta: .5, mv: 'stones', from: ['p_plate', 'p_crystal'], fee: 4, d: 'เสกหิน 3 ก้อนหมุนรอบตัว รับดาเมจแทนและชนศัตรู (ความทนขึ้นกับ INT)' },
  sp_blink: { n: 'ผ้าคลุมพริบตา', sh: 'V2', c: 11, r: 3, t: 'd', cat: 'spell', dodge: .06, mres: .1, from: ['cloak', 'p_cloth'], fee: 3, gx: { blink: 8 }, d: 'วาร์ปหนีเมื่อกำลังจะโดนตีหนัก (ทุก 8 วิ) · หลบ 6% · ต้านเวท 10%' },
  sp_ball: { ty: 'mag', sp: 1, n: 'ลูกแก้วอสนีบาต', sh: 'S1', c: 9, r: 3, t: 'w', dmg: 3, cd: 7, sta: .5, el: 'l', mv: 'ball', from: ['p_crystal', 'p_crystal', 'p_soul'], fee: 3, d: 'ปล่อยลูกบอลสายฟ้าลอยช้าๆ ช็อตรัวและผลักศัตรู' },
  sp_skel: { ty: 'mag', sp: 1, n: 'คทาโครงกระดูก', sh: 'V2', c: 8, r: 2, t: 'w', dmg: 4, cd: 12, sta: .5, mv: 'skel', from: ['p_soul', 'p_wood'], fee: 4, d: 'เรียกนักรบโครงกระดูก 2 ตนมาช่วยสู้ 10 วิ' },
  sp_sprite: { ty: 'mag', sp: 1, n: 'ภูตไฟ', sh: 'S1', c: 10, r: 2, t: 'w', dmg: 3, cd: 10, sta: .5, el: 'f', mv: 'sprite', from: ['ember', 'p_soul'], fee: 3, d: 'ภูตไฟบินวนรอบตัว ยิงลูกไฟใส่ศัตรู 8 วิ' },
  sp_totem: { ty: 'mag', sp: 1, n: 'โทเท็มเวท', sh: 'V2', c: 8, r: 2, t: 'w', dmg: 4, cd: 11, sta: .5, mv: 'totem', from: ['p_wood', 'p_crystal'], fee: 4, d: 'ปักโทเท็มลงพื้น ยิงเวทใส่ศัตรูรอบๆ 8 วิ' },
  sp_time: { ty: 'mag', sp: 1, n: 'นาฬิกาหยุดเวลา', sh: 'S1', c: 12, r: 3, t: 'w', dmg: 0, cd: 14, sta: .5, mv: 'tstop', from: ['hourglass', 'p_crystal'], fee: 3, d: 'หยุดเวลาศัตรูรอบตัว 1.5 วิ (บอส 0.6 วิ)' },
  sp_hex: { ty: 'mag', sp: 1, n: 'ไม้เท้าสาปกบ', sh: 'V2', c: 9, r: 2, t: 'w', dmg: 0, cd: 10, sta: .5, mv: 'hex', from: ['p_wood', 'p_herb', 'p_soul'], fee: 3, d: 'สาปศัตรูตัวที่แข็งที่สุดเป็นกบ 3 วิ (บอส 1.5 วิ)' },
  sp_vine: { ty: 'mag', sp: 1, n: 'เมล็ดเถาวัลย์', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 2, cd: 8, sta: .5, mv: 'vine', from: ['p_herb', 'p_wood'], fee: 4, d: 'เถาวัลย์รัดศัตรูเป็นวง ขยับไม่ได้ 2 วิ' },
  sp_silence: { ty: 'mag', sp: 1, n: 'ระฆังสะกดเสียง', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 0, cd: 12, sta: .5, mv: 'silence', from: ['p_plate', 'p_cloth'], fee: 4, d: 'ศัตรูรอบตัวใช้สกิลและยิงไม่ได้ 4 วิ (ดวล: สกิลคู่แข่งถูกปิด)' },
  sp_weak: { ty: 'mag', sp: 1, n: 'ตุ๊กตาอ่อนแรง', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 0, cd: 9, sta: .5, mv: 'weak', from: ['p_cloth', 'p_herb'], fee: 4, d: 'สาปศัตรูเป็นวง ตีเบาลง 25% นาน 5 วิ' },
  sp_brittle: { ty: 'mag', sp: 1, n: 'ตราเปราะบาง', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 0, cd: 9, sta: .5, mv: 'brittle', from: ['p_fang', 'p_cloth'], fee: 4, d: 'สาปศัตรูเป็นวง โดนดาเมจแรงขึ้น 20% นาน 5 วิ' },
  sp_mark: { ty: 'mag', sp: 1, n: 'ตรามรณะ', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 5, cd: 8, sta: .5, mv: 'mark', from: ['p_soul', 'p_fang'], fee: 4, d: 'ประทับตราศัตรู 3 ตัว เลือดต่ำกว่า 15% ตายทันที (บอส 6%)' },
  sp_spread: { ty: 'mag', sp: 1, n: 'คำสาปลามทุ่ง', sh: 'S1', c: 8, r: 2, t: 'w', dmg: 3, cd: 8, sta: .5, mv: 'spread', from: ['p_soul', 'p_herb'], fee: 4, d: 'คำสาปกัดกินต่อเนื่อง ตัวที่ตายคำสาปลามไปตัวข้างๆ' },
  t_elem: { n: 'ตำราธาตุทั้งสี่', sh: 'H2', c: 10, r: 3, t: 'g', cat: 'spell', from: ['p_crystal', 'p_cloth', 'p_soul'], fee: 4, gx: { react: .5 }, d: 'ปฏิกิริยาธาตุแรงขึ้น 50% และแรงขึ้นอีกตาม INT' },
  /* ---- GENERAL */
  critedge: { n: 'คมมรณะ', sh: 'S1', c: 8, r: 2, t: 'u', gcrit: .2, critd: .5, from: ['p_blade', 'p_fang'], fee: 4, d: 'คริติคอลทุกชิ้น +20% · ดาเมจคริ x2.5' },
  critring: { n: 'แหวนเพชฌฆาต', sh: 'S1', c: 8, r: 2, t: 'u', gcrit: .05, critd: .5, from: ['p_crystal', 'p_fang'], fee: 4, d: 'ดาเมจคริติคอล +50% · คริติคอล +5%' },
  execaxe: { n: 'ขวานประหารยักษ์', sh: 'V2', c: 20, r: 3, t: 'u', uni: 1, gcrit: .3, critd: 1.2, from: ['critedge', 'critring'], fee: 4, d: 'ของชิ้นใหญ่: คริติคอล +30% · ดาเมจคริ +120% (มีได้ชิ้นเดียว)' },
  trueeye: { n: 'เนตรเหยี่ยว', sh: 'S1', c: 9, r: 2, t: 'u', from: ['p_feather', 'p_crystal'], fee: 5, gx: { sure: 1, mhit: 2 }, d: 'ตีไม่มีวันพลาด (แก้ทางสายหลบ) · ทุกครั้งที่ตีบวกดาเมจเวท 2' },
  windblade: { n: 'ใบมีดวายุ', sh: 'V2', c: 11, r: 3, t: 'u', haste: .25, from: ['glove', 'p_feather', 'p_blade'], fee: 3, d: 'ความเร็วโจมตีทุกชิ้น +25%' },
  magecoat: { n: 'เสื้อคลุมต้านเวท', sh: 'V2', c: 8, r: 2, t: 'd', hp: 15, mres: .25, from: ['p_cloth', 'p_hide'], fee: 4, d: 'ต้านเวท 25% · +เลือด 15' },
  frostplate: { n: 'เกราะเยือกแข็ง', sh: 'SQ', c: 17, r: 3, t: 'd', hp: 36, armor: 2.6, from: ['plate', 'frost'], fee: 4, gx: { chill: .3 }, d: 'ของชิ้นใหญ่: +เลือด 36 · เกราะ +2.6 · ศัตรูที่ตีเราช้าลง 30%' },
  bloodfang: { n: 'เขี้ยวดูดเลือด', sh: 'S1', c: 9, r: 2, t: 'u', uni: 1, gls: .1, from: ['p_fang', 'p_soul'], fee: 5, d: 'อาวุธทุกชิ้นดูดเลือด 10% (มีได้ชิ้นเดียว)' },
  hunterskull: { n: 'กะโหลกนักล่า', sh: 'S1', c: 9, r: 2, t: 'u', from: ['p_fang', 'p_hide'], fee: 5, gx: { skull: 20 }, d: 'ฆ่าศัตรู 1 ตัว ดาเมจ +1 (สูงสุด +20 ต่อรอบ)' },
  autopotion: { n: 'ยาฉุกเฉิน', sh: 'S1', c: 9, r: 2, t: 'f', from: ['potion', 'p_herb'], fee: 2, gx: { potion: .35 }, d: 'เลือดต่ำกว่า 30% ดื่มเองทันที ฟื้น 35% (รอบละครั้ง)' },
  revive: { n: 'ศิลาคืนชีพ', sh: 'S1', c: 14, r: 3, t: 'u', uni: 1, from: ['p_soul', 'p_soul', 'p_crystal'], fee: 8, gx: { revive: .5 }, d: 'ตายแล้วฟื้นคืนชีพ เลือด 50% (รอบละครั้ง · มีได้ชิ้นเดียว)' },
  spellshield: { n: 'โล่กันเวท', sh: 'S1', c: 9, r: 2, t: 'd', mres: .08, from: ['p_cloth', 'p_plate'], fee: 5, gx: { sshield: 10 }, d: 'กันการโจมตีหนักหรือเวท 1 ครั้ง ทุก 10 วิ · ต้านเวท 8%' },
  nostun: { n: 'ศิลาจิตมั่น', sh: 'S1', c: 8, r: 2, t: 'u', regen: .4, from: ['p_herb', 'p_crystal'], fee: 4, gx: { nostun: 1 }, d: 'ไม่ติดมึน ไม่ติดแช่แข็ง · ฟื้นเลือดเอง 0.4/วิ' },
  /* ---- BOOTS (one pair works) */
  bt_wind: { n: 'รองเท้าสายลม', sh: 'H2', c: 9, r: 2, t: 'd', boot: 1, mspd: .2, dodge: .1, from: ['boots', 'p_feather'], fee: 3, d: 'เดินเร็ว +20% · หลบ 10%' },
  bt_sprint: { n: 'รองเท้าเร่งฝีเท้า', sh: 'H2', c: 9, r: 2, t: 'd', boot: 1, mspd: .1, from: ['boots', 'p_fang'], fee: 3, gx: { sprint: 1 }, d: 'เดินเร็ว +10% · โดนตีแล้ววิ่งเร็วขึ้นมาก 2 วิ' },
  bt_leap: { n: 'รองเท้ากระโจน', sh: 'H2', c: 10, r: 2, t: 'd', boot: 1, mspd: .1, from: ['boots', 'p_hide', 'p_blade'], fee: 2, gx: { leap: 8 }, d: 'เดินเร็ว +10% · ทุก 8 วิกระโจนใส่ศัตรู กระแทกเป็นวง' },
  bt_armor: { n: 'รองเท้าเกราะเหล็ก', sh: 'H2', c: 9, r: 2, t: 'd', boot: 1, mspd: .1, armor: 1.5, hp: 10, from: ['boots', 'p_plate'], fee: 3, d: 'เดินเร็ว +10% · เกราะ +1.5 · +เลือด 10' },
  bt_magic: { n: 'รองเท้าจอมเวท', sh: 'H2', c: 9, r: 2, t: 'd', boot: 1, mspd: .12, from: ['boots', 'p_crystal'], fee: 3, gx: { skcd: .1 }, d: 'เดินเร็ว +12% · สกิลแชมเปี้ยนมาเร็วขึ้น 10%' },
  bt_retreat: { n: 'รองเท้าถอยฉาก', sh: 'H2', c: 9, r: 2, t: 'd', cl: 'rng mag', boot: 1, mspd: .1, from: ['boots', 'p_cloth'], fee: 3, gx: { retreat: 4 }, d: 'เดินเร็ว +10% · ศัตรูเข้าประชิดจะถอยฉากออกอย่างเร็ว (ทุก 4 วิ)' },
};
const UIICONS = ['ui_pouch', 'ui_anvil', 'ui_mel', 'ui_rng', 'ui_mag', 'el_f', 'el_i', 'el_l', 'el_p', 'ui_cup', 'ui_dice'];
const BAGATTR2 = {
  b_spread: [0, 4, 0], b_thunder: [0, 3, 2], b_double: [0, 4, 0], a_pierce: [0, 2, 0], quiver: [0, 2, 0], b_rapid: [0, 5, 0], b_charge: [1, 3, 0], b_shock: [0, 3, 1],
  s_spin: [2, 2, 0], s_double: [1, 3, 0], h_bash: [4, 0, 0], s_ramp: [3, 1, 0], s_wave: [2, 1, 1], s_dash: [0, 3, 0], g_counter: [3, 0, 0], blinkdagger: [0, 4, 1],
  t_multi: [0, 0, 4], st_blast: [0, 0, 4], st_beam: [0, 0, 4], o_soul: [1, 0, 3], st_spirit: [0, 0, 4], g_mpierce: [0, 0, 3], t_haste: [0, 1, 3],
  sp_storm: [0, 1, 2], sp_stones: [2, 0, 2], sp_blink: [0, 2, 2], sp_ball: [0, 0, 3], sp_skel: [1, 0, 3], sp_sprite: [0, 0, 3], sp_totem: [0, 0, 3], sp_time: [0, 0, 4], sp_hex: [0, 0, 3], sp_vine: [1, 0, 2],
  sp_silence: [1, 0, 2], sp_weak: [0, 0, 3], sp_brittle: [0, 1, 2], sp_mark: [0, 1, 3], sp_spread: [0, 0, 3], t_elem: [0, 0, 5],
  critedge: [0, 3, 0], critring: [0, 2, 1], execaxe: [3, 5, 0], trueeye: [0, 3, 1], windblade: [0, 6, 0], magecoat: [2, 0, 2], frostplate: [7, 0, 1], bloodfang: [2, 2, 0], hunterskull: [2, 2, 0],
  autopotion: [2, 0, 0], revive: [3, 0, 3], spellshield: [2, 0, 2], nostun: [2, 0, 1],
  bt_wind: [0, 4, 0], bt_sprint: [1, 3, 0], bt_leap: [2, 2, 0], bt_armor: [4, 0, 0], bt_magic: [0, 0, 6], bt_retreat: [0, 4, 0],
};
if (typeof BAGATTR !== 'undefined') { Object.assign(BAGATTR, BAGATTR2); for (const k of ['p_blade', 'p_hide', 'p_plate', 'p_feather', 'p_crystal', 'p_fang', 'p_herb']) delete BAGATTR[k]; }
/* who may use an item ('' = everyone): its own `cl`, else weapons go by what they are */
function itemCl(d) { if (d.cl !== undefined) return d.cl; if (d.t === 'w' && !d.sp) return d.ty === 'mag' ? 'mag' : BAGRNG2.has(d.id) || BAGRNG2.has(d.base) ? 'rng' : 'mel'; return ''; }
function canUse(d, ty) { const c = itemCl(d); return !c || !ty || c.split(' ').includes(ty); }
/* the page of the build shop an item is on */
function itemCat(d) { if (d.cat) return d.cat; if (d.boot) return 'boot'; if (d.sp) return 'spell'; if (d.cl !== undefined && d.from) return 'type'; if (/^[mf]_/.test(d.id)) return 'top'; return 'gen'; }
if (typeof module !== 'undefined') module.exports = { IT2, BAGTYPE, BAGTYPEN, ELN, ELREACT, EL5, CLX, ELX, ELADJ, MATS, UIICONS, itemCl, canUse, itemCat };
