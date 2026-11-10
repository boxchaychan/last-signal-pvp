# A VFX library made from videos, like the effect packs sold for games (owner 2026-11-10: "เอาแบบ 1 [the cartoon look of the
# Meta AI explosion, thick black ink lines] เขียนพรอมต์ดีๆ ทำ VFX เก็บไว้แบบที่เค้าทำขาย ให้มันได้ทุกทิศ แมพเรา 3D").
# Every effect is one of three kinds, so it works in any direction in the 3D map:
#   B upright, the same from every side (bursts, pillars, auras): the game shows it facing the camera (a billboard)
#   D flat on the ground, shot from straight above: the game lays it on the ground and turns it to any direction
#   S travels or swings to the RIGHT in side view: the game turns / mirrors it toward the target
#   python3 tools/art/vfx_pack.py   -> docs/vfx-pack.html (copy buttons; cut the clips with vfxcut.html or tools/video/vfx_cut.py)
import html

STYLE = ('2D cartoon game VFX in a bold hand-drawn style, like a premium mobile-game effect pack: thick clean black ink outlines '
         'round every shape, flat cel-shaded colours in 2-3 tones per colour, bright saturated colours, puffy round cartoon smoke '
         'clouds, sharp spiky sparks, crisp readable shapes, smooth animation.')
KIND = {
  'B': ('Camera: seen from the front, a little from above; the effect stands upright and looks the same from every side.',
        'ตั้งขึ้น หน้าตาเหมือนกันทุกด้าน เกมหันให้เข้ากล้องเอง ใช้ได้ทุกทิศ'),
  'D': ('Camera: straight down from directly above (top view, 90 degrees); the effect lies FLAT on the ground and is drawn as '
        'seen from above, so a game can lay it on the ground and turn it to any direction.',
        'แบนราบบนพื้น ถ่ายจากด้านบนตรงๆ เกมวางลงพื้นแล้วหมุนไปทิศไหนก็ได้'),
  'S': ('Camera: pure side view; the effect moves or swings from LEFT to RIGHT, so a game can turn it toward any target.',
        'วิ่ง/ฟันจากซ้ายไปขวา เกมหมุนหรือกลับด้านให้ชี้ไปหาเป้าเอง'),
}
# owner 2026-11-10 "ทำไมล้นกรอบ": Meta AI ignores sizes written as fractions and zooms in to fill the frame; a start picture
# with a small spark in the middle (art/incoming/action/berserker/video_start/start_fx_spark.png) plus these words keep it small.
# The size IN THE GAME is set by tools/video/vfx_cut.py (SIZE), not by the video.
WIDE = ('EXTREME WIDE SHOT, zoomed far out: the camera is very far away, the effect is tiny in the centre of the frame and starts '
        'from the small spark in the attached picture. At its biggest moment the whole effect still fits inside the middle third of '
        'the frame, with a lot of empty green space all round it.')
GREEN, MAGENTA = 'flat pure green (#00FF00)', 'flat pure magenta (#FF00FF)'
END = {'once': 'Quick build-up, a strong burst, then it fades out completely and the video ends on the empty background.',
       'loop': 'It LOOPS seamlessly: no fade-out, the last frame matches the first.'}

# Class sets first (owner 2026-11-10 "แยกเป็นของตัวละคร อาชีพก่อน"): each class has its own colour line added to every prompt
G = GREEN
CLASSES = [
 ('berserker', 'เบอร์เซิร์กเกอร์', 'Colours ONLY black, glowing NEON RED and red-orange fire: black ink shapes and black smoke, neon red glowing rims and light, small red-orange fire cores; no yellow, no blue, no green, no purple.', [
  ('bz_hit', 'โดนฟัน (ตีธรรมดา)', 'B', 1, 'once', 'small: one fifth of the picture wide', 'a heavy greatsword hit impact: a black jagged starburst with a neon red rim and a hot red-orange core, sharp black-red spikes and red sparks flying out', G),
  ('bz_swing', 'รอยดาบใหญ่ (ตีธรรมดา)', 'S', 1, 'once', 'half of the picture wide', 'one huge heavy greatsword swing from left to right: a THICK black crescent trail with a glowing neon red edge, red-orange fire flickering along it, red sparks flung off the tip', G),
  ('bz_chain_all', 'Q โซ่ดึงรอบตัว (โซ่)', 'D', 2, 'once', 'the chains reach half of the picture wide', 'seen from above: from an empty spot in the middle, many black chains with glowing neon red links shoot out in ALL directions like a star (360 degrees), their hooks bite with red sparks, then all the chains yank back into the middle at once, dragging red light streaks', G),
  ('bz_chain_ring', 'Q โซ่ดึงรอบตัว (วงฟัน)', 'D', 1.5, 'once', 'a ring half of the picture wide', 'seen from above: a thick black ring slash with a neon red edge sweeps all the way round an empty centre, red sparks flung outward, then it breaks apart into black smoke and red embers', G),
  ('bz_triple', 'E ฟาดสามยมทูต', 'S', 2, 'once', 'half of the picture wide', 'three heavy greatsword slashes one after another: a wide black crescent with a neon red edge from right to left, a wider one from left to right, then a downward blow on the right that splits the ground with neon red cracks and fire; each trail breaks into black smoke and red embers', G),
  ('bz_slam', 'R / F ทุบพื้น (ระเบิด)', 'B', 2.5, 'once', 'the blast about one third of the picture wide and as tall', 'a brutal ground-slam blast: a red flash, a puffy explosion of black smoke clouds with neon red glowing rims and a red-orange fire core, black rock chunks thrown up, red embers, then the smoke thins away', G),
  ('bz_slam_ring', 'R / F ทุบพื้น (คลื่นบนพื้น)', 'D', 2, 'once', 'a ring growing to half of the picture wide', 'seen from above: a thick black shockwave ring with a neon red edge racing outward on the ground, jagged neon red cracks spreading from the centre like a spider web, black rock pieces, then the cracks glow like lava and fade', G),
  ('bz_crack_line', 'R ชาร์จฟัน (รอยแยกพุ่ง)', 'D', 2, 'once', 'a line across half of the picture', 'seen from above: a crack in the ground tearing from LEFT to RIGHT, neon red light and red-orange fire bursting up along it, black rock shards popping, then it cools to black', G),
  ('bz_shackle', 'Z ตรวนนรก', 'D', 2.5, 'once', 'a circle one third of the picture wide', 'seen from above: a glowing neon red rune circle on the ground, black chains with red-hot glowing links bursting out of it, crossing over the middle and pulling tight, red light pulsing along the links, then they crumble into black smoke', G),
  ('bz_rage', 'X ร่างคลั่งโลหิต (ออร่า)', 'B', 3, 'loop', 'a column one fifth wide, half tall', 'a berserk rage aura round an empty spot where a fighter stands: black smoke and neon red flames rising like a burning column, glowing red cracks of light flickering, red embers drifting up, a crimson pulse every second', G),
  ('bz_wave', 'X คลื่นฟัน (ตอนคลั่ง)', 'S', 1.5, 'once', 'the crescent one fifth of the picture tall', 'a slash wave flying from left to right: a thick black crescent with a glowing neon red rim and red-orange fire, speed lines behind, then it breaks into red sparks and black smoke', G),
  ('bz_hook', 'F โซ่กระชาก', 'S', 1.5, 'once', 'a line across two thirds of the picture', 'a black chain with a hooked claw and glowing neon red links shooting from the left to the right and biting into the ground with a red flash and a small black-red burst', G),
 ]),
 ('berserker_parts', 'เบอร์เซิร์กเกอร์ · ชิ้นส่วน (ประกอบเป็นสกิลด้วยโค้ด)', 'Colours ONLY black, glowing NEON RED and red-orange fire: black ink shapes and black smoke, neon red glowing rims and light, small red-orange fire cores; no yellow, no blue, no green, no purple.', [
  # owner 2026-11-10 "ทำแค่อันเดียวแล้วให้ทำตามทิศทาง ไม่เอาสกิลเป็นก้อน": like game VFX artists, small single pieces; the game turns,
  # stretches, repeats and moves them toward each target (a particle system), so every skill follows its direction
  ('bzp_slash', 'ชิ้น: รอยฟัน 1 เส้น', 'S', 0.8, 'once', 'one third of the picture wide', 'ONE single curved greatsword slash crescent swinging from left to right, a thick black trail with a neon red edge, then it thins and vanishes; nothing else', G),
  ('bzp_hit', 'ชิ้น: ประกายโดนตี', 'B', 0.6, 'once', 'small: one sixth of the picture wide', 'ONE small hit flash: a jagged black-red star burst with a hot core and a few sharp spikes, then it vanishes; nothing else', G),
  ('bzp_boom', 'ชิ้น: ระเบิดลูกเดียว', 'B', 1.2, 'once', 'one quarter of the picture wide', 'ONE round explosion puff: a red flash, a ball of red-orange fire wrapped in black smoke, then it breaks up and fades; nothing else', G),
  ('bzp_smoke', 'ชิ้น: ควันก้อนเดียว', 'B', 1.5, 'once', 'one sixth of the picture wide', 'ONE single puffy black cartoon smoke cloud with a thin red rim, rising a little, swelling, then thinning away; nothing else', G),
  ('bzp_sparks', 'ชิ้น: ประกายไฟกระเด็น', 'B', 1, 'once', 'one quarter of the picture wide', 'a small spray of red-hot sparks and embers flying out from one point and falling, then gone; nothing else', G),
  ('bzp_flame', 'ชิ้น: เปลวไฟ 1 ดวง (วนซ้ำ)', 'B', 1.5, 'loop', 'small: one sixth of the picture wide', 'ONE single neon red flame with a black outline and an orange core, flickering on the spot; nothing else', G),
  ('bzp_crack', 'ชิ้น: รอยแตกพื้นเส้นเดียว', 'D', 1.5, 'once', 'one straight crack across half of the picture', 'seen from above: ONE straight crack in the ground opening from the LEFT end to the RIGHT end, glowing neon red inside, then it cools to black and fades; nothing else', G),
 ]),
 ('swordsman', 'นักดาบ', 'Colours: deep crimson red and orange fire with white-hot cores, dark red-black outlines, a few gold sparks.', [
  ('sw_hit', 'โดนฟัน', 'B', 1, 'once', 'small: one fifth of the picture wide', 'a sword hit impact: an orange-red starburst with a white-hot core, sharp sparks and a few gold sparks', G),
  ('sw_swing', 'รอยดาบ', 'S', 1, 'once', 'half of the picture wide', 'a fast sword swing from left to right: a crimson crescent trail with a white-hot edge, small flames along it, sparks off the tip', G),
  ('sw_crack', 'Q ฟาดแยกพื้น', 'D', 2, 'once', 'a line across half of the picture', 'seen from above: a glowing crack tearing along the ground from LEFT to RIGHT, orange fire bursting up along it, rocks popping, smoke at the far end', G),
  ('sw_spin', 'E พายุดาบ', 'D', 1.5, 'loop', 'a ring half of the picture wide', 'seen from above: a whirlwind of crimson sword slash arcs spinning round an empty centre, embers and sparks flung outward', G),
  ('sw_charge', 'R ชาร์จฟัน', 'S', 2, 'once', 'half of the picture wide', 'red energy gathering in three rising pulses on the left, then one huge wide crescent slash sweeping to the right, a long crimson arc with a white-hot edge breaking into embers', G),
  ('sw_slam', 'F กระโดดทุบ', 'B', 2, 'once', 'one third of the picture wide', 'a heavy landing blow: a white flash, an orange fire burst with dark smoke, rocks and dirt thrown up', G),
  ('sw_slam_ring', 'F กระโดดทุบ (วงบนพื้น)', 'D', 2, 'once', 'a ring growing to half of the picture wide', 'seen from above: a shockwave ring racing out on the ground, glowing orange cracks spreading from the centre, dust round it', G),
  ('sw_parry', 'Z ตั้งรับสวน', 'B', 1.2, 'once', 'one quarter wide', 'a parry clash: a bright red-gold flash and a ring of sparks, then one sharp crimson counter-slash crescent', G),
  ('sw_rage', 'X คลั่ง (ออร่า)', 'B', 3, 'loop', 'a column one fifth wide, half tall', 'a fighting rage aura round an empty spot: red-orange flames rising, red-black smoke, embers drifting up', G),
 ]),
 ('guardian', 'อัศวินโล่', 'Colours: polished steel silver and white with a royal blue glow and small gold accents.', [
  ('gd_hit', 'โดนฟัน', 'B', 1, 'once', 'small: one fifth wide', 'a sword hit impact: a white-silver starburst with a blue glow and sharp steel sparks', G),
  ('gd_swing', 'รอยดาบยาว', 'S', 1, 'once', 'half of the picture wide', 'a long-sword swing from left to right: a wide silver-white crescent with a blue glowing edge, small white sparks', G),
  ('gd_bash', 'กระแทกโล่', 'B', 1.2, 'once', 'one quarter wide', 'a shield bash impact: a round blue-white shockwave burst with a gold rim, steel sparks', G),
  ('gd_block', 'Z ยกโล่สวน', 'B', 1.5, 'once', 'one quarter wide', 'a shield block: a curved wall of blue light with a hexagon pattern flashing in front, sparks bouncing off, then a white counter-slash', G),
  ('gd_slam_ring', 'F กระโดดทุบ (วงบนพื้น)', 'D', 2, 'once', 'a ring growing to half of the picture wide', 'seen from above: a blue-white shockwave ring on the ground with gold glints, stone cracks, dust', G),
 ]),
 ('rogue', 'นักมีด', 'Colours: black ink-like strokes with a thin glowing NEON PURPLE rim and a soft violet glow, a shadow-ninja look.', [
  ('rg_hit', 'โดนแทง', 'B', 1, 'once', 'small: one fifth wide', 'a quick dagger hit: a small black-purple X spark with neon purple rims', G),
  ('rg_knife', 'Q ปามีด', 'S', 1, 'once', 'a line across half of the picture', 'a spinning black throwing knife flying left to right with a neon purple streak, a small purple burst at the end', G),
  ('rg_storm', 'E พายุใบมีด', 'D', 1.5, 'loop', 'a ring half of the picture wide', 'seen from above: many small black blades with purple rims spinning round an empty centre in a whirl, purple slash streaks', G),
  ('rg_smoke', 'R ระเบิดควัน', 'B', 2.5, 'once', 'one third of the picture wide, low', 'a smoke bomb: a small dark flash then thick black-purple cartoon smoke billowing into a wide low cloud, then thinning out', G),
  ('rg_dash', 'F พุ่งฟัน', 'S', 1, 'once', 'a line across half of the picture', 'a lightning-fast dash slash: a long black streak with a neon purple edge zipping from left to right, a sharp X cut flash at the end', G),
  ('rg_vanish', 'Z ล่องหน', 'B', 1.5, 'once', 'one fifth wide', 'vanishing: black-purple smoke and shadow wisps wrapping round an empty spot and collapsing inward, a few purple sparks, then nothing', G),
  ('rg_venom', 'X มีดพิษ (ระเบิดพิษ)', 'B', 1.5, 'once', 'one quarter wide', 'a poison burst: purple-green toxic bubbles swelling and splashing out in drops and a ring of venom mist', MAGENTA),
 ]),
 ('archer', 'นักธนู', 'Colours: black ink-like strokes with a thin glowing NEON GREEN rim and a soft green glow.', [
  ('ar_hit', 'ลูกธนูโดน', 'B', 1, 'once', 'small: one fifth wide', 'an arrow hit: a small black-green star spark with neon green rims', MAGENTA),
  ('ar_shot', 'Q ยิงรัว', 'S', 1, 'once', 'a line across half of the picture', 'a fast arrow streak from left to right: a thin black arrow with a neon green trail, a tiny green burst at the end', MAGENTA),
  ('ar_bolt', 'E ลูกพลังเขียว', 'S', 1.5, 'once', 'the bolt one tenth wide', 'a glowing green energy bolt flying left to right with a swirling trail, bursting into a green star blast', MAGENTA),
  ('ar_charge', 'R ชาร์จง้าง', 'S', 1.5, 'once', 'half of the picture wide', 'a charged shot: green light gathering on the left, then a thick piercing beam-arrow shooting to the right with rings of green light round it', MAGENTA),
  ('ar_bomb', 'F ธนูระเบิด', 'B', 2, 'once', 'one third wide', 'an arrow bomb blast: a green flash, a black and neon green cartoon explosion with puffy smoke and leaves', MAGENTA),
  ('ar_vines', 'Z ธนูหนาม', 'D', 2.5, 'once', 'a circle one third of the picture wide', 'seen from above: thorny black vines with green glowing rims bursting out on the ground in a circle and tangling over the middle', MAGENTA),
  ('ar_stars', 'X ฝนดาว', 'B', 2.5, 'once', 'one third wide, the full height', 'a rain of glowing green star arrows falling from the top onto a ground area, each landing with a small green burst', MAGENTA),
 ]),
 ('mage', 'นักเวท', 'Colours: each element its own bright colours (fire orange-yellow, ice cyan-white, lightning blue-violet-white, arcane bright blue), dark outlines.', [
  ('mg_fireball', 'Q ลูกไฟ', 'S', 1.5, 'once', 'the ball one tenth wide', 'a fireball flying left to right with a flickering fire tail, exploding into a round fire blast with sparks and dark smoke', G),
  ('mg_chain', 'E สายฟ้าโซ่', 'S', 1, 'once', 'a line across half of the picture', 'a jagged lightning bolt jumping from left to right with branches, crackling bursts of sparks where it hits', G),
  ('mg_nova', 'R วงน้ำแข็ง', 'D', 2, 'once', 'a ring growing to half of the picture wide', 'seen from above: a frost nova, a ring of ice bursting outward on the ground, sharp ice spikes along the ring, frost mist, then the ice cracks and fades', G),
  ('mg_blink', 'F วาร์ป', 'B', 1.2, 'once', 'one fifth wide', 'a blink: the spot collapses into a swirl of arcane blue light, then pops in a small burst of sparks', G),
  ('mg_meteor', 'Z อุกกาบาต', 'B', 2.5, 'once', 'one third wide, full height', 'a flaming meteor falling from the top onto a ground point, a big fire explosion, rocks thrown out, a scorched crater with glowing edges', G),
  ('mg_shield', 'X โล่เวท', 'B', 2.5, 'loop', 'a bubble one quarter wide', 'a glowing blue magic shield bubble with faint hexagon patterns, gently pulsing and shimmering', G),
 ]),
 ('priest', 'นักบวช', 'Colours: warm gold and white holy light, thin gold rune lines, a soft glow, darker gold outlines.', [
  ('pr_heal', 'Q ฟื้นฟู', 'B', 2, 'once', 'one fifth wide, half tall', 'healing light: soft gold-white light rising round an empty spot, small plus-shaped sparkles and petals of light floating up', G),
  ('pr_pillar', 'E ทัณฑ์สวรรค์', 'B', 2, 'once', 'narrow, the full height', 'a pillar of holy golden light striking down onto a ground point, a gold rune circle flashing at its foot, a bright burst', G),
  ('pr_bless', 'R พรนักรบ', 'B', 2, 'once', 'one fifth wide', 'a blessing: a ring of golden light rising from the feet to above head height round an empty spot, two small wings of light opening, sparkles', G),
  ('pr_step', 'F ก้าวแสง', 'D', 2, 'loop', 'a patch one quarter of the picture wide', 'seen from above: a small glowing patch of holy light on the ground with a gold rune pattern, sparkles rising', G),
  ('pr_curse', 'Z คำสาปอ่อนแรง', 'D', 2.5, 'once', 'a circle one third of the picture wide', 'seen from above: a purple rune circle appearing on the ground, dark tendrils and slow purple smoke rising, then sinking back', G),
  ('pr_miracle', 'X ปาฏิหาริย์', 'B', 2.5, 'once', 'one quarter wide, full height', 'a miracle: a tall column of white-gold light round an empty spot, feathers of light drifting down, a radiant burst at the end', G),
 ]),
 ('gunner', 'มือปืนคู่ (คลาส 2)', 'Colours: black and glowing NEON ORANGE-YELLOW, a high-tech sci-fi look with clean light lines.', [
  ('gn_muzzle', 'ไฟปากกระบอก', 'S', 0.6, 'once', 'small: one sixth wide', 'a sci-fi pistol muzzle flash pointing to the right: a star-shaped orange-yellow neon flash with a white core and small energy sparks', G),
  ('gn_tracer', 'กระสุนพลังงาน', 'S', 0.8, 'once', 'a line across half of the picture', 'a glowing orange-yellow energy bullet streaking from left to right with a thin light trail', G),
  ('gn_hit', 'กระสุนโดน', 'B', 0.8, 'once', 'small: one sixth wide', 'an energy bullet impact: a small orange-yellow neon burst with hexagon-shaped sparks', G),
  ('gn_spin', 'ยิงหมุนรอบตัว (คริ)', 'D', 1.5, 'once', 'a ring half of the picture wide', 'seen from above: from an empty centre, glowing orange-yellow energy bullets fired outward in every direction in a spinning spiral, light streaks', G),
 ]),
 ('laserbow', 'ธนูเลเซอร์ (คลาส 2)', 'Colours: white and glowing NEON GREEN, a high-tech sci-fi look with clean light lines.', [
  ('lb_shot', 'ลูกธนูแสง', 'S', 1, 'once', 'a line across half of the picture', 'a laser arrow: a thin bright white-green beam bolt shooting from left to right with a light trail', MAGENTA),
  ('lb_charge', 'ยิงชาร์จ', 'S', 1.5, 'once', 'a beam across two thirds of the picture', 'a charged laser shot: green light gathering into a glowing point on the left, then a thick neon green laser beam blasting to the right with energy rings round it, fading', MAGENTA),
  ('lb_hit', 'แสงโดน', 'B', 0.8, 'once', 'small: one sixth wide', 'a laser impact: a small white-green neon burst with sharp light spikes', MAGENTA),
  ('lb_spin', 'หมุนตัวยิง (คริ)', 'D', 1.5, 'once', 'a ring half of the picture wide', 'seen from above: from an empty centre, neon green laser arrows fired outward all round in a spinning ring, light streaks', MAGENTA),
 ]),
]
# the shared library for monsters, items and anything else
FX = [
 ('Hits & slashes', 'โดนตี / ฟัน', [
  ('hit_spark', 'ประกายโดนตี', 'B', 1, 'once', 'small: one fifth of the picture wide', 'a punchy hit impact: a white-yellow star flash with sharp spiky sparks bursting out and a tiny puff of smoke', GREEN),
  ('hit_crit', 'คริติคอล', 'B', 1.5, 'once', 'one third of the picture wide', 'a big critical hit: a jagged red-orange starburst with a white core, thick spikes shooting outward, small stars and sparks flying', GREEN),
  ('slash_arc', 'รอยดาบโค้ง', 'S', 1, 'once', 'half of the picture wide', 'one big curved sword slash crescent swinging from left to right: a thick white-hot trail with an orange-red edge, a few sparks flung off the tip', GREEN),
  ('slash_x', 'ฟันกากบาท', 'B', 1.2, 'once', 'one third of the picture wide', 'two crossing slash strokes forming an X, a white flash where they cross, sharp sparks, then the strokes break into shards', GREEN),
  ('slash_spin', 'ฟันหมุนรอบตัว', 'D', 1.2, 'once', 'a ring half of the picture wide', 'a full 360-degree sword swing seen from above: a thick white-orange circular slash trail sweeping round an empty centre, sparks flung outward', GREEN),
  ('thrust', 'แทงพุ่ง', 'S', 1, 'once', 'a long thin line across half of the picture', 'a fast straight thrust: a long sharp white-blue light streak shooting from left to right, a small burst at the tip', GREEN),
 ]),
 ('Explosions & ground', 'ระเบิด / พื้น', [
  ('boom_fire', 'ระเบิดไฟ', 'B', 2.5, 'once', 'the cloud about one third of the picture wide', 'a cartoon fire explosion: a flash, a puffy mushroom of orange and red fire, black smoke clouds rolling up, then the smoke thins away', GREEN),
  ('boom_dark', 'ระเบิดมืด', 'B', 2.5, 'once', 'one third of the picture wide', 'a dark magic explosion: a black and deep purple puffy blast with glowing neon red cracks of light, black smoke rolling out, red embers', GREEN),
  ('slam_ring', 'คลื่นทุบพื้น', 'D', 2, 'once', 'a ring growing to half of the picture wide', 'a ground slam seen from above: a white flash in the middle, a thick round shockwave ring racing outward, dust puffs round it, small rocks thrown out', GREEN),
  ('cracks', 'พื้นแตกลาวา', 'D', 2.5, 'once', 'one third of the picture wide', 'the ground cracking open seen from above: jagged cracks spreading out from the centre glowing orange-red like lava, a few broken rock slabs, then the glow fades', GREEN),
  ('crack_line', 'รอยแยกพุ่งตรง', 'D', 2, 'once', 'a line across half of the picture', 'a crack in the ground racing from LEFT to RIGHT seen from above, glowing orange fire bursting up along it, rocks popping, then it cools', GREEN),
  ('dust_land', 'ฝุ่นตอนลงพื้น', 'B', 1.2, 'once', 'one quarter of the picture wide, low', 'a landing dust puff: round cartoon dust clouds bursting sideways along the ground, small pebbles', GREEN),
 ]),
 ('Projectiles', 'ลูกยิง', [
  ('fireball', 'ลูกไฟ', 'S', 1.5, 'once', 'the ball one tenth of the picture wide', 'a cartoon fireball flying from the left edge to the right third, a flickering fire tail, then it bursts into a small fire puff', GREEN),
  ('dark_orb', 'ลูกพลังมืด', 'S', 1.5, 'once', 'the orb one tenth of the picture wide', 'a black and purple energy orb with a red rim flying left to right with a wavy smoke tail, then it pops in a dark burst', GREEN),
  ('wave_crescent', 'คลื่นฟันพุ่ง', 'S', 1.5, 'once', 'the crescent one fifth of the picture tall', 'a sword-wave crescent flying from left to right: a thick bright crescent with a black outline, speed lines behind, it breaks into sparks at the end', GREEN),
  ('arrow_trail', 'ลูกธนูพลัง', 'S', 1, 'once', 'a thin line across half of the picture', 'a glowing magic arrow streaking from left to right with a bright trail and small sparkles, a tiny star burst at the end', GREEN),
 ]),
 ('Fire', 'ไฟ', [
  ('fire_pillar', 'เสาไฟ', 'B', 2.5, 'once', 'narrow: one fifth wide, two thirds tall', 'a pillar of fire erupting straight up from the ground: cartoon flames curling, sparks, black smoke at the top, then it dies down', GREEN),
  ('fire_field', 'พื้นไฟลุก', 'D', 3, 'loop', 'a patch one third of the picture wide', 'a round patch of burning ground seen from above: little cartoon flames flickering all over it, embers', GREEN),
  ('burn', 'ติดไฟ (สถานะ)', 'B', 2, 'loop', 'small: one sixth wide', 'small cartoon flames flickering on an empty spot where a creature would be, a few embers rising', GREEN),
 ]),
 ('Ice', 'น้ำแข็ง', [
  ('ice_spikes', 'หนามน้ำแข็ง', 'B', 2, 'once', 'one third of the picture wide', 'sharp ice crystal spikes bursting up out of the ground in a cluster, light blue and white with dark blue outlines, frost mist, then they shatter', GREEN),
  ('frost_nova', 'วงน้ำแข็ง', 'D', 2, 'once', 'a ring growing to half of the picture wide', 'a ring of frost spreading outward on the ground seen from above, ice crystals forming along it, cold mist, then it melts away', GREEN),
  ('frozen', 'แช่แข็ง (สถานะ)', 'B', 2, 'loop', 'one fifth wide', 'a block of clear blue ice with white shine round an empty spot where a creature would be, small snow sparkles', GREEN),
 ]),
 ('Lightning', 'สายฟ้า', [
  ('bolt_strike', 'ฟ้าผ่า', 'B', 1.5, 'once', 'narrow, from the top to the middle', 'a cartoon lightning bolt striking down from the top onto a ground point: a jagged white-yellow bolt with a blue glow, a bright flash and an electric burst on the ground', GREEN),
  ('chain_bolt', 'สายฟ้ากระโดด', 'S', 1, 'once', 'a line across half of the picture', 'a jagged electric arc zapping from left to right with small branches, crackling sparks at both ends', GREEN),
  ('shock', 'ช็อต (สถานะ)', 'B', 1.5, 'loop', 'one sixth wide', 'little crackling electric sparks and zigzags jumping round an empty spot where a creature would be', GREEN),
 ]),
 ('Dark & blood', 'มืด / เลือด', [
  ('rage_aura', 'ออร่าคลั่ง', 'B', 3, 'loop', 'a column one fifth wide, half tall', 'a rage aura round an empty spot where a fighter stands: black smoke and neon red flames rising, red cracks of light flickering, embers drifting up', GREEN),
  ('shadow_burst', 'ระเบิดเงา', 'B', 1.5, 'once', 'one quarter wide', 'a burst of black shadow smoke with purple rims and sharp shadow spikes, then it fades into wisps', GREEN),
  ('chains', 'โซ่ตรวน', 'D', 2.5, 'once', 'a circle one third of the picture wide', 'seen from above: a glowing red rune circle on the ground, black chains with red-hot links bursting out of it, crossing over the middle and pulling tight, then crumbling', GREEN),
  ('blood_slash', 'รอยฟันเลือด', 'S', 1, 'once', 'half of the picture wide', 'a heavy dark slash crescent from left to right: a black trail with a neon red edge, red droplet sparks flying', GREEN),
 ]),
 ('Holy & support', 'แสง / ช่วยเหลือ', [
  ('heal', 'ฟื้นเลือด', 'B', 2, 'once', 'one fifth wide, half tall', 'healing: soft green-gold light rising up round an empty spot, little plus-shaped sparkles and leaves of light floating up', MAGENTA),
  ('holy_pillar', 'เสาแสงศักดิ์สิทธิ์', 'B', 2, 'once', 'narrow, the full height', 'a pillar of golden holy light shining down onto a ground point, a gold rune circle flashing at its foot, sparkles', GREEN),
  ('shield', 'โล่พลัง', 'B', 2.5, 'loop', 'a bubble one quarter wide', 'a round glowing blue magic shield bubble with a hexagon pattern and a white shine, gently pulsing', GREEN),
  ('buff_up', 'บัฟพลัง', 'B', 1.5, 'once', 'one fifth wide', 'a power-up: a ring of light rising from the ground to above head height round an empty spot, arrows of light pointing up, sparkles', GREEN),
  ('level_up', 'เลเวลอัพ', 'B', 2, 'once', 'one quarter wide', 'a level-up: a bright gold burst, a column of light, stars and confetti-like sparkles spinning up', GREEN),
 ]),
 ('Nature & poison', 'ธรรมชาติ / พิษ', [
  ('poison_cloud', 'หมอกพิษ', 'D', 3, 'loop', 'a patch one third of the picture wide', 'a bubbling toxic green cloud on the ground seen from above, round cartoon bubbles popping, purple-green wisps', MAGENTA),
  ('roots', 'รากไม้มัด', 'B', 2, 'once', 'one quarter wide', 'thick green vines and roots bursting up from the ground and twisting round an empty spot, leaves flying', MAGENTA),
  ('tornado', 'พายุหมุน', 'B', 2.5, 'once', 'narrow: one fifth wide, half tall', 'a small cartoon whirlwind spinning on the ground, white wind streaks with blue-grey tones, leaves and dust caught in it', GREEN),
 ]),
 ('Movement & misc', 'เคลื่อนที่ / อื่นๆ', [
  ('dash_smoke', 'ควันพุ่ง', 'S', 1, 'once', 'a trail across one third of the picture', 'a dash: a trail of speed lines and cartoon smoke puffs left behind moving from left to right', GREEN),
  ('teleport', 'วาร์ป', 'B', 1.5, 'once', 'one fifth wide', 'a teleport: an empty spot collapses into a swirl of blue-violet light and pops in a star burst', GREEN),
  ('portal', 'ประตูมิติ', 'D', 3, 'loop', 'a circle one third of the picture wide', 'a magic portal on the ground seen from above: a swirling purple-blue vortex with a glowing rune rim, spinning slowly', GREEN),
  ('death_poof', 'มอนตาย', 'B', 1.2, 'once', 'one fifth wide', 'a monster defeated: a puff of round cartoon smoke with a few stars and sparkles popping out', GREEN),
  ('coin_burst', 'เหรียญกระจาย', 'B', 1.5, 'once', 'one quarter wide', 'a burst of shiny gold coins popping up and falling back with little sparkles', MAGENTA),
 ]),
]

def prompt(e, tone=''):
    key, th, kind, sec, end, size, what, bg = e
    tone = (' ' + tone) if tone else ''
    return (f'Create a {sec:g}-second VIDEO, SQUARE 1:1, of ONE game visual effect, no character, no people, no weapon. {STYLE} '
            f'Effect: {what}.{tone} {KIND[kind][0]} Size: {size}, in the middle of the picture with wide empty margins on all four sides; '
            f'nothing ever touches or leaves the edges. {WIDE} {END[end]} Background: {bg} the whole time, nothing else on it: no ground '
            f'texture, no floor, no landscape, no text. Locked camera: no zoom, no pan, no tilt, no shake, no cuts.')

def card(e, tone=''):
    key, th, kind, sec, end, *_ = e
    return (f'<div class="card"><div class="bh"><h3>{html.escape(th)} <small>{key}</small></h3><span class="chip k{kind}">{kind}</span></div>'
            f'<p class="note">{KIND[kind][1]} · {sec:g} วิ{" · วนซ้ำ" if end == "loop" else ""}</p>'
            f'<div class="blk"><div class="bh"><span>พรอมต์</span><button class="cp">คัดลอก</button></div>'
            f'<textarea rows="6" readonly>{html.escape(prompt(e, tone))}</textarea></div></div>')
cards = '<h2 class="big">ชุดของแต่ละอาชีพ</h2><p class="jump">' + ' · '.join(f'<a href="#c_{k}">{th}</a>' for k, th, _, _ in CLASSES) + '</p>'
for k, th, tone, items in CLASSES:
    cards += f'<h2 class="sec" id="c_{k}">{th} <small>{len(items)} อัน</small></h2>' + ''.join(card(e, tone) for e in items)
cards += '<h2 class="big">คลังกลาง (มอน ของ อื่นๆ)</h2>'
for en, th_sec, items in FX:
    cards += f'<h2 class="sec">{th_sec} <small>{en}</small></h2>'
    cards += ''.join(card(e) for e in items)
n = sum(len(i) for _, _, i in FX) + sum(len(c[3]) for c in CLASSES)
page = '''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VFX Video Pack</title><style>
:root{--bg:#14121c;--card:#1f1c2b;--ink:#ece8f6;--dim:#a39cb8;--line:#3a3550;--acc:#ffb340;--b:#6ec8ff;--d:#7be08a;--s:#ff8a7a}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f2f8;--card:#fff;--ink:#1d1a26;--dim:#615a74;--line:#d8d2e6;--acc:#c86a00;--b:#1a78b8;--d:#1f8f3a;--s:#c0392b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,sans-serif;padding:16px}
main{max-width:860px;margin:0 auto}h1{font-size:22px;margin:4px 0 6px}h3{font-size:16px;margin:0}h3 small,h2 small{color:var(--dim);font-weight:400;font-size:12px}
.intro{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 16px;margin:0 0 14px}.intro li{margin:4px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:0 0 12px}
.chip{font:600 12px system-ui;border:1px solid currentColor;border-radius:99px;padding:1px 9px}.kB{color:var(--b)}.kD{color:var(--d)}.kS{color:var(--s)}
.note{color:var(--dim);font-size:13px;margin:4px 0 0}.blk{margin-top:8px}.bh{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:14px;margin-bottom:4px}
textarea{width:100%;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px;font:12.5px/1.45 ui-monospace,Menlo,monospace;resize:vertical}
button.cp{background:var(--acc);color:#1a1200;border:0;border-radius:6px;padding:5px 14px;font:inherit;font-size:13px;cursor:pointer}button.cp.done{background:var(--d)}
.sec{margin:22px 0 10px;font-size:19px}.big{margin:30px 0 6px;font-size:21px;border-bottom:2px solid var(--acc);padding-bottom:4px}.jump{font-size:14px;line-height:2}.jump a{color:var(--acc)}
</style></head><body><main>
<h1>คลังเอฟเฟกต์จากวิดีโอ (''' + str(n) + ''' แบบ)</h1>
<ol class="intro">
<li><b>แยกตามอาชีพ:</b> แต่ละอาชีพมีโทนสีของตัวเองใส่ไว้ในพรอมต์แล้ว (เบอร์เซิร์กเกอร์ ดำ-แดงนีออน, นักมีด ดำ-ม่วงนีออน, นักธนู ดำ-เขียวนีออน ...) ด้านล่างสุดเป็นคลังกลางไว้ใช้กับมอนและของ</li>
<li><b>ลายเดียวกันหมด:</b> การ์ตูนเส้นดำหนา สีสด แบบที่ 1 ที่เลือก ทุกพรอมต์ขึ้นต้นเหมือนกัน เอฟเฟกต์จะได้เข้ากันเป็นชุด</li>
<li><b>ใช้ได้ทุกทิศในแมพ 3D:</b> <span class="chip kB">B</span> ตั้งขึ้น เหมือนกันทุกด้าน เกมหันเข้ากล้องเอง · <span class="chip kD">D</span> แบนบนพื้น ถ่ายจากบนลงตรงๆ เกมวางลงพื้นแล้วหมุนได้ทุกทิศ · <span class="chip kS">S</span> พุ่ง/ฟันจากซ้ายไปขวา เกมหมุนให้ชี้ไปหาเป้า</li>
<li><b>วิธีสั่ง:</b> Meta AI โหมดวิดีโอ กดคัดลอกทีละการ์ด วาง แล้วส่ง ไม่ต้องแนบรูป · สีเขียวกับสีชมพูเป็นพื้นหลังให้ตัดออก (เอฟเฟกต์สีเขียวใช้พื้นชมพู)</li>
<li><b>ได้คลิปแล้ว:</b> ตัดเองที่ <a href="../vfxcut.html">vfxcut.html</a> หรือส่ง mp4 มาพร้อมชื่อ เช่น "slam_ring"</li>
</ol>
''' + cards + '''</main><script>
document.addEventListener('click',e=>{const b=e.target.closest('button.cp');if(!b)return;const t=b.closest('.blk').querySelector('textarea');
const done=()=>{b.textContent='คัดลอกแล้ว ✓';b.classList.add('done');setTimeout(()=>{b.textContent='คัดลอก';b.classList.remove('done')},1500)};
try{navigator.clipboard.writeText(t.value).then(done,()=>{t.select();document.execCommand('copy');done()})}catch(_){t.select();document.execCommand('copy');done()}});
</script></body></html>'''
open('docs/vfx-pack.html', 'w').write(page); print('docs/vfx-pack.html', n, 'effects')
