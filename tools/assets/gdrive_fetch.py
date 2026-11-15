# Fetch files from a PUBLIC Google Drive folder (Quaternius packs link their Drive folders on quaternius.com/packs/<pack>.html).
#   python3 -I tools/assets/gdrive_fetch.py <folder id> [regex of paths to download] [out folder]   (no regex = list only)
# Needs the hosts drive.google.com + drive.usercontent.google.com allowed (added 2026-11-15). Google answers "Quota exceeded"
# (an HTML page instead of the file) when a shared file was downloaded too much: wait up to 24 h and retry.
# list a public Google Drive folder (embeddedfolderview) and optionally download files whose names match
import re, html, sys, subprocess, os
def ls(fid):
    out = subprocess.run(['curl', '-sS', '-L', '-m', '40', f'https://drive.google.com/embeddedfolderview?id={fid}'], capture_output=True, text=True).stdout
    items = []
    for m in re.finditer(r'<a href="([^"]+)"[^>]*>.*?<div class="flip-entry-title">([^<]+)</div>', out, re.S):
        url, name = m.group(1), html.unescape(m.group(2))
        f = re.search(r'/folders/([\w-]+)', url); d = re.search(r'/file/d/([\w-]+)', url)
        items.append(('dir', name, f.group(1)) if f else ('file', name, d.group(1)))
    return items
def walk(fid, path=''):
    for kind, name, i in ls(fid):
        if kind == 'dir': yield from walk(i, path + name + '/')
        else: yield path + name, i
def get(fid, dst):
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    r = subprocess.run(['curl', '-sS', '-L', '-m', '300', '-o', dst, '-w', '%{http_code}', f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'], capture_output=True, text=True)
    return r.stdout
if __name__ == '__main__':
    root, pat, out = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, sys.argv[3] if len(sys.argv) > 3 else None
    for p, i in walk(root):
        hit = pat and re.search(pat, p)
        print(('GET ' if hit and out else '    ') + p, i)
        if hit and out: print('   ', get(i, os.path.join(out, p)))
