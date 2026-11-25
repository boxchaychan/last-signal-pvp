# ศึกผู้รับพร (divine.html): art still missing, Codex brief

Work like the Zeus set (`art/divine/zeus/`, `art/incoming/divine_game/reports/zeus_v1.md`). Same chibi cartoon style as
`art/incoming/divine_game/ref/owner_tone_zeus_boy.jpg` and the approved Zeus poses: thick dark-brown outline, flat bright colours, soft cel shading,
about 2 heads tall, the SAME body size as Zeus. Transparent PNG, one 512 x 512 frame per picture, the feet on the same ground line as Zeus
(origin 256, 500). Keep the raw pictures in `art/incoming/divine_game/raw/<set>/` and add a report in `art/incoming/divine_game/reports/`.
Branch `codex/divine-<set>`. Open a PR, do not merge it, and do not change `divine.html` (Claude wires it in).

## A. Thor set (`art/divine/thor/`)
Viking kid blessed by the thunder god: a small winged silver helmet over messy blond hair, a short red cape, a blue tunic, a glowing thunder hammer.
- `idle_key.png`, `attack_key.png` (throws the hammer forward), `skill_key.png` (hammer raised, lightning)
- `vfx_thor_spirit.png`: the big translucent glowing Thor behind him (braided red beard, winged helmet, hammer), same look as `vfx_zeus_spirit.png`
- `vfx_hammer_shock.png`: a round blue lightning shockwave seen from above at an angle

## B. Anubis set (`art/divine/anubis/`)
Egyptian kid blessed by the jackal god: a blue-and-gold nemes headdress with tall black jackal ears, a white kilt, a gold collar, a golden spear.
- `idle_key.png`, `attack_key.png` (spear thrust), `skill_key.png` (spear raised, sand swirling)
- `vfx_anubis_spirit.png`: the translucent glowing jackal-headed god behind him
- `vfx_sand_beam.png`: a straight golden sand beam, horizontal

## C. Monkey King set (`art/divine/wukong/`)
Kid blessed by the Monkey King: a golden circlet, spiky orange-brown hair, monkey ears and tail, a red-gold outfit, a long red staff with flames.
- `idle_key.png`, `attack_key.png` (staff swing), `skill_key.png` (staff spinning overhead)
- `vfx_wukong_spirit.png`: the translucent glowing Monkey King behind him
- `vfx_fireball.png`: one round fireball with a short flame tail

## D. Common recruit (`art/divine/recruit/`)
A plain temple recruit kid with a bronze helmet, a round wooden shield and a short spear. Simpler than the heroes.
- `idle_key.png`, `attack_key.png`

## E. Monsters (`art/divine/mobs/`)
"Corrupted" monsters in the same cartoon style, side view walking to the LEFT, one per picture, about 70 % of a hero's height:
cracked clay soldier with purple glow, shadow wisp with a skull face, hopping stone gargoyle, bronze bull on two legs, mummy dog, armoured beetle.
- `boss_titan.png`: a huge corrupted titan of dark stone and purple crystals, TWICE a hero's height.

## F. Arena background (`art/divine/arena.png`, 1170 x 2532, portrait, NOT transparent)
A floating temple island in a bright cartoon sky: blue sky with soft clouds and sun rays at the top, far floating islands with small Greek
temples, the island's grass top with columns, bushes, flowers and two stone braziers near the bottom edge, the rock underside with vines and two
waterfalls falling into a sea of clouds below. IMPORTANT: leave the band from 24 % to 56 % of the height, full width, as ONE flat plain light
marble plaza with nothing on it (the game draws the board and the road there). Leave the top 20 % and the bottom 33 % calm (the game puts its
buttons there). No characters, no text, no UI.
