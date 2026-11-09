# Animation frames for the action-game monsters, made by Codex (owner 2026-11-09 "เฟรมเจนเอา ให้ codex ทำ"; monsters are
# NOT made in PixelLab). One picture per monster per action: 6 frames in a 3x2 grid of 512 px cells on white, side view
# facing right (the game mirrors it for the left), the monster's own turnaround attached. Same recipe that worked for the
# legends (one action per picture, "every frame a clearly DIFFERENT pose", "Do ONLY this one picture now").
#   python tools/art/mob_anim.py        -> docs/codex/action/MOB_ANIM.md (queue + full prompts); keeps rows marked done
import re, os
MOB = {   # key: (thai, what it is, walk, attack, death)
 'shroom': ('เห็ดพิษ', 'the small grumpy purple-capped walking mushroom',
   'a bouncy waddle: it hops forward on its stubby legs, the cap squashing down on landing and stretching up on the hop',
   'it squashes down low, then springs up and puffs its cap forward to spit spores at the enemy in front of it, then settles back',
   'it gets hit, wobbles, its cap droops and it shrinks and flops over on its side, lying still in the last frame'),
 'wolf': ('หมาป่าเงา', 'the shadow wolf on four legs',
   'a fast trot on four legs, legs moving in a clear gait, the smoky tail swaying',
   'it crouches low on its front legs, then lunges forward with jaws wide open for a bite (the furthest reach in frame 4), then lands back in the ready stance',
   'it yelps and recoils, its legs buckle and it collapses onto its side, lying still in the last frame'),
 'goblin_archer': ('ก็อบลินนักธนู', 'the small goblin archer with the leaf hood and the short bow',
   'a sneaky quick walk, knees bent, the bow held low',
   'it pulls an arrow from the quiver, nocks it, draws the bow back and aims forward, releases (the arrow leaves the frame, the bowstring snaps forward in frame 4), then lowers the bow; arrows always point forward with the head at the front',
   'it gets hit, staggers back, drops the bow and falls on its back, lying still in the last frame'),
 'boar_guard': ('นักรบหมูป่า', 'the big boar-headed warrior with the round shield and spiked club',
   'a heavy stomping walk, shoulders rocking, the shield held in front, the club resting on the shoulder',
   'it raises the spiked club high overhead, then smashes it down hard in front of it (the club hits the ground in frame 4), then lifts it back up',
   'it gets hit, staggers, drops to one knee, the club and shield fall and it topples forward, lying still in the last frame'),
 'skeleton': ('ทหารโครงกระดูก', 'the skeleton soldier with the rusty helmet, cracked round shield and chipped sword',
   'a stiff rattling march, bones jerking a little at each step, shield held in front',
   'it pulls the sword back behind the shield, then steps in and slashes forward in a wide arc (the blade furthest forward in frame 4), then returns behind the shield',
   'it gets hit and falls apart: the bones come loose and collapse into a pile of bones with the helmet on top in the last frame'),
 'wisp': ('ภูตตะเกียง', 'the small floating hooded spirit holding a blue-flame lantern',
   'it floats forward, bobbing gently up and down, the ragged cloak tail rippling',
   'it rears back, then swings the lantern forward and thrusts it at the enemy (the lantern furthest forward in frame 4), then floats back',
   'it gets hit, flickers, the cloak crumples inward and collapses empty to the ground with the lantern lying beside it in the last frame'),
 'golem': ('โกเลมหิน', 'the big chunky mossy stone golem with the glowing teal rune',
   'a slow heavy walk, the whole body rocking from side to side at each step',
   'it pulls one huge stone fist far back, then punches forward hard with its whole weight (the fist furthest forward in frame 4), then pulls back to the ready stance',
   'it gets hit, cracks, the rune dims and it crumbles down into a heap of mossy stones in the last frame'),
 'boss_treant': ('บอสต้นไม้อสูร', 'the huge ancient tree giant boss',
   'a slow lumbering walk on its thick roots, branches swaying',
   'it rears back with both branch arms raised, then sweeps both thorny claws down and forward in front of it (the claws furthest forward in frame 4), then rises back up',
   'it gets hit, creaks and bends, then topples over and crashes to the ground, lying still in the last frame'),
 'krahang': ('ผีกระหัง', 'the Thai flying ghost with the winnowing-basket wings riding the rice pestle',
   'it flies forward on the pestle, flapping the two basket wings up and down in a clear flap cycle',
   'it pulls back, then dives forward on the pestle swinging both basket wings forward to strike (furthest forward in frame 4), then flies back up',
   'it gets hit, the baskets fly loose, it falls off the pestle and drops to the ground, lying still in the last frame'),
 'khamot': ('ผีโขมด', 'the floating ball of pale green ghost fire with the grinning face',
   'it floats forward bobbing up and down, the flame flickering and the flame tail trailing',
   'it shrinks and pulls back, then shoots forward stretching into a long fireball with a wide grin (furthest forward in frame 4), then snaps back to a round ball',
   'it gets hit, flickers, shrinks smaller and smaller and goes out into a last tiny wisp in the last frame'),
 'phrai': ('พรายน้ำ', 'the pale Thai river water spirit with very long dripping black hair',
   'a slow eerie glide forward, the long hair swaying, water dripping',
   'she leans back, then lunges forward reaching with both pale hands while her long hair whips forward (furthest reach in frame 4), then drifts back',
   'she gets hit, recoils, sinks down and melts into a puddle of water with her hair spread out in the last frame'),
 'pret': ('เปรต', 'the extremely tall thin Thai hungry ghost',
   'a slow swaying walk on long thin legs, the long arms hanging and swinging',
   'it bends down and reaches far forward with both very long thin arms to grab (furthest reach in frame 4), then straightens up',
   'it gets hit, folds up at the knees and collapses in a heap of long thin limbs, lying still in the last frame'),
 'monkey': ('ลิงโจร', 'the mischievous macaque bandit with the red headcloth and the bag of fruit',
   'a cheeky bouncy walk, tail swinging, the bag bouncing on the hip',
   'it pulls a fruit from the bag, winds up and throws it overhand forward (the fruit leaves its hand in frame 4), then laughs in the ready pose',
   'it gets hit, tumbles backward, fruit spilling from the bag, and lies still on its back in the last frame'),
 'croc_guard': ('ทหารจระเข้', 'the crocodile-headed warrior with the bronze armour and the long Thai glaive',
   'a heavy marching walk, the glaive held upright, the tail swaying behind',
   'it lowers the glaive and thrusts it forward with a step (the blade furthest forward in frame 4), then pulls it back upright',
   'it gets hit, staggers, drops the glaive and falls forward onto its belly, lying still in the last frame'),
 'boss_chalawan': ('บอสชาละวัน', 'Chalawan the crocodile king with the gold Thai crown and two curved swords',
   'a proud heavy walk, the long tail swaying, both swords held ready',
   'he raises both curved swords, then steps forward and slashes them down crossing in front of him (the swords furthest forward in frame 4), then returns to the ready stance',
   'he gets hit, roars, drops to his knees, the swords fall and he crashes onto his side, the crown rolling off, in the last frame'),
 'jiangshi': ('ผีกระโดดจีน', 'the Chinese hopping vampire with the talisman on its forehead',
   'it hops forward with both feet together, stiff body, arms stretched out in front, the talisman flapping at each hop',
   'it crouches, then makes a big stiff hop forward and claws down with both outstretched arms (the claws furthest forward in frame 4), then lands back',
   'it gets hit, the talisman flies off, it goes rigid and topples straight over backward like a plank, lying still in the last frame'),
 'paper_doll': ('ตุ๊กตากระดาษ', 'the small paper effigy servant',
   'it scurries forward in quick light steps, the paper sleeves fluttering',
   'it leans back, then lunges forward slicing with the paper fan (the fan furthest forward in frame 4), then pulls back',
   'it gets hit, tears, crumples up into a ball of paper and falls flat in the last frame'),
 'terracotta_archer': ('ทหารดินเผานักธนู', 'the clay soldier archer with the crossbow',
   'a stiff marching walk, the crossbow held across the body',
   'it raises the crossbow, aims forward, shoots (the bolt leaves the frame, the crossbow kicks back in frame 4), then lowers it; bolts always point forward with the head at the front',
   'it gets hit, cracks spread over its body and it crumbles into a pile of clay pieces in the last frame'),
 'terracotta_general': ('นายพลดินเผา', 'the big clay general with the bronze halberd',
   'a heavy slow march, the halberd held upright, the armour plates clacking',
   'it raises the halberd high, then swings it down and forward in a big chop (the blade furthest forward in frame 4), then lifts it back up',
   'it gets hit, cracks, drops the halberd and breaks apart into big clay chunks in the last frame'),
 'fox_spirit': ('ปีศาจจิ้งจอก', 'the white three-tailed fox demon',
   'a light prancing walk on its hind legs, the three tails swaying',
   'it raises one paw gathering blue fox-fire, then flicks the paw forward to throw it (the paw furthest forward in frame 4), then settles back',
   'it gets hit, yelps, spins and collapses onto its side, its tails limp, in the last frame'),
 'toad_demon': ('ปีศาจคางคก', 'the fat toad demon with the long tongue',
   'a heavy waddle forward, belly bouncing',
   'it puffs up its throat, then shoots its long sticky tongue straight forward (the tongue at full length in frame 4), then pulls it back in',
   'it gets hit, deflates, flops onto its back with its legs up, lying still in the last frame'),
 'boss_nian': ('บอสเหนียนโซ่ว', 'Nian, the huge red and gold New Year beast on four legs',
   'a heavy prowling walk on four legs, the mane bouncing',
   'it rears up on its hind legs, then slams down forward with both front paws and a roaring bite (furthest forward in frame 4), then steps back',
   'it gets hit, staggers, its legs give way and it slumps to the ground, lying still in the last frame'),
 'kappa': ('กัปปะ', 'the a small river kappa',
   'a waddling walk, the water in its head dish sloshing',
   'it lunges forward and slaps with a webbed hand (the hand furthest forward in frame 4), then hops back',
   'it gets hit, the water spills from its head dish, it wobbles and flops onto its shell, lying still in the last frame'),
 'kasa_obake': ('ร่มผี', 'the a haunted paper umbrella yokai',
   'it hops forward on its one leg, the umbrella bouncing open and shut a little',
   'it spins and lashes its long tongue forward (the tongue at full length in frame 4), then rolls it back',
   'it gets hit, the paper tears, it folds shut and topples over, lying still in the last frame'),
 'oni': ('ยักษ์โอนิ', 'the a big red oni ogre',
   'a heavy stomping walk, the club over its shoulder',
   'it raises the spiked club high and smashes it down in front of it (the club hits the ground in frame 4), then lifts it again',
   'it gets hit, staggers, drops the club and falls forward, lying still in the last frame'),
 'tengu': ('นกเทงงู', 'the a crow tengu',
   'a quick walk with the wings half spread, robes swaying',
   'it leaps forward with the wings spread and slashes down with the sword (the blade furthest forward in frame 4), then lands back',
   'it gets hit, feathers burst off, it falls to its knees and collapses onto its side, lying still in the last frame'),
 'rokurokubi': ('ผีคอยาว', 'the a long-necked rokurokubi ghost woman',
   'a slow shuffling walk, the long neck swaying the head left and right',
   'the long neck shoots forward and the head bites at the enemy in front (the head furthest forward in frame 4), then the neck pulls back',
   'she gets hit, the neck snaps back short, she sinks down and lies in a heap of kimono in the last frame'),
 'nekomata': ('แมวสองหาง', 'the a nekomata cat demon on its hind legs',
   'a sly prowling walk on its hind legs, both tails swishing',
   'it pounces forward swiping with both claws (the claws furthest forward in frame 4), then lands crouched',
   'it gets hit, yowls, rolls over and lies still with its tails limp in the last frame'),
 'boss_orochi': ('บอสยามาตะโนะโอโรจิ', 'the the boss',
   'its coils slide forward, the heads swaying',
   'the heads rear back then strike forward together (the heads furthest forward in frame 4), then pull back',
   'it gets hit, the heads droop one by one and the body slumps into a still coil in the last frame'),
 'mummy': ('มัมมี่', 'the a shambling mummy',
   'a slow stiff shamble, arms forward, loose bandages swaying',
   'it lurches forward and swipes with both bandaged arms (furthest forward in frame 4), then steps back',
   'it gets hit, the bandages unravel and it collapses into a pile of bandages and dust in the last frame'),
 'scarab': ('ด้วงสการับ', 'the a big glossy scarab beetle',
   'a quick scuttling walk on six legs',
   'it rears up and charges forward snapping its mandibles (furthest forward in frame 4), then backs off',
   'it gets hit, flips onto its back with its legs curled, lying still in the last frame'),
 'jackal_warrior': ('นักรบหัวหมาจิ้งจอก', 'the a jackal-headed warrior (a soldier, not a god)',
   'a disciplined marching walk, the shield held in front',
   'it steps in and slashes forward with the khopesh (the blade furthest forward in frame 4), then guards again',
   'it gets hit, drops the khopesh and falls to the ground, lying still in the last frame'),
 'sand_scorpion': ('แมงป่องทะเลทราย', 'the a big desert scorpion',
   'it scuttles forward on eight legs, the tail swaying',
   'it raises its tail high and stabs the stinger down forward (the stinger furthest forward in frame 4), then lifts it again',
   'it gets hit, curls up its legs and tail and lies still in the last frame'),
 'cobra_priest': ('นักบวชงูเห่า', 'the a cobra-hooded serpent priest',
   'it slithers forward upright, the hood flaring',
   'it raises the staff and thrusts it forward casting (the staff furthest forward in frame 4), then lowers it',
   'it gets hit, the hood folds and it coils down onto the ground, lying still in the last frame'),
 'sand_golem': ('โกเลมทราย', 'a big golem made of packed desert sand and sandstone blocks, carved hieroglyph patterns on its chest glowing amber, sand trickling from its joints',
   'a heavy slow walk, sand spilling at each step',
   'it swings a huge sandstone fist forward (the fist furthest forward in frame 4), then pulls back',
   'it gets hit, cracks and crumbles into a pile of sand and blocks in the last frame'),
 'boss_sphinx': ('บอสสฟิงซ์', 'the the boss',
   'a heavy prowling walk on four legs, sand pouring',
   'it rears up and slams both front paws down forward (the paws hit the ground in frame 4), then steps back',
   'it gets hit, cracks spread and it slumps down into a heap of sandstone in the last frame'),
 'draugr': ('ดรากร์', 'the a draugr',
   'a stiff heavy march, frost drifting off its body',
   'it raises the axe and chops down forward (the axe furthest forward in frame 4), then lifts it again',
   'it gets hit, the glow in its eyes fades and it crumbles to the ground, lying still in the last frame'),
 'frost_wolf': ('หมาป่าหิมะ', 'the a frost wolf',
   'a fast trot on four legs, snow puffing at its paws',
   'it crouches then lunges with jaws open for a bite (the furthest reach in frame 4), then lands back',
   'it gets hit, yelps, its legs buckle and it collapses onto its side, lying still in the last frame'),
 'troll': ('โทรลล์', 'the a big mountain troll',
   'a lumbering walk, the club dragging',
   'it lifts the tree-trunk club and swings it down in a big arc in front (the club hits the ground in frame 4), then lifts it again',
   'it gets hit, staggers and falls over backward, lying still in the last frame'),
 'ice_wraith': ('วิญญาณน้ำแข็ง', 'the a floating ice wraith',
   'it floats forward bobbing, snowflakes swirling',
   'it rears back then slashes forward with its icy claws (the claws furthest forward in frame 4), then floats back',
   'it gets hit, shatters into ice shards and snowflakes that fall and fade in the last frame'),
 'dwarf_berserker': ('คนแคระคลั่ง', 'the a wild dwarf berserker',
   'a fast angry stomping walk, the axes swinging',
   'it spins and chops with both axes forward (the axes furthest forward in frame 4), then stops',
   'it gets hit, drops the axes and topples onto its back, lying still in the last frame'),
 'ice_golem': ('โกเลมน้ำแข็ง', 'a big golem of blue glacier ice and black rock, frost mist rising from it, a glowing cold-blue core in its chest',
   'a heavy slow walk, frost mist trailing',
   'it swings a huge ice fist forward (the fist furthest forward in frame 4), then pulls back',
   'it gets hit, cracks and shatters into ice chunks in the last frame'),
 'boss_jotun': ('บอสยักษ์น้ำแข็ง', 'the the boss',
   'a slow thunderous walk, frost cracking under its feet',
   'it raises the ice hammer high and slams it down in front (the hammer hits the ground in frame 4), then lifts it',
   'it gets hit, falls to its knees and crashes forward, lying still in the last frame'),
}
ACT = {
 'walk': 'Action: {w}. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).',
 'attack': 'Action: {a}. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.',
 'death': 'Action: {d}.',
 'hurt': 'Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.',
}
def prompt(key, act):
    th, what, w, a, d = MOB[key]
    return (f'Animation frames for a 2D action game, ONE picture. The monster is {what}, exactly as in the attached picture: same face, '
            f'colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).\n'
            f'Side view facing RIGHT in every frame, like the middle view of the attached picture.\n'
            + ACT[act].format(w=w, a=a, d=d) + '\n'
            'LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size '
            'with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.\n'
            'Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every '
            'cell. Every frame must be a clearly DIFFERENT pose.\n'
            'Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, '
            'no dust.\nPicture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.')
JOBS = [(k, a) for k in MOB for a in ('walk', 'attack', 'death', 'hurt')]
if __name__ == '__main__':
    p = 'docs/codex/action/MOB_ANIM.md'
    done = set(re.findall(r'\| (\w+) \| (walk|attack|death|hurt) \| done \|', open(p, encoding='utf-8').read())) if os.path.exists(p) else set()
    rows = '\n'.join(f'| {i + 1} | {k} | {a} | {"done" if (k, a) in done else "todo"} | `art/incoming/mobs/anim/{k}_{a}.png` |' for i, (k, a) in enumerate(JOBS))
    body = '\n\n'.join(f'### {k} {a} ({MOB[k][0]})\nAttach `art/incoming/mobs/{k}.png`.\n```\n{prompt(k, a)}\n```' for k, a in JOBS)
    open(p, 'w', encoding='utf-8', newline='\n').write(f'''# Monster animation frames (action game) — queue for Codex

Owner 2026-11-09: the monsters' frames are made by Codex (not PixelLab). Reply to the owner in Thai, short and plain.

## Rules
- ONE picture per row of the queue: one monster, one action, 6 frames in a 3x2 grid on white. Attach the monster's own
  turnaround `art/incoming/mobs/<key>.png` every time (it is the reference for face, colours and size).
- Save full size as `art/incoming/mobs/anim/<key>_<action>.png`; add one Thai line per file to
  `art/incoming/mobs/anim/REPORT_TH.txt` (anything that came out wrong: a frame crossing a cell, a turned view, a missing frame).
- Mark the row `done` here. Work in the order of the queue; when the owner says "ทำเฟรมมอนต่อ", continue at the first `todo`.
- Branch `codex/mob-anim`, open a pull request, never merge, never push to `main`. Claude works in this same folder on
  `main`: when you stop, switch the folder back with `git checkout main` so the other agent's work does not land on your branch.

## Queue
| # | key | action | status | file |
|---|-----|--------|--------|------|
{rows}

## Prompts
{body}
''')
    print(len(JOBS), 'jobs,', len(done), 'done')
