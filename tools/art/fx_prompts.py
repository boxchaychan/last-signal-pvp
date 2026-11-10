# Skill-effect prompts for the action game (owner 2026-11-09 "เอาพรอม gpt มา ... ฉันสั่งเอง", chose "เอฟเฟกต์สกิล"): one card per
# skill that still uses an old or borrowed effect, a copy button, the layout the game needs. The owner makes the pictures (ChatGPT
# images or the effect site used for Rapier Flurry / Bomb Arrow / Earthsplitter) and sends them back as files; Claude cuts them
# with tools/art/pfx_paste.py and recolours with archer_fx.py where a hero has its own tone.
#   python3 tools/art/fx_prompts.py   -> docs/fx-prompts.html
# Mark a skill done in DONE when its effect is in the game.
import html

LAYOUT = {
    'shot': ('Travels from the LEFT edge of each cell (where the caster stands, about 15% of the cell width, middle height) to a target '
             'point at about 80% of the cell width; the impact happens there.', 'ยิงจากซ้ายไปขวา'),
    'ground': ('Centred on the ground at the middle of each cell, the ground line at about 75% of the cell height. The camera looks down '
               'at an angle, so anything lying on the ground (rings, circles, cracks) is a flat ellipse about twice as wide as tall.', 'กลางพื้น'),
    'sky': ('Comes down from the top of the cell onto a ground point at the middle, the ground line at about 80% of the cell height; '
            'rings on the ground are flat ellipses about twice as wide as tall.', 'ตกจากฟ้า'),
    'self': ('Around a character standing at the centre of each cell, feet at about 80% of the cell height. Leave the character OUT '
             '(empty space where it stands), draw only the effect round it.', 'รอบตัวละคร'),
    'front': ('Starts round a character standing at about 30% of the cell width (feet at 80% height; leave the character OUT) and '
              'swings out to the RIGHT in front of it.', 'หน้าตัวไปทางขวา'),
}
TONE = {
    'swordsman': 'deep crimson red and orange fire with white-hot cores, a dark red-black outline, a few gold sparks',
    'rogue': 'black ink-like strokes with a thin glowing neon purple rim and a soft violet glow (a shadow ninja look)',
    'fire': 'orange and yellow fire with white-hot cores, dark smoke, a dark outline',
    'bolt': 'electric blue-violet lightning with white cores, small branching sparks',
    'ice': 'pale cyan and white ice crystals with deep blue edges, cold white mist',
    'arcane': 'bright blue arcane light with white cores, small rune sparks',
    'holy': 'warm gold and white holy light, thin gold rune lines, a soft glow, a darker gold outline',
    'berserker': 'pure black ink-like strokes with a thin glowing neon RED rim and a soft crimson glow, a few tiny red embers '
                 '(dark, heavy and brutal; no orange, no yellow)',
    'curse': 'deep purple and black shadow with violet rune lines, dark smoke',
}
# hero, key, Thai name, what it does in the game (Thai), English effect, layout, tone, frames (cols x rows), loop
FX = [
    ('swordsman', 'sw_spin', 'E พายุดาบ', 'กดค้างหมุนดาบฟันรอบตัว เดินได้ (ภาพวนซ้ำ)',
     'a whirlwind of sword slashes spinning round the character: several crimson crescent slash arcs circling at different heights, '
     'embers and sparks flung outward', 'self', 'swordsman', (4, 4), True),
    ('swordsman', 'sw_charge', 'R ชาร์จฟัน', 'กดค้างชาร์จ 3 ระดับ แล้วปล่อยฟันกวาดกว้าง',
     'frames 1-12: red energy gathering round the character in three rising pulses (small, bigger, biggest with flames licking up); '
     'frames 13-24: one huge wide crescent slash sweeping in front, a long crimson arc with a white-hot edge, then it breaks into embers',
     'front', 'swordsman', (6, 4), False),
    ('swordsman', 'sw_slam', 'F กระโดดทุบ', 'กระโดดไปทุบจุดที่เล็ง มอนรอบ ๆ มึน',
     'a heavy two-handed blow slams into the ground: a white flash, a wide shockwave ring racing out, glowing orange cracks spreading '
     'from the centre, rocks and dirt thrown up, a dust cloud that settles', 'ground', 'swordsman', (6, 4), False),
    ('swordsman', 'sw_parry', 'Z ตั้งรับสวน', 'ป้องกันได้แล้วฟันสวนกลับแรง 3 เท่า',
     'a parry: a bright red-gold clash flash and a ring of sparks in front of the character (the blocked hit), then a fast counter '
     'slash: one sharp crimson crescent cutting forward', 'front', 'swordsman', (6, 4), False),
    ('swordsman', 'sw_rage', 'X คลั่ง', 'คลั่ง 8 วิ ตีเร็ว ดูดเลือด (ภาพวนซ้ำ)',
     'a berserk aura: burning red flames rising round the character, red-black smoke, embers drifting up, an occasional crimson flare',
     'self', 'swordsman', (4, 4), True),
    ('rogue', 'rg_smoke', 'R ระเบิดควัน', 'ปาระเบิดควัน มอนในวงตาบอด',
     'a smoke bomb bursting: a small dark flash, then thick black-purple smoke billowing out into a wide low cloud on the ground, '
     'swirling, then thinning out', 'ground', 'rogue', (6, 4), False),
    ('rogue', 'rg_vanish', 'Z ล่องหน', 'หายเป็นเงา 4 วิ',
     'vanishing into shadow: black-purple smoke and shadow wisps wrapping round the character and collapsing inward, a few purple sparks, '
     'then nothing', 'self', 'rogue', (6, 4), False),
    ('rogue', 'rg_venom', 'X มีดพิษ', 'พิษซ้อน 5 ชั้นแล้วระเบิด',
     'a poison burst on a target: toxic purple-green bubbles swelling, then splashing outward in drops and a ring of venom mist',
     'ground', 'rogue', (6, 4), False),
    ('mage', 'mg_fireball', 'Q ลูกไฟ', 'ยิงลูกไฟไปจุดที่เล็ง ระเบิดเป็นวง มอนติดไฟ',
     'a fireball flies and explodes into a round fire blast with a burst of sparks and dark smoke', 'shot', 'fire', (6, 4), False),
    ('mage', 'mg_chain', 'E สายฟ้าโซ่', 'สายฟ้ากระโดดโดนมอน 5 ตัว',
     'a lightning bolt jumps across with jagged branches and hits the target in a crackling burst of sparks', 'shot', 'bolt', (6, 4), False),
    ('mage', 'mg_nova', 'R วงน้ำแข็ง', 'แช่แข็งมอนรอบตัว 2 วิ',
     'a frost nova: a ring of ice bursts outward on the ground from the centre, sharp ice spikes rising round the ring, frost mist, '
     'then the ice cracks and fades', 'ground', 'ice', (6, 4), False),
    ('mage', 'mg_blink', 'F วาร์ป', 'วาร์ปไปทางที่เดิน',
     'a blink teleport: the spot collapses into a swirl of arcane light, then pops in a small burst of sparks', 'self', 'arcane', (6, 4), False),
    ('mage', 'mg_meteor', 'Z อุกกาบาต', 'เรียกอุกกาบาตตกใส่จุดที่เล็ง มอนมึน',
     'a flaming meteor falls from the top right and crashes into the ground point: a big fire explosion, rocks thrown out, a dark '
     'scorched crater with glowing edges', 'sky', 'fire', (6, 4), False),
    ('mage', 'mg_shield', 'X โล่เวท', 'โล่ดูดดาเมจ (ภาพวนซ้ำ) ถ้าแตกจะช็อตมอนรอบตัว',
     'a glowing magic shield bubble round the character with faint hexagon patterns, gently pulsing and shimmering', 'self', 'arcane', (4, 4), True),
    ('priest', 'pr_heal', 'Q ฟื้นฟู', 'ฟื้นเลือดทันที แล้วค่อย ๆ ฟื้นต่อ',
     'healing light: soft gold-green light rising round the character, small plus-shaped sparkles and petals of light floating up',
     'self', 'holy', (6, 4), False),
    ('priest', 'pr_pillar', 'E ทัณฑ์สวรรค์', 'เสาแสงตกจากฟ้า มอนในวงเปราะ',
     'a pillar of holy golden light strikes down onto the point, a gold rune circle flashes on the ground, a bright burst, then the '
     'pillar thins away', 'sky', 'holy', (6, 4), False),
    ('priest', 'pr_bless', 'R พรนักรบ', 'ดาเมจ +30% 8 วิ',
     'a blessing: a ring of golden light rises from the feet to above the head, two small wings of light open behind, sparkles',
     'self', 'holy', (6, 4), False),
    ('priest', 'pr_step', 'F ก้าวแสง', 'วาร์ปสั้น ๆ ทิ้งรอยแสงที่ฟื้นเลือด',
     'a holy dash: the character dissolves into gold light motes that stream to the right and gather again, leaving a small glowing '
     'patch on the ground', 'self', 'holy', (6, 4), False),
    ('priest', 'pr_curse', 'Z คำสาปอ่อนแรง', 'มอนในวงช้าลง ตีเบาลง 6 วิ',
     'a curse circle: a purple rune ring appears on the ground, dark tendrils and slow purple smoke rise from it, then sink back',
     'ground', 'curse', (6, 4), False),
    ('priest', 'pr_miracle', 'X ปาฏิหาริย์', '10 วิ ตายแล้วฟื้นทันที',
     'a miracle: a tall column of white-gold light round the character, feathers of light drifting down, a radiant burst at the end',
     'self', 'holy', (6, 4), False),
    ('berserker', 'bz_chain', 'Q โซ่รวบวิญญาณ', 'เหวี่ยงโซ่กวาดเป็นพัดกว้าง ดึงมอนมากองหน้าตัว แล้วกดซ้ำฟันรอบตัว',
     'frames 1-12: heavy black chains with glowing red links lash out in a WIDE fan in front (several chains spreading like a 160 degree '
     'fan), then snap back toward the caster dragging red light streaks; frames 13-24: one huge horizontal cleave all the way round '
     'the caster: a full black ring slash with a neon red edge, red sparks flung outward, then it breaks into smoke', 'front', 'berserker', (6, 4), False),
    ('berserker', 'bz_triple', 'E ฟาดสามยมทูต', 'ฟัน 3 จังหวะกว้าง จังหวะสุดท้ายฟาดลงพื้นแตกพุ่งไปข้างหน้า',
     'three heavy greatsword slashes: frames 1-8 a wide crescent slash right to left, frames 9-16 a wider crescent left to right, '
     'frames 17-24 an overhead blow hitting the ground: red glowing cracks race forward in a long wedge, black rock shards and dust fly up; '
     'each slash is a thick black blade trail with a neon red edge', 'front', 'berserker', (6, 4), False),
    ('berserker', 'bz_slam', 'R ทุบพสุธาโลหิต', 'ชาร์จแล้วทุบพื้น คลื่นแผ่นดินแตกรอบตัว ลาวาดำแดงค้าง',
     'a crushing ground slam: frames 1-6 dark red energy sucked down into one point, frames 7-24 the ground shatters: a huge flat ring '
     'shockwave of black stone, glowing neon red cracks spreading out like a spider web, black rock slabs thrown up and falling back, '
     'the cracks keep glowing like dark lava and slowly dim', 'ground', 'berserker', (6, 4), False),
    ('berserker', 'bz_hook', 'F โซ่กระชาก', 'ปาโซ่ไปเกี่ยวแล้วกระชากตัวไปลงฟาด',
     'frames 1-10: a black chain with a hooked claw and glowing red links shoots from the left edge to the right and bites into the '
     'ground with a red flash; frames 11-24: a heavy landing blow on that spot: a black and red impact burst, a small flat shockwave '
     'ring, dust and red sparks', 'shot', 'berserker', (6, 4), False),
    ('berserker', 'bz_shackle', 'Z ตรวนนรก', 'โซ่พุ่งจากพื้นเป็นวงรัดมอนไว้',
     'a ring of black chains bursting up from cracks in the ground, a glowing red rune circle on the ground (flat ellipse), the chains '
     'whip up, cross over the middle and pull tight, then hold there with red light pulsing along the links', 'ground', 'berserker', (6, 4), False),
    ('berserker', 'bz_rage', 'X ร่างคลั่งโลหิต', 'ไม้ตาย 15 วิ ไอแดงนีออนรอบตัว (ภาพวนซ้ำ)',
     'a berserk aura: black smoke and neon red flame wisps rising round the character, glowing red cracks of light flickering in the air, '
     'red embers drifting upward, an occasional crimson pulse', 'self', 'berserker', (4, 4), True),
    ('berserker', 'bz_wave', 'X คลื่นฟัน (ตอนคลั่ง)', 'ระหว่างไม้ตาย ตีธรรมดาแต่ละครั้งปล่อยคลื่นฟันสั้น ๆ',
     'a short crescent slash wave flying forward: a thick black crescent with a neon red rim and a red glow, leaving a red streak, '
     'then breaking into red sparks', 'shot', 'berserker', (6, 3), False),
]
DONE = set()
HERO = {'berserker': 'เบอร์เซิร์กเกอร์ (คลาส 2)', 'swordsman': 'นักดาบ', 'rogue': 'นักมีด', 'mage': 'นักเวท', 'priest': 'นักบวช'}

def prompt(f):
    hero, key, th, does, en, lay, tone, (c, r), loop = f
    n = c * r
    return (f'2D game skill effect sprite sheet for a top-down action RPG (bright pixel-art world, camera looking down at an angle). '
            f'ONE effect only: {en}.\n\n'
            f'Layout: exactly {n} frames in a {c} x {r} grid of equal square cells, read left to right, top to bottom. '
            f'Every frame stays inside its own cell with empty space round it; nothing crosses into the next cell; the anchor point is '
            f'at the same spot in every cell. {LAYOUT[lay][0]}\n\n'
            f'Colours: {TONE[tone]}. High contrast so it reads on bright green grass.\n'
            + ('Motion: a smooth seamless loop, the last frame leads back into the first.\n' if loop else
               'Motion: quick build-up, a strong main burst, then it fades out to nothing in the last frames.\n')
            + 'Background: fully transparent (PNG with alpha). No characters, no people, no weapons held by anyone, no text, '
              'no numbers, no grid lines, no borders, no frame labels. Do ONLY this one picture.')

# Video version (owner 2026-11-10 "เอาเอฟเฟกต์เบอร์เซิร์กมาลงเจน", now making clips with Meta AI): text only, the effect alone on
# flat green, locked camera; Claude keys the green out and cuts the frames (tools/video/vid2px.py).
import re
VLAY = {'shot': 'It travels from the left side of the picture to a point on the right side and hits there.',
        'ground': 'It sits on the ground in the middle of the picture; the camera looks down at an angle, so rings and cracks on the '
                  'ground are flat ellipses about twice as wide as tall.',
        'sky': 'It comes down from the top onto a ground point in the middle; rings on the ground are flat ellipses.',
        'self': 'It surrounds an EMPTY spot in the middle of the picture where a character would stand (leave that spot empty).',
        'front': 'It starts round an empty spot on the left third of the picture (where a character would stand) and swings out to the right.'}
def vprompt(f, T=4):
    hero, key, th, does, en, lay, tone, (c, r), loop = f
    n = c * r
    en = re.sub(r'frames (\d+)-(\d+)', lambda m: f'from {(int(m.group(1)) - 1) / n * T:.1f} s to {int(m.group(2)) / n * T:.1f} s', en)
    return (f'Short 2D game skill effect animation, about {T} seconds, for a top-down pixel-art action RPG (camera looking down at an '
            f'angle). ONE effect only: {en}. {VLAY[lay]} Colours: {TONE[tone]}; crisp pixel-art look. '
            + ('It loops seamlessly. ' if loop else 'Quick build-up, a strong burst, then it fades out completely and the video ends on the empty background. ')
            + 'Locked camera: no zoom, no pan, no shake, no cuts. Plain flat pure green background (#00FF00) the whole time. '
              'No characters, no people, no weapons held by anyone, no ground texture, no text.')

def card(f):
    hero, key, th, does, en, lay, tone, (c, r), loop = f
    st = '<span class="chip ok">อยู่ในเกมแล้ว</span>' if key in DONE else '<span class="chip todo">ยังไม่ได้ทำ</span>'
    return (f'<div class="card"><div class="bh"><h2>{html.escape(th)} <small>{HERO[hero]}</small></h2>{st}</div>'
            f'<p class="note">{html.escape(does)} · {c * r} เฟรม ({c}×{r}) · {LAYOUT[lay][1]}{" · วนซ้ำ" if loop else ""}</p>'
            f'<div class="blk"><div class="bh"><span>พรอมต์</span><button class="cp">คัดลอก</button></div>'
            f'<textarea rows="9" readonly>{html.escape(prompt(f))}</textarea></div>'
            f'<div class="blk"><div class="bh"><span>พรอมต์วิดีโอ (Meta AI · พื้นเขียว)</span><button class="cp">คัดลอก</button></div>'
            f'<textarea rows="7" readonly>{html.escape(vprompt(f))}</textarea></div></div>')

secs = ''.join(f'<h2 class="sec">{HERO[h]}</h2>' + ''.join(card(f) for f in FX if f[0] == h) for h in HERO)
page = '''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Skill Effect Prompts</title><style>
:root{--bg:#14121c;--card:#1f1c2b;--ink:#ece8f6;--dim:#a39cb8;--line:#3a3550;--ok:#4cc98a;--todo:#e0a040;--acc:#c8a8ff}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f2f8;--card:#fff;--ink:#1d1a26;--dim:#615a74;--line:#d8d2e6;--ok:#1f8f57;--todo:#a8650a;--acc:#6a3fc8}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Kanit,system-ui,sans-serif;padding:16px}
main{max-width:860px;margin:0 auto}h1{font-size:22px;margin:4px 0 8px}h2{font-size:17px;margin:0}h2 small{color:var(--dim);font-weight:400;font-size:13px}
.steps{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 16px 10px 30px;margin:0 0 14px}.steps li{margin:3px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:0 0 14px}
.chip{font-size:12px;border:1px solid var(--line);border-radius:99px;padding:1px 8px;white-space:nowrap}.chip.ok{color:var(--ok)}.chip.todo{color:var(--todo)}
.note{color:var(--dim);font-size:13px;margin:6px 0 0}
.blk{margin-top:10px}.bh{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:14px;margin-bottom:4px}
textarea{width:100%;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px;font:12.5px/1.45 ui-monospace,Menlo,monospace;resize:vertical}
button.cp{background:var(--acc);color:#fff;border:0;border-radius:6px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}button.cp.done{background:var(--ok)}
h1+p{color:var(--dim);margin:0 0 12px}.sec{margin:22px 0 10px;font-size:19px}
</style></head><body><main>
<h1>พรอมต์เอฟเฟกต์สกิล</h1><p>สกิลที่ยังใช้เอฟเฟกต์เก่าหรือยืมของตัวอื่นอยู่ ทำทีละภาพ กดคัดลอกแล้ววางได้เลย นักธนูครบแล้ว นักดาบ Q กับนักมีด F ก็มีแล้ว เลยไม่มีในหน้านี้</p>
<ol class="steps">
<li><b>ทำเป็นวิดีโอก็ได้:</b> ใช้กล่อง "พรอมต์วิดีโอ" กับ Meta AI ไม่ต้องแนบรูป ได้คลิปแล้วกด Download ลงเครื่องก่อน แล้วแนบไฟล์ mp4 มา บอกชื่อสกิลด้วย เช่น "เบอร์เซิร์ก Q"</li>
<li><b>หนึ่งภาพต่อหนึ่งเอฟเฟกต์:</b> ใช้ ChatGPT หรือเว็บที่ทำ Rapier Flurry / Bomb Arrow ก็ได้ วางพรอมต์ของการ์ดเดียว รอเสร็จแล้วค่อยทำการ์ดถัดไป</li>
<li><b>พื้นหลังต้องโปร่ง:</b> ถ้าได้พื้นขาวหรือดำมา ส่งมาได้เหมือนกัน ผมตัดเอง</li>
<li><b>ส่งเป็นไฟล์:</b> ภาพที่วางในแชทจะถูกย่อลง ถ้าส่งเป็นไฟล์ (หรือ zip หลายภาพ) จะคมกว่า บอกชื่อสกิลมาด้วย เช่น "นักดาบ F"</li>
<li><b>สีไม่ต้องเป๊ะ:</b> ผมปรับสีให้เข้ากับตัวละครทีหลังได้ (แบบที่ทำนักธนูเป็นดำขอบเขียว)</li>
</ol>
''' + secs + '''</main><script>
document.addEventListener('click',e=>{const b=e.target.closest('button.cp');if(!b)return;const t=b.closest('.blk').querySelector('textarea');
const done=()=>{b.textContent='คัดลอกแล้ว ✓';b.classList.add('done');setTimeout(()=>{b.textContent='คัดลอก';b.classList.remove('done')},1500)};
try{navigator.clipboard.writeText(t.value).then(done,()=>{t.select();document.execCommand('copy');done()})}catch(_){t.select();document.execCommand('copy');done()}});
</script></body></html>'''
open('docs/fx-prompts.html', 'w').write(page); print('docs/fx-prompts.html', len(FX), 'cards')
