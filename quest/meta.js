/* quest/meta.js: the long game round the fighting: PixelLab icons, the blacksmith (gold -> upgrades), the quest chain with a guide
   arrow, the minimap. Loaded last; hooks: drawMeta (from drawHUD), metaPointer / metaKey (from the input handlers), questEvent. */
'use strict';
const ICONIMG = new Image(); ICONIMG.src = 'art/quest/icons.png?v=' + VER;
const IIDX = { atk: 0, 0: 1, 1: 2, 2: 3, dodge: 4, up_atk: 5, up_hp: 6, quest: 7 };
function icon(g, name, cx, cy, r, dim) {   /* replaces the code-drawn glyphs of ui.js; r = half the room it has, in texels */
  if (!ICONIMG.complete || !ICONIMG.naturalWidth) return; const sc = Math.max(1, Math.floor(r * 1.85 / 32)), sz = 32 * sc;
  g.globalAlpha = dim ? .4 : 1; g.drawImage(ICONIMG, IIDX[name] * 32, 0, 32, 32, Math.round(cx - sz / 2), Math.round(cy - sz / 2), sz, sz); g.globalAlpha = 1;
}

/* ---------- blacksmith */
const SHOP = { x: VILLAGE.x + 7.4, z: VILLAGE.z - 2.0, open: false, near: false };
const UPS = [{ k: 'atk', ic: 'up_atk', name: 'ลับคมดาบ', sub: 'พลังโจมตี +10% ต่อระดับ', base: 40 }, { k: 'hp', ic: 'up_hp', name: 'เสริมเกราะ', sub: 'พลังชีวิต +10% ต่อระดับ', base: 35 }];
const upCost = q => Math.round(q.base * Math.pow(1.5, SAVE.up[q.k]) / 5) * 5;
function buyUp(q) {
  const c = upCost(q); if (SAVE.gold < c || SAVE.up[q.k] >= 20) { sfx('hurt'); return; }
  SAVE.gold -= c; SAVE.up[q.k]++; const r = P.hp / P.max; calcStats(); P.hp = q.k === 'hp' ? P.max : Math.round(P.max * r); sfx('level'); questEvent('up'); saveGame();
  sparks(SHOP.x, groundH(SHOP.x, SHOP.z) + 1.2, SHOP.z, 16, K.white, K.orange, 7, .5, 2); flashLight(SHOP.x, groundH(SHOP.x, SHOP.z) + 1.5, SHOP.z, 0xffa040, 2, .4, 8);
}
function openShop(v) { SHOP.open = v; G.paused = v; if (v) sfx('coin'); }

/* ---------- quests */
const QUESTS = [
  { m: 'mush', n: 6, txt: 'กำจัดเห็ดน้อย', gold: 30, xp: 30, at: [-15, 22] },
  { m: 'slime', n: 6, txt: 'กำจัดสไลม์ใบไม้', gold: 40, xp: 40, at: [13, 23] },
  { up: 1, n: 1, txt: 'ตีบวกที่ช่างตีเหล็กในค่าย', gold: 20, xp: 20, at: [SHOP.x, SHOP.z] },
  { m: 'king', n: 1, txt: 'ปราบราชาเห็ด', gold: 150, xp: 200, at: [KINGSPOT.x, KINGSPOT.z] },
  { m: 'wolf', n: 8, txt: 'ล่าหมาป่าเงิน', gold: 90, xp: 150, at: [20, 13] },
  { m: 'goblin', n: 8, txt: 'กำจัดก็อบลิน', gold: 110, xp: 180, at: [33, 15] },
  { m: 'ghost', n: 8, txt: 'ปราบผีโคมไฟ', gold: 160, xp: 300, at: [15, -41] },
  { m: 'skel', n: 8, txt: 'ทลายนักรบกระดูก', gold: 190, xp: 350, at: [-2, -32] },
  { m: 'dragon', n: 1, txt: 'ปราบมังกรราตรี', gold: 1000, xp: 1500, at: [LAIR.x, LAIR.z] },
];
const curQuest = () => QUESTS[SAVE.q || 0] || null;
function questEvent(kind, type) {
  const q = curQuest(); if (!q) return; if (kind === 'kill' ? q.m !== type : !q.up) return;
  SAVE.qn = (SAVE.qn || 0) + 1; if (SAVE.qn < q.n) return;
  SAVE.q = (SAVE.q || 0) + 1; SAVE.qn = 0; SAVE.gold += q.gold; gainXP(q.xp); sfx('level');
  after(.9, () => { G.msg = { t: 0, life: 3, txt: 'เควสสำเร็จ!  +' + q.gold + ' ทอง', big: true, col: '#ffe27a' }; }); saveGame();
}

/* ---------- minimap */
let MINI = null;
function buildMini() { const S = 64, c = document.createElement('canvas'); c.width = c.height = S; const g = c.getContext('2d'), im = g.createImageData(S, S);
  for (let j = 0; j < S; j++) for (let i = 0; i < S; i++) { const x = -MH + (i + .5) * MS / S, z = -MH + (j + .5) * MS / S, m = mapAt(x, z), h = groundH(x, z), k = (j * S + i) * 4;
    let c3 = m[1] > .5 ? [44, 58, 104] : m[0] > .5 ? [198, 140, 62] : [96, 168, 70]; if (m[2] > .5) c3 = m[1] > .5 ? [92, 86, 130] : [214, 176, 122]; if (h < WY) c3 = [70, 150, 220]; if (Math.max(Math.abs(x), Math.abs(z)) > 57) c3 = [30, 40, 44];
    im.data[k] = c3[0]; im.data[k + 1] = c3[1]; im.data[k + 2] = c3[2]; im.data[k + 3] = 255; }
  g.putImageData(im, 0, 0); MINI = c; }

/* ---------- drawing + input */
let HITS = [];
function hitBox(x, y, w, h, f) { HITS.push({ x, y, w, h, f }); }
function panel(g, x, y, w, h, u) { g.fillStyle = '#0c0816'; g.fillRect(x - u, y - u, w + 2 * u, h + 2 * u); g.fillStyle = '#8fd8ff'; g.fillRect(x, y, w, h); g.fillStyle = '#241838'; g.fillRect(x + u, y + u, w - 2 * u, h - 2 * u); g.fillStyle = '#34245a'; g.fillRect(x + u, y + u, w - 2 * u, 2 * u); }
function drawMeta(g, W, H, u, dt) {
  HITS = []; if (!G.started) return; const f = Math.max(.75, u * PX.T / 2);
  /* minimap */
  if (!MINI) buildMini(); const mm = 54 * u, mx = W - mm - 4 * u, my = 16 * u, w2m = (x, z) => [mx + (x + MH) / MS * mm, my + (z + MH) / MS * mm];
  g.fillStyle = '#0c0816'; g.fillRect(mx - u, my - u, mm + 2 * u, mm + 2 * u); g.globalAlpha = .9; g.drawImage(MINI, mx, my, mm, mm); g.globalAlpha = 1;
  const dot = (x, z, c, s) => { const p = w2m(x, z); g.fillStyle = '#120a1c'; g.fillRect(Math.round(p[0] - s / 2) - 1, Math.round(p[1] - s / 2) - 1, s + 2, s + 2); g.fillStyle = c; g.fillRect(Math.round(p[0] - s / 2), Math.round(p[1] - s / 2), s, s); };
  dot(VILLAGE.x, VILLAGE.z, '#ffe9a8', 2 * u); dot(LAIR.x, LAIR.z, '#ff5ad0', 2 * u); const q = curQuest(); if (q && Math.floor(G.time * 3) % 2) dot(q.at[0], q.at[1], '#ffd23c', 2 * u); dot(P.x, P.z, '#ffffff', 2 * u);
  /* quest line */
  if (q) { const y = my + mm + 3 * u + 16; icon(g, 'quest', W - 4 * u - 16, y, 18); T(q.txt + (q.n > 1 ? '  ' + (SAVE.qn || 0) + '/' + q.n : ''), W - 4 * u - 36, y - 1, 13, '#ffe9a8', 'right'); T('รางวัล ' + q.gold + ' ทอง', W - 4 * u - 36, y + 11 / PX.T + 2, 10.5, '#d8f0ff', 'right', 600);
    const dx = q.at[0] - P.x, dz = q.at[1] - P.z, d = Math.hypot(dx, dz);
    if (d > 13 && !SHOP.open && !P.dead) { const sx = dx, sy = dz * SP, l = Math.hypot(sx, sy), ax = sx / l, ay = sy / l, hp = toLo(P.x, P.y + 1, P.z), r = (30 + Math.sin(G.time * 5) * 2) * u, cx = hp[0] + ax * r, cy = hp[1] + ay * r;
      for (let pass = 0; pass < 2; pass++) { g.fillStyle = pass ? '#ffd23c' : '#1a1024'; const o = pass ? 0 : u; g.beginPath(); g.moveTo(cx + ax * (6 * u + o), cy + ay * (6 * u + o)); g.lineTo(cx - ax * 3 * u - ay * (4 * u + o), cy - ay * 3 * u + ax * (4 * u + o)); g.lineTo(cx - ax * 3 * u + ay * (4 * u + o), cy - ay * 3 * u - ax * (4 * u + o)); g.closePath(); g.fill(); } } }
  else T('ทำเควสครบแล้ว!', W - 6 * u, my + mm + 14 * u, 13, '#ffe9a8', 'right');
  /* blacksmith */
  SHOP.near = !P.dead && Math.hypot(P.x - SHOP.x, P.z - SHOP.z) < 3.6; const sp = toLo(SHOP.x, groundH(SHOP.x, SHOP.z) + 3.4 + Math.sin(G.time * 3) * .12, SHOP.z);
  if (!SHOP.open) { if (sp[0] > 0 && sp[0] < W && sp[1] > 0 && sp[1] < H) icon(g, 'up_atk', sp[0], sp[1], 9 * u * (PX.T < 1.3 ? 2 : 1));
    if (SHOP.near) { const bw = 78 * u, bh = 18 * u, bx = Math.round(W / 2 - bw / 2), by = Math.round(H * .68); panel(g, bx, by, bw, bh, u); icon(g, 'up_atk', bx + 10 * u, by + bh / 2, 8 * u); T(IN.touch ? 'ตีบวกอาวุธ' : 'ตีบวกอาวุธ  [F]', bx + bw / 2 + 8 * u, by + bh / 2 + 4 * u, 13 * f, '#ffe9a8', 'center'); hitBox(bx, by, bw, bh, () => openShop(true)); } return; }
  g.fillStyle = 'rgba(8,4,16,.55)'; g.fillRect(0, 0, W, H);
  const pw = Math.min(W - 12 * u, 176 * u), ph = 92 * u, px = Math.round(W / 2 - pw / 2), py = Math.round(H / 2 - ph / 2); panel(g, px, py, pw, ph, u);
  T('ช่างตีเหล็ก', px + 8 * u, py + 13 * u, 17 * f, '#ffe27a'); g.drawImage(ICON.tex.image, 0, 0, 8, 8, px + pw - 62 * u, py + 5 * u, 8 * u, 8 * u); T(String(SAVE.gold), px + pw - 51 * u, py + 12.5 * u, 14 * f, '#ffd23c');
  const cx = px + pw - 12 * u; g.fillStyle = '#c8405a'; g.fillRect(cx - 7 * u, py + 3 * u, 14 * u, 11 * u); T('X', cx, py + 12 * u, 13 * f, '#fff', 'center'); hitBox(cx - 9 * u, py, 18 * u, 16 * u, () => openShop(false));
  UPS.forEach((q, i) => { const y = py + 20 * u + i * 34 * u, c = upCost(q), ok = SAVE.gold >= c && SAVE.up[q.k] < 20; g.fillStyle = '#1a1028'; g.fillRect(px + 5 * u, y, pw - 10 * u, 30 * u);
    icon(g, q.ic, px + 21 * u, y + 15 * u, 17 * u * (PX.T < 1.3 ? 1 : .56)); T(q.name + '  +' + SAVE.up[q.k], px + 40 * u, y + 12 * u, 14 * f, '#fff'); T(q.sub + (q.k === 'atk' ? '  (ตอนนี้ ' + Math.round(P.atk) + ')' : '  (ตอนนี้ ' + P.max + ')'), px + 40 * u, y + 23 * u, 10 * f, '#b8c8e8', 'left', 600);
    const bw = 44 * u, bx = px + pw - bw - 9 * u, by = y + 6 * u; g.fillStyle = '#0c0816'; g.fillRect(bx - u, by - u, bw + 2 * u, 18 * u + 2 * u); g.fillStyle = ok ? '#3aa860' : '#4a4458'; g.fillRect(bx, by, bw, 18 * u); g.fillStyle = ok ? '#6fe08a' : '#5e586c'; g.fillRect(bx, by, bw, 2 * u);
    g.drawImage(ICON.tex.image, 0, 0, 8, 8, bx + 4 * u, by + 5 * u, 8 * u, 8 * u); T(SAVE.up[q.k] >= 20 ? 'เต็ม' : String(c), bx + bw / 2 + 6 * u, by + 13 * u, 14 * f, ok ? '#fff' : '#a8a0b8', 'center'); hitBox(bx - 2 * u, by - 2 * u, bw + 4 * u, 22 * u, () => buyUp(q)); });
}
function metaPointer(x, y) { for (const h of HITS) if (x >= h.x && x <= h.x + h.w && y >= h.y && y <= h.y + h.h) { h.f(); return true; } if (SHOP.open) { openShop(false); return true; } return false; }
function metaKey(code) { if (code === 'KeyF' && (SHOP.near || SHOP.open)) { openShop(!SHOP.open); return true; } if (SHOP.open) { if (code === 'Escape') openShop(false); else if (code === 'Digit1') buyUp(UPS[0]); else if (code === 'Digit2') buyUp(UPS[1]); return true; } return false; }
