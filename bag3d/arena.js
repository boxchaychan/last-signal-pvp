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
  knight: { arrows: [['Q_OverhandThrow'], .5, 1], cut: [['Melee_2H_Attack_Slice', 'Melee_2H_Attack_Chop'], .5, 1], wave: [['Melee_2H_Attack_Slice', 'Melee_2H_Attack_Chop'], .52, 1], xcut: [['Melee_2H_Attack_Slice'], .48, 1], bonk: [['Melee_2H_Attack_Chop'], .5, 1], slam: [['Melee_2H_Attack_Chop'], .7, 2], cleave: [['Melee_2H_Attack_Chop'], .7, 2], block: [['Melee_Block_Attack'], .5, 0], skill: [['Melee_2H_Attack_Spin'], .8, 3] },   /* the demon knight swings his greatsword two-handed */
  rogue: { cut: [['Melee_1H_Attack_Stab', 'Melee_1H_Attack_Slice_Diagonal'], .34, 1], wave: [['Melee_1H_Attack_Slice_Diagonal', 'Melee_1H_Attack_Stab'], .36, 1], arrows: [['Q_OverhandThrow'], .4, 1] },
  ranger: {},
};
/* the duel rivals' Tripo bodies (horde.html HEROES): the demon and the black-horned knight swing two-handed like the knight class, the winged knight keeps sword and shield, the hooded mage casts */
BAGCLSANIM.demon = Object.assign({}, BAGCLSANIM.knight); BAGCLSANIM.dark = Object.assign({}, BAGCLSANIM.knight, { skill: [['Melee_2H_Attack_Slice'], .8, 3] });
BAGCLSANIM.wing = { arrows: [['Q_OverhandThrow'], .5, 1], block: [['Melee_Block_Attack'], .5, 0], skill: [['Melee_Block_Attack'], .8, 3] };
BAGCLSANIM.hood = Object.assign({}, BAGCLSANIM.mage, { skill: [['Ranged_Magic_Summon'], .9, 3] }); BAGCLSANIM.archer = {};
function bagSwing(mv, ang) { const H = HERO, M = H.M, A = (BAG.anim && BAG.anim[mv]) || BAGANIM[mv] || BAGANIM.cut; if (H.dead || BAG.done) return; if (H.atkT > 0 && A[2] <= (H.apr || 0)) return; const an = A[0][(H.combo = (H.combo | 0) + 1) % A[0].length], act = M.acts[an + '_up']; if (!act) return;
  const ts = act.getClip().duration / A[1]; chPlay(M, 'U', an, true, ts); H.atkT = A[1] * .88; H.apr = A[2]; if (ang != null && !H.moving) H.aim = ang; if (A[2] >= 2 && !H.moving) { chPlay(M, 'L', an, true, ts); H.dodgeT = A[1] * .88; } }
const bagPos = () => HERO.pos, bagNear = R => nearest(HERO.pos.x, HERO.pos.z, R), bagFx = f => { if (!NORENDER) f(); };
const bagAngD = (a, b) => Math.abs(((a - b + Math.PI) % TAU + TAU) % TAU - Math.PI);
function bagLine(x, z, a, L, c, w) { bagFx(() => boltFx(new V3(x, .7, z), new V3(x + Math.sin(a) * L, .7, z + Math.cos(a) * L), c, w)); }
/* one hit of item W on monster m: the item's own crit, execute, poison / burn / slow / stun, life steal. mul = share of its damage */
function bagHit(W, m, mul, o) {
  if (m.dead) return 0; const S = BAG.st; let d = W.dmg * (mul || 1); const crit = d > 0 && (W.sure || Math.random() < (W.crit || 0) + (S.crit || 0)); if (crit) d *= S.critd || 2; if (m.brit > BAG.t) d *= 1.2; { const G = S.gx || {}; if (d > 0) { d += (BAG.skull | 0) + (G.mhit || 0); if (G.mpierce && W.ty === 'mag' && (m.elite || m.boss) && !m.champ) d *= 1.15; } }
  const X = W.x; if (X && d > 0) { if (X.ramp) { if (W.rT !== m) { W.rT = m; W.rN = 0; } W.rN = Math.min(X.ramp[1], (W.rN | 0) + 1); d *= 1 + X.ramp[0] * (W.rN - 1); } }
  if (W.exe && m.hp < m.max * .3) d *= 1 + W.exe; if (S.rage) d *= 1 + S.rage * Math.max(0, 1 - HERO.hp / HERO.max); if (W.pierce && (m.elite || m.boss) && !m.champ) d *= 1 + W.pierce * .5;
  const q = Object.assign({ w: W.id, crit, color: W.ty === 'mag' ? '#e0c4ff' : undefined, ty: W.ty, pc: W.pierce || 0 }, o); if (q.kb) q.kb *= .45;   /* small pushes: the horde must be able to reach the champion */ if (W.burn) q.burn = W.burn * .3; if (W.frz) { q.slow = Math.min(.6, W.frz * 1.2); q.slowT = 2; } if (W.stun) q.frz = W.stun; if (X && X.bash && Math.random() < X.bash[0]) { q.frz = Math.max(q.frz || 0, X.bash[1]); num(m.x, 1.5, m.z, 'มึน!', '#ffe08a'); } if (X && X.jolt && Math.random() < X.jolt[0]) q.frz = Math.max(q.frz || 0, X.jolt[1]);
  if (X && X.chain && !(o && o.chained) && Math.random() < X.chain[0]) { const seen = new Set([m]); let from = m, nx = nearest(m.x, m.z, 4, seen); mfx('bolt', m.x, m.z, 2); for (let c = 0; c < X.chain[1] && nx; c++) { seen.add(nx); const a = from, b = nx; bagFx(() => boltFx(new V3(a.x, .8, a.z), new V3(b.x, .8, b.z), 0xbfd0ff, .09)); hitMon(b, d * X.chain[2], { w: W.id, color: '#cfe0ff' }); from = nx; nx = nearest(b.x, b.z, 4, seen); } sfx('zap', .6, 1.1); }   /* lightning bow */
  if (crit && d > 0 && !(BAG.critT > BAG.t)) { BAG.critT = BAG.t + .45; mfx('crit', m.x, m.z, 1.7 + Math.min(1, d / Math.max(10, m.max)) * .8); }   /* not every crit: the screen would fill */
  const dealt = hitMon(m, d, q); if (!m.dead && m.mark > BAG.t && m.hp < m.max * (m.boss ? .06 : .15)) { mfx('curse', m.x, m.z, 1.8); hitMon(m, m.hp + 1, { w: 'mark', color: '#ff8a8a' }); } if (W.el && W.id !== 'skill') bagEl(W, m); if (S.gx && S.gx.soul && W.ty === 'mag' && dealt) healHero(Math.min(dealt * S.gx.soul * .35, HERO.max * .02)); if (W.poi && !m.dead) m.poi = Math.min((m.poi || 0) + W.poi * .5, W.poi * 4); if (W.ls && dealt) healHero(Math.min(dealt * W.ls * .35, HERO.max * .03)); return dealt;
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
  arrows(W, C, O) { const n = O.n || 1, P0 = bagPos(), T = nearestN(P0.x, P0.z, 9.5, n); if (!T.length) return false; for (let i = 0; i < n; i++) { const m = T[i % T.length]; shootP('arrow', dirTo(m) + (i >= T.length ? (i - (n - 1) / 2) * .22 : 0), { bag: W, mul: i && O.xm ? O.xm : 1, pierce: 2 + (W.pierce ? 2 : 0) + (BAG.st.gx && BAG.st.gx.apierce ? 4 : 0), spd: 17, life: .75, r: .36, kb: 1, c: C }); } sfx('twang', .6, rnd(.95, 1.1)); return dirTo(T[0]); },
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
function bagFire(W) { const M = (W.mv && BAGFIRE[W.mv] && [W.mv, W.ty === 'mag' ? 0xc8a8ff : 0xffe2a0]) || BAGMOVE[W.id] || BAGMOVE[W.base] || (W.ty === 'mag' ? ['fireball', 0xbe8cff, { n: 1 }] : ['cut', 0xffe2a0]), f = BAGFIRE[M[0]]; let O = M[2] || {};
  if (W.x && (W.x.multi || W.x.xarr) && M[0] === 'arrows') O = Object.assign({}, O, { n: (W.x.multi || O.n || 1) + (W.x.xarr || 0), xm: .4 });   /* more arrows: the extras at 40 % */
  if (W.x) bagFireX(W); const r = f(W, M[1], O); W.sure = 0; { const G = BAG.st.gx || {}; if (r !== false && G.multicast && W.ty === 'mag' && !W.once && Math.random() < G.multicast) after(.16, () => { if (!HERO.dead) { f(W, M[1], O); num(HERO.pos.x, 2.1, HERO.pos.z, 'ร่ายซ้ำ!', '#d8b8ff'); } }); } W.mv = M[0]; if (r !== false) for (let h = 1; h < (W.hits || 1); h++) after(h * .13, () => { if (!HERO.dead) f(W, M[1], O); }); return r; }
function bagSelf(W) {   /* shields and food work on the champion */
  const H = HERO, P0 = H.pos; if (W.blk) { BAG.blk = Math.min(H.max * .6, BAG.blk + W.blk); ring(P0, 0x8fc8ff, .5, 1.5, .35, .8); spark(P0.x, 1, P0.z, { n: 4, color: 0x8fc8ff, spd: 1.5, up: 1.5, size: .22, life: .3 }); }
  if (W.heal) { const h = Math.min(W.heal, H.max - H.hp); healHero(W.heal); if (h >= 1) num(P0.x, 1.9, P0.z, '+' + Math.round(h), '#9fe870'); spark(P0.x, .5, P0.z, { n: 3 + Math.min(5, W.heal / 3 | 0), color: 0x9fe870, spd: .8, up: 3, grav: 1, size: .22, life: .6 }); if (W.heal >= 8) pfx('holy/holy-heal', P0.x, P0.z, 1.6, { follow: P0 }); }
}
function bagSkill() {   /* the champion's own skill, by class (bag3d/classes.js sk.kind); the old wolf hunter = the arrow fan */
  const K = BAG.sk, kind = K.kind || 'fan', m = bagNear(kind === 'bash' || kind === 'spin' ? 4 : 10); if (!m) return; const a = dirTo(m), P = HERO.pos; bagSwing('skill', a); if (CUR && CUR.k) num(P.x, 2.5, P.z, K.n, '#ffb0a0', true); else banner(K.n, '', false, 1.1);
  const W = Object.assign({ id: 'skill', dmg: K.pw, crit: 0, ty: 'phy' }, K.w || {}); pfx('status/power-up-aura', P.x, P.z, 1.8, { follow: P, speed: 1.6 });
  if (kind === 'fan') mfx('arrowfan', P.x + Math.sin(a) * 1.6, P.z + Math.cos(a) * 1.6, 3.2, { pri: 1 }); else if (kind === 'bash') mfx('shieldbash', P.x, P.z, 3.4, { pri: 1 }); else if (kind === 'spin') mfx('spin', P.x, P.z, 6.4, { pri: 1, speed: 1.3 }); else if (kind === 'venom') mfx('venomslash', P.x, P.z, 3.4, { pri: 1 });
  if (kind === 'fan') { for (let i = -2; i <= 2; i++) after(.18 + Math.abs(i) * .05, () => { if (!HERO.dead) shootP('arrow', a + i * .16, { bag: i ? W : Object.assign({}, W, { crit: 1 }), mul: .45, pierce: 4, spd: 19, life: .8, r: .42, kb: 2, c: 0xffe178 }); }); sfx('twang', .8, .8); }
  else if (kind === 'bash') { after(.3, () => { if (HERO.dead) return; bagBoom(Object.assign({}, W, { stun: 1 }), P.x, P.z, 2.8, 1.3, { kb: 4, c: 0xbfe4ff }); BAG.blk += K.pw * .8; sfx('boom', .8, .9); }); }
  else if (kind === 'spin') { for (let i = 0; i < 3; i++) after(.12 + i * .28, () => { if (!HERO.dead) bagBoom(W, P.x, P.z, 2.9, i === 2 ? .8 : .55, { kb: 2.5, c: 0xffb070 }); }); }
  else if (kind === 'meteor') { const t = bagDense(12, 2.5) || m; for (let i = 0; i < 3; i++) after(.35 + i * .25, () => { if (HERO.dead) return; const x = t.x + (Math.random() - .5) * 2.4, z = t.z + (Math.random() - .5) * 2.4; bagBoom(Object.assign({}, W, { burn: 1.5 }), x, z, 2.2, .7, { kb: 2, c: 0xff7a30 }); mfx('meteor', x, z, 3.6, { pri: 1 }); }); }
  else if (kind === 'wave') { after(.25, () => { if (HERO.dead) return; const p = shootP('wave', a, { bag: Object.assign({}, W, { ls: Math.max(W.ls || 0, .4) }), mul: 1, spd: 11, life: .95, r: 1.5, kb: 2.5, y: .4 }); if (!NORENDER) { p.mesh = (DEC_POOL.swoosh || []).pop() || decalMesh('swoosh'); decalSet(p.mesh, 0xff3a6a, 0xffd0e0, { full: 1, ord: 4 }); p.mesh.scale.set(3.6, 1, 3.6); p.mesh.rotation.y = a - Math.PI / 2; scene.add(p.mesh); } mfx('slash', P.x, P.z, 3); sfx('whoosh', .8, .8); }); }   /* the black-horned knight (a duel rival): a big dark sword wave that drinks life */
  else if (kind === 'venom') { const ms = MON.filter(q => !q.dead && (q.x - P.x) ** 2 + (q.z - P.z) ** 2 < 36).sort((p, q) => ((p.x - P.x) ** 2 + (p.z - P.z) ** 2) - ((q.x - P.x) ** 2 + (q.z - P.z) ** 2)).slice(0, 5);
    ms.forEach((q, i) => after(.15 + i * .1, () => { if (HERO.dead || q.dead) return; bagHit(Object.assign({}, W, { poi: (W.poi || 2) * 1.5 }), q, .7, { fx: P.x, fz: P.z, kb: 1.5 }); bagLine(P.x, P.z, Math.atan2(q.x - P.x, q.z - P.z), Math.hypot(q.x - P.x, q.z - P.z), 0x9cff7a, 2); })); }
}


/* ELEMENTS AND REACTIONS (owner 2026-11-28, the BIG ITEM DESIGN): a weapon with an element (its own, or from a touching element stone: cfg item.el)
   lays one stack of it on every monster it hits; a weapon with two elements alternates. Five stacks of one = its big effect; a DIFFERENT element
   meeting stacks already there = a REACTION with its own name and painted effect. Strength x cfg st.react (the elements tome, INT). Brittle (shatter,
   corrode) = the monster takes +20 % for 4 s; wet (fire + ice) = the next lightning is a heavy shock that jumps to every wet monster near. */
const EL_C = { f: 0xff7a3a, i: 0x7ad0ff, l: 0xffe14a, p: 0x8ae05a }, EL_H = { f: '#ffb07a', i: '#bfe8ff', l: '#fff08a', p: '#c8f08a' };
const EL_R = { fi: ['เปียกโชก!', 'react_wet'], fl: ['โอเวอร์โหลด!', 'react_overload'], il: ['แตกสลาย!', 'react_shatter'], fp: ['แก๊สระเบิด!', 'react_gas'], ip: ['พิษเยือกแข็ง!', 'react_venom'], lp: ['พิษลามทุ่ง!', 'react_venom'] };
function bagEl(W, m) {
  if (m.dead || !W.el) return; const E = m.els || (m.els = {}), R = BAG.st.react || 1, base = Math.max(2, (W.dmg || 3) * .55) * R, t = BAG.t;
  const e = W.el.length > 1 ? W.el[W.elI = ((W.elI | 0) + 1) % W.el.length] : W.el;
  if (e === 'l' && m.wet > t) {   /* wet + lightning = a heavy shock, jumps to the wet ones near */
    m.wet = 0; num(m.x, 1.7, m.z, 'ช็อตหนัก!', '#9fe0ff', true); mfx('react_shock', m.x, m.z, 3, { pri: 1 }); hitMon(m, base * 2.2, { w: 'react', frz: .9, color: '#bfe8ff' });
    inCircle(m.x, m.z, 3.4, q => { if (q !== m && q.wet > t) { q.wet = 0; hitMon(q, base * 1.6, { w: 'react', frz: .6, color: '#bfe8ff' }); bagFx(() => boltFx(new V3(m.x, .8, m.z), new V3(q.x, .8, q.z), 0x9fe0ff, .08)); } }); shake(.18); sfx('zap', .7, .8); return; }
  const other = Object.keys(E).find(k => k !== e && E[k] > 0);
  if (other) { const pr = [e, other].sort().join(''), N = EL_R[pr]; E[other] = 0; E[e] = 0; if (!N) return; num(m.x, 1.7, m.z, N[0], EL_H[e], true); mfx(N[1], m.x, m.z, pr === 'ip' || pr === 'lp' ? 3.4 : 2.8, { pri: 1 });
    if (pr === 'fi') { m.wet = t + 5; hitMon(m, base * .8, { w: 'react', slow: .4, slowT: 2, color: '#bfe8ff' }); }
    else if (pr === 'fl') { inCircle(m.x, m.z, 2.4, q => hitMon(q, base * (q === m ? 1.6 : 1), { w: 'react', kb: 3.5, fx: m.x, fz: m.z, color: '#ffc08a' })); shake(.2); sfx('boom', .6, 1.1); }
    else if (pr === 'il') { m.brit = t + 4; hitMon(m, base * 2.4, { w: 'react', color: '#e0f4ff' }); shake(.15); sfx('ice', .6, .8); }
    else if (pr === 'fp') { inCircle(m.x, m.z, 2.6, q => { hitMon(q, base * 1.1, { w: 'react', burn: base * .25, kb: 1.5, fx: m.x, fz: m.z, color: '#d8f08a' }); if (!q.dead) q.poi = (q.poi || 0) + base * .3; }); sfx('boom', .5, 1.3); }
    else if (pr === 'ip') { m.poi = (m.poi || 0) + base * .6; hitMon(m, base * .8, { w: 'react', slow: .6, slowT: 4, color: '#c8f0ff' }); }
    else if (pr === 'lp') { const p = (m.poi || 0) + base * .5; inCircle(m.x, m.z, 3.2, q => { q.poi = Math.max(q.poi || 0, p * .7); }); hitMon(m, base, { w: 'react', color: '#d8f08a' }); }
    return; }
  E[e] = (E[e] || 0) + 1; if (E[e] < 5) return; E[e] = 0;   /* five stacks of one element */
  if (e === 'f') { mfx('blaze', m.x, m.z, 2.6, { pri: 1 }); inCircle(m.x, m.z, 2, q => hitMon(q, base * 1.2, { w: 'react', burn: base * .3, color: '#ffb07a' })); num(m.x, 1.7, m.z, 'ลุกโชน!', '#ffb07a', true); }
  else if (e === 'i') { mfx('frost', m.x, m.z, 2.4, { pri: 1 }); hitMon(m, base, { w: 'react', frz: 1.5, color: '#bfe8ff' }); num(m.x, 1.7, m.z, 'แช่แข็ง!', '#bfe8ff', true); }
  else if (e === 'l') { mfx('bolt', m.x, m.z, 2.6, { pri: 1 }); hitMon(m, base * 1.8, { w: 'react', frz: .4, color: '#fff08a' }); const q = nearest(m.x, m.z, 4, new Set([m])); if (q) { hitMon(q, base, { w: 'react', color: '#fff08a' }); bagFx(() => boltFx(new V3(m.x, .8, m.z), new V3(q.x, .8, q.z), 0xffe14a, .09)); } num(m.x, 1.7, m.z, 'ฟ้าผ่า!', '#fff08a', true); sfx('zap', .6, 1); }
  else if (e === 'p') { mfx('poisoncloud', m.x, m.z, 2.4, { pri: 1 }); m.brit = t + 4; m.poi = (m.poi || 0) + base * .5; num(m.x, 1.7, m.z, 'กัดกร่อน!', '#c8f08a', true); }
}
/* WEAPON MECHANICS of the new items (cfg item.x, bag3d/items2.js): multi / xarr = more arrows (extras at 40 %), twice = a chance to fire again at once,
   nth = every n-th use is special (crit = a sure crit through the line, wave = a long sword wave, spirit = a hunting spirit), spin = a chance to cut all
   round, bash / jolt = a chance to stun / jolt, ramp / rapid = the same target again: harder / faster (stacks). chain / gx effects: not yet (cloud). */
function bagFireX(W) { const X = W.x; if (!X) return; W.nN = (W.nN | 0) + 1;
  if (X.nth && W.nN % X.nth[0] === 0) { const m = bagNear(9); if (m) { const a = dirTo(m); if (X.nth[1] === 'crit') { W.sure = 1; mfx('crit', m.x, m.z, 2); } else if (X.nth[1] === 'wave') { const p = shootP('wave', a, { bag: W, mul: 1.4, spd: 12, life: .9, r: 1.3, kb: 2.5, y: .4 }); if (!NORENDER) { p.mesh = (DEC_POOL.swoosh || []).pop() || decalMesh('swoosh'); decalSet(p.mesh, 0x8fd0ff, 0xffffff, { full: 1, ord: 4 }); p.mesh.scale.set(3.4, 1, 3.4); p.mesh.rotation.y = a - Math.PI / 2; scene.add(p.mesh); } mfx('slash', HERO.pos.x, HERO.pos.z, 2.6); }
      else if (X.nth[1] === 'spirit') shootP('spirit', a, { bag: W, mul: 1.2, spd: 8, life: 3, r: .45, y: 1, c: 0x9ff0ff, boomR: 1.3 }); } }
  if (X.spin && Math.random() < X.spin) { const P0 = HERO.pos; inCircle(P0.x, P0.z, 3, q => bagHit(W, q, .8, { kb: 2.5 })); mfx('spin', P0.x, P0.z, 6, { speed: 1.4 }); sfx('slash', .5, .9); }
  if (X.twice && Math.random() < X.twice) after(.12, () => { if (!HERO.dead) { const M = BAGMOVE[W.id] || BAGMOVE[W.base]; if (M && BAGFIRE[M[0]]) BAGFIRE[M[0]](W, M[1], M[2] || {}); } });
  if (X.rapid) { const m = bagNear(10); if (m && W.rpT === m) W.rpN = Math.min(X.rapid[1], (W.rpN | 0) + 1); else { W.rpT = m; W.rpN = 0; } W.cdM = 1 / (1 + X.rapid[0] * W.rpN); }
}
/* META EFFECTS (owner 2026-11-28 "ทำให้ดูดี รวมถึงเอฟเฟค", "vfx สวยๆ"): 56 hand-painted effects cut from Meta AI videos by tools/art/bag_vfx.py into
   art/bag3d/fx/<key>.webp + fx.json. In the bag fight they REPLACE the small pixel effects wherever one fits (bagMfx is called from the top of
   horde.html pfx(), MF_PF maps a pixel effect to ours), and play at the big moments (crits, class skills, a boss coming in, the win).
   An effect shot from above (fx.json flat) lies on the sand and turns with the floor; the others face the camera, their foot point on the ground
   (MF_FOOT = how far up the picture the ground is, .5 = a burst in the middle of the air). Sheets load on first use (the pixel one plays that time).
   ?mfx=0 = only the old pixel effects. */
const MFX = { J: null, T: {}, n: 0, on: true, go: false };   /* this file loads before horde.html's own script: the first call reads ?mfx and fetches the list */
function mfxInit() { if (MFX.go) return; MFX.go = true; MFX.on = Q.get('mfx') !== '0'; if (!NORENDER && MFX.on) fetch('art/bag3d/fx/fx.json?v=2').then(r => r.json()).then(j => { MFX.J = j; }).catch(() => { }); }
const MF_FOOT = { pillar: .06, blaze: .08, bolt: .05, spikes: .18, rain: .1, heal: .08, vines: .1, frost: .12, poisoncloud: .12, coins: .1, tornado: .06, meteor: .26, aura: .08, react_wet: .16, revive: .28, st_poison: .2, st_burn: .22, react_shatter: .3 };
const MF_PF = { 'fire/meteor-strike': 'meteor', 'lightning/lightning-strike': 'bolt', 'lightning/static-burst': 'react_shock', 'shadow/void-implosion': 'void', 'explosions/implosion': 'void', 'nature/poison-cloud': 'poisoncloud',
  'ice/blizzard': 'blizzard', 'ice/frost-nova': 'frost', 'ice/freeze-encase': 'frost', 'ice/ice-spike': 'react_shatter', 'holy/divine-beam': 'pillar', 'holy/holy-smite': 'pillar', 'holy/shield-bubble': 'guard', 'holy/barrier-block': 'guard',
  'holy/regen-aura': 'heal', 'nature/bloom-heal': 'heal', 'holy/holy-heal': 'heal', 'holy/resurrect': 'revive', 'impacts/ground-slam': 'slam', 'nature/earth-spike': 'spikes', 'wind/whirlwind': 'tornado', 'fire/fire-tornado': 'tornado',
  'melee/sword-combo': 'spin', 'melee/shadow-claw': 'blood', 'impacts/blood-splat': 'blood', 'impacts/crit-hit': 'crit', 'shadow/curse': 'curse', 'explosions/arcane-burst': 'nova', 'shadow/shadow-tendrils': 'nova',
  'projectiles/arrow-impact': 'rain', 'wind/wind-gust': 'slash', 'melee/axe-smear': 'slash', 'impacts/shockwave-ring': 'slam', 'impacts/parry': 'parry', 'fire/ground-flames': 'blaze', 'fire/lava-burst': 'react_overload',
  'explosions/big-explosion': 'ko', 'explosions/fire-nova': 'react_overload', 'status/power-up-aura': 'aura', 'nature/acid-splash': 'react_gas', 'nature/spore-burst': 'react_gas', 'ui/star-burst-pickup': 'craft', 'fire/fire-pillar': 'blaze' };
function mfxTex(k) { let t = MFX.T[k]; if (!t) { t = MFX.T[k] = TL.load(`art/bag3d/fx/${k}.webp?v=2`, q => { q.ok = true; }); t.encoding = THREE.sRGBEncoding; t.minFilter = THREE.LinearFilter; t.generateMipmaps = false; } return t.ok ? t : null; }
function mfx(k, x, z, size, o = {}) {   /* size = width in world units; o.pri, o.dur (loops), o.speed, o.y, o.follow, o.add (light blend), o.turn (flat ones), o.opacity */
  mfxInit(); if (NORENDER || !MFX.on || !MFX.J) return false; const E = MFX.J[k]; if (!E) return false; const base = mfxTex(k); if (!base) return false; if (MFX.n >= (o.pri ? 30 : 20)) return true; MFX.n++;
  const tex = base.clone(); tex.needsUpdate = true; tex.repeat.set(1 / E.cols, 1 / E.rows); tex.offset.set(0, 1 - 1 / E.rows); const s = size, op = o.opacity || 1;
  const mo = { map: tex, transparent: true, depthWrite: false, fog: false, opacity: op, blending: o.add ? THREE.AdditiveBlending : THREE.NormalBlending }; let m;
  if (E.flat) { m = new THREE.Mesh(GEO.plane, new THREE.MeshBasicMaterial(mo)); m.scale.set(s, 1, s); m.rotation.y = o.turn != null ? o.turn : Math.random() * TAU; m.position.set(x, (o.y || 0) + .05 + MFX.n * .002, z); m.renderOrder = 3; }
  else { const a = MF_FOOT[k] != null ? MF_FOOT[k] : .5; m = new THREE.Sprite(new THREE.SpriteMaterial(mo)); m.center.set(.5, a); m.scale.set(s, s, 1); m.position.set(x, o.y != null ? o.y : a < .5 ? .02 : s * .36, z); m.renderOrder = 6; }
  const clip = E.n / E.fps / (o.speed || 1), life = o.dur || clip;
  addFx(m, life, (q, kk, dt, f) => { const fr = E.loop ? Math.floor(f.t * E.fps * (o.speed || 1)) % E.n : Math.min(E.n - 1, Math.floor(f.t / clip * E.n)); tex.offset.set((fr % E.cols) / E.cols, 1 - (Math.floor(fr / E.cols) + 1) / E.rows);
    q.material.opacity = op * Math.min(1, (life - f.t) / Math.min(.25, life * .3)); if (o.follow) q.position.set(o.follow.x, q.position.y, o.follow.z); }, () => { MFX.n--; tex.dispose(); m.material.dispose(); });
  return true;
}
function bagMfx(nm, x, z, size, o) { mfxInit(); if (!BAGM || !MFX.on) return false; const k = MF_PF[nm]; if (!k) return false; return mfx(k, x, z, size * 1.12, { pri: o.pri, dur: o.dur && MFX.J && MFX.J[k] && MFX.J[k].loop ? o.dur : 0, follow: o.follow, speed: o.speed ? Math.min(1.6, o.speed / 1.25) : 1, opacity: o.opacity }); }

/* THE SPELL ITEMS AND THE NEW MOVES (bag3d/items2.js mv; everyone may use the spells, their power is from INT): each one a few lines with its
   painted Meta effect. Return false = nothing to hit (the item waits a moment). */
const bagStrong = (R, n) => MON.filter(q => !q.dead && (q.x - HERO.pos.x) ** 2 + (q.z - HERO.pos.z) ** 2 < R * R).sort((p, q) => q.hp - p.hp).slice(0, n);
const bagKeep = (x, z) => { const L = Math.hypot(x, z), mx = ARENA - .8; return L > mx ? [x * mx / L, z * mx / L] : [x, z]; };
Object.assign(BAGFIRE, {
  blast(W, C) { const m = bagDense(9, 2.5) || bagNear(9); if (!m) return false; const a = dirTo(m), d = Math.hypot(m.x - HERO.pos.x, m.z - HERO.pos.z), T = Math.max(.12, d / 11), x = m.x, z = m.z; shootP('fire', a, { bag: W, mul: 1, spd: 11, life: T, r: 2.3, c: C }); after(T, () => mfx('react_overload', x, z, 3.2)); sfx('whoosh', .5, 1.2); return a; },
  beam(W, C) { const m = bagNear(9); if (!m) return false; const a = dirTo(m), x0 = HERO.pos.x, z0 = HERO.pos.z, sx = Math.sin(a), sz = Math.cos(a), L = 9; for (const q of MON) { if (q.dead) continue; const dx = q.x - x0, dz = q.z - z0, t = dx * sx + dz * sz; if (t > 0 && t < L && Math.abs(dx * sz - dz * sx) < .9 + q.r) bagHit(W, q, 1, { kb: 1.5 }); }
    bagLine(x0, z0, a, L, 0xe8f4ff, .2); bagLine(x0, z0, a, L, C, .4); sfx('zap', .6, 1.4); return a; },
  storm(W) { if (!bagNear(4)) return false; const P0 = HERO.pos; mfx('storm', P0.x, P0.z, 7.5, { pri: 1 }); inCircle(P0.x, P0.z, 3.6, q => bagHit(W, q, 1, { kb: 7, fx: P0.x, fz: P0.z })); sfx('whoosh', .8, .7); return true; },
  stones(W) { const H = HERO; BAG.blk = Math.min(H.max * .6, BAG.blk + W.dmg * 3); mfx('guard', H.pos.x, H.pos.z, 2.4, { pri: 1, follow: H.pos }); num(H.pos.x, 2, H.pos.z, 'ศิลาพิทักษ์', '#d8d0c0');
    for (let k = 0; k < 10; k++) after(k * .45, () => { if (HERO.dead) return; const Q = HERO.pos; inCircle(Q.x, Q.z, 1.9, q => bagHit(W, q, .5, { kb: 2, fx: Q.x, fz: Q.z })); for (let i = 0; i < 3; i++) { const b = k * .9 + i * 2.09; spark(Q.x + Math.cos(b) * 1.5, .7, Q.z + Math.sin(b) * 1.5, { n: 2, color: 0xd8c8a8, spd: .6, size: .3, life: .4 }); } }); return true; },
  ball(W) { const m = bagNear(10); if (!m) return false; const p = { x: HERO.pos.x, z: HERO.pos.z }; let a = dirTo(m); mfx('ball', p.x, p.z, 2.2, { pri: 1, dur: 4, follow: p, y: .8 });
    for (let k = 1; k <= 13; k++) after(k * .3, () => { const t = nearest(p.x, p.z, 6); if (t) a = Math.atan2(t.x - p.x, t.z - p.z); [p.x, p.z] = bagKeep(p.x + Math.sin(a) * .8, p.z + Math.cos(a) * .8); inCircle(p.x, p.z, 1.5, q => bagHit(W, q, .7, { kb: 1.8, fx: p.x, fz: p.z })); if (k % 3 === 0) sfx('zap', .3, 1.3); }); return a; },
  skel(W) { if (!bagNear(11)) return false; const P0 = HERO.pos; mfx('summon', P0.x, P0.z, 3.2, { pri: 1 }); loadKind(BAG_SKEL); for (let i = 0; i < 2; i++) after(.35 + i * .25, () => { if (!HERO.dead) bagAlly(W, HERO.pos.x + (i ? 1 : -1) * .9, HERO.pos.z + .5); }); sfx('chime', .6, .7); return true; },   /* two real skeleton warriors (bagAlly) */
  sprite(W) { if (!bagNear(11)) return false; const H = HERO; mfx('summon', H.pos.x, H.pos.z, 2.6, { pri: 1 }); mfx('st_burn', H.pos.x, H.pos.z, 1.1, { dur: 8, follow: H.pos, y: 2.2 });
    for (let k = 1; k <= 10; k++) after(k * .8, () => { if (HERO.dead) return; const m = bagNear(9); if (m) shootP('fire', dirTo(m), { bag: W, mul: 1, spd: 10, life: Math.max(.15, Math.hypot(m.x - HERO.pos.x, m.z - HERO.pos.z) / 10), r: 1.2, c: 0xff8a3a }); }); return true; },
  totem(W) { if (!bagNear(9)) return false; const x = HERO.pos.x, z = HERO.pos.z; mfx('summon', x, z, 2.6, { pri: 1 }); mfx('st_shock', x, z, 1.4, { dur: 8, y: 1.2 });
    for (let k = 1; k <= 11; k++) after(k * .7, () => { const m = nearest(x, z, 6.5); if (!m) return; bagFx(() => boltFx(new V3(x, 1.2, z), new V3(m.x, .6, m.z), 0xb8a8ff, .08)); bagHit(W, m, 1, {}); }); return true; },
  tstop(W) { if (!bagNear(5)) return false; const P0 = HERO.pos; mfx('timestop', P0.x, P0.z, 9, { pri: 1 }); inCircle(P0.x, P0.z, 5, q => { q.frzT = Math.max(q.frzT, q.boss ? .6 : 1.5); }); sfx('chime', .8, .6); return true; },
  hex(W) { const m = bagStrong(8, 1)[0]; if (!m) return false; mfx('hex', m.x, m.z, 2.4, { pri: 1 }); m.frzT = Math.max(m.frzT, m.boss ? 1.5 : 3); m.hexT = BAG.t + (m.boss ? 1.5 : 3); m.brit = BAG.t + 3; num(m.x, 1.7, m.z, 'กลายเป็นกบ!', '#b8ff8a', true); return dirTo(m); },
  vine(W) { const m = bagDense(9, 2.4) || bagNear(9); if (!m) return false; const x = m.x, z = m.z; mfx('vines', x, z, 3, { pri: 1 }); inCircle(x, z, 2.4, q => { q.frzT = Math.max(q.frzT, q.boss ? .7 : 2); bagHit(W, q, 1, { kb: 0 }); }); return dirTo(m); },
  silence(W) { if (!bagNear(5)) return false; const P0 = HERO.pos; mfx('silence', P0.x, P0.z, 7, { pri: 1 }); inCircle(P0.x, P0.z, 5, q => { q.atkT = Math.max(q.atkT, 4); q.slowT = Math.max(q.slowT, 2); q.slowK = Math.min(q.slowK, .7); }); return true; },
  weak(W) { const m = bagDense(9, 3) || bagNear(9); if (!m) return false; mfx('curse', m.x, m.z, 2.6, { pri: 1 }); inCircle(m.x, m.z, 3, q => { q.weakT = BAG.t + 5; }); return dirTo(m); },
  brittle(W) { const m = bagDense(9, 3) || bagNear(9); if (!m) return false; mfx('curse', m.x, m.z, 2.6, { pri: 1 }); inCircle(m.x, m.z, 3, q => { q.brit = BAG.t + 5; }); return dirTo(m); },
  mark(W) { const L = bagStrong(9, 3); if (!L.length) return false; for (const q of L) { q.mark = BAG.t + 6; mfx('curse', q.x, q.z, 1.6); bagHit(W, q, 1, {}); } return dirTo(L[0]); },
  spread(W) { const m = bagNear(9); if (!m) return false; mfx('poisoncloud', m.x, m.z, 2.4); m.spread = 1; m.poi = (m.poi || 0) + W.dmg * 1.5; bagHit(W, m, 1, {}); return dirTo(m); },
  leapcut(W) { const m = MON.filter(q => !q.dead).sort((p, q) => Math.hypot(q.x - HERO.pos.x, q.z - HERO.pos.z) - Math.hypot(p.x - HERO.pos.x, p.z - HERO.pos.z)).find(q => Math.hypot(q.x - HERO.pos.x, q.z - HERO.pos.z) < 10); if (!m) return false; const H = HERO.pos;
    mfx('dash', H.x, H.z, 2.2); H.x = m.x - (m.x - H.x) * .12; H.z = m.z - (m.z - H.z) * .12; inCircle(H.x, H.z, 2.4, q => bagHit(W, q, 1, { kb: 2.5 })); mfx('spin', H.x, H.z, 5); sfx('slash', .6, 1); return dirTo(m); },
  blinkstab(W) { const m = bagStrong(9, 1)[0]; if (!m) return false; const H = HERO.pos; mfx('blink', H.x, H.z, 2); const a = dirTo(m); [H.x, H.z] = bagKeep(m.x + Math.sin(a) * .9, m.z + Math.cos(a) * .9); mfx('blink', H.x, H.z, 2); after(.08, () => { if (!m.dead) { bagHit(bagW(W, { crit: 1 }), m, 2, { kb: 2 }); mfx('crit', m.x, m.z, 2); } }); sfx('slash', .7, 1.3); return a + Math.PI; },
});
/* ---- what the engine asks (hooks in horde.html) */
function bagHurt(d, src, o) {   /* before armour: magic resist for shots, dodge, thorns, the shield. o (a duel hit): ty, pc = shield pierce, mp = magic pierce, dot, tru, ref = a hit back (no counters) */
  const H = HERO, S = BAG.st, P0 = H.pos, q = o || {};
  if (BAG.duel) { if (q.tru) return d; if (q.ty === 'mag' || q.dot) d *= 1 - Math.max(0, (S.mres || 0) - (q.mp || 0)); else if (S.dodge && !q.ref && Math.random() < S.dodge) { num(P0.x, 1.8, P0.z, 'หลบ', '#cfe8ff'); return 0; } if (q.dot) return d; }   /* a duel: like the side view (magic resist for magic, dodge for weapons), poison / burn skip the shields */
  else { if (BAG.t > BAG.dur) d *= 1 + (BAG.t - BAG.dur) * .05; if (!src) d *= 1 - (S.mres || 0); else if (S.dodge && Math.random() < S.dodge) { num(P0.x, 1.8, P0.z, 'หลบ', '#cfe8ff'); H.inv = .25; return 0; } }
  if (src && src.weakT > BAG.t) d *= .75;   /* weakness curse */
  const X = S.gx || {}, t = BAG.t;   /* whole-bag item effects (bag3d/items2.js gx) */
  if (X.sprint && src && d > 0) { if (!(BAG.spT > t)) { mfx('dash', P0.x, P0.z, 2); num(P0.x, 2.1, P0.z, 'เร่งฝีเท้า!', '#bfffd0'); } BAG.spT = t + 2; }   /* sprint boots: any hit that was not dodged, even one the shield takes */
  if (X.blink && src && d >= H.max * .08 && !(BAG.blT > t)) { BAG.blT = t + X.blink; mfx('blink', P0.x, P0.z, 2.2, { pri: 1 }); const a = Math.atan2(P0.z - src.z, P0.x - src.x); let x = P0.x + Math.cos(a) * 3.2, z = P0.z + Math.sin(a) * 3.2; const L = Math.hypot(x, z), mx = ARENA - .8; if (L > mx) { x *= mx / L; z *= mx / L; } P0.x = x; P0.z = z; mfx('blink', x, z, 2.2, { pri: 1 }); H.inv = .4; sfx('whoosh', .6, 1.6); return 0; }   /* blink cloak: out of a heavy hit */
  if (X.sshield && d >= H.max * .05 && !(BAG.ssT > t)) { BAG.ssT = t + X.sshield; mfx('guard', P0.x, P0.z, 2.4, { pri: 1 }); num(P0.x, 1.8, P0.z, 'กันเวท', '#bfe4ff'); H.inv = .3; return 0; }   /* spell shield: one big hit every few seconds */
  if (X.counter && src && !src.dead && !q.ref && Math.random() < X.counter) { const W = BAG.its.filter(q => q.dmg > 0 && !q.self && !q.once).sort((p, q) => q.dmg - p.dmg)[0]; if (W) { bagHit(W, src, .8, { kb: 2, ref: 1 }); mfx('parry', src.x, src.z, 1.6); } }   /* counter strike */
  if (X.chill && src && !src.dead) { src.slowT = Math.max(src.slowT, 1.5); src.slowK = Math.min(src.slowK, 1 - X.chill); }   /* frost armour: attackers slow down */
  if (src && S.thorn && !src.dead && !q.ref) hitMon(src, S.thorn * 2.5, { w: 'thorn', color: '#c8e8a0', ref: 1, ty: 'phy' });
  if (BAG.blk > 0) { const a = Math.min(BAG.blk, d * (1 - Math.min(.9, (q.pc || 0) + (q.ap || 0)))); BAG.blk -= a; d -= a; if (d < .5) { if (!BAG.duel) H.inv = .3; num(P0.x, 1.8, P0.z, 'กัน', '#8fc8ff'); spark(P0.x, 1, P0.z, { n: 4, color: 0x8fc8ff, spd: 2.5, size: .22, life: .25 }); sfx('tick', .3, 1.6); return 0; } }
  if (d >= 1) bagSwing('hurt', null); if (X.potion && !BAG.potion && H.hp - d < H.max * .3) { BAG.potion = 1; after(.05, () => { if (!HERO.dead) { healHero(H.max * X.potion); num(P0.x, 2, P0.z, '+' + Math.round(H.max * X.potion), '#9fe870', true); mfx('heal', P0.x, P0.z, 2.2, { pri: 1, follow: P0 }); } }); }   /* emergency potion, once a round */
  return d; }
function bagKill(m) { if (m.spread) { let n = 0; inCircle(m.x, m.z, 3, q => { if (n < 2 && q !== m && !q.dead && !q.spread) { n++; q.spread = 1; q.poi = (q.poi || 0) + (m.poi || 3) * .8; mfx('poisoncloud', q.x, q.z, 1.8); } }); }
  const X = BAG.st.gx || {}; if (X.skull) BAG.skull = Math.min(X.skull, (BAG.skull | 0) + 1);   /* hunter skull: +1 damage a kill this round */
  bagKill0(m); }
function bagKill0(m) {   /* no xp gems in this mode: a few coins (bonus gold for the shop), a rare heart */
  bagCheer(m.boss ? 1.6 : m.elite ? .35 : .025, m.boss);   /* the arena crowd: louder with every kill, wild for a boss */
  if (m.boss) { G.boss = null; mfx('ko', m.x, m.z, 5, { pri: 1 }); shake(.6); sfx('boom', 1, .6); FLASH.w = .4; for (let i = 0; i < 3; i++) after(i * .22, () => pfx('explosions/big-explosion', m.x + rnd(-1, 1), m.z + rnd(-.6, .6), 4.5)); ring(m, 0xffd060, .5, 7, .8); column(m, 0xffd060, 1, 1, 6); for (let i = 0; i < 5; i++) drop('coin', m.x + rnd(-1.4, 1.4), m.z + rnd(-1.4, 1.4), 1); return; }
  if (m.elite) { pfx('explosions/arcane-burst', m.x, m.z, 3); sfx('boom', .6, 1.2); shake(.25); for (let i = 0; i < 2; i++) drop('coin', m.x + rnd(-.6, .6), m.z + rnd(-.6, .6), 1); return; }
  const r = Math.random(); if (r < BAG.coinP) drop('coin', m.x, m.z, 1); else if (r < BAG.coinP + .012) drop('heart', m.x, m.z, 1); }
function bagWave(round, boss) {   /* how many monsters, how strong, when they come. ALL of them must die */
  const N = Math.min(120, Math.round(16 + round * 5)), dur = 16 + Math.min(16, round * 1.1), plan = [], tier = Math.min(3, Math.floor((round - 1) / 4)), R = rng((G.seed | 0) + round * 131);
  const L = MAP.mobs[tier].filter(k => MOBS[k]).slice(); for (let i = L.length - 1; i > 0; i--) { const j = R() * (i + 1) | 0;[L[i], L[j]] = [L[j], L[i]]; } const kinds = L.slice(0, 3); if (tier > 0) { const O = MAP.mobs[tier - 1].filter(k => MOBS[k]); kinds.push(O[R() * O.length | 0]); }
  const up = Math.max(0, round - 5); BAG.mhp = (4 + round * 1.6 + round * round * .1) * (1 + up * .03); BAG.mdmg = (2.2 + round * .42) * (1 + up * .02);   /* x1.3 life / x1.2 hits by round 15: the item skills (2026-11-28) made rounds 10-15 always won */ G.spdMul = 1.2 + Math.min(.4, round * .025); BAG.dur = dur + 12;   /* monsters are faster here than in the survival game: the champion cannot simply outrun them */ BAG.kinds = kinds;
  const n0 = Math.round(N * .34); let left = N - n0; for (let i = 0; i < n0;) { const c = Math.min(n0 - i, 2 + (R() * 3 | 0)), a = R() * TAU; plan.push({ t: .3, n: c, a, d: 7.5 + R() * 4, k: kinds[R() * kinds.length | 0] }); i += c; }
  const sw = round >= 3 ? Math.min(left, Math.min(26, 6 + round)) : 0; left -= sw;
  /* PACKS (owner 2026-11-28 "ให้มอนวิ่งมารุมตามรอบ"): the rest come as packs that RUN IN from one side at a time (a red arrow at the screen edge warns
     .9 s before), a pack every ~3 s, bigger every round (6 -> 14), the side turning round the champion so they swarm from everywhere */
  const pk = Math.min(14, 5 + Math.round(round * .8)), np = Math.max(1, Math.ceil(left / pk)); let a0 = R() * TAU;
  for (let i = 0, j = 0; i < left; j++) { const c = Math.min(left - i, pk), t = 2.5 + (dur - 2.5) * (j / np); a0 += 1.9 + R() * 1.4; plan.push({ t, n: c, a: a0, d: 0, pack: 1, k: kinds[R() * kinds.length | 0] }); if (c >= 4) plan.push({ t: Math.max(.6, t - .9), n: 0, warn: a0 }); i += c; }
  if (sw) plan.push({ t: dur * .55, n: sw, ring: 1, k: kinds[0], o: { hp: .55, spd: .85 } });
  if (!boss && round >= 4) for (let e = 0; e < (round >= 9 ? 2 : 1); e++) plan.push({ t: dur * (.4 + e * .3), n: 1, a: R() * TAU, d: 0, k: kinds[R() * kinds.length | 0], o: { hp: 5 + round * .3, sc: 1.65, dmg: 1.5, elite: true, tint: [1.45, 1.2, .5] }, note: 'มอนหัวหน้าฝูงปรากฏ' });
  plan.sort((p, q) => p.t - q.t); BAG.warn = []; BAG.plan = plan; BAG.pi = 0; BAG.total = plan.reduce((s, p) => s + p.n, 0) + (boss ? 1 : 0); BAG.bossHp = Math.round((110 + round * round * 8 + round * 20) * 1.15); return kinds;
}
/* THE ARENA (horde.html map=arena): every pack runs out of the gate nearest its side; the boss comes through the main gate (far side) */
const bagIsArena = () => typeof MAPK !== 'undefined' && MAPK === 'arena' && typeof ARENA_GATES !== 'undefined' && ARENA_GATES;
const bagPaint = () => typeof PAINT !== 'undefined' && PAINT;
function bagGateP(a) { let best = PA.gates[0], bd = 9; for (const g of PA.gates) { const d = bagAngD(a, Math.atan2(g[1], g[0])); if (d < bd) { bd = d; best = g; } } return best; }   /* the painted arena: the way in nearest to that side */
function bagGate(a) { let best = ARENA_GATES[0], bd = 9; for (const g of ARENA_GATES) { const d = bagAngD(a, g); if (d < bd) { bd = d; best = g; } } return best; }
function bagCheer(v, hold) { if (typeof CROWDU !== 'undefined') CROWDU.value = hold ? Math.max(CROWDU.value, v) : Math.min(1.7, CROWDU.value + v); }
function bagFair(k, o) { const K = KIND[k], q = Object.assign({}, o); if (K && K.st) { q.hp = (q.hp || 1) * Math.pow(K.st.hp, -.4); q.dmg = (q.dmg || 1) * Math.pow(K.st.dmg, -.4); } return q; }   /* big kinds are tougher, but less than in the survival game: the round's level already makes them stronger */
function bagSpawn(e) {
  if (e.warn != null) { if (bagPaint()) { const g = bagGateP(e.warn); BAG.warn.push({ a: Math.atan2(g[1] - HERO.pos.z, g[0] - HERO.pos.x), t: 1.3 }); } else BAG.warn.push({ a: bagIsArena() ? bagGate(e.warn) : e.warn, t: 1.3 }); return; }
  if (bagPaint() && !e.ring) { const g = bagGateP(e.a), L = Math.hypot(g[0], g[1]), tx = -g[1] / L, tz = g[0] / L; if (e.n >= 4) note('ฝูงมอนวิ่งออกจากประตู! ×' + e.n, '#ff9a7a');   /* out of a painted gate, spread across its mouth and a little behind it */
    for (let i = 0; i < e.n; i++) { const t = rnd(-.9, .9), b = rnd(0, Math.min(2.2, e.n * .16)); spawnMon(e.k, g[0] + tx * t + g[0] / L * b, g[1] + tz * t + g[1] / L * b, bagFair(e.k, e.o)); } pfx('smoke/dust-puff', g[0] * .93, g[1] * .93, 2.6); if (e.note) note(e.note, '#ffd86a'); return; }
  if (bagIsArena() && !e.ring) { const g = bagGate(e.a), cx = Math.cos(g), cz = Math.sin(g); if (e.n >= 4) note('ฝูงมอนวิ่งออกจากประตู! ×' + e.n, '#ff9a7a');   /* out of the gate, spread across its mouth */
    for (let i = 0; i < e.n; i++) { const r = ARENA - .7 - rnd(0, Math.min(2.4, e.n * .18)), t = rnd(-1, 1); spawnMon(e.k, cx * r - cz * t, cz * r + cx * t, bagFair(e.k, e.o)); } pfx('smoke/dust-puff', cx * (ARENA - 1), cz * (ARENA - 1), 2.6); if (e.note) note(e.note, '#ffd86a'); return; }
  if (e.ring) { for (let i = 0; i < e.n; i++) { const [x, z] = ringPos(Math.min(SPAWNR - .5, 11.5), i / e.n * TAU); spawnMon(e.k, x, z, bagFair(e.k, e.o)); } banner('ฝูงใหญ่ล้อมแล้ว!', 'ฝ่าวงล้อมออกไป', true, 1.8); sfx('hurt', .6, .6); return; }
  if (e.pack && e.n >= 4) note('ฝูงมอนวิ่งมารุม! ×' + e.n, '#ff9a7a');
  for (let i = 0; i < e.n; i++) { const [x, z] = ringPos((e.d || SPAWNR + rnd(0, 2)) + rnd(0, e.pack ? 2.4 : 1.2), e.a + rnd(e.pack ? -.38 : -.22, e.pack ? .38 : .22)); const m = spawnMon(e.k, x, z, bagFair(e.k, e.o)); if (m && e.d) spark(x, .3, z, { n: 3, color: 0xd8d0c0, spd: 1.5, up: 2, size: .25, life: .35 }); } if (e.note) note(e.note, '#ffd86a'); }
function bagBoss() { const bi = Math.min(3, Math.floor(BAG.cfg.round / 5) - 1), k = MAP.boss[Math.max(0, bi) % MAP.boss.length]; BAG.bossWait = true;
  loadKind(k).then(() => { const K = KIND[k]; if (!K || !K.ok || !BAG.on) { BAG.bossWait = false; BAG.total--; return; } const [x, z] = bagPaint() ? [PA.gates[0][0], PA.gates[0][1] + .6] : bagIsArena() ? [0, -(ARENA - 1.4)] : ringPos(Math.min(SPAWNR - 1, 11)), m = spawnMon(k, x, z, { boss: true, bi: Math.max(0, bi), spd: .85, dmg: .75 }); BAG.bossWait = false; if (!m) { BAG.total--; return; }
    m.hp = m.max = BAG.bossHp; m.r = Math.max(m.r, .8); G.boss = m; mfx('bossin', x, z, 7, { pri: 1 }); banner('บอสบุก!', MOBS[k].name, true, 2.6); bagCheer(1.5, true); setMusic('drums'); shake(.4); sfx('boom', .9, .6); sfx('roar', 1); G.slow = 1.2; CAM.focus = { m, t: 0, dur: 2 }; }); }
function bagUpd(dt) {   /* instead of the weapons / director / shrines / ultimate of the normal game */
  if (typeof CROWDU !== 'undefined') CROWDU.value += (.32 - CROWDU.value) * Math.min(1, dt * .45);   /* the cheer dies down */
  const H = HERO; BAG.t += dt; while (BAG.pi < BAG.plan.length && BAG.plan[BAG.pi].t <= BAG.t) bagSpawn(BAG.plan[BAG.pi++]); if (BAG.cfg.boss && !BAG.bossed && BAG.t > 4) { BAG.bossed = true; bagBoss(); }
  bagSideUpd(dt); if (BAG.duel) { bagWith(SIDES[1], () => { if (!HERO.dead) bagSideUpd(dt); }); bagDuelUpd(dt); }
  if (BAG.raged && !BAG.duel) { BAG.rk = (BAG.rk || 0) - dt; if (BAG.rk <= 0) { BAG.rk = 1; for (const m of MON) if (!m.dead && m.spd < 6) m.spd *= 1.04; } }
  if (!BAG.duel && BAG.t > BAG.dur && !BAG.raged) { BAG.raged = true; banner('ฝูงมอนคลั่ง!', 'รีบกวาดให้หมด: ยิ่งนานมอนยิ่งตีแรง', true, 2.2); }
  if (!BAG.done && BAG.pi >= BAG.plan.length && !BAG.bossWait && (!BAG.cfg.boss || BAG.bossed) && aliveN() === 0 && G.endT <= 0) { { const M = H.M; bagCheer(1.8, true); chPlay(M, 'U', 'Cheer', true, 1.2); chPlay(M, 'L', 'Cheer', true, 1.2); H.atkT = H.dodgeT = 3; H.apr = 9; } BAG.done = true; G.won = true; G.endT = 1.4; jingle('win'); mfx('victory', H.pos.x, H.pos.z, 4.6, { pri: 1, y: 1.4 }); mfx('aura', H.pos.x, H.pos.z, 2.4, { pri: 1, dur: 1.4, follow: H.pos }); banner(BAG.duel ? 'ชนะการดวล!' : 'ชนะ!', BAG.duel ? BAG.rname + ' ล้มแล้ว' : 'กวาดฝูงมอนรอบ ' + BAG.cfg.round + ' หมดแล้ว', false, 1.6); for (const g of GEMS) g.pull = true; }
}
function bagSideUpd(dt) {   /* ONE champion's bag: stamina, the items, boots, the class skill, the poison on what it hit. A duel runs it for both sides (bagWith); a stunned / frog champion does nothing, a slowed one is slower */
  const S = BAG.st, H = HERO, me = BAG.duel && CUR ? CUR.me : null, stun = !!me && (me.frzT > 0 || me.hexT > BAG.t); if (H.atkT <= 0) H.apr = 0;
  if (BAG.mv0) P.spd = BAG.mv0 * (BAG.spT > BAG.t ? 1.6 : 1);   /* sprint boots: +60 % for 2 s after a hit */ if (!stun && !H.dead) bagRetreat(S.gx || {}); bagAllies(dt);
  BAG.sta = Math.min(S.stam, BAG.sta + S.sreg * dt); const hs = (1 + (S.haste || 0)) * (me && me.slowT > 0 ? .5 + .5 * me.slowK : 1);
  if (!stun) {
  for (const W of BAG.its) { if (W.fl > 0) W.fl -= dt;
    if (W.once) { if (!W.done && BAG.t >= 3.5 && bagFire(W) !== false) { W.done = 1; W.fl = .4; bagPop(W); bagSwing(W.mv, null); } continue; }
    W.t += dt * hs; if (W.t < W.cd * (W.cdM || 1)) continue; if (W.self) { W.t = 0; W.fl = .25; bagSelf(W); bagSwing(W.blk ? 'block' : 'eat', null); bagIskUse(W); continue; } if (BAG.sta < W.sta) continue;
    const r = bagFire(W); if (r === false) { W.t = W.cd - .12; continue; } W.t = 0; BAG.sta -= W.sta; W.fl = .25; bagPop(W); bagSwing(W.mv, typeof r === 'number' ? r : null); bagIskUse(W); }
  { const X = S.gx || {}; if (X.leap && BAG.t > 2 && !(BAG.lpT > BAG.t)) { const m = MON.filter(q => !q.dead).sort((p, q) => Math.hypot(q.x - H.pos.x, q.z - H.pos.z) - Math.hypot(p.x - H.pos.x, p.z - H.pos.z))[0]; if (m && Math.hypot(m.x - H.pos.x, m.z - H.pos.z) > 3) { BAG.lpT = BAG.t + X.leap; H.pos.x = m.x - (m.x - H.pos.x) * .15; H.pos.z = m.z - (m.z - H.pos.z) * .15; mfx('dash', H.pos.x, H.pos.z, 2.4); after(.05, () => { const W = BAG.its.filter(q => q.dmg > 0 && !q.self && !q.once).sort((p, q) => q.dmg - p.dmg)[0]; if (W) bagBoom(W, H.pos.x, H.pos.z, 2.4, 1, { kb: 3, c: 0xffd890 }); mfx('slam', H.pos.x, H.pos.z, 4, { pri: 1 }); shake(.2); }); } } }   /* leap boots */
  if (BAG.sk && !(me && me.atkT > 0)) { BAG.sk.g += dt * hs; if (BAG.sk.g >= BAG.sk.cd && bagNear(10)) { BAG.sk.g = 0; bagSkill(); } }
  }
  BAG.tk -= dt; if (BAG.tk <= 0) { BAG.tk = .5; for (const m of MON) if (!m.dead && m.poi > 0) hitMon(m, m.poi * .5, { w: 'poison', color: '#c8f080', dot: 1 }); }
}
function bagAuto(dt) {   /* the champion holds the ground and lets the bag fight: walks to the nearest monster when nothing is in reach, steps out of a boss's body and away from shots, picks up coins when it is quiet, dashes out when badly hurt in a crowd */
  if (BAG.duel) return bagDuelAuto(dt); const H = HERO.pos; let fx = 0, fz = 0, nd = 1e9, nm = null, close = 0, cx = 0, cz = 0;
  for (const m of MON) { if (m.dead) continue; const dx = H.x - m.x, dz = H.z - m.z, d2 = dx * dx + dz * dz; if (d2 < nd) { nd = d2; nm = m; } if (d2 < 4) { close++; cx += dx; cz += dz; } if (m.boss) { const R = 3 + m.r; if (d2 < R * R) { const w = 5 / (d2 + .3); fx += dx * w; fz += dz * w; } } }
  for (const b of BUL) { const dx = H.x - b.x, dz = H.z - b.z, d2 = dx * dx + dz * dz; if (d2 < 9) { fx += dx / (d2 + .2) * 2; fz += dz / (d2 + .2) * 2; } }
  if (!close) { let gd = 7, gx = 0, gz = 0; for (const g of GEMS) { const d = Math.hypot(g.x - H.x, g.z - H.z); if (d < gd) { gd = d; gx = g.x - H.x; gz = g.z - H.z; } } if (gd < 7) { fx += gx / (gd || 1) * .8; fz += gz / (gd || 1) * .8; } }
  const TY = BAG.ty; if (nm && !nm.boss && TY !== 'mel' && nd < 2.4 * 2.4) { const d = Math.sqrt(nd) || 1; fx -= (nm.x - H.x) / d * .9; fz -= (nm.z - H.z) / d * .9; }   /* ranged and mages step back a little */
  if (nm && !nm.boss) { const d = Math.sqrt(nd); if (d > BAG.reach) { fx += (nm.x - H.x) / d; fz += (nm.z - H.z) / d; } } else if (nm && nd > 36) { const d = Math.sqrt(nd); fx += (nm.x - H.x) / d; fz += (nm.z - H.z) / d; }
  const R = Math.hypot(H.x, H.z), eg = bagPaint() ? 1 : bagIsArena() ? 3 : 6; if (R > ARENA - eg) { fx -= H.x / R * (R - ARENA + eg) * .6; fz -= H.z / R * (R - ARENA + eg) * .6; }   /* the arena is small: keep off its wall, not off half of it */
  const L = Math.hypot(fx, fz); if (L < .06) INP.x = INP.z = 0; else { INP.x = fx / L; INP.z = fz / L; }
  if (TY !== 'mel' && HERO.dashCd <= 0 && HERO.hp < HERO.max * .5 && close >= 4) {   /* melee never runs away */ const c = Math.hypot(cx, cz) || 1; INP.x = cx / c; INP.z = cz / c; heroDash(); }
}
function bagInp(dt) { JOY.on = false; if (!HERO.dead && G.endT <= 0 && BAG.t > .7) bagAuto(dt); else INP.x = INP.z = 0; }   /* owner 2026-11-27 "ไม่ต้องบังคับดิ ให้มันออโต้ โดยเราจัดกระเป๋าแบบเดิม": the player never steers, the fight is fully automatic */
/* RETREAT BOOTS (gx.retreat = seconds between two, ranged / mages only): an enemy within 1.9 = a quick roll away (along the wall when the wall is
   behind), the roll's short dodge included. SKELETON WARRIORS (the skeleton staff, mv 'skel'): two real allies (BAG.allies, a bone-guard card in a
   ghostly green; a duel rival's in red) that walk to the nearest enemy and strike it every .8 s (.4 of the staff's hit, with its elements) for 10 s.
   Monsters do not attack them (they are not in MON); horde.html fillBatches draws them through bagMonsDraw. */
const BAG_SKEL = 'mob_graveyard_bone_guard';
function bagRetreat(X) { const H = HERO; if (!X.retreat || BAG.ty === 'mel' || BAG.rtT > BAG.t || H.dashCd > 0 || H.dashT > 0 || G.state !== 'play' || BAG.t < 1) return; const m = nearest(H.pos.x, H.pos.z, 1.9); if (!m) return;
  let ax = H.pos.x - m.x, az = H.pos.z - m.z; const L = Math.hypot(ax, az) || 1; ax /= L; az /= L; if (Math.hypot(H.pos.x + ax * 3, H.pos.z + az * 3) > ARENA - 1) { const R = Math.hypot(H.pos.x, H.pos.z) || 1, tx = -H.pos.z / R, tz = H.pos.x / R, sg = tx * ax + tz * az >= 0 ? 1 : -1; ax = tx * sg - H.pos.x / R * .4; az = tz * sg - H.pos.z / R * .4; const L2 = Math.hypot(ax, az) || 1; ax /= L2; az /= L2; }
  INP.x = ax; INP.z = az; if (heroDash()) { BAG.rtT = BAG.t + X.retreat; mfx('dash', H.pos.x, H.pos.z, 2.2); num(H.pos.x, 2.1, H.pos.z, 'ถอยฉาก!', '#cfe8ff'); } }
function bagAlly(W, x, z) { const K = KIND[BAG_SKEL]; if (!K || !K.ok || !BAG.allies || BAG.allies.length >= 6) return; [x, z] = bagKeep(x, z);
  BAG.allies.push({ ally: 1, k: BAG_SKEL, K, x, z, kx: 0, kz: 0, hp: 1, max: 1, r: K.rad, sc: K.bsc * 1.05, fr: Math.random() * 4, row: 0, flip: 1, flash: 0, dead: false, deadT: 0, y: 0, tint: CUR && CUR.k ? [1.45, .75, .7] : [.75, 1.35, 1.2], atkT: .5, life: 10, W, slowT: 0, frzT: 0, burnT: 0 });
  pfx('smoke/dust-puff', x, z, 1.6, { opacity: .8 }); spark(x, .5, z, { n: 6, color: 0xc8f0d8, spd: 2, up: 3, size: .25, life: .5 }); }
function bagAllies(dt) { const A = BAG.allies; if (!A || !A.length) return; const H = HERO;
  for (let i = A.length - 1; i >= 0; i--) { const a = A[i]; if (a.dead) { a.deadT += dt; if (a.deadT > .3) A.splice(i, 1); continue; } a.life -= dt; a.atkT -= dt; a.flash = Math.max(0, a.flash - dt * 7);
    if (a.life <= 0 || H.dead) { a.dead = true; a.deadT = 0; pfx('smoke/dust-puff', a.x, a.z, 1.4, { opacity: .8 }); continue; }
    const m = nearest(a.x, a.z, 14); a.row = 0; let dx, dz;
    if (m) { dx = m.x - a.x; dz = m.z - a.z; const d = Math.hypot(dx, dz) || 1, reach = m.r + a.r + .25; if (d > reach) { a.x += dx / d * 3.4 * dt; a.z += dz / d * 3.4 * dt; } else { if (a.K.rows > 1) a.row = 1; if (a.atkT <= 0) { a.atkT = .8; bagHit(a.W, m, .4, { kb: .8, fx: a.x, fz: a.z }); spark(m.x, .6, m.z, { n: 2, color: 0xd8f0e0, spd: 2, size: .2, life: .25 }); } } }
    else { dx = H.pos.x - a.x; dz = H.pos.z - a.z; const d = Math.hypot(dx, dz) || 1; if (d > 1.8) { a.x += dx / d * 3.4 * dt; a.z += dz / d * 3.4 * dt; } }
    for (const b of A) { if (b === a || b.dead) continue; const ex = a.x - b.x, ez = a.z - b.z, e = Math.hypot(ex, ez); if (e > 1e-4 && e < .7) { a.x += ex / e * (.7 - e) * .5; a.z += ez / e * (.7 - e) * .5; } }
    [a.x, a.z] = bagKeep(a.x, a.z); if (Math.abs(dx) > .15) a.flip = dx > 0 ? -1 : 1; a.fr += dt * (a.row ? 8 : 6); } }
function bagMonsDraw() { let L = MON; for (const sd of SIDES) { const A = sd === CUR ? BAG.allies : sd.b.allies; if (A && A.length) L = L.concat(A); } return L; }   /* the monster cards to draw: the monsters + every side's skeletons */
/* ITEM SKILLS (bag3d/itemskills.js, owner 2026-11-28 "ไอเทมมีสกิลเฉพาะ", "vfx สวยๆ"): every `every` uses of an item its own named skill goes off,
   built from the CC0 pixel effects of art/pvfx + the arena's rings, beams, bolts, decals and sparks. A kind returns false when it has nothing to hit
   (then the next use tries again). The name floats over the champion in the item's colour and the item's icon pops. */
const bagW = (W, o) => Object.assign({}, W, o), ipfx = (nm, x, z, s, o) => pfx(nm, x, z, s * 1.3, Object.assign({ pri: 1, max: .075 }, o));   /* skill effects may be bigger than the normal cap and still play when the screen is busy */
const BAGISK = {
  meteor(W, S) { const n = S.count || 1; let any = false; for (let i = 0; i < n; i++) { const t = bagDense(11, 2.4) || bagNear(11); if (!t) break; any = true; const x = t.x + (i ? rnd(-1.4, 1.4) : 0), z = t.z + (i ? rnd(-1.4, 1.4) : 0);
      after(i * .32, () => { ipfx(S.pf, x, z, 3.4); bagFx(() => decal('target', x, z, 3.4, S.c, 0xffffff, { life: .6 }));
        after(.55, () => { if (HERO.dead) return; bagBoom(bagW(W, { burn: (W.burn || 0) + (S.burn || 0) }), x, z, 2.3, 1.7, { c: S.c, kb: 3.5 }); if (S.pf2) ipfx(S.pf2, x, z, 2.4, { dur: 1.6 }); shake(.35); FLASH.w = Math.max(FLASH.w, .25); sfx('boom', .9, .8); }); }); }
    return any; },
  thunder(W, S) { const P = HERO.pos, n = S.count || 5, hit = new Set(), W2 = bagW(W, { stun: Math.max(W.stun || 0, .7) }); let cur = bagNear(9); if (!cur) return false; let prev = { x: P.x, z: P.z };
    for (let i = 0; i < n && cur; i++) { const m = cur, a = prev; hit.add(m); after(i * .09, () => { if (m.dead && i) return; bagFx(() => boltFx(new V3(a.x, 1.2, a.z), new V3(m.x, .6, m.z), S.c, .12)); ipfx(S.pf, m.x, m.z, 2.2); bagHit(W2, m, 1.4, { kb: 1.5 }); spark(m.x, .8, m.z, { n: 6, color: S.c, spd: 4, up: 3, size: .25, life: .35 }); });
      prev = { x: m.x, z: m.z }; let best = null, bd = 4.5 * 4.5; for (const q of MON) { if (q.dead || hit.has(q)) continue; const d = (q.x - m.x) ** 2 + (q.z - m.z) ** 2; if (d < bd) { bd = d; best = q; } } cur = best; }
    if (S.pf2) ipfx(S.pf2, P.x, P.z, 2.6); sfx('zap', .9, 1); shake(.25); FLASH.w = Math.max(FLASH.w, .3); return true; },
  nova(W, S) { const P = HERO.pos; ipfx(S.pf, P.x, P.z, 3.6); if (S.pf2) ipfx(S.pf2, P.x, P.z, 2.6); ring(P, S.c, .5, 4.2, .5, .9); bagBoom(bagW(W, { poi: (W.poi || 0) + (S.poi || 0) }), P.x, P.z, 3.8, 1.5, { c: S.c, kb: 5 }); shake(.3); sfx('boom', .8, 1.1); return true; },
  pillar(W, S) { const n = S.count || 1; let any = false; for (let i = 0; i < n; i++) { const t = bagDense(11, 2) || bagNear(11); if (!t) break; any = true; const x = t.x + (i ? rnd(-1.6, 1.6) : 0), z = t.z + (i ? rnd(-1.6, 1.6) : 0);
      after(i * .2, () => { ipfx(S.pf, x, z, 2.6); column({ x, z }, S.c, .9, .9, 6); bagFx(() => decal('sigil', x, z, 3, S.c, 0xffffff, { life: 1 })); for (let k = 0; k < 3; k++) after(.25 + k * .28, () => { if (!HERO.dead) bagBoom(W, x, z, 1.9, .75, { c: S.c, kb: 1 }); }); }); }
    if (any) { sfx('chime', .8, .8); FLASH.w = Math.max(FLASH.w, .2); } return any; },
  spikes(W, S) { const m = bagNear(9); if (!m) return false; const P = HERO.pos, a = dirTo(m), sx = Math.sin(a), sz = Math.cos(a), x0 = P.x, z0 = P.z, hit = new Set(), W2 = bagW(W, S.frz ? { stun: Math.max(W.stun || 0, S.frz) } : {});
    for (let i = 1; i <= 7; i++) { const x = x0 + sx * i * 1.15, z = z0 + sz * i * 1.15; after(i * .06, () => { ipfx(S.pf, x, z, 2.2); spark(x, .3, z, { n: 3, color: S.c, spd: 2, up: 3, size: .25, life: .4 }); inCircle(x, z, 1.2, q => { if (hit.has(q)) return; hit.add(q); bagHit(W2, q, 1.8, { fx: x, fz: z, kb: 2.5 }); }); }); }
    shake(.2); sfx('boom', .6, 1.3); return a; },
  tornado(W, S) { const m = bagNear(9); if (!m) return false; const x0 = HERO.pos.x, z0 = HERO.pos.z, a = dirTo(m), sx = Math.sin(a), sz = Math.cos(a), pos = { x: x0, z: z0 }, W2 = bagW(W, { burn: (W.burn || 0) + (S.burn || 0) }); ipfx(S.pf, pos.x, pos.z, 2.4, { follow: pos, dur: 2.5 });
    for (let k = 1; k <= 12; k++) after(k * .2, () => { const d = k * .2 * 3.6, w = Math.sin(k * .9) * .8; let x = x0 + sx * d + sz * w, z = z0 + sz * d - sx * w; const L = Math.hypot(x, z), mx = ARENA - .8; if (L > mx) { x *= mx / L; z *= mx / L; } pos.x = x; pos.z = z;
      inCircle(x, z, 1.6, q => { bagHit(W2, q, .42, { kb: 0 }); if (!q.boss) { q.x += (x - q.x) * .3; q.z += (z - q.z) * .3; } }); spark(x, .4, z, { n: 3, color: S.c, spd: 2.5, up: 2, size: .24, life: .4 }); });
    sfx('whoosh', .8, .7); return a; },
  blades(W, S) { const dur = S.dur || 2, P = HERO.pos; ipfx(S.pf, P.x, P.z, 2.8, { follow: P, dur: Math.min(dur, 1.4) }); ring(P, S.c, .4, 2.8, .4, .7); const n = Math.round(dur / .22);
    for (let k = 0; k < n; k++) after(k * .22, () => { if (HERO.dead) return; const Q = HERO.pos, b = k * 1.3; bagFx(() => { arcFx(Q.x, Q.z, b, 2.4, S.c, .22, k % 2 ? 1 : -1); arcFx(Q.x, Q.z, b + Math.PI, 2.4, S.c, .22, k % 2 ? 1 : -1); }); inCircle(Q.x, Q.z, 2.6, q => bagHit(W, q, .38, { fx: Q.x, fz: Q.z, kb: 1.2 })); if (k % 3 === 0) sfx('slash', .4, 1.4); });
    return true; },
  rain(W, S) { const t = bagDense(10, 3) || bagNear(10); if (!t) return false; const cx = t.x, cz = t.z, n = S.count || 10; bagFx(() => decal('target', cx, cz, 6, S.c, 0xffffff, { life: 1.4 }));
    for (let i = 0; i < n; i++) after(.15 + i * .08, () => { const r = Math.sqrt(Math.random()) * 2.8, b = Math.random() * TAU, x = cx + Math.cos(b) * r, z = cz + Math.sin(b) * r; ipfx(i % 2 && S.pf2 ? S.pf2 : S.pf, x, z, 1.6); column({ x, z }, S.c, .25, .12, 4); inCircle(x, z, 1.0, q => bagHit(W, q, .6, { fx: x, fz: z, kb: 1 })); if (i % 3 === 0) sfx('slash', .3, 1.6); });
    return true; },
  void(W, S) { const t = bagDense(10, 3) || bagNear(10); if (!t) return false; const x = t.x, z = t.z, W2 = bagW(W, { poi: (W.poi || 0) + 1 }); ipfx(S.pf, x, z, 3.2); bagFx(() => decal('sigil', x, z, 4.5, S.c, 0x200030, { life: 1.4 }));
    for (let k = 0; k < 8; k++) after(k * .1, () => { for (const q of MON) { if (q.dead || q.boss) continue; const dx = x - q.x, dz = z - q.z, d = Math.hypot(dx, dz); if (d < 5 && d > .3) { const s = Math.min(d - .3, .45); q.x += dx / d * s; q.z += dz / d * s; } } });
    after(1.0, () => { if (HERO.dead) return; bagBoom(W2, x, z, 2.8, 2.2, { c: S.c, kb: 4 }); if (S.pf2) ipfx(S.pf2, x, z, 3); shake(.4); FLASH.w = Math.max(FLASH.w, .3); sfx('boom', 1, .6); }); sfx('whoosh', .8, .5); return true; },
  quake(W, S) { const P = HERO.pos, x0 = P.x, z0 = P.z, W2 = bagW(W, { stun: Math.max(W.stun || 0, .8) }); ipfx(S.pf, x0, z0, 4.2);
    for (let i = 0; i < 6; i++) { const b = i * TAU / 6, x = x0 + Math.cos(b) * 2.4, z = z0 + Math.sin(b) * 2.4; after(.08 + i * .04, () => { if (S.pf2) ipfx(S.pf2, x, z, 1.8); spark(x, .3, z, { n: 4, color: 0xc8a878, spd: 3, up: 4, size: .28, life: .5 }); }); }
    after(.1, () => { if (HERO.dead) return; bagBoom(W2, x0, z0, 3.4, 1.6, { c: S.c, kb: 4.5 }); ring({ x: x0, z: z0 }, S.c, .5, 4, .5, .9); shake(.5); }); sfx('boom', 1, .7); return true; },
  blood(W, S) { const P = HERO.pos, n = S.count || 4, list = MON.filter(q => !q.dead && (q.x - P.x) ** 2 + (q.z - P.z) ** 2 < 49).sort((p, q) => ((p.x - P.x) ** 2 + (p.z - P.z) ** 2) - ((q.x - P.x) ** 2 + (q.z - P.z) ** 2)).slice(0, n); if (!list.length) return false; let tot = 0;
    list.forEach((q, i) => after(i * .08, () => { if (q.dead || HERO.dead) return; const Q = HERO.pos; tot += bagHit(W, q, 1.5, { fx: Q.x, fz: Q.z, kb: 1.5 }) || 0; ipfx(S.pf, q.x, q.z, 1.8); bagLine(Q.x, Q.z, Math.atan2(q.x - Q.x, q.z - Q.z), Math.hypot(q.x - Q.x, q.z - Q.z), 0xff3c5a, .08); }));
    after(n * .08 + .1, () => { const h = Math.round(Math.min(tot * (S.heal || .3), HERO.max * .2)); if (h > 0 && !HERO.dead) { healHero(h); num(HERO.pos.x, 2.2, HERO.pos.z, '+' + h, '#ff8aa0'); } }); sfx('slash', .7, .8); return true; },
  frost(W, S) { const t = bagDense(10, 2.5) || bagNear(10); if (!t) return false; const x = t.x, z = t.z, W2 = bagW(W, { stun: Math.max(W.stun || 0, 1.1) }); ipfx(S.pf, x, z, 3, { dur: 2 }); bagFx(() => decal('pool', x, z, 5.2, S.c, 0xffffff, { life: 2.2 })); ring({ x, z }, S.c, .5, 3, .55, 1); spark(x, .5, z, { n: 14, color: 0xe8f8ff, spd: 3, up: 4, size: .28, life: .6 });
    for (let k = 0; k < 4; k++) after(.15 + k * .45, () => { if (HERO.dead) return; inCircle(x, z, 2.6, q => bagHit(W2, q, .55, { fx: x, fz: z, kb: 0 })); if (k === 0 && S.pf2) ipfx(S.pf2, x, z, 2.6); }); sfx('chime', .7, 1.4); return true; },
  poison(W, S) { const t = bagDense(10, 2.5) || bagNear(10); if (!t) return false; const x = t.x, z = t.z; ipfx(S.pf, x, z, 2.6, { dur: 3 }); if (S.pf2) ipfx(S.pf2, x, z, 2.4); bagFx(() => decal('pool', x, z, 5, S.c, 0x203010, { life: 3.2 }));
    for (let k = 0; k < 8; k++) after(.2 + k * .4, () => { if (HERO.dead) return; inCircle(x, z, 2.5, q => { bagHit(W, q, .3, { fx: x, fz: z, kb: 0 }); if (!q.dead) q.poi = Math.min((q.poi || 0) + Math.max(1, (W.poi || 0) + (W.dmg || 3) * .15), (W.dmg || 4) * 3); }); }); sfx('whoosh', .6, .6); return true; },
  crit(W, S) { const m = bagTop(8); if (!m) return false; const W2 = bagW(W, { crit: 1 }); G.slow = Math.max(G.slow || 0, .25);
    after(.12, () => { if (m.dead || HERO.dead) return; ipfx(S.pf, m.x, m.z, 2.6); if (S.pf2) ipfx(S.pf2, m.x, m.z, 2.2); bagHit(W2, m, S.mul || 3, { kb: 4 }); ring(m, S.c, .3, 2.2, .35, 1); shake(.4); FLASH.w = Math.max(FLASH.w, .35); sfx('slash', 1, .7); }); return dirTo(m); },
  guard(W, S) { const P = HERO.pos, H = HERO, b = (W.blk || 4) * 2.5, th = (W.blk || 4) * (S.thorn || 1); BAG.blk = Math.min(H.max * .8, BAG.blk + b); ipfx(S.pf, P.x, P.z, 2.4, { follow: P, dur: 1.6 }); ring(P, S.c, .6, 2.8, .5, .9); num(P.x, 2.4, P.z, 'โล่ +' + Math.round(b), '#bfe4ff');
    after(.15, () => { if (!HERO.dead) inCircle(HERO.pos.x, HERO.pos.z, 2.6, q => bagHit(bagW(W, { dmg: th }), q, 1, { fx: HERO.pos.x, fz: HERO.pos.z, kb: 3.5 })); }); sfx('chime', .8, .9); return true; },
  feast(W, S) { const P = HERO.pos, H = HERO; if (H.hp >= H.max * .97) return false; const tot = (W.heal || 3) * 1.8, n = 6; ipfx(S.pf, P.x, P.z, 2, { follow: P, dur: 2.4 });
    for (let k = 0; k < n; k++) after(k * .4, () => { if (HERO.dead) return; healHero(tot / n); spark(HERO.pos.x, .4, HERO.pos.z, { n: 3, color: S.c, spd: .8, up: 3, grav: 1, size: .22, life: .6 }); }); num(P.x, 2.4, P.z, '+' + Math.round(tot), '#9fe870'); sfx('chime', .7, 1.2); return true; },
};
const BAG_ISKP = .7;   /* skill damage in the swarm: area skills against a horde are strong (all rounds to 15 were won at 1.0) */
function bagIskPrep(items) { if (Q.get('isk') === '0') return;   /* ?isk=0 = no item skills (balance comparisons) */ for (const W of items) { const S = typeof iskOf === 'function' ? iskOf(W.id, W.base) : null; if (!S || W.once) continue; W.isk = S; W.iskE = iskEvery(S, W); W.iskN = 0; for (const p of [S.pf, S.pf2]) if (p) loadPfx(p); } }
function bagIskUse(W) { if (!W.isk || HERO.dead) return; if (++W.iskN < W.iskE) return; W.iskN = 0; const S = W.isk, K = BAGISK[S.k]; if (!K) return; const r = K(bagW(W, { dmg: (W.dmg || 0) * BAG_ISKP }), S); if (r === false) { W.iskN = W.iskE - 1; return; }
  const P = HERO.pos, hex = '#' + S.c.toString(16).padStart(6, '0'); num(P.x, 2.3, P.z, '✦ ' + S.n, hex, true); W.fl = .6; W.isf = .8; bagPop(W);
  ring(P, S.c, .3, 2.6, .45, .9); spark(P.x, 1, P.z, { n: 12, color: S.c, spd: 3.5, up: 5, size: .32, life: .55 }); bagFx(() => decal('sigil', P.x, P.z, 2.8, S.c, 0xffffff, { life: .8 })); if (!(BAG.iskSw > BAG.t)) { BAG.iskSw = BAG.t + 1.6; bagSwing('skill', null); }   /* the champion casts it (the class skill move, at most every 1.6 s so it keeps walking): a ring and a sign at the feet, the class's skill move */
  (BAG.calls || (BAG.calls = [])).push({ n: S.n, c: hex, ic: W.ic, t: 0 }); if (BAG.calls.length > 3) BAG.calls.shift(); if (typeof bagCheer === 'function') bagCheer(.12); BAG.iskUsed = (BAG.iskUsed || 0) + 1; }
/* ---- DUELS IN THE ARENA (owner 2026-11-28 "รอบคนสู้กัน ให้ทำแบบมอนเลย": every fight in the 3D arena, no side view). bag3d.html sends cfg.rv = the
   rival's numbers in the same shape as ours (its bag built by rivalMake / rivalFoe, its Tripo body = HEROES[cls]). The duel is TWO SIDES of the same
   engine: each side has its champion (HERO), what its items can hit (MON = the other champion as a stand-in object, `champ`), its own shots / zones
   (PROJ, ZONES), its bag numbers (BAG.st, its, sta, blk, sk ...) and its P numbers. bagWith(side, fn) swaps all of that in, runs fn, swaps it back, so
   every BAGFIRE move, item skill, element and whole-bag effect works for the rival exactly as for us. hitMon on a stand-in goes to bagChampHit ->
   the victim's side: armour (physical, minus shield pierce), magic resist (magic), dodge, the shield, counter / thorns / chill (no counter of a counter),
   then the life. Statuses on a champion: stun (frzT, at most 1.2 s a hit), slow, burn, poison, frog (hex), silence (no skill gauge), knock-back (small).
   Win = the rival falls; from 28 s both lose (t - 28) x 0.8 life a second (the side view's fatigue); at 90 s the one with less life share falls. */
const SIDES = []; let CUR = null;
const SIDEF = ['st', 'its', 'sta', 'blk', 'sk', 'anim', 'skull', 'potion', 'blT', 'ssT', 'lpT', 'critT', 'iskSw', 'calls', 'iskUsed', 'reach', 'cname', 'ty', 'tk', 'spT', 'rtT', 'mv0', 'allies'], SIDEP = ['pow', 'crit', 'critX', 'steal', 'numMin', 'armor', 'spd', 'regen', 'area'];
function bagSwap(s) { const c = CUR; for (const k of SIDEF) c.b[k] = BAG[k]; for (const k of SIDEP) c.p[k] = P[k]; c.hero = HERO; c.rev = G.revive; c.mon = MON; c.proj = PROJ; c.zones = ZONES;
  for (const k of SIDEF) BAG[k] = s.b[k]; for (const k of SIDEP) P[k] = s.p[k]; HERO = s.hero; G.revive = s.rev; MON = s.mon; PROJ = s.proj; ZONES = s.zones; CUR = s; regrid(); }
function bagWith(s, fn) { if (!s || s === CUR || !BAG.duel) return fn(); const o = CUR; bagSwap(s); try { return fn(); } finally { bagSwap(o); } }
function bagOnSide(fn) { const s = CUR; return () => bagWith(s, fn); }   /* horde.html after(): a timer runs on the side that set it */
/* the rival bodies: the five Tripo champions of horde.html (HEROES archer / wing / demon / dark / hood), kept out of HCACHE so showHero leaves them alone */
const RVM = {}, BAGRVCLIPS = ['Melee_2H_Attack_Chop', 'Melee_2H_Attack_Slice', 'Melee_2H_Attack_Spin', 'Melee_2H_Idle', 'Melee_Block_Attack', 'Melee_1H_Attack_Slice_Diagonal', 'Dodge_Forward'];
function bagRivalModel(k) { if (RVM[k]) return Promise.resolve(RVM[k]); const D = HEROES[k]; if (!D) return Promise.reject(new Error('no rival body ' + k)); if (RVM['p_' + k]) return RVM['p_' + k];
  D.atks = [...new Set(D.atks.concat(HEROES.wolf.atks, BAGRVCLIPS))];   /* every clip the bag moves play */
  return RVM['p_' + k] = loadHeroModel(k).then(M => { delete HCACHE[k]; M.T.root.scale.multiplyScalar(1.15); RVM[k] = M; return M; }, e => { delete RVM['p_' + k]; throw e; }); }
let RRING = null;
function bagProxy(sd) {   /* the champion of side sd as the other side sees it: a monster-like object whose place / life ARE the champion's */
  const m = { champ: sd, K: { hgt: 1.75, bsc: 1, rad: .45 }, sc: 1, y: 0, r: .45, kx: 0, kz: 0, slowT: 0, slowK: 1, frzT: 0, burnT: 0, burnD: 0, atkT: 0, flash: 0, elite: false, boss: true, poi: 0, fr: 0, row: 0, flip: 1, seed: 1, spd: 3, stfx: {} };
  Object.defineProperties(m, { x: { get: () => sd.hero.pos.x, set: v => { sd.hero.pos.x = v; } }, z: { get: () => sd.hero.pos.z, set: v => { sd.hero.pos.z = v; } },
    hp: { get: () => sd.hero.hp, set: v => { sd.hero.hp = v; } }, max: { get: () => sd.hero.max, set: () => { } }, dead: { get: () => sd.hero.dead, set: () => { } } }); return m; }
function bagDuelSetup(cfg) {   /* side 1 = the rival: its body, both stand-ins, its numbers; the two face each other across the sand */
  const R = { k: 1, b: {}, p: {}, hero: makeHero(RVM[cfg.rv.cls]), mon: [], proj: [], zones: [], me: null, rev: 0 }, A = SIDES[0]; SIDES.push(R); BAG.duel = true;
  A.me = bagProxy(A); R.me = bagProxy(R); MON.push(R.me); R.mon.push(A.me); bagWith(R, () => bagSideInit(cfg.rv));
  HERO.pos.set(-3.2, 0, 2); HERO.face = Math.PI / 2; R.hero.pos.set(3.2, 0, 2); R.hero.face = -Math.PI / 2; const M = R.hero.M;   /* on the sun medallion, under the banner */
  { const mat = M.T.mat; if (mat && !mat.userData.c0) mat.userData.c0 = mat.color.clone(); if (mat) { if (M.D.file && M.D.file === HERO.D.file) mat.color.copy(mat.userData.c0).multiply(new THREE.Color(1.15, .62, .62)); else mat.color.copy(mat.userData.c0); } }   /* the same body as ours (the knight class vs the demon knight rival): the rival in a blood-red shade */ if (!M.T.root.parent) { scene.add(M.T.root); if (M.str) scene.add(...M.str.rods); } chPlay(M, 'U', M.idle); chPlay(M, 'L', M.idle); M.mixer.update(0);
  if (!RRING && !NORENDER) { RRING = new THREE.Mesh(GEO.plane, new THREE.MeshBasicMaterial({ map: TEX.disc, color: 0xff6a5a, transparent: true, opacity: .6, depthWrite: false, fog: false })); RRING.scale.set(1.3, 1, 1.3); RRING.position.y = .05; RRING.renderOrder = 2; scene.add(RRING); } if (RRING) RRING.visible = true;
  BAG.rname = cfg.rv.cname || 'คู่แข่ง'; BAG.rcls = cfg.rv.clsn || ''; BAG.plan = []; BAG.pi = 0; BAG.total = 1; BAG.dur = 28; BAG.kinds = []; BAG.fk = 1; return []; }
function bagDuelOff() {   /* back to one side (before every fight, and on 'stop') */
  if (SIDES[0] && CUR && CUR !== SIDES[0]) bagSwap(SIDES[0]); const R = SIDES[1]; if (R) { const M = R.hero.M; scene.remove(M.T.root); if (M.str) scene.remove(...M.str.rods); for (const p of R.proj) if (p.mesh) { scene.remove(p.mesh); freeDecal(p.mesh); } R.proj.length = 0; R.zones.length = 0; } if (RRING) RRING.visible = false;
  if (SIDES[0]) { MON = SIDES[0].mon; PROJ = SIDES[0].proj; ZONES = SIDES[0].zones; } SIDES.length = Math.min(SIDES.length, 1); BAG.duel = false; }
function bagChampHit(m, dmg, o) {   /* (attacker's side) one hit on the other champion */
  const V = m.champ, A = CUR; if (!BAG.duel || !V || V === A || V.hero.dead || BAG.done || G.state !== 'play') return 0;
  const d = Math.max(1, dmg * (P.pow || 1) * (o.tru ? 1 : BAG_DUEL.dmg) * rnd(.92, 1.08)), X = BAG.st.gx || {}, ty = o.ty || 'phy', q = { ty, pc: o.pc || 0, ap: X.apierce && ty !== 'mag' ? .5 : 0, mp: X.mpierce && ty === 'mag' ? .3 : 0, ref: o.ref, dot: o.dot, tru: o.tru, crit: !!o.crit, color: o.color };
  if (!o.dot) { if (o.slow) { m.slowT = Math.max(m.slowT, (o.slowT || 2) * .8); m.slowK = Math.min(m.slowK, 1 - Math.min(.6, o.slow) * .8); } if (o.frz) m.frzT = Math.max(m.frzT, Math.min(1.2, o.frz)); if (o.burn) { m.burnT = 3; m.burnD = Math.max(m.burnD || 0, o.burn); }
    if (o.kb) { const dx = m.x - (o.fx !== undefined ? o.fx : A.hero.pos.x), dz = m.z - (o.fz !== undefined ? o.fz : A.hero.pos.z), L = Math.hypot(dx, dz) || 1; m.kx += dx / L * o.kb * .35; m.kz += dz / L * o.kb * .35; } }
  const dealt = bagWith(V, () => bagChampHurt(d, A.me, q)); if (dealt > 0) { m.flash = 1; if (A.k === 0) { G.dealt += dealt; if (o.w) STATS[o.w] = (STATS[o.w] || 0) + dealt; } } return dealt; }
function bagChampHurt(d, src, q) {   /* (victim's side) armour, resist, dodge, the shield ... then the life */
  const H = HERO, S = BAG.st; if (H.dead || BAG.done) return 0; if (H.inv > 0 && !q.dot) return 0;
  if (!q.dot && !q.tru && q.ty !== 'mag') d = Math.max(1, d - (S.armor || 0) * (1 - Math.min(.9, (q.pc || 0) + (q.ap || 0))));
  d = bagHurt(d, src, q); if (!(d > 0)) return 0; d = Math.max(1, Math.round(d)); H.hp -= d; H.hurtT = .2; const P0 = H.pos;
  if (CUR.k === 0) { FLASH.r = Math.min(.5, FLASH.r + (q.dot ? .03 : .1)); G.taken += d; num(P0.x, 1.8, P0.z, '-' + d, q.crit ? '#ffb030' : q.dot ? '#e8a0ff' : '#ff6a5a', q.crit || d >= H.max * .08); if (!q.dot) shake(.05); }
  else num(P0.x, 1.9, P0.z, d, q.crit ? '#ffe14a' : q.dot ? '#e0c0ff' : (q.color || '#fffaf0'), q.crit);
  if (H.hp <= 0) bagChampDown(); return d; }
function bagChampDown() {   /* (that side) the revive stone, or the champion falls */
  const H = HERO; if (G.revive > 0) { G.revive--; H.hp = Math.round(H.max * .4); H.inv = 1.5; mfx('revive', H.pos.x, H.pos.z, 2.6, { pri: 1 }); num(H.pos.x, 2.3, H.pos.z, 'ฟื้นคืนชีพ!', '#ffe9a0', true); sfx('lvl', .7, .8); return; }
  H.hp = 0; H.dead = true; chPlay(H.M, 'U', 'Death_A', true); chPlay(H.M, 'L', 'Death_A', true); mfx('ko', H.pos.x, H.pos.z, 3.4, { pri: 1 }); shake(.4); sfx('boom', .8, .7);
  if (CUR.k === 0) { G.endT = 1.8; G.won = false; BAG.done = true; setMusic('calm'); jingle('lose'); const R = SIDES[1].hero; chPlay(R.M, 'U', 'Cheer', true, 1.2); chPlay(R.M, 'L', 'Cheer', true, 1.2); R.atkT = R.dodgeT = 3; R.apr = 9; banner('แพ้...', BAG.rname + ' ชนะการดวล', true, 1.6); } }
const BAG_STFX = [['frzT', 'st_shock'], ['burnT', 'st_burn'], ['poi', 'st_poison'], ['slowT', 'st_chill']];
function bagChampSt(sd, dt) {   /* the statuses on one champion tick down (its stand-in holds them); burn hurts every .5 s; knock-back slides */
  const m = sd.me, H = sd.hero; if (!m) return; if (m.frzT > 0) m.frzT -= dt; if (m.slowT > 0) { m.slowT -= dt; if (m.slowT <= 0) m.slowK = 1; } if (m.atkT > 0) m.atkT -= dt; m.flash = Math.max(0, m.flash - dt * 7);
  if (m.kx || m.kz) { H.pos.x += m.kx * dt; H.pos.z += m.kz * dt; const f = Math.exp(-7 * dt); m.kx *= f; m.kz *= f; if (Math.abs(m.kx) + Math.abs(m.kz) < .05) m.kx = m.kz = 0; }
  if (H.dead) return; const O = SIDES[1 - sd.k];
  if (m.burnT > 0) { m.burnT -= dt; m.burnK = (m.burnK || 0) - dt; if (m.burnK <= 0) { m.burnK = .5; bagWith(O, () => hitMon(m, m.burnD, { w: 'burn', color: '#ffb070', dot: 1 })); } }
  if (!NORENDER) for (const [k, fx] of BAG_STFX) { if (!(m[k] > 0)) continue; if (m.stfx[k] > BAG.t) continue; m.stfx[k] = BAG.t + .9; mfx(fx, H.pos.x, H.pos.z, k === 'frzT' ? 1.3 : 1.1, { dur: .95, follow: H.pos, y: k === 'frzT' ? 2.1 : 1.2 }); } }
function bagHero2(dt) {   /* (tick, after our champion moved) both statuses, the rival walks and its shots fly; the rings under both */
  const R = SIDES[1]; if (!R) return; for (const sd of SIDES) bagChampSt(sd, dt);
  bagWith(R, () => { if (!HERO.dead && G.endT <= 0 && G.state === 'play' && BAG.t > .7) bagDuelAuto(dt); else INP.x = INP.z = 0; updHero(dt); updProj(dt); });
  HRING.position.x = HERO.pos.x; HRING.position.z = HERO.pos.z; if (RRING) { RRING.position.x = R.hero.pos.x; RRING.position.z = R.hero.pos.z; RRING.visible = !R.hero.dead; } }
function bagDuelAuto(dt) {   /* how a champion moves in a duel: melee walks in to its reach; ranged and mages keep their distance (back off slowly, circle a little) */
  const H = HERO.pos, me = CUR.me, o = MON[0]; if (!o || o.dead || !me || me.frzT > 0 || me.hexT > BAG.t) { INP.x = INP.z = 0; return; }
  const dx = o.x - H.x, dz = o.z - H.z, d = Math.hypot(dx, dz) || 1, ux = dx / d, uz = dz / d; let fx = 0, fz = 0;
  if (BAG.ty === 'mel') { if (d > BAG.reach) { fx = ux; fz = uz; } }
  else { const near = 3.4, far = 6.8; if (d < near) { fx = -ux * BAG_DUEL.back; fz = -uz * BAG_DUEL.back; } else if (d > far) { fx = ux; fz = uz; } const sw = Math.sin(BAG.t * .8 + CUR.k * 2.1) * BAG_DUEL.circle; fx += -uz * sw; fz += ux * sw; }
  const R = Math.hypot(H.x, H.z), eg = 1.4; if (R > ARENA - eg) { const k = (R - ARENA + eg) / eg, tx = -H.z / R, tz = H.x / R, sg = fx * tx + fz * tz >= 0 ? 1 : -1; fx = fx * (1 - k) + (tx * sg - H.x / R * .5) * k; fz = fz * (1 - k) + (tz * sg - H.z / R * .5) * k; }   /* at the wall: slide along it */
  const L = Math.hypot(fx, fz), sl = me.slowT > 0 ? me.slowK : 1; if (L < .06) INP.x = INP.z = 0; else { const f = Math.min(1, L) / L * sl; INP.x = fx * f; INP.z = fz * f; } }
const BAG_DUEL = { back: .75, circle: .35, tmax: 90, dmg: .6 };   /* ranged back-off speed (share of a walk), how much they circle, the time limit, damage share (1.0 ended duels in 5 s: the item skills + reactions hit on top of the side view's numbers; .6 = about 9 s like the side view) */
function bagDuelUpd(dt) {   /* (our side) fatigue and the time limit */
  const R = SIDES[1]; if (!R || BAG.done) return;
  if (BAG.t > BAG.dur) { if (!BAG.raged) { BAG.raged = true; banner('เหนื่อยล้า!', 'เกิน 28 วิ: ทั้งคู่เสียเลือดทุกวิ', true, 1.8); } BAG.fk -= dt; if (BAG.fk <= 0) { BAG.fk = 1; const f = (BAG.t - BAG.dur) * .8; for (const sd of SIDES) if (!sd.hero.dead) bagWith(SIDES[1 - sd.k], () => hitMon(sd.me, f, { w: 'tired', dot: 1, tru: 1, color: '#ff9a8a' })); } }
  if (BAG.t > BAG_DUEL.tmax && !HERO.dead && !R.hero.dead) { const lo = HERO.hp / HERO.max >= R.hero.hp / R.hero.max ? R : SIDES[0]; bagWith(lo, () => { G.revive = 0; HERO.hp = 0; bagChampDown(); }); } }
function bagDrawAll(fn) { const R = SIDES[1]; if (!R || CUR !== SIDES[0]) return fn(); const p0 = PROJ; PROJ = p0.concat(R.proj); try { fn(); } finally { PROJ = p0; } }   /* the drawing sees both sides' shots */
/* ---- start / end */
function bagStart(cfg) {
  mfxInit(); if (!NORENDER && MFX.on) for (const k of ['crit', 'slam', 'spin', 'slash', 'meteor', 'bolt', 'pillar', 'blood', 'heal', 'guard', 'nova', 'void', 'frost', 'blizzard', 'poisoncloud', 'tornado', 'rain', 'spikes', 'react_shock', 'react_overload', 'react_gas', 'curse', 'blaze', 'ko', 'bossin', 'victory', 'aura', 'arrowfan', 'shieldbash', 'venomslash']) mfxTex(k);   /* load the painted effects before the fight needs them */
  if (!BAG.ready || !HERO) return false;
  if (cfg.rv && !RVM[cfg.rv.cls]) {   /* a duel: the rival's body loads first (bag3d.html asks for it while the shop is open: bag 'pre') */
    BAG.cfg = cfg; BAG.on = true; G.state = 'load'; LOAD.msg = 'คู่แข่งกำลังเข้าสนาม...'; LOAD.f = .6;
    bagRivalModel(cfg.rv.cls).catch(() => { cfg.rv.cls = cfg.rv.cls === 'wing' ? 'demon' : 'wing'; return bagRivalModel(cfg.rv.cls); }).then(() => { if (BAG.cfg === cfg) bagStart(cfg); }, e => { console.error(e); if (BAG.cfg === cfg) { G.won = true; bagFinish(); } }); return true; }
  CAM.zoom = bagIsArena() ? .74 : 1.22; if (bagIsArena()) CAM.dir.copy(CAM.arenaDir); resize();   /* the arena: a little farther back, so its stands are on screen */ audioInit(); bagDuelOff(); clearRun();   /* closer than the survival game: the champion and the item effects read bigger */ const M = HERO.M; HERO = makeHero(M); showHero(M); BAG.cfg = cfg; BAG.result = null; BAG.on = true; BAG.done = BAG.raged = BAG.bossed = false; BAG.bossWait = false; BAG.t = 0; BAG.man = 0;
  BAG.spd = cfg.spd > 1 ? 2 : 1; BAG.icr = cfg.icr || 14; SIDES.length = 0; SIDES.push(CUR = { k: 0, b: {}, p: {}, hero: HERO, mon: MON, proj: PROJ, zones: ZONES, me: null, rev: 0 });
  bagSideInit(cfg); BAG.hpShow = HERO.hp; G.seed = (Math.random() * 1e9) | 0; G.hpMul = G.dmgMul = G.rateMul = 1; G.pend = 0; G.hk = HERO.k;
  const kinds = cfg.rv ? bagDuelSetup(cfg) : bagWave(cfg.round, !!cfg.boss); DIR.cur = kinds; kinds.forEach(loadKind); if (cfg.boss) loadKind(MAP.boss[Math.max(0, Math.min(3, Math.floor(cfg.round / 5) - 1)) % MAP.boss.length]);
  CAM.look.set(0, 0, 0); INP.x = INP.z = 0; JOY.on = false; G.state = 'load'; LOAD.msg = cfg.rv ? 'คู่แข่งกำลังเข้าสนาม...' : 'กำลังเรียกฝูงมอน...'; LOAD.f = .6;
  Promise.all(kinds.map(loadKind)).then(() => { if (BAG.cfg !== cfg) return; G.state = 'play'; for (const sd of SIDES) bagWith(sd, () => { const M = HERO.M, d = chPlay(M, 'U', 'Spawn_Ground', true, 1.5); chPlay(M, 'L', 'Spawn_Ground', true, 1.5); HERO.atkT = HERO.dodgeT = Math.min(.8, d || 0); HERO.apr = 9; });   /* the champion rises out of the ground */ setMusic(MAP.music === 'calm' ? 'battle' : MAP.music);
    if (cfg.rv) { banner('⚔ ดวลผู้เล่น', BAG.rname + ' · ' + (cfg.rv.clsn || ''), true, 2); mfx('clash', 0, 2, 5, { pri: 1 }); bagCheer(1.2, true); sfx('boom', .7, .8); } else banner(cfg.boss ? 'รอบ ' + cfg.round + ' · บอส' : 'รอบ ' + cfg.round, cfg.name || '', !!cfg.boss, 1.8); }); return true;
}
function bagSideInit(cfg) {   /* one champion's numbers from its cfg, on the side now in play (a duel calls it for the rival too) */
  const S = BAG.st = Object.assign({ armor: 0, mres: 0, dodge: 0, regen: 0, thorn: 0, haste: 0, crit: 0, critd: 2, stam: 5, sreg: 1, rage: 0, sblk: 0 }, cfg.st || {});
  Object.assign(P, { pow: 1, cd: 1, area: 1, spd: 3.3, magnet: 2.4, crit: 0, critX: 2, armor: S.armor, regen: S.regen, xp: 0, gold: 1, luck: 1, multi: 0, dur: 1, steal: 0, numMin: 0 }); HERO.max = Math.round(cfg.hp); HERO.hp = HERO.max; BAG.blk = S.sblk || 0; BAG.sta = S.stam; BAG.tk = .5; BAG.ty = cfg.ty || null;
  BAG.calls = []; BAG.iskSw = 0; BAG.critT = 0; BAG.its = (cfg.items || []).map(q => { const W = Object.assign({ t: Math.random() * .4, fl: 0 }, q); if (W.start != null) { W.once = true; W.dmg = W.start; } else if (W.blk || W.heal) W.self = true; return W; }); bagIskPrep(BAG.its); BAG.iskUsed = 0;
  const melee = BAG.its.some(W => !W.once && !W.self && ['stab', 'xcut', 'thrust', 'bonk', 'claws', 'reap', 'cut', 'cleave'].includes((BAGMOVE[W.id] || BAGMOVE[W.base] || ['cut'])[0])); BAG.reach = melee ? 1.8 : 5.5;
  BAG.sk = cfg.sk ? { n: cfg.sk.n, cd: cfg.sk.cd, pw: cfg.sk.pw, g: cfg.sk.cd * .4, kind: cfg.sk.kind, w: cfg.sk.w } : null; BAG.cname = cfg.cname || ''; BAG.anim = Object.assign({}, BAGCLSANIM[cfg.cls] || {});
  if (cfg.cls && typeof BAGCLS !== 'undefined' && BAGCLS[cfg.cls]) BAG.anim.skill = [BAGCLS[cfg.cls].anim.skill.slice(-1), .8, 3];   /* the class's own skill move */ G.revive = cfg.st && cfg.st.gx && cfg.st.gx.revive ? 1 : 0; BAG.potion = 0; BAG.skull = 0; BAG.blT = BAG.ssT = BAG.lpT = 0; if (cfg.st && cfg.st.mspd) P.spd *= 1 + cfg.st.mspd; if (cfg.ty === 'mel') P.spd *= 1.15;   /* melee walks 15 % faster */   /* revive stone, boots */
  BAG.mv0 = P.spd; BAG.spT = BAG.rtT = 0; BAG.allies = []; if (BAG.its.some(W => W.mv === 'skel' || W.id === 'sp_skel')) loadKind(BAG_SKEL);   /* the skeleton warriors' card loads before the fight needs it */
}
function bagFinish() {   /* the wave is cleared or the champion fell: tell bag3d.html */
  const left = aliveN() + BAG.plan.slice(BAG.pi).reduce((s, p) => s + p.n, 0), r = { bag: 'end', win: !!G.won && !HERO.dead, t: +BAG.t.toFixed(1), kills: G.kills, total: BAG.total, left, coins: G.coins, hp: Math.max(0, Math.round(HERO.hp)), dmg: Object.assign({}, STATS) };
  if (BAG.duel && SIDES[1]) { const R = SIDES[1].hero; r.duel = 1; r.rhp = Math.max(0, Math.round(R.hp)); r.rmax = R.max; r.left = R.dead ? 0 : 1; }   /* a duel: the rival's life left */
  BAG.result = r; BAG.on = false; G.state = 'bagdone'; INP.x = INP.z = 0; JOY.on = false; setMusic('calm'); try { if (parent !== window) parent.postMessage(r, '*'); } catch (_) { } }
function bagBoot() { BAG.ready = true; G.state = 'bagidle'; HERO.M.T.root.scale.multiplyScalar(1.15); if (!NORENDER) bagIcons(); try { if (parent !== window) parent.postMessage({ bag: 'ready', map: MAPK === 'arena' ? 'arena:' + (Q.get('land') || 'forest') : MAPK }, '*');   /* the arena answers with its land, so a page of an older land is not taken */ } catch (_) { } if (BAG.wait) { const c = BAG.wait; BAG.wait = null; bagStart(c); } }
function bagIcons() { if (BAG.img) return true; BAG.img = new Image(); BAG.img.src = 'art/bag3d/icons_all.png?v=3'; BAG.tex = TL.load('art/bag3d/icons_all.png?v=3'); BAG.tex.magFilter = THREE.NearestFilter; BAG.tex.encoding = THREE.sRGBEncoding; return true; }
addEventListener('message', e => { const d = e.data; if (!d || !d.bag || !BAGM) return; if (d.bag === 'start') { if (BAG.ready) bagStart(d.cfg); else BAG.wait = d.cfg; } else if (d.bag === 'spd') BAG.spd = d.v > 1 ? 2 : 1; else if (d.bag === 'stop') { BAG.on = false; G.state = 'bagidle'; bagDuelOff(); clearRun(); } else if (d.bag === 'pre' && BAG.ready && HEROES[d.k]) bagRivalModel(d.k).catch(() => { }); });   /* pre = load the next duel rival's body while the shop is open */
window.BAGAPI = { BAG, SIDES, start: c => bagStart(c), fire: bagFire, moves: BAGMOVE, rival: k => bagRivalModel(k), DUEL: BAG_DUEL };
/* ---- drawing: item icons that fly / drop / pop up over the champion (sprites cut from bag3d's icon sheet) */
function bagIcon(ic) { const t = BAG.tex.clone(); t.needsUpdate = true; t.repeat.set(1 / 8, 1 / BAG.icr); t.offset.set((ic % 8) / 8, 1 - (Math.floor(ic / 8) + 1) / BAG.icr); const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false, fog: false })); s.renderOrder = 6; s.userData.ic = ic; return s; }
function bagSprite(ic) { let s = null; for (const q of BAG.spr) if (!q.visible && q.userData.ic === ic) { s = q; break; } if (!s) { if (BAG.spr.length > 40) return null; s = bagIcon(ic); BAG.spr.push(s); scene.add(s); } s.visible = true; s.material.rotation = 0; s.material.opacity = 1; return s; }
function bagPop(W) { if (NORENDER || W.ic == null || !BAG.tex) return; if (BAG.pops.length > 5) { const o = BAG.pops.shift(); o.s.visible = false; } const s = bagSprite(W.ic); if (s) BAG.pops.push({ s, t: 0, off: (BAG.pops.length % 3 - 1) * .5, at: HERO.pos }); }
function bagDrop(W, x, z, life) { if (NORENDER || W.ic == null || !BAG.tex) return; const s = bagSprite(W.ic); if (s) BAG.drops.push({ s, x, z, t: 0, life }); }
function bagDraw() {   /* once a frame, from fillBatches */
  if (!BAG.tex) return; const used = new Set(), now = performance.now(), dt = Math.min(.05, (now - (BAG.lt || now)) / 1000); BAG.lt = now;
  for (const p of PROJ) { if (p.type === 'lance') { for (let q = 0; q < 5; q++) glow(p.x - p.vx * q * .012, p.y, p.z - p.vz * q * .012, .7 - q * .1, q ? p.c : 0xffffff, 1 - q * .17); continue; } if (p.type !== 'toss') continue; if (!p.spr) p.spr = bagSprite(p.ic); if (!p.spr) continue; used.add(p.spr); const z = p.sz || 1; p.spr.position.set(p.x, p.y, p.z); p.spr.scale.set(z, z, 1); p.spr.material.rotation = p.spin ? -p.t * p.spin : p.a - Math.PI * .75; glow(p.x, p.y, p.z, z * 1.1, p.c, .45); }
  for (let i = BAG.pops.length - 1; i >= 0; i--) { const o = BAG.pops[i]; o.t += dt; if (o.t > .42 || !BAG.on) { o.s.visible = false; BAG.pops.splice(i, 1); continue; } used.add(o.s); const k = o.t / .42, pop = k < .25 ? k / .25 * 1.2 : 1.2 - (k - .25) * .27; const at = o.at || HERO.pos; o.s.position.set(at.x + o.off, 1.95 + k * .45, at.z); o.s.scale.set(.6 * pop, .6 * pop, 1); o.s.material.opacity = k > .7 ? (1 - k) / .3 : 1; }
  for (let i = BAG.drops.length - 1; i >= 0; i--) { const o = BAG.drops[i]; o.t += dt; if (o.t > o.life + .1) { o.s.visible = false; BAG.drops.splice(i, 1); continue; } used.add(o.s); const k = Math.min(1, o.t / o.life); o.s.position.set(o.x, .6 + (1 - k * k) * 5, o.z); o.s.scale.set(1.5, 1.5, 1); o.s.material.rotation = -2.4 + k * 2.4; }
  for (const s of BAG.spr) if (s.visible && !used.has(s)) s.visible = false;
}
/* ---- the screen: life + shield + stamina, the wave, the items with their cooldowns, the speed button */
function bagDuelUI(pad) {   /* a duel: the rival's name, class, life + shield at the top; a small bar over each champion; the seconds before fatigue */
  const R = SIDES[1]; if (!R) return; const H = R.hero, w = Math.min(330 * S, SW * .44), x = SW / 2 - w / 2, y = pad, b = R.b; rr(x, y, w, 46 * S, 10 * S); ui.fillStyle = 'rgba(34,8,12,.78)'; ui.fill(); ui.lineWidth = 1.5 * S; ui.strokeStyle = 'rgba(255,150,130,.85)'; ui.stroke();
  txt('⚔ ' + BAG.rname + (BAG.rcls ? ' · ' + BAG.rcls : ''), SW / 2, y + 12 * S, 12.5 * S, '#ffd8c8'); bar(x + 10 * S, y + 23 * S, w - 20 * S, 14 * S, H.hp / H.max, '#ff7a5a', '#b81a2a');
  if (b.blk > 0) { ui.save(); ui.globalAlpha = .85; bar(x + 10 * S, y + 23 * S, (w - 20 * S) * Math.min(1, b.blk / H.max), 5 * S, 1, '#bfe4ff', '#5aa8f0', 'rgba(0,0,0,0)'); ui.restore(); }
  txt(Math.ceil(H.hp) + ' / ' + H.max + (b.blk >= 1 ? '   โล่ ' + Math.round(b.blk) : ''), SW / 2, y + 30.5 * S, 10.5 * S, '#fff', 'center', 800, 'rgba(60,0,0,.8)', 2.5);
  const tl = BAG.dur - BAG.t; txt(tl > 0 ? Math.ceil(tl) + ' วินาที' : 'เหนื่อยล้า', x + w - 9 * S, y + 12 * S, 11 * S, tl > 0 ? '#ffe9a8' : '#ff9a8a', 'right', 700);
  for (const sd of SIDES) { const Q2 = sd.hero; if (Q2.dead) continue; const [sx, sy, ok] = toScreen(Q2.pos.x, 2.3, Q2.pos.z); if (!ok) continue; bar(sx - 24 * S, sy, 48 * S, 5.5 * S, Q2.hp / Q2.max, sd.k ? '#ff7a5a' : '#8ae87a', sd.k ? '#b81a2a' : '#2a9a3a');
    if (sd.me && (sd.me.frzT > 0 || sd.me.hexT > BAG.t)) txt(sd.me.hexT > BAG.t ? 'กบ!' : 'มึน', sx, sy - 9 * S, 10.5 * S, '#ffe08a', 'center', 800, 'rgba(0,0,0,.8)', 2.5); }
}
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
  /* the wave (a duel: the rival's plate) */
  if (BAG.duel) bagDuelUI(pad); else { const left = Math.max(0, BAG.total - G.kills), tw0 = 190 * S, x = SW / 2 - tw0 / 2, y = pad; rr(x, y, tw0, 40 * S, 10 * S); ui.fillStyle = 'rgba(10,14,30,.75)'; ui.fill(); ui.lineWidth = 1.5 * S; ui.strokeStyle = BAG.cfg.boss ? 'rgba(255,150,130,.8)' : 'rgba(255,233,168,.7)'; ui.stroke();
    txt((BAG.cfg.boss ? 'บอส · รอบ ' : 'รอบ ') + BAG.cfg.round + '   เหลือมอน ' + left, SW / 2, y + 14 * S, 13.5 * S, BAG.raged ? '#ff9a8a' : '#fff6dc'); bar(x + 10 * S, y + 26 * S, tw0 - 20 * S, 7 * S, clamp(G.kills / Math.max(1, BAG.total), 0, 1), '#9ae87a', '#3aa83a');
    if (G.boss && !G.boss.dead) { const bw = Math.min(360 * S, SW * .46), by = y + 62 * S; txt(MOBS[G.boss.k].name, SW / 2, by - 9 * S, 13 * S, '#ffb0a0'); bar(SW / 2 - bw / 2, by, bw, 12 * S, G.boss.hp / G.boss.max, '#ff7a5a', '#b81a2a'); } }
  /* coins, AUTO, speed */
  { const rx = SW - pad, y = pad, bh = 30 * S; button('bagspd', rx - 54 * S, y, 54 * S, bh, 'x' + BAG.spd, { c: BLUE, tc: '#fff', ts: 'rgba(0,0,40,.6)', size: 14 * S, fn: () => { BAG.spd = BAG.spd > 1 ? 1 : 2; try { parent.postMessage({ bag: 'spd', v: BAG.spd }, '*'); } catch (_) { } } });
    coinIc(rx - 54 * S - 52 * S, y + bh / 2, 8 * S); txt(String(G.coins), rx - 54 * S - 40 * S, y + bh / 2 + 1, 13 * S, '#ffe08a', 'left'); }
  /* the items of the bag: a strip along the bottom, the dark part is the cooldown, a flash when one fires */
  if (BAG.img && BAG.img.width) { const L = BAG.its, n = L.length, z = Math.min(34 * S, (SW * .62) / Math.max(1, n) - 3 * S), w = n * (z + 3 * S), x0 = SW / 2 - w / 2, y = SH - pad - z; ui.imageSmoothingEnabled = false;
    L.forEach((W, i) => { const x = x0 + i * (z + 3 * S), k = W.once ? (W.done ? 0 : 1) : clamp(W.t / W.cd, 0, 1), col = W.self ? (W.heal ? '#3f8a3a' : '#2f5f98') : W.once ? '#8a6a1e' : W.ty === 'mag' ? '#6a3ad8' : '#a8402e'; rr(x, y, z, z, 6 * S); ui.fillStyle = 'rgba(10,12,24,.8)'; ui.fill(); ui.lineWidth = 1.5 * S; ui.strokeStyle = W.fl > 0 ? '#ffffff' : col; ui.stroke();
      if (W.ic != null) ui.drawImage(BAG.img, (W.ic % 8) * 64, Math.floor(W.ic / 8) * 64, 64, 64, x + 2 * S, y + 2 * S, z - 4 * S, z - 4 * S); if (k < 1 || (W.once && W.done)) { ui.fillStyle = 'rgba(6,8,18,.62)'; ui.fillRect(x + 1, y + 1, z - 2, (z - 2) * (W.once ? 1 : 1 - k)); } else if (!W.self && !W.once && BAG.sta < W.sta) { ui.fillStyle = 'rgba(160,30,20,.4)'; ui.fillRect(x + 1, y + 1, z - 2, z - 2); }
      if (W.fl > 0) { ui.globalAlpha = Math.min(1, W.fl / .25) * .6; ui.fillStyle = '#fff'; ui.fillRect(x, y, z, z); ui.globalAlpha = 1; }
      if (W.isk && W.iskE) { const hx = '#' + W.isk.c.toString(16).padStart(6, '0'), q = W.isf > 0 ? 1 : W.iskN / W.iskE; ui.fillStyle = 'rgba(0,0,0,.6)'; ui.fillRect(x + 2 * S, y + z + 1.5 * S, z - 4 * S, 3 * S); ui.fillStyle = hx; ui.fillRect(x + 2 * S, y + z + 1.5 * S, (z - 4 * S) * q, 3 * S);   /* item skill charge: fills with every use, full = the skill */
        if (W.isf > 0) { W.isf -= dt; ui.save(); ui.shadowColor = hx; ui.shadowBlur = 14 * S; ui.lineWidth = 2.5 * S; ui.strokeStyle = hx; ui.globalAlpha = Math.min(1, W.isf * 2); rr(x - 1.5 * S, y - 1.5 * S, z + 3 * S, z + 3 * S, 7 * S); ui.stroke(); ui.restore(); } } });
    if (BAG.calls && BAG.calls.length) { const fs = 12.5 * S, h = 24 * S; BAG.calls.forEach((o, i) => { o.t += dt; });   /* item skill callouts: icon + name, over the bar */
      BAG.calls = BAG.calls.filter(o => o.t < 1.7); BAG.calls.forEach((o, i) => { const a = clamp(Math.min(o.t / .12, (1.7 - o.t) / .3), 0, 1), pop = o.t < .14 ? 1.18 - o.t / .14 * .18 : 1, yy = y - 10 * S - (BAG.calls.length - 1 - i) * (h + 4 * S) - h;
        ui.font = `800 ${fs}px Kanit, sans-serif`; const tw = ui.measureText('✦ ' + o.n).width, bw = tw + h + 16 * S; ui.save(); ui.globalAlpha = a; ui.translate(SW / 2, yy + h / 2); ui.scale(pop, pop); rr(-bw / 2, -h / 2, bw, h, h / 2); ui.fillStyle = 'rgba(16,8,26,.82)'; ui.fill(); ui.shadowColor = o.c; ui.shadowBlur = 12 * S; ui.lineWidth = 2 * S; ui.strokeStyle = o.c; ui.stroke(); ui.shadowBlur = 0;
        if (o.ic != null) ui.drawImage(BAG.img, (o.ic % 8) * 64, Math.floor(o.ic / 8) * 64, 64, 64, -bw / 2 + 5 * S, -h / 2 + 2 * S, h - 4 * S, h - 4 * S); ui.restore(); ui.save(); ui.globalAlpha = a; txt('✦ ' + o.n, SW / 2 + (h - 4 * S) / 2, yy + h / 2, fs * pop, o.c, 'center', 800, 'rgba(14,6,22,.95)', 3.2 * S); ui.restore(); }); }
    ui.imageSmoothingEnabled = true; }
  NOTES.forEach((n, i) => { n.t += dt; const a = clamp(Math.min(n.t * 5, (3 - n.t) * 2), 0, 1), ny = pad + 64 * S + i * 21 * S; ui.globalAlpha = a; txt(n.s, pad + 4 * S, ny, 11 * S, n.color, 'left', 600, 'rgba(0,0,0,.7)', 2.5); ui.globalAlpha = 1; }); while (NOTES.length && NOTES[0].t > 3) NOTES.shift();
  if (BANNER.t > 0) { BANNER.t -= dt; const k = clamp(Math.min((BANNER.max - BANNER.t) * 4, BANNER.t * 2.5), 0, 1), y = SH * .34; ui.globalAlpha = k; const g = ui.createLinearGradient(0, 0, SW, 0), c = BANNER.red ? '120,10,10' : '20,30,70'; g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(.5, `rgba(${c},.82)`); g.addColorStop(1, `rgba(${c},0)`); ui.fillStyle = g; ui.fillRect(0, y - 34 * S, SW, 68 * S);
    txt(BANNER.a, SW / 2, y - (BANNER.b ? 8 : 0) * S, 28 * S * (1 + (1 - k) * .3), BANNER.red ? '#ffd0c0' : '#ffe9a8'); if (BANNER.b) txt(BANNER.b, SW / 2, y + 19 * S, 15 * S, '#fff', 'center', 600); ui.globalAlpha = 1; }
  if (BAG.t < 5 && G.state === 'play') { ui.globalAlpha = clamp(5 - BAG.t, 0, 1); txt('สู้อัตโนมัติ: แชมเปี้ยนเดินและใช้ของในกระเป๋าเองทั้งหมด', SW / 2, SH * .8, 12.5 * S, '#fff6dc', 'center', 600); ui.globalAlpha = 1; }
  if (H.dead || G.state === 'bagdone') { ui.fillStyle = 'rgba(6,8,18,.45)'; ui.fillRect(0, 0, SW, SH); txt(G.won && !H.dead ? 'ชนะ!' : 'แพ้...', SW / 2, SH * .45, 40 * S, G.won && !H.dead ? '#ffe08a' : '#ff9a8a'); }
}
