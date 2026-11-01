#!/usr/bin/env bash
# Syntax-check the game script inside index.html (run from the repo root).
set -e
python3 - <<'PY'
import re, tempfile, os
s = open('index.html', encoding='utf-8').read()
m = max(re.findall(r'<script>(.*?)</script>', s, re.S), key=len)
p = os.path.join(tempfile.gettempdir(), 'last-signal-game.js')
open(p, 'w', encoding='utf-8').write(m)
print(p)
PY
node --check "$(python3 -c "import tempfile,os;print(os.path.join(tempfile.gettempdir(),'last-signal-game.js'))")" && echo "syntax OK"
