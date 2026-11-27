/* TIMELINE = make a move INSIDE the tool, like Spine's animate mode (owner 2026-11-28: "Spine 2D ทำงานแบบไหน ... เอามาทำของเรา").
   Loaded by rig.html after its own script; uses its globals (R, B, PL, PLAY, SEL, PAN, LEFT, DPR, W, H, ctx, $, vnow, hit, select, save, stop, play, hint).
   - pick a piece (tap it) = pick its ROLE; a move is keyed per role, so a move made on one hero plays on every hero;
   - drag the piece = turn it at the time under the playhead (or move / size it: the buttons under the sliders); a key is set by itself (auto-key);
   - the bar at the bottom = the time: tap / drag to go to a time, diamonds = keys (yellow = the picked role), red = a release moment (ปล่อยของ);
   - the ease of a key = how the pose travels INTO that key from the one before;
   - "เก็บท่า" keeps it in the rig (rig.moves, saved with the rig: คัดลอกส่ง Claude / ดาวน์โหลด), "ส่งออกท่า" = a moves file a game loads with Bones2D.addMoves. */
const TL = { on: false, key: '', mv: null, u: 0, role: 'armF', play: false, gap: 0, tool: 'r', drag: null, msg: '', msgT: 0 };
const TLON = () => TL.on && PLAY === '_tl';
function tlLeave() { if (!TL.on) return; TL.on = false; TL.play = false; TL.drag = null; if (document.getElementById('tlEd')) tlUI(); }
const TL_EASE = { lin: 'เส้นตรง', out: 'เร็วแล้วช้า', in: 'ช้าแล้วเร็ว', io: 'ช้า-เร็ว-ช้า', back: 'เลยแล้วเด้งกลับ', snap: 'ดีดทันที', hold: 'ค้างแล้วกระโดด' };
const TL_CH = [['r', 'หมุน', -180, 180, 1, '°'], ['x', 'ย้าย ซ้าย-ขวา', -60, 60, .5, ''], ['y', 'ย้าย ขึ้น-ลง', -60, 60, .5, ''], ['s', 'ขนาด', .2, 2.5, .01, 'x'], ['sx', 'ยืด กว้าง', .2, 2.5, .01, 'x'], ['sy', 'ยืด สูง', .2, 2.5, .01, 'x'], ['a', 'ความชัด', 0, 1, .05, '']];
const TL_PERIOD = { idle: .64, walk: .9, run: .5 };

function tlInit() {
  const box = document.createElement('div'); box.id = 'tlBox';
  box.innerHTML = `<h3>สร้างท่าเอง (ไทม์ไลน์ แบบ Spine)</h3>
  <div class="row"><button id="tlNew">ท่าใหม่</button><button id="tlFromB">เริ่มจากท่า</button></div>
  <select id="tlFrom" style="width:100%"></select>
  <label>ท่าของฉัน</label><select id="tlPick" style="width:100%"></select>
  <div id="tlEd" style="display:none">
  <label>ชื่อท่า</label><input id="tlName" style="width:100%;box-sizing:border-box;height:30px;border-radius:8px;border:0;padding:0 8px;font:600 13px system-ui">
  <label>ความยาว <span id="tlVd"></span></label><input id="tlDur" type="range" min="0.2" max="3" step="0.05">
  <div class="row"><button id="tlPlay">▶ เล่น</button><button id="tlLoop">วนซ้ำ</button></div>
  <label>ขยับส่วนไหน</label><select id="tlRole" style="width:100%"></select>
  <div class="row"><button id="tlTr" class="on">ลาก = หมุน</button><button id="tlTm">ลาก = ย้าย</button><button id="tlTs">ลาก = ขนาด</button></div>
  <div id="tlSl"></div>
  <div class="row"><button id="tlZ">อยู่หน้าสุด</button></div>
  <div class="row"><button id="tlPrev">◀ คีย์</button><button id="tlNext">คีย์ ▶</button></div>
  <div class="row"><button id="tlKey">ใส่คีย์</button><button id="tlDel" class="r">ลบคีย์</button></div>
  <label>ช่วงก่อนคีย์นี้ขยับแบบ</label><select id="tlEase" style="width:100%"></select>
  <div class="row"><button id="tlEv">จังหวะปล่อยของ</button><button id="tlCopyK">คัดลอกคีย์แรกไปท้าย</button></div>
  <div class="row"><button id="tlSave" class="g">เก็บท่า</button><button id="tlOff">เลิกแก้</button></div>
  <div class="row"><button id="tlDelMv" class="r">ลบท่านี้</button><button id="tlOut">ส่งออกท่า</button></div>
  </div>`;
  const h = [...document.querySelectorAll('#pn h3')].find(e => e.textContent.startsWith('ต่อชิ้น')); $('#pn').insertBefore(box, h);
  const opt = (sel, v, t) => { const o = document.createElement('option'); o.value = v; o.textContent = t; $(sel).append(o); };
  for (const k in B.MOVES) if (!(R.view === 'front' && (k === 'walk' || k === 'run'))) opt('#tlFrom', k, (B.MOVES[k].n || B.NAMES[k] || k));
  for (const e in TL_EASE) opt('#tlEase', e, TL_EASE[e]);
  const roles = [...new Set(names.map(k => R.parts[k].role).filter(r => r && r !== 'none'))]; opt('#tlRole', '_root', 'ทั้งตัว (กระโดด / เอียง / ยืด)'); for (const r of roles) opt('#tlRole', r, B.ROLES[r] || r);
  $('#tlSl').innerHTML = TL_CH.map(([c, n, a, b, st]) => `<label>${n} <span id="tlV_${c}"></span></label><input id="tlS_${c}" type="range" min="${a}" max="${b}" step="${st}">`).join('');
  for (const [c] of TL_CH) $('#tlS_' + c).oninput = e => { tlSet({ [c]: +e.target.value }); };
  $('#tlNew').onclick = () => tlOpen(tlNewKey(), { n: 'ท่าใหม่ ' + (Object.keys(R.moves || {}).length + 1), dur: .8, tracks: {}, ev: [] });
  $('#tlFromB').onclick = () => { const k = $('#tlFrom').value; tlOpen(tlNewKey(), tlCopy(k)); };
  $('#tlPick').onchange = e => { const k = e.target.value; if (k && R.moves && R.moves[k]) tlOpen(k, JSON.parse(JSON.stringify(R.moves[k]))); };
  $('#tlName').oninput = e => { if (TL.mv) TL.mv.n = e.target.value; };
  $('#tlDur').oninput = e => { if (!TL.mv) return; TL.mv.dur = +e.target.value; tlUI(); };
  $('#tlPlay').onclick = () => { TL.play = !TL.play; TL.gap = 0; tlUI(); };
  $('#tlLoop').onclick = () => { TL.mv.loop = !TL.mv.loop; tlUI(); };
  $('#tlRole').onchange = e => { TL.role = e.target.value; tlUI(); };
  for (const [id, t] of [['#tlTr', 'r'], ['#tlTm', 'm'], ['#tlTs', 's']]) $(id).onclick = () => { TL.tool = t; tlUI(); };
  $('#tlZ').onclick = () => { const v = tlVal(); tlSet({ z: v.z > 1.5 ? 0 : 2 }); };
  $('#tlKey').onclick = () => { tlSet({}); tlSay('ใส่คีย์แล้ว'); };
  $('#tlDel').onclick = () => { const tr = tlTrack(false), i = tr ? tlKeyAt(tr) : -1; if (i < 0) { tlSay('ตรงนี้ไม่มีคีย์'); return; } tr.splice(i, 1); if (!tr.length) delete TL.mv.tracks[TL.role]; tlUI(); };
  $('#tlEase').onchange = e => { const tr = tlTrack(false), i = tr ? tlKeyAt(tr) : -1; if (i < 0) { tlSay('เลือกคีย์ก่อน (เลื่อนเวลาไปที่คีย์)'); return; } tr[i][2] = e.target.value; };
  $('#tlPrev').onclick = () => tlJump(-1); $('#tlNext').onclick = () => tlJump(1);
  $('#tlEv').onclick = () => { const ev = TL.mv.ev || (TL.mv.ev = []), i = ev.findIndex(e => Math.abs(e[0] - TL.u) < .02); if (i >= 0) ev.splice(i, 1); else { ev.push([+TL.u.toFixed(3), 'release']); ev.sort((a, b) => a[0] - b[0]); } tlSay(i >= 0 ? 'เอาจังหวะปล่อยของออก' : 'ใส่จังหวะปล่อยของ (ลูกธนู / สายฟ้า ออกจากมือตรงนี้)'); };
  $('#tlCopyK').onclick = () => { const tr = tlTrack(false); if (!tr || !tr.length) return; const f = tr[0], i = tr.findIndex(k => Math.abs(k[0] - 1) < .004); if (i >= 0) tr[i][1] = Object.assign({}, f[1]); else tr.push([1, Object.assign({}, f[1]), 'io']); tlSay('ท้ายท่ากลับมาเหมือนต้นท่า (วนได้เนียน)'); };
  $('#tlSave').onclick = () => { R.moves = R.moves || {}; R.moves[TL.key] = JSON.parse(JSON.stringify(TL.mv)); save(); tlList(); tlButtons(); tlSay('เก็บท่า "' + TL.mv.n + '" แล้ว (อยู่ในปุ่มท่าด้านบนด้วย)'); };
  $('#tlOff').onclick = () => stop();
  $('#tlDelMv').onclick = () => { if (!R.moves || !R.moves[TL.key]) { stop(); return; } if (!confirm('ลบท่า "' + TL.mv.n + '" ?')) return; delete R.moves[TL.key]; save(); stop(); tlList(); tlButtons(); };
  $('#tlOut').onclick = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify({ moves: R.moves || {} }, null, 1)], { type: 'application/json' })); a.download = (R.name || CHAR) + '_moves.json'; a.click(); };
  tlList(); tlButtons(); tlUI();
}
const tlNewKey = () => { let i = 1; while ((R.moves && R.moves['my' + i]) || B.MOVES['my' + i]) i++; return 'my' + i; };
function tlCopy(k) {   /* a shared move as keys; a move made of a formula (idle / walk / run) is sampled into 16 keys over one round */
  const m = B.MOVES[k]; if (!m.fn) { const o = JSON.parse(JSON.stringify({ dur: m.dur, loop: !!m.loop, hold: !!m.hold, upright: !!m.upright, tracks: m.tracks, ev: m.ev || [] })); o.n = (m.n || B.NAMES[k] || k) + ' (แก้)';
    /* a hero seen from the front plays this move's front arm angles (bones.js frontTracks): copy THOSE, as this hero's own role values, so the copy looks the same */
    const FR = R.view === 'front' && m.front ? B.frontTracks(R, m) : null; if (FR) { const fl = R.flip ? -1 : 1;
      for (const role in FR.tracks) { const pk = Object.keys(R.parts).find(q => R.parts[q].role === role); if (!pk) continue; const q = R.parts[pk], sg = /armB|foreB|weaponB/.test(role) ? -fl : fl, g = q.g == null ? 1 : (q.g || 1), fx = FR.fx[role] || 1;
        /* turn from the front angles, every other channel (size, fade, in front) from the move's own keys: keys at both sets of times */
        const side = m.tracks[role] || [], ft = FR.tracks[role], times = [...new Set(side.filter(k => Object.keys(k[1]).some(c => c !== 'r')).map(k => k[0]).concat(ft.map(k => k[0])))].sort((x, y) => x - y)   /* side keys only where they carry more than a turn (size, fade) */, sv = {}, fv = {};
        o.tracks[role] = times.map(u => { B.sample({ dur: 1, tracks: { a: side } }, u, sv); B.sample({ dur: 1, tracks: { a: ft } }, u, fv); const v = tlCompact(Object.assign({}, B.REST, sv.a || {}, { r: (fv.a ? fv.a.r : 0) * fx / (sg * g) }));
          const kf = ft.find(k => Math.abs(k[0] - u) < 1e-6), ks = side.find(k => Math.abs(k[0] - u) < 1e-6); return [u, v, (kf || ks)[2]]; }); } }
    return o; }
  const dur = TL_PERIOD[k] || 1, tracks = {}, out = {}, N = 16; for (let i = 0; i <= N; i++) { const o = m.fn(dur * i / N); for (const r in o) { const f = Object.assign({}, B.REST, o[r]); (tracks[r] = tracks[r] || []).push([+(i / N).toFixed(4), tlCompact(f), 'lin']); } } void out;
  return { n: (B.NAMES[k] || k) + ' (แก้)', dur, loop: true, tracks, ev: [] };
}
function tlCompact(f) { const o = {}; for (const c in B.REST) if (f[c] != null && Math.abs(f[c] - B.REST[c]) > 1e-4) o[c] = +(+f[c]).toFixed(c === 'r' ? 1 : 3); return o; }
function tlOpen(key, mv) { stop(); TL.on = true; TL.key = key; TL.mv = mv; TL.u = 0; TL.play = false; PLAY = '_tl'; PL = B.player(R, { base: null }); PL.play('idle'); PL.move = mv; PL.name = '_tl';
  if (![...$('#tlRole').options].some(o => o.value === TL.role)) TL.role = $('#tlRole').options[1] ? $('#tlRole').options[1].value : '_root'; if (SEL) tlPickPiece(SEL); tlUI(); }
function tlList() { $('#tlPick').innerHTML = ''; const o = document.createElement('option'); o.value = ''; o.textContent = Object.keys(R.moves || {}).length ? '(เลือกท่าที่จะแก้)' : '(ยังไม่มี)'; $('#tlPick').append(o);
  for (const k in R.moves || {}) { const e = document.createElement('option'); e.value = k; e.textContent = R.moves[k].n || k; $('#tlPick').append(e); } }
function tlButtons() {   /* the rig's own moves as buttons among the shared ones */
  for (const b of document.querySelectorAll('#mvs button.my')) b.remove(); const stopB = [...document.querySelectorAll('#mvs button')].find(b => !b.dataset.mv);
  for (const k in R.moves || {}) { const b = document.createElement('button'); b.className = 'mv my'; b.dataset.mv = k; b.textContent = '★ ' + (R.moves[k].n || k); b.onclick = () => play(k); $('#mvs').insertBefore(b, stopB || null); } }
function tlTrack(make) { const t = TL.mv.tracks; if (!t[TL.role] && make) t[TL.role] = []; return t[TL.role]; }
function tlKeyAt(tr) { const fr = 1 / Math.max(1, TL.mv.dur * 30); return tr.findIndex(k => Math.abs(k[0] - TL.u) < fr * .6); }
function tlVal() { const o = {}; B.sample(TL.mv, TL.u * TL.mv.dur, o); return Object.assign({}, B.REST, o[TL.role] || {}); }
function tlSet(ch) {   /* change channels of the picked role at the playhead: the key there is made (with the whole present pose) or changed */
  if (!TL.mv) return; const tr = tlTrack(true), v = tlVal(); if (ch.s != null) { ch.sx = ch.s; ch.sy = ch.s; delete ch.s; } Object.assign(v, ch);
  const u = Math.round(TL.u * TL.mv.dur * 30) / Math.max(1e-6, TL.mv.dur * 30), i = tlKeyAt(tr), val = tlCompact(v);
  if (i >= 0) tr[i][1] = val; else { tr.push([+Math.min(1, u).toFixed(4), val, 'io']); tr.sort((a, b) => a[0] - b[0]); } tlUI(); }
function tlJump(d) { const ks = [...new Set(Object.values(TL.mv.tracks).flat().map(k => k[0]))].sort((a, b) => a - b), fr = .5 / Math.max(1, TL.mv.dur * 30);
  const n = d > 0 ? ks.find(t => t > TL.u + fr) : [...ks].reverse().find(t => t < TL.u - fr); if (n != null) { TL.u = n; TL.play = false; tlUI(); } }
function tlSay(t) { TL.msg = t; TL.msgT = 2.2; }
function tlPickPiece(k) { TL.piece = null; let q = k; while (q && R.parts[q] && (!R.parts[q].role || R.parts[q].role === 'none')) q = R.parts[q].p; const r = q && R.parts[q] ? R.parts[q].role : null;
  if (r && [...$('#tlRole').options].some(o => o.value === r)) { TL.role = r; TL.piece = q; } }
function tlUI() {
  $('#tlEd').style.display = TL.on ? '' : 'none'; if (!TL.on || !TL.mv) return; const m = TL.mv;
  if (document.activeElement !== $('#tlName')) $('#tlName').value = m.n || ''; $('#tlDur').value = m.dur; $('#tlVd').textContent = m.dur.toFixed(2) + ' วินาที';
  $('#tlPlay').textContent = TL.play ? '■ หยุด' : '▶ เล่น'; $('#tlPlay').classList.toggle('on', TL.play); $('#tlLoop').classList.toggle('on', !!m.loop); $('#tlRole').value = TL.role;
  for (const [id, t] of [['#tlTr', 'r'], ['#tlTm', 'm'], ['#tlTs', 's']]) $(id).classList.toggle('on', TL.tool === t);
  const v = tlVal(); for (const [c, , , , , unit] of TL_CH) { const x = c === 's' ? (v.sx + v.sy) / 2 : v[c]; if (document.activeElement !== $('#tlS_' + c)) $('#tlS_' + c).value = x; $('#tlV_' + c).textContent = (Math.abs(x) < 10 ? (+x).toFixed(2) : Math.round(x)) + unit; }
  $('#tlZ').classList.toggle('on', v.z > 1.5); const tr = tlTrack(false), i = tr ? tlKeyAt(tr) : -1; $('#tlEase').value = i >= 0 ? tr[i][2] : 'io'; $('#tlEase').disabled = i < 0;
  hint();
}
/* ---- every frame (rig.html draw() calls these while the timeline is open) */
function tlTick(dt) {
  const m = TL.mv, P = PL; P.pop = +$('#pop').value; P.move = m; P.name = '_tl'; P.from = null; P.done = false; let step = 0;
  if (TL.play) { if (TL.gap > 0) { TL.gap -= dt; if (TL.gap <= 0) TL.u = 0; } else step = dt * +$('#spd').value; }
  P.t = step ? TL.u * m.dur : Math.min(TL.u * m.dur, m.dur - 1e-4); P.update(step); if (TL.play && TL.gap <= 0) { TL.u = Math.min(1, P.t / m.dur); if (!m.loop && TL.u >= 1 - 1e-6) TL.gap = .5; }
  if (TL.msgT > 0) TL.msgT -= dt; if (TL.play && (TL._ui = (TL._ui || 0) + dt) > .25) { TL._ui = 0; tlUI(); }
}
function tlBar() { const pw = $('#pn').classList.contains('hide') ? 0 : 262 * DPR; return { x0: 18 * DPR, x1: W - pw - 18 * DPR, y0: H - 92 * DPR, y1: H - 34 * DPR }; }
function tlDraw() {
  const m = TL.mv, b = tlBar(), X = u => b.x0 + (b.x1 - b.x0) * u, d = DPR; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  if (PL && PL.mats) { const V = vnow(); for (const k of R.order) { const q = R.parts[k]; if (!q.role || q.role === 'none' || /weapon/.test(q.role)) continue; const p = B.pt(B.mul(V, PL.mats[k]), 0, 0), on = q.role === TL.role;
      if (q.p && R.parts[q.p]) { const pp = B.pt(B.mul(V, PL.mats[q.p]), 0, 0); ctx.strokeStyle = on ? '#ffd24a' : '#7fe7c466'; ctx.lineWidth = (on ? 3 : 2) * d; ctx.beginPath(); ctx.moveTo(pp[0], pp[1]); ctx.lineTo(p[0], p[1]); ctx.stroke(); }
      ctx.fillStyle = on ? '#ffd24a' : '#7fe7c4'; ctx.strokeStyle = '#fff'; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.arc(p[0], p[1], (on ? 8 : 4) * d, 0, 7); ctx.fill(); ctx.stroke(); } }
  ctx.fillStyle = '#10141fdd'; ctx.beginPath(); (ctx.roundRect ? ctx.roundRect.bind(ctx) : (x, y, w, h) => ctx.rect(x, y, w, h))(b.x0 - 8 * d, b.y0 - 18 * d, b.x1 - b.x0 + 16 * d, b.y1 - b.y0 + 24 * d, 10 * d); ctx.fill();
  ctx.font = `700 ${11 * d}px system-ui`; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  for (let t = 0; t <= m.dur + 1e-6; t += .1) { const x = X(t / m.dur), big = Math.abs(t * 2 - Math.round(t * 2)) < 1e-3; ctx.fillStyle = big ? '#8fa0c8' : '#4a5678'; ctx.fillRect(x - d * .5, b.y0, d, big ? 8 * d : 5 * d); if (big) ctx.fillText(t.toFixed(1), x, b.y0 - 5 * d); }
  const row = (y, h, col) => { ctx.fillStyle = col; ctx.fillRect(b.x0, y, b.x1 - b.x0, h); };
  row(b.y0 + 12 * d, 14 * d, '#1d2436'); row(b.y0 + 30 * d, 22 * d, '#262f48');
  const dia = (x, y, r, c) => { ctx.fillStyle = c; ctx.beginPath(); ctx.moveTo(x, y - r); ctx.lineTo(x + r, y); ctx.lineTo(x, y + r); ctx.lineTo(x - r, y); ctx.closePath(); ctx.fill(); };
  for (const r in m.tracks) if (r !== TL.role) for (const k of m.tracks[r]) dia(X(k[0]), b.y0 + 19 * d, 4 * d, '#8a94b0');
  for (const k of m.tracks[TL.role] || []) { dia(X(k[0]), b.y0 + 41 * d, 8 * d, '#ffd24a'); ctx.strokeStyle = '#000'; ctx.lineWidth = d; ctx.stroke(); }
  for (const e of m.ev || []) { const x = X(e[0]); ctx.fillStyle = '#ff4a5a'; ctx.beginPath(); ctx.moveTo(x - 6 * d, b.y0 + 12 * d); ctx.lineTo(x + 6 * d, b.y0 + 12 * d); ctx.lineTo(x, b.y0 + 22 * d); ctx.fill(); }
  const x = X(TL.u); ctx.fillStyle = '#fff'; ctx.fillRect(x - d, b.y0 + 8 * d, 2 * d, b.y1 - b.y0 - 6 * d); ctx.fillText((TL.u * m.dur).toFixed(2) + ' s', Math.min(b.x1 - 20 * d, Math.max(b.x0 + 20 * d, x)), b.y1 + 13 * d);
  ctx.textAlign = 'left'; ctx.fillStyle = '#ffd24a'; ctx.fillText((m.n || '') + ' · ' + ($('#tlRole').selectedOptions[0] || {}).textContent, b.x0, b.y0 - 5 * d - 12 * d);
  if (TL.msgT > 0) { ctx.textAlign = 'center'; ctx.font = `700 ${14 * d}px system-ui`; ctx.fillStyle = '#ffffff'; ctx.fillText(TL.msg, (b.x0 + b.x1) / 2, 46 * d); }
}
function tlHint() { return 'สร้างท่า: แตะชิ้นเพื่อเลือก · ' + (TL.tool === 'r' ? 'ลากชิ้น = หมุน' : TL.tool === 'm' ? 'ลากชิ้น = ย้าย' : 'ลากขึ้นลง = ขนาด') + ' (ใส่คีย์ให้เอง) · แถบล่าง = เวลา แตะ/ลากเพื่อเลื่อน · ลากที่ว่าง = เลื่อนจอ'; }
/* ---- pointer (rig.html sends its events here first while the timeline is open; true = used) */
function tlScrub(x) { const b = tlBar(), m = TL.mv; let u = Math.max(0, Math.min(1, (x - b.x0) / (b.x1 - b.x0))); const fr = m.dur * 30; u = Math.round(u * fr) / fr;
  for (const k of Object.values(m.tracks).flat()) if (Math.abs((k[0] - u) * (b.x1 - b.x0)) < 8 * DPR) { u = k[0]; break; } TL.u = u; TL.play = false; tlUI(); }
function tlDown(e) { const x = e.clientX * DPR, y = e.clientY * DPR, b = tlBar(); cv.setPointerCapture(e.pointerId);
  if (y > b.y0 - 18 * DPR && y < b.y1 + 16 * DPR && x > b.x0 - 10 * DPR && x < b.x1 + 10 * DPR) { TL.drag = { k: 'scrub' }; tlScrub(x); return true; }
  const k = hit(x, y); if (!k) { TL.drag = { k: 'pan', x, y, p0: PAN.slice() }; return true; }
  select(k); tlPickPiece(k); if (TL.role === '_root') TL.role = 'body'; TL.play = false; const kk = TL.piece || k, V = vnow(), c = B.pt(B.mul(V, PL.mats[kk]), 0, 0), v = tlVal();
  TL.drag = { k: TL.tool, x, y, c, a0: Math.atan2(y - c[1], x - c[0]), v, kk }; tlUI(); return true; }
function tlMove(e) { const D = TL.drag; if (!D) return false; const x = e.clientX * DPR, y = e.clientY * DPR;
  if (D.k === 'scrub') { tlScrub(x); return true; } if (D.k === 'pan') { PAN = [D.p0[0] + x - D.x, D.p0[1] + y - D.y]; return true; }
  const V = vnow(), sc = Math.abs(V[3]), dir = LEFT ? -1 : 1, q = R.parts[D.kk], fl = R.flip ? -1 : 1, far = /armB|foreB|weaponB/.test(q.role), sg = R.view === 'front' && far ? -fl : fl, g = q.g == null ? 1 : q.g, u = R._u || 1;
  if (D.k === 'r') { let da = (Math.atan2(y - D.c[1], x - D.c[0]) - D.a0) * 180 / Math.PI; da = ((da + 540) % 360) - 180; tlSet({ r: Math.round((D.v.r + da * dir / (sg * (g || 1))) * 2) / 2 }); }
  else if (D.k === 'm') tlSet({ x: +(D.v.x + (x - D.x) / sc * dir / u / fl).toFixed(2), y: +(D.v.y + (y - D.y) / sc / u).toFixed(2) });
  else { const f = Math.max(.2, Math.min(2.5, Math.exp(-(y - D.y) / (120 * DPR)))); tlSet({ sx: +(D.v.sx * f).toFixed(3), sy: +(D.v.sy * f).toFixed(3) }); }
  return true; }
function tlUp() { if (!TL.drag) return false; TL.drag = null; return true; }
