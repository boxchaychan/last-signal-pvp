// Trims the CC0 KayKit Adventurers characters for tribe3d.html: keeps only the moves the game uses (one shared set on the
// Barbarian; the others get none: same rig, so the Barbarian's clips play on all of them) and drops props we never show.
// Needs @gltf-transform/core@4 + functions@4: npm i them in a scratch folder, copy this file there and run it from there (ESM ignores NODE_PATH).
//   node tools/art/kaykit_trim.mjs <kaykit .../Characters/gltf folder> art/tribe3d/people
import { NodeIO } from '@gltf-transform/core';
import { prune, dedup, resample } from '@gltf-transform/functions';
const [src, out] = process.argv.slice(2);
const KEEP = ['Idle', 'Walking_A', 'Running_A', '1H_Melee_Attack_Chop', '1H_Melee_Attack_Slice_Diagonal', '2H_Melee_Attack_Chop', 'PickUp', 'Interact', 'Throw', 'Hit_A', 'Death_A', 'Cheer', 'Sit_Floor_Idle',
  '1H_Ranged_Shoot', 'Spellcast_Shoot', 'Spellcast_Raise', 'Block'];   // + shooting / spells for the hunters and shamans
const JOBS = [
  ['Barbarian', KEEP, ['1H_Axe_Offhand', 'Mug']],
  ['Rogue', [], ['Knife_Offhand', '1H_Crossbow', '2H_Crossbow', 'Throwable']],
  ['Knight', [], ['1H_Sword_Offhand', 'Badge_Shield', 'Rectangle_Shield', 'Spike_Shield', '2H_Sword']],   // warriors
  ['Mage', [], ['Spellbook', 'Spellbook_open', '1H_Wand']],   // shamans
  ['Rogue_Hooded', [], ['Knife_Offhand', '2H_Crossbow', 'Knife', 'Throwable']],   // crossbow hunters
];
const io = new NodeIO();
for (const [name, keep, drop] of JOBS) {
  const doc = await io.read(`${src}/${name}.glb`), root = doc.getRoot();
  for (const a of root.listAnimations()) if (!keep.includes(a.getName())) { for (const c of a.listChannels()) c.dispose(); for (const sm of a.listSamplers()) sm.dispose(); a.dispose(); }
  for (const n of root.listNodes()) if (drop.includes(n.getName())) n.dispose();
  await doc.transform(resample(), prune(), dedup());
  await io.write(`${out}/${name}.glb`, doc);
  console.log(name, root.listAnimations().map(a => a.getName()).join(','));
}
