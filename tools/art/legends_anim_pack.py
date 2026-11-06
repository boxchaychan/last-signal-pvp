# One zip per character for the animation job (owner 2026-11-06: "ทำเป็นไฟล์ บวกรูปบวกพรอมต์ ... เอาเป็นตัวๆ"):
# the reference picture + the prompt + Thai steps, so the owner attaches ONE file to Codex and types one line.
#   python3 tools/art/legends_anim_pack.py <out dir> [--4dir] [key ...]        (default: every character, facing right only)
# One direction is the default: the 4-direction try for Wukong (2026-11-06) came back half done (no skill, no south/north,
# the generator could not turn him), while the one-direction runs (Loki, Wukong) came back complete.
# Reads the prompts written by legends_codex.py (docs/codex/legends/prompts/anim_XX_<key>[_4dir].txt), so run that first after changes.
import sys, os, glob, zipfile

out = sys.argv[1]; dirs = '--4dir' in sys.argv; want = [a for a in sys.argv[2:] if a != '--4dir']
os.makedirs(out, exist_ok=True)
for pf in sorted(glob.glob('docs/codex/legends/prompts/anim_*.txt')):
    if pf.endswith('_4dir.txt') != dirs: continue
    num, key = os.path.basename(pf)[5:7], os.path.basename(pf)[8:-9 if dirs else -4]
    if want and key not in want: continue
    head, body = open(pf, encoding='utf-8').read().split('\n\n', 1)
    name = head.split('\n')[0].strip('= ').split(' animation')[0]
    body = body.replace('Reference: the attached picture (', 'Reference: the attached picture %s (' % (key + '.png'), 1)
    prompt = ('Files in this package: %s.png = the reference picture (the final design of this character). PROMPT.txt = this job.\n\n' % key) + body
    readme = ('ท่าเคลื่อนไหว: %s\r\n\r\n'
              'วิธีใช้ใน Codex (ต้องติดตั้งสกิล $game-character-sprites แล้ว):\r\n'
              '1. แนบไฟล์ zip นี้ทั้งไฟล์\r\n'
              '2. พิมพ์: ทำตาม PROMPT.txt ใช้รูป %s.png เป็นต้นแบบ\r\n'
              '3. เสร็จแล้วดาวน์โหลด zip ที่ Codex ให้มา ส่งให้ Claude ทั้งไฟล์ (ห้ามย่อ)\r\n\r\n'
              + ('ได้: 3 ทิศ (ล่าง ขวา บน) x ท่ายืน 4 + ท่าตี 6 + ท่าไม้ตาย 6 / ทิศซ้ายเกมกลับด้านจากขวาให้เอง\r\n' if dirs else
                 'ได้: หันขวา ท่ายืน 4 + ท่าตี 6 + ท่าไม้ตาย 6 (หันซ้ายเกมกลับภาพให้เอง)\r\n')) % (name, key)
    zp = os.path.join(out, 'anim_%s_%s.zip' % (num, key))
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write('art/incoming/legends/%s.png' % key, key + '.png')
        z.writestr('PROMPT.txt', prompt + '\n')
        z.writestr('README_TH.txt', readme.encode('utf-8-sig'))
    print(zp, os.path.getsize(zp))
