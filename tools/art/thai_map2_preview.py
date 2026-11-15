# Thai map 2 (floating market) preview: Meta's 3 pictures as 3 separate blocks, canals between them, a straight boardwalk bridge
# below and Meta's rope bridge with huts on the roofs, carved lantern posts over the joins (owner: "แยกออก ละทำสะพานเชื่อม").
#   python3 tools/art/thai_map2_preview.py  -> art/incoming/thai/map2/meta_bridges.jpg
from PIL import Image, ImageDraw
import numpy as np
D='art/incoming/thai/map2/'; S='/tmp/claude-0/-home-user-last-signal-pvp/4afdd359-3ed6-58f4-972b-1cb5e61c151e/scratchpad/'
L,M,R=[Image.open(D+f'meta_{n}.jpg').convert('RGB') for n in ['left','mid','right']]
H=860
def place(im,s,dy):
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS); c=Image.new('RGB',(im.width,H)); c.paste(im,(0,dy)); return c
L2,M2,R2=place(L,1,0),place(M,1,5),place(R,1.021,1)
# canal gap: sky / hills / mist from the open end of the middle picture down to y 550 (above its boat and old pier);
# below: clean misty canal water from the right picture (between the big tree and the broken pier), tiled with mirrored rows, darker going down
top=np.array(M2.crop((1805,0,2000,H)).resize((300,H))).astype(float)
w=np.array(R.crop((1540,525,1840,570))).astype(float); rows=[]
while sum(r.shape[0] for r in rows)<H: rows.append(w if len(rows)%2==0 else w[::-1])
wat=np.concatenate(rows,0)[:H]
y0=550; t=np.clip((np.arange(H)-y0)/24,0,1)[:,None,None]
f=top*(1-t)+wat*t
dark=np.clip((np.arange(H)-600)/245,0,1)[:,None,None]*.35; f=f*(1-dark)
fill=Image.fromarray(f.clip(0,255).astype(np.uint8))
deck=M.crop((540,701,760,743)).convert('RGBA')
OL=(34,20,12,255); WOOD=(104,66,38,255); WOOD2=(132,86,48,255); ROPE=(206,176,116,255)
def bridge(W=420, top=70):
    b=Image.new('RGBA',(W,top+deck.height+110),(0,0,0,0)); d=ImageDraw.Draw(b)
    for px in range(14,W-10,96): d.rectangle((px,top+deck.height-6,px+13,b.height-4),fill=WOOD,outline=OL,width=2)
    x=0; i=0
    while x<W: b.alpha_composite(deck if i%2==0 else deck.transpose(Image.FLIP_LEFT_RIGHT),(x,top)); x+=deck.width; i+=1
    d.line((0,top,W,top),fill=OL,width=2)
    for px in range(40,W-30,64): d.rectangle((px,top-30,px+8,top+2),fill=WOOD2,outline=OL,width=2)
    for k in (26,13):
        pts=[(cx,top-k+3*np.sin((cx-40)/64*np.pi)**2) for cx in range(40,W-24,4)]; d.line(pts,fill=OL,width=4); d.line(pts,fill=ROPE,width=2)
    return b
parts=[L2.crop((0,0,1990,H)),fill,M2.crop((12,0,1796,H)),fill.transpose(Image.FLIP_LEFT_RIGHT),R2]
O=Image.new('RGBA',(sum(p.width for p in parts),H)); x=0; gaps=[]
for i,p in enumerate(parts):
    O.paste(p,(x,0))
    if i in (1,3): gaps.append((x,x+p.width))
    x+=p.width
P={k:Image.open(D+f'cut_{k}.png') for k in ['rope','post']}
def put(im,w,x,bottom,flip=False):
    h=round(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    O.alpha_composite(im,(round(x),round(bottom-h)))
br=bridge()
for a_,b_ in gaps:
    c=(a_+b_)/2; pw=round(P['post'].width*520/P['post'].height)
    O.alpha_composite(br,(round(c-210),708-70))
    put(P['post'],pw,a_-pw*.35,780); put(P['post'],pw,b_-pw*.65,780,True)
    put(P['rope'],720,c-360,262)
O=O.convert('RGB').crop((0,0,O.width,845)); O.save(D+'meta_bridges.jpg',quality=88)
O.crop((1650,0,2650,845)).resize((750,634)).save(S+'fin.jpg')
O.crop((3750,0,4750,845)).resize((750,634)).save(S+'fin2.jpg')
