# Skill / attack effects for the action game, made by Codex (owner 2026-11-09 "มีเอฟเฟคที่อยากได้ไหม"). One picture per
# effect: 6 frames in a 3x2 grid of 512 px cells on PURE BLACK, so the importer can turn brightness into see-through
# (glows stay soft). Seen from the game's camera: low top-down, so things lying on the ground are flat ellipses.
#   python tools/art/fx_codex.py       -> docs/codex/action/FX.md (queue + full prompts; keeps rows marked done)
import re, os
FX = [   # key, thai, for, what happens over the 6 frames
 ('fireball', 'ลูกไฟ', 'mage Q', 'a round fireball flying to the RIGHT: a bright yellow-white core inside orange and red flames with a short flame tail streaming to the left; a looping flight, every frame a slightly different flicker of the flames'),
 ('meteor', 'อุกกาบาต', 'mage Z', 'a flaming meteor rock falling diagonally down to the right: a dark cracked rock with glowing orange cracks, wrapped in fire with a long fire trail behind it up to the top left; a looping fall, the flames flickering'),
 ('meteor_hit', 'อุกกาบาตตก', 'mage Z', 'a big fire explosion where a meteor hits the ground: frame 1 a white-hot flash on the ground, frames 2-3 a huge orange fireball blast with rocks and embers flying out, frames 4-5 a flat ring of fire and smoke spreading on the ground (a wide flat ellipse), frame 6 only glowing embers fading'),
 ('frost_nova', 'วงน้ำแข็ง', 'mage R', 'an ice nova bursting outward on the ground around a centre point: frame 1 a small bright ice-blue flash, frames 2-4 a ring of sharp ice crystals and frost mist spreading outward as a wide flat ellipse lying on the ground, frames 5-6 the ice shards sparkling and fading'),
 ('mana_shield', 'โล่เวท', 'mage X', 'a magic shield bubble: a see-through glowing teal sphere with a bright rim and faint floating hexagon runes, empty in the middle (a character stands inside it); a looping shimmer, the runes slowly drifting round'),
 ('blink', 'วาร์ป', 'mage F', 'a teleport flash: frame 1 a thin vertical teal light, frames 2-3 a burst of teal and white arcane sparks and small star shapes, frames 4-6 the sparks drifting up and fading'),
 ('ground_crack', 'รอยแยกพื้น', 'swordsman Q', 'a glowing crack splitting the ground, running from the LEFT edge to the RIGHT: frame 1 a short crack at the left, frames 2-4 the jagged crack racing to the right with orange-yellow light and small rock chunks bursting up along it, frames 5-6 the whole crack glowing then dimming. The crack lies flat on the ground (seen from a low top-down angle)'),
 ('whirlwind', 'พายุดาบ', 'swordsman E', 'a whirlwind of sword slashes: a wide flat ring of bright white-blue wind and blade streaks spinning round an empty centre, lying almost flat like an ellipse seen from a low top-down angle; a looping spin, the streaks in a different place each frame'),
 ('berserk', 'คลั่ง', 'swordsman X', 'a red rage aura: tall red and dark-red flames rising around an empty centre where a character stands, a few red sparks; a looping flicker, the flames rising and falling'),
 ('leap_slam', 'กระโดดทุบ', 'swordsman F', 'a heavy ground slam: frame 1 a white impact flash, frames 2-3 a shockwave ring of dust and light bursting outward as a wide flat ellipse on the ground with rock chunks flying up, frames 4-6 dust settling and fading'),
 ('spore_cloud', 'สปอร์เห็ด', 'mushroom attack', 'a puff of poison spores: frames 1-2 a small burst of purple and pale yellow spores, frames 3-5 a round drifting cloud of purple spore dust with tiny sparkles, frame 6 thin wisps fading'),
 ('ghost_fire', 'ไฟผี', 'lantern wisp + khamot shots', 'a ghost fire shot flying to the RIGHT: a ball of pale blue-white spirit flame with a wavy tail to the left and a faint skull-like shape in the flame; a looping flight, the flame flickering'),
 ('root_spikes', 'รากแทงพื้น', 'treant boss', 'thorny tree roots erupting from the ground: frame 1 the ground cracking, frames 2-3 sharp dark-brown roots with thorns stabbing up out of the ground in a cluster, frame 4 the roots at full height, frames 5-6 the roots sinking back into the ground'),
 ('water_wave', 'คลื่นน้ำ', 'Chalawan boss + phrai', 'a wave of river water rushing to the RIGHT along the ground: frame 1 a splash, frames 2-4 a curling wave of blue-green water with white foam surging forward, frames 5-6 the water spraying and falling apart'),
 ('steam', 'ไอน้ำระเบิด', 'mage reaction fire+ice', 'a steam explosion: frame 1 a bright white flash, frames 2-4 a big billowing burst of white steam with a little orange and ice-blue light inside, frames 5-6 the steam spreading thin and fading'),
 ('shatter', 'น้ำแข็งแตก', 'mage reaction ice+lightning', 'ice shattering: frame 1 a block of ice cracked with yellow lightning lines, frames 2-3 the ice exploding into many sharp ice shards flying outward with sparks, frames 4-6 the shards falling and sparkling out'),
 ('overload', 'ระเบิดสายฟ้า', 'mage reaction lightning+fire', 'an electric fire explosion: frame 1 a violet-white flash, frames 2-3 a round blast of orange fire laced with purple and yellow lightning arcs, frames 4-6 crackling sparks and smoke fading'),
]
def prompt(key, what):
    return ('Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: ' + what + '.\n'
            'Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.\n'
            'LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; '
            'the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.\n'
            'Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, '
            'no grid lines. Every frame must be clearly different.\n'
            'Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.')
if __name__ == '__main__':
    p = 'docs/codex/action/FX.md'
    done = set(re.findall(r'\| (\w+) \| done \|', open(p, encoding='utf-8').read())) if os.path.exists(p) else set()
    rows = '\n'.join(f'| {i + 1} | {k} | {"done" if k in done else "todo"} | {th} | {who} |' for i, (k, th, who, _) in enumerate(FX))
    body = '\n\n'.join(f'### {k} ({th}, {who})\nSave as `art/incoming/fx_codex/{k}.png`.\n```\n{prompt(k, w)}\n```' for k, th, who, w in FX)
    open(p, 'w', encoding='utf-8', newline='\n').write(f'''# Effects for the action game — queue for Codex

Owner 2026-11-09. Reply to the owner in Thai, short and plain.

## Rules
- ONE picture per row: one effect, 6 frames in a 3x2 grid on PURE BLACK (the game turns the black into see-through).
  No reference picture is needed.
- Save full size as `art/incoming/fx_codex/<key>.png`; one Thai line per file in `art/incoming/fx_codex/REPORT_TH.txt`.
- Mark the row `done` here. Work in the order of the queue; "ทำเอฟเฟคต่อ" = continue at the first `todo`.
- Branch `codex/fx`, commit, never merge, never push to `main`. Claude works in this same folder on `main`: when you stop,
  switch the folder back with `git checkout main`.

## Queue
| # | key | status | thai | for |
|---|-----|--------|------|-----|
{rows}

## Prompts
{body}
''')
    print(len(FX), 'effects,', len(done), 'done')
