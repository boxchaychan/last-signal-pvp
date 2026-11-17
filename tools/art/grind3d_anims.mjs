// The heroes' moves for grind3d.html (archer + knight) (the new level-grinding game, owner 2026-11-17), from the KayKit Character Animations pack (CC0,
// Rig_Medium, already in art/incoming/kaykit/character_animations/). Writes art/grind3d/hero_anims.glb: only the moves below, renamed.
// Needs @gltf-transform/core@4 + functions@4: npm i them in a scratch folder, copy this file there and run it from there:
//   node grind3d_anims.mjs <repo>/art/incoming/kaykit/character_animations/Rig_Medium <repo>/art/grind3d/hero_anims.glb
import { NodeIO } from '@gltf-transform/core';
import { prune, dedup, resample, mergeDocuments, unpartition } from '@gltf-transform/functions';
const [anim, out] = process.argv.slice(2);
const KEEP = {
  General: { Idle_A: 'Idle', Idle_B: 'Idle_B', Hit_A: 'Hit_A', Hit_B: 'Hit_B', Death_A: 'Death_A', Death_B: 'Death_B', Spawn_Ground: 'Spawn_Ground', Use_Item: 'Use_Item', PickUp: 'PickUp' },
  MovementBasic: { Walking_A: 'Walking_A', Running_A: 'Running_A', Jump_Full_Short: 'Jump_Full_Short' },
  MovementAdvanced: { Dodge_Forward: 'Dodge_Forward', Dodge_Backward: 'Dodge_Backward', Dodge_Left: 'Dodge_Left', Dodge_Right: 'Dodge_Right', Running_HoldingBow: 'Running_HoldingBow',
    Running_Strafe_Left: 'Running_Strafe_Left', Running_Strafe_Right: 'Running_Strafe_Right', Walking_Backwards: 'Walking_Backwards' },
  CombatRanged: { Ranged_Bow_Idle: 'Ranged_Bow_Idle', Ranged_Bow_Aiming_Idle: 'Ranged_Bow_Aiming_Idle', Ranged_Bow_Draw: 'Ranged_Bow_Draw', Ranged_Bow_Release: 'Ranged_Bow_Release',
    Ranged_Bow_Draw_Up: 'Ranged_Bow_Draw_Up', Ranged_Bow_Release_Up: 'Ranged_Bow_Release_Up', Ranged_Magic_Summon: 'Ranged_Magic_Summon' },
  Simulation: { Cheering: 'Cheer' },
  CombatMelee: { Melee_2H_Idle: 'Melee_2H_Idle', Melee_2H_Attack_Slice: 'Melee_2H_Attack_Slice', Melee_2H_Attack_Chop: 'Melee_2H_Attack_Chop', Melee_2H_Attack_Stab: 'Melee_2H_Attack_Stab',
    Melee_2H_Attack_Spin: 'Melee_2H_Attack_Spin', Melee_2H_Attack_Spinning: 'Melee_2H_Attack_Spinning', Melee_1H_Attack_Jump_Chop: 'Melee_1H_Attack_Jump_Chop',
    Melee_1H_Attack_Slice_Horizontal: 'Melee_1H_Attack_Slice_Horizontal', Melee_Block: 'Melee_Block', Melee_Blocking: 'Melee_Blocking' },   // the knight (2026-11-17)
};
const io = new NodeIO(); let adoc = null;
for (const [file, keep] of Object.entries(KEEP)) {
  const doc = await io.read(`${anim}/Rig_Medium_${file}.glb`), root = doc.getRoot();
  for (const a of root.listAnimations()) { const nn = keep[a.getName()]; if (nn) { a.setName(nn); continue; } for (const c of a.listChannels()) c.dispose(); for (const sm of a.listSamplers()) sm.dispose(); a.dispose(); }
  for (const n of root.listNodes()) if (n.getMesh()) n.dispose();
  for (const m of root.listMeshes()) m.dispose(); for (const sk of root.listSkins()) sk.dispose(); for (const t of root.listTextures()) t.dispose(); for (const m of root.listMaterials()) m.dispose();
  if (!adoc) adoc = doc; else mergeDocuments(adoc, doc);
}
await adoc.transform(unpartition(), resample(), prune(), dedup());
await io.write(out, adoc);
console.log('moves', adoc.getRoot().listAnimations().map(a => a.getName()).join(','));
