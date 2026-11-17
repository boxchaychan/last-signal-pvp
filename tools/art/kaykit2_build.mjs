// Builds the people of tribe3d.html from KayKit Adventurers 2.0 (owner 2026-11-17: "พวกนี้ทำระดับ 1 ดาว 2 ดาว เอาตัวเวอร์ชันเก่าออก ทำให้สวย
// เตรียมทำ 3 ดาว"). Writes into art/tribe3d/people/:
//   <Hero>.glb       the 6 heroes as they are (Rig_Medium, no moves)
//   weapons.glb      the weapons we use, one top-level node each (named after the file); they share the hero textures
//   anims.glb        the moves we use from the Character Animations pack, RENAMED to the names the game code uses
// Needs @gltf-transform/core@4 + functions@4: npm i them in a scratch folder, copy this file there and run it from there:
//   node kaykit2_build.mjs <repo>/art/incoming/kaykit/adventurers_2.0 <repo>/art/incoming/kaykit/character_animations/Rig_Medium <repo>/art/tribe3d/people
import { NodeIO } from '@gltf-transform/core';
import { prune, dedup, resample, mergeDocuments, unpartition } from '@gltf-transform/functions';
import fs from 'fs';
const [adv, anim, out] = process.argv.slice(2);
const KK = adv.replace(/adventurers_2\.0\/?$/, '');   // art/incoming/kaykit/
const io = new NodeIO();
for (const h of ['Barbarian', 'Knight', 'Mage', 'Rogue', 'Rogue_Hooded', 'Ranger']) fs.copyFileSync(`${adv}/characters/${h}.glb`, `${out}/${h}.glb`);
// weapons
const W = ['sword_1handed', 'sword_2handed_color', 'shield_round', 'shield_badge_color', 'shield_spikes_color', 'axe_1handed', 'axe_2handed', 'shield_round_barbarian', 'crossbow_1handed', 'dagger', 'bow_withString', 'arrow_bow_bundle', 'staff', 'wand', 'spellbook_open'];
const wdoc = await io.read(`${adv}/assets/${W[0]}.gltf`);
for (const w of W.slice(1)) mergeDocuments(wdoc, await io.read(`${adv}/assets/${w}.gltf`));
{ const root = wdoc.getRoot(), scenes = root.listScenes(), main = scenes[0];
  scenes.forEach((sc, i) => { for (const n of sc.listChildren()) { if (i) { sc.removeChild(n); main.addChild(n); } } if (i) sc.dispose(); });
  const names = new Set(); for (const n of main.listChildren()) { names.add(n.getName()); }
  for (const t of root.listTextures()) t.dispose();   // the game draws them with the hero's own texture
  await wdoc.transform(unpartition(), prune({ keepAttributes: true }), dedup());   // keepAttributes: without textures prune() would drop the UVs
  await io.write(`${out}/weapons.glb`, wdoc); console.log('weapons', [...names].join(',')); }
// moves (new name -> old name the game uses)
const KEEP = {
  General: { Idle_A: 'Idle', Hit_A: 'Hit_A', Death_A: 'Death_A', PickUp: 'PickUp', Interact: 'Interact', Throw: 'Throw' },
  MovementBasic: { Walking_A: 'Walking_A', Running_A: 'Running_A' },
  CombatMelee: { Melee_1H_Attack_Chop: '1H_Melee_Attack_Chop', Melee_1H_Attack_Slice_Diagonal: '1H_Melee_Attack_Slice_Diagonal', Melee_2H_Attack_Chop: '2H_Melee_Attack_Chop', Melee_Block: 'Block', Melee_2H_Attack_Spin: '2H_Melee_Attack_Spin' },
  CombatRanged: { Ranged_1H_Shoot: '1H_Ranged_Shoot', Ranged_Magic_Shoot: 'Spellcast_Shoot', Ranged_Magic_Raise: 'Spellcast_Raise', Ranged_Bow_Idle: 'Ranged_Bow_Idle', Ranged_Bow_Draw: 'Ranged_Bow_Draw', Ranged_Bow_Release: 'Ranged_Bow_Release' },
  Simulation: { Cheering: 'Cheer', Sit_Floor_Idle: 'Sit_Floor_Idle' },
  Tools: { Chopping: 'Chopping', Pickaxing: 'Pickaxing', Hammering: 'Hammering' },
};
let adoc = null;
for (const [file, keep] of Object.entries(KEEP)) {
  const doc = await io.read(`${anim}/Rig_Medium_${file}.glb`), root = doc.getRoot();
  for (const a of root.listAnimations()) { const nn = keep[a.getName()]; if (nn) { a.setName(nn); continue; } for (const c of a.listChannels()) c.dispose(); for (const sm of a.listSamplers()) sm.dispose(); a.dispose(); }
  for (const n of root.listNodes()) if (n.getMesh()) n.dispose();
  for (const m of root.listMeshes()) m.dispose(); for (const sk of root.listSkins()) sk.dispose(); for (const t of root.listTextures()) t.dispose(); for (const m of root.listMaterials()) m.dispose();
  if (!adoc) adoc = doc; else mergeDocuments(adoc, doc);
}
await adoc.transform(unpartition(), resample(), prune(), dedup());
await io.write(`${out}/anims.glb`, adoc);
console.log('anims', adoc.getRoot().listAnimations().map(a => a.getName()).join(','));

// "bits" packs keep their own texture atlas: one glb each, one top-level node per item
async function bits(dir, items, file) {
  const doc = await io.read(`${dir}/${items[0]}.gltf`);
  for (const it of items.slice(1)) mergeDocuments(doc, await io.read(`${dir}/${it}.gltf`));
  const root = doc.getRoot(), scenes = root.listScenes(), main = scenes[0];
  scenes.forEach((sc, i) => { if (!i) return; for (const n of sc.listChildren()) { sc.removeChild(n); main.addChild(n); } sc.dispose(); });
  await doc.transform(unpartition(), prune({ keepAttributes: true }), dedup());
  await io.write(`${out}/${file}`, doc); console.log(file, main.listChildren().map(n => n.getName()).join(','));
}
await bits(KK + 'rpg_tools_bits/gltf', ['axe', 'pickaxe', 'hammer', 'shovel', 'bucket_metal', 'torch'], 'tools.glb');
await bits(KK + 'fantasy_weapons_bits/gltf', ['bow_A_withString', 'staff_A', 'staff_B', 'halberd', 'sword_E', 'shield_B', 'spear_A', 'arrow_A'], 'fweapons.glb');
