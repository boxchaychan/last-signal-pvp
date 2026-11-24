"""clash.html batch 15 = SPECIAL UNITS again at 40 px, prettier (owner 2026-11-24 "ยูนิตพิเศษมัน 40 ไม่ใช่หรือ" -> "เจน 40 เอาสวยกว่าเดิม": batch 14 was made at 32 px
by mistake; the demon specials are ~40 px). Same 64 ideas as batch 14 (human 13, alien 13, animal 13, machine 13, god 12), each line given more look detail
(glow, cape, weapon). Prettier = (1) slot 40 px, (2) style pictures = the owner's OWN liked 16-bit cuts (the 3 demon specials in the game, the picked
37 px dinos, the 16-bit rhino / elk riders), padded onto 40 x 40 (the style picture's size sets the slot size), (3) "16-bit console pixel art" + max_colors 16.
64 items at 33-42 px = 15 generations. Dry run by default (writes the exact style pictures to <out>/style_sent.png); `--go` sends."""
import json, base64, sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch15')
K = ('unique SPECIAL hero unit, 16-bit console pixel art, chibi proportions, highly detailed ornate gear, rich shading with bright highlights, '
     'glowing accents, bold dark outline, heroic and fierce, bigger and grander than a common soldier')
TONE = {'human': 'human tribe, dark steel armour, rich cloth and gold trim', 'alien': 'alien tribe, dark purple with toxic green glow',
        'animal': 'animal tribe, mighty beast with tribal war paint and bone ornaments', 'machine': 'machine tribe, light steel metal with glowing neon blue lights',
        'god': 'god tribe, white and gold with light blue holy glow'}
CL = {
 'human': ['wandering ronin with a straw hat, a tattered red scarf and two drawn swords', 'plague doctor with a beak mask, a long black coat and a green glowing lantern',
   'alchemist with a belt of potions throwing a glowing purple flask', 'bard in a feathered hat playing a golden war lute with music sparks', 'hooded executioner with a giant bloodstained axe',
   'siege engineer with goggles pushing a small bronze cannon', 'staff monk in orange robes spinning a long staff', 'gladiator with a crested helmet, a net and a trident',
   'musketeer with a plumed hat and a long smoking musket', 'witch hunter with a wide hat, a long coat and a silver crossbow', 'knight in plate armour riding a brown war bear',
   'giant empty suit of living armour with blue fire in the visor', 'battle priestess in white and gold with a glowing holy hammer'],
 'alien': ['floating brain alien with a glowing brain and psychic rings', 'crystal shard being made of glowing green crystals', 'giant acid slime with bones and a skull inside',
   'shapeshifter mimic half-transformed with claws and many teeth', 'insect hive queen with a tall crest and four arms', 'plasma ghost alien with a glowing core',
   'cloaked alien hunter with a trophy skull spear', 'swarm cloud of tiny parasites with many red eyes', 'giant alien worm bursting from the ground with a round toothy mouth',
   'levitating probe orb with metal tendrils and a scanning eye', 'many-eyed tentacle seer floating in a robe', 'alien knight in spiked armour with a living green sword',
   'walking spore pod plant with glowing spores'],
 'animal': ['ape king with a golden crown, a red cape and a stone club', 'ancient giant tortoise elder with a moss and shrine shell', 'white tiger spirit with blue stripes of light',
   'thunder bison with lightning horns and crackling sparks', 'scorpion king with a golden crown and a huge stinger', 'owl sage in robes with a glowing open book',
   'chimera beast with a lion head, a goat head and a snake tail', 'lion knight in armour with a mane cape and a broadsword', 'giant cobra charmer, a snake man with a flute and a cobra hood',
   'sabre-tooth shaman with a skull staff and spirit fire', 'spirit elk with huge glowing cyan antlers', 'honey badger berserker with two axes and war paint',
   'praying mantis swordsman with blade arms'],
 'machine': ['clockwork knight with a big wind-up key on its back and a lance', 'steam golem with smoking chimneys and furnace glow', 'commander robot with a swarm of small laser drones',
   'walking cannon mech on two thick legs', 'robot samurai with a glowing blue laser katana', 'tesla coil tower on spider legs crackling with electricity',
   'round walking bomb robot with a lit fuse', 'small mech dragon with metal wings and a blue fire mouth', 'twin android sisters back to back with blades',
   'scrap golem made of junk, pipes and gears', 'drill tank robot with a huge spinning drill arm', 'satellite robot with solar panel wings orbiting small orbs',
   'hologram AI warrior made of blue light lines'],
 'god': ['titan of the sun with a burning crown and a spear of light', 'thunder god with a white beard, a cape and a lightning hammer', 'moon goddess with a silver crescent bow and a moon crown',
   'angel of judgment with white wings holding golden scales and a sword', 'golden sphinx guardian with a pharaoh crown', 'holy stone golem with glowing blue runes',
   'time keeper in robes with a giant golden hourglass', 'star child floating in starlight with tiny stars around', 'archangel with six wings and a flaming sword',
   'sea god riding a wave with a golden trident', 'phoenix god with golden flame wings', 'twin-faced god of light and dark, half white half black'],
}
items, keys, names = [], [], {}
for cls, lst in CL.items():
    for d in lst:
        k = f'c15_{len(keys):02d}'; items.append(f'{K}, {TONE[cls]}, {d}, side view facing right, full body'); keys.append(k); names[k] = f'{cls}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['demon_special/fallen_40_16bit', 'demon_special/lich_40_16bit', 'demon_special/queen_40_16bit', 'gptdino/pick37_16/dino_01',
      'gptdino/pick37_16/dino_03', 'gptdino/pick37_16/dino_06', 'gptrider/rhino_50_16bit', 'gptrider/elk_50_16bit']
def pad40(f):
    a = np.asarray(Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA')).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    for i in range(1, n + 1):   # drop stray specks (style copy only)
        if (lab == i).sum() < 4: a[lab == i] = 0
    im = Image.fromarray(a); im = im.crop(im.getbbox()); assert max(im.size) <= 40, (f, im.size)
    c = Image.new('RGBA', (40, 40), (0, 0, 0, 0)); c.paste(im, ((40 - im.width) // 2, 40 - im.height), im); return c
pads = [pad40(f) for f in SP]
def b64(im): b = io.BytesIO(); im.save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()
style = [{'type': 'base64', 'base64': b64(c), 'format': 'png'} for c in pads]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body', 'name': 'clash special units 40px batch 15', 'view': 'sidescroller',
        'style_images': style, 'item_descriptions': items, 'max_colors': 16}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
prev = Image.new('RGBA', (8 * 44 * 4, 44 * 4), (92, 98, 92, 255))
for i, c in enumerate(pads): prev.alpha_composite(c.resize((160, 160), Image.NEAREST), (i * 176 + 8, 8))
prev.save(os.path.join(OUT, 'style_sent.png'))
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'special units at 40 px, max 16 colours; style', len(style), 'x', pads[0].size, '; dry run')
