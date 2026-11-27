'use strict';
/* THE HORDE FIGHT OF THE BACKPACK GAME (owner 2026-11-27: "อยากให้รูปแบบภาพต่อสู้เป็นเหมือน ... แนวๆ แวมไพร์เราก็ได้ แต่เอาระบบกระเป๋าเข้าไป",
   "ตัวเดียวสู้กับฝูงมอนตามไอเทมในกระเป๋าเรา"). Runs inside horde.html?bag=1 (its engine: map, pixel monster cards, hero, effects), shown by
   bag3d.html in an iframe for every monster / boss round. This file = the bag mode only; horde.html calls it from a few `if (BAGM)` hooks.
   - bag3d.html posts { bag: 'start', cfg }: cfg = round, boss, the champion's built numbers (build() in bag3d.html: life, armour, crit ...) and
     every working item with its own numbers after neighbour bonuses. This page answers { bag: 'ready' } once and { bag: 'end', win, ... }.
   - One champion (the wolf hunter) against the round's horde: all monsters of the wave must die. Items fire by themselves on their own
     cooldown and stamina, each with its own move (BAGMOVE -> BAGFIRE). The fight is fully AUTOMATIC (owner: "ไม่ต้องบังคับดิ ให้มันออโต้"): the champion
     walks and dashes by itself (bagAuto), the player only arranges the bag before the fight and may switch x1 / x2.
   - Numbers to tune: bagWave() (how many, how strong), BAGFIRE reach / area. Names here all start with bag / BAG (horde.html has none). */
const BAG = { on: false, ready: false, cfg: null, st: {}, its: [], t: 0, mhp: 8, mdmg: 4, spd: 1, auto: true, man: 0, plan: [], pi: 0, total: 0, dur: 30, blk: 0, sta: 5, tk: 0, sk: null, done: false, bossWait: false, fear: 1.6, reach: 2, coinP: .2, img: null, tex: null, icr: 14, spr: [], pops: [], drops: [], hpShow: 0 };
/* item id -> [move, colour, options]. An item made from another one (cfg item.base) that is not listed uses its base's move. */
const BAGMOVE = {
  dagger: ['stab', 0xcda0ff], venomknife: ['stab', 0x8cff5a], sword: ['wave', 0x96c8ff], flamesword: ['wave', 0xff8228], katana: ['iai', 0xaaffeb],
  greatsword: ['cleave', 0xaa6eff], executioner: ['guillotine', 0xff4646], twinblades: ['xcut', 0xcdb9ff], stormblades: ['xcut', 0x96e6ff, { storm: 1 }],
  rapier: ['thrust', 0xebf0ff], luckrapier: ['thrust', 0xb4ff96], spear: ['pierce', 0xffdc8c], frostlance: ['pierce', 0x96dcff], javelin: ['toss', 0xffe6aa, { fast: 1 }],
  axe: ['toss', 0xffaa64], bloodaxe: ['toss', 0xff3c3c], hammer: ['slam', 0xffdc96], thunderhammer: ['slam', 0xbeb4ff, { bolt: 1 }], club: ['bonk', 0xf0c88c],
  claw: ['claws', 0xff8c50], vampclaw: ['claws', 0xff326e], scythe: ['reap', 0xb46eff], shuriken: ['star', 0xdce6ff], chakram: ['disc', 0xff9632],
  bow: ['arrows', 0xfff0c8, { n: 1 }], frostbow: ['arrows', 0x96e1ff, { n: 1 }], f_godbow: ['arrows', 0xffe178, { n: 3 }],
  wand: ['fireball', 0xff8228, { n: 1 }], archstaff: ['fireball', 0xff5a1e, { n: 3 }], icestaff: ['icicle', 0x96dcff], orb: ['chain', 0xbeb4ff],
  poison: ['flask', 0x82ff5a], skull: ['curse', 0xaa6eff], holytome: ['skyray', 0xffeb96], divinetome: ['skyray', 0xfff5be, { big: 1 }], voidorb: ['implode', 0x9650ff], f_lichstaff: ['lich', 0x78ffa0],
  bomb: ['bombtoss', 0xffaa50], meteor: ['meteor', 0xff6a30], comet: ['meteor', 0xff6a30, { big: 1 }], lantern: ['wisps', 0x78c8ff, { n: 3 }], soullantern: ['wisps', 0xff5a8c, { n: 6 }],
};
/* THE CHAMPION'S MOVES (owner 2026-11-27 "ท่าอนิเมชั่นสวยๆ เท่ๆ"): every item move plays its own body move: [clips (taken in turn), speed, weight].
   A move in progress is only cut short by a heavier one (weight 3 > 2 > 1 > 0). Weight 2+ uses the whole body when the champion stands still.
   Clips = KayKit + Quaternius Universal Animation Library (both CC0), already on our skeleton (art/grind3d/hero_anims.glb, ual_anims.json). */
const BAGANIM = { cut: [['Q_Sword_Regular_A', 'Q_Sword_Regular_B'], .45, 1], wave: [['Q_Sword_Regular_A', 'Q_Sword_Regular_B'], .46, 1], xcut: [['Q_Sword_Regular_B', 'Q_Sword_Regular_A'], .4, 1], claws: [['Q_Sword_Regular_A', 'Q_Sword_Regular_B'], .34, 1],
  stab: [['Melee_1H_Attack_Stab'], .45, 1], thrust: [['Melee_1H_Attack_Stab'], .42, 1], pierce: [['Melee_1H_Attack_Stab'], .55, 1], iai: [['Q_Sword_Dash'], .6, 2], bonk: [['Q_Sword_Regular_B'], .5, 1],
  cleave: [['Melee_1H_Attack_Jump_Chop'], .7, 2], guillotine: [['Melee_1H_Attack_Jump_Chop'], .75, 2], slam: [['Melee_1H_Attack_Jump_Chop'], .7, 2], reap: [['Melee_2H_Attack_Spin'], .8, 2],
  toss: [['Q_OverhandThrow'], .5, 1], star: [['Q_OverhandThrow'], .36, 1], disc: [['Q_OverhandThrow'], .5, 1], flask: [['Q_OverhandThrow'], .55, 1], bombtoss: [['Q_OverhandThrow'], .6, 2],
  arrows: [['Ranged_Bow_Release'], .55, 1], fireball: [['Q_Spell_Simple_Shoot'], .45, 1], icicle: [['Q_Spell_Simple_Shoot'], .45, 1], chain: [['Q_Spell_Simple_Shoot'], .4, 1], curse: [['Q_Spell_Simple_Shoot'], .5, 1], skyray: [['Q_Spell_Simple_Shoot'], .5, 1],
  lich: [['Ranged_Magic_Summon'], .9, 2], implode: [['Ranged_Magic_Summon'], .9, 2], meteor: [['Ranged_Magic_Summon'], 1, 2], wisps: [['Ranged_Magic_Summon'], 1, 2],
  skill: [['Ranged_Bow_Release_Up'], .8, 3], block: [['Melee_Block'], .5, 0], eat: [['Use_Item'], .6, 0], hurt: [['Hit_A'], .32, 0] };   /* [clips taken in turn, seconds the move takes, weight] */
/* class moves (bag3d/classes.js, owner 2026-11-28): the same item move looks like the class that does it: the axe barbarian swings two-handed, the
   mage casts what others throw, the knight cuts with sword and shield, the ranger keeps the bow. bagStart fills BAG.anim from cfg.cls. */
const BAGCLSANIM = {
  barbarian: { cut: [['Melee_2H_Attack_Chop', 'Melee_2H_Attack_Slice'], .55, 1], wave: [['Melee_2H_Attack_Slice', 'Melee_2H_Attack_Chop'], .55, 1], xcut: [['Melee_2H_Attack_Slice'], .5, 1], bonk: [['Melee_2H_Attack_Chop'], .55, 1], claws: [['Melee_2H_Attack_Slice'], .45, 1], cleave: [['Melee_2H_Attack_Chop'], .7, 2], slam: [['Melee_2H_Attack_Chop'], .7, 2], guillotine: [['Melee_2H_Attack_Chop'], .75, 2], arrows: [['Q_OverhandThrow'], .5, 1] },
  mage: { arrows: [['Q_Spell_Simple_Shoot'], .45, 1], toss: [['Q_Spell_Simple_Shoot'], .45, 1], star: [['Q_Spell_Simple_Shoot'], .36, 1], disc: [['Q_Spell_Simple_Shoot'], .45, 1], cut: [['Melee_1H_Attack_Stab'], .45, 1], wave: [['Melee_1H_Attack_Stab'], .45, 1] },
  knight: { arrows: [['Q_OverhandThrow'], .5, 1], cut: [['Melee_1H_Attack_Slice_Horizontal', 'Q_Sword_Regular_A'], .45, 1], block: [['Melee_Block_Attack'], .5, 0] },
  rogue: { cut: [['Melee_1H_Attack_Stab', 'Melee_1H_Attack_Slice_Diagonal'], .34, 1], wave: [['Melee_1H_Attack_Slice_Diagonal', 'Melee_1H_Attack_Stab'], .36, 1], arrows: [['Q_OverhandThrow'], .4, 1] },
  ranger: {},
};
function bagSwing(mv, ang) { const H = HERO, M = H.M, A = (BAG.anim && BAG.anim[mv]) || BAGANIM[mv] || BAGANIM.cut; if (H.dead || BAG.done) return; if (H.atkT > 0 && A[2] <= (H.apr || 0)) return; const an = A[0][(H.combo = (H.combo | 0) + 1) % A[0].length], act = M.acts[an + '_up']; if (!act) return;
  const ts = act.getClip().duration / A[1]; chPlay(M, 'U', an, true, ts); H.atkT = A[1] * .88; H.apr = A[2]; if (ang != null && !H.moving) H.aim = ang; if (A[2] >= 2 && !H.moving) { chPlay(M, 'L', an, true, ts); H.dodgeT = A[1] * .88; } }
const bagPos = () => HERO.pos, bagNear = R => nearest(HERO.pos.x, HERO.pos.z, R), bagFx = f => { if (!NORENDER) f(); };
const bagAngD = (a, b) => Math.abs(((a - b + Math.PI) % TAU + TAU) % TAU - Math.PI);
function bagLine(x, z, a, L, c, w) { bagFx(() => boltFx(new V3(x, .7, z), new V3(x + Math.sin(a) * L, .7, z + Math.cos(a) * L), c, w)); }
/* one hit of item W on monster m: the item's own crit, execute, poison / burn / slow / stun, life steal. mul = share of its damage */
function bagHit(W, m, mul, o) {
  if (m.dead) return 0; const S = BAG.st; let d = W.dmg * (mul || 1); const crit = d > 0 && Math.random() < (W.crit || 0) + (S.crit || 0); if (crit) d *= S.critd || 2;
  if (W.exe && m.hp < m.max * .3) d *= 1 + W.exe; if (S.rage) d *= 1 + S.rage * Math.max(0, 1 - HERO.hp / HERO.max); if (W.pierce && (m.elite || m.boss)) d *= 1 + W.pierce * .5;
  const q = Object.assign({ w: W.id, crit, color: W.ty === 'mag' ? '#e0c4ff' : undefined }, o); if (q.kb) q.kb *= .45;   /* small pushes: the horde must be able to reach the champion */ if (W.burn) q.burn = W.burn * .3; if (W.frz) { q.slow = Math.min(.6, W.frz * 1.2); q.slowT = 2; } if (W.stun) q.frz = W.stun;
  const dealt = hitMon(m, d, q); if (W.poi && !m.dead) m.poi = Math.min((m.poi || 0) + W.poi * .5, W.poi * 4); if (W.ls && dealt) healHero(Math.min(dealt * W.ls * .35, HERO.max * .03)); return dealt;
}
function bagBoom(W, x, z, r, mul, o = {}) {   /* everything in the circle (o.main = that one takes the full hit, the others half) */
  inCircle(x, z, r, m => bagHit(W, m, (mul || 1) * (o.main && m !== o.main ? .5 : 1), { fx: x, fz: z, kb: o.kb === undefined ? 2.5 : o.kb })); const c = o.c || 0xffa040;
  PARTS.push({ x, y: .5, z, vx: 0, vy: 0, vz: 0, t: 0, life: .22, s: r * 2.2, c, g: 0, a: BRIGHT ? .45 : .8 }); spark(x, .4, z, { n: Math.min(14, 5 + r * 3 | 0), color: c, spd: 3 + r, up: 3, size: .3, life: .4 }); decal('shock', x, z, r * 2.25, c, 0xfff6e0, { life: .4, y: .09 }); if (o.pf) pfx(o.pf, x, z, r * (o.pfs || 2.4), { cut: o.pfc });
}
function bagZone(z, m) { const W = z.bag; hitMon(m, Math.max(1, ((W.poi || 0) + (z.curse ? W.burn || 0 : 0)) * .55 + (W.dmg || 0) * .2), { w: W.id, slow: .3, slowT: .7, burn: z.curse && W.burn ? W.burn * .3 : undefined, color: z.curse ? '#e0b0ff' : '#c8f080' }); if (!m.dead && W.poi) m.poi = Math.min((m.poi || 0) + W.poi * .15, W.poi * 4); }
function bagDense(R, r) { let best = null, bn = -1; for (const m of MON) { if (m.dead || (m.x - HERO.pos.x) ** 2 + (m.z - HERO.pos.z) ** 2 > R * R) continue; let n = m.boss ? 4 : 0; for (const q of MON) if (!q.dead && (q.x - m.x) ** 2 + (q.z - m.z) ** 2 < r * r) n++; if (n > bn) { bn = n; best = m; } } return best; }
function bagTop(R) { let m = null; for (const q of MON) if (!q.dead && (q.x - HERO.pos.x) ** 2 + (q.z - HERO.pos.z) ** 2 < R * R && (!m || q.hp > m.hp)) m = q; return m; }
/* ---- the moves: return false = nothing in reach (the item waits), a number = the direction it fired in */
const BAGFIRE = {
  wave(W, C) { const m = bagNear(8.5); if (!m) return false; const a = dirTo(m), p = shootP('wave', a, { bag: W, mul: 1, spd: 10.5, life: .85, r: 1.05, kb: 2, y: .4 });
    if (!NORENDER) { p.mesh = (DEC_POOL.swoosh || []).pop() || decalMesh('swoosh'); decalSet(p.mesh, C, 0xffffff, { full: 1, ord: 4 }); p.mesh.scale.set(2.7, 1, 2.7); p.mesh.rotation.y = a - Math.PI / 2; scene.add(p.mesh); } sfx('whoosh', .5, 1.1); return a; },
  stab(W, C) { const m = bagNear(2.7); if (!m) return false; const a = dirTo(m), P0 = bagPos(); bagHit(W, m, 1, { kb: 1 }); arcFx(P0.x, P0.z, a, 1.9, C, .16, 1); after(.07, () => arcFx(bagPos().x, bagPos().z, a, 1.9, C, .16, -1)); spark(m.x, .6, m.z, { n: 3, color: C, spd: 2.5, size: .22, life: .25 }); sfx('slash', .3, 1.5); return a; },
  iai(W, C) { const m = bagNear(6.5); if (!m) return false; const a = dirTo(m), sx = Math.sin(a), sz = Math.cos(a), x0 = bagPos().x, z0 = bagPos().z, L = 7.2; bagLine(x0, z0, a, L, 0xffffff, .05);
    after(.1, () => { for (const q of MON) { if (q.dead) continue; const dx = q.x - x0, dz = q.z - z0, t = dx * sx + dz * sz; if (t > -.2 && t < L && Math.abs(dx * sz - dz * sx) < .8 + q.r) bagHit(W, q, 1, { kb: 1.5 }); } bagLine(x0, z0, a, L, C, .16); }); sfx('slash', .5, 1.7); return a; },
  cleave(W, C) { const m = bagNear(4.6); if (!m) return false; const x = m.x, z = m.z; column({ x, z }, C, .3, .5, 5); after(.12, () => { bagBoom(W, x, z, 2.3, 1, { c: C, pf: 'impacts/ground-slam', pfs: 2.2 }); shake(.2); }); sfx('whoosh', .6, .8); return dirTo(m); },
  guillotine(W, C) { const m = bagTop(7); if (!m) return false; const x = m.x, z = m.z; column({ x, z }, C, .45, .7, 7); bagDrop(W, x, z, .16); after(.16, () => { bagBoom(W, x, z, 1.5, 1, { c: C, main: m, pf: 'impacts/ground-slam', pfs: 2 }); shake(.3); sfx('boom', .5, .8); }); return dirTo(m); },
  xcut(W, C, O) { const m = bagNear(3); if (!m) return false; const a = dirTo(m), P0 = bagPos(); W.sw = -(W.sw || 1); inCircle(P0.x, P0.z, 2.8, q => { if (bagAngD(dirTo(q), a) < 1.25) bagHit(W, q, 1, { kb: 2 }); }); arcFx(P0.x, P0.z, a, 2.8, C, .22, W.sw);
    if (O.storm) { const q = nearest(m.x, m.z, 4, new Set([m])); if (q) { bagFx(() => boltFx(new V3(m.x, .7, m.z), new V3(q.x, .7, q.z), 0xd8f0ff, .07)); bagHit(W, q, .5, {}); } } sfx('slash', .4, 1.3); return a; },
  thrust(W, C) { const m = bagNear(3.2); if (!m) return false; const a = dirTo(m); bagHit(W, m, 1, { kb: 1.2 }); bagLine(bagPos().x, bagPos().z, a, 3.5, C, .06); spark(m.x, .7, m.z, { n: 4, color: C, spd: 3, size: .22, life: .25 }); sfx('slash', .3, 1.9); return a; },
  pierce(W, C) { const m = bagNear(7.5); if (!m) return false; const a = dirTo(m); shootP('lance', a, { bag: W, mul: 1, spd: 21, life: .36, r: .6, kb: 2.5, pierce: 8, c: C, y: .7 }); sfx('whoosh', .5, 1.5); return a; },
  toss(W, C, O) { const m = bagNear(8); if (!m) return false; const a = dirTo(m); shootP('toss', a, { bag: W, mul: 1, spd: O.fast ? 18 : 11.5, life: O.fast ? .5 : .75, r: O.fast ? .5 : .75, kb: 2, pierce: O.fast ? 4 : 3, c: C, y: .8, ic: W.ic, spin: O.fast ? 0 : 14, sz: 1 }); sfx('whoosh', .5, 1.2); return a; },
  slam(W, C, O) { const m = bagNear(5.6); if (!m) return false; const x = m.x, z = m.z; bagDrop(W, x, z, .2);
    after(.2, () => { bagBoom(W, x, z, 2.1, 1, { c: C, pf: 'impacts/ground-slam', pfs: 2.3 }); shake(.25); sfx('boom', .5, 1);
      if (O.bolt) { pfx('lightning/lightning-strike', x, z, 2.8, { speed: 2 }); const seen = new Set(); let from = new V3(x, .8, z), q = nearest(x, z, 4.5, seen); for (let c = 0; c < 3 && q; c++) { seen.add(q); const to = new V3(q.x, .6, q.z), f0 = from; bagFx(() => boltFx(f0, to, 0xd8d0ff, .08)); bagHit(W, q, .5, {}); from = to; q = nearest(to.x, to.z, 3.6, seen); } } }); return dirTo(m); },
  bonk(W, C) { const m = bagNear(2.8); if (!m) return false; bagBoom(W, m.x, m.z, 1.25, 1, { c: C }); sfx('boom', .3, 1.5); return dirTo(m); },
  claws(W, C) { const m = bagNear(2.5); if (!m) return false; const a = dirTo(m), P0 = bagPos(); inCircle(P0.x, P0.z, 2.4, q => { if (bagAngD(dirTo(q), a) < 1) bagHit(W, q, 1, { kb: 1 }); }); for (const s of [-.35, 0, .35]) arcFx(P0.x, P0.z, a + s, 2.2, C, .14, 1); sfx('slash', .3, 1.6); return a; },
  reap(W, C) { if (!bagNear(3.5)) return false; const P0 = bagPos(); inCircle(P0.x, P0.z, 3.1, q => bagHit(W, q, 1, { kb: 2.5 })); for (let i = 0; i < 3; i++) arcFx(P0.x, P0.z, HERO.face + i * 2.09, 3.1, C, .3, 1); pfx('shadow/shadow-tendrils', P0.x, P0.z, 3.2, { speed: 1.8, opacity: .8 }); sfx('slash', .6, .8); return HERO.face; },
  star(W, C) { const m = bagNear(8); if (!m) return false; const a = dirTo(m) + rnd(-.06, .06); shootP('toss', a, { bag: W, mul: 1, spd: 19, life: .5, r: .32, pierce: 1, kb: .5, c: C, y: .8, ic: W.ic, spin: 24, sz: .6 }); return a; },
  disc(W, C) { const m = bagNear(8); if (!m) return false; const a = dirTo(m), p = shootP('blade', a, { bag: W, mul: 1, spd: 18, life: 2.2, r: .75, kb: 1.5, back: false, y: .55, c: C });
    if (!NORENDER) { p.mesh = (DEC_POOL.chak || []).pop() || decalMesh('chak'); decalSet(p.mesh, C, 0xffffff, { ord: 4 }); p.mesh.scale.set(2.2, 1, 2.2); scene.add(p.mesh); } sfx('whoosh', .5, 1.7); return a; },
  arrows(W, C, O) { const n = O.n || 1, P0 = bagPos(), T = nearestN(P0.x, P0.z, 9.5, n); if (!T.length) return false; for (let i = 0; i < n; i++) { const m = T[i % T.length]; shootP('arrow', dirTo(m) + (i >= T.length ? (i - (n - 1) / 2) * .22 : 0), { bag: W, mul: 1, pierce: 2 + (W.pierce ? 2 : 0), spd: 17, life: .75, r: .36, kb: 1, c: C }); } sfx('twang', .6, rnd(.95, 1.1)); return dirTo(T[0]); },
  fireball(W, C, O) { const n = O.n || 1, P0 = bagPos(), T = nearestN(P0.x, P0.z, 9, n); if (!T.length) return false; for (let i = 0; i < n; i++) { const m = T[i % T.length], d = Math.hypot(m.x - P0.x, m.z - P0.z); shootP('fire', dirTo(m) + (i >= T.length ? rnd(-.5, .5) : 0), { bag: W, mul: 1, spd: 10, life: Math.max(.15, d / 10), r: 1.45, c: C }); } sfx('whoosh', .5, 1.5); return dirTo(T[0]); },
  icicle(W, C) { const m = bagNear(7.5); if (!m) return false; const x = m.x, z = m.z, P0 = bagPos(); bagFx(() => boltFx(new V3(P0.x, 1, P0.z), new V3(x, .5, z), C, .07)); after(.1, () => { bagBoom(W, x, z, 1.7, 1, { c: C, kb: .5 }); pfx('ice/frost-nova', x, z, 3, { speed: 1.8 }); sfx('ice', .5); }); return dirTo(m); },
  chain(W, C) { const P0 = bagPos(); let m = randomMon(P0.x, P0.z, 8); if (!m) return false; const a = dirTo(m), seen = new Set(); let from = new V3(P0.x, 1.2, P0.z);
    for (let c = 0; c < 4 && m; c++) { seen.add(m); const to = new V3(m.x, .6 + m.y, m.z), f0 = from; bagFx(() => boltFx(f0, to, C, c ? .07 : .1)); bagHit(W, m, c ? .75 : 1, {}); spark(m.x, .6, m.z, { n: 2, color: 0xcfe0ff, spd: 2, size: .2, life: .2 }); from = to; m = nearest(to.x, to.z, 3.8, seen); } sfx('zap', .6, rnd(.9, 1.2)); return a; },
  flask(W, C) { const P0 = bagPos(), m = randomMon(P0.x, P0.z, 7.5); if (!m) return false; ZONES.push({ type: 'poison', x: m.x, z: m.z, r: 1.5, t: 0, dur: 3.5, tk: 0, bag: W, c: C });
    decal('pool', m.x, m.z, 3.4, 0x58c020, 0xd8ff70, { life: 3.5, y: .07, ord: 2, upd: (q, k, f, U) => { U.uF.value = Math.min(1, f.t / .35); U.uO.value = Math.min(1, (f.life - f.t) * 2.5); } }); pfx('nature/poison-cloud', m.x, m.z, 1.8, { opacity: .9, speed: 1.5 }); return dirTo(m); },
  curse(W, C) { const P0 = bagPos(), m = randomMon(P0.x, P0.z, 7.5); if (!m) return false; ZONES.push({ type: 'poison', x: m.x, z: m.z, r: 2, t: 0, dur: 3.5, tk: 0, bag: W, c: C, curse: 1 }); decal('sigil', m.x, m.z, 4.2, C, 0xf0d0ff, { life: 3.5, y: .085, ord: 2 }); pfx('shadow/shadow-tendrils', m.x, m.z, 2.6, { speed: 1.5, opacity: .85 }); return dirTo(m); },
  skyray(W, C, O) { const m = bagTop(9); if (!m) return false; const x = m.x, z = m.z, r = O.big ? 1.8 : 1.25; after(.1, () => { column({ x, z }, C, .5, r * .5, 6); disc({ x, z }, C, r, .4, .55, TEX.rune); pfx('holy/holy-smite', x, z, O.big ? 3.2 : 2.4, { speed: 1.8 }); bagBoom(W, x, z, r, 1, { c: C, main: m, kb: .5 }); sfx('lvl', .2, 2); }); return dirTo(m); },
  implode(W, C) { const m = bagNear(7.5); if (!m) return false; const x = m.x, z = m.z; pfx('shadow/void-implosion', x, z, 3.6, { speed: 1.6 }); inCircle(x, z, 3.4, q => { if (!q.boss) { q.kx += (x - q.x) * 4; q.kz += (z - q.z) * 4; } }); after(.3, () => { bagBoom(W, x, z, 2.4, 1, { c: C, kb: 1 }); shake(.15); sfx('boom', .4, .7); }); return dirTo(m); },
  lich(W, C) { if (!bagNear(11)) return false; for (let i = 0; i < 3; i++) shootP('spirit', HERO.face + (i - 1) * 1.2, { bag: W, mul: .5, spd: 8, life: 3, r: .4, y: 1, c: i % 2 ? 0xaa6eff : C, boomR: 1.3 }); return HERO.face; },
  bombtoss(W, C) { const m = bagDense(8, 3); if (!m) return false; ZONES.push({ type: 'meteor', x: m.x, z: m.z, r: 3, t: 0, dur: .5, bag: W, mul: 1 }); decal('target', m.x, m.z, 6.3, C, 0xfff0c0, { life: .5, y: .08, ord: 2, full: 1, dir: .7 }); return true; },
  meteor(W, C, O) { const r = O.big ? 4.6 : 3.4, m = bagDense(9, r); if (!m) return false; ZONES.push({ type: 'meteor', x: m.x, z: m.z, r, t: 0, dur: .85, bag: W, mul: 1, pil: 1, big: !!O.big }); decal('target', m.x, m.z, r * 2.1, C, 0xfff0c0, { life: .85, y: .08, ord: 2, full: 1, dir: clamp(2.2 / r, .35, 1.2) }); return true; },
  wisps(W, C, O) { if (!bagNear(12)) return false; const n = O.n || 3; for (let i = 0; i < n; i++) shootP('spirit', Math.random() * TAU, { bag: W, mul: 1.5 / n, spd: 8, life: 3.5, r: .45, y: 1, c: C, boomR: 1.2 }); return true; },
  cut(W, C) { const m = bagNear(2.8); if (!m) return false; const a = dirTo(m), P0 = bagPos(); inCircle(P0.x, P0.z, 2.6, q => { if (bagAngD(dirTo(q), a) < 1.1) bagHit(W, q, 1, { kb: 2 }); }); arcFx(P0.x, P0.z, a, 2.6, C, .22, 1); sfx('slash', .4, 1.1); return a; },   /* an item this page does not know */
};
function bagFire(W) { const M = BAGMOVE[W.id] || BAGMOVE[W.base] || (W.ty === 'mag' ? ['fireball', 0xbe8cff, { n: 1 }] : ['cut', 0xffe2a0]), f = BAGFIRE[M[0]], r = f(W, M[1], M[2] || {}); W.mv = M[0]; if (r !== false) for (let h = 1; h < (W.hits || 1); h++) after(h * .13, () => { if (!HERO.dead) f(W, M[1], M[2] || {}); }); return r; }
function bagSelf(W) {   /* shields and food work on the champion */
  const H = HERO, P0 = H.pos; if (W.blk) { BAG.blk = Math.min(H.max * .6, BAG.blk + W.blk); ring(P0, 0x8fc8ff, .5, 1.5, .35, .8); spark(P0.x, 1, P0.z, { n: 4, color: 0x8fc8ff, spd: 1.5, up: 1.5, size: .22, life: .3 }); }
  if (W.heal) { const h = Math.min(W.heal, H.max - H.hp); healHero(W.heal); if (h >= 1) num(P0.x, 1.9, P0.z, '+' + Math.round(h), '#9fe870'); spark(P0.x, .5, P0.z, { n: 3 + Math.min(5, W.heal / 3 | 0), color: 0x9fe870, spd: .8, up: 3, grav: 1, size: .22, life: .6 }); if (W.heal >= 8) pfx('holy/holy-heal', P0.x, P0.z, 1.6, { follow: P0 }); }
}
function bagSkill() {   /* the champion's own skill, by class (bag3d/classes.js sk.kind); the old wolf hunter = the arrow fan */
  const K = BAG.sk, kind = K.kind || 'fan', m = bagNear(kind === 'bash' || kind === 'spin' ? 4 : 10); if (!m) return; const a = dirTo(m), P = HERO.pos; bagSwing('skill', a); banner(K.n, '', false, 1.1);
  const W = Object.assign({ id: 'skill', dmg: K.pw, crit: 0, ty: 'phy' }, K.w || {}); pfx('status/power-up-aura', P.x, P.z, 1.8, { follow: P, speed: 1.6 });
  if (kind === 'fan') { for (let i = -2; i <= 2; i++) after(.18 + Math.abs(i) * .05, () => { if (!HERO.dead) shootP('arrow', a + i * .16, { bag: i ? W : Object.assign({}, W, { crit: 1 }), mul: .45, pierce: 4, spd: 19, life: .8, r: .42, kb: 2, c: 0xffe178 }); }); sfx('twang', .8, .8); }
  else if (kind === 'bash') { after(.3, () => { if (HERO.dead) return; bagBoom(Object.assign({}, W, { stun: 1 }), P.x, P.z, 2.8, 1.3, { kb: 4, c: 0xbfe4ff }); BAG.blk += K.pw * .8; sfx('boom', .8, .9); }); }
  else if (kind === 'spin') { for (let i = 0; i < 3; i++) after(.12 + i * .28, () => { if (!HERO.dead) bagBoom(W, P.x, P.z, 2.9, i === 2 ? .8 : .55, { kb: 2.5, c: 0xffb070 }); }); }
  else if (kind === 'meteor') { const t = bagDense(12, 2.5) || m; for (let i = 0; i < 3; i++) after(.35 + i * .25, () => { if (HERO.dead) return; const x = t.x + (Math.random() - .5) * 2.4, z = t.z + (Math.random() - .5) * 2.4; bagBoom(Object.assign({}, W, { burn: 1.5 }), x, z, 2.2, .7, { kb: 2, c: 0xff7a30 }); }); }
  else if (kind === 'venom') { const ms = MON.filter(q => !q.dead && (q.x - P.x) ** 2 + (q.z - P.z) ** 2 < 36).sort((p, q) => ((p.x - P.x) ** 2 + (p.z - P.z) ** 2) - ((q.x - P.x) ** 2 + (q.z - P.z) ** 2)).slice(0, 5);
    ms.forEach((q, i) => after(.15 + i * .1, () => { if (HERO.dead || q.dead) return; bagHit(Object.assign({}, W, { poi: (W.poi || 2) * 1.5 }), q, .7, { fx: P.x, fz: P.z, kb: 1.5 }); bagLine(P.x, P.z, Math.atan2(q.x - P.x, q.z - P.z), Math.hypot(q.x - P.x, q.z - P.z), 0x9cff7a, 2); })); }
}
/* ---- what the engine asks (hooks in horde.html) */
function bagHurt(d, src) {   /* before armour: magic resist for shots, dodge, thorns, the shield */
  const H = HERO, S = BAG.st, P0 = H.pos; if (BAG.t > BAG.dur) d *= 1 + (BAG.t - BAG.dur) * .05; if (!src) d *= 1 - (S.mres || 0); else if (S.dodge && Math.random() < S.dodge) { num(P0.x, 1.8, P0.z, 'หลบ', '#cfe8ff'); H.inv = .25; return 0; }
  if (src && S.thorn && !src.dead) hitMon(src, S.thorn * 2.5, { w: 'thorn', color: '#c8e8a0' });
  if (BAG.blk > 0) { const a = Math.min(BAG.blk, d); BAG.blk -= a; d -= a; if (d < .5) { H.inv = .3; num(P0.x, 1.8, P0.z, 'กัน', '#8fc8ff'); spark(P0.x, 1, P0.z, { n: 4, color: 0x8fc8ff, spd: 2.5, size: .22, life: .25 }); sfx('tick', .3, 1.6); return 0; } }
  if (d >= 1) bagSwing('hurt', null); return d; }
function bagKill(m) {   /* no xp gems in this mode: a few coins (bonus gold for the shop), a rare heart */
  if (m.boss) { G.boss = null; shake(.6); sfx('boom', 1, .6); FLASH.w = .4; for (let i = 0; i < 3; i++) after(i * .22, () => pfx('explosions/big-explosion', m.x + rnd(-1, 1), m.z + rnd(-.6, .6), 4.5)); ring(m, 0xffd060, .5, 7, .8); column(m, 0xffd060, 1, 1, 6); for (let i = 0; i < 5; i++) drop('coin', m.x + rnd(-1.4, 1.4), m.z + rnd(-1.4, 1.4), 1); return; }
  if (m.elite) { pfx('explosions/arcane-burst', m.x, m.z, 3); sfx('boom', .6, 1.2); shake(.25); for (let i = 0; i < 2; i++) drop('coin', m.x + rnd(-.6, .6), m.z + rnd(-.6, .6), 1); return; }
  const r = Math.random(); if (r < BAG.coinP) drop('coin', m.x, m.z, 1); else if (r < BAG.coinP + .012) drop('heart', m.x, m.z, 1); }
function bagWave(round, boss) {   /* how many monsters, how strong, when they come. ALL of them must die */
  const N = Math.min(120, Math.round(16 + round * 5)), dur = 16 + Math.min(16, round * 1.1), plan = [], tier = Math.min(3, Math.floor((round - 1) / 4)), R = rng((G.seed | 0) + round * 131);
  const L = MAP.mobs[tier].filter(k => MOBS[k]).slice(); for (let i = L.length - 1; i > 0; i--) { const j = R() * (i + 1) | 0;[L[i], L[j]] = [L[j], L[i]]; } const kinds = L.slice(0, 3); if (tier > 0) { const O = MAP.mobs[tier - 1].filter(k => MOBS[k]); kinds.push(O[R() * O.length | 0]); }
  BAG.mhp = 4 + round * 1.6 + round * round * .1; BAG.mdmg = 2.2 + round * .42; G.spdMul = 1.2 + Math.min(.4, round * .025); BAG.dur = dur + 12;   /* monsters are faster here than in the survival game: the champion cannot simply outrun them */ BAG.kinds = kinds;
  const n0 = Math.round(N * .34); let left = N - n0; for (let i = 0; i < n0;) { const c = Math.min(n0 - i, 2 + (R() * 3 | 0)), a = R() * TAU; plan.push({ t: .3, n: c, a, d: 7.5 + R() * 4, k: kinds[R() * kinds.length | 0] }); i += c; }
  const sw = round >= 3 ? Math.min(left, Math.min(26, 6 + round)) : 0; left -= sw;
  /* PACKS (owner 2026-11-28 "ให้มอนวิ่งมารุมตามรอบ"): the rest come as packs that RUN IN from one side at a time (a red arrow at the screen edge warns
     .9 s before), a pack every ~3 s, bigger every round (6 -> 14), the side turning round the champion so they swarm from everywhere */
  const pk = Math.min(14, 5 + Math.round(round * .8)), np = Math.max(1, Math.ceil(left / pk)); let a0 = R() * TAU;
  for (let i = 0, j = 0; i < left; j++) { const c = Math.min(left - i, pk), t = 2.5 + (dur - 2.5) * (j / np); a0 += 1.9 + R() * 1.4; plan.push({ t, n: c, a: a0, d: 0, pack: 1, k: kinds[R() * kinds.length | 0] }); if (c >= 4) plan.push({ t: Math.max(.6, t - .9), n: 0, warn: a0 }); i += c; }
  if (sw) plan.push({ t: dur * .55, n: sw, ring: 1, k: kinds[0], o: { hp: .55, spd: .85 } });
  if (!boss && round >= 4) for (let e = 0; e < (round >= 9 ? 2 : 1); e++) plan.push({ t: dur * (.4 + e * .3), n: 1, a: R() * TAU, d: 0, k: kinds[R() * kinds.length | 0], o: { hp: 5 + round * .3, sc: 1.65, dmg: 1.5, elite: true, tint: [1.45, 1.2, .5] }, note: 'มอนหัวหน้าฝูงปรากฏ' });
  plan.sort((p, q) => p.t - q.t); BAG.warn = []; BAG.plan = plan; BAG.pi = 0; BAG.total = plan.reduce((s, p) => s + p.n, 0) + (boss ? 1 : 0); BAG.bossHp = Math.round(110 + round * round * 8 + round * 20); return kinds;
}
function bagFair(k, o) { const K = KIND[k], q = Object.assign({}, o); if (K && K.st) { q.hp = (q.hp || 1) * Math.pow(K.st.hp, -.4); q.dmg = (q.dmg || 1) * Math.pow(K.st.dmg, -.4); } return q; }   /* big kinds are tougher, but less than in the survival game: the round's level already makes them stronger */
function bagSpawn(e) {
  if (e.warn != null) { BAG.warn.push({ a: e.warn, t: 1.3 }); return; }
  if (e.ring) { for (let i = 0; i < e.n; i++) { const [x, z] = ringPos(Math.min(SPAWNR - .5, 11.5), i / e.n * TAU); spawnMon(e.k, x, z, bagFair(e.k, e.o)); } banner('ฝูงใหญ่ล้อมแล้ว!', 'ฝ่าวงล้อมออกไป', true, 1.8); sfx('hurt', .6, .6); return; }
  if (e.pack && e.n >= 4) note('ฝูงมอนวิ่งมารุม! ×' + e.n, '#ff9a7a');
  for (let i = 0; i < e.n; i++) { const [x, z] = ringPos((e.d || SPAWNR + rnd(0, 2)) + rnd(0, e.pack ? 2.4 : 1.2), e.a + rnd(e.pack ? -.38 : -.22, e.pack ? .38 : .22)); const m = spawnMon(e.k, x, z, bagFair(e.k, e.o)); if (m && e.d) spark(x, .3, z, { n: 3, color: 0xd8d0c0, spd: 1.5, up: 2, size: .25, life: .35 }); } if (e.note) note(e.note, '#ffd86a'); }
function bagBoss() { const bi = Math.min(3, Math.floor(BAG.cfg.round / 5) - 1), k = MAP.boss[Math.max(0, bi) % MAP.boss.length]; BAG.bossWait = true;
  loadKind(k).then(() => { const K = KIND[k]; if (!K || !K.ok || !BAG.on) { BAG.bossWait = false; BAG.total--; return; } const [x, z] = ringPos(Math.min(SPAWNR - 1, 11)), m = spawnMon(k, x, z, { boss: true, bi: Math.max(0, bi), spd: .85, dmg: .75 }); BAG.bossWait = false; if (!m) { BAG.total--; return; }
    m.hp = m.max = BAG.bossHp; m.r = Math.max(m.r, .8); G.boss = m; banner('บอสบุก!', MOBS[k].name, true, 2.6); setMusic('drums'); shake(.4); sfx('boom', .9, .6); sfx('roar', 1); G.slow = 1.2; CAM.focus = { m, t: 0, dur: 2 }; }); }
function bagUpd(dt) {   /* instead of the weapons / director / shrines / ultimate of the normal game */
  const S = BAG.st, H = HERO; BAG.t += dt; if (H.atkT <= 0) H.apr = 0; while (BAG.pi < BAG.plan.length && BAG.plan[BAG.pi].t <= BAG.t) bagSpawn(BAG.plan[BAG.pi++]); if (BAG.cfg.boss && !BAG.bossed && BAG.t > 4) { BAG.bossed = true; bagBoss(); }
  BAG.sta = Math.min(S.stam, BAG.sta + S.sreg * dt); const hs = 1 + (S.haste || 0);
  for (const W of BAG.its) { if (W.fl > 0) W.fl -= dt;
    if (W.once) { if (!W.done && BAG.t >= 3.5 && bagFire(W) !== false) { W.done = 1; W.fl = .4; bagPop(W); bagSwing(W.mv, null); } continue; }
    W.t += dt * hs; if (W.t < W.cd) continue; if (W.self) { W.t = 0; W.fl = .25; bagSelf(W); bagSwing(W.blk ? 'block' : 'eat', null); continue; } if (BAG.sta < W.sta) continue;
    const r = bagFire(W); if (r === false) { W.t = W.cd - .12; continue; } W.t = 0; BAG.sta -= W.sta; W.fl = .25; bagPop(W); bagSwing(W.mv, typeof r === 'number' ? r : null); }
  if (BAG.sk) { BAG.sk.g += dt * hs; if (BAG.sk.g >= BAG.sk.cd && bagNear(10)) { BAG.sk.g = 0; bagSkill(); } }
  BAG.tk -= dt; if (BAG.tk <= 0) { BAG.tk = .5; for (const m of MON) if (!m.dead && m.poi > 0) hitMon(m, m.poi * .5, { w: 'poison', color: '#c8f080' }); }
  if (BAG.raged) { BAG.rk = (BAG.rk || 0) - dt; if (BAG.rk <= 0) { BAG.rk = 1; for (const m of MON) if (!m.dead && m.spd < 6) m.spd *= 1.04; } }
  if (BAG.t > BAG.dur && !BAG.raged) { BAG.raged = true; banner('ฝูงมอนคลั่ง!', 'รีบกวาดให้หมด: ยิ่งนานมอนยิ่งตีแรง', true, 2.2); }
  if (!BAG.done && BAG.pi >= BAG.plan.length && !BAG.bossWait && (!BAG.cfg.boss || BAG.bossed) && aliveN() === 0 && G.endT <= 0) { { const M = H.M; chPlay(M, 'U', 'Cheer', true, 1.2); chPlay(M, 'L', 'Cheer', true, 1.2); H.atkT = H.dodgeT = 3; H.apr = 9; } BAG.done = true; G.won = true; G.endT = 1.4; jingle('win'); banner('ชนะ!', 'กวาดฝูงมอนรอบ ' + BAG.cfg.round + ' หมดแล้ว', false, 1.6); for (const g of GEMS) g.pull = true; }
}
function bagAuto(dt) {   /* the champion holds the ground and lets the bag fight: walks to the nearest monster when nothing is in reach, steps out of a boss's body and away from shots, picks up coins when it is quiet, dashes out when badly hurt in a crowd */
  const H = HERO.pos; let fx = 0, fz = 0, nd = 1e9, nm = null, close = 0, cx = 0, cz = 0;
  for (const m of MON) { if (m.dead) continue; const dx = H.x - m.x, dz = H.z - m.z, d2 = dx * dx + dz * dz; if (d2 < nd) { nd = d2; nm = m; } if (d2 < 4) { close++; cx += dx; cz += dz; } if (m.boss) { const R = 3 + m.r; if (d2 < R * R) { const w = 5 / (d2 + .3); fx += dx * w; fz += dz * w; } } }
  for (const b of BUL) { const dx = H.x - b.x, dz = H.z - b.z, d2 = dx * dx + dz * dz; if (d2 < 9) { fx += dx / (d2 + .2) * 2; fz += dz / (d2 + .2) * 2; } }
  if (!close) { let gd = 7, gx = 0, gz = 0; for (const g of GEMS) { const d = Math.hypot(g.x - H.x, g.z - H.z); if (d < gd) { gd = d; gx = g.x - H.x; gz = g.z - H.z; } } if (gd < 7) { fx += gx / (gd || 1) * .8; fz += gz / (gd || 1) * .8; } }
  if (nm && !nm.boss) { const d = Math.sqrt(nd); if (d > BAG.reach) { fx += (nm.x - H.x) / d; fz += (nm.z - H.z) / d; } } else if (nm && nd > 36) { const d = Math.sqrt(nd); fx += (nm.x - H.x) / d; fz += (nm.z - H.z) / d; }
  const R = Math.hypot(H.x, H.z); if (R > ARENA - 6) { fx -= H.x / R * (R - ARENA + 6) * .6; fz -= H.z / R * (R - ARENA + 6) * .6; }
  const L = Math.hypot(fx, fz); if (L < .06) INP.x = INP.z = 0; else { INP.x = fx / L; INP.z = fz / L; }
  if (HERO.dashCd <= 0 && HERO.hp < HERO.max * .5 && close >= 4) { const c = Math.hypot(cx, cz) || 1; INP.x = cx / c; INP.z = cz / c; heroDash(); }
}
function bagInp(dt) { JOY.on = false; if (!HERO.dead && G.endT <= 0 && BAG.t > .7) bagAuto(dt); else INP.x = INP.z = 0; }   /* owner 2026-11-27 "ไม่ต้องบังคับดิ ให้มันออโต้ โดยเราจัดกระเป๋าแบบเดิม": the player never steers, the fight is fully automatic */
/* ---- start / end */
function bagStart(cfg) {
  if (!BAG.ready || !HERO) return false; CAM.zoom = 1.22; resize(); audioInit(); clearRun();   /* closer than the survival game: the champion and the item effects read bigger */ const M = HERO.M; HERO = makeHero(M); showHero(M); BAG.cfg = cfg; BAG.result = null; BAG.on = true; BAG.done = BAG.raged = BAG.bossed = false; BAG.bossWait = false; BAG.t = 0; BAG.tk = .5; BAG.man = 0;
  const S = BAG.st = Object.assign({ armor: 0, mres: 0, dodge: 0, regen: 0, thorn: 0, haste: 0, crit: 0, critd: 2, stam: 5, sreg: 1, rage: 0, sblk: 0 }, cfg.st || {}); BAG.spd = cfg.spd > 1 ? 2 : 1; BAG.icr = cfg.icr || 14;
  Object.assign(P, { pow: 1, cd: 1, area: 1, spd: 3.3, magnet: 2.4, crit: 0, critX: 2, armor: S.armor, regen: S.regen, xp: 0, gold: 1, luck: 1, multi: 0, dur: 1, steal: 0, numMin: 0 }); HERO.max = Math.round(cfg.hp); HERO.hp = HERO.max; BAG.hpShow = HERO.hp; BAG.blk = S.sblk || 0; BAG.sta = S.stam;
  BAG.its = (cfg.items || []).map(q => { const W = Object.assign({ t: Math.random() * .4, fl: 0 }, q); if (W.start != null) { W.once = true; W.dmg = W.start; } else if (W.blk || W.heal) W.self = true; return W; });
  const melee = BAG.its.some(W => !W.once && !W.self && ['stab', 'xcut', 'thrust', 'bonk', 'claws', 'reap', 'cut', 'cleave'].includes((BAGMOVE[W.id] || BAGMOVE[W.base] || ['cut'])[0])); BAG.reach = melee ? 1.8 : 5.5;
  BAG.sk = cfg.sk ? { n: cfg.sk.n, cd: cfg.sk.cd, pw: cfg.sk.pw, g: cfg.sk.cd * .4, kind: cfg.sk.kind, w: cfg.sk.w } : null; BAG.cname = cfg.cname || ''; BAG.anim = Object.assign({}, BAGCLSANIM[cfg.cls] || {});
  if (cfg.cls && typeof BAGCLS !== 'undefined' && BAGCLS[cfg.cls]) BAG.anim.skill = [BAGCLS[cfg.cls].anim.skill.slice(-1), .8, 3];   /* the class's own skill move */ G.seed = (Math.random() * 1e9) | 0; G.hpMul = G.dmgMul = G.rateMul = 1; G.revive = 0; G.pend = 0; G.hk = HERO.k;
  const kinds = bagWave(cfg.round, !!cfg.boss); DIR.cur = kinds; kinds.forEach(loadKind); if (cfg.boss) loadKind(MAP.boss[Math.max(0, Math.min(3, Math.floor(cfg.round / 5) - 1)) % MAP.boss.length]);
  CAM.look.set(0, 0, 0); INP.x = INP.z = 0; JOY.on = false; G.state = 'load'; LOAD.msg = 'กำลังเรียกฝูงมอน...'; LOAD.f = .6;
  Promise.all(kinds.map(loadKind)).then(() => { if (BAG.cfg !== cfg) return; G.state = 'play'; { const M = HERO.M, d = chPlay(M, 'U', 'Spawn_Ground', true, 1.5); chPlay(M, 'L', 'Spawn_Ground', true, 1.5); HERO.atkT = HERO.dodgeT = Math.min(.8, d || 0); HERO.apr = 9; }   /* the champion rises out of the ground */ setMusic(MAP.music === 'calm' ? 'battle' : MAP.music); banner(cfg.boss ? 'รอบ ' + cfg.round + ' · บอส' : 'รอบ ' + cfg.round, cfg.name || '', !!cfg.boss, 1.8); }); return true;
}
function bagFinish() {   /* the wave is cleared or the champion fell: tell bag3d.html */
  const left = aliveN() + BAG.plan.slice(BAG.pi).reduce((s, p) => s + p.n, 0), r = { bag: 'end', win: !!G.won && !HERO.dead, t: +BAG.t.toFixed(1), kills: G.kills, total: BAG.total, left, coins: G.coins, hp: Math.max(0, Math.round(HERO.hp)), dmg: Object.assign({}, STATS) };
  BAG.result = r; BAG.on = false; G.state = 'bagdone'; INP.x = INP.z = 0; JOY.on = false; setMusic('calm'); try { if (parent !== window) parent.postMessage(r, '*'); } catch (_) { } }
function bagBoot() { BAG.ready = true; G.state = 'bagidle'; HERO.M.T.root.scale.multiplyScalar(1.15); if (!NORENDER) bagIcons(); try { if (parent !== window) parent.postMessage({ bag: 'ready', map: MAPK }, '*'); } catch (_) { } if (BAG.wait) { const c = BAG.wait; BAG.wait = null; bagStart(c); } }
function bagIcons() { if (BAG.img) return true; BAG.img = new Image(); BAG.img.src = 'art/bag3d/icons_all.png?v=3'; BAG.tex = TL.load('art/bag3d/icons_all.png?v=3'); BAG.tex.magFilter = THREE.NearestFilter; BAG.tex.encoding = THREE.sRGBEncoding; return true; }
addEventListener('message', e => { const d = e.data; if (!d || !d.bag || !BAGM) return; if (d.bag === 'start') { if (BAG.ready) bagStart(d.cfg); else BAG.wait = d.cfg; } else if (d.bag === 'spd') BAG.spd = d.v > 1 ? 2 : 1; else if (d.bag === 'stop') { BAG.on = false; G.state = 'bagidle'; clearRun(); } });
window.BAGAPI = { BAG, start: c => bagStart(c), fire: bagFire, moves: BAGMOVE };
/* ---- drawing: item icons that fly / drop / pop up over the champion (sprites cut from bag3d's icon sheet) */
function bagIcon(ic) { const t = BAG.tex.clone(); t.needsUpdate = true; t.repeat.set(1 / 8, 1 / BAG.icr); t.offset.set((ic % 8) / 8, 1 - (Math.floor(ic / 8) + 1) / BAG.icr); const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false, fog: false })); s.renderOrder = 6; s.userData.ic = ic; return s; }
function bagSprite(ic) { let s = null; for (const q of BAG.spr) if (!q.visible && q.userData.ic === ic) { s = q; break; } if (!s) { if (BAG.spr.length > 40) return null; s = bagIcon(ic); BAG.spr.push(s); scene.add(s); } s.visible = true; s.material.rotation = 0; s.material.opacity = 1; return s; }
function bagPop(W) { if (NORENDER || W.ic == null || !BAG.tex) return; if (BAG.pops.length > 5) { const o = BAG.pops.shift(); o.s.visible = false; } const s = bagSprite(W.ic); if (s) BAG.pops.push({ s, t: 0, off: (BAG.pops.length % 3 - 1) * .5 }); }
function bagDrop(W, x, z, life) { if (NORENDER || W.ic == null || !BAG.tex) return; const s = bagSprite(W.ic); if (s) BAG.drops.push({ s, x, z, t: 0, life }); }
function bagDraw() {   /* once a frame, from fillBatches */
  if (!BAG.tex) return; const used = new Set(), now = performance.now(), dt = Math.min(.05, (now - (BAG.lt || now)) / 1000); BAG.lt = now;
  for (const p of PROJ) { if (p.type === 'lance') { for (let q = 0; q < 5; q++) glow(p.x - p.vx * q * .012, p.y, p.z - p.vz * q * .012, .7 - q * .1, q ? p.c : 0xffffff, 1 - q * .17); continue; } if (p.type !== 'toss') continue; if (!p.spr) p.spr = bagSprite(p.ic); if (!p.spr) continue; used.add(p.spr); const z = p.sz || 1; p.spr.position.set(p.x, p.y, p.z); p.spr.scale.set(z, z, 1); p.spr.material.rotation = p.spin ? -p.t * p.spin : p.a - Math.PI * .75; glow(p.x, p.y, p.z, z * 1.1, p.c, .45); }
  for (let i = BAG.pops.length - 1; i >= 0; i--) { const o = BAG.pops[i]; o.t += dt; if (o.t > .42 || !BAG.on) { o.s.visible = false; BAG.pops.splice(i, 1); continue; } used.add(o.s); const k = o.t / .42, pop = k < .25 ? k / .25 * 1.2 : 1.2 - (k - .25) * .27; o.s.position.set(HERO.pos.x + o.off, 1.95 + k * .45, HERO.pos.z); o.s.scale.set(.6 * pop, .6 * pop, 1); o.s.material.opacity = k > .7 ? (1 - k) / .3 : 1; }
  for (let i = BAG.drops.length - 1; i >= 0; i--) { const o = BAG.drops[i]; o.t += dt; if (o.t > o.life + .1) { o.s.visible = false; BAG.drops.splice(i, 1); continue; } used.add(o.s); const k = Math.min(1, o.t / o.life); o.s.position.set(o.x, .6 + (1 - k * k) * 5, o.z); o.s.scale.set(1.5, 1.5, 1); o.s.material.rotation = -2.4 + k * 2.4; }
  for (const s of BAG.spr) if (s.visible && !used.has(s)) s.visible = false;
}
/* ---- the screen: life + shield + stamina, the wave, the items with their cooldowns, the speed button */
function bagDrawUI(dt) {
  if (G.state === 'pause') G.state = 'play'; const H = HERO, pad = 10 * S;
  if (BAG.on && BAG.warn && BAG.warn.length && HERO && G.state === 'play') {   /* where the next pack runs in from: red chevrons at the screen edge */
    const [hx, hy] = toScreen(HERO.pos.x, .5, HERO.pos.z);
    for (const w of BAG.warn) { w.t -= dt; if (w.t <= 0) continue; const [px, py] = toScreen(HERO.pos.x + Math.cos(w.a) * 8, .5, HERO.pos.z + Math.sin(w.a) * 8), an = Math.atan2(py - hy, px - hx), m = 34 * S;
      const k = Math.min((SW / 2 - m) / Math.max(1e-3, Math.abs(Math.cos(an))), (SH / 2 - m) / Math.max(1e-3, Math.abs(Math.sin(an)))), ex = SW / 2 + Math.cos(an) * k, ey = SH / 2 + Math.sin(an) * k, pul = .55 + .45 * Math.sin(NOW * 14);
      ui.save(); ui.translate(ex, ey); ui.rotate(an); ui.globalAlpha = Math.min(1, w.t * 2.5) * pul; ui.fillStyle = '#ff3a2a'; ui.strokeStyle = 'rgba(60,0,0,.9)'; ui.lineWidth = 2.5 * S;
      for (const o of [-12, 0]) { ui.beginPath(); ui.moveTo((o + 12) * S, 0); ui.lineTo((o - 4) * S, -12 * S); ui.lineTo((o - 4) * S, 12 * S); ui.closePath(); ui.fill(); ui.stroke(); } ui.restore(); }
    BAG.warn = BAG.warn.filter(w => w.t > 0); }
  if (!BAG.on && G.state !== 'bagdone') { ui.fillStyle = '#141a2a'; ui.fillRect(0, 0, SW, SH); txt(BAG.ready ? 'พร้อมสู้' : LOAD.msg, SW / 2, SH / 2, 16 * S, '#cfd8f0', 'center', 600); return; }
  if (G.state === 'load') { ui.fillStyle = '#141a2a'; ui.fillRect(0, 0, SW, SH); txt('รอบ ' + BAG.cfg.round, SW / 2, SH * .42, 38 * S, '#ffe08a'); txt(LOAD.msg, SW / 2, SH * .56, 15 * S, '#cfd8f0', 'center', 600); return; }
  { const g0 = ui.createRadialGradient(SW / 2, SH / 2, SH * .5, SW / 2, SH / 2, Math.hypot(SW, SH) * .56); g0.addColorStop(0, 'rgba(4,6,16,0)'); g0.addColorStop(1, 'rgba(4,6,16,.4)'); ui.fillStyle = g0; ui.fillRect(0, 0, SW, SH); }
  for (let i = NUMS.length - 1; i >= 0; i--) { const n = NUMS[i], life = n.big ? .85 : .62; n.t += dt; if (n.t > life) { NUMS.splice(i, 1); continue; } const k = n.t / life, e = 1 - (1 - k) * (1 - k), [x, y, ok] = toScreen(n.x + n.dx * e, n.y + e * (n.big ? 1.15 : .8), n.z); if (!ok) continue;
    ui.globalAlpha = Math.min(1, (life - n.t) * 9); txt(n.text, x, y, (n.big ? 19 : 12.5) * S * (1 + Math.max(0, (n.big ? .16 : .09) - n.t) * (n.big ? 5 : 4)), n.color, 'center', 800, n.big ? 'rgba(60,16,0,.95)' : 'rgba(10,12,24,.92)', (n.big ? 4.5 : 3.2) * S); ui.globalAlpha = 1; }
  for (const m of MON) if (m.elite && !m.dead) { const [x, y, ok] = toScreen(m.x, m.K.hgt * m.sc / m.K.bsc + .25, m.z); if (ok) bar(x - 22 * S, y, 44 * S, 6 * S, m.hp / m.max, '#ffd86a', '#d88a1a'); }
  if (FLASH.r > 0) { const g = ui.createRadialGradient(SW / 2, SH / 2, SH * .35, SW / 2, SH / 2, SH * .95); g.addColorStop(0, 'rgba(255,0,0,0)'); g.addColorStop(1, `rgba(255,20,10,${FLASH.r})`); ui.fillStyle = g; ui.fillRect(0, 0, SW, SH); FLASH.r = Math.max(0, FLASH.r - dt * 1.6); }
  if (FLASH.w > 0) { ui.fillStyle = `rgba(255,250,230,${FLASH.w})`; ui.fillRect(0, 0, SW, SH); FLASH.w = Math.max(0, FLASH.w - dt * 1.5); }
  /* the champion's plate */
  { const w = Math.min(230 * S, SW * .36), x = pad, y = pad, hp = H.hp / H.max; BAG.hpShow += (H.hp - BAG.hpShow) * Math.min(1, dt * 8); rr(x, y, w, 46 * S, 10 * S); ui.fillStyle = 'rgba(10,14,30,.74)'; ui.fill(); ui.lineWidth = 1.5 * S; ui.strokeStyle = 'rgba(255,233,168,.65)'; ui.stroke();
    bar(x + 8 * S, y + 8 * S, w - 16 * S, 15 * S, BAG.hpShow / H.max, hp < .3 ? '#ff7a5a' : '#ff6a7a', hp < .3 ? '#b81a1a' : '#c8283c'); if (BAG.blk > 0) { ui.save(); ui.globalAlpha = .85; bar(x + 8 * S, y + 8 * S, (w - 16 * S) * Math.min(1, BAG.blk / H.max), 5 * S, 1, '#bfe4ff', '#5aa8f0', 'rgba(0,0,0,0)'); ui.restore(); }
    txt(Math.ceil(H.hp) + ' / ' + H.max + (BAG.blk >= 1 ? '   โล่ ' + Math.round(BAG.blk) : ''), x + w / 2, y + 16 * S, 10.5 * S, '#fff', 'center', 800, 'rgba(60,0,0,.8)', 2.5);
    bar(x + 8 * S, y + 27 * S, (w - 16 * S) * .62, 5 * S, BAG.sta / BAG.st.stam, '#ffe27a', '#e0a020'); txt(BAG.cname || 'นักล่าหมาป่า', x + w - 8 * S, y + 36 * S, 10 * S, '#ffe9a8', 'right', 600, 'rgba(0,0,0,.7)', 2);
    if (BAG.sk) { const k = Math.min(1, BAG.sk.g / BAG.sk.cd); bar(x + 8 * S, y + 35 * S, (w - 16 * S) * .62, 5 * S, k, k >= 1 ? '#ffffff' : '#ffb020', '#e07a10'); } }
  /* the wave */
  { const left = Math.max(0, BAG.total - G.kills), tw0 = 190 * S, x = SW / 2 - tw0 / 2, y = pad; rr(x, y, tw0, 40 * S, 10 * S); ui.fillStyle = 'rgba(10,14,30,.75)'; ui.fill(); ui.lineWidth = 1.5 * S; ui.strokeStyle = BAG.cfg.boss ? 'rgba(255,150,130,.8)' : 'rgba(255,233,168,.7)'; ui.stroke();
    txt((BAG.cfg.boss ? 'บอส · รอบ ' : 'รอบ ') + BAG.cfg.round + '   เหลือมอน ' + left, SW / 2, y + 14 * S, 13.5 * S, BAG.raged ? '#ff9a8a' : '#fff6dc'); bar(x + 10 * S, y + 26 * S, tw0 - 20 * S, 7 * S, clamp(G.kills / Math.max(1, BAG.total), 0, 1), '#9ae87a', '#3aa83a');
    if (G.boss && !G.boss.dead) { const bw = Math.min(360 * S, SW * .46), by = y + 62 * S; txt(MOBS[G.boss.k].name, SW / 2, by - 9 * S, 13 * S, '#ffb0a0'); bar(SW / 2 - bw / 2, by, bw, 12 * S, G.boss.hp / G.boss.max, '#ff7a5a', '#b81a2a'); } }
  /* coins, AUTO, speed */
  { const rx = SW - pad, y = pad, bh = 30 * S; button('bagspd', rx - 54 * S, y, 54 * S, bh, 'x' + BAG.spd, { c: BLUE, tc: '#fff', ts: 'rgba(0,0,40,.6)', size: 14 * S, fn: () => { BAG.spd = BAG.spd > 1 ? 1 : 2; try { parent.postMessage({ bag: 'spd', v: BAG.spd }, '*'); } catch (_) { } } });
    coinIc(rx - 54 * S - 52 * S, y + bh / 2, 8 * S); txt(String(G.coins), rx - 54 * S - 40 * S, y + bh / 2 + 1, 13 * S, '#ffe08a', 'left'); }
  /* the items of the bag: a strip along the bottom, the dark part is the cooldown, a flash when one fires */
  if (BAG.img && BAG.img.width) { const L = BAG.its, n = L.length, z = Math.min(34 * S, (SW * .62) / Math.max(1, n) - 3 * S), w = n * (z + 3 * S), x0 = SW / 2 - w / 2, y = SH - pad - z; ui.imageSmoothingEnabled = false;
    L.forEach((W, i) => { const x = x0 + i * (z + 3 * S), k = W.once ? (W.done ? 0 : 1) : clamp(W.t / W.cd, 0, 1), col = W.self ? (W.heal ? '#3f8a3a' : '#2f5f98') : W.once ? '#8a6a1e' : W.ty === 'mag' ? '#6a3ad8' : '#a8402e'; rr(x, y, z, z, 6 * S); ui.fillStyle = 'rgba(10,12,24,.8)'; ui.fill(); ui.lineWidth = 1.5 * S; ui.strokeStyle = W.fl > 0 ? '#ffffff' : col; ui.stroke();
      if (W.ic != null) ui.drawImage(BAG.img, (W.ic % 8) * 64, Math.floor(W.ic / 8) * 64, 64, 64, x + 2 * S, y + 2 * S, z - 4 * S, z - 4 * S); if (k < 1 || (W.once && W.done)) { ui.fillStyle = 'rgba(6,8,18,.62)'; ui.fillRect(x + 1, y + 1, z - 2, (z - 2) * (W.once ? 1 : 1 - k)); } else if (!W.self && !W.once && BAG.sta < W.sta) { ui.fillStyle = 'rgba(160,30,20,.4)'; ui.fillRect(x + 1, y + 1, z - 2, z - 2); }
      if (W.fl > 0) { ui.globalAlpha = W.fl / .25 * .6; ui.fillStyle = '#fff'; ui.fillRect(x, y, z, z); ui.globalAlpha = 1; } }); ui.imageSmoothingEnabled = true; }
  NOTES.forEach((n, i) => { n.t += dt; const a = clamp(Math.min(n.t * 5, (3 - n.t) * 2), 0, 1), ny = pad + 64 * S + i * 21 * S; ui.globalAlpha = a; txt(n.s, pad + 4 * S, ny, 11 * S, n.color, 'left', 600, 'rgba(0,0,0,.7)', 2.5); ui.globalAlpha = 1; }); while (NOTES.length && NOTES[0].t > 3) NOTES.shift();
  if (BANNER.t > 0) { BANNER.t -= dt; const k = clamp(Math.min((BANNER.max - BANNER.t) * 4, BANNER.t * 2.5), 0, 1), y = SH * .34; ui.globalAlpha = k; const g = ui.createLinearGradient(0, 0, SW, 0), c = BANNER.red ? '120,10,10' : '20,30,70'; g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(.5, `rgba(${c},.82)`); g.addColorStop(1, `rgba(${c},0)`); ui.fillStyle = g; ui.fillRect(0, y - 34 * S, SW, 68 * S);
    txt(BANNER.a, SW / 2, y - (BANNER.b ? 8 : 0) * S, 28 * S * (1 + (1 - k) * .3), BANNER.red ? '#ffd0c0' : '#ffe9a8'); if (BANNER.b) txt(BANNER.b, SW / 2, y + 19 * S, 15 * S, '#fff', 'center', 600); ui.globalAlpha = 1; }
  if (BAG.t < 5 && G.state === 'play') { ui.globalAlpha = clamp(5 - BAG.t, 0, 1); txt('สู้อัตโนมัติ: แชมเปี้ยนเดินและใช้ของในกระเป๋าเองทั้งหมด', SW / 2, SH * .8, 12.5 * S, '#fff6dc', 'center', 600); ui.globalAlpha = 1; }
  if (H.dead || G.state === 'bagdone') { ui.fillStyle = 'rgba(6,8,18,.45)'; ui.fillRect(0, 0, SW, SH); txt(G.won && !H.dead ? 'ชนะ!' : 'แพ้...', SW / 2, SH * .45, 40 * S, G.won && !H.dead ? '#ffe08a' : '#ff9a8a'); }
}
