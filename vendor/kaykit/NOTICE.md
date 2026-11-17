# KayKit : Adventurers Character Pack 1.0 (CC0)

By Kay Lousberg (www.kaylousberg.com), Creative Commons Zero: free for any use, credit not required (given here anyway).
Source: github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0

Used in `tribe3d.html` as the villagers and the chief: `art/tribe3d/people/Barbarian.glb` (13 of the 76 moves kept,
shared by both bodies), `Rogue.glb` (no moves of its own), recoloured cloth textures `tex_*.png`.
Made with `tools/art/kaykit_trim.mjs` and `tools/art/kaykit_recolor.py`. Full licence: `License_adventurers.txt`.

# KayKit : Character Animations 1.1 (CC0) — given by the owner 2026-11-16 ("เอานี้ไปด้วยเผื่ออนาคตใช้ท่า")

Kept in `art/incoming/kaykit/character_animations/` (glTF only; the FBX copies of the zip are the same moves): `Rig_Medium/*.glb`
(CombatMelee, CombatRanged incl. bow + magic, General, MovementBasic / Advanced, Simulation, Special, Tools = chop, dig,
pickaxe, hammer, saw, fishing, work) for normal-size characters, `Rig_Large/*.glb` for big ones, the grey mannequins.
Rig_Medium uses the same bone names as our Adventurers 1.0 characters (no IK helper bones), so its moves can play on them.
Full licence: `License_character_animations.txt`.

# KayKit : Adventurers Character Pack 2.0 FREE (CC0) — owner's download 2026-11-17
Kept in `art/incoming/kaykit/adventurers_2.0/`: `characters/` (Knight, Barbarian, Mage, Rogue, Rogue_Hooded, Ranger .glb +
textures; Rig_Medium, no moves inside: the moves come from the Character Animations pack in
`art/incoming/kaykit/character_animations/Rig_Medium`), `assets/` (31 weapons / shields / books / bow / quiver as glTF, attached to the
`handslot.l` / `handslot.r` bones), `contents.png`. Licence `License_adventurers_2.0.txt`.

# KayKit : RPG Tools Bits 1.0 FREE + Fantasy Weapons Bits 1.0 FREE (CC0) — owner's downloads 2026-11-17
glTF kept in `art/incoming/kaykit/rpg_tools_bits/gltf/` and `art/incoming/kaykit/fantasy_weapons_bits/gltf/` (+ `contents.png`); each pack uses
its own texture atlas. tribe3d uses `art/tribe3d/people/tools.glb` (axe, pickaxe, hammer, shovel: villagers' tools) and `fweapons.glb`
(ornate bow / staff for ★★★ units), built by `tools/art/kaykit2_build.mjs`. Licences `License_rpg_tools_bits.txt`, `License_fantasy_weapons_bits.txt`.

# KayKit : Character Pack Skeletons 1.0 (CC0) — from github.com/KayKit-Game-Assets/KayKit-Character-Pack-Skeletons-1.0 (owner sent the org link 2026-11-17)
Kept in `art/incoming/kaykit/skeletons_1.0/`: `characters/` (Skeleton_Warrior / Mage / Rogue / Minion .glb, each with 95 moves incl. Spawn_Ground_Skeletons,
Death_C_Skeletons = falls apart into bones, Death_C_Skeletons_Resurrect), `assets/` (blade, axe, staff, crossbow, shields, arrows, quiver; glTF), `LICENSE.txt`.
Same Rig_Medium bone names as our people (+ IK helper bones). Not in a game yet. Preview: `art/incoming/kaykit/skeletons_preview.mp4` (not in git).
