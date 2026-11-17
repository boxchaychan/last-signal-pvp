// The red-scarf hero of tribe3d.html (owner's design picture, art/incoming/tribe3d/hero_ref.png): the KayKit Adventurers 2.0 Knight with no
// helmet and no cape, its body parts pointed at the new swatches of tex_hero_0.png (tools/art/hero_tex.py): purple tunic, dark purple trousers,
// brown boots, gold bands / buckle / chest badge, reddish-brown hair, bare hands. Hair spikes, headband, scarf, pads and sword: tools/blender/hero_gear.py.
//   needs @gltf-transform/core + functions (copy this file next to their node_modules and run it there):
//   node hero_build.mjs <repo>/art/incoming/kaykit/adventurers_2.0/characters/Knight.glb <repo>/art/tribe3d/people/Hero.glb
import { NodeIO } from '@gltf-transform/core';
import { prune } from '@gltf-transform/functions';
const [src, out] = process.argv.slice(2), io = new NodeIO(), doc = await io.read(src);
const DROP = ['Knight_Helmet', 'Knight_HelmetVisor', 'Knight_Cape'];
for (const n of doc.getRoot().listNodes()) if (DROP.includes(n.getName())) n.dispose();
const CELL = (c, r) => [c, r];   // swatch cell: 8 columns, 4 rows (row = v * 4)
const S = { P: CELL(0, 2), PD: CELL(1, 2), PD2: CELL(2, 2), B: CELL(3, 2), BD: CELL(4, 2), BD2: CELL(5, 2), G: CELL(6, 2), G2: CELL(7, 2), G3: CELL(0, 3), H: CELL(1, 3), PD4: CELL(2, 3), SK: CELL(3, 3), ST: CELL(4, 3), BL: CELL(5, 3) };
// rules: [part regex, source cell "c,r", test(x, y, z) or null, target slot]; the first match wins
const RULES = [
  [/Head/, '1,0', null, 'H'],
  [/Arm/, '3,0', (x) => Math.abs(x) > .78, 'SK'], [/Arm/, '7,0', (x) => Math.abs(x) > .78, 'SK'], [/Arm/, '4,0', (x) => Math.abs(x) > .78, 'SK'],   // bare fists
  [/Arm/, '6,0', null, 'G'], [/Arm/, '3,0', null, 'P'], [/Arm/, '7,0', null, 'PD'], [/Arm/, '4,0', null, 'PD4'],
  [/Body/, '3,0', null, 'P'], [/Body/, '7,0', null, 'PD'], [/Body/, '7,1', null, 'PD2'], [/Body/, '0,1', null, 'P'],   /* the chest rosette goes; a gold badge comes from hero_gear */ [/Body/, '1,1', null, 'G3'], [/Body/, '2,1', (x, y) => y < .8, 'G3'], [/Body/, '6,0', null, 'BL'], [/Body/, '4,0', null, 'PD4'],
  [/Leg/, '3,0', (x, y) => y < .27, 'B'], [/Leg/, '7,0', (x, y) => y < .27, 'BD'], [/Leg/, '7,1', (x, y) => y < .27, 'BD2'],
  [/Leg/, '6,0', null, 'G'], [/Leg/, '3,0', null, 'PD'], [/Leg/, '7,0', null, 'PD2'], [/Leg/, '7,1', null, 'PD2'],
];
const used = {};
for (const n of doc.getRoot().listNodes()) {
  const m = n.getMesh(); if (!m) continue; const name = n.getName();
  for (const p of m.listPrimitives()) {
    const uv = p.getAttribute('TEXCOORD_0'), pos = p.getAttribute('POSITION'), a = [0, 0], q = [0, 0, 0];
    const nuv = uv.clone(); p.setAttribute('TEXCOORD_0', nuv);   // own copy: parts may share accessors
    for (let i = 0; i < uv.getCount(); i++) {
      uv.getElement(i, a); pos.getElement(i, q);
      const c = Math.min(7, Math.floor(a[0] * 8)), r = Math.min(3, Math.floor(a[1] * 4)), key = c + ',' + r;
      const rule = RULES.find(([re, k, t]) => re.test(name) && k === key && (!t || t(q[0], q[1], q[2]))); if (!rule) continue;
      const [tc, tr] = S[rule[3]]; nuv.setElement(i, [a[0] - c / 8 + tc / 8, a[1] - r / 4 + tr / 4]);
      used[name + ' ' + key + '>' + rule[3]] = (used[name + ' ' + key + '>' + rule[3]] || 0) + 1;
    }
  }
}
await doc.transform(prune({ keepAttributes: true }));
await io.write(out, doc); console.log(used); console.log('wrote', out);
