# PixelLab icons for the bag3d.html crafted + new items (owner 2026-11-26 "ไม่พอก็เจนเพิ่ม"): the SAME recipe as the 40 originals
# (art/incoming/bag/gen.py: create_image_pixen 64x64, no background, highly detailed, black outline, 1 credit each). Raw files: art/incoming/bag3d/pl/<id>.png
#   PL_KEY=proxy-injected python3 art/incoming/bag3d/gen.py <id> [<id> ...]      (ids = keys of P)
import sys, json, subprocess, time, urllib.request, os
ST = "dark fantasy pixel art game item icon, a single object centered, filling most of the frame, viewed straight on, thick dark outline, moody rich colours with strong highlights, gothic style, no text, no frame, no hand"
P = dict(
 flamesword="a gothic longsword whose dark steel blade is wrapped in roaring orange fire, a fire gem in the hilt",
 venomknife="a short curved black dagger dripping glowing green venom from the blade",
 frostbow="a crossbow carved from clear blue ice with frost crystals and a glowing ice bolt",
 bloodaxe="a blood-red battle axe with a demon fang set in the head and a dark red glow",
 thunderhammer="a heavy iron war hammer crackling with bright purple lightning",
 archstaff="a black archmage staff topped with a big burning fire crystal and a floating glowing rune",
 vampclaw="a black iron clawed gauntlet with a glowing red vampire heart gem in the back",
 comet="a blazing comet of fire and rock with a long fiery tail",
 fortress="a golden fortress tower shield with a knight helmet crest on top and gold rivets",
 spikeshield="a round dark green shield covered in sharp cactus thorns",
 feast="a roasted meat leg and a goblet of red wine on a small silver plate",
 luckycoin="a golden lucky coin with a glowing green four-leaf clover engraved on it",
 twinblades="two crossed curved twin swords with a pale moonlight-blue glow",
 rapier="a thin elegant rapier with a silver swept basket hilt, diagonal",
 greatsword="a huge black and purple two-handed greatsword with glowing purple runes, diagonal",
 katana="a katana with a pale blade and a swirl of white wind around it, diagonal",
 javelin="a throwing javelin with a bronze leaf tip and red feathers, diagonal",
 chakram="a round spinning chakram ring blade wrapped in orange fire",
 holytome="a holy book with a gold cover and a glowing white sun symbol",
 voidorb="a dark crystal orb with swirling purple void and stars inside on a black claw stand",
 buckler="a small round bronze buckler shield with a raised boss in the middle",
 towershield="a tall upright knight tower shield, flat front view, rectangular with a rounded top, polished steel with a gold rim and a blue lion emblem, held by no one",
 boots="a pair of light leather boots with small teal wind wings on the heels",
 amulet="a golden priest amulet on a chain with a glowing white gem",
 bread="a round loaf of crusty travel bread",
 potion="a big round red health potion flask with a cork, glowing",
 honey="a clay jar of golden wild honey with a wooden dipper, dripping",
 elixir="a tall golden elixir flask with sparkles of light inside",
 furyrune="a red rune stone carved with an angry glowing fury symbol",
 venomgland="a green venom gland sac dripping glowing poison",
 thunderstone="a purple stone crackling with small yellow lightning",
 holyseal="a golden holy seal medallion with a white wax stamp and a glowing cross",
 ragemask="a red demon berserker mask with horns and glowing angry eyes",
 wardrum="a small red war drum with two wooden drumsticks",
 lantern="an iron ghost lantern with a blue spirit flame inside",
 goldbag="a leather merchant bag overflowing with gold coins",
 stormblades="two crossed twin swords wrapped in a swirling blue storm wind with lightning",
 luckrapier="a rapier with a green four-leaf clover charm on the hilt and a lucky golden glow, diagonal",
 executioner="a giant executioner sword dripping red with a demon fang on the crossguard, diagonal",
 frostlance="a long ice lance of clear blue crystal with frost mist, diagonal",
 divinetome="a radiant divine holy book with golden angel wings and holy light",
 parrybuckler="a small round buckler with sharp parry spikes and a gauntlet behind it",
 honeybread="a loaf of bread glazed with dripping golden honey",
 soullantern="a cursed iron lantern with a purple skull-shaped flame inside",
 # BUILD TREE (owner 2026-11-27 "เจนรูปไอเทมได้เลย"): 7 parts, 6 mid items, 8 ultimate items
 p_blade="a bare forged steel sword blade with no hilt, polished and sharp, diagonal",
 p_hide="a rolled thick brown beast hide with fur edges, tied with a leather cord",
 p_plate="a single curved iron armor plate with round rivets",
 p_feather="a single brown and white striped hawk feather",
 p_crystal="a raw cluster of glowing purple magic crystal shards",
 p_fang="a large curved ivory beast fang hanging on a leather cord",
 p_herb="a small bundle of green wild herbs with tiny white flowers tied with twine",
 m_edge="a short broad warrior blade of bright steel crossed with a white beast fang, its edge glowing orange",
 m_mail="a chainmail shirt with leather trim and iron shoulder plates",
 m_boots="a pair of fur-lined leather boots with brown hawk feathers on the ankles and a green swirl of wind",
 m_orb="a round arcane crystal ball with glowing purple runes floating inside, on a small gold ring stand",
 m_charm="a leaf-shaped green jade amulet wrapped in leather cord with herbs, soft green glow",
 m_claws="three curved steel claw blades on a leather hand strap decorated with hawk feathers",
 f_kingslayer="a legendary greatsword with a golden crown-shaped crossguard and a glowing red blade edge, diagonal",
 f_bastion="a massive iron shield shaped like a castle gate with battlements on top and a glowing green gem in the middle",
 f_stormstep="a pair of legendary steel boots wrapped in a swirling blue tornado with small lightning bolts",
 f_archmage="an archmage crown of dark gold with tall purple crystal spikes and a glowing arcane gem",
 f_bloodpact="a dark sealed scroll with a red wax skull seal dripping blood, glowing red",
 f_titan="a huge titan chest armor of dark steel with big spiked shoulders and a glowing orange core",
 f_lichstaff="a demon king staff of black bone topped with a horned skull holding a green flame, purple gems",
 f_godbow="a legendary golden longbow with white angel wing limbs and a glowing arrow of light")
out = 'art/incoming/bag3d/pl/'; os.makedirs(out, exist_ok=True)
def call(tool, args): return subprocess.run(['python3', 'tools/pl_rpc.py', tool, json.dumps(args)], capture_output=True, text=True).stdout
jobs, todo, left, t0 = {}, [k for k in sys.argv[1:] if not os.path.exists(out + k + '.png')], {}, time.time()
def submit(k):
    a = dict(description=P[k] + '. ' + ST, width=64, height=64, no_background=True, detail='highly detailed', outline='single color black outline')
    r = call('create_image_pixen', a); j = [l.split()[1] for l in r.splitlines() if l.startswith('job_id')]
    if j: jobs[k] = left[k] = j[0]; return True
    if 'wait for a job' not in r and 'concurrent' not in r.lower(): print('FAIL', k, r[:300]); todo.remove(k)
    return False
while (todo or left) and time.time() - t0 < 560:   # PixelLab runs about 8 jobs at a time: keep 7 going, send the next when one is done
    for k in [k for k in todo if k not in jobs][:max(0, 7 - len(left))]:
        if not submit(k): break
    for k, j in list(left.items()):
        try:
            d = urllib.request.urlopen(urllib.request.Request('https://api.pixellab.ai/mcp/images/%s/download' % j, headers={'Authorization': 'Bearer x'}), timeout=30).read()
            if d[:4] == b'\x89PNG': open(out + k + '.png', 'wb').write(d); del left[k]; todo.remove(k)
        except Exception: pass
    json.dump({**(json.load(open(out + 'jobs.json')) if os.path.exists(out + 'jobs.json') else {}), **jobs}, open(out + 'jobs.json', 'w'), indent=1)
    time.sleep(5)
print('done', sorted(k for k in jobs if k not in left), 'missing', sorted(set(todo) | set(left)))
