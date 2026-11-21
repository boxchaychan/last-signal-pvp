// Quaternius Universal Animation Library (CC0, UE-mannequin skeleton) -> KayKit Rig_Medium bone names, so our heroes (KayKit skeleton,
// or Tripo models re-bound onto it by rigTripo) can play them. Runs three.js in a headless page (python3 -m http.server 8000 first):
//   node tools/art/ual_retarget.js [out=art/grind3d/ual_anims.json]
// Method: both skeletons are put in their T-pose (UAL: the "A_TPose" clip; KayKit: its rest pose). For every frame, each mapped bone gets the
// source bone's WORLD rotation change from its T-pose, applied to the target bone's T-pose world rotation, turned back into a local rotation.
// Hips height follows the source (scaled by leg length). Unmapped KayKit bones (wrists, hand slots, toes...) keep their rest rotation.
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = process.argv[2] || 'art/grind3d/ual_anims.json';
const PICK = process.env.UAL_PICK === 'zombie' ? {   // zcity.html: UAL_PICK=zombie node tools/art/ual_retarget.js art/zcity/zombie_anims.json
  'art/incoming/quaternius/ual/UAL1_Standard.glb': ['Death01', 'Hit_Chest', 'Sprint_Loop'],
  'art/incoming/quaternius/ual/UAL2_Standard.glb': ['Zombie_Idle_Loop', 'Zombie_Scratch', 'Zombie_Walk_Fwd_Loop', 'Hit_Knockback'],
} : {   // source file -> moves kept (name in the game = 'Q_' + name)
  'art/incoming/quaternius/ual/UAL1_Standard.glb': ['Idle_Loop', 'Sword_Idle', 'Sword_Attack', 'Spell_Simple_Enter', 'Spell_Simple_Idle_Loop', 'Spell_Simple_Shoot', 'Spell_Simple_Exit', 'Roll', 'Jog_Fwd_Loop', 'Sprint_Loop', 'Walk_Loop', 'Punch_Jab', 'Punch_Cross', 'Hit_Chest', 'Hit_Head', 'Death01', 'Jump_Start', 'Jump_Loop', 'Jump_Land', 'Dance_Loop', 'Crouch_Idle_Loop', 'Interact', 'Idle_Talking_Loop'],
  'art/incoming/quaternius/ual/UAL2_Standard.glb': ['Sword_Regular_A', 'Sword_Regular_B', 'Sword_Regular_C', 'Sword_Regular_Combo', 'Sword_Heavy_Combo', 'Sword_Dash', 'Sword_Block', 'Shield_Dash', 'Shield_OneShot', 'Idle_Shield_Loop', 'Idle_Shield_Break', 'Melee_Hook', 'OverhandThrow', 'Hit_Knockback', 'NinjaJump_Start', 'NinjaJump_Idle_Loop', 'NinjaJump_Land', 'Slide_Start', 'Slide_Loop', 'Slide_Exit', 'Idle_FoldArms_Loop', 'Yes', 'Zombie_Walk_Fwd_Loop'],
};
const MAP = { pelvis: 'hips', spine_01: 'spine', spine_03: 'chest', Head: 'head', upperarm_l: 'upperarml', lowerarm_l: 'lowerarml', hand_l: 'wristl', upperarm_r: 'upperarmr', lowerarm_r: 'lowerarmr', hand_r: 'wristr',
  thigh_l: 'upperlegl', calf_l: 'lowerlegl', foot_l: 'footl', ball_l: 'toesl', thigh_r: 'upperlegr', calf_r: 'lowerlegr', foot_r: 'footr', ball_r: 'toesr' };
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); pg.on('console', m => console.log('page:', m.text())); pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8000/vendor/threejs/three.min.js'); await pg.setContent('<html><body></body></html>');
  for (const s of ['three.min.js', 'GLTFLoader.js']) await pg.addScriptTag({ url: `http://localhost:8000/vendor/threejs/${s}` });
  const res = await pg.evaluate(async ([PICK, MAP]) => {
    const ld = new THREE.GLTFLoader(), V3 = THREE.Vector3, Qt = THREE.Quaternion, B = 'http://localhost:8000/';
    const K = await ld.loadAsync(B + 'art/tribe3d/people/Knight.glb'); const tgt = K.scene; tgt.updateMatrixWorld(true);
    const tB = {}; tgt.traverse(o => { if (o.isBone) tB[o.name] = o; });
    const order = []; tgt.traverse(o => { if (o.isBone) order.push(o); });
    const tRestLocal = {}, tRefW = {}; for (const o of order) { tRestLocal[o.name] = o.quaternion.clone(); tRefW[o.name] = o.getWorldQuaternion(new Qt()); }
    const tHips = tB.hips.getWorldPosition(new V3()), tFoot = tB.footl.getWorldPosition(new V3());
    const out = [];
    for (const [file, names] of Object.entries(PICK)) {
      const U = await ld.loadAsync(B + file); const src = U.scene, sB = {}; src.traverse(o => { if (o.isBone) sB[o.name] = o; });
      const mx = new THREE.AnimationMixer(src), clip = n => U.animations.find(c => c.name === n);
      const pose = (c, t) => { mx.stopAllAction(); const a = mx.clipAction(c); a.reset().play(); mx.setTime(t); src.updateMatrixWorld(true); };
      pose(clip('A_TPose'), 0); const sRefW = {}; for (const s in MAP) sRefW[s] = sB[s].getWorldQuaternion(new Qt());
      const sHips = sB.pelvis.getWorldPosition(new V3()), sFoot = sB.foot_l.getWorldPosition(new V3()), k = (tHips.y - tFoot.y) / (sHips.y - sFoot.y);
      // facing: the toes point forward in both T-poses; turn the source deltas if the two face different ways
      const fwd = (a, b) => { const v = b.getWorldPosition(new V3()).sub(a.getWorldPosition(new V3())); v.y = 0; return v.normalize(); };
      const fs = fwd(sB.foot_l, sB.ball_l), ft = fwd(tB.footl, tB.toesl), C = new Qt().setFromUnitVectors(fs, ft), Ci = C.clone().invert();
      for (const n of names) {
        const c = clip(n); if (!c) { console.log('missing ' + n); continue; }
        const fps = 30, nf = Math.max(2, Math.round(c.duration * fps) + 1), times = [], Q = {}, HP = [];
        for (const o of order) Q[o.name] = [];
        for (let f = 0; f < nf; f++) { const t = Math.min(c.duration, f / fps); times.push(+t.toFixed(4)); pose(c, t);
          for (const o of order) o.quaternion.copy(tRestLocal[o.name]); tgt.updateMatrixWorld(true);
          for (const o of order) {   // parents come first in traverse order
            const s = Object.keys(MAP).find(q => MAP[q] === o.name);
            if (s) { const d = sB[s].getWorldQuaternion(new Qt()).multiply(sRefW[s].clone().invert()); d.premultiply(C).multiply(Ci);
              const w = d.multiply(tRefW[o.name]), pw = o.parent.getWorldQuaternion(new Qt()); o.quaternion.copy(pw.invert().multiply(w)); o.updateMatrixWorld(true); }
            Q[o.name].push(...o.quaternion.toArray().map(v => +v.toFixed(4)));
          }
          const sp = sB.pelvis.getWorldPosition(new V3()).sub(sHips).applyQuaternion(C).multiplyScalar(k), hw = tHips.clone().add(sp), hl = tB.hips.parent.worldToLocal(hw.clone());
          HP.push(+hl.x.toFixed(4), +hl.y.toFixed(4), +hl.z.toFixed(4)); }
        const tracks = order.map(o => ({ name: o.name + '.quaternion', type: 'quaternion', times, values: Q[o.name] })); tracks.push({ name: 'hips.position', type: 'vector', times, values: HP });
        out.push({ name: 'Q_' + n, duration: +c.duration.toFixed(4), tracks });
      }
    }
    return out;
  }, [PICK, MAP]);
  fs.writeFileSync(OUT, JSON.stringify({ source: 'Quaternius Universal Animation Library 1 + 2 [Standard], CC0, retargeted to KayKit Rig_Medium by tools/art/ual_retarget.js', clips: res }));
  console.log('wrote', OUT, res.length, 'clips', (fs.statSync(OUT).size / 1e6).toFixed(2), 'MB'); await b.close();
})();
