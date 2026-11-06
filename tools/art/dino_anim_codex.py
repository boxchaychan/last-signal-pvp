# Builds the Codex package for the prehistoric forms' attack animations (owner 2026-11-06: "คำสั่งมาเลย จะเอาเข้า codex").
# Uses the owner's skill https://github.com/tachikomared/character-animation-creator-skill ($game-character-sprites).
# Output: docs/codex/dino_anim/ (COMMANDS.md, README_TH.txt, refs/) + docs/codex/dino_anim_codex.zip
# Run from the repo root: python3 tools/art/dino_anim_codex.py
import os, shutil, zipfile
from PIL import Image

OUT = 'docs/codex/dino_anim'
KIDS = [
 ('assassin', 'Nin', 'girl', 'velociraptor', 'two curved sickle-claw daggers in a reverse grip',
  ['standing pose, both claw daggers ready (same as the reference)',
   'crouch low, both daggers pulled back by the hips, weight on the back foot',
   'spring forward, the front foot stepping ahead, both arms coming forward',
   'cross slash: both claw daggers slash across in front of her in an X, body stretched forward',
   'follow-through: arms crossed past the body, the feathered tail cape flaring behind',
   'step back and return to the standing pose'],
  'Keep the reverse grip in every frame: a ring on top of each fist, the curved blade coming out of the bottom of the fist and curving back toward her body.'),
 ('hunter', 'Fah', 'girl', 'pteranodon', 'a big longbow made of pteranodon wing bones',
  ['standing pose with the bow held forward and an arrow nocked (same as the reference)',
   'raise the bow and start pulling the string back',
   'full draw: the string pulled back to her cheek, the bow bent, aiming straight ahead',
   'release: the string snaps forward, the arrow is gone from the bow, a small recoil',
   'follow-through: the bow arm stays forward, the wing cape flutters',
   'reach to the quiver for a new arrow and return to the standing pose'],
  'Do not draw the flying arrow: the game draws the shot itself.'),
 ('mage', 'Ratri', 'girl', 'stegosaurus', 'a tall staff topped with a glowing violet crystal',
  ['standing pose with the staff planted on the ground (same as the reference)',
   'lift the staff up in front of her, the free hand rising',
   'staff raised high, the crystal on the staff and the crystal plates on her hood and cape glowing brighter',
   'thrust the staff forward, pointing the crystal at the enemy in front of her, a small step forward',
   'hold the thrust, the crystals at their brightest',
   'lower the staff and return to the standing pose'],
  'Only the crystals that are part of the costume glow; do not draw magic bolts or sparks flying away: the game draws the spell itself.'),
 ('support', 'Chan', 'boy', 'triceratops', 'a healing staff topped with a glowing pink crystal horn, and a small round frill shield',
  ['standing pose with the staff upright and the shield on his arm (same as the reference)',
   'raise the frill shield in front of him and lift the staff back over his shoulder',
   'step forward behind the shield, the staff at the top of the swing',
   'swing the staff down and forward so the pink crystal horn points at the enemy in front of him, the shield pushed forward',
   'follow-through, the crystal glowing brightest',
   'return to the standing pose'],
  'Only the crystal that is part of the staff glows; do not draw heal bolts or sparks flying away: the game draws them itself.'),
 ('curse', 'Mok', 'girl', 'spinosaurus', 'a jaw-bone staff topped with a glowing purple eye orb',
  ['standing pose with the staff held at her side (same as the reference)',
   'lean back, raise the staff, the free hand curling like a claw',
   'the sail on her back spreads up taller and its purple veins glow brighter, the staff held high',
   'thrust the staff forward, pointing the eye orb at the enemy in front of her, the free hand pushing forward',
   'hold the cast, the eye orb and the sail veins at their brightest',
   'lower the staff and return to the standing pose'],
  'Only the eye orb and the sail veins that are part of the costume glow; do not draw curse bolts or smoke flying away: the game draws the curse itself.'),
]

def command(i, k):
    cls, en, he, cr, weapon, frames, extra = k
    his = 'his' if he == 'boy' else 'her'
    steps = '\n'.join('  %d. %s' % (n + 1, f) for n, f in enumerate(frames))
    return ('Use $game-character-sprites.\n'
        'Reference: the attached picture refs/%02d_%s_%s.png (%s in %s armour, holding %s). Keep the exact same character, face, hair, outfit, colours and weapon in every frame.\n'
        'Scope: cell 128x128 only. 4 directions, in this order: south (facing the viewer), east (facing right, the same three-quarter view as the reference), north (back to the viewer), west (facing left). '
        'Actions for EACH direction: idle (4 frames) and attack (6 frames). No walk, no other sizes.\n'
        'The reference shows the east view. For south, north and west, turn the same character to face that way and keep every costume part the same (dinosaur helmet head, armour, cape, weapon, colours).\n'
        'Idle: gentle breathing, the feet do not move.\n'
        'Attack, 6 frames, the same beats in every direction, aimed the way that direction faces (south = toward the viewer, north = away, east = right, west = left):\n%s\n'
        '%s\n'
        'Keep both feet on the same ground line in every frame (a forward step is fine). Keep the whole body, cape and weapon inside the frame.\n'
        'No detached effects, no dust, no shadows, transparent background.\n'
        'Save the results in a folder named dino_%s.') % (i, en.lower(), cr, en, cr, weapon, steps, extra, cls)

ALL_HEAD = ('Use $game-character-sprites for 5 separate characters, one after another. The reference pictures are in refs/. '
    'Do each character as its own job with its own run folder (run_assassin, run_hunter, run_mage, run_support, run_curse) and finish one before starting the next. '
    'All five share the same rules: cell 128x128 only, 4 directions (south, east, north, west), idle 4 frames + attack 6 frames for each direction, no walk, transparent background, no detached effects, no dust, no shadows.\n\n'
    'When all five are done, zip EVERYTHING into one file dino_anim.zip: every run folder in full, including the full-size raw images in source/ and generated/, the clean sheets, and the GIF previews. '
    'Also put in the zip one large preview picture per character showing all its rows (idle and attack for each of the 4 directions, as large as you can). Do not shrink anything.\n\n')

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/refs')
    for i, k in enumerate(KIDS, 1):
        im = Image.open('art/bb/dino_%s.png' % k[0]).convert('RGBA'); s = 6
        big = im.resize((im.width * s, im.height * s), Image.NEAREST)
        bg = Image.new('RGBA', (big.width + 72, big.height + 72), (255, 255, 255, 255)); bg.alpha_composite(big, (36, 36))
        bg.convert('RGB').save(OUT + '/refs/%02d_%s_%s.png' % (i, k[1].lower(), k[3]), optimize=True)
    md = ['# Attack animations for the 5 prehistoric forms, 4 directions (Codex + $game-character-sprites)\n',
          'Skill: https://github.com/tachikomared/character-animation-creator-skill (install it first: "Install this skill: <link>").\n',
          '## A. All five in one go (paste this, with the whole refs/ folder attached)\n', '```', ALL_HEAD + '\n\n'.join(command(i, k) for i, k in enumerate(KIDS, 1)), '```\n',
          '## B. One at a time (attach only that character\'s picture)\n']
    for i, k in enumerate(KIDS, 1):
        md += ['### %d. %s - %s\n' % (i, k[1], k[3]), '```', command(i, k) + '\nWhen done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of all rows (idle and attack for each of the 4 directions). Do not shrink anything.', '```\n']
    open(OUT + '/COMMANDS.md', 'w', encoding='utf-8').write('\n'.join(md))
    open(OUT + '/README_TH.txt', 'w', encoding='utf-8').write(
        'ท่าโจมตีฟอร์มดึกดำบรรพ์ 5 ตัว (นิล ฟ้า ราตรี จันทร์ หมอก) 4 ทิศ (ล่าง ขวา บน ซ้าย) ด้วย Codex + สกิล game-character-sprites\r\n'
        'ทิศ: south = หันหน้าเข้าจอ (ล่าง) · east = หันขวา · north = หันหลัง (บน) · west = หันซ้าย · แต่ละทิศมีท่ายืน 4 + ท่าโจมตี 6\r\n\r\n'
        '1. ถ้า Codex ยังไม่มีสกิล: พิมพ์ Install this skill: https://github.com/tachikomared/character-animation-creator-skill\r\n'
        '2. แตก zip นี้ แนบทั้งโฟลเดอร์ (หรือแนบรูปทั้ง 5 ใน refs) ให้ Codex\r\n'
        '3. เปิด COMMANDS.md ก๊อปคำสั่งข้อ A (ทำทีเดียว 5 ตัว) ไปวาง\r\n'
        '   ถ้ามันทำทีเดียวไม่ไหว ใช้ข้อ B ทีละตัว (แนบแค่รูปของตัวนั้น)\r\n'
        '4. ได้ zip กลับมา ส่งให้ Claude ในแชตได้เลย (อย่าย่อรูป) Claude จะใส่ท่าเข้าเกมให้\r\n')
    z = 'docs/codex/dino_anim_codex.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, fs in os.walk(OUT):
            for f in sorted(fs):
                p = os.path.join(root, f); zf.write(p, os.path.join('dino_anim', os.path.relpath(p, OUT)))
    print('wrote', OUT, z, os.path.getsize(z))

if __name__ == '__main__':
    main()
