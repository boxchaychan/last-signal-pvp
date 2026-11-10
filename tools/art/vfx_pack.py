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
GREEN, MAGENTA = 'flat pure green (#00FF00)', 'flat pure magenta (#FF00FF)'
END = {'once': 'Quick build-up, a strong burst, then it fades out completely and the video ends on the empty background.',
       'loop': 'It LOOPS seamlessly: no fade-out, the last frame matches the first.'}

# key, Thai name, kind, seconds, once/loop, size line, effect, background
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

def prompt(e):
    key, th, kind, sec, end, size, what, bg = e
    return (f'Create a {sec:g}-second VIDEO, LANDSCAPE 16:9, of ONE game visual effect, no character, no people, no weapon. {STYLE} '
            f'Effect: {what}. {KIND[kind][0]} Size: {size}, in the middle of the picture with wide empty margins on all four sides; '
            f'nothing ever touches or leaves the edges. {END[end]} Background: {bg} the whole time, nothing else on it: no ground '
            f'texture, no floor, no landscape, no text. Locked camera: no zoom, no pan, no tilt, no shake, no cuts.')

cards = ''
for en, th_sec, items in FX:
    cards += f'<h2 class="sec">{th_sec} <small>{en}</small></h2>'
    for e in items:
        key, th, kind, sec, end, *_ = e
        cards += (f'<div class="card"><div class="bh"><h3>{html.escape(th)} <small>{key}</small></h3><span class="chip k{kind}">{kind}</span></div>'
                  f'<p class="note">{KIND[kind][1]} · {sec:g} วิ{" · วนซ้ำ" if end == "loop" else ""}</p>'
                  f'<div class="blk"><div class="bh"><span>พรอมต์</span><button class="cp">คัดลอก</button></div>'
                  f'<textarea rows="6" readonly>{html.escape(prompt(e))}</textarea></div></div>')
n = sum(len(i) for _, _, i in FX)
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
.sec{margin:22px 0 10px;font-size:19px}
</style></head><body><main>
<h1>คลังเอฟเฟกต์จากวิดีโอ (''' + str(n) + ''' แบบ)</h1>
<ol class="intro">
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
