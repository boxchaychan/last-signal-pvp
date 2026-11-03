# Owner 2026-11-03: the gold tier does not need to be gold. Recolour the gold parts of the code-drawn gold-tier kids
# to each kid's own accent colour. usage: python3 gold_recolor.py art/bb
import sys, colorsys, numpy as np
from PIL import Image
ACC={'warrior':(355/360,.75),'mage':(250/360,.12),'support':(335/360,.45),'curse':(275/360,.65)}  # hue, saturation
for k,(h,sat) in ACC.items():
    p=f'{sys.argv[1]}/kid_{k}_gold.png';a=np.array(Image.open(p).convert('RGBA'));n=0
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            r,g,b,al=a[y,x]
            if not al:continue
            H,S,V=colorsys.rgb_to_hsv(r/255,g/255,b/255)
            if 42/360<=H<=58/360 and S>.62 and V>.45:
                nr,ng,nb=colorsys.hsv_to_rgb(h,min(1,sat*(.6+S*.5)),V*(.95 if sat>.3 else 1.0));a[y,x,:3]=[int(nr*255),int(ng*255),int(nb*255)];n+=1
    Image.fromarray(a,'RGBA').save(p);print(k,n)
