#!/usr/bin/env python3
"""clash.html moves from PixelLab (owner 2026-11-23 "มันไม่ขยับอยู่ดี เจน20เครดิตมาสิ"): animate_image_pixminimax on our own
pixel units (art/clash/units/<key>.png) padded onto a 68 x 68 canvas (just over the 64 price step: up to 16 frames = 1 generation),
side view facing east, feet 4 px above the bottom, body a little left of centre so a lunge has room.
  python3 tools/art/clash_anim.py prep                 -> art/incoming/clash/anim/<key>_in.png (free)
  python3 tools/art/clash_anim.py go <key:move> ...    -> sends the jobs (PAID, 1 each), job ids in jobs.json
  python3 tools/art/clash_anim.py fetch                -> frames to art/incoming/clash/anim/<key>_<move>/f00.png (f00 = our input)"""
import base64, json, os, sys, time, urllib.request
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools')); os.environ.setdefault('PL_KEY', 'proxy-injected')
OUT = os.path.join(ROOT, 'art/incoming/clash/anim'); C = 68; FOOT = 64
SUBJ = {
 'm_saw': 'a small grey robot warrior with a circular saw arm', 'm_shield': 'a bulky grey robot holding a glowing cyan energy shield',
 'a_wolf': 'a brown wolf warrior on four legs with green war paint', 'a_rhino': 'an armoured grey rhino with bone plates',
 'e_psychic': 'a small teal big-headed alien holding a pink glowing orb', 'e_jelly': 'a big teal jelly blob with one eye',
 'h_spear': 'a small soldier with a red-plumed helmet and a long spear', 'h_archer': 'a hooded archer holding a bow',
 'd_imp': 'a small red flying imp with bat wings and a pitchfork', 'd_brute': 'a big red horned demon brute with lava cracks',
 'g_angel': 'a winged angel knight with a glowing sword', 'g_titan': 'a big stone titan golem with gold runes'}
MOVE = {
 'attack': {'m_saw': 'swings the spinning saw arm forward to the right in a fast cut, sparks fly, then returns to stance',
   'm_shield': 'bashes forward to the right with the energy shield, then steps back to stance',
   'a_wolf': 'lunges forward to the right and bites, snapping its jaws, then lands back in stance',
   'a_rhino': 'lowers its head and rams forward to the right with its horn, then steps back',
   'e_psychic': 'raises the orb and fires a pink psychic blast forward to the right, then lowers it',
   'e_jelly': 'squashes down and slams its body forward to the right, wobbling, then reforms',
   'h_spear': 'thrusts the long spear forward to the right with a quick lunge, then pulls back to stance',
   'h_archer': 'draws the bow, aims to the right and releases an arrow, then lowers the bow',
   'd_imp': 'flaps its wings and stabs forward to the right with the pitchfork, then hovers back',
   'd_brute': 'raises both fists and smashes them down in front of it to the right, then straightens up',
   'g_angel': 'swings the glowing sword in a wide slash forward to the right, wings flaring, then returns',
   'g_titan': 'lifts a huge stone fist and pounds the ground in front of it to the right, then stands up'},
 'walk': {'a_wolf': 'running forward to the right in place, four legs galloping, a looping run cycle',
   'h_spear': 'marching forward to the right in place, legs stepping, spear held upright, a looping walk cycle',
   'm_saw': 'walking forward to the right in place with heavy robot steps, a looping walk cycle',
   'd_imp': 'flying in place, flapping its bat wings up and down, bobbing, a looping flight cycle',
   'g_angel': 'hovering in place, flapping its white wings, sword ready, a looping flight cycle',
   'h_archer': 'walking forward to the right in place, legs stepping, bow in hand, a looping walk cycle'}}
FRAMES = {'attack': 12, 'walk': 8}

def prep():
    for k in SUBJ:
        im = Image.open(os.path.join(ROOT, 'art/clash/units', k + '.png')).convert('RGBA'); w, h = im.size
        c = Image.new('RGBA', (C, C), (0, 0, 0, 0)); x = max(2, min(C - w - 2, 30 - w // 2)); c.paste(im, (x, FOOT - h), im)
        c.save(os.path.join(OUT, k + '_in.png')); print(k, 'at', x, FOOT - h)

def go(items):
    from pl_rpc import call
    jf = os.path.join(OUT, 'jobs.json'); jobs = json.load(open(jf)) if os.path.exists(jf) else {}
    for it in items:
        k, mv = it.split(':'); b = base64.b64encode(open(os.path.join(OUT, k + '_in.png'), 'rb').read()).decode()
        args = {'description': MOVE[mv][k], 'frame_count': FRAMES[mv], 'first_frame_url': 'data:image/png;base64,' + b, 'no_background': True,
                'direction': 'east', 'view': 'side', 'subject_description': SUBJ[k], 'initial_pose': 'standing in a ready stance facing right'}
        r = call('animate_image_pixminimax', args); print(it, r[:400]); jid = next((w.strip(' .,:') for w in r.replace('\n', ' ').split() if len(w.strip(' .,:')) == 36 and w.count('-') == 4), None)
        jobs[it] = {'job': jid, 'reply': r[:600], 'at': time.strftime('%Y-%m-%d %H:%M')}; json.dump(jobs, open(jf, 'w'), indent=1)

def fetch():
    from pl_rpc import call
    jobs = json.load(open(os.path.join(OUT, 'jobs.json')))
    for it, j in jobs.items():
        k, mv = it.split(':'); d = os.path.join(OUT, f'{k}_{mv}')
        if os.path.exists(os.path.join(d, 'f00.png')) or not j.get('job'): continue
        r = call('get_image', {'job_id': j['job']}); n = next((int(l.split(':')[1]) for l in r.splitlines() if l.startswith('frames:')), 0)
        if 'status: completed' not in r or not n: print(it, 'not ready:', r[:160]); continue
        base = f"https://api.pixellab.ai/mcp/images/{j['job']}/download?index="; os.makedirs(d, exist_ok=True); urls = [base + str(i) for i in range(n)]
        for i, u in enumerate(urls): open(os.path.join(d, f'f{i:02d}.png'), 'wb').write(urllib.request.urlopen(u, timeout=60).read())
        print(it, len(urls), 'frames ->', d)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'prep': prep()
    elif cmd == 'go': go(sys.argv[2:])
    elif cmd == 'fetch': fetch()
