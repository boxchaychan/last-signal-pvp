/* bag3d.html: ITEM SKILL EFFECTS (owner 2026-11-27 "ไอเท็มก็ออกคล้ายสกิล คือให้มันมีเอฟเฟคเฉพาะออกมา").
   Every item that fires in a fight (weapons, shields, food, start-of-fight items) casts its OWN effect, like a small skill:
   CAST[id] = [move, options] for attacks, CASTSELF[id] for shields / food. A move is a function in CASTFX / SELFFX that draws on the
   2D battle layer with the page's particle list (sp / vfx in bag3d.html) plus `fn` particles (own draw + own movement).
   All made in code, no art files. Loaded by bag3d.html before its game script; uses its globals at call time (sp, vfx, geo, glw, ICON, IT).
   Sizes: u = screen height / 390; wt = weight of the item (slow heavy items = bigger effect). Each attack move returns the seconds until
   it lands, so the page shows the damage number and the hit flash at that moment. */
const cR = (a, c) => a + Math.random() * (c - a);
function castKit(b, s) {   /* s = the side that casts: 0 our champion (left), 1 the enemy (right) */
  const G = geo(), W = G.W, H = G.H, dpr = devicePixelRatio || 1;
  return { b, s, T: 1 - s, W, H, u: H / 390 * 1.5, d: s ? -1 : 1, cx: W * (s ? .74 : .26), tx: W * (s ? .26 : .74), by: G.gy - H * .15, fy: G.gy + 2,
    py: G.gy - 150 * Math.max(1, Math.round(H * dpr / 400)) / dpr - 10 };   /* py = where the item icon pops up above its owner */
}
/* ---- small emitters ---- */
function cGlow(b, x, y, s0, s1, life, c, t0, o) { sp(b, Object.assign({ k: 'glow', x, y, s: s0, s1, life, c, t: -(t0 || 0) }, o)); }
function cRing(b, x, y, r, life, c, w, t0) { sp(b, { k: 'ring', x, y, s: r * .15, s1: r, life, c, w: w || 3, t: -(t0 || 0) }); }
function cFlare(b, x, y, s0, s1, life, c, rot, t0) { sp(b, { k: 'flare', x, y, s: s0, s1, life, c, rot: rot || 0, t: -(t0 || 0) }); }
function cSparks(b, x, y, n, c, v, life, dir, spread, u, grav) { for (let i = 0; i < n; i++) { const a = dir + cR(-spread, spread), sv = cR(.35, 1) * v; sp(b, { k: 'streak', x, y, vx: Math.cos(a) * sv, vy: Math.sin(a) * sv, g: (grav == null ? 500 : grav) * u, dr: 3, life: cR(life * .6, life), s: cR(1.5, 3) * u, c }); } }
function cSmoke(b, x, y, n, sz, life, u) { for (let i = 0; i < n; i++) sp(b, { k: 'smoke', x: x + cR(-24, 24) * u, y: y + cR(-8, 8) * u, vx: cR(-50, 50) * u, vy: cR(-50, -8) * u, life: cR(life, life * 1.5), s: sz * .35 * u, s1: sz * u, add: 0, a: .8 }); }
function cFn(b, o) { b.px.push(Object.assign({ t: 0, life: .3, s: 0, s1: 0, a: 1, g: 0, dr: 0, vx: 0, vy: 0, rot: 0, vr: 0, x: 0, y: 0, k: 'fn', c: '255,255,255', add: 1 }, o)); }   /* o.fn(g, p, q) draws (q = 0..1 of its life), o.mv(p, q, dt) moves, o.then() at the end */
function cAt(b, t0, f) { if (t0 <= 0) f(); else cFn(b, { life: t0, then: f }); }
/* ---- shapes ---- */
function cresPath(g, r, d) { const a = Math.acos(-d / (2 * r)), a2 = Math.acos(d / (2 * r)); g.beginPath(); g.arc(0, 0, r, -a, a); g.arc(-d, 0, r, a2, -a2, true); g.closePath(); }
function drawCres(g, x, y, r, rot, flip, thick, col, al, sy) {   /* a crescent blade of light, leading edge to the right (flip -1 = to the left) */
  if (al <= 0 || r <= 1) return; g.save(); g.translate(x, y); g.rotate(rot); g.scale(flip, sy || 1);
  g.globalCompositeOperation = 'source-over'; g.globalAlpha = al * .3; g.fillStyle = '#140a1e'; cresPath(g, r * 1.06, thick * 1.5); g.fill();   /* a dark backing so it reads on a bright sky */
  g.globalCompositeOperation = 'lighter'; g.fillStyle = `rgb(${col})`; g.globalAlpha = al * .35; cresPath(g, r * 1.1, thick * 1.8); g.fill();
  g.globalAlpha = al * .9; cresPath(g, r, thick); g.fill(); g.globalAlpha = al; g.fillStyle = '#fff'; cresPath(g, r * .985, thick * .4); g.fill(); g.restore();
}
function drawCut(g, x, y, L, w, rot, col, al) {   /* a tapered cut line */
  if (al <= 0) return; g.save(); g.translate(x, y); g.rotate(rot);
  g.globalCompositeOperation = 'source-over'; g.globalAlpha = al * .3; g.fillStyle = '#140a1e'; g.beginPath(); g.moveTo(-L, 0); g.quadraticCurveTo(0, -w * 2.2, L, 0); g.quadraticCurveTo(0, w * 2.2, -L, 0); g.fill();
  g.globalCompositeOperation = 'lighter';
  for (const [k2, c, a2] of [[1.7, col, .45], [1, col, .95], [.4, '255,255,255', 1]]) { g.globalAlpha = al * a2; g.fillStyle = `rgb(${c})`; g.beginPath(); g.moveTo(-L, 0); g.quadraticCurveTo(0, -w * k2, L, 0); g.quadraticCurveTo(0, w * k2, -L, 0); g.fill(); }
  g.restore();
}
function drawIco(g, id, x, y, z, rot, al, col, flip) {   /* the item's own icon as a glowing ghost */
  if (!ICON.width || al <= 0) return; const i = IT[id].i; g.save(); g.translate(x, y);
  if (col) { g.globalCompositeOperation = 'lighter'; g.globalAlpha = al * .7; g.drawImage(glw(col), -z * .8, -z * .8, z * 1.6, z * 1.6); }
  g.globalCompositeOperation = 'source-over'; g.globalAlpha = al; if (flip) g.scale(-1, 1); g.rotate(rot); g.drawImage(ICON, i % 8 * 64, (i >> 3) * 64, 64, 64, -z / 2, -z / 2, z, z); g.restore();
}
function drawStar(g, x, y, r, r2, n, rot, fill, al) { g.save(); g.translate(x, y); g.rotate(rot); g.globalAlpha = al; g.fillStyle = fill; g.beginPath(); for (let i = 0; i < n * 2; i++) { const a = i * Math.PI / n, R2 = i % 2 ? r2 : r; g.lineTo(Math.cos(a) * R2, Math.sin(a) * R2); } g.closePath(); g.fill(); g.restore(); }
function drawSkull(g, x, y, r, col, al) { g.save(); g.translate(x, y); g.globalCompositeOperation = 'lighter'; g.globalAlpha = al * .6; g.drawImage(glw(col), -r * 2, -r * 2, r * 4, r * 4);
  g.globalCompositeOperation = 'source-over'; g.globalAlpha = al; g.fillStyle = '#f2ecff'; g.beginPath(); g.arc(0, -r * .1, r, 0, 6.283); g.fill(); g.fillRect(-r * .55, r * .5, r * 1.1, r * .55);
  g.fillStyle = '#1a0a26'; g.beginPath(); g.arc(-r * .38, -r * .1, r * .27, 0, 6.283); g.arc(r * .38, -r * .1, r * .27, 0, 6.283); g.fill(); g.fillRect(-r * .08, r * .3, r * .16, r * .3); for (const q of [-.3, 0, .3]) g.fillRect(r * q - r * .03, r * .62, r * .06, r * .42); g.restore(); }
function drawRune(g, x, y, r, rot, col, al, n) {   /* a magic circle lying on the ground */
  if (al <= 0) return; g.save(); g.translate(x, y); g.scale(1, .34); g.globalCompositeOperation = 'lighter'; g.strokeStyle = `rgb(${col})`; g.globalAlpha = al; g.lineWidth = Math.max(1, r * .05);
  g.beginPath(); g.arc(0, 0, r, 0, 6.283); g.stroke(); g.beginPath(); g.arc(0, 0, r * .78, 0, 6.283); g.stroke(); g.rotate(rot); n = n || 3;
  for (let k = 0; k < 2; k++) { g.beginPath(); for (let i = 0; i <= n; i++) { const a = i * 6.283 / n + k * Math.PI / n; g.lineTo(Math.cos(a) * r * .78, Math.sin(a) * r * .78); } g.stroke(); }
  g.globalAlpha = al * .25; g.fillStyle = `rgb(${col})`; g.beginPath(); g.arc(0, 0, r, 0, 6.283); g.fill(); g.restore();
}
/* ---- pieces shared by several moves ---- */
function cutMark(K, c, L, rot, t0, w) { const { b, u } = K, x = K.tx, y = K.by; cFn(b, { t: -(t0 || 0), life: .24, fn(g, p, q) { const grow = Math.min(1, q / .25), al = q > .45 ? (1 - q) / .55 : 1; drawCut(g, x, y, L * u * (.25 + .75 * grow), (w || 5) * u * (1 - q * .5), rot, c, al); } }); }
function hitSpark(K, c, n, big) { const { b, u } = K; cGlow(b, K.tx, K.by, 16 * u, (big ? 62 : 44) * u, .16, c); cSparks(b, K.tx, K.by, n, c, (big ? 340 : 250) * u, .3, K.d > 0 ? 0 : Math.PI, 1.2, u); }
function groundCrack(K, c, r, t0) { const { b, u } = K, x = K.tx, y = K.fy, rays = Array.from({ length: 7 }, (_, i) => { const a = i / 7 * 6.283 + cR(-.3, .3), pts = [[0, 0]]; let px = 0, py = 0; for (let j = 1; j <= 4; j++) { px += Math.cos(a + cR(-.5, .5)) * r / 4; py += Math.sin(a + cR(-.5, .5)) * r / 4; pts.push([px, py]); } return pts; });
  cFn(b, { t: -(t0 || 0), life: .7, fn(g, p, q) { const grow = Math.min(1, q / .15), al = q > .5 ? (1 - q) / .5 : 1; g.translate(x, y); g.scale(1, .34);
    for (const [wd, col, a2, op] of [[5, '20,10,10', .7, 'source-over'], [2, c, 1, 'lighter']]) { g.globalCompositeOperation = op; g.globalAlpha = al * a2; g.strokeStyle = `rgb(${col})`; g.lineWidth = wd * u; g.lineJoin = 'round'; for (const pts of rays) { g.beginPath(); pts.forEach(([px, py], i) => i ? g.lineTo(px * u * grow, py * u * grow) : g.moveTo(0, 0)); g.stroke(); } } } }); }
function spikes(K, c, n, h, t0, x, edge) {   /* spikes burst out of the ground */
  const { b, u } = K, y = K.fy, X = x == null ? K.tx : x, list = Array.from({ length: n }, (_, i) => ({ dx: (i - (n - 1) / 2) * 15 * u + cR(-4, 4) * u, h: h * u * cR(.6, 1.15), w: cR(6, 10) * u, lean: cR(-.25, .25), d: i * .012 }));
  cFn(b, { t: -(t0 || 0), life: .6, fn(g, p, q) { g.translate(X, y); for (const S of list) { const t = q * .6 - S.d, up = Math.max(0, Math.min(1, t / .08)), al = q > .6 ? (1 - q) / .4 : 1, hh = S.h * (1 - (1 - up) * (1 - up));
      g.globalCompositeOperation = 'source-over'; g.globalAlpha = al * .85; g.fillStyle = `rgb(${c})`; g.strokeStyle = edge || 'rgba(110,190,255,.95)'; g.lineWidth = 1.2; g.beginPath(); g.moveTo(S.dx - S.w, 0); g.lineTo(S.dx + S.lean * hh, -hh); g.lineTo(S.dx + S.w, 0); g.closePath(); g.fill(); g.stroke();
      g.globalAlpha = al * .7; g.fillStyle = '#fff'; g.beginPath(); g.moveTo(S.dx - S.w * .2, 0); g.lineTo(S.dx + S.lean * hh, -hh); g.lineTo(S.dx + S.w * .3, 0); g.closePath(); g.fill(); } } }); }
function column(K, x, c, w, t0, life, top) {   /* a pillar of light from the sky (top = 0) or from the ground upward */
  const { b, u } = K, y1 = K.fy, y0 = top == null ? -10 : top; cFn(b, { t: -(t0 || 0), life: life || .4, fn(g, p, q) { const al = q < .15 ? q / .15 : 1 - (q - .15) / .85, ww = w * u * (1 + q * .3); g.globalCompositeOperation = 'lighter';
    for (const [k2, col, a2] of [[1, c, .45], [.5, c, .6], [.18, '255,255,255', .9]]) { const gr = g.createLinearGradient(x - ww * k2, 0, x + ww * k2, 0); gr.addColorStop(0, `rgba(${col},0)`); gr.addColorStop(.5, `rgba(${col},${a2})`); gr.addColorStop(1, `rgba(${col},0)`); g.globalAlpha = al; g.fillStyle = gr; g.fillRect(x - ww * k2, y0, ww * k2 * 2, y1 - y0); } } }); }
function fly(K, o) {   /* something that flies from A to B: o = { x0, y0, x1, y1, dur, t0, arc, draw(g, x, y, ang, q), trail(x, y, q), then() } */
  cFn(K.b, { t: -(o.t0 || 0), life: o.dur, x: o.x0, y: o.y0, ang: Math.atan2(o.y1 - o.y0, o.x1 - o.x0),
    mv(p, q) { const e = o.ease ? o.ease(q) : q, nx = o.x0 + (o.x1 - o.x0) * e, ny = o.y0 + (o.y1 - o.y0) * e - Math.sin(q * Math.PI) * (o.arc || 0); if (nx !== p.x || ny !== p.y) p.ang = Math.atan2(ny - p.y, nx - p.x); p.x = nx; p.y = ny; if (o.trail) o.trail(nx, ny, q); },
    fn(g, p, q) { o.draw(g, p.x, p.y, p.ang, q); }, then: o.then });
}
function healGlow(K, c, k) { const { b, u } = K; cGlow(b, K.cx, K.by, 30 * u * k, 62 * u * k, .45, c, 0, { a: .55 }); sp(b, { k: 'beam', x: K.cx, y: K.fy, s: 34 * u * k, s1: 34 * u * k, life: .5, c }); }   /* a soft light on the one who is healed */
function drainBack(K, c, n) { const { b, u } = K; for (let i = 0; i < (n || 5); i++) sp(b, { k: 'orb', x: K.tx, y: K.by, x0: K.tx, y0: K.by, x1: K.cx, y1: K.by, t: -i * .05, life: .42, s: 6 * u, s1: 6 * u, c, arc: cR(-60, -20) * u }); }
function shake(b, v, punch) { b.sh = Math.max(b.sh, v); if (punch) b.punch = Math.max(b.punch || 0, punch); }

/* ---- ATTACK MOVES: (K kit, o options, e hit event, wt weight, n2 = which hit of a multi-hit item) -> seconds until it lands ---- */
const CASTFX = {
  wave(K, o, e, wt) {   /* a crescent blade wave flies across (sword; fire = flame sword) */
    const { b, u, d } = K, r = 30 * u * wt, dur = .19, x0 = K.cx + d * 44 * u, x1 = K.tx - d * 6 * u, y = K.by - 2 * u, tilt = cR(-.22, .22);
    cFn(b, { life: dur + .09, x: x0, mv(p, q) { const m = Math.min(1, q * (dur + .09) / dur); p.x = x0 + (x1 - x0) * (1 - (1 - m) * (1 - m)); if (o.fire) cGlow(b, p.x - d * 12 * u, y + cR(-r, r) * .8, cR(8, 15) * u, 2 * u, cR(.2, .4), Math.random() < .5 ? '255,120,30' : '255,200,90', 0, { vy: -70 * u }); },
      fn(g, p, q) { const al = q > .68 ? (1 - q) / .32 : 1, gr = .55 + .45 * Math.min(1, q * 3); for (let i = 2; i >= 0; i--) drawCres(g, p.x - d * i * 12 * u, y, r * gr * (1 - i * .09), tilt, d, r * .36, o.c, al * (i ? .3 / i : 1), 1.3); } });
    cAt(b, dur, () => { cutMark(K, o.c, 46 * wt, (d > 0 ? -.55 : .55) + tilt, 0, 5); hitSpark(K, o.c, 7, e.big); if (o.fire) vfx(b, 'fire', K.T); }); return dur; },
  stab(K, o, e, wt) {   /* quick double cut from the shadows (dagger; drip = venom knife) */
    const { b, u, d } = K, n = o.n || 2; cFn(b, { life: .14, fn(g, p, q) { drawCut(g, (K.cx + K.tx) / 2, K.by, Math.abs(K.tx - K.cx) * .5 * Math.min(1, q * 2.5), 2.2 * u, 0, o.c, (1 - q) * .55); } });
    for (let i = 0; i < n; i++) cutMark(K, o.c, 38 * wt, (i % 2 ? .95 : -.95) * d, .05 + i * .07, 4.5);
    cAt(b, .06, () => { hitSpark(K, o.c, 4); if (o.drip) for (let i = 0; i < 7; i++) sp(b, { k: 'drop', x: K.tx + cR(-10, 10) * u, y: K.by + cR(-10, 10) * u, vx: cR(-70, 70) * u, vy: cR(-150, -20) * u, g: 650 * u, life: cR(.4, .7), s: cR(2.5, 5) * u, s1: 1.5 * u, c: o.drip }); }); return .06; },
  iai(K, o, e, wt) {   /* wind blade: one thin line, then the cut opens (katana) */
    const { b, u, d } = K; cFlare(b, K.cx + d * 20 * u, K.by, 6 * u, 28 * u, .12, o.c, .4);
    cFn(b, { life: .34, fn(g, p, q) { const L = 86 * u * wt; drawCut(g, K.tx, K.by, L * Math.min(1, q / .1), (q < .35 ? 2 : 8 * (1 - q)) * u, d * -.12, q < .35 ? '255,255,255' : o.c, q > .7 ? (1 - q) / .3 : 1); } });
    cAt(b, .13, () => { hitSpark(K, o.c, 5, e.big); for (let i = 0; i < 6; i++) sp(b, { k: 'streak', x: K.tx + cR(-30, 30) * u, y: K.by + cR(-24, 24) * u, vx: d * cR(220, 420) * u, vy: cR(-30, 30) * u, dr: 4, life: cR(.2, .35), s: cR(1.2, 2.2) * u, c: o.c }); }); return .13; },
  cleave(K, o, e, wt) {   /* a giant blade of darkness comes down (greatsword) */
    const { b, u } = K, r = 50 * u * wt, y0 = K.by - 130 * u, y1 = K.fy - 20 * u, dur = .12, t0 = .1; cGlow(b, K.tx, y0, 10 * u, 40 * u, .2, o.c);
    cFn(b, { t: -t0, life: dur + .14, y: y0, mv(p, q) { const m = Math.min(1, q * (dur + .14) / dur); p.y = y0 + (y1 - y0) * m * m; }, fn(g, p, q) { const al = q > .55 ? (1 - q) / .45 : 1; for (let i = 2; i >= 0; i--) drawCres(g, K.tx, p.y - i * 16 * u, r * (1 - i * .08), Math.PI / 2, 1, r * .42, o.c, al * (i ? .3 / i : 1), 1.15); } });
    cAt(b, t0 + dur, () => { groundCrack(K, o.c, 70 * wt); cRing(b, K.tx, K.fy, 100 * u, .42, o.c, 5 * u); hitSpark(K, o.c, 10, 1); cSmoke(b, K.tx, K.fy - 4 * u, 4, 34, .6, u); shake(b, .2, .5); }); return t0 + dur; },
  guillotine(K, o, e, wt, n2, id) {   /* the executioner's blade falls from the sky */
    const { b, u, d } = K, z = 86 * u, y0 = -z, y1 = K.by - 6 * u, dur = .2, t0 = .06; column(K, K.tx, o.c, 10, 0, .3);
    fly(K, { x0: K.tx, y0, x1: K.tx, y1, dur, t0, ease: q => q * q, draw(g, x, y) { drawIco(g, id, x, y, z, 2.36, 1, o.c, d < 0); for (let i = 1; i < 4; i++) drawIco(g, id, x, y - i * 22 * u, z, 2.36, .22 / i, null, d < 0); },
      then() { cutMark(K, o.c, 70, 1.57, 0, 7); cutMark(K, o.c, 44, .7, .05, 5); cutMark(K, o.c, 44, -.7, .05, 5); vfx(b, 'blood', K.T, { big: 1 }); groundCrack(K, o.c, 60); cRing(b, K.tx, K.fy, 110 * u, .45, o.c, 5 * u); shake(b, .25, .7); } }); return t0 + dur; },
  xcut(K, o, e, wt, n2) {   /* crossing cuts, one for each blade (twin blades; storm = lightning blades) */
    const { b, u, d } = K, t0 = n2 ? .09 : 0, rot = (n2 % 2 ? .72 : -.72) * d; cutMark(K, o.c, 44 * wt, rot, t0, 5);
    cFn(b, { t: -t0, life: .16, fn(g, p, q) { drawCres(g, K.tx - d * 20 * u * (1 - q), K.by, 26 * u, rot * .6, d, 9 * u, o.c, 1 - q, 1.2); } });
    cAt(b, t0 + .04, () => { hitSpark(K, o.c, 4); if (o.storm) { sp(b, { k: 'bolt', pts: Array.from({ length: 6 }, (_, i) => [K.tx + cR(-22, 22) * u, K.by - 46 * u + i * 18 * u]), life: .16, s: 3 * u, s1: 3 * u, c: '190,220,255' }); for (let i = 0; i < 5; i++) sp(b, { k: 'streak', x: K.tx, y: K.by + cR(-20, 20) * u, vx: cR(-1, 1) * 260 * u, vy: cR(-160, -40) * u, dr: 3, life: .3, s: 2 * u, c: '170,235,255' }); } }); return t0 + .04; },
  thrust(K, o, e, wt) {   /* a flurry of needle thrusts (rapier; luck = lucky rapier) */
    const { b, u, d } = K, n = o.n || 3; for (let i = 0; i < n; i++) { const dy = (i - (n - 1) / 2) * 13 * u + cR(-4, 4) * u, t0 = i * .05;
      cFn(b, { t: -t0, life: .15, fn(g, p, q) { const x0 = K.tx - d * 110 * u, L = 62 * u; drawCut(g, x0 + d * (40 + 100 * Math.min(1, q * 2.2)) * u, K.by + dy, L, 3.6 * u, 0, o.c, q > .5 ? (1 - q) * 2 : 1); } });
      cAt(b, t0 + .06, () => { cGlow(b, K.tx, K.by + dy, 6 * u, 22 * u, .14, o.c); cSparks(b, K.tx, K.by + dy, 2, o.c, 220 * u, .22, d > 0 ? 0 : Math.PI, .5, u); }); }
    if (o.luck) cAt(b, .1, () => { for (let i = 0; i < 5; i++) sp(b, { k: 'plus', x: K.tx + cR(-26, 26) * u, y: K.by + cR(-26, 20) * u, vy: cR(-70, -30) * u, life: cR(.4, .7), s: cR(3, 5) * u, s1: 1, c: i % 2 ? '150,255,120' : '255,230,120' }); }); return .08; },
  pierce(K, o, e, wt) {   /* a lance of light goes straight through (spear; ice = frost lance) */
    const { b, u, d } = K, dur = .13, x0 = K.cx + d * 30 * u, x1 = K.tx + d * 90 * u, y = K.by; let done = 0;
    fly(K, { x0, y0: y, x1, y1: y, dur, draw(g, x, yy, a, q) { drawCut(g, x - d * 46 * u, yy, 70 * u * wt, 4.5 * u, 0, o.c, 1); g.save(); g.translate(x, yy); g.scale(d, 1); g.globalCompositeOperation = 'lighter'; g.fillStyle = '#fff'; g.beginPath(); g.moveTo(26 * u, 0); g.lineTo(-4 * u, -8 * u); g.lineTo(2 * u, 0); g.lineTo(-4 * u, 8 * u); g.closePath(); g.fill(); g.restore(); },
      trail(x) { if (!done && (d > 0 ? x >= K.tx : x <= K.tx)) { done = 1; for (let i = 0; i < 2; i++) cFn(b, { t: -i * .05, life: .28, fn(g, p, q) { g.globalCompositeOperation = 'lighter'; g.globalAlpha = 1 - q; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 3 * u * (1 - q); g.beginPath(); g.ellipse(K.tx + d * i * 16 * u, y, (6 + q * 10) * u, (14 + q * 26) * u, 0, 0, 6.283); g.stroke(); } });
          cSparks(b, K.tx, y, 8, o.c, 360 * u, .3, d > 0 ? 0 : Math.PI, .35, u, 200); if (o.ice) { spikes(K, '215,245,255', 5, 38); vfx(b, 'ice', K.T); } } } });
    const tl = Math.abs(K.tx - x0) / Math.abs(x1 - x0) * dur; return tl; },
  toss(K, o, e, wt, n2, id) {   /* the weapon itself is thrown (axe spins, javelin flies straight; blood = blood axe) */
    const { b, u, d } = K, z = 52 * u * wt, dur = o.spin ? .26 : .17, x0 = K.cx + d * 20 * u, y0 = K.py + 12 * u, x1 = K.tx, y1 = K.by; let sp0 = cR(0, 6);
    fly(K, { x0, y0, x1, y1, dur, arc: o.spin ? 26 * u : 4 * u, draw(g, x, y, a, q) { if (o.spin) drawIco(g, id, x, y, z, d * (sp0 + q * 15), 1, o.c); else { g.save(); g.translate(x, y); g.scale(d, 1); g.rotate(Math.atan2(y1 - y0, Math.abs(x1 - x0)) + .78); g.globalCompositeOperation = 'lighter'; g.globalAlpha = .6; g.drawImage(glw(o.c), -z * .7, -z * .7, z * 1.4, z * 1.4); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; const i = IT[id].i; if (ICON.width) g.drawImage(ICON, i % 8 * 64, (i >> 3) * 64, 64, 64, -z / 2, -z / 2, z, z); g.restore(); } },
      trail(x, y) { cGlow(b, x, y, 9 * u, 2 * u, .16, o.c); },
      then() { if (o.chop) { cutMark(K, o.c, 50 * wt, d * -.9, 0, 6); cSparks(b, K.tx, K.by, 9, o.c, 320 * u, .32, d > 0 ? 0 : Math.PI, 1.3, u); } else { hitSpark(K, o.c, 7, e.big); cSmoke(b, K.tx, K.by + 10 * u, 2, 22, .4, u); } if (o.blood) { vfx(b, 'blood', K.T); if (e.crit || Math.random() < .4) drainBack(K, '255,50,80'); } } }); return dur; },
  slam(K, o, e, wt, n2, id) {   /* the hammer drops on the enemy's head (bolt = thunder hammer) */
    const { b, u, d } = K, z = 70 * u * wt, dur = .16, t0 = .08, x0 = K.tx - d * 34 * u, y0 = K.by - 150 * u, y1 = K.by - 16 * u; cGlow(b, x0, y0, 10 * u, 44 * u, .2, o.c);
    fly(K, { x0, y0, x1: K.tx, y1, dur, t0, ease: q => q * q * q, draw(g, x, y, a, q) { drawIco(g, id, x, y, z, d * (-1.3 + q * 2.6), 1, o.c, d < 0); },
      then() { vfx(b, 'smash', K.T, { big: 1 }); groundCrack(K, o.c, 72 * wt); if (o.bolt) { vfx(b, 'bolt', K.T); cRing(b, K.tx, K.fy, 130 * u, .5, o.c, 4 * u, .06); } shake(b, o.bolt ? .28 : .2, o.bolt ? .7 : .45); } }); return t0 + dur; },
  bonk(K, o, e, wt, n2, id) {   /* a short heavy swing and a "pow" star (nail club) */
    const { b, u, d } = K, z = 46 * u, px = K.tx - d * 40 * u, py = K.by + 14 * u, dur = .15;
    cFn(b, { life: dur + .08, fn(g, p, q) { const m = Math.min(1, q * (dur + .08) / dur), a = -2 + m * m * 2.3, al = q > .75 ? (1 - q) * 4 : 1; g.save(); g.translate(px, py); g.scale(d, 1); g.rotate(a); drawIco(g, id, 34 * u, -8 * u, z, .3, al, o.c); g.restore(); } });
    cAt(b, dur, () => { cFn(b, { life: .22, fn(g, p, q) { g.globalCompositeOperation = 'source-over'; drawStar(g, K.tx, K.by - 4 * u, (16 + 26 * Math.min(1, q * 4)) * u, (8 + 10 * Math.min(1, q * 4)) * u, 7, .3, '#fff6c8', q > .5 ? (1 - q) * 2 : 1); } });
      for (let i = 0; i < 6; i++) sp(b, { k: 'shard', x: K.tx, y: K.by, vx: cR(-200, 200) * u, vy: cR(-260, -60) * u, g: 800 * u, life: cR(.4, .6), s: cR(3, 5) * u, rot: cR(0, 6), vr: cR(-14, 14), c: '190,190,200', add: 0 }); cSparks(b, K.tx, K.by, 5, o.c, 240 * u, .3, -1.57, 1.4, u); shake(b, .1); }); return dur; },
  claws(K, o, e, wt) {   /* three claw marks (x2 = both hands, drain = vampire claws) */
    const { b, u, d } = K, mk = (t0, f) => cFn(b, { t: -t0, life: .3, fn(g, p, q) { const grow = Math.min(1, q / .3), al = q > .5 ? (1 - q) * 2 : 1; g.translate(K.tx, K.by); g.scale(f * d, 1); g.lineCap = 'round';
        for (const [wd, col, a2, op] of [[7, '20,6,10', .45, 'source-over'], [5, o.c, .9, 'lighter'], [1.6, '255,255,255', 1, 'lighter']]) { g.globalCompositeOperation = op; g.globalAlpha = al * a2; g.strokeStyle = `rgb(${col})`; g.lineWidth = wd * u * (1 - q * .4);
          for (let i = -1; i <= 1; i++) { const x0 = (-20 + i * 13) * u, y0 = -30 * u, x1 = (14 + i * 13) * u, y1 = 30 * u; g.beginPath(); g.moveTo(x0, y0); g.quadraticCurveTo(x0 + 22 * u * grow, y0 + (y1 - y0) * .4 * grow, x0 + (x1 - x0) * grow, y0 + (y1 - y0) * grow); g.stroke(); } } } });
    mk(0, 1); if (o.x2) mk(.09, -1); cAt(b, .07, () => { hitSpark(K, o.c, 4); if (o.drain && (e.crit || Math.random() < .5)) drainBack(K, '255,50,80', 4); }); return .07; },
  reap(K, o, e, wt, n2, id) {   /* the reaper's sweep: a full circle round the enemy, then a soul rises (scythe) */
    const { b, u, d } = K, r = 46 * u * wt, dur = .26;
    cFn(b, { life: dur + .12, fn(g, p, q) { const m = Math.min(1, q * (dur + .12) / dur), a1 = -2.4 + m * 5.6, al = q > .68 ? (1 - q) / .32 : 1; g.translate(K.tx, K.by); g.scale(d, .8); g.lineCap = 'round';
        for (const [wd, col, a2, op] of [[13, '14,4,24', .5, 'source-over'], [10, o.c, .55, 'lighter'], [4, o.c, 1, 'lighter'], [1.4, '255,255,255', 1, 'lighter']]) { g.globalCompositeOperation = op; g.globalAlpha = al * a2; g.strokeStyle = `rgb(${col})`; g.lineWidth = wd * u; g.beginPath(); g.arc(0, 0, r, Math.max(-2.4, a1 - 2.6), a1); g.stroke(); }
        g.rotate(a1); g.translate(r, 0); drawIco(g, id, 0, 0, 40 * u, 1.9, al, o.c); } });
    cAt(b, dur * .7, () => { hitSpark(K, o.c, 6, 1); cFn(b, { life: .8, x: K.tx, y: K.by, mv(p, q) { p.y = K.by - q * 80 * u; p.x = K.tx + Math.sin(q * 9) * 10 * u; cGlow(b, p.x, p.y, 7 * u, 1, .25, '200,170,255'); }, fn(g, p, q) { g.globalCompositeOperation = 'lighter'; g.globalAlpha = 1 - q; g.drawImage(glw('230,215,255'), p.x - 12 * u, p.y - 12 * u, 24 * u, 24 * u); } }); if (e.crit || Math.random() < .4) drainBack(K, '200,120,255', 4); }); return dur * .7; },
  star(K, o, e, wt) {   /* a small spinning steel star, thrown fast (shuriken) */
    const { b, u, d } = K, dur = .13, y0 = K.py + cR(6, 26) * u, sp0 = cR(0, 6);
    fly(K, { x0: K.cx + d * 18 * u, y0, x1: K.tx, y1: K.by + cR(-12, 12) * u, dur, draw(g, x, y, a, q) { g.globalCompositeOperation = 'lighter'; g.globalAlpha = .5; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 2 * u; g.beginPath(); g.moveTo(x, y); g.lineTo(x - Math.cos(a) * 34 * u, y - Math.sin(a) * 34 * u); g.stroke(); g.globalCompositeOperation = 'source-over'; drawStar(g, x, y, 13 * u, 5 * u, 4, sp0 + q * 22, '#1c1c28', 1); drawStar(g, x, y, 11 * u, 3.8 * u, 4, sp0 + q * 22, '#e6ecff', 1); },
      then() { cGlow(b, K.tx, K.by, 6 * u, 22 * u, .12, o.c); cSparks(b, K.tx, K.by, 3, o.c, 200 * u, .22, d > 0 ? 0 : Math.PI, 1, u); } }); return dur; },
  disc(K, o, e, wt) {   /* a ring of fire flies out and comes back (flame chakram) */
    const { b, u, d } = K, r = 15 * u, x0 = K.cx + d * 18 * u, y0 = K.py + 16 * u, dr = (g, x, y, a, q) => { g.globalCompositeOperation = 'lighter'; g.globalAlpha = .8; g.drawImage(glw(o.c), x - r * 1.8, y - r * 1.8, r * 3.6, r * 3.6); g.globalAlpha = 1; g.strokeStyle = '#fff3c0'; g.lineWidth = 3 * u; g.beginPath(); g.ellipse(x, y, r, r * .5, q * 30, 0, 6.283); g.stroke(); g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 5 * u; g.globalAlpha = .7; g.beginPath(); g.ellipse(x, y, r * 1.15, r * .6, q * 30, 0, 6.283); g.stroke(); },
      tr = (x, y) => cGlow(b, x + cR(-4, 4) * u, y + cR(-4, 4) * u, cR(7, 12) * u, 2 * u, cR(.18, .32), Math.random() < .5 ? '255,120,30' : '255,200,90', 0, { vy: -40 * u });
    fly(K, { x0, y0, x1: K.tx, y1: K.by, dur: .18, arc: 14 * u, draw: dr, trail: tr, then() { cGlow(b, K.tx, K.by, 14 * u, 46 * u, .16, o.c); cSparks(b, K.tx, K.by, 5, '255,200,90', 240 * u, .3, -1.57, 1.6, u); fly(K, { x0: K.tx, y0: K.by, x1: x0, y1: y0, dur: .24, arc: -22 * u, draw: dr, trail: tr }); } }); return .18; },
  arrows(K, o, e, wt, n2) {   /* arrows of light (bow; ice = frost bow; holy = the god bow fires three) */
    const { b, u, d } = K, n = o.n || 1, dur = .15, x0 = K.cx + d * 26 * u, y0 = K.py + 14 * u;
    for (let i = 0; i < n; i++) { const off = (i - (n - 1) / 2), t0 = i * .045;
      fly(K, { x0, y0: y0 + off * 22 * u, x1: K.tx, y1: K.by + off * 5 * u, dur, t0, draw(g, x, y, a) { g.translate(x, y); g.rotate(a); g.scale(1.5, 1.5); g.globalCompositeOperation = 'lighter'; const gr = g.createLinearGradient(-70 * u, 0, 6 * u, 0); gr.addColorStop(0, `rgba(${o.c},0)`); gr.addColorStop(1, `rgba(${o.c},.85)`); g.fillStyle = gr; g.fillRect(-70 * u, -2.6 * u, 76 * u, 5.2 * u);
          g.globalCompositeOperation = 'source-over'; g.fillStyle = o.ice ? '#3a7ab8' : o.holy ? '#fff2b0' : '#6b4a2a'; g.fillRect(-22 * u, -1.3 * u, 26 * u, 2.6 * u); g.fillStyle = o.ice ? '#dff6ff' : '#f4f4fa'; g.beginPath(); g.moveTo(11 * u, 0); g.lineTo(1 * u, -4.5 * u); g.lineTo(1 * u, 4.5 * u); g.closePath(); g.fill(); g.fillStyle = o.ice ? '#8fe0ff' : o.holy ? '#ffd060' : '#d94a4a'; g.fillRect(-24 * u, -3.4 * u, 6 * u, 6.8 * u); },
        trail(x, y) { if (o.ice && Math.random() < .7) cGlow(b, x, y, 6 * u, 12 * u, .3, '190,235,255', 0, { a: .5 }); },
        then() { if (i === 0) { if (o.ice) vfx(b, 'ice', K.T); else hitSpark(K, o.c, 6, e.big); } else cGlow(b, K.tx, K.by + off * 5 * u, 8 * u, 30 * u, .14, o.c); if (o.holy && i === n - 1) { column(K, K.tx, o.c, 22, 0, .36); cRing(b, K.tx, K.fy, 80 * u, .4, o.c, 3 * u); cFlare(b, K.tx, K.by, 20 * u, 80 * u, .2, o.c, .3); } } }); }
    return dur; },
  fireball(K, o, e, wt) {   /* a ball of fire (wand); n:3 + nova = the arch staff's volley from a magic circle */
    const { b, u, d } = K, n = o.n || 1, dur = .22, x0 = K.cx + d * 22 * u, y0 = K.py + 12 * u;
    if (n > 1) cFn(b, { life: .5, fn(g, p, q) { drawRune(g, K.cx, K.fy, 46 * u, q * 3, o.c, q < .2 ? q * 5 : (1 - q) / .8, 3); } });
    for (let i = 0; i < n; i++) { const off = i - (n - 1) / 2;
      fly(K, { x0, y0: y0 + off * 26 * u, x1: K.tx, y1: K.by, dur, t0: i * .08, arc: (12 - off * 16) * u, draw(g, x, y) { g.globalCompositeOperation = 'lighter'; const r = 13 * u * wt; g.drawImage(glw(o.c), x - r * 2, y - r * 2, r * 4, r * 4); g.drawImage(glw('255,235,170'), x - r, y - r, r * 2, r * 2); },
        trail(x, y) { cGlow(b, x + cR(-5, 5) * u, y + cR(-5, 5) * u, cR(8, 14) * u, 2 * u, cR(.2, .38), Math.random() < .5 ? '255,120,30' : '255,200,90', 0, { vy: -50 * u }); },
        then() { if (i === 0) vfx(b, 'fire', K.T, { big: e.big }); else cGlow(b, K.tx, K.by, 16 * u, 56 * u, .18, o.c); if (o.nova && i === n - 1) { cRing(b, K.tx, K.fy, 130 * u, .45, '255,150,60', 6 * u); for (let j = 0; j < 14; j++) { const a = j / 14 * 6.283; sp(b, { x: K.tx, y: K.fy - 6 * u, vx: Math.cos(a) * 240 * u, vy: Math.sin(a) * 80 * u - 40 * u, dr: 2.5, life: .45, s: 16 * u, s1: 3 * u, c: j % 2 ? '255,110,30' : '255,210,100' }); } } } }); }
    return dur; },
  icicle(K, o, e, wt) {   /* three shards of ice, then spikes grow under the enemy (ice staff) */
    const { b, u, d } = K, dur = .17, x0 = K.cx + d * 22 * u, y0 = K.py + 12 * u;
    for (let i = 0; i < 3; i++) fly(K, { x0, y0: y0 + (i - 1) * 16 * u, x1: K.tx, y1: K.by + (i - 1) * 10 * u, dur, t0: i * .04, draw(g, x, y, a) { g.translate(x, y); g.rotate(a); g.globalCompositeOperation = 'lighter'; g.globalAlpha = .7; g.drawImage(glw(o.c), -16 * u, -10 * u, 32 * u, 20 * u); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.fillStyle = '#e4f8ff'; g.strokeStyle = '#5ab4ee'; g.lineWidth = 1.2; g.beginPath(); g.moveTo(15 * u, 0); g.lineTo(-4 * u, -4.4 * u); g.lineTo(-13 * u, 0); g.lineTo(-4 * u, 4.4 * u); g.closePath(); g.fill(); g.stroke(); },
      trail(x, y) { if (Math.random() < .5) cGlow(b, x, y, 5 * u, 11 * u, .28, '190,235,255', 0, { a: .45 }); }, then() { if (i === 0) { vfx(b, 'ice', K.T); spikes(K, '215,245,255', 5, 36 * wt, .03); } } });
    return dur; },
  chain(K, o, e, wt) {   /* a crackling arc of lightning jumps to the enemy (lightning orb) */
    const { b, u, d } = K, x0 = K.cx + d * 20 * u, y0 = K.py + 12 * u; cGlow(b, x0, y0, 14 * u, 34 * u, .25, o.c);
    cFn(b, { life: .24, fn(g, p, q) { const n = 9, pts = []; for (let i = 0; i <= n; i++) { const m = i / n; pts.push([x0 + (K.tx - x0) * m + (i && i < n ? cR(-10, 10) * u : 0), y0 + (K.by - y0) * m + (i && i < n ? cR(-16, 16) * u : 0)]); } g.globalCompositeOperation = 'lighter'; g.lineJoin = 'round';
        for (const [w, a2, c] of [[13, .22, o.c], [5, .7, o.c], [1.8, 1, '255,255,255']]) { g.globalAlpha = (1 - q * q) * a2; g.strokeStyle = `rgb(${c})`; g.lineWidth = w * u; g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); } } });
    cAt(b, .04, () => { cGlow(b, K.tx, K.by, 20 * u, 60 * u, .2, o.c); cSparks(b, K.tx, K.by, 10, '210,210,255', 300 * u, .3, 0, 3.14, u, 100); cRing(b, K.tx, K.fy, 70 * u, .35, o.c, 3 * u); }); return .04; },
  flask(K, o, e, wt, n2, id) {   /* a bottle is lobbed over, breaks into a poison cloud (witch's poison) */
    const { b, u, d } = K, dur = .32, z = 34 * u, sp0 = cR(0, 6);
    fly(K, { x0: K.cx + d * 18 * u, y0: K.py + 14 * u, x1: K.tx, y1: K.by + 12 * u, dur, arc: 46 * u, draw(g, x, y, a, q) { drawIco(g, id, x, y, z, d * (sp0 + q * 9), 1, o.c); },
      then() { for (let i = 0; i < 6; i++) sp(b, { k: 'shard', x: K.tx, y: K.by + 10 * u, vx: cR(-180, 180) * u, vy: cR(-240, -60) * u, g: 800 * u, life: cR(.35, .55), s: cR(3, 5) * u, rot: cR(0, 6), vr: cR(-14, 14), c: '220,255,225', add: 0 });
        for (let i = 0; i < 7; i++) cGlow(b, K.tx + cR(-30, 30) * u, K.by + cR(-16, 24) * u, 18 * u, cR(44, 66) * u, cR(.7, 1.1), o.c, i * .03, { a: .5, vy: -14 * u, vx: cR(-14, 14) * u });
        for (let i = 0; i < 6; i++) sp(b, { k: 'bubble', x: K.tx + cR(-26, 26) * u, y: K.by + cR(0, 24) * u, vy: cR(-60, -25) * u, life: cR(.6, 1), s: cR(4, 8) * u, s1: cR(4, 8) * u, c: '150,255,110' }); } }); return dur; },
  curse(K, o, e, wt) {   /* a cursed skull drifts over and brands the enemy (curse skull) */
    const { b, u, d } = K, dur = .36;
    fly(K, { x0: K.cx + d * 18 * u, y0: K.py + 12 * u, x1: K.tx, y1: K.by - 8 * u, dur, arc: 18 * u, draw(g, x, y, a, q) { drawSkull(g, x, y + Math.sin(q * 14) * 4 * u, 11 * u, o.c, 1); }, trail(x, y) { cGlow(b, x, y, 9 * u, 2 * u, .34, Math.random() < .5 ? o.c : o.c2); },
      then() { cFn(b, { life: .7, fn(g, p, q) { drawRune(g, K.tx, K.fy, 56 * u, -q * 2.5, o.c, q < .15 ? q / .15 : (1 - q) / .85, 3); } }); cGlow(b, K.tx, K.by, 20 * u, 64 * u, .22, o.c);
        for (let i = 0; i < 8; i++) cGlow(b, K.tx + cR(-22, 22) * u, K.fy - cR(0, 14) * u, cR(8, 13) * u, 2 * u, cR(.45, .8), i % 2 ? o.c2 : '255,130,40', i * .03, { vy: cR(-150, -70) * u }); } }); return dur; },
  skyray(K, o, e, wt) {   /* a ray of holy light from above; its light heals the caster (holy tome; big = the divine tome) */
    const { b, u } = K, w = o.big ? 38 : 24; cFn(b, { life: .5, fn(g, p, q) { drawRune(g, K.tx, K.fy, (o.big ? 70 : 52) * u, q * 1.5, o.c, q < .2 ? q * 5 : (1 - q) / .8, 4); } });
    column(K, K.tx, o.c, w, .06, .42); cAt(b, .1, () => { cGlow(b, K.tx, K.by, 24 * u, (o.big ? 110 : 76) * u, .26, o.c); cRing(b, K.tx, K.fy, (o.big ? 130 : 90) * u, .45, o.c, 4 * u);
      for (let i = 0; i < (o.big ? 14 : 8); i++) cGlow(b, K.tx + cR(-w, w) * u, K.fy - cR(0, 60) * u, cR(4, 7) * u, 1, cR(.5, .9), '255,250,210', 0, { vy: cR(-180, -80) * u }); if (o.big) { cFlare(b, K.tx, K.by - 10 * u, 30 * u, 120 * u, .3, o.c, 0); shake(b, .12); } drainBack(K, '255,235,150', o.big ? 6 : 4); }); return .1; },
  implode(K, o, e, wt) {   /* darkness gathers into a black sphere, then bursts (void orb) */
    const { b, u } = K, dur = .26; for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283, r = 84 * u; sp(b, { k: 'orb', x: 0, y: 0, x0: K.tx + Math.cos(a) * r, y0: K.by + Math.sin(a) * r * .7, x1: K.tx, y1: K.by, t: -i * .008, life: dur, s: 5 * u, s1: 5 * u, c: o.c, arc: 0 }); }
    cFn(b, { life: dur + .1, fn(g, p, q) { const r = (q < .7 ? 8 + 26 * (q / .7) : 34 * (1 - (q - .7) / .3)) * u; g.globalCompositeOperation = 'source-over'; g.globalAlpha = .92; g.fillStyle = '#0a0214'; g.beginPath(); g.arc(K.tx, K.by, r, 0, 6.283); g.fill(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = 1; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 3 * u; g.beginPath(); g.arc(K.tx, K.by, r + 2 * u, 0, 6.283); g.stroke(); g.globalAlpha = .5; g.drawImage(glw(o.c), K.tx - r * 2.4, K.by - r * 2.4, r * 4.8, r * 4.8); } });
    cAt(b, dur + .08, () => { cGlow(b, K.tx, K.by, 30 * u, 110 * u, .24, o.c); cFlare(b, K.tx, K.by, 30 * u, 110 * u, .22, '220,190,255', .5); cSparks(b, K.tx, K.by, 14, '200,150,255', 340 * u, .4, 0, 3.14, u, 60); cRing(b, K.tx, K.fy, 100 * u, .42, o.c, 4 * u); shake(b, .12); }); return dur + .08; },
  lich(K, o, e, wt) {   /* three soul skulls spiral out of a green circle and light a toxic fire (staff of the demon king) */
    const { b, u, d } = K, dur = .32; cFn(b, { life: .6, fn(g, p, q) { drawRune(g, K.cx, K.fy, 50 * u, -q * 3, o.c, q < .2 ? q * 5 : (1 - q) / .8, 5); } });
    for (let i = 0; i < 3; i++) { const ph = i * 2.1; fly(K, { x0: K.cx + d * 18 * u, y0: K.py + 14 * u, x1: K.tx, y1: K.by, dur, t0: i * .07, draw(g, x, y, a, q) { drawSkull(g, x, y + Math.sin(q * 10 + ph) * 16 * u * (1 - q), 8 * u, i % 2 ? o.c2 : o.c, 1); }, trail(x, y, q) { cGlow(b, x, y + Math.sin(q * 10 + ph) * 16 * u * (1 - q), 8 * u, 2 * u, .3, i % 2 ? o.c2 : o.c); },
      then() { if (i < 2) { cGlow(b, K.tx, K.by, 14 * u, 50 * u, .16, o.c); return; } cRing(b, K.tx, K.fy, 110 * u, .45, o.c, 5 * u); column(K, K.tx, o.c, 26, 0, .45, K.fy - 150 * u); for (let j = 0; j < 18; j++) cGlow(b, K.tx + cR(-22, 22) * u, K.fy - cR(0, 20) * u, cR(10, 18) * u, 2 * u, cR(.4, .8), j % 3 ? o.c : o.c2, j * .015, { vy: cR(-230, -90) * u, vx: cR(-20, 20) * u }); shake(b, .14); } }); }
    return dur + .14; },
  bombtoss(K, o, e, wt, n2, id) {   /* start of the fight: a bomb with a burning fuse */
    const { b, u, d } = K, dur = .4, sp0 = cR(0, 6); fly(K, { x0: K.cx + d * 18 * u, y0: K.py + 14 * u, x1: K.tx, y1: K.by + 14 * u, dur, arc: 60 * u, draw(g, x, y, a, q) { drawIco(g, id, x, y, 40 * u, d * (sp0 + q * 8), 1, '255,170,80'); }, trail(x, y) { cSparks(b, x, y - 12 * u, 1, '255,220,120', 120 * u, .25, -1.57, 1, u); }, then() { vfx(b, 'boom', K.T); shake(b, .25, .6); } }); return dur; },
  meteor(K, o, e, wt) { const { b, u } = K; cFn(b, { life: .6, fn(g, p, q) { drawRune(g, K.tx, K.fy, (o.big ? 84 : 60) * u, q * 2, '255,110,40', q < .2 ? q * 5 : (1 - q) / .8, 4); } }); vfx(b, 'comet', K.T); if (o.big) for (const t of [.16, .3]) cAt(b, t, () => vfx(b, 'comet', K.T)); return .38; },
  wisps(K, o, e, wt) {   /* start of the fight: spirits leave the lantern (boom = the evil lantern's swarm) */
    const { b, u, d } = K, n = o.n || 3, dur = .36; for (let i = 0; i < n; i++) { const ph = i * 1.9, amp = cR(18, 40) * u * (i % 2 ? 1 : -1);
      fly(K, { x0: K.cx + d * 18 * u, y0: K.py + 14 * u, x1: K.tx, y1: K.by, dur, t0: i * .07, draw(g, x, y, a, q) { const yy = y + Math.sin(q * Math.PI * 2 + ph) * amp * (1 - q); g.globalCompositeOperation = 'lighter'; g.drawImage(glw(o.c), x - 16 * u, yy - 16 * u, 32 * u, 32 * u); g.drawImage(glw('255,255,255'), x - 6 * u, yy - 6 * u, 12 * u, 12 * u); },
        trail(x, y, q) { cGlow(b, x, y + Math.sin(q * Math.PI * 2 + ph) * amp * (1 - q), 9 * u, 2 * u, .32, o.c); }, then() { cGlow(b, K.tx, K.by, 14 * u, 50 * u, .18, o.c); cSparks(b, K.tx, K.by, 4, o.c, 220 * u, .3, 0, 3.14, u, 60); if (o.boom && i === n - 1) { cFlare(b, K.tx, K.by, 30 * u, 130 * u, .25, o.c, .4); cRing(b, K.tx, K.fy, 120 * u, .45, o.c, 5 * u); shake(b, .2, .5); } } }); }
    return dur; },
};
/* which move each item uses. c = its own colour. Items made from another one (base) that are not listed use their base's move. */
const CAST = {
  dagger: ['stab', { c: '205,160,255' }], venomknife: ['stab', { c: '140,255,90', n: 3, drip: '120,240,70' }],
  sword: ['wave', { c: '150,200,255' }], flamesword: ['wave', { c: '255,130,40', fire: 1 }], katana: ['iai', { c: '170,255,235' }],
  greatsword: ['cleave', { c: '170,110,255' }], executioner: ['guillotine', { c: '255,70,70' }],
  twinblades: ['xcut', { c: '205,185,255' }], stormblades: ['xcut', { c: '150,230,255', storm: 1 }],
  rapier: ['thrust', { c: '235,240,255', n: 3 }], luckrapier: ['thrust', { c: '180,255,150', n: 4, luck: 1 }],
  spear: ['pierce', { c: '255,220,140' }], frostlance: ['pierce', { c: '150,220,255', ice: 1 }], javelin: ['toss', { c: '255,230,170' }],
  axe: ['toss', { c: '255,170,100', spin: 1, chop: 1 }], bloodaxe: ['toss', { c: '255,60,60', spin: 1, chop: 1, blood: 1 }],
  hammer: ['slam', { c: '255,220,150' }], thunderhammer: ['slam', { c: '190,180,255', bolt: 1 }], club: ['bonk', { c: '240,200,140' }],
  claw: ['claws', { c: '255,140,80' }], vampclaw: ['claws', { c: '255,50,110', x2: 1, drain: 1 }], scythe: ['reap', { c: '180,110,255' }],
  shuriken: ['star', { c: '220,230,255' }], chakram: ['disc', { c: '255,150,50' }],
  bow: ['arrows', { c: '255,240,200' }], frostbow: ['arrows', { c: '150,225,255', ice: 1 }], f_godbow: ['arrows', { c: '255,225,120', n: 3, holy: 1 }],
  wand: ['fireball', { c: '255,130,40' }], archstaff: ['fireball', { c: '255,90,30', n: 3, nova: 1 }], icestaff: ['icicle', { c: '150,220,255' }],
  orb: ['chain', { c: '190,180,255' }], poison: ['flask', { c: '130,255,90' }], skull: ['curse', { c: '170,110,255', c2: '130,255,90' }],
  holytome: ['skyray', { c: '255,235,150' }], divinetome: ['skyray', { c: '255,245,190', big: 1 }], voidorb: ['implode', { c: '150,80,255' }],
  f_lichstaff: ['lich', { c: '120,255,160', c2: '170,110,255' }],
  bomb: ['bombtoss', {}], meteor: ['meteor', {}], comet: ['meteor', { big: 1 }], lantern: ['wisps', { c: '120,200,255', n: 3 }], soullantern: ['wisps', { c: '255,90,140', n: 6, boom: 1 }],
};
/* ---- SHIELD AND FOOD MOVES (on the owner) ---- */
const SELFFX = {
  dome(K, o) {   /* a dome of light plates (spikes = spiked shield) */
    const { b, u } = K, x = K.cx, y = K.by - 6 * u; sp(b, { k: 'bubble2', x, y, s: 54 * u, s1: 64 * u, life: .5, c: o.c });
    cFn(b, { life: .5, fn(g, p, q) { const al = q < .15 ? q / .15 : (1 - q) / .85, r = 58 * u; g.globalCompositeOperation = 'lighter'; g.globalAlpha = al * .8; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 1.4 * u; g.translate(x, y);
        for (let i = 0; i < 6; i++) { const a = i / 6 * 6.283 + q; g.beginPath(); g.ellipse(0, 0, r * .8 * Math.abs(Math.cos(a)), r, 0, 0, 6.283); g.stroke(); } g.beginPath(); g.ellipse(0, 0, r * .8, r * .34, 0, 0, 6.283); g.stroke();
        if (o.spikes) { g.globalCompositeOperation = 'source-over'; g.fillStyle = '#dfe6f2'; g.strokeStyle = '#3a4050'; g.lineWidth = 1; const out = Math.min(1, q / .15); for (let i = 0; i < 9; i++) { const a = -2.9 + i / 8 * 2.66; g.save(); g.rotate(a + Math.PI / 2); g.translate(0, -r * .96); g.beginPath(); g.moveTo(-5 * u, 0); g.lineTo(0, -18 * u * out); g.lineTo(5 * u, 0); g.closePath(); g.fill(); g.stroke(); g.restore(); } } } }); },
  parry(K, o) {   /* a small round shield flashes in front (buckler; cross = parry buckler) */
    const { b, u, d } = K, x = K.cx + d * 30 * u, y = K.by; cFn(b, { life: .32, fn(g, p, q) { const al = q < .2 ? q * 5 : (1 - q) / .8, pop = 1 + .25 * Math.sin(Math.min(1, q * 4) * 3.14); g.globalCompositeOperation = 'lighter'; g.translate(x, y); g.scale(pop, pop);
        g.globalAlpha = al * .5; g.drawImage(glw(o.c), -30 * u, -34 * u, 60 * u, 68 * u); g.globalAlpha = al; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 4 * u; g.beginPath(); g.ellipse(0, 0, 11 * u, 22 * u, 0, 0, 6.283); g.stroke(); g.strokeStyle = '#fff'; g.lineWidth = 1.5 * u; g.beginPath(); g.ellipse(0, 0, 6 * u, 13 * u, 0, 0, 6.283); g.stroke(); } });
    if (o.cross) { cFlare(b, x, y, 10 * u, 46 * u, .2, o.c, .78); cSparks(b, x, y, 4, o.c, 200 * u, .25, d > 0 ? 0 : 3.14, .9, u); } },
  slab(K, o) {   /* a tall wall of light rises (tower shield) */
    const { b, u, d } = K, x = K.cx + d * 34 * u; cFn(b, { life: .6, fn(g, p, q) { const up = Math.min(1, q / .15), al = q > .5 ? (1 - q) * 2 : 1, h = 108 * u * (1 - (1 - up) * (1 - up)), w = 26 * u; g.globalCompositeOperation = 'lighter'; const gr = g.createLinearGradient(0, K.fy - h, 0, K.fy); gr.addColorStop(0, `rgba(${o.c},.15)`); gr.addColorStop(1, `rgba(${o.c},.75)`); g.globalAlpha = al; g.fillStyle = gr; g.strokeStyle = '#fff'; g.lineWidth = 1.6 * u;
        g.beginPath(); g.moveTo(x - w / 2, K.fy); g.lineTo(x - w / 2, K.fy - h + 10 * u); g.quadraticCurveTo(x, K.fy - h - 8 * u, x + w / 2, K.fy - h + 10 * u); g.lineTo(x + w / 2, K.fy); g.closePath(); g.fill(); g.stroke(); g.beginPath(); g.moveTo(x, K.fy - h + 8 * u); g.lineTo(x, K.fy); g.moveTo(x - w / 2, K.fy - h * .55); g.lineTo(x + w / 2, K.fy - h * .55); g.stroke(); } }); cRing(b, x, K.fy, 40 * u, .35, o.c, 3 * u); },
  rampart(K, o) {   /* stone blocks push up out of the ground (fortress shield) */
    const { b, u, d } = K, blocks = [[26, 62, 22], [46, 78, 24], [66, 50, 20]]; cFn(b, { life: .75, fn(g, p, q) { const al = q > .7 ? (1 - q) / .3 : 1; g.globalCompositeOperation = 'source-over'; blocks.forEach(([dx, h, w], i) => { const up = Math.max(0, Math.min(1, (q * .75 - i * .03) / .1)), hh = h * u * (1 - (1 - up) * (1 - up)), x = K.cx + d * dx * u; g.globalAlpha = al;
          g.fillStyle = '#6e6258'; g.strokeStyle = '#2a211c'; g.lineWidth = 1.5; g.beginPath(); g.rect(x - w * u / 2, K.fy - hh, w * u, hh); g.fill(); g.stroke(); g.fillStyle = '#a89886'; g.fillRect(x - w * u / 2, K.fy - hh, w * u, 5 * u); g.fillStyle = '#51463e'; g.fillRect(x - w * u / 2 + 3 * u, K.fy - hh * .55, w * u - 6 * u, 2 * u); g.globalCompositeOperation = 'lighter'; g.globalAlpha = al * .5 * up; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 2.5 * u; g.strokeRect(x - w * u / 2, K.fy - hh, w * u, hh); g.globalCompositeOperation = 'source-over'; }); } });
    cSmoke(b, K.cx + d * 46 * u, K.fy - 4 * u, 4, 30, .5, u); cRing(b, K.cx + d * 46 * u, K.fy, 60 * u, .35, o.c, 3 * u); },
  mend(K, o) {   /* small lights rise (apple; small = bread crumbs) */
    const { b, u } = K, n = o.n || 8; healGlow(K, o.c2 || o.c, o.small ? .6 : 1); for (let i = 0; i < n; i++) sp(b, { k: i % 3 === 2 ? 'plus' : 'glow', x: K.cx + cR(-26, 26) * u, y: K.fy - cR(0, 40) * u, vy: cR(-120, -55) * u, life: cR(.55, .95), s: (o.small ? cR(5, 8) : cR(8, 13)) * u, s1: 1, c: i % 2 ? o.c : (o.c2 || o.c) }); if (!o.small) cRing(b, K.cx, K.fy, 56 * u, .4, o.c2 || o.c, 3 * u); },
  drip(K, o) {   /* golden honey runs down (honey; plus = honey bread) */
    const { b, u } = K; healGlow(K, o.c, .8); cGlow(b, K.cx, K.by - 40 * u, 16 * u, 44 * u, .45, o.c); for (let i = 0; i < 9; i++) sp(b, { k: 'drop', x: K.cx + cR(-22, 22) * u, y: K.by - cR(34, 50) * u, vy: cR(40, 90) * u, g: 260 * u, t: -i * .03, life: cR(.45, .7), s: cR(4, 6.5) * u, s1: 2.5 * u, c: o.c });
    if (o.plus) for (let i = 0; i < 4; i++) sp(b, { k: 'plus', x: K.cx + cR(-24, 24) * u, y: K.by + cR(-10, 20) * u, vy: cR(-80, -40) * u, life: .7, s: 5 * u, s1: 1, c: '170,255,150' }); },
  steam(K, o) {   /* warm steam curls up (roast meat) */
    const { b, u } = K; healGlow(K, o.c, .9); for (let i = 0; i < 3; i++) { const x0 = K.cx + (i - 1) * 16 * u, ph = cR(0, 6); cFn(b, { t: -i * .06, life: .8, fn(g, p, q) { g.globalCompositeOperation = 'lighter'; g.globalAlpha = (q < .2 ? q * 5 : 1 - (q - .2) / .8) * .8; g.strokeStyle = `rgb(${o.c})`; g.lineWidth = 6 * u; g.lineCap = 'round'; g.beginPath(); for (let j = 0; j <= 8; j++) { const yy = K.by + 10 * u - (j / 8) * 50 * u - q * 46 * u, xx = x0 + Math.sin(j * .9 + ph + q * 5) * 6 * u; j ? g.lineTo(xx, yy) : g.moveTo(xx, yy); } g.stroke(); } }); }
    for (let i = 0; i < 3; i++) sp(b, { k: 'plus', x: K.cx + cR(-22, 22) * u, y: K.by + cR(-10, 20) * u, vy: cR(-80, -40) * u, life: .7, s: 5 * u, s1: 1, c: '170,255,150' }); },
  swirl(K, o) {   /* lights wind upward round the body (blood wine; big = elixir of life) */
    const { b, u } = K, n = o.big ? 14 : 9; healGlow(K, o.c, o.big ? 1.2 : .9); cFn(b, { life: .8, fn(g, p, q) { g.globalCompositeOperation = 'lighter'; for (let i = 0; i < n; i++) { const m = (q * 1.3 + i / n) % 1, a = m * 9 + i, r = (30 - m * 12) * u, x = K.cx + Math.cos(a) * r, y = K.fy - m * 110 * u + Math.sin(a) * r * .3, z = (o.big ? 13 : 10) * u; g.globalAlpha = (1 - m) * (q > .8 ? (1 - q) * 5 : 1); g.drawImage(glw(i % 2 && o.c2 ? o.c2 : o.c), x - z, y - z, z * 2, z * 2); } } });
    if (o.big) cRing(b, K.cx, K.fy, 70 * u, .5, o.c2 || o.c, 3 * u); },
  gulp(K, o) {   /* one big red wave of health (big potion) */
    const { b, u } = K; cRing(b, K.cx, K.fy, 80 * u, .5, o.c, 5 * u); column(K, K.cx, o.c, 22, 0, .5, K.fy - 130 * u); for (let i = 0; i < 10; i++) sp(b, { k: 'plus', x: K.cx + cR(-30, 30) * u, y: K.fy - cR(0, 40) * u, vy: cR(-140, -60) * u, life: cR(.6, 1), s: cR(5, 8) * u, s1: 1, c: i % 2 ? '170,255,150' : '255,160,160' }); },
  banquet(K, o) {   /* a feast: golden rings, sparks and health (warrior's feast) */
    const { b, u } = K; healGlow(K, o.c, 1.3); cRing(b, K.cx, K.fy, 70 * u, .45, o.c, 5 * u); cRing(b, K.cx, K.fy, 100 * u, .55, o.c, 4 * u, .1); cFlare(b, K.cx, K.by - 20 * u, 24 * u, 90 * u, .34, o.c, .4);
    for (let i = 0; i < 18; i++) sp(b, { k: i % 3 ? 'glow' : 'plus', x: K.cx + cR(-36, 36) * u, y: K.fy - cR(0, 30) * u, vy: cR(-170, -60) * u, life: cR(.6, 1), s: cR(8, 13) * u, s1: 1, c: i % 2 ? '170,255,150' : o.c }); },
};
const CASTSELF = {
  shield: ['dome', { c: '130,200,255' }], spikeshield: ['dome', { c: '190,205,230', spikes: 1 }], buckler: ['parry', { c: '215,230,255' }], parrybuckler: ['parry', { c: '255,225,140', cross: 1 }],
  towershield: ['slab', { c: '150,190,255' }], fortress: ['rampart', { c: '220,200,170' }],
  apple: ['mend', { c: '255,100,100', c2: '140,255,150', n: 8 }], bread: ['mend', { c: '255,225,160', n: 5, small: 1 }], honey: ['drip', { c: '255,200,60' }], honeybread: ['drip', { c: '255,210,90', plus: 1 }],
  meat: ['steam', { c: '255,170,100' }], wine: ['swirl', { c: '225,70,150' }], elixir: ['swirl', { c: '120,240,255', c2: '255,230,140', big: 1 }], potion: ['gulp', { c: '255,80,90' }], feast: ['banquet', { c: '255,215,120' }],
};
/* ---- entry points used by bag3d.html ---- */
function castOf(tab, it) { if (!it) return null; let d = IT[it.id], c = tab[it.id]; while (!c && d && d.base) { c = tab[d.base]; d = IT[d.base]; } return c; }
function castWeight(it) { const d = it && IT[it.id]; if (!d) return 1; return d.start ? 1.3 : Math.max(.75, Math.min(1.4, .6 + (d.cd || 1.5) * .26)); }
function castHit(b, e, it) {   /* a hit event of side e.s from item `it` (null = a monster's own blow) -> seconds until it lands */
  const K = castKit(b, e.s), c = castOf(CAST, it); if (b.px.length > 380) return 0; b.lc = b.lc || {}; let n2 = 0;
  if (it) { const L = b.lc[it.u]; if (L && b.T - L.t < .04) n2 = L.n + 1; b.lc[it.u] = { t: b.T, n: n2 }; }   /* an item that hits twice at once: the second cut comes a moment later */
  let dl; if (c) dl = CASTFX[c[0]](K, c[1], e, castWeight(it), n2, it.id); else if (e.mg) dl = CASTFX.fireball(K, { c: '190,140,255' }, e, 1, n2); else { cutMark(K, '255,226,160', 40, (K.d > 0 ? -.6 : .6) + cR(-.3, .3), 0, 5); hitSpark(K, '255,226,160', 7, e.big); dl = .03; }
  if (e.crit) cAt(b, dl, () => { vfx(b, 'crit', K.T); b.flash = Math.max(b.flash, .18); shake(b, .12, .6); }); return dl; }
function castSelf(b, e, it) { const c = castOf(CASTSELF, it), K = castKit(b, e.s); if (b.px.length > 380) return; if (c) SELFFX[c[0]](K, c[1], e); else vfx(b, e.k === 'heal' ? 'heal' : 'shield', e.s); }
function castMiss(b, e) {   /* a dodge: the target slips aside in a puff of wind */
  const K = castKit(b, e.s), { u, d } = K; for (let i = 0; i < 5; i++) sp(b, { k: 'streak', x: K.tx + cR(-14, 14) * u, y: K.by + cR(-30, 30) * u, vx: d * cR(180, 320) * u, vy: 0, dr: 5, life: .28, s: 2 * u, c: '225,240,255' }); cGlow(b, K.tx + d * 16 * u, K.by, 20 * u, 44 * u, .22, '200,225,255', 0, { a: .45 }); }
function castThorn(b, s) {   /* thorns: a few thin spikes flick out of the one that was hit (side s) */
  const K = castKit(b, 1 - s), { u } = K, d = s ? -1 : 1, x = K.tx + d * 14 * u, y = K.by; if (b.px.length > 300) return;
  cFn(b, { life: .26, fn(g, p, q) { const out = Math.min(1, q / .3), al = q > .5 ? (1 - q) * 2 : 1; g.translate(x, y); g.scale(d, 1); g.lineCap = 'round'; for (let i = 0; i < 5; i++) { const a = -.9 + i * .45, r0 = 14 * u, r1 = (22 + 16 * out) * u;
      for (const [w, c, op] of [[3.4, '30,60,24', 'source-over'], [1.6, '200,255,150', 'lighter']]) { g.globalCompositeOperation = op; g.globalAlpha = al; g.strokeStyle = `rgb(${c})`; g.lineWidth = w * u; g.beginPath(); g.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); g.lineTo(Math.cos(a) * r1, Math.sin(a) * r1); g.stroke(); } } } }); }
function castPassive(b) {   /* start of a fight: every passive item in a bag sends its power to its owner */
  const cv = document.getElementById('cv').getBoundingClientRect(), col = { d: '130,200,255', g: '200,140,255', u: '255,215,110', f: '150,255,150', w: '255,170,120' };
  for (const [s, root, list] of [[0, '#mybag', (typeof G !== 'undefined' ? G.items.filter(o => o.bag) : [])], [1, '#fbag', b.B.list || []]]) { const K = castKit(b, s); let n = 0;
    for (const o of list) { const d = IT[o.id]; if (!d || d.cd || d.start || d.t === 'w' || n > 11) continue; const el = document.querySelector(`${root} [data-u="${o.u}"]`); if (!el) continue; const r = el.getBoundingClientRect(), x0 = r.left + r.width / 2 - cv.left, y0 = r.top + r.height / 2 - cv.top, c = col[d.t] || col.u, t0 = .15 + n++ * .07;
      sp(b, { k: 'orb', x: x0, y: y0, x0, y0, x1: K.cx, y1: K.by, t: -t0, life: .45, s: 5 * K.u, s1: 5 * K.u, c, arc: 30 * K.u }); cGlow(b, x0, y0, 6 * K.u, 22 * K.u, .3, c, t0); cGlow(b, K.cx, K.by, 10 * K.u, 34 * K.u, .2, c, t0 + .45); }
    if (n) { cRing(b, K.cx, K.fy, 70 * K.u, .5, '255,225,150', 3 * K.u, .2 + n * .07 + .4); } } }
/* champion skills: what flies when the skill starts (s = side), and what each of its hits looks like */
function castSkill(b, s, k) { const K = castKit(b, s), { u, d } = K; vfx(b, 'aura', s);
  if (k === 'wolf' || k === 'archer') { const c = k === 'wolf' ? '255,225,120' : '150,255,170', ts = k === 'wolf' ? [.41, .61, .81] : [.46, .76]; ts.forEach((t0, i) => fly(K, { x0: K.cx + d * 30 * u, y0: K.by - 14 * u + (i - 1) * 8 * u, x1: K.tx, y1: K.by, dur: .09, t0: t0 - .05, draw(g, x, y, a) { g.translate(x, y); g.rotate(a); g.globalCompositeOperation = 'lighter'; const gr = g.createLinearGradient(-120 * u, 0, 10 * u, 0); gr.addColorStop(0, `rgba(${c},0)`); gr.addColorStop(1, `rgba(${c},.95)`); g.fillStyle = gr; g.fillRect(-120 * u, -4 * u, 130 * u, 8 * u); g.fillStyle = '#fff'; g.beginPath(); g.moveTo(18 * u, 0); g.lineTo(2 * u, -7 * u); g.lineTo(2 * u, 7 * u); g.closePath(); g.fill(); } })); }
  else if (k === 'wing') { cAt(b, .2, () => SELFFX.dome(K, { c: '255,225,140' })); cFn(b, { t: -.36, life: .2, fn(g, p, q) { const x = K.cx + (K.tx - K.cx) * q; g.globalCompositeOperation = 'lighter'; g.globalAlpha = 1 - q * .4; g.drawImage(glw('255,225,140'), x - 50 * u, K.by - 60 * u, 100 * u, 120 * u); g.strokeStyle = '#fff'; g.lineWidth = 4 * u; g.beginPath(); g.ellipse(x, K.by, 16 * u, 40 * u, 0, 0, 6.283); g.stroke(); } }); }
  else if (k === 'demon') [.32, .57, .82].forEach((t0, i) => cFn(b, { t: -t0, life: .2, fn(g, p, q) { drawCres(g, K.tx - d * 30 * u * (1 - q), K.by, (44 + i * 8) * u, (i - 1) * .8 * d, d, 16 * u, '255,70,50', 1 - q * q, 1.2); } }));
  else if (k === 'dark') cFn(b, { t: -.42, life: .26, x: K.cx, mv(p, q) { p.x = K.cx + d * 40 * u + (K.tx - K.cx - d * 40 * u) * Math.min(1, q / .7); }, fn(g, p, q) { for (let i = 3; i >= 0; i--) drawCres(g, p.x - d * i * 16 * u, K.by - 6 * u, 62 * u * (1 - i * .07), 0, d, 24 * u, '150,70,255', (q > .7 ? (1 - q) / .3 : 1) * (i ? .3 / i : 1), 1.3); } });
  else if (k === 'hood') { cFn(b, { life: .9, fn(g, p, q) { drawRune(g, K.tx, K.fy, 80 * u, q * 3, '190,120,255', q < .15 ? q / .15 : (1 - q) / .85, 5); } }); cAt(b, .32, () => sp(b, { k: 'comet', x: 0, y: 0, x0: K.tx - d * K.W * .2, y0: -30, x1: K.tx, y1: K.by, life: .36, s: 24 * u, s1: 24 * u, c: '190,120,255' })); } }
function castSkillHit(b, e) { const K = castKit(b, e.s), { u } = K, k = e.sk;
  if (k === 'hood') { vfx(b, 'boom', K.T, { big: 1 }); shake(b, .3, .8); } else if (k === 'wing') { vfx(b, 'smash', K.T, { big: 1 }); cFlare(b, K.tx, K.by, 30 * u, 130 * u, .25, '255,225,140', .2); shake(b, .22, .6); }
  else if (k === 'dark') { cutMark(K, '150,70,255', 80, 1.2 * K.d, 0, 8); vfx(b, 'arcane', K.T, { big: 1 }); drainBack(K, '200,120,255', 6); groundCrack(K, '170,110,255', 70); shake(b, .25, .7); }
  else if (k === 'demon') { cutMark(K, '255,70,50', e.crit ? 76 : 54, cR(-1.2, 1.2), 0, 6); vfx(b, 'blood', K.T); shake(b, e.crit ? .2 : .1); }
  else { hitSpark(K, k === 'archer' ? '150,255,170' : '255,225,120', e.crit ? 14 : 8, 1); if (e.crit) { column(K, K.tx, '255,225,120', 16, 0, .3); shake(b, .2, .5); } }
  if (e.crit) vfx(b, 'crit', K.T); }
