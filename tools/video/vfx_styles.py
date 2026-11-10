# Compare one cut effect (fx/vfx_bzslam) in 6 looks next to the Berserker (owner 2026-11-10 "เอฟเฟกต์ไม่เข้ากับตัวละคร ลองแปลงหลายแบบ").
# Run from the repo root; OUT below is a scratch folder.
import json, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
OUT='/tmp/claude-0/-home-user-last-signal-pvp/be576c95-f8fc-5b1b-80a5-8423c4aa1256/scratchpad/sty/'
m=json.load(open('fx/manifest.json'))['vfx_bzslam']; sh=Image.open('fx/vfx_bzslam.png').convert('RGBA')
def frame(i): return sh.crop(((i%m['cols'])*m['w'],(i//m['cols'])*m['h'],(i%m['cols']+1)*m['w'],(i//m['cols']+1)*m['h']))
K=0.85   # effect shrunk so the explosion is ~2.5x the hero's height (at 1.5 it was 4-6x: part of why it did not match)
hero=Image.open('art/incoming/action/berserker/pl_dl_paid/Idle/rotations/south-east.png').convert('RGBA'); hero=hero.crop(hero.getbbox())
RAMP=[(0,(8,3,6)),(.25,(45,4,14)),(.45,(150,10,34)),(.62,(255,28,60)),(.8,(255,80,44)),(.93,(255,130,70)),(1,(255,215,170))]
def outline(a, col=(20,8,10,255)):
    al=a[...,3]>0; nb=np.zeros_like(al)
    for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)): nb|=np.roll(np.roll(al,dy,0),dx,1)
    a=a.copy(); a[nb&~al]=col; return a
def pix(im, k=1, ncol=20, ramp=False):
    w,h=im.size; s=im.resize((max(1,round(w/k)),max(1,round(h/k))),Image.BOX); a=np.asarray(s).copy()
    a[...,3]=np.where(a[...,3]>110,255,0)
    if ramp:
        rgb=a[...,:3]/255; L=np.clip(.45*rgb.max(-1)+.55*(rgb@[.3,.55,.15]),0,1)**1.5; xs=[r[0] for r in RAMP]
        for c in range(3): a[...,c]=np.interp(L,xs,[r[1][c] for r in RAMP])
    q=Image.fromarray(a).convert('RGB').quantize(ncol,dither=Image.Dither.NONE).convert('RGB'); b=np.dstack([np.asarray(q),a[...,3]])
    b=outline(b); return Image.fromarray(b.astype(np.uint8)).resize((w,h),Image.NEAREST)
def cel(im):
    a=np.asarray(im).copy(); rgb=a[...,:3].astype(float)/255; L=rgb@[.3,.55,.15]
    pal=np.array([[25,10,12],[150,20,20],[240,70,30],[255,170,40],[255,240,170]]); idx=np.digitize(L,[.12,.32,.55,.78])
    a[...,:3]=pal[idx]; a[...,3]=np.where(a[...,3]>90,255,0); return Image.fromarray(a.astype(np.uint8))
def glow(im):
    a=np.asarray(im).astype(float); rgb=a[...,:3]; L=(rgb@[.3,.55,.15])/255
    a[...,3]=a[...,3]*np.clip((L-.08)/.25,0,1)          # drop the black ink lines and the dark smoke
    base=Image.fromarray(a.clip(0,255).astype(np.uint8)); bl=base.filter(ImageFilter.GaussianBlur(10))
    out=Image.alpha_composite(bl, base); return out
STY=[('1 ต้นฉบับ (การ์ตูนเส้นดำ เนียน)', lambda f: f),
     ('2 พิกเซลขนาดเท่าตัวละคร', lambda f: pix(f,1,20)),
     ('3 พิกเซลเม็ดใหญ่ (×2)', lambda f: pix(f,2,16)),
     ('4 พิกเซล โทนแดงนีออน-ดำ', lambda f: pix(f,1,16,True)),
     ('5 การ์ตูนสีแบน 5 สี', lambda f: cel(f)),
     ('6 แสงเรือง ไม่มีเส้น (แบบ HD-2D)', lambda f: glow(f))]
F=ImageFont.truetype('/usr/share/fonts/opentype/tlwg/Loma-Bold.otf', 22)
PW,PH=440,440; bgc=(92,150,62,255)
def panel(i, sty, label):
    f=frame(i); f=f.resize((round(f.width*K),round(f.height*K)),Image.LANCZOS); g=sty(f)
    c=Image.new('RGBA',(PW,PH),bgc); fx,fy=110,PH-40
    c.alpha_composite(hero,(fx-hero.width//2-10,fy-hero.height))
    ex=fx+40+round(m['ax']*K); c.alpha_composite(g,(ex-round(m['ax']*K), fy-round(m['ay']*K)))
    d=ImageDraw.Draw(c); d.rectangle((0,0,PW,36),fill=(0,0,0,180)); d.text((10,6),label,font=F,fill=(255,255,255,255)); return c
def grid(i, s=1.0):
    G=Image.new('RGBA',(PW*3+20,PH*2+10),(30,30,30,255))
    for j,(lab,sty) in enumerate(STY): G.alpha_composite(panel(i,sty,lab),((j%3)*(PW+10),(j//3)*(PH+10)))
    return G if s==1 else G.resize((round(G.width*s),round(G.height*s)),Image.NEAREST)
grid(12).convert('RGB').save(OUT+'compare_peak.png'); grid(30).convert('RGB').save(OUT+'compare_late.png')
fr=[grid(i,.5).convert('RGB').quantize(200,dither=Image.Dither.NONE) for i in range(0,48,2)]
fr[0].save(OUT+'compare.gif',save_all=True,append_images=fr[1:],duration=83,loop=0); print('ok')
