from pathlib import Path
import base64, json, sys
P=Path(__file__).resolve().parent
def build():
    files=['source','bolt','sword','hand-open','hand-grip','face-blink','face-focused','face-shout']
    assets={n:'data:image/png;base64,'+base64.b64encode((P/'assets'/f'{n}.png').read_bytes()).decode() for n in files}
    markup=(P/'src'/'index.html').read_text()
    css=(P/'src'/'style.css').read_text()
    script='const ART='+json.dumps(assets)+';\n'+'\n'.join((P/'src'/f'{n}.js').read_text() for n in ['engine','render','scene','gif','project','app'])
    return markup.replace('/*CSS*/',css).replace('/*SCRIPT*/',script)
if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else P/'chibi_live_studio.html'
    path.write_text(build())
