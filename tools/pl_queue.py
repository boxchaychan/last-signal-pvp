# Run a list of PixelLab animate_character jobs one after another (trial accounts have ONE job slot), downloading the
# character ZIP after each job so finished moves can be used while the rest run. Key from PL_KEY (see pl_rpc.py).
#   python tools/pl_queue.py <jobs.json> <character id> <zip out dir> [log file]
# jobs.json: [{"anim": "run", "dir": "east", "frames": 8, "keep": false, "action": "...", "pose": "..."}, ...]
# Jobs of the same "anim" share one animation group. A job whose anim/dir folder already exists in the download is
# skipped (so the queue can be restarted without paying twice). Stops on any error.
import sys, json, time, os, zipfile, io, urllib.request, re
sys.path.insert(0, os.path.dirname(__file__))
from pl_rpc import call, KEY

jobs = json.load(open(sys.argv[1], encoding='utf-8'))
cid, out = sys.argv[2], sys.argv[3]
logf = open(sys.argv[4] if len(sys.argv) > 4 else os.path.join(out, 'queue.log'), 'a', encoding='utf-8')
SUBJ = 'a young woman rogue with a short curved dagger in her right hand'

def log(*a):
    s = time.strftime('%H:%M:%S ') + ' '.join(str(x) for x in a); print(s, flush=True); logf.write(s + '\n'); logf.flush()

def download():
    for k in range(20):
        req = urllib.request.Request(f'https://api.pixellab.ai/mcp/characters/{cid}/download', headers={'Authorization': 'Bearer ' + KEY})
        try:
            data = urllib.request.urlopen(req, timeout=300).read()
            zipfile.ZipFile(io.BytesIO(data)).extractall(out); return True
        except urllib.error.HTTPError as e:
            if e.code in (409, 423, 425, 202) or 'still being generated' in e.read().decode(errors='ignore'): time.sleep(15); continue
            raise
    return False

def have(anim, d):
    return os.path.isdir(os.path.join(out, 'Idle', 'animations', anim, d))

groups = {}
gfile = os.path.join(out, 'groups.json')
if os.path.exists(gfile): groups = json.load(open(gfile))
for j in jobs:
    a, d = j['anim'], j['dir']
    if have(a, d): log('skip (already downloaded)', a, d); continue
    args = {'character_id': cid, 'mode': 'pixminimax', 'directions': [d], 'frame_count': j['frames'], 'animation_name': a,
            'subject_description': j.get('subject', SUBJ), 'action_description': j['action'], 'keep_first_frame': j.get('keep', True)}
    if j.get('pose'): args['initial_pose'] = j['pose']
    if a in groups: args['animation_group_id'] = groups[a]
    r = call('animate_character', args)
    m = re.search(r'group: ([0-9a-f-]{36})', r); c = re.search(r'cost: ([^\n]+)', r)
    if not m: log('ERROR submitting', a, d, r[:400]); sys.exit(1)
    groups[a] = m.group(1); json.dump(groups, open(gfile, 'w'))
    log('queued', a, d, j['frames'], 'frames', '|', c.group(1) if c else '?', '| group', m.group(1))
    while True:
        w = call('wait_for_jobs', {'timeout_seconds': 300})
        if 'failed' in w: log('ERROR job failed', a, d, w[:400]); sys.exit(1)
        if 'nothing else is running' in w or 'no active jobs' in w: break
    time.sleep(3)
    log('done', a, d, '| download', 'ok' if download() else 'FAILED')
log('queue finished;', call('get_balance', {}).splitlines()[1])
