/* Bones2DFX: the effects that go with the shared moves (rig2d/bones.js), drawn in code, no pictures needed except the weapon's own.
   - charge: while a 'throw' winds up, light gathers round the weapon (soft glow + sparks that orbit and fall in);
   - release (move event): the weapon picture flies off from the hand with a glowing trail, sparks burst at the hand, a short white flash;
   - impact: where the bolt lands, a burst ring + sparks.
   Use:  const fx = Bones2DFX.create();  each frame after player.update + player.draw:  fx.step(player, dt, { ground, scale, left, range });  fx.draw(ctx);
         fx.on = name => ...   (optional callback when a bolt lands: 'impact') */
'use strict';
const Bones2DFX = (() => {
  const TAU = Math.PI * 2, rnd = (a, b) => a + Math.random() * (b - a);
  function create(opt) {
    opt = opt || {}; const F = { parts: [], shots: [], flash: 0, col: opt.col || [150, 210, 255], core: opt.core || [255, 248, 210], on: null };
    const spark = (x, y, vx, vy, life, size, c) => F.parts.push({ x, y, vx, vy, life, t: 0, size, c: c || F.col });
    F.step = (P, dt, o) => {
      o = o || {}; const sc = o.scale || 1, rig = P.rig, wk = Object.keys(rig.parts).find(k => rig.parts[k].role === 'weapon'), dir = (rig.flip ? -1 : 1) * (o.left ? -1 : 1);
      const mv = P.move, u = mv && mv.dur ? P.t / mv.dur : 0, cl = P.clip, c = cl ? (cl.release && P.clipPoint(cl.release)) : wk && P.centre(wk);
      if (cl && P.fired.includes('release') && c) { const im = rig.img[wk], k = P.clipV ? Math.abs(P.clipV[1]) : 1, d2 = (cl.dirx || 1) * (P.clipV && P.clipV[0] < 0 ? -1 : 1); F.shots.push({ x: c[0], y: c[1], vx: d2 * 1500 * sc, vy: 0, ang: d2 > 0 ? Math.PI / 2 : -Math.PI / 2, ta: d2 > 0 ? Math.PI / 2 : -Math.PI / 2, im, w: im.width * k * (cl.boltScale || .55), h: im.height * k * (cl.boltScale || .55), t: 0, life: (o.range || 520) * sc / (1500 * sc), trail: [] }); for (let i = 0; i < 26; i++) { const a = rnd(0, TAU), v = rnd(150, 520) * sc; spark(c[0], c[1], Math.cos(a) * v + d2 * 200 * sc, Math.sin(a) * v, rnd(.2, .45), rnd(2, 5) * sc); } F.flash = .12; F.ring = { x: c[0], y: c[1], t: 0, r: 70 * sc }; }
      if (P.name === 'throw' && !cl && c && u > .22 && u < .5) {   /* charge */
        const k = Math.min(1, (u - .22) / .22); F.charge = { x: c[0], y: c[1], k, r: 40 * sc * (.6 + .6 * k) };
        for (let i = 0; i < 3; i++) { const a = rnd(0, TAU), d = rnd(30, 70) * sc; spark(c[0] + Math.cos(a) * d, c[1] + Math.sin(a) * d, -Math.cos(a) * d * 3.5, -Math.sin(a) * d * 3.5, .22, rnd(2, 4) * sc); }
      } else F.charge = null;
      if (!cl && P.fired.includes('release') && c) {
        const im = P.image(wk), ang = P.angle(wk), s = Math.hypot(P.view ? P.view[0] : 1, P.view ? P.view[1] : 0) * (rig.parts[wk].s || 1);
        F.shots.push({ x: c[0], y: c[1], vx: dir * 1500 * sc, vy: 0, ang, ta: dir > 0 ? Math.PI / 2 : -Math.PI / 2, im, w: im.width * s * .9, h: im.height * s * .9, t: 0, life: (o.range || 520) * sc / (1500 * sc), trail: [] });
        for (let i = 0; i < 26; i++) { const a = rnd(0, TAU), v = rnd(150, 520) * sc; spark(c[0], c[1], Math.cos(a) * v + dir * 200 * sc, Math.sin(a) * v, rnd(.2, .45), rnd(2, 5) * sc); }
        F.flash = .12; F.ring = { x: c[0], y: c[1], t: 0, r: 70 * sc };
      }
      if (P.fired.includes('hit') && wk && !cl) {   /* a stab lands: a burst + a streak at the weapon's point (the top of its picture) */
        const im = rig.img[wk], q = rig.parts[wk], tip = P.at(wk, im.width / 2 - q.pv[0], 4 - q.pv[1]), base = P.at(wk, im.width / 2 - q.pv[0], im.height * .6 - q.pv[1]);
        if (tip) { const dx = tip[0] - base[0], dy = tip[1] - base[1], dl = Math.hypot(dx, dy) || 1; F.streak = { x: tip[0], y: tip[1], ux: dx / dl, uy: dy / dl, t: 0, L: 120 * sc };
          for (let i = 0; i < 30; i++) { const a = Math.atan2(dy, dx) + rnd(-.9, .9), v = rnd(200, 700) * sc; spark(tip[0], tip[1], Math.cos(a) * v, Math.sin(a) * v, rnd(.2, .5), rnd(2, 5) * sc); }
          F.ring2 = { x: tip[0], y: tip[1], t: 0, r: 80 * sc }; F.flash = Math.max(F.flash, .05); } }
      if (F.streak) F.streak.t += dt;
      for (const s of F.shots) { s.t += dt; s.x += s.vx * dt; s.y += s.vy * dt; s.ang += (s.ta - s.ang) * Math.min(1, dt * 18); s.trail.push([s.x, s.y]); if (s.trail.length > 9) s.trail.shift();
        if (Math.random() < .9) spark(s.x - dir * rnd(0, 30) * sc, s.y + rnd(-14, 14) * sc, -s.vx * .12, rnd(-90, 90) * sc, .25, rnd(1.5, 3.5) * sc);
        if (s.t >= s.life && !s.hit) { s.hit = 1; F.ring2 = { x: s.x, y: s.y, t: 0, r: 110 * sc }; F.flash = Math.max(F.flash, .08); for (let i = 0; i < 40; i++) { const a = rnd(0, TAU), v = rnd(200, 700) * sc; spark(s.x, s.y, Math.cos(a) * v, Math.sin(a) * v - 120 * sc, rnd(.25, .6), rnd(2, 6) * sc); } if (F.on) F.on('impact', s); } }
      F.shots = F.shots.filter(s => !s.hit);
      for (const p of F.parts) { p.t += dt; p.x += p.vx * dt; p.y += p.vy * dt; p.vx *= .9; p.vy = p.vy * .9 + 300 * sc * dt; } F.parts = F.parts.filter(p => p.t < p.life);
      F.flash = Math.max(0, F.flash - dt); for (const r of [F.ring, F.ring2]) if (r) r.t += dt;
      F.W = o.width || 0; F.H = o.height || 0;
    };
    F.draw = ctx => {
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'lighter'; const [r, g, b] = F.col, [cr, cg, cb] = F.core;
      const glow = (x, y, rad, a) => { const gr = ctx.createRadialGradient(x, y, 0, x, y, rad); gr.addColorStop(0, `rgba(${cr},${cg},${cb},${a})`); gr.addColorStop(.35, `rgba(${r},${g},${b},${a * .6})`); gr.addColorStop(1, `rgba(${r},${g},${b},0)`); ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(x, y, rad, 0, TAU); ctx.fill(); };
      if (F.charge) { const c = F.charge, fl = .75 + .25 * Math.sin(performance.now() / 40); glow(c.x, c.y, c.r * fl, .55 * c.k + .2); }
      for (const s of F.shots) {
        for (let i = 0; i < s.trail.length; i++) { const [x, y] = s.trail[i], k = (i + 1) / s.trail.length; glow(x, y, s.h * .35 * k, .35 * k); }
        glow(s.x, s.y, s.h * .55, .7); ctx.save(); ctx.globalCompositeOperation = 'source-over'; ctx.translate(s.x, s.y); ctx.rotate(s.ang); ctx.drawImage(s.im, -s.w / 2, -s.h / 2, s.w, s.h); ctx.restore(); }
      for (const p of F.parts) { const k = 1 - p.t / p.life; ctx.fillStyle = `rgba(${p.c[0]},${p.c[1]},${p.c[2]},${k})`; ctx.beginPath(); ctx.arc(p.x, p.y, p.size * (.5 + k * .5), 0, TAU); ctx.fill(); ctx.fillStyle = `rgba(255,255,255,${k * .8})`; ctx.beginPath(); ctx.arc(p.x, p.y, p.size * .4, 0, TAU); ctx.fill(); }
      for (const ri of [F.ring, F.ring2]) { if (!ri || ri.t > .35) continue; const k = ri.t / .35; ctx.strokeStyle = `rgba(${r},${g},${b},${(1 - k) * .9})`; ctx.lineWidth = 10 * (1 - k) + 2; ctx.beginPath(); ctx.arc(ri.x, ri.y, ri.r * (.3 + k), 0, TAU); ctx.stroke(); glow(ri.x, ri.y, ri.r * .6 * (1 - k * .5), .6 * (1 - k)); }
      if (F.streak && F.streak.t < .22) { const s = F.streak, k = s.t / .22, L = s.L * (.4 + k), x0 = s.x - s.ux * L * .6, y0 = s.y - s.uy * L * .6, x1 = s.x + s.ux * L * .5, y1 = s.y + s.uy * L * .5, gr = ctx.createLinearGradient(x0, y0, x1, y1);
        gr.addColorStop(0, `rgba(${r},${g},${b},0)`); gr.addColorStop(.7, `rgba(${cr},${cg},${cb},${(1 - k) * .95})`); gr.addColorStop(1, `rgba(255,255,255,0)`); ctx.strokeStyle = gr; ctx.lineWidth = 16 * (1 - k) + 3; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); }
      if (F.flash > 0 && F.W) { ctx.fillStyle = `rgba(255,255,255,${F.flash * 1.6})`; ctx.fillRect(0, 0, F.W, F.H); }
      ctx.restore();
    };
    F.busy = () => F.parts.length || F.shots.length || F.charge;
    return F;
  }
  return { create };
})();
if (typeof module !== 'undefined') module.exports = Bones2DFX;
