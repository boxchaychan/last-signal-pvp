# Attack animations for the 5 prehistoric forms, 4 directions (Codex + $game-character-sprites)

Skill: https://github.com/tachikomared/character-animation-creator-skill (install it first: "Install this skill: <link>").

## A. All five in one go (paste this, with the whole refs/ folder attached)

```
Use $game-character-sprites for 5 separate characters, one after another. The reference pictures are in refs/. Do each character as its own job with its own run folder (run_assassin, run_hunter, run_mage, run_support, run_curse) and finish one before starting the next. All five share the same rules: cell 128x128 only, 4 directions (south, east, north, west), idle 4 frames + attack 6 frames for each direction, no walk, transparent background, no detached effects, no dust, no shadows.

When all five are done, zip EVERYTHING into one file dino_anim.zip: every run folder in full, including the full-size raw images in source/ and generated/, the clean sheets, and the GIF previews. Also put in the zip one large preview picture per character showing all its rows (idle and attack for each of the 4 directions, as large as you can). Do not shrink anything.

Use $game-character-sprites.
Reference: the attached picture refs/01_nin_velociraptor.png (Nin in velociraptor armour, holding two curved sickle-claw daggers in a reverse grip). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose, both claw daggers ready (same as the reference)
  2. crouch low, both daggers pulled back by the hips, weight on the back foot
  3. spring forward, the front foot stepping ahead, both arms coming forward
  4. cross slash: both claw daggers slash across in front of her in an X, body stretched forward
  5. follow-through: arms crossed past the body, the feathered tail cape flaring behind
  6. step back and return to the standing pose
Keep the reverse grip in every frame: a ring on top of each fist, the curved blade coming out of the bottom of the fist and curving back toward her body.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_assassin.

Use $game-character-sprites.
Reference: the attached picture refs/02_fah_pteranodon.png (Fah in pteranodon armour, holding a big longbow made of pteranodon wing bones). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the bow held forward and an arrow nocked (same as the reference)
  2. raise the bow and start pulling the string back
  3. full draw: the string pulled back to her cheek, the bow bent, aiming straight ahead
  4. release: the string snaps forward, the arrow is gone from the bow, a small recoil
  5. follow-through: the bow arm stays forward, the wing cape flutters
  6. reach to the quiver for a new arrow and return to the standing pose
Do not draw the flying arrow: the game draws the shot itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_hunter.

Use $game-character-sprites.
Reference: the attached picture refs/03_ratri_stegosaurus.png (Ratri in stegosaurus armour, holding a tall staff topped with a glowing violet crystal). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the staff planted on the ground (same as the reference)
  2. lift the staff up in front of her, the free hand rising
  3. staff raised high, the crystal on the staff and the crystal plates on her hood and cape glowing brighter
  4. thrust the staff forward, pointing the crystal at the enemy in front of her, a small step forward
  5. hold the thrust, the crystals at their brightest
  6. lower the staff and return to the standing pose
Only the crystals that are part of the costume glow; do not draw magic bolts or sparks flying away: the game draws the spell itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_mage.

Use $game-character-sprites.
Reference: the attached picture refs/04_chan_triceratops.png (Chan in triceratops armour, holding a healing staff topped with a glowing pink crystal horn, and a small round frill shield). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the staff upright and the shield on his arm (same as the reference)
  2. raise the frill shield in front of him and lift the staff back over his shoulder
  3. step forward behind the shield, the staff at the top of the swing
  4. swing the staff down and forward so the pink crystal horn points at the enemy in front of him, the shield pushed forward
  5. follow-through, the crystal glowing brightest
  6. return to the standing pose
Only the crystal that is part of the staff glows; do not draw heal bolts or sparks flying away: the game draws them itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_support.

Use $game-character-sprites.
Reference: the attached picture refs/05_mok_spinosaurus.png (Mok in spinosaurus armour, holding a jaw-bone staff topped with a glowing purple eye orb). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the staff held at her side (same as the reference)
  2. lean back, raise the staff, the free hand curling like a claw
  3. the sail on her back spreads up taller and its purple veins glow brighter, the staff held high
  4. thrust the staff forward, pointing the eye orb at the enemy in front of her, the free hand pushing forward
  5. hold the cast, the eye orb and the sail veins at their brightest
  6. lower the staff and return to the standing pose
Only the eye orb and the sail veins that are part of the costume glow; do not draw curse bolts or smoke flying away: the game draws the curse itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_curse.
```

## B. One at a time (attach only that character's picture)

### 1. Nin - velociraptor

```
Use $game-character-sprites.
Reference: the attached picture refs/01_nin_velociraptor.png (Nin in velociraptor armour, holding two curved sickle-claw daggers in a reverse grip). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose, both claw daggers ready (same as the reference)
  2. crouch low, both daggers pulled back by the hips, weight on the back foot
  3. spring forward, the front foot stepping ahead, both arms coming forward
  4. cross slash: both claw daggers slash across in front of her in an X, body stretched forward
  5. follow-through: arms crossed past the body, the feathered tail cape flaring behind
  6. step back and return to the standing pose
Keep the reverse grip in every frame: a ring on top of each fist, the curved blade coming out of the bottom of the fist and curving back toward her body.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_assassin.
When done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of all rows (idle and attack for each of the 4 directions). Do not shrink anything.
```

### 2. Fah - pteranodon

```
Use $game-character-sprites.
Reference: the attached picture refs/02_fah_pteranodon.png (Fah in pteranodon armour, holding a big longbow made of pteranodon wing bones). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the bow held forward and an arrow nocked (same as the reference)
  2. raise the bow and start pulling the string back
  3. full draw: the string pulled back to her cheek, the bow bent, aiming straight ahead
  4. release: the string snaps forward, the arrow is gone from the bow, a small recoil
  5. follow-through: the bow arm stays forward, the wing cape flutters
  6. reach to the quiver for a new arrow and return to the standing pose
Do not draw the flying arrow: the game draws the shot itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_hunter.
When done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of all rows (idle and attack for each of the 4 directions). Do not shrink anything.
```

### 3. Ratri - stegosaurus

```
Use $game-character-sprites.
Reference: the attached picture refs/03_ratri_stegosaurus.png (Ratri in stegosaurus armour, holding a tall staff topped with a glowing violet crystal). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the staff planted on the ground (same as the reference)
  2. lift the staff up in front of her, the free hand rising
  3. staff raised high, the crystal on the staff and the crystal plates on her hood and cape glowing brighter
  4. thrust the staff forward, pointing the crystal at the enemy in front of her, a small step forward
  5. hold the thrust, the crystals at their brightest
  6. lower the staff and return to the standing pose
Only the crystals that are part of the costume glow; do not draw magic bolts or sparks flying away: the game draws the spell itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_mage.
When done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of all rows (idle and attack for each of the 4 directions). Do not shrink anything.
```

### 4. Chan - triceratops

```
Use $game-character-sprites.
Reference: the attached picture refs/04_chan_triceratops.png (Chan in triceratops armour, holding a healing staff topped with a glowing pink crystal horn, and a small round frill shield). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the staff upright and the shield on his arm (same as the reference)
  2. raise the frill shield in front of him and lift the staff back over his shoulder
  3. step forward behind the shield, the staff at the top of the swing
  4. swing the staff down and forward so the pink crystal horn points at the enemy in front of him, the shield pushed forward
  5. follow-through, the crystal glowing brightest
  6. return to the standing pose
Only the crystal that is part of the staff glows; do not draw heal bolts or sparks flying away: the game draws them itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_support.
When done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of all rows (idle and attack for each of the 4 directions). Do not shrink anything.
```

### 5. Mok - spinosaurus

```
Use $game-character-sprites.
Reference: the attached picture refs/05_mok_spinosaurus.png (Mok in spinosaurus armour, holding a jaw-bone staff topped with a glowing purple eye orb). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.
Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.
The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).
Idle: gentle breathing, the feet do not move.
Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):
  1. standing pose with the staff held at her side (same as the reference)
  2. lean back, raise the staff, the free hand curling like a claw
  3. the sail on her back spreads up taller and its purple veins glow brighter, the staff held high
  4. thrust the staff forward, pointing the eye orb at the enemy in front of her, the free hand pushing forward
  5. hold the cast, the eye orb and the sail veins at their brightest
  6. lower the staff and return to the standing pose
Only the eye orb and the sail veins that are part of the costume glow; do not draw curse bolts or smoke flying away: the game draws the curse itself.
Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.
No detached effects, no dust, no shadows, transparent background.
Save the results in a folder named dino_curse.
When done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of all rows (idle and attack for each of the 4 directions). Do not shrink anything.
```
