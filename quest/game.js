/* quest/game.js: save, sprite cards, the hero (sword), monsters, combat, skills, pickups.
   Heroes and monsters are PixelLab pixel sprites made for this game; 1 sprite pixel = 1 texel (see tools/art/quest_sheet.py, quest_mob.py). */
'use strict';
const SAVE_KEY = 'quest_save_v1';
let SAVE = { gold: 0, lv: 1, xp: 0, up: { atk: 0, hp: 0 }, boss: 0, snd: 1 };
function loadSave() { try { const s = JSON.parse(localStorage.getItem(SAVE_KEY) || 'null'); if (s && s.lv) Object.assign(SAVE, s); } catch (e) { } if (Q.get('mute') === '1') SAVE.snd = 0; if (Q.has('lv')) { SAVE.lv = +Q.get('lv'); SAVE.xp = 0; } }
function saveGame() { if (Q.has('lv')) return; try { localStorage.setItem(SAVE_KEY, JSON.stringify(SAVE)); } catch (e) { } }
const xpNeed = lv => Math.round(25 * Math.pow(lv, 1.6) + 15);
const G = { time: 0, stop: 0, paused: false, started: false, glow: 0, au: 0, zone: -1, banner: null, boss: null, god: Q.get('god') === '1', msg: null };
const TIMERS = [];
function after(t, f) { TIMERS.push({ t, f }); }
function updTimers(dt) { for (let i = TIMERS.length - 1; i >= 0; i--) { const q = TIMERS[i]; q.t -= dt; if (q.t <= 0) { TIMERS.splice(i, 1); q.f(); } } }
function hitStop(t) { G.stop = Math.max(G.stop, t); }

/* ---------- sprite cards */
const SPR_VS = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }';
const SPR_FS = `uniform sampler2D map; uniform vec4 uUV; uniform vec3 uTint, uFlash; uniform float uFlashA, uAlpha; varying vec2 vUv;
  void main(){ vec4 c = texture2D(map, uUV.xy + vUv * uUV.zw); if (c.a < .5) discard;
    if (uAlpha < .99) { float d = (mod(floor(gl_FragCoord.x), 2.) + mod(floor(gl_FragCoord.y), 2.) * 2. + .5) / 4.; if (d > uAlpha) discard; }
    gl_FragColor = vec4(mix(c.rgb * uTint, uFlash, uFlashA), 1.); }`;
const SPR_DFS = `#include <packing>
  uniform sampler2D map; uniform vec4 uUV; varying vec2 vUv; void main(){ if (texture2D(map, uUV.xy + vUv * uUV.zw).a < .5) discard; gl_FragColor = packDepthToRGBA(gl_FragCoord.z); }`;
const SHEETS = {};
async function loadSheet(name) { const [meta, tex] = await Promise.all([fetch(`art/quest/${name}.json?v=${VER}`).then(r => r.json()), TL.loadAsync(`art/quest/${name}.png?v=${VER}`)]); return (SHEETS[name] = { tex: pixTex(tex), meta }); }
class Spr {
  constructor(sh, cw, ch, ax, ay, o = {}) { this.sh = sh; this.cw = cw; this.ch = ch; this.W = sh.meta.w; this.H = sh.meta.h;
    const g = new THREE.PlaneGeometry(cw * TW, ch * TWC).translate((cw / 2 - ax) * TW, (ay - ch / 2) * TWC, 0);
    const u = this.u = { map: { value: sh.tex }, uUV: { value: new THREE.Vector4(0, 0, 1, 1) }, uTint: SPRTINT, uFlash: { value: new THREE.Color(1, 1, 1) }, uFlashA: { value: 0 }, uAlpha: { value: 1 } };
    this.o = new THREE.Mesh(g, new THREE.ShaderMaterial({ uniforms: u, vertexShader: SPR_VS, fragmentShader: SPR_FS, side: THREE.DoubleSide })); this.o.frustumCulled = false;
    if (o.shadow !== false) { this.o.castShadow = true; this.o.customDepthMaterial = new THREE.ShaderMaterial({ uniforms: { map: u.map, uUV: u.uUV }, vertexShader: SPR_VS, fragmentShader: SPR_DFS, side: THREE.DoubleSide }); } }
  frame(col, row) { this.u.uUV.value.set(col * this.cw / this.W, 1 - (row + 1) * this.ch / this.H, this.cw / this.W, this.ch / this.H); }
  place(x, y, z, flip) { const s = snapPt(x, y, z); this.o.position.set(s[0], s[1], z); this.o.scale.x = flip ? -1 : 1; }
}

/* ---------- hero */
const HERO = { name: 'นักดาบ', sheet: 'hero_sword', hp: 160, atk: 14, def: 3, spd: 5.8, c1: 0xffffff, c2: 0x5fdcff };
const SK = [
  { id: 'leap', name: 'กระโดดฟาดปฐพี', cd: 6, range: 7.5, r: 3.2, aim: 'ground', lv: 1 },
  { id: 'whirl', name: 'พายุดาบหมุน', cd: 9, r: 2.9, aim: 'self', lv: 1 },
  { id: 'wave', name: 'คลื่นดาบแสง', cd: 7, range: 11, aim: 'dir', lv: 1 },
];
const P = { x: VILLAGE.x, z: VILLAGE.z + 3.5, y: 0, jy: 0, face: 0, hp: 1, max: 1, atk: 1, def: 0, spd: 5, lv: 1, state: 'free', act: null, combo: 0, comboT: 0, buf: 0, cds: [0, 0, 0], dodgeCd: 0, inv: 0, flash: 0, dead: false, deadT: 0,
  an: { name: 'idle', t: 0, fps: 5, from: 0, to: 3, loop: true }, spr: null, stepT: 0, regenT: 0 };
const DKEY = ['S', 'SE', 'E', 'NE', 'N', 'NE', 'E', 'SE'], DFLIP = [0, 0, 0, 0, 0, 1, 1, 1];
const dirOf = a => ((Math.round(a / (Math.PI / 4)) % 8) + 8) % 8;
function setAn(name, o = {}, force) { const a = P.an; if (!force && a.name === name) { a.fps = o.fps || a.fps; return; } P.an = { name, t: 0, fps: o.fps || 10, from: o.from || 0, to: o.to !== undefined ? o.to : 7, loop: o.loop !== false }; }
function calcStats() { const lv = SAVE.lv; P.lv = lv; P.max = Math.round(HERO.hp * (1 + .14 * (lv - 1)) * (1 + .1 * SAVE.up.hp)); P.atk = HERO.atk * (1 + .12 * (lv - 1)) * (1 + .1 * SAVE.up.atk); P.def = HERO.def + Math.floor(lv / 3); P.spd = HERO.spd; }
function moveHero(dt, mx, mz, spd) {
  const q = { x: P.x + mx * spd * dt, z: P.z + mz * spd * dt }; collide(q, .38);
  if (walkable(q.x, q.z)) { P.x = q.x; P.z = q.z; } else if (walkable(q.x, P.z)) P.x = q.x; else if (walkable(P.x, q.z)) P.z = q.z;
}
function startAct(a) { P.state = 'act'; a.t = 0; a.ei = 0; a.ev = (a.ev || []).sort((p, q) => p[0] - q[0]); P.act = a; P.buf = 0; }
function endAct() { const a = P.act; P.state = 'free'; P.act = null; P.jy = 0; if (a && a.combo) { P.combo = (a.ci + 1) % COMBO.length; P.comboT = .55; } if (a && a.end) a.end(); }
function aimAngle(range) {
  if (IN.mouseAim && IN.aim) return Math.atan2(IN.aim.x - P.x, IN.aim.z - P.z);
  const m = nearestMob(P.x, P.z, range); return m ? Math.atan2(m.x - P.x, m.z - P.z) : P.face;
}
const COMBO = [
  { an: 'slash', fps: 24, from: 2, to: 8, hit: .09, len: .33, chain: .2, mult: 1, arc: 2.9, r: 2.7, lunge: .5, tilt: .15, flip: 1 },
  { an: 'spin', fps: 24, from: 2, to: 8, hit: .1, len: .33, chain: .2, mult: 1.1, arc: 5.4, r: 2.6, lunge: .4, tilt: -.1, flip: -1 },
  { an: 'chop', fps: 19, from: 1, to: 8, hit: .21, len: .5, chain: .37, mult: 2, heavy: true, lunge: .8 },
];
function attack() { if (P.dead || !G.started) return; if (P.state === 'act') { if (P.act.combo) P.buf = .3; return; } startCombo(P.comboT > 0 ? P.combo : 0); }
function startCombo(i) {
  const c = COMBO[i], ang = aimAngle(4.2), sx = Math.sin(ang), sz = Math.cos(ang); P.face = ang;
  setAn(c.an, { fps: c.fps, from: c.from, to: c.to, loop: false }, true);
  startAct({ combo: true, ci: i, len: c.len, chain: c.chain, ev: [[c.hit, () => comboHit(c, ang)]], move: (a, dt) => { if (a.t < c.hit && !nearestMob(P.x + sx * .8, P.z + sz * .8, .9)) moveHero(dt, sx, sz, c.lunge / c.hit); } });
  sfx('swing');
}
function comboHit(c, ang) {
  const y = P.y + 1;
  if (!c.heavy) { swoosh(P.x, y, P.z, ang, { r0: 1, r1: c.r, arc: c.arc, c1: HERO.c1, c2: HERO.c2, tilt: c.tilt, flip: c.flip, dur: .1, hold: .12 });
    const hits = mobsInArc(P.x, P.z, ang, c.r + .3, Math.min(c.arc + .4, TAU)); for (const m of hits) damage(m, c.mult, { kb: 2.4 }); if (hits.length) { hitStop(.04); shake(.035); sfx('hit'); } }
  else { const cx = P.x + Math.sin(ang) * 1.6, cz = P.z + Math.cos(ang) * 1.6, g = gy(cx, cz);
    swoosh(P.x, y + .4, P.z, ang, { r0: 1.1, r1: 3, arc: 2.6, tilt: 1.35, c1: HERO.c1, c2: HERO.c2, dur: .09, hold: .15 });
    shock(cx, cz, 2.4, 0xffffff, HERO.c2); cracks(cx, cz, 1.8, HERO.c2); sparks(cx, g + .3, cz, 12, K.white, K.cyan, 8, .36, 2); flashLight(cx, g + 1, cz, HERO.c2, 1.6, .25, 7);
    const hits = mobsInCircle(cx, cz, 2.3); for (const m of hits) damage(m, c.mult, { kb: 5, hop: 1 }); hitStop(hits.length ? .08 : .02); shake(.12); sfx('heavy'); }
}
function trySkill(i, tx, tz) {
  const s = SK[i]; if (P.dead || !G.started || P.cds[i] > 0 || SAVE.lv < s.lv) return false; if (P.state === 'act' && P.act.lock) return false;
  if (tx === undefined) { const t = autoTarget(s.range || 4, s.r || 2); tx = t[0]; tz = t[1]; }
  if (P.state === 'act') endAct(); P.cds[i] = s.cd; P.comboT = 0;
  if (i === 0) skLeap(tx, tz); else if (i === 1) skWhirl(); else skWave(tx, tz); return true;
}
function skLeap(tx, tz) {
  let dx = tx - P.x, dz = tz - P.z, d = Math.hypot(dx, dz); const R = SK[0].range, rr = SK[0].r; if (d > R) { dx *= R / d; dz *= R / d; } if (d < .4) { dx = Math.sin(P.face) * .4; dz = Math.cos(P.face) * .4; }
  let ex = P.x + dx, ez = P.z + dz; for (let k = 0; k < 10 && !walkable(ex, ez); k++) { ex -= dx * .1; ez -= dz * .1; }
  const x0 = P.x, z0 = P.z, T = .4; P.face = Math.atan2(dx, dz); P.inv = Math.max(P.inv, T + .2);
  setAn('chop', { fps: 8, from: 1, to: 4, loop: false }, true); ring(ex, gy(ex, ez), ez, rr, { c1: 0xffffff, c2: HERO.c2, life: T, w: .07, from: .93, a: .9 }); dustRing(P.x, P.y, P.z, .8, 8); sfx('jump');
  startAct({ lock: true, len: T + .32, move: (a) => { if (a.t < T) { const k = a.t / T; P.x = lerp(x0, ex, k); P.z = lerp(z0, ez, k); P.jy = Math.sin(k * Math.PI) * 2.5; } },
    ev: [[T, () => { P.jy = 0; P.x = ex; P.z = ez; setAn('chop', { fps: 20, from: 5, to: 8, loop: false }, true); const g = gy(ex, ez);
      shock(ex, ez, rr * 1.15, 0xffffff, HERO.c2); ring(ex, g, ez, rr * 1.6, { c1: HERO.c2, c2: HERO.c2, life: .6, w: .06, delay: .08, a: .6 }); cracks(ex, ez, rr * .85, HERO.c2);
      disc(ex, g + .05, ez, rr, { c1: 0xffffff, c2: HERO.c2, life: .28, h: .5, grow: .5 }); pillar(ex, g, ez, .9, 6, { c1: 0xffffff, c2: HERO.c2, life: .4 });
      sparks(ex, g + .4, ez, 26, K.white, K.cyan, 12, .5, 3); embers(ex, g, ez, 12, rr * .7, K.white, K.cyan, 4); flashLight(ex, g + 1.3, ez, HERO.c2, 2.8, .45, 11);
      for (const m of mobsInCircle(ex, ez, rr)) damage(m, 3.2, { kb: 7, hop: 1, fx: ex, fz: ez }); hitStop(.09); shake(.3); sfx('boom'); }]] });
}
function skWhirl() {
  const T = 1.9, rr = SK[1].r, ev = []; let n = 0;
  for (let t = .06; t < T - .05; t += .19) ev.push([t, () => { const a = rnd(0, TAU); n++;
    swoosh(P.x, P.y + .95, P.z, a, { r0: 1.1, r1: rr + .3, arc: 5.3, dur: .15, hold: .07, c1: HERO.c1, c2: HERO.c2, flip: 1, tilt: rnd(-.14, .14) });
    if (n % 2) ring(P.x, gy(P.x, P.z), P.z, rr + .4, { c1: HERO.c2, c2: HERO.c2, life: .3, w: .07, from: .5, a: .5 });
    const hits = mobsInCircle(P.x, P.z, rr); for (const m of hits) damage(m, .62, { kb: -1.2, quiet: n % 2 === 0 }); if (hits.length) { shake(.03); sfx('hit'); } sfx('swing');
    for (let i = 0; i < 4; i++) { const q = rnd(0, TAU); PA.spawn(P.x + Math.cos(q) * rr, P.y + rnd(.3, 1.3), P.z + Math.sin(q) * rr * .8, -Math.sin(q) * 5, rnd(0, 1.5), Math.cos(q) * 5, .3, 2, 1, K.white, K.cyan, 1, 0, 2); } }]);
  P.an = { name: 'still', t: 0, fps: 22, from: 0, to: 7, loop: true };
  startAct({ len: T, free: .72, ev });
}
const PROJ = [];
function skWave(tx, tz) {
  const ang = Math.atan2(tx - P.x, tz - P.z), sx = Math.sin(ang), sz = Math.cos(ang); P.face = ang; setAn('slash', { fps: 21, from: 2, to: 8, loop: false }, true);
  startAct({ len: .4, ev: [[.11, () => { const y = P.y + 1;
    swoosh(P.x, y, P.z, ang, { r0: 1, r1: 3.2, arc: 3.1, c1: HERO.c1, c2: HERO.c2, tilt: .1, dur: .09, hold: .14 });
    const f = swoosh(P.x + sx * 1.2, y, P.z + sz * 1.2, ang, { mode: 1, r0: 1.3, r1: 2.9, arc: 2.2, dur: .62, hold: .08, c1: 0xffffff, c2: HERO.c2 });
    const f2 = swoosh(P.x + sx * .5, y, P.z + sz * .5, ang, { mode: 1, r0: 1.0, r1: 2.2, arc: 1.9, dur: .62, hold: .08, c1: HERO.c2, c2: 0x2a7cff, a: .7 });
    PROJ.push({ x: P.x + sx * 1.2, y, z: P.z + sz * 1.2, vx: sx * 18, vz: sz * 18, t: 0, life: .6, r: 2.1, mult: 2.5, kb: 5, hit: new Set(), fx: [f, f2], off: [0, -.7], ang });
    flashLight(P.x + sx, y, P.z + sz, HERO.c2, 2, .3, 9); shake(.07); sfx('wave'); }]] });
}
function updProj(dt) {
  for (let i = PROJ.length - 1; i >= 0; i--) { const p = PROJ[i]; p.t += dt; p.x += p.vx * dt; p.z += p.vz * dt; const sx = Math.sin(p.ang), sz = Math.cos(p.ang);
    p.fx.forEach((f, k) => f.o.position.set(p.x + sx * p.off[k], p.y, p.z + sz * p.off[k]));
    for (let k = 0; k < 3; k++) { const w = rnd(-1.8, 1.8); PA.spawn(p.x + sz * w, p.y + rnd(-.5, .4), p.z - sx * w, -p.vx * .15, rnd(0, 1), -p.vz * .15, rnd(.2, .4), 2, 1, K.white, K.cyan, 1, 0, 2); }
    for (const m of ACT) if (m.alive && !p.hit.has(m) && Math.hypot(m.x - p.x, m.z - p.z) < p.r + m.d.r) { p.hit.add(m); damage(m, p.mult, { kb: p.kb, fx: p.x - sx, fz: p.z - sz }); hitStop(.03); }
    if (p.t >= p.life) { const g = gy(p.x, p.z); ring(p.x, g, p.z, 2.4, { c1: 0xffffff, c2: HERO.c2, life: .3 }); sparks(p.x, p.y, p.z, 10, K.white, K.cyan, 7, .3, 2); PROJ.splice(i, 1); } }
}
const GHOSTS = [];
function ghost() { let g = GHOSTS.find(q => q.t <= 0); if (!g) { if (GHOSTS.length > 9) return; const M = P.spr.sh.meta; g = { s: new Spr(P.spr.sh, M.cell, M.cell, M.ax, M.ay, { shadow: false }), t: 0 }; g.s.u.uFlash.value.set(HERO.c2); g.s.u.uFlashA.value = .75; GHOSTS.push(g); scene.add(g.s.o); }
  g.t = .22; g.s.u.uUV.value.copy(P.spr.u.uUV.value); g.s.o.position.copy(P.spr.o.position); g.s.o.position.z -= .02; g.s.o.scale.x = P.spr.o.scale.x; g.s.o.visible = true; }
function dodge() {
  if (P.dead || !G.started || P.dodgeCd > 0 || (P.state === 'act' && P.act.lock)) return; if (P.state === 'act') endAct();
  const ang = (IN.mx || IN.mz) ? Math.atan2(IN.mx, IN.mz) : P.face, sx = Math.sin(ang), sz = Math.cos(ang); let gt = 0; P.face = ang; P.dodgeCd = .85; P.inv = Math.max(P.inv, .3); P.comboT = 0;
  setAn('run', { fps: 24, from: 0, to: 7 }, true); dustRing(P.x, P.y, P.z, .6, 8); sfx('dash');
  startAct({ len: .2, move: (a, dt) => { moveHero(dt, sx, sz, 24); gt -= dt; if (gt <= 0) { gt = .03; ghost(); } } });
}
function hurtHero(dmg, fx, fz) {
  if (P.dead || P.inv > 0 || G.god) return; const d = Math.max(1, Math.round(dmg * rnd(.9, 1.1) - P.def)); P.hp -= d; P.flash = .16; P.regenT = 5;
  popNum(P.x, P.y + 2.2, P.z, d, 'hurt'); sparks(P.x, P.y + 1, P.z, 6, K.white, K.red, 5, .25, 2); shake(.07); sfx('hurt');
  if (P.hp <= 0) { P.hp = 0; P.dead = true; P.deadT = 0; P.state = 'dead'; P.act = null; P.jy = 0; setAn('death', { fps: 9, from: 0, to: 6, loop: false }, true); P.face = 0; for (const m of ACT) if (m.alive && !m.d.boss) m.state = 'back'; G.msg = { t: 0, life: 3.2, txt: 'พลาดท่า... กลับไปตั้งหลักที่ค่าย' }; }
}
function respawn() { P.dead = false; P.state = 'free'; P.x = VILLAGE.x; P.z = VILLAGE.z + 3.5; P.hp = P.max; P.inv = 2; P.face = 0; CAMT.set(P.x, groundH(P.x, P.z), P.z); for (const m of ACT) if (m.alive) { m.state = 'back'; if (m.d.boss) { m.hp = m.max; G.boss = null; } } levelUpFx(P.x, groundH(P.x, P.z), P.z); }
function gainXP(n) { SAVE.xp += n; let up = false; while (SAVE.xp >= xpNeed(SAVE.lv) && SAVE.lv < 30) { SAVE.xp -= xpNeed(SAVE.lv); SAVE.lv++; up = true; }
  if (up) { calcStats(); P.hp = P.max; levelUpFx(P.x, P.y, P.z); G.msg = { t: 0, life: 2.4, txt: 'เลเวลอัป!  Lv ' + SAVE.lv, big: true }; sfx('level'); saveGame(); } }
function updHero(dt) {
  for (let i = 0; i < 3; i++) P.cds[i] = Math.max(0, P.cds[i] - dt); P.dodgeCd = Math.max(0, P.dodgeCd - dt); P.inv = Math.max(0, P.inv - dt); P.flash = Math.max(0, P.flash - dt); P.comboT = Math.max(0, P.comboT - dt); P.buf = Math.max(0, P.buf - dt);
  for (const g of GHOSTS) if (g.t > 0) { g.t -= dt; g.s.u.uAlpha.value = Math.max(0, g.t / .22) * .8; if (g.t <= 0) g.s.o.visible = false; }
  if (P.dead) { P.deadT += dt; if (P.deadT > 3.2) respawn(); }
  else if (P.state === 'free') {
    if (IN.mx || IN.mz) { moveHero(dt, IN.mx, IN.mz, P.spd); P.face = Math.atan2(IN.mx, IN.mz); setAn('run', { fps: 13, from: 0, to: 7 });
      P.stepT -= dt; if (P.stepT <= 0) { P.stepT = .24; const m = mapAt(P.x, P.z); PN.spawn(P.x - Math.sin(P.face) * .3, P.y + .08, P.z - Math.cos(P.face) * .3, rnd(-.4, .4), rnd(.5, 1), rnd(-.3, .3), .35, 2, 3, m[2] > .5 ? K.dust : [.55, .75, .35], K.dust, .7, 1, 2); } }
    else setAn('idle', { fps: 5, from: 0, to: 3 });
    if (IN.atk) attack();
    P.regenT -= dt; if (P.regenT <= 0 && P.hp < P.max) P.hp = Math.min(P.max, P.hp + P.max * .04 * dt);
  } else if (P.state === 'act') { const a = P.act; a.t += dt;
    while (P.act === a && a.ei < a.ev.length && a.ev[a.ei][0] <= a.t) a.ev[a.ei++][1]();
    if (P.act === a) { if (a.move) a.move(a, dt); if (a.free && (IN.mx || IN.mz)) moveHero(dt, IN.mx, IN.mz, P.spd * a.free);
      if (IN.atk && a.combo) P.buf = .3;
      if (a.combo && P.buf > 0 && a.t >= a.chain) { const n = (a.ci + 1) % COMBO.length; P.state = 'free'; P.act = null; startCombo(n); }
      else if (a.t >= a.len) endAct(); } }
  P.y = groundH(P.x, P.z); P.an.t += dt;
  const A = P.an, M = P.spr.sh.meta, d = dirOf(P.face), n = A.to - A.from + 1, k = Math.floor(A.t * A.fps), col = A.from + (A.loop ? k % n : Math.min(n - 1, k));
  if (A.name === 'still') { P.spr.frame((d + k) % 8, M.still.row); P.spr.place(P.x, P.y + P.jy, P.z, false); }
  else { const an = M.anims[A.name]; P.spr.frame(Math.min(col, an.n - 1), an.rows[DKEY[d]]); P.spr.place(P.x, P.y + P.jy, P.z, !!DFLIP[d] && A.name !== 'death'); }
  P.spr.u.uFlashA.value = P.flash > 0 ? .7 : 0; P.spr.u.uAlpha.value = P.inv > .35 && !P.act ? (Math.floor(G.time * 14) % 2 ? .5 : 1) : 1;
}

/* ---------- monsters */
const MOBT = {
  mush: { sheet: 'mob_mush', name: 'เห็ดน้อย', r: .62, hp: 38, atk: 8, spd: 2, rng: 1.55, cd: 1.5, xp: 9, gold: 2, aggro: 6.5, wu: .42, hitF: 6, wfps: 9, col: K.red },
  slime: { sheet: 'mob_slime', name: 'สไลม์ใบไม้', r: .72, hp: 46, atk: 7, spd: 1.8, rng: 1.6, cd: 1.6, xp: 10, gold: 2, aggro: 6, wu: .45, hitF: 5, wfps: 8, col: K.green },
  wolf: { sheet: 'mob_wolf', name: 'หมาป่าเงิน', r: .75, hp: 62, atk: 10, spd: 3.7, rng: 1.75, cd: 1.3, xp: 20, gold: 4, aggro: 8, wu: .36, hitF: 5, wfps: 13, col: K.white },
  goblin: { sheet: 'mob_goblin', name: 'ก็อบลิน', r: .6, hp: 80, atk: 12, spd: 2.6, rng: 1.65, cd: 1.6, xp: 24, gold: 7, aggro: 7, wu: .45, hitF: 5, wfps: 10, col: K.green },
  ghost: { sheet: 'mob_ghost', name: 'ผีโคมไฟ', r: .7, hp: 78, atk: 13, spd: 2.7, rng: 1.8, cd: 1.6, xp: 40, gold: 9, aggro: 8, wu: .45, hitF: 5, wfps: 8, fly: 10, col: K.cyan },
  skel: { sheet: 'mob_skel', name: 'นักรบกระดูก', r: .65, hp: 105, atk: 15, spd: 2.5, rng: 1.85, cd: 1.7, xp: 52, gold: 12, aggro: 7.5, wu: .48, hitF: 5, wfps: 9, col: K.violet },
  king: { sheet: 'mob_king', name: 'ราชาเห็ด', big: 1, r: 1.3, hp: 520, atk: 16, spd: 2, rng: 2.8, cd: 2.3, xp: 150, gold: 45, aggro: 9, hitF: 5, wfps: 7, col: K.red },
  dragon: { sheet: 'mob_dragon', name: 'มังกรราตรี', big: 2, boss: 1, r: 2.2, hp: 1500, atk: 26, spd: 2.3, rng: 5, cd: 2.2, xp: 1200, gold: 400, aggro: 13, hitF: 5, wfps: 8, col: K.pink },
};
const PACKS = [
  { t: ['mush'], x: -15, z: 22, n: 4, lv: 1 }, { t: ['slime'], x: 13, z: 23, n: 4, lv: 1 }, { t: ['slime'], x: -18, z: 7, n: 5, lv: 2 }, { t: ['mush'], x: 4, z: 14, n: 5, lv: 2 },
  { t: ['mush', 'slime'], x: -28, z: 28, n: 5, lv: 3 }, { t: ['slime'], x: -30, z: 8, n: 5, lv: 3 }, { t: ['mush', 'slime'], x: -8, z: 1, n: 6, lv: 4 }, { t: ['mush'], x: -22, z: -9, n: 5, lv: 4 }, { t: ['slime', 'mush'], x: -6, z: -15, n: 6, lv: 4 },
  { t: ['king'], x: KINGSPOT.x, z: KINGSPOT.z, n: 1, lv: 5, big: 1, esc: ['mush', 'mush', 'mush'] },
  { t: ['wolf'], x: 20, z: 13, n: 3, lv: 5 }, { t: ['goblin'], x: 33, z: 15, n: 3, lv: 5 }, { t: ['wolf'], x: 45, z: 5, n: 4, lv: 6 }, { t: ['goblin'], x: 27, z: -4, n: 4, lv: 6 }, { t: ['goblin', 'wolf'], x: 50, z: 21, n: 5, lv: 6 },
  { t: ['wolf'], x: 49, z: -13, n: 4, lv: 7 }, { t: ['goblin'], x: 41, z: -21, n: 5, lv: 7 }, { t: ['wolf', 'goblin'], x: 15, z: -18, n: 6, lv: 8 },
  { t: ['ghost'], x: 15, z: -41, n: 4, lv: 9 }, { t: ['skel'], x: -2, z: -32, n: 3, lv: 9 }, { t: ['ghost'], x: 27, z: -49, n: 4, lv: 10 }, { t: ['skel'], x: -12, z: -54, n: 4, lv: 10 }, { t: ['skel', 'ghost'], x: 41, z: -44, n: 5, lv: 11 }, { t: ['ghost', 'skel'], x: -19, z: -34, n: 5, lv: 11 }, { t: ['skel'], x: -50, z: -36, n: 5, lv: 12 },
  { t: ['dragon'], x: LAIR.x, z: LAIR.z - 2, n: 1, lv: 13, big: 1, boss: 1 },
];
const ACT = [], MPOOL = {};
function getMob(type) { const pool = MPOOL[type] || (MPOOL[type] = []); let m = pool.pop(); if (!m) { const d = MOBT[type], sh = SHEETS[d.sheet], M = sh.meta; m = { type, d, spr: new Spr(sh, M.cw, M.ch, M.ax, M.ay), hW: (M.ay - M.top) * TWC, M }; } return m; }
function spawnMob(type, x, z, lv, pack) {
  if (!SHEETS[MOBT[type].sheet]) return null; const m = getMob(type), d = m.d;
  Object.assign(m, { x, z, hx: x, hz: z, lv, pack, max: Math.round(d.hp * (1 + .32 * (lv - 1))), atk: d.atk * (1 + .22 * (lv - 1)), state: 'idle', t: 0, cd: rnd(.3, 1), kx: 0, kz: 0, jy: 0, vy: 0, flash: 0, stun: 0, frozen: 0, alive: true, wt: rnd(0, 2), tx: x, tz: z, fx: Math.random() < .5 ? 1 : -1, moving: false, at: rnd(0, 3), tel: null, n: 0, ph: 0, lx: 0, lz: 0 });
  m.hp = m.max; m.spr.u.uAlpha.value = 1; m.spr.u.uFlashA.value = 0; scene.add(m.spr.o); ACT.push(m); return m;
}
function removeMob(m) { scene.remove(m.spr.o); const i = ACT.indexOf(m); if (i >= 0) ACT.splice(i, 1); MPOOL[m.type].push(m); if (G.boss === m) G.boss = null; }
function updPacks(dt) {
  for (const p of PACKS) { const d = Math.hypot(P.x - p.x, P.z - p.z);
    if (!p.on) { if (p.resp > 0) { p.resp -= dt; continue; } if (d < 30 && (d > 11 || !p.cleared)) { p.on = true; p.cleared = false; p.mobs = []; const list = [];
        for (let i = 0; i < p.n; i++) list.push(p.t[i % p.t.length]); for (const e of p.esc || []) list.push(e);
        list.forEach((ty, i) => { const a = i / list.length * TAU + rnd(0, .8), r = i < p.n && p.big ? 0 : rnd(1, 3.2); let x = p.x + Math.cos(a) * r, z = p.z + Math.sin(a) * r; if (!walkable(x, z)) { x = p.x; z = p.z; } const m = spawnMob(ty, x, z, p.lv, p); if (m) p.mobs.push(m); }); } }
    else { const live = p.mobs.filter(m => m.alive).length; if (!live && !p.mobs.some(m => ACT.includes(m))) { p.on = false; p.cleared = true; p.resp = p.boss ? 90 : p.big ? 60 : 22; }
      else if (d > 44 && p.mobs.every(m => m.state === 'idle' || !m.alive)) { for (const m of p.mobs) if (ACT.includes(m)) removeMob(m); p.on = false; p.cleared = false; } } }
}
function nearestMob(x, z, maxD) { let b = null, bd = maxD; for (const m of ACT) if (m.alive) { const d = Math.hypot(m.x - x, m.z - z) - m.d.r; if (d < bd) { bd = d; b = m; } } return b; }
function mobsInCircle(x, z, r) { return ACT.filter(m => m.alive && Math.hypot(m.x - x, m.z - z) < r + m.d.r); }
function mobsInArc(x, z, ang, r, arc) { return ACT.filter(m => { if (!m.alive) return false; const dx = m.x - x, dz = m.z - z, d = Math.hypot(dx, dz); return d < r + m.d.r && (d < m.d.r + .6 || arc >= TAU - .01 || Math.abs(angDiff(ang, Math.atan2(dx, dz))) < arc / 2 + Math.atan2(m.d.r, d)); }); }
function autoTarget(range, r) {
  let best = null, bs = -1; for (const m of ACT) { if (!m.alive) continue; const d = Math.hypot(m.x - P.x, m.z - P.z); if (d > range + 1.5) continue; let s = (1 - d / (range + 2)) * .6 + (m.d.big ? 3 : 0); for (const q of ACT) if (q.alive && Math.hypot(q.x - m.x, q.z - m.z) < r) s++; if (s > bs) { bs = s; best = m; } }
  if (!best) return [P.x + Math.sin(P.face) * range * .6, P.z + Math.cos(P.face) * range * .6];
  let sx = 0, sz = 0, n = 0; for (const q of ACT) if (q.alive && Math.hypot(q.x - best.x, q.z - best.z) < r) { sx += q.x; sz += q.z; n++; } return [sx / n, sz / n];
}
function aggro(m) { if (m.state === 'idle' || m.state === 'back') { m.state = 'chase'; if (!m.seen) { m.seen = true; popNum(m.x, m.y + m.hW + .3, m.z, '!', 'warn'); } } if (m.pack) for (const q of m.pack.mobs) if (q !== m && q.alive && q.state === 'idle') { q.state = 'chase'; q.cd = rnd(.2, 1); } if (m.d.boss && G.boss !== m) { G.boss = m; G.msg = { t: 0, life: 2.6, txt: m.d.name + ' ตื่นแล้ว!', big: true, col: '#ff7a8a' }; sfx('roar'); } }
function damage(m, mult, o = {}) {
  if (!m.alive) return; let d = P.atk * mult * rnd(.9, 1.1); const crit = Math.random() < .13; if (crit) d *= 1.8; d = Math.max(1, Math.round(d));
  m.hp -= d; m.flash = .1; popNum(m.x, m.y + m.hW, m.z, d, crit ? 'crit' : 'dmg'); if (!o.quiet) hitSpark(m.x, m.y + m.hW * .5, m.z + .05, K.white, K.cyan, crit || mult >= 2);
  const fx = o.fx !== undefined ? o.fx : P.x, fz = o.fz !== undefined ? o.fz : P.z, dx = m.x - fx, dz = m.z - fz, l = Math.hypot(dx, dz) || 1, kb = (o.kb || 0) * (m.d.big ? (m.d.boss ? 0 : .15) : 1);
  m.kx += dx / l * kb; m.kz += dz / l * kb; if (o.hop && !m.d.big) m.vy = 5;
  aggro(m);
  if (m.hp <= 0) killMob(m); else if (!m.d.big && m.state !== 'back') { m.state = 'hurt'; m.t = 0; if (m.tel) { m.tel.end = null; m.tel.t = m.tel.life; m.tel = null; } }
}
function killMob(m) {
  m.alive = false; m.t = 0; m.hp = 0; if (m.tel) { m.tel.end = null; m.tel.t = m.tel.life; m.tel = null; }
  deathPoof(m.x, m.y, m.z, m.hW, m.d.col); gainXP(Math.round(m.d.xp * (1 + .3 * (m.lv - 1))));
  const g = Math.max(1, Math.round(m.d.gold * (1 + .25 * (m.lv - 1)) * rnd(.7, 1.3))), n = clamp(Math.ceil(g / 3), 1, m.d.boss ? 24 : m.d.big ? 10 : 4);
  for (let i = 0; i < n; i++) dropItem('coin', m.x, m.y + .5, m.z, g / n); if (Math.random() < (m.d.big ? 1 : .13)) dropItem('heart', m.x, m.y + .5, m.z, 0);
  if (m.d.big) { explosion(m.x, m.z, m.d.boss ? 5 : 3.2, { c2: m.d.boss ? 0xff5ad0 : 0xffb040, pow: 1.6, scorch: false }); hitStop(.14); G.msg = { t: 0, life: 3, txt: 'ปราบ ' + m.d.name + ' สำเร็จ!', big: true, col: '#ffe27a' }; sfx('level'); if (m.d.boss) { SAVE.boss++; } saveGame(); }
  sfx('die');
}
function stepTo(m, tx, tz, spd, dt) {
  const dx = tx - m.x, dz = tz - m.z, l = Math.hypot(dx, dz); if (l < .15) { m.moving = false; return; }
  const q = { x: m.x + dx / l * spd * dt, z: m.z + dz / l * spd * dt }; collide(q, m.d.r * .8); if (walkable(q.x, q.z)) { m.x = q.x; m.z = q.z; } m.moving = true; if (Math.abs(dx) > .15) m.fx = dx > 0 ? 1 : -1;
}
function teleHit(kind, x, z, ang, sz, warn, mult, m, o = {}) {   /* a red warning, then the hit */
  return tele(kind, x, z, ang, sz, warn, () => { if (m && !m.alive) return; if (inShape(kind, x, z, ang, sz, P.x, P.z, .35, o.arc || 1)) hurtHero((m ? m.atk : o.atk) * mult, x, z); if (o.fire) o.fire(); }, o);
}
function bigBrain(m, dt, dx, dz, dist) {   /* the mushroom king and the dragon: red ground warnings before every hit */
  const d = m.d, hp = m.hp / m.max, ang = Math.atan2(dx, dz);
  if (m.state === 'idle') { m.moving = false; if (!P.dead && dist < d.aggro && zoneAt(P.x, P.z) !== 0) aggro(m); return; }
  if (m.state === 'back') { stepTo(m, m.hx, m.hz, d.spd * 1.4, dt); m.hp = Math.min(m.max, m.hp + m.max * .3 * dt); if (Math.hypot(m.x - m.hx, m.z - m.hz) < 1) { m.state = 'idle'; if (G.boss === m) G.boss = null; } return; }
  if (P.dead || Math.hypot(m.x - m.hx, m.z - m.hz) > 30 || dist > 34) { m.state = 'back'; return; }
  if (m.state === 'atk') { m.t += dt; if (m.leap) { const k = clamp(m.t / m.leap.T, 0, 1); m.x = lerp(m.leap.x0, m.leap.x1, k); m.z = lerp(m.leap.z0, m.leap.z1, k); m.jy = Math.sin(k * Math.PI) * 4; if (k >= 1) { m.leap = null; m.jy = 0; } }
    if (m.t >= m.dur) { m.state = 'chase'; m.cd = d.cd * (hp < .35 ? .65 : 1) * rnd(.85, 1.15); } return; }
  if (dist > d.rng * .75) stepTo(m, P.x, P.z, d.spd * (hp < .35 ? 1.3 : 1), dt); else { m.moving = false; m.fx = dx >= 0 ? 1 : -1; }
  if (m.cd > 0) return; m.n++; m.state = 'atk'; m.t = 0; m.fx = dx >= 0 ? 1 : -1; m.aa = ang; m.moving = false;
  const G0 = (x, z) => gy(x, z);
  if (!d.boss) {   /* mushroom king */
    if (m.n % 3 === 0) { m.dur = 1.75; m.wu = 1.2; teleHit('circle', m.x, m.z, 0, 5.6, 1.2, 1.25, m, { fire: () => { shock(m.x, m.z, 5.6, 0xffffff, 0xff7a3a); smoke(m.x, G0(m.x, m.z), m.z, 14, 4, [.8, .5, .7], [.4, .25, .4], 2, 4); shake(.2); sfx('boom');
      if (ACT.filter(q => q.alive && q.type === 'mush').length < 5) for (let i = 0; i < 2; i++) { const a = rnd(0, TAU), q = spawnMob('mush', m.x + Math.cos(a) * 2.5, m.z + Math.sin(a) * 2.5, Math.max(1, m.lv - 2), m.pack); if (q) { m.pack.mobs.push(q); q.state = 'chase'; deathPoof(q.x, G0(q.x, q.z), q.z, 1, K.red); } } } }); }
    else if (dist > 4.5) { const T = 1, x1 = P.x, z1 = P.z; m.dur = T + .5; m.wu = T; m.leap = { x0: m.x, z0: m.z, x1, z1, T }; sfx('jump');
      teleHit('circle', x1, z1, 0, 3.1, T, 1.7, m, { fire: () => { shock(x1, z1, 3.4, 0xffffff, 0xff7a3a); cracks(x1, z1, 2.6, 0xff9a30); shake(.26); sfx('boom'); } }); }
    else { const cx = m.x + Math.sin(ang) * 2, cz = m.z + Math.cos(ang) * 2; m.dur = 1.3; m.wu = .85; teleHit('circle', cx, cz, 0, 3, .85, 1.5, m, { fire: () => { shock(cx, cz, 3.1, 0xffffff, 0xff7a3a); cracks(cx, cz, 2.2, 0xff9a30); shake(.2); sfx('heavy'); } }); }
    return; }
  /* dragon */
  const fireAt = (x, z, r) => { explosion(x, z, r, { c2: 0xff5ad0, ka: K.pink, kb: K.violet }); sfx('boom'); };
  if (hp < .35 && !m.summoned) { m.summoned = true; m.dur = 1.6; m.wu = 1; G.msg = { t: 0, life: 2.4, txt: 'มังกรคลั่ง!', big: true, col: '#ff5ad0' }; sfx('roar'); shake(.3); ring(m.x, G0(m.x, m.z), m.z, 9, { c1: 0xffffff, c2: 0xff5ad0, life: .9, w: .08 });
    for (let i = 0; i < 4; i++) { const a = i / 4 * TAU + .6, q = spawnMob('ghost', m.x + Math.cos(a) * 5, m.z + Math.sin(a) * 5, 10, m.pack); if (q) { m.pack.mobs.push(q); q.state = 'chase'; deathPoof(q.x, G0(q.x, q.z), q.z, 1.5, K.cyan); } } return; }
  if (hp < .65 && m.n % 3 === 0) { m.dur = 2; m.wu = 1.1; sfx('roar');
    for (let i = 0; i < 8; i++) { const a = rnd(0, TAU), r = i ? rnd(2, 7.5) : 0, x = P.x + Math.cos(a) * r, z = P.z + Math.sin(a) * r, w = 1 + i * .11;
      teleHit('circle', x, z, 0, 2.4, w, 1.1, m, { fire: () => fireAt(x, z, 2.4) }); after(w - .32, () => { for (let k = 0; k < 8; k++) PA.spawn(x - 1.6 + k * .2, G0(x, z) + 9 - k * 1.1, z - .5, 1.6, -26, .5, .34, 3, 2, K.white, K.pink, 1); }); } return; }
  if (dist < 5.6 && m.n % 2) { m.dur = 1.25; m.wu = .72; teleHit('cone', m.x, m.z, ang, 6.2, .72, 1.1, m, { arc: 2.6, fire: () => { swoosh(m.x, m.y + 1.4, m.z, ang, { r0: 2, r1: 6.2, arc: 2.6, c1: 0xffffff, c2: 0xff5ad0, dur: .12, hold: .16 }); shake(.16); sfx('heavy'); } }); return; }
  if (dist < 7.5) { m.dur = 1.3; m.wu = .75; teleHit('rect', m.x, m.z, ang, [7.6, 3.4], .75, 1.35, m, { fire: () => { const x = m.x + Math.sin(ang) * 5, z = m.z + Math.cos(ang) * 5; shock(x, z, 2.6, 0xffffff, 0xff5ad0); sparks(x, G0(x, z) + 1, z, 16, K.white, K.pink, 10, .4, 3); shake(.18); sfx('heavy'); } }); m.lx = Math.sin(ang) * 2.2; m.lz = Math.cos(ang) * 2.2; return; }
  m.dur = 2.6; m.wu = 1; sfx('roar');   /* fire breath: a long cone, then a stream that burns for a second */
  teleHit('cone', m.x, m.z, ang, 12.5, 1, .6, m, { arc: .95, fire: () => { let t = 0; const tick = () => { if (!m.alive || t > 4) return; t++;
    if (inShape('cone', m.x, m.z, ang, 12.5, P.x, P.z, .35, .95)) hurtHero(m.atk * .5, m.x, m.z); shake(.06); after(.22, tick); }; tick(); m.breath = { t: 1.1, ang }; sfx('fire'); } });
}
function updMob(m, dt) {
  const d = m.d; m.flash = Math.max(0, m.flash - dt); m.at += dt;
  if (m.kx || m.kz) { const nx = m.x + m.kx * dt, nz = m.z + m.kz * dt; if (walkable(nx, nz)) { m.x = nx; m.z = nz; } const f = Math.exp(-9 * dt); m.kx *= f; m.kz *= f; if (Math.abs(m.kx) + Math.abs(m.kz) < .06) m.kx = m.kz = 0; }
  if (m.vy || m.jy > 0) { if (!m.leap) { m.jy += m.vy * dt; m.vy -= 26 * dt; if (m.jy <= 0) { m.jy = 0; m.vy = 0; } } }
  if (!m.alive) { m.t += dt; m.spr.u.uAlpha.value = Math.max(0, 1 - m.t / .42); if (m.t > .42) { removeMob(m); return; } }
  else if (m.frozen > 0) m.frozen -= dt; else if (m.stun > 0) m.stun -= dt;
  else { m.cd -= dt; const dx = P.x - m.x, dz = P.z - m.z, dist = Math.hypot(dx, dz);
    if (d.big) bigBrain(m, dt, dx, dz, dist);
    else switch (m.state) {
      case 'idle': m.wt -= dt; if (m.wt <= 0) { m.wt = rnd(1.5, 4.5); const a = rnd(0, TAU), r = rnd(.5, 3); m.tx = m.hx + Math.cos(a) * r; m.tz = m.hz + Math.sin(a) * r; } stepTo(m, m.tx, m.tz, d.spd * .4, dt); if (!P.dead && dist < d.aggro && zoneAt(P.x, P.z) !== 0) aggro(m); break;
      case 'chase': if (P.dead || Math.hypot(m.x - m.hx, m.z - m.hz) > 26 || zoneAt(P.x, P.z) === 0) { m.state = 'back'; break; }
        if (dist > d.rng * .8) stepTo(m, P.x, P.z, d.spd, dt); else { m.moving = false; m.fx = dx >= 0 ? 1 : -1; }
        if (dist < d.rng && m.cd <= 0) { m.state = 'atk'; m.t = 0; m.hitDone = false; m.aa = Math.atan2(dx, dz); m.fx = dx >= 0 ? 1 : -1; m.moving = false; m.tel = tele('cone', m.x, m.z, m.aa, d.rng + .55, d.wu, null, { arc: 1.7, soft: .55 }); } break;
      case 'atk': m.t += dt; if (!m.hitDone && m.t >= d.wu) { m.hitDone = true; m.tel = null; if (inShape('cone', m.x, m.z, m.aa, d.rng + .55, P.x, P.z, .35, 1.7)) hurtHero(m.atk, m.x, m.z); }
        if (m.t >= d.wu + .4) { m.state = 'chase'; m.cd = d.cd * rnd(.8, 1.25); } break;
      case 'hurt': m.t += dt; m.moving = false; if (m.t > .24) m.state = 'chase'; break;
      case 'back': stepTo(m, m.hx, m.hz, d.spd * 1.4, dt); m.hp = Math.min(m.max, m.hp + m.max * .5 * dt); if (Math.hypot(m.x - m.hx, m.z - m.hz) < 1) { m.state = 'idle'; m.seen = false; } break;
    }
    for (const q of ACT) if (q !== m && q.alive) { const ex = m.x - q.x, ez = m.z - q.z, l = Math.hypot(ex, ez), mn = d.r + q.d.r; if (l < mn && l > .001 && !d.big) { const p = (mn - l) * .5; m.x += ex / l * p; m.z += ez / l * p; } }
    const hl = Math.hypot(m.x - P.x, m.z - P.z), hm = d.r + .55; if (hl < hm && hl > .001 && !m.leap && !d.boss) { m.x += (m.x - P.x) / hl * (hm - hl); m.z += (m.z - P.z) / hl * (hm - hl); }
  }
  if (m.breath) { m.breath.t -= dt; const a = m.breath.ang, hx = m.x + Math.sin(a) * 2.2, hz = m.z + Math.cos(a) * 2.2; for (let i = 0; i < 5; i++) { const s = rnd(-.45, .45), sp = rnd(9, 15); PA.spawn(hx, m.y + 1.6, hz, Math.sin(a + s) * sp, rnd(-1, 1.5), Math.cos(a + s) * sp, rnd(.5, .85), 3, 5, K.white, K.pink, 1, 0, .6); }
    if (Math.random() < .5) flashLight(hx + Math.sin(a) * 4, m.y + 1, hz + Math.cos(a) * 4, 0xff5ad0, 1.6, .2, 9); if (m.breath.t <= 0) m.breath = null; }
  /* draw */
  m.y = groundH(m.x, m.z); const A = m.M.anims; let row = A.walk.row, col = 0, ox = 0, oz = 0;
  if (m.alive && m.state === 'atk') { const an = (d.boss && m.dur > 2 && A.breath) ? A.breath : A.attack, n = an.n, wu = d.big ? m.wu : d.wu; row = an.row;
    col = m.t < wu ? Math.floor(m.t / wu * d.hitF) : Math.min(n - 1, d.hitF + Math.floor((m.t - wu) / .4 * (n - d.hitF)));
    if (!d.big && m.t >= d.wu) { const k = Math.sin(clamp((m.t - d.wu) / .3, 0, 1) * Math.PI) * .45; ox = Math.sin(m.aa) * k; oz = Math.cos(m.aa) * k; }
    if (d.boss && m.lx && m.t >= m.wu) { const k = Math.sin(clamp((m.t - m.wu) / .45, 0, 1) * Math.PI); ox = m.lx * k; oz = m.lz * k; if (m.t >= m.wu + .45) m.lx = m.lz = 0; } }
  else if (m.moving || d.fly || d.big) col = Math.floor(m.at * d.wfps * (m.moving ? 1 : .55)) % A.walk.n; else col = Math.floor(m.at * 2.2) % 2 ? 0 : (A.walk.n > 4 ? 4 : 0);
  m.spr.frame(col, row); m.spr.place(m.x + ox, m.y + m.jy + (d.fly || 0) * TWC, m.z + oz, m.fx < 0);
  const u = m.spr.u; if (m.flash > 0) { u.uFlash.value.setRGB(1, 1, 1); u.uFlashA.value = .9; } else if (m.frozen > 0) { u.uFlash.value.setRGB(.55, .85, 1); u.uFlashA.value = .6; } else u.uFlashA.value = 0;
}

/* ---------- pickups: coins and hearts, small code-drawn pixel icons */
const PICK = [];
const ICON = (() => { const c = document.createElement('canvas'); c.width = 16; c.height = 8; const g = c.getContext('2d');
  const px = (rows, ox, pal) => rows.forEach((r, y) => [...r].forEach((ch, x) => { if (ch !== '.') { g.fillStyle = pal[ch]; g.fillRect(ox + x, y, 1, 1); } }));
  px(['.oooo..', 'oyyywo.', 'oywyyo.', 'oyyyyo.', 'oyyydo.', '.oooo..'], 0, { o: '#6b3a10', y: '#ffc93c', w: '#fff3b0', d: '#e09a1c' });
  px(['.oo.oo.', 'orrorro', 'orwrrro', 'orrrrro', '.orrro.', '..oro..', '...o...'], 8, { o: '#5a1020', r: '#ff4a6a', w: '#ffd0d8' });
  const t = new THREE.CanvasTexture(c); pixTex(t); return { tex: t, meta: { w: 16, h: 8 } }; })();
function dropItem(kind, x, y, z, v) { let s = null; const a = rnd(0, TAU), sp = rnd(1.5, 4);
  s = new Spr(ICON, 8, 8, 3, kind === 'coin' ? 6 : 7, { shadow: false }); s.frame(kind === 'coin' ? 0 : 1, 0); scene.add(s.o);
  PICK.push({ kind, v, x, y, z, vx: Math.cos(a) * sp, vz: Math.sin(a) * sp, vy: rnd(5, 8), t: 0, s }); }
function updPick(dt) {
  for (let i = PICK.length - 1; i >= 0; i--) { const p = PICK[i]; p.t += dt; const g = groundH(p.x, p.z) + .12, dx = P.x - p.x, dz = P.z - p.z, d = Math.hypot(dx, dz);
    if (p.t > .45 && d < 4.2 && !P.dead) { const sp = 6 + p.t * 16; p.x += dx / d * sp * dt; p.z += dz / d * sp * dt; p.y += (P.y + .8 - p.y) * Math.min(1, dt * 10); }
    else { p.vy -= 24 * dt; p.x += p.vx * dt; p.z += p.vz * dt; p.y += p.vy * dt; if (p.y < g) { p.y = g; p.vy = Math.abs(p.vy) > 2 ? -p.vy * .4 : 0; p.vx *= .5; p.vz *= .5; } }
    p.s.place(p.x, p.y + (p.vy === 0 ? Math.sin(p.t * 5) * .06 + .06 : 0), p.z, false);
    if ((d < .6 && p.t > .45) || p.t > 40) { scene.remove(p.s.o); p.s.o.geometry.dispose(); p.s.o.material.dispose(); PICK.splice(i, 1);
      if (p.t <= 40) { if (p.kind === 'coin') { SAVE.gold += Math.max(1, Math.round(p.v)); sfx('coin'); PA.spawn(P.x, P.y + 1.2, P.z, 0, 2, 0, .3, 2, 1, K.white, K.gold, 1); } else { const h = Math.round(P.max * .22); P.hp = Math.min(P.max, P.hp + h); popNum(P.x, P.y + 2.2, P.z, '+' + h, 'heal'); ring(P.x, gy(P.x, P.z), P.z, 1.4, { c1: 0xffffff, c2: 0x6aff9a, life: .4 }); sfx('heal'); } } } }
}
