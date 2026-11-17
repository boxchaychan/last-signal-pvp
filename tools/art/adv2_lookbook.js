// Lookbook: KayKit Adventurers 1.0 (what tribe3d uses now) above 2.0 FREE (art/incoming/kaykit/adventurers_2.0), each 2.0 hero
// with its weapons on the hand slots and a move from the Character Animations pack (Rig_Medium). Pretty render for the owner.
//   python3 -m http.server 8000 ; node tools/art/adv2_lookbook.js out.png
const {chromium} = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await (await b.newContext({viewport: {width: 900, height: 500}})).newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/tribe3d.html?autostart=1&animals=0'); await pg.waitForFunction(() => window.GAME && GAME.on && GAME.PEOPLE.ready, null, {timeout: 150000});
  const res = await pg.evaluate(async () => {
    const ld = new THREE.GLTFLoader(), R = TB.renderer, A2 = 'art/incoming/kaykit/adventurers_2.0/', AN = 'art/incoming/kaykit/character_animations/Rig_Medium/';
    const load = u => ld.loadAsync(u);
    const anims = (await Promise.all(['CombatMelee', 'CombatRanged', 'General', 'MovementBasic', 'Tools'].map(n => load(AN + 'Rig_Medium_' + n + '.glb')))).flatMap(g => g.animations);
    const lift = m => { const q = new THREE.MeshLambertMaterial({ map: m.map || null, color: m.map ? 0xffffff : m.color }); if (q.map) { q.map.encoding = THREE.LinearEncoding; q.map.magFilter = THREE.LinearFilter; } return q; };
    const find = (r, n) => { let f = null; r.traverse(o => { if (o.name === n && !f) f = o; }); return f; };
    const W2 = { Knight: [['sword_1handed', 'handslotr'], ['shield_badge_color', 'handslotl']], Barbarian: [['axe_2handed', 'handslotr']], Ranger: [['bow_withString', 'handslotl']], Rogue_Hooded: [['crossbow_1handed', 'handslotr']], Mage: [['staff', 'handslotr'], ['spellbook_open', 'handslotl']], Rogue: [['dagger', 'handslotr'], ['dagger', 'handslotl']] };
    const POSE2 = { Knight: ['Melee_Block', .5], Barbarian: ['Melee_2H_Attack_Chop', .4], Ranger: ['Ranged_Bow_Draw', .9], Rogue_Hooded: ['Ranged_1H_Aiming', .5], Mage: ['Ranged_Magic_Raise', .6], Rogue: ['Melee_Dualwield_Attack_Slice', .35] };
    const ORDER = ['Knight', 'Barbarian', 'Ranger', 'Rogue_Hooded', 'Mage', 'Rogue'];
    const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x6a5a48, .7)); const k = new THREE.DirectionalLight(0xfff0d8, 1); k.position.set(-4, 8, 10); sc.add(k); const rim = new THREE.DirectionalLight(0xbfe0ff, .7); rim.position.set(6, 5, -8); sc.add(rim);
    const miss = [];
    // row 1: our 1.0 templates as used in the game now
    const ours = [['warrior', 'นักรบ'], ['man', 'ชาวบ้านชาย'], ['hunter2', 'นักธนู ★★'], ['hunter', 'พราน'], ['shaman', 'หมอผี'], ['woman', 'ชาวบ้านหญิง']];
    ours.forEach(([key], i) => { const T = GAME.PEOPLE.tpl[key], r = THREE.SkeletonUtils.clone(T.root); r.scale.setScalar(2.4 / T.h); r.position.set(i * 3, 0, 0); r.rotation.y = -.4;
      r.traverse(o => { if (o.isSkinnedMesh) o.material = lift(T.mats[0]); }); const c = GAME.PEOPLE.clips.find(c => c.name === 'Idle'); const mx = new THREE.AnimationMixer(r); mx.clipAction(c).play(); mx.update(.4); sc.add(r); });
    // row 2: 2.0
    for (const [i, n] of ORDER.entries()) {
      const g = await load(A2 + 'characters/' + n + '.glb'); const r = g.scene; r.traverse(o => { if (o.isMesh) o.material = lift(o.material); });
      for (const [w, bone] of W2[n]) { try { const wg = (await load(A2 + 'assets/' + w + '.gltf')).scene; wg.traverse(o => { if (o.isMesh) o.material = lift(o.material); }); const bn = find(r, bone); if (bn) bn.add(wg); else miss.push(bone); } catch (e) { miss.push(w); } }
      const [cn, t] = POSE2[n], c = anims.find(c => c.name === cn); if (!c) miss.push(cn); else { const mx = new THREE.AnimationMixer(r); mx.clipAction(c).play(); mx.update(c.duration * t); }
      r.position.set(i * 3, 0, 8); r.rotation.y = -.4; sc.add(r);
    }
    const W = 1800, H = 1150, vw = 18.4, vh = vw * H / W, cam = new THREE.OrthographicCamera(-vw / 2, vw / 2, vh / 2, -vh / 2, .1, 200); cam.position.set(7.5, 15, 28); cam.lookAt(7.5, 1.1, 4);
    const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4 }); R.setRenderTarget(rt); R.setClearColor(0x2c3a4a, 1); R.clear(); R.render(sc, cam); const px = new Uint8Array(W * H * 4); R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g2 = cv.getContext('2d'), id = g2.createImageData(W, H); for (let y = 0; y < H; y++) id.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4); g2.putImageData(id, 0, 0);
    await document.fonts.load('800 20px Kanit'); g2.font = '800 30px Kanit'; g2.fillStyle = '#ffd27a'; g2.fillText('ตอนนี้ (รุ่น 1.0)', 24, 44); g2.fillText('รุ่น 2.0 FREE (ใหม่)', 24, H / 2 + 40);
    return { url: cv.toDataURL(), miss };
  });
  console.log('missing', res.miss.join(',') || 'none');
  fs.writeFileSync(process.argv[2], Buffer.from(res.url.split(',')[1], 'base64')); await b.close(); })();
