# docs/action-prompts.html: the monster prompts of docs/codex/action/MOBS.md as ready-to-paste ChatGPT prompts (shared
# style lines + the monster's own lines, one copy button each). Owner 2026-11-09 "เตรียมคำสั่งต่อ gpt".
#   python tools/art/action_prompts_page.py
import re, html
src = open('docs/codex/action/MOBS.md', encoding='utf-8').read()
shared = re.search(r'## Shared prompt.*?```\n(.*?)```', src, re.S).group(1).strip()
mobs = re.findall(r'\*\*(\d+) (\w+)\*\* \(([^)]*)\)\n```\n(.*?)```', src, re.S)
status = dict(re.findall(r'\| \d+ \| (\w+) \| (\w+) \|', src))
cards = []
for n, key, th, lines in mobs:
    full = shared + '\n' + lines.strip()
    done = status.get(key) == 'done'
    cards.append(f'''<section class="card{' done' if done else ''}"><header><b>{n}. {html.escape(th)}</b><code>{key}</code>{'<i>เสร็จแล้ว</i>' if done else ''}
<button data-i="{len(cards)}">ก๊อปปี้</button></header><pre id="p{len(cards)}">{html.escape(full)}</pre>
<p class="save">บันทึกรูปเป็น <code>{key}.png</code></p></section>''')
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mob_anim
ma = open('docs/codex/action/MOB_ANIM.md', encoding='utf-8').read() if os.path.exists('docs/codex/action/MOB_ANIM.md') else ''
adone = set(re.findall(r'\| (\w+) \| (walk|attack|death) \| done \|', ma))
TH = {'walk': 'เดิน', 'attack': 'ตี', 'death': 'ตาย'}
anim = ['<h2>เฟรมขยับของมอน (ท่าละ 1 รูป)</h2><p>แนบรูปของมอนตัวนั้น (กดรูปเล็กเพื่อบันทึก) แล้วก๊อปพรอมต์ทีละท่า</p>']
for k in mob_anim.MOB:
    anim.append(f'<h3><a href="../art/incoming/mobs/{k}.png" download><img class="th" src="../art/incoming/mobs/px128/{k}/preview.png" alt=""></a>{html.escape(mob_anim.MOB[k][0])} <code>{k}</code></h3>')
    for a in ('walk', 'attack', 'death'):
        d = (k, a) in adone; i = len(cards) + len(anim)
        anim.append(f'''<section class="card{' done' if d else ''}"><header><b>{TH[a]}</b><code>{k}_{a}.png</code>{'<i>เสร็จแล้ว</i>' if d else ''}
<button data-i="{i}">ก๊อปปี้</button></header><pre id="p{i}">{html.escape(mob_anim.prompt(k, a))}</pre></section>''')
page = f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>พรอมต์มอนสเตอร์</title><style>
:root{{--bg:#16131c;--card:#221d2b;--ink:#efe7d6;--mut:#a99fb5;--acc:#ffd23c;--ok:#7cf24a}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif;padding:16px}}
main{{max-width:860px;margin:0 auto}} h1{{font-size:22px;margin:4px 0 8px}} p{{color:var(--mut)}}
.top{{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start;background:var(--card);padding:12px;border-radius:10px}}
.top img{{width:min(100%,420px);background:#fff;border-radius:6px}} .top ol{{margin:0;padding-left:20px}}
.card{{background:var(--card);border-radius:10px;padding:10px 12px;margin:12px 0}} .card.done{{opacity:.55}}
header{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}} header code{{color:var(--mut)}} header i{{color:var(--ok);font-style:normal}}
button{{margin-left:auto;background:var(--acc);color:#2a2000;border:0;border-radius:8px;padding:8px 16px;font-weight:700;font-size:15px}}
button.ok{{background:var(--ok)}} pre{{white-space:pre-wrap;word-break:break-word;font-size:12.5px;color:#d8d0e4;max-height:150px;overflow:auto;margin:8px 0 4px}}
.save{{margin:0;font-size:13px}} h2{{font-size:19px;margin:28px 0 4px}} h3{{display:flex;align-items:center;gap:10px;font-size:16px;margin:18px 0 4px}} .th{{height:56px;background:#7aa85a;border-radius:6px;image-rendering:pixelated}} code{{font-family:ui-monospace,monospace}}
</style></head><body><main>
<h1>พรอมต์มอนสเตอร์ (เกมแอ็กชัน)</h1>
<div class="top"><a href="codex/action/refs/00_STYLE_hero.png" download><img src="codex/action/refs/00_STYLE_hero.png" alt="รูปต้นแบบสไตล์ นักดาบ"></a>
<ol><li>กดรูปนักดาบเพื่อบันทึก แล้ว<b>แนบรูปนี้ทุกครั้ง</b>ใน ChatGPT</li><li>กดก๊อปปี้ของมอนตัวที่จะทำ แล้ววาง</li>
<li>ทีละตัว ทีละรูป แล้วส่งรูปมาให้ Claude</li><li>หรือให้ Codex ทำเอง: <code>อ่าน docs/codex/action/MOBS.md แล้วทำมอนสเตอร์ตามคิว ทีละรูป</code></li></ol></div>
{''.join(cards)}
{''.join(anim)}
</main><script>
document.querySelectorAll('button[data-i]').forEach(b => b.onclick = async () => {{
  const t = document.getElementById('p' + b.dataset.i).textContent;
  try {{ await navigator.clipboard.writeText(t); }} catch (e) {{ const a = document.createElement('textarea'); a.value = t; document.body.append(a); a.select(); document.execCommand('copy'); a.remove(); }}
  b.textContent = 'ก๊อปแล้ว'; b.classList.add('ok'); setTimeout(() => {{ b.textContent = 'ก๊อปปี้'; b.classList.remove('ok'); }}, 1500);
}});
</script></body></html>'''
open('docs/action-prompts.html', 'w', encoding='utf-8').write(page)
print(len(mobs), 'monsters')
