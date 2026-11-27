/* Spring bones: the ponytail and scarf tails of the adventurer (tools/blender/adventurer_model.py writes the chains into the GLB extras; rigTripo()
   adds those bones under the KayKit skeleton and calls springMake). Every chain bone chases its rest pose with a soft spring, so hair and cloth
   lag behind a turn, bounce on a landing and wave a little in the wind. Shared by bag3d.html (duel view) and horde.html?bag=1 (horde fight).
     springMake(T)            T = what rigTripo returns (root, bone, chains), still in the bind pose
     springStep(S, dt)        once a frame, after the mixer and after the root is placed
   chain = { b: [bone names root -> end], tip: [x, y, z] the free end (model space), k: spring (rad2 / s2), d: speed kept per 1/60 s, g: droop, w: wind, lim: most bend (rad) } */
'use strict';
function springMake(T) {
  if (!T.chains || !T.chains.length) return null; T.root.updateMatrixWorld(true); const V = THREE.Vector3, S = { root: T.root, ch: [], acc: 0, t: Math.random() * 9 };
  for (const c of T.chains) { const bs = c.b.map(n => T.bone[n]); if (bs.some(b => !b)) continue; const js = [];
    bs.forEach((b, i) => { const axis = i < bs.length - 1 ? bs[i + 1].position.clone() : b.worldToLocal(new V(...c.tip).applyMatrix4(T.root.matrixWorld)); js.push({ b, q0: b.quaternion.clone(), axis, dir: axis.clone().normalize(), tail: b.localToWorld(axis.clone()), prev: null, ph: i * 1.7 + S.ch.length * 2.3 }); });
    for (const j of js) j.prev = j.tail.clone(); S.ch.push({ js, k: c.k || 120, d: c.d == null ? .9 : c.d, g: c.g || 0, w: c.w || 0, lim: c.lim || 1.1 }); }
  return S.ch.length ? S : null;
}
const _spM = new THREE.Matrix4(), _spI = new THREE.Matrix4(), _spP = new THREE.Vector3(), _spR = new THREE.Vector3(), _spN = new THREE.Vector3(), _spD = new THREE.Vector3(), _spQ = new THREE.Quaternion();
function springStep(S, dt) {
  if (!S) return; S.root.updateMatrixWorld(true); S.acc = Math.min(S.acc + dt, .07); const h = 1 / 60; let n = Math.floor(S.acc / h); S.acc -= n * h; if (n < 1) n = 0;
  do { S.t += h;   /* at least one pass: the bones must follow the body even on a frame without a physics step */
    for (const c of S.ch) for (const j of c.js) { const b = j.b, par = b.parent;
      _spM.compose(b.position, j.q0, b.scale).premultiply(par.matrixWorld); _spP.setFromMatrixPosition(_spM); _spR.copy(j.axis).applyMatrix4(_spM); const len = _spR.distanceTo(_spP) || 1e-6;
      if (n > 0) { _spN.copy(j.tail).sub(j.prev).multiplyScalar(c.d).add(j.tail); _spD.copy(_spR).sub(j.tail); if (_spD.length() > len * 3) { j.tail.copy(_spR); j.prev.copy(_spR); _spN.copy(_spR); } else { _spN.addScaledVector(_spD, Math.min(.9, c.k * h * h));
          _spN.y -= c.g * len * h * h; if (c.w) { _spN.x += Math.sin(S.t * 2.3 + j.ph) * c.w * len * h * h; _spN.z += Math.sin(S.t * 3.1 + j.ph * 1.3) * c.w * len * h * h; _spN.y += Math.sin(S.t * 4.3 + j.ph * .7) * c.w * .5 * len * h * h; } }
        _spN.sub(_spP).normalize(); _spD.copy(_spR).sub(_spP).normalize(); const a = Math.acos(Math.min(1, Math.max(-1, _spN.dot(_spD)))); if (a > c.lim) _spN.lerp(_spD, 1 - c.lim / a).normalize();   /* never bend further than lim from the rest pose */
        j.prev.copy(j.tail); j.tail.copy(_spP).addScaledVector(_spN, len); }
      _spN.copy(j.tail).applyMatrix4(_spI.copy(_spM).invert()).normalize(); b.quaternion.copy(j.q0).multiply(_spQ.setFromUnitVectors(j.dir, _spN)); b.updateMatrix(); b.matrixWorld.multiplyMatrices(par.matrixWorld, b.matrix); }
  } while (--n > 0);
}
