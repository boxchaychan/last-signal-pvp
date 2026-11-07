# One page with every PixelLab job still to do (owner 2026-11-07 "เอาไรอีกพรอมต์มา"): per legend the style picture,
# its colours, the character description, the attack and the skill prompt, plus the skill-effect prompts.
#   python3 tools/art/pixellab_page.py        -> docs/pixellab.html + docs/pixellab/<key>_front_128.png, <key>_palette.png
# Edit STATUS when a part arrives. Uses the cast data of legends_codex.py.
import sys, os, html, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legends_codex import C, ANIM

# done parts per key: char = character made in PixelLab, atk / sk = attack / skill animation in the game
STATUS = {'god_warrior': {'char', 'atk', 'sk'}, 'god_hunter': {'char', 'atk'}}
NOTE = {'god_warrior': 'ท่าตีกับไม้ตายตอนนี้เป็นด้านข้าง (ใช้ได้แล้ว) ถ้าอยากให้เฉียงเหมือนตัวอื่น ทำท่าตี + ไม้ตาย ทิศ south-east เพิ่ม',
        'god_hunter': 'เหลือท่าไม้ตาย'}
ORDER = ['god_hunter', 'god_assassin', 'god_mage', 'god_support', 'god_curse', 'god_warrior',
         'hero_warrior', 'hero_assassin', 'hero_hunter', 'hero_mage', 'hero_support', 'hero_curse']
ARROW = ' The arrowheads (sharp silver points) face forward toward the target; the white feathers are at the back, at the bowstring.'
EFFECTS = [
    ('🎯 เป้าติดหัวปีศาจ (ใช้กับทุกตัว)', 'เปิด Loop · 64×64 · 12 เฟรม',
     'Small red-orange target reticle circle with crosshair marks, rotating slowly and pulsing, looping, pixel art'),
    ('🐒 หงอคง · กระบองยืดฟาด', 'ปิด Loop · 96×128 · 16 เฟรม',
     'A giant golden staff with a red middle shaft shoots down from the top of the frame, growing long very fast, and slams into the ground at the bottom. '
     'On impact: a wide golden shockwave ring on the ground, short cracks, orange sparks and dust bursting out. Then the staff shrinks back up and everything fades. Snappy and powerful, pixel art, no background.'),
    ('🐍 โลกิ · พิษเขี้ยวงู', 'ปิด Loop · 64×64 · 12 เฟรม',
     'Green snake-fang poison splash: two quick bite marks, venom droplets spray out and drip, snappy'),
    ('🌙 อาร์เทมิส · ศรจันทร์ (ใส่ลูกธนูในช่อง Projectile)', 'ปิด Loop · 128×64 · 16 เฟรม',
     'The arrow flies to the right trailing a silver-blue moonlight streak, and bursts into a crescent-moon flash with pale blue sparkles on impact'),
    ('⚡ โอดิน · สายฟ้ารูน', 'ปิด Loop · 64×96 · 16 เฟรม',
     'Blue lightning strike from above with a glowing rune circle on the ground, crackling sparks'),
    ('☀️ อพอลโล · แสงอาทิตย์', 'ปิด Loop · 96×96 · 16 เฟรม',
     'Golden sun burst with rays spinning outward and small music notes floating up'),
    ('𓂀 อนูบิส · คำสาปดูอัต', 'ปิด Loop · 96×96 · 16 เฟรม',
     'Dark teal curse: a glowing eye-of-Horus sigil appears on the ground, black and teal smoke rises and swirls, then fades, snappy'),
]

def desc(c):
    k, en, th, tier, job, who, look, face, head, body, back, weapon, pose, sil, pal = c
    return ('Chibi ' + en + ', ' + who + '. Original design, not a copy of any existing game, film or comic version.\n\n'
            'Body: chibi proportions, big head about one third of the height, ' + pose + '.\n'
            'Face: ' + look + ', ' + face + '. Both eyes bright and clearly visible' + (' (the eye patch is the only exception)' if k == 'god_mage' else '') + '.\n'
            'Head: ' + head + '.\nClothing: ' + body + '.\nBack: ' + back + '.\nWeapon: ' + weapon + '.\n'
            'Must read as ' + en + ' at a glance: ' + sil + '.\n'
            'Colours: ' + ', '.join(n for n, h in pal) + '.\n'
            'Style: clean pixel art, dark outline, rich shading, ' + ('divine gold ornament, ' if tier == 'god' else '') + 'game character sprite.')

def steps(L): return ', then '.join(s.rstrip('.') for s in L)

def anim(a, which):
    k, en, th, d, idle, an, asteps, sn, swhat, ssteps = a[:10]; extra = a[10] if len(a) > 10 else ''
    ok = extra and 'cell' not in extra and 'flying arrows' not in extra
    if which == 'atk':
        t = en + ' ' + an + ': ' + steps(asteps) + '. Big clear movement, feet stay planted, the weapon keeps its normal size.'
    else:
        t = en + ' ultimate "' + sn.split(' (')[0] + '" (' + swhat + '): ' + steps(ssteps) + '. Big clear movement, every pose different.'
    if 'hunter' in k: t += ARROW
    if ok: t += ' ' + extra
    return t

out = 'docs/pixellab'; os.makedirs(out, exist_ok=True)
for c in C:   # style picture + palette for every character
    k = c[0]
    if not os.path.exists(os.path.join(out, k + '_front_128.png')):
        subprocess.run([sys.executable, '-I', 'tools/art/pixellab_pack.py', k, out], check=True, capture_output=True)
        for f in os.listdir(out):
            if f.startswith(k) and not f.endswith(('_front_128.png', '_palette.png')): os.remove(os.path.join(out, f))
hexes = {}
for c in C:
    k = c[0]; t = subprocess.run([sys.executable, '-I', 'tools/art/pixellab_pack.py', k, '/tmp/plpk_' + k], capture_output=True, text=True).stdout.splitlines()
    hexes[k] = t[1] if len(t) > 1 else ''
CC = {c[0]: c for c in C}; AA = {a[0]: a for a in ANIM}
e = html.escape
def block(title, text, rows=4):
    return ('<div class="blk"><div class="bh"><b>' + title + '</b><button type="button" class="cp">คัดลอก</button></div>'
            '<textarea readonly rows="' + str(rows) + '">' + e(text) + '</textarea></div>')
cards = []
for k in ORDER:
    c = CC[k]; a = AA[k]; st = STATUS.get(k, set())
    chip = lambda n, l: '<span class="chip ' + ('ok' if n in st else 'todo') + '">' + ('✅ ' if n in st else '⬜ ') + l + '</span>'
    later = k.startswith('hero')
    cards.append('<section class="card' + (' later' if later else '') + '"><div class="top"><img src="pixellab/' + k + '_front_128.png" alt="">'
                 '<div><h2>' + e(c[2]) + ' <small>' + e(c[1]) + (' · วีรชน (ทำทีหลัง)' if later else ' · เทพ') + '</small></h2>'
                 '<div class="chips">' + chip('char', 'ตัวละคร') + chip('atk', 'ท่าตี') + chip('sk', 'ท่าไม้ตาย') + '</div>'
                 + ('<p class="note">' + e(NOTE[k]) + '</p>' if k in NOTE else '') +
                 '<p class="dl"><a href="pixellab/' + k + '_front_128.png" download>⬇ รูปตัวอย่าง</a> · <a href="pixellab/' + k + '_palette.png" download>⬇ แถบสี</a></p></div></div>'
                 + ('' if 'char' in st else block('1. สี (Paste hex colours)', hexes[k], 2) + block('2. คำบรรยายตัวละคร (Character Description)', desc(c), 9))
                 + ('' if 'atk' in st else block('3. ท่าตี (Custom Animation)', anim(a, 'atk'), 4))
                 + ('' if 'sk' in st else block('4. ท่าไม้ตาย (Custom Animation)', anim(a, 'sk'), 4)) + '</section>')
fx = ''.join('<section class="card fx"><h2>' + e(t) + '</h2><p class="note">' + e(s) + '</p>' + block('คำสั่ง (ช่อง Chat)', p, 3) + '</section>' for t, s, p in EFFECTS)
page = '''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PixelLab Jobs</title><style>
:root{--bg:#14121c;--card:#1f1c2b;--ink:#ece8f6;--dim:#a39cb8;--line:#3a3550;--ok:#4cc98a;--todo:#e0a040;--acc:#c8a8ff}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f2f8;--card:#fff;--ink:#1d1a26;--dim:#615a74;--line:#d8d2e6;--ok:#1f8f57;--todo:#a8650a;--acc:#6a3fc8}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Kanit,system-ui,sans-serif;padding:16px}
main{max-width:860px;margin:0 auto}h1{font-size:22px;margin:4px 0 8px}h2{font-size:18px;margin:0 0 6px}h2 small{color:var(--dim);font-weight:400;font-size:13px}
.steps{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 16px;margin:0 0 14px}.steps li{margin:3px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:0 0 14px}.card.later{opacity:.85}
.top{display:flex;gap:12px;align-items:flex-start}.top img{width:96px;height:96px;image-rendering:pixelated;background:#fff;border-radius:8px;flex:none}
.chips{display:flex;gap:6px;flex-wrap:wrap}.chip{font-size:12px;border:1px solid var(--line);border-radius:99px;padding:1px 8px}.chip.ok{color:var(--ok)}.chip.todo{color:var(--todo)}
.note{color:var(--dim);font-size:13px;margin:6px 0 0}.dl{font-size:13px;margin:6px 0 0}a{color:var(--acc)}
.blk{margin-top:10px}.bh{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:14px;margin-bottom:4px}
textarea{width:100%;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px;font:12.5px/1.45 ui-monospace,Menlo,monospace;resize:vertical}
button.cp{background:var(--acc);color:#fff;border:0;border-radius:6px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}button.cp.done{background:var(--ok)}
h1+p{color:var(--dim);margin:0 0 12px}.sec{margin:22px 0 10px;font-size:19px}
</style></head><body><main>
<h1>งาน PixelLab ที่เหลือ</h1><p>ทำทีละตัวจากบนลงล่าง กดคัดลอกแล้ววางในช่องของ PixelLab ได้เลย ได้ไฟล์แล้วส่งให้ Claude</p>
<ol class="steps">
<li><b>ตัวละคร:</b> Create Character · ขนาด <b>128×128</b> · Style image = รูปตัวอย่างของตัวนั้น (ปุ่ม ⬇) · กล้อง <b>Low Top-Down</b> · สี = Paste hex colours (ข้อ 1) · คำบรรยาย = ข้อ 2</li>
<li><b>ท่าตี / ท่าไม้ตาย:</b> Custom Animation · <b>PixMiniMax</b> · ทิศ <b>south-east</b> (เฉียงหน้าขวา) ทิศเดียว · <b>24</b> ภาพ · วางข้อ 3 หรือ 4</li>
<li><b>ส่งให้ Claude:</b> ดาวน์โหลด ZIP (all frames) หรือ GIF ของท่านั้น · ท่ายืนไม่ต้องทำ เกมทำให้ตัวหายใจเอง · ซ้าย = เกมพลิกให้</li>
</ol>
''' + ''.join(cards) + '''<h2 class="sec">✨ เอฟเฟกต์สกิล (หน้า Effect Creator)</h2><p class="note" style="margin:0 0 10px">พิมพ์ในช่อง Chat · ช่อง Your sprite ใส่ตัวละครไว้ดูขนาดได้ · ดาวน์โหลดแบบ <b>For a game (ZIP)</b></p>
''' + fx + '''</main><script>
document.addEventListener('click',e=>{const b=e.target.closest('button.cp');if(!b)return;const t=b.closest('.blk').querySelector('textarea');
const done=()=>{b.textContent='คัดลอกแล้ว ✓';b.classList.add('done');setTimeout(()=>{b.textContent='คัดลอก';b.classList.remove('done')},1500)};
try{navigator.clipboard.writeText(t.value).then(done,()=>{t.select();document.execCommand('copy');done()})}catch(_){t.select();document.execCommand('copy');done()}});
</script></body></html>'''
open('docs/pixellab.html', 'w', encoding='utf-8').write(page)
print('docs/pixellab.html', len(page), 'bytes;', sorted(os.listdir(out)))
