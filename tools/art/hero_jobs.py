# Base moves (no skills) for a new action-game hero, as a job list for tools/pl_queue.py. Owner 2026-11-09: swordsman +
# mage "เอาท่าจำเป็นก่อน สกิลยังไม่ต้อง". Same recipe as the rogue's jobs_base.json (idle / run 8 dirs looped, roll / hurt
# 8 dirs, death E S W N) plus the 2-hit attack in E S N NE NW (16 frames; SE / SW / W play east, mirrored where needed).
#   python tools/art/hero_jobs.py <swordsman|mage> > art/incoming/action/<key>/jobs_base.json
import sys, json
K = sys.argv[1]
H = {
 'swordsman': dict(
   subj='a young man swordsman with a big two-handed greatsword, a long red scarf, a steel-blue tunic',
   pose='relaxed standing pose, the greatsword resting on his right shoulder',
   back='his back, his red scarf and the back of his head',
   idle='a calm breathing idle in a ready stance: shoulders rising and falling slightly, the red scarf swaying gently, the greatsword resting on his right shoulder; a seamless loop, feet stay planted.',
   run='a strong running cycle in place (he does not travel across the frame): the greatsword stays resting on his right shoulder, his left arm pumping, knees lifting, the red scarf streaming behind him; a smooth loop where the last frame flows back into the first.',
   roll='a quick dodge roll forward, in place (he stays in the middle of the frame): he crouches, tucks into a ball holding the greatsword close and rolls over along the ground, then springs back up into the standing pose with the sword back on his shoulder.',
   hurt='he gets hit: a sharp flinch, head and shoulders jerk back, then he recovers to the standing pose.',
   death='he is defeated: he staggers, drops to his knees, the greatsword falls beside him and he collapses to the ground, lying still in the last frames.',
   attack='a heavy two-hit greatsword combo: he swings the greatsword off his shoulder in a big wide horizontal sweep in front of him with a step forward (hit 1), then lifts it high overhead with both hands and slams it straight down in front of him (hit 2), then brings it back up onto his right shoulder.'),
 'mage': dict(
   subj='a young man mage in a deep indigo hooded robe with a short teal cape, holding a tall wooden staff with a teal crystal',
   pose='relaxed standing pose, the staff held upright in his right hand',
   back='his back, his hood and teal cape',
   idle='a calm breathing idle: shoulders rising and falling slightly, the robe and short cape swaying gently, the staff held upright in his right hand; a seamless loop, feet stay planted.',
   run='a light running cycle in place (he does not travel across the frame): the staff held in his right hand and angled forward, his left arm pumping, knees lifting under the robe, the robe hem and the cape bouncing; a smooth loop where the last frame flows back into the first.',
   roll='a quick dodge roll forward, in place (he stays in the middle of the frame): he crouches, tucks into a ball holding the staff close to his body and rolls over along the ground, then springs back up into the standing pose with the staff upright.',
   hurt='he gets hit: a sharp flinch, head and shoulders jerk back, then he recovers to the standing pose.',
   death='he is defeated: he staggers, drops to his knees, the staff falls beside him and he collapses to the ground, lying still in the last frames.',
   attack='a two-cast magic attack with the staff: he draws the staff back, then thrusts it forward pointing the crystal at the enemy in front of him (cast 1), pulls it back, swings it forward in a short arc and points it at the enemy again (cast 2), then returns to the standing pose with the staff upright. Only his body and the staff move: no magic, no projectiles, no glow.'),
 'priest': dict(
   subj='a young woman priestess with long wavy light-brown hair under a white hood, a white and gold robe with blue trim and a gold sun emblem, holding a long staff topped with a gold sun ring and a small bell',
   pose='relaxed standing pose, the staff held upright in her right hand',
   back='her back, her white hood, her long hair and the back of the robe',
   idle='a calm breathing idle: shoulders rising and falling slightly, the robe, hood and long hair swaying gently, the staff held upright in her right hand; a seamless loop, feet stay planted.',
   run='a light running cycle in place (she does not travel across the frame): the staff held in her right hand and angled forward, her left arm pumping, knees lifting under the robe, the robe hem and hair bouncing; a smooth loop where the last frame flows back into the first.',
   roll='a quick dodge roll forward, in place (she stays in the middle of the frame): she crouches, tucks into a ball holding the staff close to her body and rolls over along the ground, then springs back up into the standing pose with the staff upright.',
   hurt='she gets hit: a sharp flinch, head and shoulders jerk back, then she recovers to the standing pose.',
   death='she is defeated: she staggers, drops to her knees, the staff falls beside her and she collapses to the ground, lying still in the last frames.',
   attack='a two-cast holy attack with the staff: she draws the staff back, then thrusts it forward pointing the sun ring at the enemy in front of her (cast 1), pulls it back, swings it forward in a short arc and points it at the enemy again (cast 2), then returns to the standing pose. Only her body and the staff move: no magic, no glow.'),
 'archer': dict(
   subj='a young woman archer with a long brown ponytail, a green hooded short cape, a wooden recurve bow in her LEFT hand and a quiver on her back',
   pose='relaxed standing pose, the bow held low in her left hand',
   back='her back, her ponytail, her green cape and the quiver',
   idle='a calm breathing idle: shoulders rising and falling slightly, the ponytail and short cape swaying gently, the bow held low in her left hand; a seamless loop, feet stay planted.',
   run='a light running cycle in place (she does not travel across the frame): the bow held in her left hand, her right arm pumping, knees lifting, the ponytail and cape bouncing; a smooth loop where the last frame flows back into the first.',
   roll='a quick dodge roll forward, in place (she stays in the middle of the frame): she crouches, tucks into a ball holding the bow close and rolls over along the ground, then springs back up into the standing pose.',
   hurt='she gets hit: a sharp flinch, head and shoulders jerk back, then she recovers to the standing pose.',
   death='she is defeated: she staggers, drops to her knees, the bow falls beside her and she collapses to the ground, lying still in the last frames.',
   attack='a lively single bow shot with the whole body moving: she reaches back and pulls one arrow from the quiver, nocks it, raises the bow and leans into the shot as she draws the string back to her cheek, releases (the arrow flies away out of the frame, the string snaps forward and her body rocks back a little), follows through with the bow arm, then lowers the bow back to the standing pose. The arrow points the right way: arrowhead at the front, feathers at the back.',
   crit='a powerful critical shot in a different pose: she drops into a low kneeling stance on one knee, tilts the bow, draws the string to full extent with her whole body coiled, holds for a beat, releases a heavy shot with a strong recoil that rocks her body back, then rises back to the standing pose. The arrow points the right way: arrowhead at the front, feathers at the back.'),
}[K]
FACE = {
 'east': 'Side view facing right, keep the same side-on angle in every frame.',
 'south-east': 'He faces down-right, toward the camera and to the right (three-quarter front view) the whole time; keep the same facing in every frame.',
 'south': 'He faces straight toward the camera (front view) the whole time; keep the same facing in every frame.',
 'south-west': 'He faces down-left, toward the camera and to the left (three-quarter front view) the whole time; keep the same facing in every frame.',
 'west': 'Side view facing left, keep the same side-on angle in every frame.',
 'north-west': 'Seen from BEHIND the whole time, facing up-left (three-quarter back view): we see only {b}, his face is never visible, he never turns around.',
 'north': 'Seen from BEHIND the whole time, straight back view: we see only {b}, his face is never visible, he never turns around.',
 'north-east': 'Seen from BEHIND the whole time, facing up-right (three-quarter back view): we see only {b}, his face is never visible, he never turns around.',
}
END = ' No effects, no smoke, no dust, no motion trails.'
D8 = ['east', 'south-east', 'south', 'south-west', 'west', 'north-west', 'north', 'north-east']
plan = [('idle', D8, 8, False), ('run', D8, 8, False), ('attack', ['east', 'south', 'north', 'north-east', 'north-west'], 16, True)] + ([('crit', ['east', 'south', 'north', 'north-east', 'north-west'], 16, True)] if K == 'archer' else []) + [(
'roll', D8, 8, True), ('hurt', D8, 4, True), ('death', ['east', 'south', 'west', 'north'], 8, True)]
# skill moves (owner 2026-11-09 "เจนมา" after the skill plan): python tools/art/hero_jobs.py <key> skills
SKM = {
 'swordsman': dict(
   spin='a whirlwind spin attack: he holds the greatsword straight out to the side with both hands and spins round on the spot in one full turn, the blade sweeping a full circle around him; a smooth loop where the last frame flows back into the first.',
   leap='a leaping slam: he crouches low, jumps high with the greatsword raised overhead in both hands, comes down and slams the blade into the ground in front of him, then rises back up with the sword on his shoulder. He jumps straight up and lands on the same spot (he stays in the middle of the frame).',
   guard='a parry guard: he swings the greatsword off his shoulder and holds it upright in front of his body with both hands like a shield, braced in a wide stance, and holds that guard.',
   charge='charging a heavy strike: he sinks into a wide low stance and pulls the greatsword back low behind him with both hands, gathering power, and holds that coiled pose with the sword trembling slightly.'),
 'priest': dict(
   pray='a holy prayer: she lifts the staff high above her head with both hands, the sun ring pointing at the sky, tilts her face up and holds it for a moment, then brings it back down to the standing pose. Only her body and the staff move: no magic, no glow.',
   bless='a blessing: she holds the staff upright in front of her and rings the little bell with a gentle shake, her free hand raised with the palm open, then returns to the standing pose. Only her body and the staff move: no magic, no glow.'),
 'mage': dict(
   cast_up='casting a big spell: he raises the staff high above his head with both hands, the crystal pointing at the sky, holds it up for a moment, then brings it back down to the standing pose. Only his body and the staff move: no magic, no glow.',
   staff_slam='a ground spell: he lifts the staff and strikes its bottom end down hard onto the ground in front of him, then returns to the standing pose with the staff upright. Only his body and the staff move: no magic, no glow.'),
}
SPLAN = {'swordsman': [('spin', ['south'], 8, False), ('leap', ['east', 'south', 'north', 'north-west'], 16, True),
                       ('guard', ['east', 'south', 'north', 'north-west'], 4, True), ('charge', ['east', 'south', 'north', 'north-west'], 8, True)],
         'priest': [('pray', ['east', 'south', 'north', 'north-west'], 8, True), ('bless', ['east', 'south', 'north', 'north-west'], 8, True)],
         'mage': [('cast_up', ['east', 'south', 'north', 'north-west'], 8, True), ('staff_slam', ['east', 'south', 'north', 'north-west'], 8, True)]}
if len(sys.argv) > 2 and sys.argv[2] == 'skills':
    H.update(SKM[K]); plan = SPLAN[K]
jobs = [{'anim': a, 'dir': d, 'frames': n, 'keep': keep, 'subject': H['subj'], 'pose': H['pose'],
         'action': H[a] + ' ' + FACE[d].format(b=H['back']) + END} for a, dirs, n, keep in plan for d in dirs]
print(json.dumps(jobs, indent=1, ensure_ascii=False))
