from pathlib import Path
from PIL import Image
import json
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'qa-output')
meta=json.loads((root/'Zeus_attack_frames.json').read_text())
frames=meta['frames']
with Image.open(root/'Zeus_attack.gif') as gif, Image.open(root/'Zeus_attack_sheet.png') as sheet:
    assert gif.n_frames == len(frames) == 35
    assert gif.size == (512,512)
    assert sheet.size == (meta['columns']*512,meta['rows']*512)
    for i,f in enumerate(frames):
        gif.seek(i)
        assert gif.convert('RGBA').getbbox()
        alpha=sheet.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])).convert('RGBA').getchannel('A')
        assert alpha.getbbox() and alpha.getpixel((0,0))==0
        assert f['index']==i
with Image.open(root/'Zeus_attack.png') as png:
    assert png.size == (512,512) and png.mode=='RGBA' and png.getpixel((0,0))[3]==0
print('PNG and sprite atlas validated. All 35 GIF frames decoded.')
