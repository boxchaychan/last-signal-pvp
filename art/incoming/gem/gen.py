# PixelLab pictures for gem.html (owner 2026-11-14 "อะไรขาดเจนได้เลยให้งบ100"): create_image_pixen, standard, 1 generation each.
#   PL_KEY=proxy-injected python3 art/incoming/gem/gen.py <id> [<id> ...]      ids = keys of BG / IC / EX below
# Raw results: art/incoming/gem/raw/<id>.png (+ jobs.json). Every job is in the log at the top of docs/action-game.md.
import sys, json, subprocess, time, urllib.request, os
BGT = "dark fantasy pixel art battle arena background, side view: %s; a flat %s across the bottom third for fighters to stand on, empty in the middle, no characters, no people, no text"
BG = dict(
 siam=("an ancient Siamese temple ruin deep in a tropical jungle at dusk, tall bell-shaped stone stupas and corn-cob prang towers overgrown with banyan roots and vines, a weathered stone guardian statue, small oil lamps and incense smoke, palm and banana leaves, an orange and teal sky through the canopy, fireflies", "terrace of old reddish laterite stone slabs"),
 china=("inside a vast underground imperial tomb hall, rows of terracotta warrior statues standing in alcoves along the back wall, tall red lacquered pillars with golden dragon carvings, bronze braziers burning with warm fire, hanging red paper lanterns, jade-green mist", "floor of dark polished stone tiles"),
 japan=("a haunted mountain shrine at night, a row of tall red torii gates on stone steps, glowing stone lanterns, twisted pine trees, falling cherry blossom petals, a huge pale moon behind a pagoda roof, drifting purple mist and small blue spirit flames", "floor of mossy stone paving"),
 egypt=("a desert temple courtyard at sunset, giant sandstone pharaoh statues and hieroglyph-carved columns, a pyramid and palm trees in the distance, burning bronze braziers, drifting sand, an orange and violet sky", "floor of worn sandstone slabs"),
 norse=("a frozen northern fjord at night under a green aurora, snow-covered pine trees, carved rune stones, a wooden viking longhouse with dragon-head beams, jagged ice cliffs, burning torches, falling snow", "ground of packed snow and blue ice"),
 camp=("a heroes' camp at night on a mountain ledge, a crackling campfire on the left, canvas tents with tribal banners, a weapon rack, wooden crates and barrels, lanterns on poles, a starry sky with a huge moon over distant misty mountains, cosy warm firelight", "ground of trodden earth and grass"))
ICT = "%s. Dark fantasy pixel art game UI icon, a single object centered, filling most of the frame, viewed straight on, thick dark outline, rich colours with strong highlights, no text, no frame, no hand"
IC = dict(
 lock="a heavy iron padlock with a gold keyhole plate", skull="a horned demon skull with glowing red eyes", swords="two crossed steel swords with gold hilts",
 gear="a bronze cogwheel gear with eight teeth", speaker="a brass hunting horn, a curved signal horn with a wide bell", note="a golden musical note, a beamed eighth note",
 map="a rolled parchment treasure map with a red ribbon and a compass rose", chest="a wooden treasure chest with gold bands, lid open, overflowing with gold coins and gems", book="an open spell book with a blue ribbon bookmark and glowing pages")
EX = dict(
 emblem=dict(description="a heraldic game logo emblem without any letters: a huge brilliant-cut white diamond in the centre with a war hammer and a flaming staff crossed behind it, golden laurel wings on both sides and a small crown on top, dark fantasy pixel art, thick dark outline, rich gold and purple with strong highlights, no text, no letters, no banner", width=176, height=128, no_background=True, detail='highly detailed', outline='single color black outline'))
out = 'art/incoming/gem/raw/'
def call(tool, args): return subprocess.run(['python3', 'tools/pl_rpc.py', tool, json.dumps(args)], capture_output=True, text=True).stdout
jobs = {}
for k in sys.argv[1:]:
    if k in BG: a = dict(description=BGT % BG[k], width=480, height=272, view='side', detail='highly detailed')
    elif k in IC: a = dict(description=ICT % IC[k], width=32, height=32, no_background=True, detail='medium detail', outline='single color black outline')
    else: a = EX[k]
    r = call('create_image_pixen', a); j = [l.split()[1] for l in r.splitlines() if l.startswith('job_id')]
    if j: jobs[k] = j[0]; print('queued', k, j[0], [l for l in r.splitlines() if l.startswith('cost')])
    else: print('FAIL', k, r[:300])
jf = out + 'jobs.json'; json.dump({**(json.load(open(jf)) if os.path.exists(jf) else {}), **jobs}, open(jf, 'w'), indent=0)
left = dict(jobs); t0 = time.time()
while left and time.time() - t0 < 300:
    for k, j in list(left.items()):
        try:
            d = urllib.request.urlopen(urllib.request.Request('https://api.pixellab.ai/mcp/images/%s/download' % j, headers={'Authorization': 'Bearer x'}), timeout=30).read()
            open(out + k + '.png', 'wb').write(d); del left[k]
        except Exception: pass
    time.sleep(6)
print('done', sorted(set(jobs) - set(left)), 'missing', sorted(left))
