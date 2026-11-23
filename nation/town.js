'use strict';
/* ก่อร่างสร้างชาติ: town planning for the painted look. Streets in blocks, a real centre, homes around it, farms and industry at the edge. */
if (typeof ISO_ON !== 'undefined' && ISO_ON) (function () {
  const SQUARE = { hut: 2, house: 2, row: 3, apt: 3, tower: 3, mega: 4, farm: 4, bigfarm: 6, lumber: 3, shop: 2, workshop: 3, market: 3, office: 3, factory: 4, cbd: 3, plant: 6, techpark: 5, well: 1, waterworks: 3, dam: 5, gen: 2, coal: 4, solar: 5, nuclear: 6, school: 4, hischool: 5, univ: 5, clinic: 3, hospital: 4, medcenter: 5, police: 2, policehq: 3, base: 5, trash: 2, recycle: 4, park: 3, port: 4, airport: 6, parliament: 5 };
  for (const t in SQUARE) if (BT[t]) BT[t].s = [SQUARE[t], SQUARE[t]];
  /* where each kind of building belongs, as a share of the town radius */
  const ZONE = { shop: [.34, 3], market: [.2, 3], office: [.22, 2], cbd: [.12, 2], mega: [.1, 2], tower: [.3, 2], row: [.46, 2.4], apt: [.62, 1.7], school: [.5, 1.2], hischool: [.62, 1.2], univ: [.8, 1], clinic: [.42, 1.3], hospital: [.5, 1.3], medcenter: [.55, 1.2], police: [.36, 1.3], policehq: [.4, 1.2], parliament: [.2, 2], park: [.55, 1], well: [.3, 1], house: [.88, 1.5], hut: [1.02, 1.5], farm: [1.5, 1.1], bigfarm: [1.7, 1], lumber: [1.34, 1], workshop: [1.22, 1.2], factory: [1.45, 1.1], plant: [1.7, 1], techpark: [1.1, 1], gen: [1.15, 1], coal: [1.65, 1], solar: [1.7, 1], nuclear: [1.9, 1], waterworks: [1.2, 1], dam: [1.8, 1], trash: [1.3, 1], recycle: [1.5, 1], base: [1.6, 1], port: [1.2, 1], airport: [1.9, 1] };
  const EDGE = { farm: 1, bigfarm: 1, lumber: 1 }, WORK = { workshop: 1, factory: 1, plant: 1, coal: 1, recycle: 1, trash: 1, gen: 1, solar: 1, nuclear: 1, waterworks: 1, base: 1 };
  const SP = 7, canPlace0 = W.canPlace, findSpot0 = W.findSpot, init3 = W.init;
  W.init = function (cv, seed) { W.plan = new Uint8Array(N * N); init3(cv, seed); };
  W.canPlace = function (x, z, w, d, soft) { if (W.plan && inMap(x, z) && inMap(x + w - 1, z + d - 1)) for (let a = x; a < x + w; a++) for (let b = z; b < z + d; b++) if (W.plan[ci(a, b)]) return false; return canPlace0(x, z, w, d, soft); };
  const townR = c => { const i = G.cities.indexOf(c); let n = 0; for (const b of G.blds) if (b.city === i && !EDGE[b.t]) n++; return 4.5 + Math.sqrt(n + 1) * 1.45; };
  /* streets are laid out first; the government still pays crews to build each piece */
  function planCity(c) {
    const cx = Math.round(c.x), cz = Math.round(c.z), R = Math.min(52, Math.ceil(townR(c) * 1.9) + 10); if ((c.planR || 0) >= R) return; c.planR = R;
    for (let dz = -R; dz <= R; dz++) for (let dx = -R; dx <= R; dx++) { const x = cx + dx, z = cz + dz; if (!inMap(x, z)) continue; const on = ((dx - 3) % SP + SP) % SP === 0 || ((dz - 3) % SP + SP) % SP === 0; if (!on) continue; const q = ci(x, z), t = W.T[q]; if (t < 1 || t === 6 || W.occ[q]) continue; if (t === 1 && !(((dx - 3) === 0) || ((dz - 3) === 0))) continue; W.plan[q] = 1; if (Math.hypot(dx, dz) < townR(c) * 1.5) W.clearTrees(x, z, 1, 1); }
  }
  W.planCity = planCity;
  /* the side of town with the most open land becomes the working district */
  function workSide(c) { if (c.workA != null) return c.workA; let best = 0, bs = -1; for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283; let s = 0; for (let r = 8; r <= 26; r += 3) { const x = Math.round(c.x + Math.cos(a) * r), z = Math.round(c.z + Math.sin(a) * r); if (inMap(x, z) && (W.T[ci(x, z)] === 3 || W.T[ci(x, z)] === 4)) s++; } if (s > bs) { bs = s; best = a; } } c.workA = best; return best; }

  W.findSpot = function (city, t, R0) {
    /* past this many, new farms and yards count in the numbers but do not eat the map */
    if (EDGE[t] && !W._moving) { let n = 0; for (const b of G.blds) if (t === 'lumber' ? b.t === 'lumber' : b.t === 'farm' || b.t === 'bigfarm') n++; if (n >= (t === 'lumber' ? 3 + G.cities.length * 2 : 9 + G.cities.length * 5)) return null; }
    planCity(city); const def = BT[t] || { s: [3, 3] }, w = def.s[0], d = def.s[1], Z = ZONE[t] || [.8, 1.2], Rc = townR(city), want = EDGE[t] ? Rc + 4 + w : Z[0] * Rc, cx = city.x, cz = city.z, wa = WORK[t] ? workSide(city) : 0;
    for (let round = 0; round < 4; round++) {
      const reach = Math.min(58, want + Rc * (.42 + round * .4) + w + 3), x0 = Math.max(1, Math.floor(cx - reach)), x1 = Math.min(N - w - 2, Math.ceil(cx + reach)), z0 = Math.max(1, Math.floor(cz - reach)), z1 = Math.min(N - d - 2, Math.ceil(cz + reach)); let best = null, bs = -1e9;
      for (let z = z0; z <= z1; z++) for (let x = x0; x <= x1; x++) {
        if (W.occ[ci(x, z)] || W.occ[ci(x + w - 1, z + d - 1)] || W.plan[ci(x, z)]) continue; const mx = x + w / 2, mz = z + d / 2, dist = Math.hypot(mx - cx, mz - cz); if (dist > reach || !W.canPlace(x, z, w, d, true)) continue;
        let street = 0, near = 0, sliver = 0; const edge = (p, q, p2, q2) => { if (!inMap(p, q)) return; const c = ci(p, q); if (W.plan[c] || W.road[c] >= 2) street++; else if (W.occ[c]) near++; else if (inMap(p2, q2)) { const e = ci(p2, q2); if (W.plan[e] || W.occ[e]) sliver++; } };
        for (let a = x; a < x + w; a++) { edge(a, z - 1, a, z - 2); edge(a, z + d, a, z + d + 1); } for (let b = z; b < z + d; b++) { edge(x - 1, b, x - 2, b); edge(x + w, b, x + w + 1, b); }
        const off = dist - want; let s = -(off > 0 ? off : -off * (EDGE[t] ? 1 : .32)) * (EDGE[t] ? .9 : Z[1]) + Math.min(street, w + 1) * 1.5 + near * .62 - sliver * .85 + Math.random() * .25;
        if (!street && !EDGE[t]) s -= 7; if (WORK[t]) { let da = Math.atan2(mz - cz, mx - cx) - wa; while (da > Math.PI) da -= 6.2832; while (da < -Math.PI) da += 6.2832; s -= Math.abs(da) * 2.6; } if (EDGE[t]) { let da = Math.atan2(mz - cz, mx - cx) - workSide(city); while (da > Math.PI) da -= 6.2832; while (da < -Math.PI) da += 6.2832; s -= Math.max(0, .9 - Math.abs(da)) * 3; }
        if (s > bs) { const door = W.doorFor(x, z, w, d, cx, cz); if (door) { bs = s; let rw = 0; for (let p = -2; p <= w + 1; p += 2) for (let q = -2; q <= d + 1; q += 2) if (inMap(x + p, z + q) && W.T[ci(x + p, z + q)] === 1) rw++; best = { x, z, w, d, door, rw }; } }
      }
      if (best) return best;
    }
    return EDGE[t] ? null : findSpot0(city, t, R0);
  };
  /* when the town grows over a farm, the farm moves out to the edge and the land becomes town */
  function moveOut(b, c, Rc) {
    const cells = []; for (let a = b.x; a < b.x + b.w; a++) for (let q = b.z; q < b.z + b.d; q++) { cells.push(ci(a, q)); W.occ[ci(a, q)] = 0; } const dc = ci(b.door[0], b.door[1]); W.reserved[dc] = 0;
    W._moving = true; const sp = W.findSpot(c, b.t); W._moving = false; if (!sp || Math.hypot(sp.x + sp.w / 2 - c.x, sp.z + sp.d / 2 - c.z) <= Rc + 1) { for (const q of cells) W.occ[q] = b.id; W.reserved[dc] = 1; return false; }
    W.removeInstance(b); b.x = sp.x; b.z = sp.z; b.w = sp.w; b.d = sp.d; b.rot = sp.door[2]; b.door = [sp.door[0], sp.door[1]]; W.occupy(b); W.placeInstance(b); W.layoutV = (W.layoutV || 0) + 1; return true;
  }
  W.townTick = function (S) {
    if (S.m % 2) return; G.cities.forEach((c, i) => { const Rc = townR(c); let tries = 0; for (const b of G.blds) { if (tries >= 3) break; if (b.city !== i || !b.done || !EDGE[b.t] || Math.hypot(b.x + b.w / 2 - c.x, b.z + b.d / 2 - c.z) > Rc + 1) continue; tries++; moveOut(b, c, Rc); } });
  };
  ROAD_STYLE[1] = ['#c6ad7f', .3, 0]; ROAD_STYLE[2] = ['#d2bd96', .84, '#bda67c']; ROAD_STYLE[3] = ['#8e8f92', .8, '#e6dfcf']; ROAD_STYLE[4] = ['#62646a', .8, '#e8e1d2'];
  const setRoad0 = W.setRoad; W.setRoad = function (c, t) { setRoad0(c, t); if (W.treeAt.has(c)) W.clearTrees(c % N, c / N | 0, 1, 1); };
})();
