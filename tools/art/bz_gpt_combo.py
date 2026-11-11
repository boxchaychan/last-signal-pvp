# Owner's 3-attack GPT sheet (art/incoming/action/berserker/v4_cool/gpt_slash2/sheet.png, 3 rows x 12) -> pixel frames at game size, one
# scale per row (each row's first stance frame = 137 px incl. horns, owner "ห้ามให้ตัวไม่เท่ากัน"), joined into one combo GIF.
#   python3 tools/art/bz_gpt_combo.py
from PIL import Image, ImageFilter; import numpy as np
from scipy import ndimage
D='art/incoming/action/berserker/v4_cool/gpt_slash2/'
im=Image.open(D+'sheet.png').convert('RGBA'); a=np.asarray(im).copy()
a[(a[...,:3].min(2)>238)]=0
bands=[(0,152),(152,310),(310,495)]; C=12; cw0=1500/C; PAD=70
cells=[]
for (s,e) in bands:
    band=a[s:e]; m=band[...,3]>40
    lab,n=ndimage.label(m,structure=np.ones((3,3)))
    objs=ndimage.find_objects(lab)
    com=ndimage.center_of_mass(m,lab,range(1,n+1))
    X=np.arange(band.shape[1])[None,:].repeat(band.shape[0],0); cellof=np.minimum(C-1,(X//cw0).astype(int))
    for c in range(C):
        keep=np.zeros_like(m)
        for i in range(n):
            sl=objs[i]; wide=(sl[1].stop-sl[1].start)>1.6*cw0
            if wide: keep|=(lab==i+1)&(cellof==c)          # merged with neighbours: hard split at the cell lines
            elif int(min(C-1,max(0,com[i][1]//cw0)))==c: keep|=(lab==i+1)
        x0=int(max(0,c*cw0-PAD)); x1=int(min(1500,(c+1)*cw0+PAD))
        t=band[:,x0:x1].copy(); t[~keep[:,x0:x1]]=0
        km=keep[:,x0:x1]; l2,n2=ndimage.label(km,structure=np.ones((3,3)))
        if n2>1:
            sz=ndimage.sum(km,l2,range(1,n2+1)); big=int(np.argmax(sz))+1; sl=ndimage.find_objects(l2)
            for j in range(n2):   # pieces cut off a neighbour's swing at the cell lines go
                if j+1!=big and (sl[j][1].start<=1 or sl[j][1].stop>=km.shape[1]-1 or abs((sl[j][1].start+sl[j][1].stop)/2-((c+.5)*cw0-x0))>cw0*.75): t[l2==j+1]=0
        cells.append((t,(c+.5)*cw0-x0))
# one scale PER ROW from its first frame (the stance with the sword on the shoulder): every row's body = 137 incl. horns
fr=[]
for r in range(3):
    f0=cells[r*C][0][...,3]>60; ys,xs=np.nonzero(f0); K=137/(ys.max()-ys.min()); print('row',r,'scale',round(K,3))
    for t,ax in cells[r*C:(r+1)*C]:
        i=Image.fromarray(t); fr.append((i.resize((round(i.width*K),round(i.height*K)),Image.LANCZOS),ax*K))
W=sum(f.width for f,_ in fr); H=max(f.height for f,_ in fr)
strip=Image.new('RGBA',(W,H)); x=0; pos=[]
for f,_ in fr: strip.alpha_composite(f,(x,0)); pos.append(x); x+=f.width
arr=np.asarray(strip).copy(); m=arr[...,3]>110
q=Image.fromarray(arr[...,:3]).filter(ImageFilter.UnsharpMask(1.0,80,2)).quantize(40,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
pal=np.array(q.getpalette()[:120]).reshape(-1,3); idx=np.asarray(q)
o=np.zeros_like(arr); o[...,:3]=pal[idx]; o[...,3]=m*255
out=[]
for (f,ax),x in zip(fr,pos):
    t=o[:f.height,x:x+f.width].copy()
    P=np.zeros((t.shape[0]+2,t.shape[1]+2,4),np.uint8); P[1:-1,1:-1]=t; al=P[...,3]>0; nb=np.zeros_like(al)
    for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)): nb|=np.roll(np.roll(al,dy,0),dx,1)
    P[nb&~al]=(12,6,8,255); out.append((Image.fromarray(P),ax))
CW=max(f.width for f,_ in out)+20; CH=max(f.height for f,_ in out)
G=(150,160,110,255); gifs=[]
for j in range(C):
    sh=Image.new('RGBA',(CW*3,CH),G)
    for r in range(3):
        f,ax=out[r*C+j]; sh.alpha_composite(f,(int(r*CW+CW/2-ax),CH-f.height))
    gifs.append(sh.resize((sh.width*2,sh.height*2),0).convert('RGB').quantize(255))
gifs[0].save('art/incoming/action/berserker/v4_cool/gpt_slash2_x2.gif',save_all=True,append_images=gifs[1:],duration=[220]+[80]*10+[300],loop=0)
for i,(f,_) in enumerate(out): f.save(D+'px_%02d.png'%i)
# the combo: slash down -> rising slash -> overhead slam, joined where the poses meet
seq=[(0,j) for j in range(0,11)]+[(1,j) for j in range(1,12)]+[(2,j) for j in range(4,12)]
CW2=CW+60; frames=[]
# feet anchor per row = its first frame's feet centre
anc=[]
for r in range(3):
    f,ax=out[r*C]; al=np.asarray(f)[...,3]>0; ys,xs=np.nonzero(al); b=ys.max(); anc.append(xs[ys>=b-4].mean()-ax)
for r,j in seq:
    f,ax=out[r*C+j]; sh=Image.new('RGBA',(CW2,CH),G); sh.alpha_composite(f,(int(CW2*.42-ax-anc[r]),CH-f.height)); frames.append(sh)
gg=[x.resize((x.width*2,x.height*2),0).convert('RGB').quantize(255) for x in frames]
gg[0].save('art/incoming/action/berserker/v4_cool/gpt_combo_x2.gif',save_all=True,append_images=gg[1:],duration=[200]+[75]*(len(gg)-2)+[400],loop=0)
strip=Image.new('RGBA',(CW2*len(frames)//2,CH*2),G)
for i,x in enumerate(frames): strip.alpha_composite(x,((i%(len(frames)//2))*CW2,(i//(len(frames)//2))*CH))
strip.save(D+'combo_strip.png'); print(len(frames))
