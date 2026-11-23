"""clash.html batch 8 = COMMANDERS (owner 2026-11-23 "ตัวแรกฝั่งคนอยากทำลิโป้ ขี่ม้า ของคาสไรเดอร์": slots c8_00, c8_02, c8_10 = 3 different
Lu Bu style mounted warlords for the human RIDER commander, described by look only: own design, no game's version copied); (owner 2026-11-23 "กำหนดตัวแปรชัยชนะ โดยเพิ่มแม่ทัพ" -> picked "เจนใหม่ด้วย PixelLab"):
64 DIFFERENT army commanders for all 6 tribes (human 12, alien 11, animal 11, machine 10, demon 10, god 10), own designs, public-domain myths only.
Slot = 32 px, the SAME size as the soldiers (owner "เอาไม่ต้องใหญ่ มาพอๆกับทหาร"): the style pictures are 32 px fierce sprites from batches 3 / 4 / 6 / 7
(the style picture's size sets the slot size). 64 items at 16-32 px = 10 generations. Dry run by default; `--go` only after the owner says "เจน"."""
import json, base64, sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch8')
K = 'fierce chibi army COMMANDER, heroic leader pose, ornate gear, bold silhouette, battle ready'
CM = {
 'human': ['legendary ancient chinese warlord riding a red warhorse, two very long pheasant tail feathers on his helmet, crescent-bladed halberd raised, red and gold armour', 'knight commander on foot holding a tall war banner and a longsword, blue cape',
   'ancient chinese warlord charging on a dark red horse, halberd pointed forward, black and gold armour, two long pheasant feathers on his helmet, flowing red cape', 'paladin commander with a glowing holy hammer and a tower shield, white and gold armour',
   'battle queen in silver armour with a spear and a flowing red cape', 'old wizard general in blue robes with a long white beard and a lightning orb staff',
   'crossbow captain in a feathered hat and leather coat with a heavy crossbow', 'dark knight lord in spiky black armour with a flaming two-handed sword',
   'shogun in red lacquered armour with a big horned helmet and a katana', 'war priest commander blowing a golden war horn, holding a mace',
   'ancient chinese general on a rearing red horse, crescent halberd behind him, golden lion-face chest armour, two long curved pheasant feathers on his helmet', 'one-eyed general with two swords, an eyepatch and a fur cape'],
 'alien': ['alien overlord with a huge brain head on a floating hover throne', 'alien insect queen with a tall crest and four arms', 'alien warlord in spiked power armour with a plasma glaive',
   'bloated alien hive mother with egg sacs and tentacles', 'tall grey alien commander with a staff topped by a floating crystal and a dark cape', 'small alien piloting a two-legged walker mech',
   'alien beast lord riding a six-legged crawler, holding a spear', 'alien psychic master with a glowing third eye and floating rocks around', 'alien hunter chief with bone mask trophies and a net launcher',
   'alien tentacle titan with many tentacles and one huge eye', 'alien general with a laser cannon arm and an energy shield'],
 'animal': ['lion king warlord standing upright with a golden mane, bone armour and a war club', 'giant gorilla chieftain with tribal war paint and a stone hammer',
   'woolly mammoth carrying a war tower on its back', 'huge long-necked dinosaur with a war drum platform on its back', 'golden griffin king with spread wings and a crown',
   'great white wolf alpha with glowing blue eyes', 'spinosaurus commander roaring with a glowing sail on its back', 'bear shaman chieftain standing upright with a bone staff and skull necklace',
   'elder giant tortoise with a stone shrine on its shell', 'sabre-tooth tiger chief wearing tribal armour', 'king cobra commander rearing up with a golden hood crown'],
 'machine': ['giant war robot commander with a cannon arm and a red visor', 'robot general on tank treads with a shoulder missile pod', 'sleek android commander with a glowing energy sword',
   'spider mech command unit with a radar dish', 'steam powered colossus with chimney stacks and a huge wrench', 'robot king with a gear crown, a cape and a scepter',
   'drone carrier robot with small drones orbiting it', 'heavy mech with twin gatling gun arms', 'floating AI core, a glowing sphere inside a metal frame with cables',
   'cyborg samurai commander with a laser katana'],
 'demon': ['demon lord with huge horns, bat wings and a flaming whip', 'hell knight general in black armour with lava cracks and a burning sword', 'demon queen with dark wings and a cursed staff',
   'giant fire golem made of lava rocks', 'lich commander in tattered robes with a skull staff and green soul fire', 'demon centaur warlord with a flaming spear',
   'three-eyed demon emperor on a bone throne', 'demon hound master holding chains', 'fallen angel with black wings, a broken halo and a scythe', 'four-armed demon berserker with two axes'],
 'god': ['sun god king with a radiant golden halo and a spear of light', 'thunder god with a lightning hammer, white beard and flowing cape', 'moon goddess with a silver bow and a crescent crown',
   'war goddess in gold armour with a winged helmet, shield and sword', 'six-winged seraph commander glowing white', 'ancient titan of stone and gold with glowing runes',
   'sea god with a trident riding a wave', 'white and gold celestial dragon floating', 'sky god on a golden chariot pulled by two white horses', 'wisdom goddess with an owl and a glowing book'],
}
TONE = {'human': 'dark steel armour', 'alien': 'dark purple with toxic green glow', 'animal': 'tribal war paint', 'machine': 'steel grey with orange warning stripes',
        'demon': 'crimson and black with orange glow', 'god': 'white and gold with light blue glow'}
items, keys, names = [], [], {}
for tribe, lst in CM.items():
    for i, d in enumerate(lst):
        k = f'c8_{len(keys):02d}'; items.append(f'{K}, {tribe} tribe, {d}, {TONE[tribe]}, side view facing right, full body'); keys.append(k); names[k] = f'{tribe}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['batch3/raw/k3_02', 'batch3/raw/k3_18', 'batch4/raw/a4_12', 'batch4/raw/a4_34', 'batch6/raw/p6_00', 'batch7/raw/m7_01', 'batch7/raw/m7_12', 'batch3/raw/k3_10']
style = []
for f in SP:
    im = Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA'); assert im.size == (32, 32), im.size
    b = io.BytesIO(); im.save(b, 'PNG'); style.append({'type': 'base64', 'base64': base64.b64encode(b.getvalue()).decode(), 'format': 'png'})
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline, bright colours', 'name': 'clash commanders batch 8',
        'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'commanders, all different; style', len(style), 'x 32 px; dry run')
