# PixelLab icons for bag.html (owner 2026-11-13 "เจนมา"): create_image_pixen 64x64, no background, 1 credit each.
#   python3 art/incoming/bag/gen.py <id> [<id> ...]   (ids = keys of P below; "arena" = the battle backdrop 480x272)
import sys, json, subprocess, time, urllib.request, os
ST = "dark fantasy pixel art game item icon, a single object centered, filling most of the frame, viewed straight on, thick dark outline, moody rich colours with strong highlights, gothic style, no text, no frame, no hand"
P = dict(dagger="a short curved black-steel dagger with a purple gem in the hilt", sword="a gothic longsword with a dark steel blade, silver edge and a crescent-moon crossguard", bow="a dark wooden hunting bow with a nocked arrow and bone tips",
 axe="a heavy rusted battle axe with a jagged blade and a wrapped leather handle", hammer="a huge iron war hammer with spikes and glowing red runes", wand="a twisted black staff topped with a burning red flame crystal",
 poison="a round glass potion bottle full of bubbling green poison with a skull label and a cork", bomb="a round black powder bomb with a burning fuse and iron bands", shield="a battered knight's kite shield, dark steel with a silver cross and dents",
 helm="a dark iron knight's helmet with a visor and a red plume", cactus="a black iron chest armour covered in sharp thorns and spikes", feather="a single glowing pale blue raven feather",
 apple="a blood-red apple with a dark leaf, glossy, one bite taken", meat="a big roasted meat leg on the bone, steaming", juice="a small blue glowing stamina potion in a square bottle with a cork",
 stone="a grey whetstone block with sparks and scratch marks", glove="a pair of dark leather gauntlets with silver studs", clover="a glowing emerald four-leaf clover charm on a thin chain",
 ember="a faceted fire-red gemstone with flames inside", frost="a faceted ice-blue gemstone covered in frost crystals", heart="an anatomical dark red heart pierced by a small silver fang, dripping",
 star="a golden falling star charm with a glowing trail and runes", pig="a small bronze piggy bank shaped like a boar with a coin slot and gold coins", crown="a tarnished golden king's crown with red jewels and black spikes")
out = 'art/incoming/bag/icons/'
def call(tool, args): return subprocess.run(['python3', 'tools/pl_rpc.py', tool, json.dumps(args)], capture_output=True, text=True).stdout
jobs = {}
for k in sys.argv[1:]:
    if k == 'arena': a = dict(description="dark fantasy pixel art battle arena background, side view: a ruined gothic cathedral courtyard at night, a huge pale full moon behind broken arches and pillars, dead twisted trees, gravestones, burning torches on the walls, low purple fog, a flat cracked stone floor across the bottom third for fighters to stand on, empty in the middle, no characters, no text", width=480, height=272, view='side', detail='highly detailed')
    else: a = dict(description=P[k] + '. ' + ST, width=64, height=64, no_background=True, detail='highly detailed', outline='single color black outline')
    r = call('create_image_pixen', a); j = [l.split()[1] for l in r.splitlines() if l.startswith('job_id')]
    if j: jobs[k] = j[0]
    else: print('FAIL', k, r[:200])
json.dump({**(json.load(open(out + 'jobs.json')) if os.path.exists(out + 'jobs.json') else {}), **jobs}, open(out + 'jobs.json', 'w'))
left = dict(jobs); t0 = time.time()
while left and time.time() - t0 < 240:
    for k, j in list(left.items()):
        try:
            d = urllib.request.urlopen(urllib.request.Request('https://api.pixellab.ai/mcp/images/%s/download' % j, headers={'Authorization': 'Bearer x'}), timeout=30).read()
            open(out + k + '.png', 'wb').write(d); del left[k]
        except Exception: pass
    time.sleep(6)
print('done', sorted(set(jobs) - set(left)), 'missing', sorted(left))
