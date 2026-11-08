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
plan = [('idle', D8, 8, False), ('run', D8, 8, False), ('attack', ['east', 'south', 'north', 'north-east', 'north-west'], 16, True),
        ('roll', D8, 8, True), ('hurt', D8, 4, True), ('death', ['east', 'south', 'west', 'north'], 8, True)]
jobs = [{'anim': a, 'dir': d, 'frames': n, 'keep': keep, 'subject': H['subj'], 'pose': H['pose'],
         'action': H[a] + ' ' + FACE[d].format(b=H['back']) + END} for a, dirs, n, keep in plan for d in dirs]
print(json.dumps(jobs, indent=1, ensure_ascii=False))
