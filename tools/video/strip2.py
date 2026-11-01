import sys,json
from PIL import Image
import numpy as np
# usage: strip2.py src out mode rows cols row(-1=all) [targetH]
src,out,mode,rows,cols,rowsel=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
TH=int(sys.argv[7]) if len(sys.argv)>7 else 320
im=Image.open(src).convert('RGBA');a=np.array(im)
a[...,3]=np.where(a[...,3]<32,0,a[...,3]);a[a[...,3]==0]=0
H,W=a.shape[:2];cw,ch=W//cols,H//rows
frames=[];anc=[]
for r in range(rows):
  if rowsel>=0 and r!=rowsel:continue
  for c in range(cols):
    sub=a[r*ch:(r+1)*ch,c*cw:(c+1)*cw].copy();al=sub[...,3]>128
    ys,xs=np.where(al);ymin,ymax=ys.min(),ys.max();hh=ymax-ymin
    if mode=='head':band=al[ymin:ymin+int(hh*.3)]
    else:band=al[ymax-int(hh*.12):ymax+1]
    bx=np.where(band.any(0))[0];ax=(bx.min()+bx.max())/2
    anc.append((ax,ymax));frames.append(sub)
n=len(frames)
L=T=R=B=0
for f,(ax,ay) in zip(frames,anc):
  ys,xs=np.where(f[...,3]>0);L=max(L,ax-xs.min());R=max(R,xs.max()-ax);T=max(T,ay-ys.min());B=max(B,ys.max()-ay)
L,R,T,B=[int(np.ceil(v))+4 for v in (L,R,T,B)];fw0,fh0=L+R,T+B
chh=max(ay-np.where(f[...,3]>128)[0].min() for f,(ax,ay) in zip(frames,anc))
sc=TH/chh;fw,fh=round(fw0*sc),round(fh0*sc)
strip=Image.new('RGBA',(fw*n,fh),(0,0,0,0))
for i,(f,(ax,ay)) in enumerate(zip(frames,anc)):
  cv=Image.new('RGBA',(fw0,fh0),(0,0,0,0));fi=Image.fromarray(f);cv.paste(fi,(int(round(L-ax)),int(round(T-ay))),fi)
  strip.paste(cv.convert('RGBa').resize((fw,fh),Image.LANCZOS).convert('RGBA'),(i*fw,0))
strip.quantize(256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE).save(out,optimize=True)
fax,fay=L*sc,T*sc
# head centre of last frame (to line up strips that were aligned on the feet)
last=np.array(strip.crop(((n-1)*fw,0,n*fw,fh)))[...,3]>128;ys,xs=np.where(last);band=last[ys.min():ys.min()+int((ys.max()-ys.min())*.3)];bx=np.where(band.any(0))[0]
# hand point in frame 0: rightmost opaque pixel between 35% and 62% of the height (fingers in front of the chest)
f0=np.array(strip.crop((0,0,fw,fh)))[...,3]>128;ys0,xs0=np.where(f0);top,bot=ys0.min(),ys0.max();y1,y2=int(top+(bot-top)*.35),int(top+(bot-top)*.62)
best=(0,0)
for y in range(y1,y2):
  r_=np.where(f0[y])[0]
  if len(r_) and r_.max()>best[0]:best=(r_.max(),y)
print(json.dumps(dict(n=n,fw=fw,fh=fh,fax=round(fax,1),fay=round(fay,1),ch=TH,headLast=round((bx.min()+bx.max())/2,1),hand=[round(best[0]-fax-12,1),round(best[1]-fay,1)])))
bg=Image.new('RGBA',strip.size,(90,100,90,255));bg.alpha_composite(strip);bg.convert('RGB').save(out.split('/')[-1].replace('.png','_prev.png'))
