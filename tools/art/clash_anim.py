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
# the human knights (owner 2026-11-23 "เอาไปเจนท่าเลยทั้งหมดที่พูดมา"): picks from batch 3 (k3_02 18 20 07 14 10) and batch 2 (33 32 44)
SUBJ.update({'hk_tank': 'a small bronze knight with a tall tower shield and a short sword', 'hk_samurai': 'a small red samurai knight with a katana',
 'hk_bat': 'a small dark knight with a bat-wing helmet and two daggers', 'hk_ranger': 'a small hooded ranger knight with a longbow',
 'hk_mage': 'a small blue hooded mage knight with a crystal staff', 'hk_banner': 'a small knight captain holding a tall blue war banner',
 'hk_glaive': 'a small silver knight with a unicorn-horn helmet and a glaive', 'hk_rider': 'a small knight riding a brown horse, holding a lance',
 'hk_blood': 'a small crimson knight with a long whip sword'})
MOVE['attack'].update({'hk_tank': 'bashes forward to the right with the tower shield and stabs with the short sword, then steps back to stance',
 'hk_samurai': 'swings the katana in a fast horizontal slash forward to the right, then returns to stance',
 'hk_bat': 'dashes forward to the right and slashes with both daggers in a quick cross cut, then hops back to stance',
 'hk_ranger': 'draws the longbow fully, aims to the right and releases an arrow, then lowers the bow',
 'hk_mage': 'raises the crystal staff and casts a blue magic bolt forward to the right, then lowers the staff',
 'hk_banner': 'swings the war banner forward to the right in a rallying sweep, the flag waving, then plants it again',
 'hk_glaive': 'swings the glaive in a wide forward arc to the right, then returns to stance',
 'hk_rider': 'the horse rears up and the knight thrusts the lance forward to the right, then the horse settles',
 'hk_blood': 'lashes the whip sword forward to the right in a long snaking strike, then pulls it back'})
MOVE['walk'].update({'hk_tank': 'marching forward to the right in place behind the tower shield, legs stepping, a looping walk cycle',
 'hk_samurai': 'walking forward to the right in place, katana held ready, legs stepping, a looping walk cycle',
 'hk_bat': 'sneaking forward to the right in place, crouched low with daggers ready, a looping walk cycle',
 'hk_ranger': 'walking forward to the right in place, longbow in hand, legs stepping, a looping walk cycle',
 'hk_mage': 'walking forward to the right in place, robe swaying, staff in hand, a looping walk cycle',
 'hk_banner': 'marching forward to the right in place holding the banner upright, the flag waving, a looping walk cycle',
 'hk_glaive': 'marching forward to the right in place, glaive held upright, a looping walk cycle',
 'hk_rider': 'the horse gallops in place to the right, legs moving, rider bouncing, a looping gallop cycle',
 'hk_blood': 'walking forward to the right in place, whip sword trailing, a looping walk cycle'})
FRAMES = {'attack': 12, 'walk': 8}

# alien tribe (owner 2026-11-23 picks from batch 4: a4_12 00 07 29 34 19 55 45; "เจนท่า")
SUBJ.update({'ax_tank': 'a dark red armoured alien brute with big crab claws', 'ax_hunter': 'an alien hunter with a bone-white skull mask and an energy spear',
 'ax_hound': 'an eyeless black and toxic green alien hound with huge jaws', 'ax_assassin': 'a black cyborg alien assassin with two magenta energy blades',
 'ax_eye': 'a shadow tentacle horror with one huge glowing cyan eye', 'ax_priestess': 'a purple alien hive priestess with long antennae and a glowing staff',
 'ax_saucer': 'an alien riding a small spiked flying saucer', 'ax_tk': 'a purple telekinetic alien surrounded by floating rocks'})
MOVE['attack'].update({'ax_tank': 'snaps forward to the right with both huge crab claws, then pulls back',
 'ax_hunter': 'lunges forward to the right and thrusts the energy spear, then pulls back to stance',
 'ax_hound': 'pounces forward to the right and snaps its huge jaws, then lands back',
 'ax_assassin': 'dashes forward to the right and slashes with both energy blades in a fast cross cut, then hops back',
 'ax_eye': 'the huge eye glows and fires a cyan beam forward to the right, tentacles writhing, then dims',
 'ax_priestess': 'raises the glowing staff and sends a pulse of purple energy forward to the right, then lowers it',
 'ax_saucer': 'the spiked saucer rams forward to the right, spinning its spikes, then pulls back',
 'ax_tk': 'raises both hands and hurls a floating rock forward to the right with a purple aura, then the rocks circle again'})
MOVE['walk'].update({'ax_tank': 'stomping forward to the right in place on heavy legs, claws swaying, a looping walk cycle',
 'ax_hunter': 'stalking forward to the right in place, spear ready, a looping walk cycle',
 'ax_hound': 'running forward to the right in place on four legs, a looping run cycle',
 'ax_assassin': 'sneaking forward to the right in place, blades ready, a looping walk cycle',
 'ax_eye': 'slithering forward to the right in place on writhing tentacles, a looping crawl cycle',
 'ax_priestess': 'gliding forward to the right in place, robe swaying, staff in hand, a looping walk cycle',
 'ax_saucer': 'the saucer hovers and bobs in place, lights blinking, a looping hover cycle',
 'ax_tk': 'walking forward to the right in place, floating rocks circling around it, a looping walk cycle'})

def prep(only=None):
    for k in (only or SUBJ):
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
    if cmd == 'prep': prep(sys.argv[2:] or None)
    elif cmd == 'go': go(sys.argv[2:])
    elif cmd == 'fetch': fetch()
