'use strict';
/* ก่อร่างสร้างชาติ: everything the player sees and taps. */
const svg = d => '<svg class="i" viewBox="0 0 24 24" fill="currentColor">' + d + '</svg>';
const IC = {
  pop: svg('<circle cx="12" cy="7" r="4.5"/><path d="M3 22c0-6 4-9 9-9s9 3 9 9z"/>'), money: svg('<circle cx="12" cy="12" r="10"/><path d="M9 6h4.500a3 3 0 0 1 1 5.800A3.200 3.200 0 0 1 14 18H9zM9 12h5M11 4v16" stroke="#14263a" stroke-width="1.700" fill="none"/>'),
  idx: svg('<path d="M3 21V13h4v8zM10 21V8h4v13zM17 21V3h4v18z"/>'), happy: svg('<circle cx="12" cy="12" r="10"/><path d="M7.500 14c1 2.500 2.700 3.600 4.500 3.600s3.500-1.100 4.500-3.600" stroke="#14263a" stroke-width="2" fill="none"/><circle cx="8.500" cy="9" r="1.400" fill="#14263a"/><circle cx="15.500" cy="9" r="1.400" fill="#14263a"/>'), trust: svg('<path d="M12 2l9 4v6c0 5.200-3.800 8.700-9 10-5.200-1.300-9-4.800-9-10V6z"/>'),
  build: svg('<path d="M2 21h20v-2H2zM4 18h6V9H4zM12 18h8V4h-8z"/>'), budget: svg('<path d="M3 6a2 2 0 0 1 2-2h14v4H5v12h15v-3h2v5H5a2 2 0 0 1-2-2zM15 11h7v5h-7a2.500 2.500 0 0 1 0-5z"/>'), country: svg('<path d="M5 2h2v20H5zM8 3h12l-3 4.500L20 12H8z"/>'), future: svg('<path d="M12 2a10 10 0 1 0 10 10h-2a8 8 0 1 1-2.500-5.800L15 9h7V2l-3 3a10 10 0 0 0-7-3z"/><path d="M11 7h2v5l4 2-1 1.800-5-2.800z"/>'), rank: svg('<path d="M7 2h10v2h4v3a5 5 0 0 1-4.300 5 5 5 0 0 1-3.700 3v3h3v3H8v-3h3v-3a5 5 0 0 1-3.700-3A5 5 0 0 1 3 7V4h4z"/>'),
  water: svg('<path d="M12 2s7 7.500 7 13a7 7 0 0 1-14 0C5 9.500 12 2 12 2z"/>'), power: svg('<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>'), edu: svg('<path d="M12 3L1 9l11 6 9-5v7h2V9zM5 14v4c2 2 4.500 3 7 3s5-1 7-3v-4l-7 4z"/>'), health: svg('<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>'), safe: svg('<path d="M12 2l9 4v6c0 5.200-3.800 8.700-9 10-5.200-1.300-9-4.800-9-10V6z"/>'), clean: svg('<path d="M9 2h6l1 2h5v2H3V4h5zM5 8h14l-1.200 14H6.200z"/>'), life: svg('<path d="M12 2l4 7h-2.500l4 6H14v7h-4v-7H6.500l4-6H8z"/>'), state: svg('<path d="M12 2l10 6v2H2V8zM4 12h3v7H4zM10.500 12h3v7h-3zM17 12h3v7h-3zM2 20h20v2H2z"/>'), land: svg('<path d="M2 19c2.500-2 4.500-2 7 0s4.500 2 7 0 4-1.700 6-.5v3c-2-1.200-3.500-1-6 .5s-4.500 1.500-7 0-4.500-1.500-7 0zM5 15c1-5 4-9 8-9s6 3 7 8c-2-.8-3.500-.4-5 .7-2.500 1.700-4.500 1.700-7 0-1-.7-2-.4-3 .3z"/>'), pause: svg('<path d="M6 4h4v16H6zM14 4h4v16h-4z"/>')
};
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const pct = v => Math.round(v * 100) + '%';
const UI = window.UI = { dirty: true, tab: null, cat: 'all', fYears: 10, fIf: 'none', fRes: null };

UI.toast = function (t, kind) { const d = document.createElement('div'); d.className = 'toast ' + kind; d.textContent = t; const T = $('toasts'); T.appendChild(d); while (T.children.length > 4) T.firstChild.remove(); setTimeout(() => d.remove(), 6500); };

const DOCK = [['build', 'สั่งสร้าง'], ['gov', 'รัฐบาล'], ['budget', 'งบ/ภาษี'], ['country', 'ประเทศ'], ['future', 'อนาคต'], ['world', 'โลก']];
IC.gov = IC.state; IC.world = svg('<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm7.900 9h-3.500a15 15 0 0 0-1.800-6.600A8 8 0 0 1 19.900 11zM12 4c1 1 2.200 3.500 2.400 7H9.600C9.800 7.500 11 5 12 4zM4.100 13h3.500a15 15 0 0 0 1.800 6.600A8 8 0 0 1 4.100 13zm3.500-2H4.100a8 8 0 0 1 5.300-6.600A15 15 0 0 0 7.600 11zM12 20c-1-1-2.200-3.500-2.400-7h4.800c-.2 3.500-1.400 6-2.400 7zm2.600-.4a15 15 0 0 0 1.800-6.600h3.500a8 8 0 0 1-5.300 6.600z"/>');
const TITLES = { world: 'โลกและเพื่อนบ้าน', gov: 'รัฐบาลของคุณ', build: 'สั่งสร้างของส่วนรวม', budget: 'งบประมาณและภาษี', country: 'สถานะประเทศ', future: 'จำลองอนาคต', rank: 'อันดับโลก' };
UI.init = function () {
  $('dock').innerHTML = DOCK.map(d => '<button data-tab="' + d[0] + '">' + IC[d[0]] + '<span>' + d[1] + '</span></button>').join('');
  $('speed').innerHTML = [[0, IC.pause], [1, '1'], [3, '3'], [10, '10']].map(s => '<button data-sp="' + s[0] + '" aria-label="ความเร็ว ' + s[0] + '">' + s[1] + '</button>').join('');
  $('dock').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) UI.openTab(b.dataset.tab); });
  $('speed').addEventListener('click', e => { const b = e.target.closest('[data-sp]'); if (b) { G.speed = +b.dataset.sp; UI.speedBtn(); } });
  $('sClose').onclick = () => UI.closeSheet();
  $('sbody').addEventListener('click', UI.sheetClick); $('sbody').addEventListener('input', UI.sheetInput);
  $('cname').value = pick(COUNTRY_NAMES); if (hasSave()) $('bCont').classList.remove('hide');
  $('bNew').onclick = () => UI.start(false); $('bCont').onclick = () => UI.start(true);
  addEventListener('keydown', e => { if (!G.started || /INPUT/.test(e.target.tagName)) return; if (e.key === ' ') { e.preventDefault(); G.speed = G.speed ? 0 : 1; UI.speedBtn(); } if (e.key === 'Escape') { if (G.prop) cancelProp(); else UI.closeSheet(); } });
  addEventListener('pagehide', () => { if (G.started) { saveGame(); saveScore(); } });
  readFriend(); requestAnimationFrame(frame);
};
UI.start = function (cont) {
  $('load').classList.remove('hide');
  setTimeout(async () => {
    try {
      await W.atlasP; let ok = false; if (cont) ok = loadGame(); if (!ok) newGame(($('cname').value || 'นวรัฐ').trim().slice(0, 18) || 'นวรัฐ');
      W.onTap = UI.tap; $('title').classList.add('hide'); for (const q of ['top', 'dock', 'goal']) $(q).classList.remove('hide'); G.started = true; UI.speedBtn(); UI.hud(); if (!ok) UI.showIntro();
      if (G.friend) news('เพิ่ม ' + G.friend + ' เข้าตารางอันดับแล้ว แข่งกันเลย', 'good');
    } finally { $('load').classList.add('hide'); }
  }, 40);
};
UI.speedBtn = () => { for (const b of $('speed').children) b.classList.toggle('on', +b.dataset.sp === G.speed); };

UI.hud = function () {
  const S = G.S, x = S.x, st = STAGES[x.stage || 0], nx = STAGES[(x.stage || 0) + 1]; $('bName').textContent = S.name; $('bStage').textContent = st.n; $('date').innerHTML = '<b>' + dateOf(S.m) + '</b>ครองอำนาจ ' + Math.floor(S.m / 12) + ' ปี';
  const stat = (ic, v, l, w, cl = '') => '<div class="st ' + (w ? 'warn ' : '') + cl + '">' + ic + '<div><b>' + v + '</b><small>' + l + '</small></div></div>';
  $('stats').innerHTML = stat(IC.pop, fmt(x.pop), 'ประชากร', 0) + stat(IC.money, fmt(S.treas), 'เงินคลัง', S.treas < Math.max(120, S.gdp * .25)) + stat(IC.idx, Math.round(x.idx), 'ดัชนีเจริญ', 0) + stat(IC.happy, Math.round(x.happy), 'ความสุข', x.happy < 40) + stat(IC.trust, Math.round(100 - (S.unrest || 0)), 'บัลลังก์', (S.unrest || 0) > 60, 'opt2');
  if (nx) { const p = clamp(x.pop / nx.p), q = clamp(x.idx / nx.i); $('goal').innerHTML = '<small>เป้าหมายถัดไป: ' + nx.n + '</small>คน ' + fmt(x.pop) + '/' + fmt(nx.p) + ' · ดัชนี ' + Math.round(x.idx) + '/' + nx.i + '<i><u style="width:' + Math.round(Math.min(p, q) * 100) + '%"></u></i>'; } else $('goal').innerHTML = '<small>ถึงจุดสูงสุด</small>ประเทศของคุณเป็นมหาอำนาจแล้ว';
};

/* ---------- folder tabs ---------- */
UI.openTab = function (k) {
  if (UI.tab === k) { UI.closeSheet(); return; } if (G.prop) cancelProp(); G.sel = null; W.ring.visible = false; UI.tab = k; if (k === 'future') UI.fRes = null;
  $('sheet').classList.remove('hide'); document.body.classList.add('sheet-open'); $('sTitle').textContent = TITLES[k] || ''; for (const b of $('dock').children) b.classList.toggle('on', b.dataset.tab === k); $('sbody').scrollTop = 0; UI.render();
};
UI.closeSheet = function () { UI.tab = null; G.sel = null; if (!G.prop) W.ring.visible = false; $('sheet').classList.add('hide'); document.body.classList.remove('sheet-open'); for (const b of $('dock').children) b.classList.remove('on'); };
UI.render = function () { const k = UI.tab; if (!k) return; const body = $('sbody'), top = body.scrollTop; body.innerHTML = UI['tab_' + k](); body.scrollTop = top; };
UI.refresh = function () { if (!UI.tab) return; if (UI.tab === 'budget') { const d = $('bSum'); if (d) d.innerHTML = UI.budgetSum(); } else if (UI.tab !== 'future') UI.render(); };
UI.sheetClick = function (e) {
  const q = e.target.closest('[data-a]'); if (!q) return; const a = q.dataset.a, v = q.dataset.v;
  if (['gtab', 'mhire', 'mfire', 'lawlv'].includes(a)) { UI.govClick(a, v); return; }
  if (['ctab', 'wtab', 'pact', 'wact', 'newcity'].includes(a)) { UI.geoClick(a, v); return; }
  if (a === 'cat') { UI.cat = v; UI.render(); } else if (a === 'order') { UI.closeSheet(); proposeBuild(v); }
  else if (a === 'yrs') { UI.fYears = +v; UI.fRes = null; UI.render(); } else if (a === 'if') { UI.fIf = v; UI.fRes = null; UI.render(); } else if (a === 'run') { UI.fRes = forecast(G.S, UI.fYears, UI.fIf); UI.render(); }
  else if (a === 'borrow') { const n = Math.max(500, Math.round(G.S.gdp * 3)); G.S.debt += n; G.S.treas += n; news('กู้เงิน ' + fmt(n) + ' บาท'); UI.hud(); UI.render(); }
  else if (a === 'repay') { const n = Math.min(G.S.debt, G.S.treas, Math.max(500, Math.round(G.S.gdp * 3))); G.S.debt -= n; G.S.treas -= n; UI.hud(); UI.render(); }
  else if (a === 'share') { const l = shareLink(); const done = () => { q.textContent = 'คัดลอกลิงก์แล้ว ส่งให้เพื่อนได้เลย'; }; if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(l).then(done, () => prompt('คัดลอกลิงก์นี้', l)); else prompt('คัดลอกลิงก์นี้', l); }
  else if (a === 'urgent') { const b = G.byId.get(+v); if (b) { b.urgent = !b.urgent; UI.render(); } }
};
UI.sheetInput = function (e) {
  const r = e.target; if (r.type !== 'range') return; const S = G.S, k = r.dataset.k, v = +r.value;
  if (r.dataset.g === 'tax') { S.tax[k] = v; r.parentElement.querySelector('b').textContent = v + '%'; } else if (r.dataset.g === 'road') { S.roadPct = v; r.parentElement.querySelector('b').textContent = v + '%'; } else { S.bud[k] = v / 100; r.parentElement.querySelector('b').textContent = v + '%'; }
  const d = $('bSum'); if (d) d.innerHTML = UI.budgetSum();
};
UI.tab_build = function () {
  const st = G.S.x.stage || 0, cats = ['all', 'land', 'water', 'power', 'edu', 'health', 'safe', 'clean', 'life', 'state']; let h = '<div class="chips">' + cats.map(c => '<button class="chip ' + (UI.cat === c ? 'on' : '') + '" data-a="cat" data-v="' + c + '">' + (c === 'all' ? 'ทั้งหมด' : CAT_N[c]) + '</button>').join('') + '</div>';
  const L = PUBLIC_ORDER.filter(t => UI.cat === 'all' || BT[t].cat === UI.cat);
  h += L.map(t => { const d = BT[t], ok = d.st <= st, can = G.S.treas >= d.c; return '<button class="card ' + (ok ? '' : 'lock') + '" ' + (ok ? 'data-a="order" data-v="' + t + '"' : 'disabled') + '><span class="ic">' + IC[d.cat] + '</span><span class="tx"><b>' + d.n + '</b><small>' + (ok ? d.d : 'ปลดล็อกเมื่อเป็น' + STAGES[d.st].n) + '</small></span><span class="pr ' + (can ? '' : 'no') + '">' + fmt(d.c) + '<small>บาท</small></span></button>'; }).join('');
  return h + '<p class="muted">คุณสั่งว่าจะสร้างอะไร ชาวเมืองจะเลือกที่เหมาะเอง บ้าน ร้านค้า และโรงงานเอกชนจะเกิดเองเมื่อมีคนและเงินลงทุน</p>';
};
UI.budgetSum = function () {
  const S = G.S, x = S.x, gdp = S.gdp, t = S.tax, rev = gdp * (.62 * t.inc + .38 * t.corp + .7 * t.vat) / 100 * (1 - S.corr * .55) * (.72 + .28 * S.trust / 100); let sp = 0; for (const q in BUDGET_N) sp += gdp * S.bud[q] * BUDGET_N[q][1] / 100;
  const road = rev * S.roadPct / 100, intr = S.debt * (.0035 + .012 * Math.max(0, (x.debtRatio || 0) - .6)), net = rev - sp - road - intr, load = t.inc + t.corp * .35 + t.vat * 1.1;
  return '<div class="kv"><span>รายรับต่อเดือน</span><b class="g">+' + fmt(rev) + '</b></div><div class="kv"><span>งบกระทรวง</span><b class="r">-' + fmt(sp) + '</b></div><div class="kv"><span>งบจ้างสร้างถนน</span><b class="r">-' + fmt(road) + '</b></div><div class="kv"><span>ดอกเบี้ย</span><b class="r">-' + fmt(intr) + '</b></div><div class="kv"><span>เหลือต่อเดือน</span><b class="' + (net >= 0 ? 'g' : 'r') + '">' + (net >= 0 ? '+' : '') + fmt(net) + '</b></div><div class="kv"><span>เงินคลัง / หนี้</span><b>' + fmt(S.treas) + ' / ' + fmt(S.debt) + '</b></div>' + (load > 30 ? '<p class="muted" style="color:var(--red)">ภาษีสูงมาก ธุรกิจและประชาชนอาจไม่พอใจ</p>' : '');
};
UI.tab_budget = function () {
  const S = G.S, sl = (l, g, k, v, mx, st = 1) => '<label class="sl"><span>' + l + '</span><input type="range" min="0" max="' + mx + '" step="' + st + '" value="' + v + '" data-g="' + g + '" data-k="' + k + '" aria-label="' + l + '"><b>' + v + '%</b></label>';
  let h = '<div id="bSum">' + UI.budgetSum() + '</div><h3>ภาษี</h3>' + sl('ภาษีเงินได้', 'tax', 'inc', Math.round(S.tax.inc), 45) + sl('ภาษีธุรกิจ', 'tax', 'corp', Math.round(S.tax.corp), 45) + sl('ภาษีการขาย', 'tax', 'vat', Math.round(S.tax.vat), 25);
  h += '<h3>ถนน: รัฐจ่ายเงินจ้างคนสร้าง</h3>' + sl('งบสร้างถนน', 'road', 'roadPct', Math.round(S.roadPct), 60) + '<p class="muted">แบ่งจากรายรับ ทีมงานเสื้อส้มจะไปสร้างถนนตรงที่คนเดินผ่านมากที่สุด กำลังจ้าง ' + (G.crewN || 0) + ' คน สร้างแล้ว ' + fmt(W.roadCount) + ' ช่อง</p>';
  h += '<h3>งบกระทรวง (100% = ระดับมาตรฐาน)</h3>' + Object.keys(BUDGET_N).map(k => sl(BUDGET_N[k][0], 'bud', k, Math.round(S.bud[k] * 100), 200, 5)).join('');
  return h + '<h3>เงินกู้</h3><div style="display:flex;gap:6px"><button class="btn ghost" style="flex:1" data-a="borrow">กู้เพิ่ม</button><button class="btn ghost" style="flex:1" data-a="repay">ใช้หนี้</button></div>';
};
UI.tab_country = function () {
  const S = G.S, x = S.x, q = S.month || {}, color = v => v > .66 ? '#27825c' : v > .38 ? '#d29a2e' : '#b8392c', bar = (l, v, t) => '<div class="bar"><span>' + l + '</span><i><u style="width:' + Math.round(clamp(v) * 100) + '%;background:' + color(clamp(v)) + '"></u></i><b>' + t + '</b></div>';
  const lad = STAGES.map((s, i) => '<i class="' + (i < x.stage ? 'd' : i === x.stage ? 'c' : '') + '"></i>').join(''), net = (q.born || 0) + (q.inM || 0) - (q.died || 0) - (q.outM || 0);
  let h = '<div style="display:flex;justify-content:space-between;align-items:flex-end"><div><span class="muted">ดัชนีความเจริญ (เต็ม 1,000)</span><div class="big">' + Math.round(x.idx) + '</div></div><div style="text-align:right"><span class="muted">คะแนน</span><div style="font-size:24px;font-weight:800">' + fmt(x.score) + '</div></div></div><div class="ladder">' + lad + '</div><p class="muted">ระดับ: ' + STAGES[x.stage].n + '</p>';
  h += '<h3>ความเป็นอยู่</h3>' + bar('มีงานทำ', 1 - x.u, pct(1 - x.u)) + bar('รายได้ต่อคน', Math.log((x.gdpPc + 20) / 60) / Math.log(60), fmt(x.gdpPc)) + bar('อาหาร', x.foodMonths / 2, x.foodMonths.toFixed(1) + ' ด.') + bar('น้ำสะอาด', x.cleanW, pct(x.cleanW)) + bar('ไฟฟ้า', x.pw, pct(x.pw)) + bar('ที่อยู่อาศัย', x.houseRatio, pct(Math.min(x.houseRatio, 9.99)));
  h += '<h3>คุณภาพคน</h3>' + bar('การศึกษา', x.eduY / 14, x.eduY.toFixed(1) + ' ปี') + bar('เด็กได้เรียน', x.schoolCov, pct(x.schoolCov)) + bar('เข้าถึงหมอ', x.hospCov, pct(x.hospCov)) + bar('อายุขัย', (x.LE - 40) / 45, Math.round(x.LE) + ' ปี') + bar('คนไม่ป่วย', 1 - x.sick * 4, pct(1 - x.sick));
  h += '<h3>สังคมและโลก</h3>' + bar('บัลลังก์มั่นคง', 1 - (x.unrest || 0) / 100, Math.round(100 - (x.unrest || 0)) + '%') + bar('แรงสนับสนุน', x.trust / 100, Math.round(x.trust) + '%') + bar('ปลอดภัย', 1 - x.crime * 2.4, pct(1 - x.crime)) + bar('ไม่โกงกิน', 1 - x.corr * 2.5, pct(1 - x.corr)) + bar('เท่าเทียม', 1 - (x.gini - .2) / .45, 'จีนี ' + x.gini.toFixed(2)) + bar('อากาศดี', 1 - x.P * 2, pct(1 - x.P)) + bar('ป่าไม้', x.forest, pct(x.forest)) + bar('ถนนไม่ติด', 1 - x.cong, pct(1 - x.cong)) + bar('ชื่อเสียงโลก', x.rep, pct(x.rep)) + bar('สันติภาพ', 1 - x.tension * 1.6, pct(1 - x.tension));
  h += '<h3>ประชากรเดือนนี้</h3><div class="kv"><span>เกิด / ย้ายเข้า</span><b class="g">+' + (q.born || 0).toFixed(1) + ' / +' + (q.inM || 0).toFixed(1) + '</b></div><div class="kv"><span>ตาย / ย้ายออก</span><b class="r">-' + (q.died || 0).toFixed(1) + ' / -' + (q.outM || 0).toFixed(1) + '</b></div><div class="kv"><span>เลือกไม่มีลูกเพราะเศรษฐกิจ</span><b>' + (q.noKid || 0).toFixed(2) + '</b></div><div class="kv"><span>สุทธิ</span><b class="' + (net >= 0 ? 'g' : 'r') + '">' + (net >= 0 ? '+' : '') + net.toFixed(1) + '</b></div><div class="kv"><span>เด็ก / วัยทำงาน / สูงวัย</span><b>' + fmt(x.kids) + ' / ' + fmt(x.work) + ' / ' + fmt(x.old) + '</b></div><div class="kv"><span>ลูกเฉลี่ยต่อผู้หญิง</span><b>' + x.tfr.toFixed(2) + '</b></div>';
  return h;
};
function sparkSvg(a, col) { if (a.length < 2) return ''; const lo = Math.min(...a), hi = Math.max(...a), r = hi - lo || 1, P = a.map((v, i) => (i / (a.length - 1) * 100).toFixed(1) + ',' + (31 - (v - lo) / r * 28).toFixed(1)).join(' '); return '<svg viewBox="0 0 100 34" preserveAspectRatio="none"><polyline points="' + P + '" fill="none" stroke="' + col + '" stroke-width="2.200" vector-effect="non-scaling-stroke"/></svg>'; }
UI.tab_future = function () {
  let h = '<p class="muted">จำลองจากสภาพประเทศตอนนี้ ไม่นับเหตุไม่คาดฝัน ผลเป็นการคาดการณ์ ไม่ใช่เรื่องที่ต้องเกิดแน่นอน</p><h3>ถ้า...</h3><div class="chips">' + Object.keys(WHATIF).map(k => '<button class="chip ' + (UI.fIf === k ? 'on' : '') + '" data-a="if" data-v="' + k + '">' + WHATIF[k][0] + '</button>').join('') + '</div><h3>ดูไปข้างหน้า</h3><div class="chips">' + [5, 10, 25, 50].map(y => '<button class="chip ' + (UI.fYears === y ? 'on' : '') + '" data-a="yrs" data-v="' + y + '">' + y + ' ปี</button>').join('') + '</div><button class="btn gold" style="width:100%" data-a="run">จำลองอนาคต</button>';
  const R = UI.fRes; if (R) {
    const p = R.pts, l = p[p.length - 1], c = (t, k, f, col) => '<div><small>' + t + '</small><b>' + f(l[k]) + '</b>' + sparkSvg(p.map(q => q[k]), col) + '</div>';
    h += '<h3>อีก ' + UI.fYears + ' ปี: ' + WHATIF[UI.fIf][0] + '</h3><div class="spark">' + c('ประชากร', 'pop', fmt, '#1f7a78') + c('ดัชนีเจริญ', 'idx', v => Math.round(v), '#b8862a') + c('ความสุข', 'happy', v => Math.round(v), '#27825c') + c('รายได้ต่อคน', 'gdpPc', fmt, '#2d4a69') + c('มลพิษ', 'P', pct, '#b8392c') + c('หนี้ต่อ GDP', 'debt', pct, '#7a4f9a') + '</div><h3>ปัญหาที่อาจเกิด</h3>';
    h += R.warn.length ? R.warn.slice(0, 9).map(w => '<div class="warn-row"><b>' + (w.y < 1 ? 'ภายในปีนี้' : 'อีก ' + Math.round(w.y) + ' ปี') + '</b><span>' + w.t + '</span></div>').join('') : '<div class="ok-row">ช่วงนี้ยังไม่เห็นปัญหาใหญ่</div>';
  }
  return h;
};
UI.tab_rank = function () {
  const L = ranking(), x = G.S.x, me = L.findIndex(q => q.me) + 1;
  return '<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:6px"><div><span class="muted">คะแนนของคุณ</span><div class="big">' + fmt(x.score) + '</div></div><div style="text-align:right"><span class="muted">อันดับโลก</span><div style="font-size:26px;font-weight:800">' + me + ' / ' + L.length + '</div></div></div>' + L.slice(0, 16).map((q, i) => '<div class="rank ' + (q.me ? 'me' : '') + '"><span>' + (i + 1) + '</span><span>' + esc(q.n) + '</span><b>' + fmt(q.score) + '</b></div>').join('') + '<p class="muted" style="margin-top:7px">คะแนนคิดจากดัชนีความเจริญ จำนวนประชากร และระดับประเทศ ประเทศอื่นในตารางเป็นประเทศสมมติ</p><button class="btn gold" style="width:100%;margin-top:4px" data-a="share">ส่งคะแนนท้าเพื่อน</button>';
};

/* ---------- tap a person or building ---------- */
UI.tap = function (sx, sy) {
  if (G.modal || G.prop) return; let best = null, bd = 26;
  for (const a of W.agents) { if (a.indoor) continue; const p = W.project(a.x, W.h(a.x, a.z) + .3, a.z), d = Math.hypot(p[0] - sx, p[1] - sy); if (p[2] < 1 && d < bd) { bd = d; best = a; } }
  if (best) { UI.openInfo({ a: best }); return; } const g = W.groundAt(sx, sy); if (!g) return; const id = W.occ[ci(clamp(g[0] | 0, 0, N - 1), clamp(g[1] | 0, 0, N - 1))]; if (id && G.byId.has(id)) UI.openInfo({ b: G.byId.get(id) }); else if (UI.tab === 'info') UI.closeSheet();
};
UI.openInfo = function (sel) {
  G.sel = sel; UI.tab = 'info'; for (const b of $('dock').children) b.classList.remove('on'); $('sheet').classList.remove('hide'); document.body.classList.add('sheet-open'); W.ring.visible = true;
  if (sel.b) { const b = sel.b; W.ring.scale.setScalar(Math.max(b.w, b.d) * .85); W.ring.position.set(b.x + b.w / 2, W.h(b.x + b.w / 2, b.z + b.d / 2) + .18, b.z + b.d / 2); } else W.ring.scale.setScalar(.42); UI.render();
};
const EDU_N = v => v < 1.5 ? 'ยังไม่ได้เรียน' : v < 5 ? 'ประถม' : v < 9 ? 'มัธยมต้น' : v < 12 ? 'มัธยมปลาย / อาชีวะ' : 'ปริญญา';
UI.thought = function (a) {
  const x = G.S.x; if (a.kid) return a.age < 6 ? 'อยากวิ่งเล่นกับเพื่อน' : x.schoolCov > .5 ? 'วันนี้ได้ไปโรงเรียน' : 'อยากมีโรงเรียนใกล้บ้าน'; if (a.crew) return 'รัฐจ้างมาสร้างถนน มีรายได้เดือนนี้แล้ว'; if (a.site) return 'กำลังช่วยก่อสร้าง'; if (!a.job && a.age < 66) return x.u > .1 ? 'ไม่มีงาน ไม่มีรายได้ ยังไม่กล้ามีลูก อาจต้องย้ายออก' : 'กำลังหางานทำ';
  if (x.hunger > .03) return 'อาหารไม่พอ ลูกหิวทุกวัน'; if (x.cleanW < .6) return 'น้ำไม่สะอาด กลัวลูกป่วย'; if (x.hospCov < .4) return 'ถ้าป่วยจะไปหาหมอที่ไหน'; if (x.houseRatio < .9) return 'บ้านแออัดเกินไป'; if (x.crime > .2) return 'ช่วงนี้ไม่ค่อยปลอดภัย'; if (x.infl > .012) return 'ของแพงขึ้นทุกเดือน'; if (x.P > .3) return 'อากาศแย่จนหายใจไม่สะดวก'; if (x.taxLoad > 32) return 'ภาษีแพงเกินไป'; return x.happy > 70 ? 'ชีวิตช่วงนี้ดีขึ้นเรื่อยๆ' : 'ก็พอไปได้ หวังว่าปีหน้าจะดีกว่านี้';
};
UI.tab_info = function () {
  const s = G.sel; if (!s) return ''; const kv = (k, v) => '<div class="kv"><span>' + k + '</span><b>' + v + '</b></div>';
  if (s.a) { const a = s.a, j = G.byId.get(a.job), hm = G.byId.get(a.home); $('sTitle').textContent = a.name; const eduV = clamp(G.S.eduY * (a.age < 15 ? a.age / 15 : 1) + (a.id % 5 - 2) * .7, 0, 16); return '<div class="ok-row" style="margin-bottom:7px">“' + UI.thought(a) + '”</div>' + kv('อายุ', Math.floor(a.age) + ' ปี') + kv('อาชีพ', a.kid ? 'เด็ก' : a.crew ? 'คนงานสร้างถนน' : a.age >= 66 ? 'เกษียณ' : j ? (JOB_N[j.t] || 'พนักงาน') : 'ว่างงาน') + kv('การศึกษา', EDU_N(eduV)) + kv('ที่อยู่', hm ? BT[hm.t].n : 'ไม่มีบ้าน'); }
  const b = s.b, d = BT[b.t]; $('sTitle').textContent = d ? d.n : 'ที่ทำการรัฐบาล'; if (!d) return '<p>' + esc(G.cities[b.city].name) + '</p><p class="muted">ศูนย์กลางของเมือง คลังวัสดุอยู่ที่นี่</p>';
  let h = d.d ? '<p class="muted">' + d.d + '</p>' : ''; const gv = d.g; if (gv.house) h += kv('อยู่ได้', gv.house + ' คน'); const jobs = (gv.ag || 0) + (gv.ind || 0) + (gv.svc || 0) + (gv.pub || 0) + (gv.tech || 0); if (jobs) h += kv('ตำแหน่งงาน', fmt(jobs));
  if (!b.done && b.f) { const f = b.f, q = (l, v) => '<div class="bar"><span>' + l + '</span><i><u style="width:' + Math.round(clamp(v / 1.2) * 100) + '%;background:' + (v >= .9 ? '#27825c' : v >= .7 ? '#d29a2e' : '#b8392c') + '"></u></i><b>×' + v.toFixed(2) + '</b></div>'; h += '<h3>กำลังสร้าง ' + Math.round(b.prog * 100) + '%</h3>' + kv('คนงาน', f.w.toFixed(1) + ' คน') + kv('แหล่งเงิน', FUNDS[b.fund] ? FUNDS[b.fund][0] : 'เอกชน') + kv('จะเสร็จในอีก', f.sp > 0 ? Math.ceil((1 - b.prog) * d.wk / f.sp) + ' เดือน' : 'หยุดรอ') + '<h3>อะไรทำให้เร็วหรือช้า</h3>' + q('ฝีมือคนงาน', f.skill) + q('ขวัญกำลังใจ', f.mood) + q(f.rainy ? 'อากาศ (ฤดูฝน)' : 'อากาศ', f.weather) + q('การขนส่ง', f.road) + q('คนแน่นไซต์', f.crowd) + q('วัสดุ', f.mat) + '<button class="btn ' + (b.urgent ? 'gold' : 'ghost') + '" style="width:100%;margin-top:7px" data-a="urgent" data-v="' + b.id + '">' + (b.urgent ? 'เป็นงานด่วนอยู่' : 'สั่งเป็นงานด่วน') + '</button>'; }
  return h;
};

/* ---------- letters on the mayor's desk ---------- */
const FX_X = { tax: ['ภาษี', 0], bud: ['งบรัฐ', 0], road: ['ถนน', 0], cong: ['รถติด', 1], tfr: ['อัตราเกิด', 0] };
function fxChips(fx) {
  const o = []; for (const k in fx) {
    const v = fx[k]; if (k === 'build') { o.push('<span class="n">สั่งสร้าง</span>'); continue; } if (k === 'later' || k === 'next') { o.push('<span class="n">มีผลตามมาทีหลัง</span>'); continue; } if (k === 'fire') { o.push('<span class="n">ปลดรัฐมนตรี</span>'); continue; } if (k === 'loy') { o.push('<span class="g">รัฐมนตรีภักดีขึ้น</span>'); continue; }
    if (k === 'c') { const n = Math.abs(v) * Math.max(G.S.gdp, 700); o.push(v > 0 ? '<span class="r">ใช้เงิน ' + fmt(n) + '</span>' : '<span class="g">ได้เงิน ' + fmt(n) + '</span>'); continue; }
    const name = FX_N[k] || (FX_X[k] && FX_X[k][0]); if (!name) continue; const bad = FX_BAD[k] || (FX_X[k] && FX_X[k][1]), good = bad ? v < 0 : v > 0; o.push('<span class="' + (good ? 'g' : 'r') + '">' + name + (v > 0 ? ' ▲' : ' ▼') + '</span>');
  } return '<div class="fx">' + o.join('') + '</div>';
}
function openModal(html, top) { G.modal = true; $('modal').innerHTML = html; $('modal').style.borderTopColor = top || 'var(--red)'; $('modal').scrollTop = 0; $('modalW').classList.remove('hide'); }
function closeModal() { G.modal = false; $('modalW').classList.add('hide'); }
UI.showEvent = function (e) {
  openModal('<span class="cat">' + e.cat + '</span><span class="dt">' + dateOf(G.S.m) + '</span><h1>' + e.t + '</h1><div class="bd">' + e.b + '</div>' + e.o.map((o, i) => '<button class="opt" data-o="' + i + '"><b>' + o[0] + '</b>' + fxChips(o[1]) + '</button>').join(''));
  $('modal').onclick = v => { const q = v.target.closest('[data-o]'); if (!q) return; $('modal').onclick = null; closeModal(); answerEvent(e, e.o[+q.dataset.o]); news('ตัดสินใจ: ' + e.o[+q.dataset.o][0]); UI.hud(); };
};
UI.showIntro = function () {
  openModal('<span class="cat">ประกาศสถาปนา</span><h1>คุณคือเจ้าของประเทศ' + esc(G.S.name) + '</h1><div class="bd">แผ่นดินใหม่นี้มีคนเพียง 10 คน ทุกอย่างอยู่ในมือคุณ และไม่มีการเลือกตั้ง<br>• <b>คุณสั่ง</b> ว่าจะสร้างอะไรและใช้เงินอย่างไร<br>• <b>ชาวเมือง</b> จะเลือกที่และลงมือสร้างเอง ถนนต้องใช้งบรัฐจ้างคนสร้าง<br>• <b>ปัญหาเกิดจากเหตุจริง</b> ฝน ป่า และสิ่งที่คุณสร้าง ดูความเสี่ยงได้ที่เมนูเฝ้าระวัง<br>• <b>บัลลังก์</b> ถ้าคนโกรธหรือทหารไม่พอใจ คุณอาจถูกโค่นล้ม</div><button class="btn gold" style="width:100%" id="mGo">เริ่มปกครองประเทศ</button>', 'var(--gold)');
  $('mGo').onclick = () => closeModal();
};
UI.showStage = function (s) { openModal('<span class="cat">ก้าวใหม่ของชาติ</span><h1>' + esc(G.S.name) + ' เป็น' + STAGES[s].n + ' แล้ว!</h1><div class="bd">ปลดล็อก: ' + (PUBLIC_ORDER.filter(t => BT[t].st === s).map(t => BT[t].n).join(' · ') || 'ความท้าทายใหม่') + '</div><button class="btn gold" style="width:100%" id="mGo">ไปต่อ</button>', 'var(--gold)'); $('mGo').onclick = () => closeModal(); };
UI.showEnd = function (t, b) {
  G.over = true; saveScore(); try { localStorage.removeItem(SAVE_KEY); } catch (e) {} const S = G.S, x = S.x, L = ranking(), me = L.findIndex(q => q.me) + 1;
  openModal('<span class="cat">สรุปผลงาน</span><h1>' + t + '</h1><div class="bd">' + b + '</div><div class="kv"><span>คะแนนสูงสุด</span><b>' + fmt(Math.max(S.best, x.score)) + '</b></div><div class="kv"><span>ระดับสูงสุด</span><b>' + STAGES[S.stageMax].n + '</b></div><div class="kv"><span>ประชากร</span><b>' + fmt(x.pop) + '</b></div><div class="kv"><span>ครองอำนาจ</span><b>' + Math.floor(S.m / 12) + ' ปี</b></div><div class="kv"><span>อันดับโลก</span><b>' + me + ' / ' + L.length + '</b></div><div style="display:flex;gap:6px;margin-top:9px"><button class="btn ghost" style="flex:1" id="mShare">ส่งคะแนนท้าเพื่อน</button><button class="btn gold" style="flex:1" id="mGo">ก่อตั้งประเทศใหม่</button></div>', 'var(--ink)');
  $('mShare').onclick = () => { const l = shareLink(); if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(l).then(() => { $('mShare').textContent = 'คัดลอกแล้ว'; }, () => prompt('คัดลอกลิงก์นี้', l)); else prompt('คัดลอกลิงก์นี้', l); };
  $('mGo').onclick = () => location.replace(location.pathname);
};
UI.showProposal = function (P) {
  if (UI.tab) { const keep = G.prop; UI.closeSheet(); G.prop = keep; W.ring.visible = true; } const d = BT[P.t], ways = moneyWays(d.c).filter(q => !FUNDS[q.f]), F = Object.keys(FUNDS); $('prop').classList.remove('hide');
  $('prop').innerHTML = '<button class="x" id="pX">ยกเลิก</button><h4>' + d.n + '</h4> <span class="muted">' + fmt(d.c) + ' บาท · วัสดุ ' + fmt(d.m) + '</span><div class="why">ชาวเมืองเลือกจุดนี้: ' + P.why.join(' · ') + '</div><div class="funds">' + F.map(f => '<button class="fund" data-f="' + f + '" ' + (fundOK(P.t, f) ? '' : 'disabled') + '><b>' + FUNDS[f][0] + '</b><small>' + FUNDS[f][1] + '</small></button>').join('') + ways.map(q => '<button class="fund" data-f="' + q.f + '" ' + (q.ok ? '' : 'disabled') + '><b>' + q.n + '</b><small>' + q.d + '</small></button>').join('') + '</div>';
  $('pX').onclick = () => cancelProp(); $('prop').querySelector('.funds').onclick = e => { const q = e.target.closest('[data-f]'); if (q && !q.disabled) { approve(q.dataset.f); UI.hud(); } };
};
UI.closeProposal = () => $('prop').classList.add('hide');

/* ---------- main loop ---------- */
let lastT = performance.now(), hudT = 0;
function frame(n) {
  requestAnimationFrame(frame); const dt = Math.min(.1, Math.max(0, (n - lastT) / 1000)); lastT = n; if (!G.started) return; G.time += dt; tick(dt);
  W.setDay(G.dayF, G.S.P); W.drawAgents(G.time); if (G.sel && G.sel.a) W.ring.position.set(G.sel.a.x, W.h(G.sel.a.x, G.sel.a.z) + .12, G.sel.a.z);
  if (G.floodT > 0) G.floodT -= dt * Math.max(G.speed, 1); W.water.position.y += ((G.floodT > 0 ? .3 : 0) - W.water.position.y) * Math.min(1, dt * 1.2);
  W.render(G.time, dt); hudT += dt; if (UI.dirty && hudT > .25) { hudT = 0; UI.dirty = false; UI.hud(); UI.refresh(); }
}
