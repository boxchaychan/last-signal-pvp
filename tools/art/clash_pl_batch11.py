"""clash.html batch 11 = GOD TRIBE test in TRUE 16-bit (owner 2026-11-24 "ลองเทสเอาเผ่าพระเจ้า", after "ตอนสั่ง pixlab ได้กำหนดไหมว่า 16 bit":
earlier batches never asked for it and came back with ~50 colours a sprite). 64 DIFFERENT god-tribe units at 32 px (our soldiers' size), side view
facing right, all 8 classes, "16-bit console pixel art" in the text AND max_colors = 16. Style pictures = 4 god units from batch 1 + 4 crisp picks
of ours (NOT a previous batch together with the same list: batch 10 lesson). 64 x 32 px = 10 generations. Dry run by default; `--go` sends."""
import json, base64, sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch11')
K = 'god-tribe divine warrior, 16-bit console pixel art, chibi proportions, white and gold armour with light blue holy glow, bold dark outline, few flat colours, majestic and fierce'
CL = {
 'tank': ['golden titan guardian with a tower shield', 'marble colossus with a stone shield', 'holy paladin with a sun emblem shield', 'heavy angel knight with a great shield',
   'bronze gate guardian with a spiked shield', 'lion-headed temple guardian with a mace', 'crystal golem glowing blue', 'sphinx-helmed warden with a halberd'],
 'warrior': ['valkyrie with a winged helmet and a spear', 'thunder warrior with a lightning hammer', 'angel swordsman with a flaming sword', 'sun-blade warrior with a curved golden sword',
   'war goddess with a sword and a round shield', 'six-winged seraph with twin blades', 'centurion of light with a long spear', 'storm giant warrior with a great axe',
   'celestial monk with glowing fists', 'griffin-helmed knight with a lance'],
 'assassin': ['winged messenger with a dagger and winged sandals', 'moon huntress with crescent blades', 'star assassin with a glowing dagger', 'mirage djinn with a scimitar',
   'owl-masked silent killer', 'comet striker with a trailing light tail', 'light blade dancer with ribbons', 'masked judge with a hidden blade'],
 'shooter': ['sun archer with a golden bow', 'moon archer with a silver bow', 'cherub archer with tiny wings', 'valkyrie javelin thrower', 'angel with a crystal crossbow',
   'seraph with a star sling', 'herald shooting light from a golden horn', 'eagle-winged ranger with a longbow', 'storm archer with a lightning bow', 'priest throwing light orbs'],
 'mage': ['sun mage with a radiant staff', 'oracle with a floating blue crystal', 'star sorceress with a starry robe', 'time keeper with an hourglass staff',
   'thunder god caster with sparks', 'frost goddess with an ice wand', 'prism wizard with rainbow light', 'rune scholar with a floating book',
   'celestial dragon priest', 'aurora mage with waving lights'],
 'support': ['healing angel with green-gold light', 'priestess with a golden harp', 'sun priest with a swinging censer', 'herald of light with a war trumpet and banner',
   'harvest goddess with wheat and a sickle', 'temple monk with a holy bell', 'mother goddess with a lantern', 'cherub healer with a little staff'],
 'rider': ['knight riding a pegasus', 'charioteer of the sun on a small golden chariot', 'valkyrie on a winged horse', 'rider on a golden lion', 'rider on a white elephant', 'rider on a celestial stag'],
 'special': ['golden phoenix avatar', 'living sun spirit', 'sphinx sage', 'floating eye of light guardian'],
}
items, keys, names = [], [], {}
for cls, lst in CL.items():
    for d in lst:
        k = f'c11_{len(keys):02d}'; items.append(f'{K}, {d}, side view facing right, full body'); keys.append(k); names[k] = f'{cls}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['batch1/raw/40_g_lightwar_1', 'batch1/raw/42_g_lightarcher_1', 'batch1/raw/44_g_oracle_1', 'batch1/raw/46_g_healer_1', 'batch3/raw/k3_02', 'batch3/raw/k3_14', 'batch7/raw/m7_18', 'batch3/raw/k3_10']
def clean(f):   # drop bits of the NEIGHBOUR cell at the slot edge (style copy only)
    a = np.asarray(Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA')).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 24 and (xs.min() == 0 or ys.min() == 0 or xs.max() == a.shape[1] - 1 or ys.max() == a.shape[0] - 1): a[lab == i] = 0
    b = io.BytesIO(); Image.fromarray(a).save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()
style = [{'type': 'base64', 'base64': clean(f), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body', 'name': 'clash god tribe 16-bit batch 11', 'view': 'sidescroller',
        'style_images': style, 'item_descriptions': items, 'max_colors': 16}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'god-tribe units, all different, max 16 colours; dry run')
