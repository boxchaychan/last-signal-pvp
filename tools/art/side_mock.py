from PIL import Image, ImageDraw; import numpy as np, json, math
from scipy import ndimage
D='art/incoming/action/berserker/v5_style/'
def cut(im):
    a=np.asarray(im.convert('RGBA')).copy(); bgm=(a[...,:3].min(2)>225)|(a[...,3]<20)
    lab,_=ndimage.label(bgm); bd=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}; a[np.isin(lab,list(bd))]=0
    a[(a[...,:3].min(2)>238)]=0; return Image.fromarray(a)
def figs(im):
    a=np.asarray(im)[...,3]>0; lab,n=ndimage.label(ndimage.binary_dilation(a,iterations=2))
    ob=sorted([s for s in ndimage.find_objects(lab) if s and s[0].stop-s[0].start>40],key=lambda s:s[1].start)
    return [im.crop((s[1].start,s[0].start,s[1].stop,s[0].stop)) for s in ob]
side256=figs(cut(Image.open(D+'out_256.png')))[1]; side160=figs(cut(Image.open(D+'out_basic.png')))[1]
SW,SH=2532,1170
def mob(k):
    m=json.load(open('art/action/mobs_hr/%s.json'%k)); im=Image.open('art/action/mobs_hr/%s.png'%k).convert('RGBA')
    c=im.crop((0,0,m['w'],m['h'])); return c.crop(c.getbbox())
mobs=[mob(k) for k in ('skeleton','wolf','shroom','boar_guard')]
def scene(hero,k):
    img=Image.new('RGBA',(SW,SH)); d=ImageDraw.Draw(img)
    for y in range(SH):
        t=y/SH; d.line((0,y,SW,y),fill=(int(111+122*t),int(180+66*t),255))
    for col,top,amp,ph in (((159,196,232),420,160,1),((127,176,138),640,120,2),((93,148,96),800,80,3)):
        d.polygon([(0,SH)]+[(x,int(top-amp*(.5+.3*math.sin(x/260+ph)+.2*math.sin(x/90+ph*2)))) for x in range(0,SW+10,10)]+[(SW,SH)],fill=col)
    floor=SH-150
    def plat(x,y,w,h):
        d.rectangle((x,y,x+w,y+h),fill=(122,79,44)); d.rectangle((x,y,x+w,y+12*k),fill=(63,154,58)); d.rectangle((x,y,x+w,y+4*k),fill=(111,208,90))
        for i in range(int(w/40)): xx=x+(i*37*k)%w; yy=y+20*k+(i*13)%max(1,h-30*k); d.rectangle((xx,yy,xx+8*k,yy+4*k),fill=(94,59,31))
    plat(0,floor,SW,150); plat(1300,floor-int(hero.height*k*1.25),700,int(40*k)); plat(150,floor-int(hero.height*k*1.1),520,int(40*k))
    H=hero.resize((hero.width*k,hero.height*k),Image.NEAREST); img.alpha_composite(H,(700,floor-H.height+4))
    sc=hero.height*k*0.8/mobs[0].height
    for m,x in zip(mobs,(1150,1600,1900,2250)):
        M=m.resize((max(1,int(m.width*sc)),max(1,int(m.height*sc))),Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT); img.alpha_composite(M,(x,floor-M.height+4))
    ov=Image.new('RGBA',(SW,SH),(0,0,0,0)); o=ImageDraw.Draw(ov)
    o.rectangle((0,SH-70,SW,SH),fill=(0,0,0,150)); o.rectangle((40,SH-52,520,SH-22),fill=(196,30,42,255)); o.rectangle((560,SH-52,1040,SH-22),fill=(30,86,196,255)); o.rectangle((0,SH-12,SW,SH),fill=(224,176,32,255))
    for (x,y,r) in ((2380,900,90),(2210,1010,62),(2210,830,62),(2330,700,62)): o.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,40),outline=(255,255,255,150),width=6)
    o.ellipse((60,760,300,1000),fill=(255,255,255,30),outline=(255,255,255,130),width=6)
    img.alpha_composite(ov); return img.convert('RGB')
out=[]
for hero,k,L in ((side160,1,'A'),(side256,1,'B'),(side160,2,'C')):
    s=scene(hero,k); s.save(D+'mock_%s.png'%L); out.append(s)
st=Image.new('RGB',(SW//2,SH//2*3+40),(20,20,20))
for i,s in enumerate(out): st.paste(s.resize((SW//2,SH//2),Image.LANCZOS),(0,i*(SH//2+20)))
st.save(D+'mock_all.png')
