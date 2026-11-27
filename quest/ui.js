/* quest/ui.js: input (keys + mouse, touch stick + buttons), sound, HUD on two canvases (pixel shapes on the texel canvas, Thai text on the
   full-resolution one), boot and the main loop. */
'use strict';
const IN = { keys: {}, mx: 0, mz: 0, atk: false, aim: null, mouseAim: false, touch: false, joy: null, atkId: null, sk: null, mouseAtk: false };
const UI = { u: 1, btn: [], W: 0, H: 0 };
const POPS = [];
function popNum(x, y, z, txt, kind) { POPS.push({ x: x + rnd(-.25, .25), y, z, txt: String(txt), kind, t: 0 }); if (POPS.length > 60) POPS.shift(); }

/* ---------- sound: small synth, no files */
let AC = null, sfxLast = {};
function audioOn() { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { } } if (AC && AC.state === 'suspended') AC.resume(); }
function tone(f0, f1, dur, type = 'square', vol = .06, delay = 0) { const t = AC.currentTime + delay, o = AC.createOscillator(), g = AC.createGain(); o.type = type; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t + dur);
  g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(.0008, t + dur); o.connect(g).connect(AC.destination); o.start(t); o.stop(t + dur + .02); }
let NBUF = null;
function noise(dur, vol, f0, f1, delay = 0) { if (!NBUF) { NBUF = AC.createBuffer(1, AC.sampleRate, AC.sampleRate); const d = NBUF.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; }
  const t = AC.currentTime + delay, s = AC.createBufferSource(), f = AC.createBiquadFilter(), g = AC.createGain(); s.buffer = NBUF; s.loop = true; f.type = 'bandpass'; f.Q.value = .9; f.frequency.setValueAtTime(f0, t); f.frequency.exponentialRampToValueAtTime(Math.max(30, f1), t + dur);
  g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(.0008, t + dur); s.connect(f).connect(g).connect(AC.destination); s.start(t, Math.random()); s.stop(t + dur + .02); }
const SFX = {
  swing: () => noise(.13, .16, 3200, 700), hit: () => { noise(.07, .22, 1200, 250); tone(190, 70, .09, 'square', .06); }, heavy: () => { noise(.2, .3, 700, 90); tone(120, 40, .22, 'sawtooth', .1); },
  boom: () => { noise(.5, .42, 500, 40); tone(90, 28, .5, 'sawtooth', .14); }, coin: () => { tone(988, 988, .05, 'square', .04); tone(1319, 1319, .12, 'square', .04, .05); },
  level: () => [523, 659, 784, 1047, 1319].forEach((f, i) => tone(f, f, .16, 'square', .05, i * .08)), hurt: () => { tone(300, 110, .16, 'sawtooth', .09); noise(.08, .12, 600, 200); },
  dash: () => noise(.16, .14, 900, 3000), jump: () => tone(220, 520, .18, 'square', .05), wave: () => { noise(.35, .2, 4000, 500); tone(880, 220, .3, 'sawtooth', .05); },
  die: () => { tone(420, 90, .2, 'square', .05); noise(.15, .1, 1500, 300); }, roar: () => { tone(110, 55, .7, 'sawtooth', .16); noise(.7, .2, 300, 80); }, fire: () => noise(1, .22, 900, 200), heal: () => { tone(660, 990, .18, 'sine', .08); tone(990, 1320, .2, 'sine', .06, .1); },
};
function sfx(n) { if (!SAVE.snd || !AC || AC.state !== 'running') return; const now = performance.now(); if (now - (sfxLast[n] || 0) < 45) return; sfxLast[n] = now; try { SFX[n] && SFX[n](); } catch (e) { } }

/* ---------- input */
const KEYMOVE = { KeyW: [0, -1], ArrowUp: [0, -1], KeyS: [0, 1], ArrowDown: [0, 1], KeyA: [-1, 0], ArrowLeft: [-1, 0], KeyD: [1, 0], ArrowRight: [1, 0] };
addEventListener('keydown', e => { if (e.repeat) return; IN.keys[e.code] = 1; if (!G.started) { if (e.code === 'Enter' || e.code === 'Space') startGame(); return; }
  const si = { KeyQ: 0, KeyE: 1, KeyR: 2, Digit1: 0, Digit2: 1, Digit3: 2 }[e.code];
  if (si !== undefined) { if (IN.mouseAim && IN.aim) trySkill(si, IN.aim.x, IN.aim.z); else trySkill(si); }
  if (e.code === 'Space' || e.code === 'ShiftLeft') { dodge(); e.preventDefault(); } if (e.code === 'KeyM') { SAVE.snd = SAVE.snd ? 0 : 1; saveGame(); } });
addEventListener('keyup', e => { IN.keys[e.code] = 0; });
addEventListener('blur', () => { IN.keys = {}; IN.mouseAtk = false; IN.joy = null; IN.atkId = null; IN.sk = null; });
hiC.addEventListener('contextmenu', e => e.preventDefault());
const cssToLo = (x, y) => [x / PX.T, y / PX.T];
function btnAt(x, y) { for (const b of UI.btn) if (Math.hypot(x - b.x, y - b.y) < b.r * 1.15) return b; return null; }
hiC.addEventListener('pointerdown', e => { audioOn(); e.preventDefault();
  if (!G.started) { startGame(e.pointerType !== 'mouse'); return; }
  const [x, y] = cssToLo(e.clientX, e.clientY);
  if (x > UI.W - 16 * UI.u && y < 16 * UI.u) { SAVE.snd = SAVE.snd ? 0 : 1; saveGame(); return; }
  if (e.pointerType === 'mouse') { IN.touch = false; const b = btnAt(x, y); if (b && b.id !== 'atk') { if (b.id === 'dodge') dodge(); else trySkill(b.i); return; }
    if (e.button === 2) dodge(); else if (e.button === 0) { IN.mouseAtk = true; IN.mouseAim = true; IN.aim = groundAt(x, y); } return; }
  if (!IN.touch) { IN.touch = true; IN.mouseAim = false; layoutUI(); }
  try { hiC.setPointerCapture(e.pointerId); } catch (_) { }
  const b = btnAt(x, y);
  if (b) { if (b.id === 'atk') IN.atkId = e.pointerId; else if (b.id === 'dodge') dodge(); else IN.sk = { id: e.pointerId, i: b.i, x0: e.clientX, y0: e.clientY, dx: 0, dy: 0, aim: false }; }
  else if (e.clientX < PX.SW * .55 && !IN.joy) IN.joy = { id: e.pointerId, x0: e.clientX, y0: e.clientY, x: e.clientX, y: e.clientY }; });
hiC.addEventListener('pointermove', e => {
  if (e.pointerType === 'mouse') { const [x, y] = cssToLo(e.clientX, e.clientY); IN.aim = groundAt(x, y); IN.mouseAim = true; IN.touch = false; return; }
  if (IN.joy && IN.joy.id === e.pointerId) { IN.joy.x = e.clientX; IN.joy.y = e.clientY; }
  if (IN.sk && IN.sk.id === e.pointerId) { IN.sk.dx = e.clientX - IN.sk.x0; IN.sk.dy = e.clientY - IN.sk.y0; if (Math.hypot(IN.sk.dx, IN.sk.dy) > 14) IN.sk.aim = true; } });
function pUp(e) { if (e.pointerType === 'mouse') { if (e.button === 0) IN.mouseAtk = false; return; }
  if (IN.joy && IN.joy.id === e.pointerId) IN.joy = null; if (IN.atkId === e.pointerId) IN.atkId = null;
  if (IN.sk && IN.sk.id === e.pointerId) { const s = IN.sk; IN.sk = null; if (s.aim) { const t = skAim(s); trySkill(s.i, t[0], t[1]); } else trySkill(s.i); } }
hiC.addEventListener('pointerup', pUp); hiC.addEventListener('pointercancel', pUp);
function skAim(s) { const k = SK[s.i], R = k.range || 3, l = Math.hypot(s.dx, s.dy), f = Math.min(1, l / 70) * R / (l || 1); return [P.x + s.dx * f, P.z + s.dy * f]; }
function readInput() {
  let mx = 0, mz = 0; for (const k in KEYMOVE) if (IN.keys[k]) { mx += KEYMOVE[k][0]; mz += KEYMOVE[k][1]; }
  if (IN.joy) { const dx = IN.joy.x - IN.joy.x0, dy = IN.joy.y - IN.joy.y0, l = Math.hypot(dx, dy); if (l > 9) { mx = dx / l; mz = dy / l; } }
  const l = Math.hypot(mx, mz); IN.mx = l ? mx / l : 0; IN.mz = l ? mz / l : 0; IN.atk = !!(IN.mouseAtk || IN.keys.KeyJ || IN.atkId !== null);
}
let AIMR = null;
function updAim() {   /* the spot a dragged skill will land on */
  if (!AIMR) { const mk = (c, w) => { const m = fxClone(M_RING); m.uniforms.uC1.value.set(0xffffff); m.uniforms.uC2.value.set(c); m.uniforms.uW.value = w; m.uniforms.uR.value = 1 - w; const o = new THREE.Mesh(FLAT, m); o.frustumCulled = false; o.visible = false; fxScene.add(o); return o; }; AIMR = [mk(HERO.c2, .08), mk(0x3a6aa0, .02)]; }
  const s = IN.sk; if (!s || !s.aim) { AIMR[0].visible = AIMR[1].visible = false; return; }
  const k = SK[s.i], t = skAim(s), r = k.r || 1.6; AIMR[0].visible = true; AIMR[0].position.set(t[0], gy(t[0], t[1]), t[1]); AIMR[0].scale.set(r, 1, r); AIMR[0].material.uniforms.uA.value = .8;
  AIMR[1].visible = !!k.range; AIMR[1].position.set(P.x, gy(P.x, P.z), P.z); AIMR[1].scale.set(k.range || 1, 1, k.range || 1); AIMR[1].material.uniforms.uA.value = .5;
}

/* ---------- HUD */
function layoutUI() {
  UI.W = PX.w; UI.H = PX.h; UI.u = Math.max(1, Math.round(2 / PX.T)); const c = v => v / PX.T, W = UI.W, H = UI.H; UI.btn = [];
  if (IN.touch) { const ax = W - c(64), ay = H - c(64);
    UI.btn.push({ id: 'atk', x: ax, y: ay, r: c(40) }, { id: 'sk', i: 0, x: ax - c(86), y: ay + c(4), r: c(26) }, { id: 'sk', i: 1, x: ax - c(62), y: ay - c(62), r: c(26) }, { id: 'sk', i: 2, x: ax + c(4), y: ay - c(86), r: c(26) }, { id: 'dodge', x: ax - c(146), y: ay + c(14), r: c(24) }); }
  else { const s = 13 * UI.u, gap = 4 * UI.u, n = 4, x0 = W / 2 - (n * (s * 2 + gap) - gap) / 2 + s, y = H - s - 5 * UI.u;
    for (let i = 0; i < 3; i++) UI.btn.push({ id: 'sk', i, x: x0 + i * (s * 2 + gap), y, r: s, key: 'QER'[i], sq: true }); UI.btn.push({ id: 'dodge', x: x0 + 3 * (s * 2 + gap), y, r: s, key: 'SPACE', sq: true }); }
}
const DIG = { 0: '111101101101111', 1: '010110010010111', 2: '111001111100111', 3: '111001111001111', 4: '101101111001001', 5: '111100111001111', 6: '111100111101111', 7: '111001010010010', 8: '111101111101111', 9: '111101111001111', '+': '000010111010000', '!': '010010010000010', '-': '000000111000000' };
function pixText(g, txt, x, y, s, col, out = '#1a1024') {   /* 3x5 pixel digits, centred on x */
  const w = txt.length * 4 * s - s; let cx = Math.round(x - w / 2); y = Math.round(y);
  for (let pass = 0; pass < 2; pass++) { let px = cx; g.fillStyle = pass ? col : out;
    for (const ch of txt) { const d = DIG[ch]; if (d) for (let i = 0; i < 15; i++) if (d[i] === '1') { const qx = px + (i % 3) * s, qy = y + ((i / 3) | 0) * s; if (pass) g.fillRect(qx, qy, s, s); else g.fillRect(qx - 1, qy - 1, s + 2, s + 2); } px += 4 * s; } }
}
const ICONS = {
  atk: ['.........ww', '........wcw', '.......wcw.', '......wcw..', '.....wcw...', '.y..wcw....', '.yywcw.....', '..yyw......', '.byyy......', 'bb..yy.....', 'b..........'],
  0: ['....w......', '....w......', '..w.w.w....', '...www.....', '....w......', '...........', '.c.....c...', '..ccccc....', '.c.ccc.c...', 'c..c.c..c..', '...........'],
  1: ['...ccccc...', '..c.....c..', '.c..www..c.', '.c.w...w...', 'c..w.w.w..c', 'c..w...w..c', 'c...www...c', '...w.....c.', '.c......cc.', '..c....ccc.', '...cccc....'],
  2: ['......cc...', '.......cc..', '..w.....cc.', '...w.....cw', '....w....cw', '....w....cw', '....w....cw', '...w.....cw', '..w.....cc.', '.......cc..', '......cc...'],
  dodge: ['...........', '...........', '..ww.......', '....ww..w..', '.ww...www..', '....wwwww..', '.ww...www..', '....ww..w..', '..ww.......', '...........', '...........'],
};
const ICOL = { w: '#ffffff', c: '#5fdcff', y: '#ffc93c', b: '#8a5a2a' };
function icon(g, name, cx, cy, s, dim) { const p = ICONS[name]; if (!p) return; const x0 = Math.round(cx - 5.5 * s), y0 = Math.round(cy - 5.5 * s); g.globalAlpha = dim ? .35 : 1;
  for (let y = 0; y < 11; y++) for (let x = 0; x < 11; x++) { const ch = p[y][x]; if (ch !== '.') { g.fillStyle = ICOL[ch]; g.fillRect(x0 + x * s, y0 + y * s, s, s); } } g.globalAlpha = 1; }
function pixCircle(g, cx, cy, r, fill, edge) { cx = Math.round(cx); cy = Math.round(cy); r = Math.round(r);
  for (let y = -r; y <= r; y++) { const w = Math.round(Math.sqrt(r * r - y * y)); g.fillStyle = edge; g.fillRect(cx - w, cy + y, w * 2 + 1, 1); if (w > 1 && Math.abs(y) < r - 1) { const w2 = Math.round(Math.sqrt((r - 2) * (r - 2) - y * y)) || 0; g.fillStyle = fill; g.fillRect(cx - w2, cy + y, w2 * 2 + 1, 1); } } }
function bar(g, x, y, w, h, k, c1, c2, back = '#2a1830') { g.fillStyle = '#120a1c'; g.fillRect(x - 1, y - 1, w + 2, h + 2); g.fillStyle = back; g.fillRect(x, y, w, h); const f = Math.round(w * clamp(k, 0, 1)); g.fillStyle = c1; g.fillRect(x, y, f, h); g.fillStyle = c2; g.fillRect(x, y, f, Math.max(1, Math.round(h * .4))); }
const HT = [];   /* text jobs for the sharp canvas: [text, x, y (texels), size (css px), colour, align, weight] */
function T(txt, x, y, size, col = '#fff', align = 'left', wt = 800) { HT.push([txt, x, y, size, col, align, wt]); }
function drawHUD(dt) {
  const g = lo, W = UI.W, H = UI.H, u = UI.u; g.clearRect(0, 0, W, H); g.imageSmoothingEnabled = false; HT.length = 0;
  /* monster bars + numbers */
  for (const m of ACT) if (m.alive && m.hp < m.max && !m.d.boss) { const p = toLo(m.x, m.y + m.hW + .2 + m.jy, m.z), w = (m.d.big ? 30 : 14) * u; bar(g, Math.round(p[0] - w / 2), Math.round(p[1]), w, 2 * u, m.hp / m.max, '#ff5a4a', '#ffb09a'); }
  for (let i = POPS.length - 1; i >= 0; i--) { const q = POPS[i]; q.t += dt; const life = q.kind === 'crit' ? .9 : .7; if (q.t > life) { POPS.splice(i, 1); continue; }
    const k = q.t / life, p = toLo(q.x, q.y + .3 + (1 - (1 - k) * (1 - k)) * 1.1, q.z), big = q.kind === 'crit', s = u + (big ? (k < .15 ? 2 : 1) : 0);
    if (k > .8 && Math.floor(q.t * 30) % 2) continue;
    pixText(g, q.txt, p[0], p[1], s, q.kind === 'crit' ? '#ffd23c' : q.kind === 'hurt' ? '#ff5a5a' : q.kind === 'heal' ? '#7dff9a' : q.kind === 'warn' ? '#ff4a4a' : '#ffffff'); }
  if (!G.started) return;
  /* hero bars */
  const bx = 6 * u, by = 6 * u, bw = 66 * u; bar(g, bx, by, bw, 5 * u, P.hp / P.max, '#e8364a', '#ff8a8a'); bar(g, bx, by + 7 * u, bw, 2 * u, SAVE.xp / xpNeed(SAVE.lv), '#4ab8ff', '#b0e4ff', '#182840');
  T('Lv ' + SAVE.lv + '  ' + HERO.name, bx + bw + 4 * u, by + 5 * u, 13, '#fff'); T(Math.ceil(P.hp) + '/' + P.max, bx + 2 * u, by + 4.4 * u, 9.5, '#fff', 'left', 600);
  const ic = ICON.tex.image; g.drawImage(ic, 0, 0, 8, 8, bx, by + 12 * u, 8 * u, 8 * u); pixText(g, String(SAVE.gold), bx + 10 * u + String(SAVE.gold).length * 2 * u, by + 13 * u, u, '#ffd23c');
  /* sound switch */
  g.fillStyle = '#120a1c'; g.fillRect(W - 14 * u, 4 * u, 10 * u, 9 * u); g.fillStyle = SAVE.snd ? '#bfe8ff' : '#5a5068'; g.fillRect(W - 12 * u, 7 * u, 2 * u, 3 * u); g.fillRect(W - 10 * u, 6 * u, 2 * u, 5 * u); if (SAVE.snd) { g.fillRect(W - 7 * u, 6 * u, u, 5 * u); } else { g.fillStyle = '#ff5a5a'; g.fillRect(W - 7 * u, 7 * u, 2 * u, u); g.fillRect(W - 7 * u, 9 * u, 2 * u, u); }
  /* buttons */
  for (const b of UI.btn) { const cd = b.id === 'sk' ? P.cds[b.i] / SK[b.i].cd : b.id === 'dodge' ? P.dodgeCd / .85 : 0, down = (b.id === 'atk' && IN.atkId !== null) || (IN.sk && b.id === 'sk' && IN.sk.i === b.i);
    if (b.sq) { const s = b.r; g.fillStyle = '#120a1c'; g.fillRect(b.x - s - 1, b.y - s - 1, s * 2 + 2, s * 2 + 2); g.fillStyle = cd > 0 ? '#241a34' : '#3a2a58'; g.fillRect(b.x - s, b.y - s, s * 2, s * 2); g.fillStyle = cd > 0 ? '#2e2444' : '#5a4688'; g.fillRect(b.x - s, b.y - s, s * 2, u);
      icon(g, b.id === 'sk' ? b.i : b.id, b.x, b.y - u, Math.max(1, Math.round(s / 7)), cd > 0); if (cd > 0) { g.fillStyle = 'rgba(8,4,16,.6)'; const h = Math.round(s * 2 * cd); g.fillRect(b.x - s, b.y + s - h, s * 2, h); }
      T(b.key, b.x, b.y + s - 1.5 * u, b.key.length > 1 ? 8 : 10, cd > 0 ? '#8a80a0' : '#ffe9a8', 'center'); }
    else { pixCircle(g, b.x, b.y, b.r, down ? '#5a4688' : 'rgba(40,28,64,.72)', b.id === 'atk' ? '#ffe9a8' : cd > 0 ? '#4a4060' : '#8fd8ff');
      icon(g, b.id === 'sk' ? b.i : b.id, b.x, b.y, Math.max(1, Math.round(b.r / 9)), cd > 0);
      if (cd > 0) { g.fillStyle = 'rgba(8,4,16,.62)'; const h = Math.round(b.r * 2 * cd); g.save(); g.beginPath(); g.rect(b.x - b.r, b.y + b.r - h, b.r * 2, h); g.clip(); pixCircle(g, b.x, b.y, b.r - 1, 'rgba(8,4,16,.62)', 'rgba(8,4,16,.62)'); g.restore(); if (b.id === 'sk') T(Math.ceil(P.cds[b.i]) + '', b.x, b.y + 5 * u / 2, 15, '#fff', 'center'); } } }
  if (IN.joy) { const j = IN.joy, x0 = j.x0 / PX.T, y0 = j.y0 / PX.T, dx = j.x - j.x0, dy = j.y - j.y0, l = Math.hypot(dx, dy), m = Math.min(l, 44) / (l || 1) / PX.T; pixCircle(g, x0, y0, 46 / PX.T, 'rgba(30,22,50,.35)', 'rgba(160,220,255,.5)'); pixCircle(g, x0 + dx * m, y0 + dy * m, 18 / PX.T, 'rgba(150,215,255,.75)', '#ffffff'); }
  /* boss bar */
  const b = G.boss; if (b && b.alive) { const w = Math.min(W * .5, 150 * u), x = Math.round(W / 2 - w / 2), y = 14 * u; bar(g, x, y, w, 5 * u, b.hp / b.max, '#d83ad0', '#ff9aee'); T(b.d.name, W / 2, y - 3 * u, 14, '#ffd0f4', 'center'); }
}
function drawText(dt) {
  const g = hi, k = PX.k, d = PX.dpr; g.clearRect(0, 0, hiC.width, hiC.height); g.textBaseline = 'alphabetic'; g.lineJoin = 'round';
  for (const [txt, x, y, size, col, align, wt] of HT) { g.font = `${wt} ${Math.round(size * d)}px Kanit, sans-serif`; g.textAlign = align; g.lineWidth = Math.max(2, size * d * .22); g.strokeStyle = '#150c20'; g.strokeText(txt, x * k, y * k); g.fillStyle = col; g.fillText(txt, x * k, y * k); }
  const cw = hiC.width, ch = hiC.height, big = (txt, y, size, col, a) => { g.globalAlpha = a; g.font = `800 ${Math.round(size * d)}px Kanit, sans-serif`; g.textAlign = 'center'; g.lineWidth = size * d * .2; g.strokeStyle = '#150c20'; g.strokeText(txt, cw / 2, y); g.fillStyle = col; g.fillText(txt, cw / 2, y); g.globalAlpha = 1; };
  const S = Math.min(1.6, Math.max(.8, PX.SH / 420));
  if (!ready) { big('กำลังโหลด...', ch * .55, 20 * S, '#ffe9a8', 1); return; }
  if (!G.started) { g.fillStyle = 'rgba(12,8,24,.38)'; g.fillRect(0, 0, cw, ch); big('ผู้กล้าแดนพิกเซล', ch * .36, 44 * S, '#ffe27a', 1); big('เก็บเลเวล ล่าฝูงอสูร ปราบมังกรราตรี', ch * .36 + 30 * S * d, 15 * S, '#d8f0ff', 1);
    big(Math.floor(G.time * 2) % 2 ? '' : 'แตะหรือคลิกเพื่อเริ่ม', ch * .7, 20 * S, '#ffffff', 1);
    g.fillStyle = 'rgba(12,8,24,.6)'; g.fillRect(0, ch * .82, cw, ch * .18); big('PC: WASD เดิน · คลิกซ้ายตี · Q E R สกิล · Space หลบ', ch * .885, 11.5 * S, '#d8e4ff', 1); big('มือถือ: ลากซ้ายเดิน · ปุ่มขวาตี/สกิล · ลากปุ่มสกิลเพื่อเล็งจุด', ch * .955, 11.5 * S, '#d8e4ff', 1); return; }
  const bn = G.banner; if (bn) { bn.t += dt; const a = clamp(Math.min(bn.t / .4, (3 - bn.t) / .6), 0, 1), z = ZONES[bn.z]; big(z.name, ch * .2, 26 * S, z.col, a); big(z.sub, ch * .2 + 22 * S * d, 13 * S, '#ffffff', a * .9); if (bn.t > 3) G.banner = null; }
  const ms = G.msg; if (ms) { ms.t += dt; const a = clamp(Math.min(ms.t / .2, (ms.life - ms.t) / .5), 0, 1); big(ms.txt, ch * (ms.big ? .4 : .46), (ms.big ? 30 : 18) * S, ms.col || (ms.big ? '#ffe27a' : '#ffffff'), a); if (ms.t > ms.life) G.msg = null; }
}

/* ---------- loop */
let last = performance.now(), ready = false, saveT = 0;
const _c1 = new THREE.Color(), _c2 = new THREE.Color(), _sv = new V3();
function zoneLook(dt) {   /* light and grade follow the zone: warm afternoon -> golden autumn -> moonlit woods */
  const m = mapAt(P.x, P.z), k = Math.min(1, dt * 1.6); G.glow += (m[1] - G.glow) * k; G.au += (m[0] - G.au) * k; const g = G.glow, a = G.au;
  sun.intensity = lerp(.62, .34, g); sun.color.copy(_c1.set(0xfff0d0)).lerp(_c2.set(0xffd9a0), a).lerp(_c2.set(0x9db8ff), g);
  hemi.color.copy(_c1.set(0xa9b6ff)).lerp(_c2.set(0x6a72e0), g); hemi.groundColor.copy(_c1.set(0x8a7a92)).lerp(_c2.set(0x4a3f78), g);
  postMat.uniforms.uGrade.value.set(lerp(lerp(1, 1.05, a), .88, g), lerp(1, .92, g), lerp(lerp(1, .93, a), 1.12, g));
  SPRTINT.value.setRGB(lerp(1, .74, g), lerp(1, .8, g), lerp(lerp(1, .95, a), 1, g));
  const z = zoneAt(P.x, P.z); if (z !== G.zone) { G.zone = z; if (G.started) G.banner = { z, t: 0 }; }
  if (z === 0 && !P.dead && P.hp < P.max) P.hp = Math.min(P.max, P.hp + P.max * .25 * dt);
}
function tick(dt) {
  G.time += dt; TIMEU.value = G.time; readInput();
  let g = dt; if (G.stop > 0) { G.stop -= dt; g = dt * .05; }
  if (!G.started) { IN.mx = IN.mz = 0; IN.atk = false; }
  updHero(g);
  if (G.started) { updPacks(g); for (let i = ACT.length - 1; i >= 0; i--) updMob(ACT[i], g); updProj(g); updPick(g); updTimers(g); }
  const hw = PX.bw * TW / 2, hd = PX.bh * TW / 2 / SP, tx = clamp(P.x + IN.mx * 1.6, -62 + hw, 62 - hw), tz = clamp(P.z - 1.1 + IN.mz * 1.2, -60 + hd, 58 - hd * .6), k = 1 - Math.exp(-dt * 7);
  CAMT.x += (tx - CAMT.x) * k; CAMT.z += (tz - CAMT.z) * k; CAMT.y += (P.y - CAMT.y) * k;
  zoneLook(dt); GRASSU.uCam.value.set(CAMT.x, CAMT.z); GRASSU.uHero.value.set(P.x, P.y, P.z);
  updFx(g); updAmbient(dt, P.x, P.z); PA.update(g); PN.update(g); updLights(g); updShake(dt); updAim();
  postMat.uniforms.uDark.value += ((P.dead ? .8 : 0) - postMat.uniforms.uDark.value) * Math.min(1, dt * 3);
  placeCamera(); placeSun(); cullChunks();
  _sv.set(P.x, P.y + 1.1 + P.jy, P.z).project(cam); SEEU.uSee.value.set((_sv.x * .5 + .5) * PX.bw, (_sv.y * .5 + .5) * PX.bh, _sv.z * .5 + .5); SEEU.uSeeR.value = 30;
  saveT += dt; if (saveT > 6) { saveT = 0; if (G.started) saveGame(); }
}
function frame(now) { requestAnimationFrame(frame); const dt = Math.min(.05, (now - last) / 1000); last = now; if (!ready) { drawText(dt); return; } tick(dt); renderFrame(); drawHUD(dt); drawText(dt); }
function startGame(touch) { if (!ready || G.started) return; audioOn(); G.started = true; G.zone = -1; if (touch) { IN.touch = true; layoutUI(); const el = document.documentElement; try { (el.requestFullscreen || el.webkitRequestFullscreen || (() => { })).call(el).catch(() => { }); } catch (e) { } } }
const MOBSHEETS = ['mob_mush', 'mob_slime', 'mob_wolf', 'mob_goblin', 'mob_ghost', 'mob_skel', 'mob_king', 'mob_dragon'];
async function boot() {
  resize(); loadSave(); try { await document.fonts.load('800 20px Kanit', 'ก'); } catch (e) { }
  await Promise.all([loadProps(), loadSheet('hero_sword'), ...MOBSHEETS.map(n => loadSheet(n).catch(() => console.warn('no sheet yet:', n)))]);
  buildWorld(); buildAmbientFx(); warmFx();
  const M = SHEETS.hero_sword.meta; P.spr = new Spr(SHEETS.hero_sword, M.cell, M.cell, M.ax, M.ay); scene.add(P.spr.o);
  calcStats(); P.hp = P.max; P.y = groundH(P.x, P.z); CAMT.set(P.x, P.y, P.z - 1.1); layoutUI(); ready = true;
  if (Q.get('auto') === '1') startGame(Q.get('touch') === '1');
}
window.QG = { P, G, IN, PX, ACT, PACKS, SK, get SAVE() { return SAVE; }, go: (x, z) => { P.x = x; P.z = z; CAMT.set(x, groundH(x, z), z - 1.1); }, start: startGame, atk: attack, skill: trySkill, dodge,
  sim: (sec, dt = 1 / 30) => { for (let t = 0; t < sec; t += dt) tick(dt); renderFrame(); drawHUD(dt); drawText(dt); }, err: [] };
addEventListener('error', e => { QG.err.push(e.message + ' @' + (e.filename || '').split('/').pop() + ':' + e.lineno); });
boot().catch(e => { console.error(e); QG.err.push('boot: ' + e.message); });
requestAnimationFrame(frame);
