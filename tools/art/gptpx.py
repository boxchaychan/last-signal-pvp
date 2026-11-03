# needs numpy, pillow, scipy
# GPT "pixel art" picture (white bg) -> true pixel sprite on GPT's own grid
# usage: python3 gptpx.py in.png out.png [merge distance, 14] [noline]
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
src,out=sys.argv[1],sys.argv[2];NC=int(sys.argv[3]) if len(sys.argv)>3 else 32
A=np.array(Image.open(src).convert('RGB')).astype(int);H,W,_=A.shape
near=(A.min(2)>226)&(A.max(2)-A.min(2)<26)
lab,n=nd.label(near)
edge=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
sizes=nd.sum(near,lab,range(1,n+1))
bg=np.zeros((H,W),bool)
for i in range(1,n+1):
    if i in edge or sizes[i-1]>2500:bg|=lab==i   # outside + very big enclosed holes; eye whites stay
# GPTPX_HALO=1: also cut a pale glow round the figure (light, low-saturation pixels joined to the border)
import os
if os.environ.get('GPTPX_HALO'):
    mx=A.max(2);pale=(mx>196)&(A.min(2)>120)&((mx-A.min(2))/np.maximum(mx,1)<.45)
    l2,n2=nd.label(pale);e2=set(np.unique(np.r_[l2[0],l2[-1],l2[:,0],l2[:,-1]]))-{0}
    for i in e2:bg|=l2==i
fig=~bg
# drop small separate bits (sparkles); keep parts bigger than 2% of the main body
fl,fn=nd.label(fig);fs=nd.sum(fig,fl,range(1,fn+1));keep=fs>fs.max()*.02
fig=np.isin(fl,np.where(keep)[0]+1);print('parts kept',keep.sum(),'of',fn)
# grid
def fit(ax):
    d=np.abs(np.diff(A,axis=ax)).sum(2)>60;prof=d.sum(axis=1-ax).astype(float);xs=np.arange(len(prof))+1;best=None
    for p in np.arange(9,16,0.01):
        z=(prof*np.exp(2j*np.pi*xs/p)).sum();s=abs(z)
        if best is None or s>best[0]:best=(s,p,(np.angle(z)/(2*np.pi)*p)%p)
    return best[1],best[2]
px,ox=fit(1);py,oy=fit(0);print('grid x %.2f+%.1f  y %.2f+%.1f'%(px,ox,py,oy))
BIN=(A[:,:,0]//20)*169+(A[:,:,1]//20)*13+(A[:,:,2]//20)
xs=np.arange(ox-px,W,px);ys=np.arange(oy-py,H,py)
rows=[];
for y0 in ys:
    row=[]
    for x0 in xs:
        a0,a1=int(round(y0+py*.2)),int(round(y0+py*.8));b0,b1=int(round(x0+px*.2)),int(round(x0+px*.8))
        a0,b0=max(a0,0),max(b0,0);a1,b1=min(a1,H),min(b1,W)
        if a1<=a0 or b1<=b0:row.append((0,0,0,0));continue
        m=fig[a0:a1,b0:b1]
        if m.mean()<.5:row.append((0,0,0,0));continue
        v=BIN[a0:a1,b0:b1][m];c=np.bincount(v).argmax();px_=A[a0:a1,b0:b1][m][v==c].mean(0).round().astype(int);row.append((*px_,255))
    rows.append(row)
im=np.array(rows,np.uint8)
al=im[:,:,3]>0;yy,xx=np.where(al);im=im[yy.min():yy.max()+1,xx.min():xx.max()+1]
# merge near-identical colours (palette from cells, so small features like eyes keep their colour)
if NC:  # merge near-identical shades only (greedy, most common first); rare distinct colours like blush stay
  m=im[:,:,3]>0;cols,cnt=np.unique(im[m][:,:3],axis=0,return_counts=True);order=np.argsort(-cnt);pal=[];mp={}
  for i in order:
    c=cols[i].astype(int);hit=None
    for p in pal:
      if ((p-c)**2).sum()<NC*NC:hit=p;break
    if hit is None:pal.append(c);hit=c
    mp[tuple(cols[i])]=hit
  for y,x in zip(*np.where(m)):im[y,x,:3]=mp[tuple(im[y,x,:3])]
  print('colours',len(pal))
# 1-px dark outline (skip with a 4th arg 'noline')
if len(sys.argv)>4 and sys.argv[4]=='noline':
  Image.fromarray(im,'RGBA').save(out);print('size',im.shape[1],'x',im.shape[0]);sys.exit()
h,w=im.shape[:2];pad=np.zeros((h+2,w+2,4),np.uint8);pad[1:-1,1:-1]=im;al=pad[:,:,3]>0
ring=nd.binary_dilation(al,structure=[[0,1,0],[1,1,1],[0,1,0]])&~al;pad[ring]=(26,18,22,255)
Image.fromarray(pad,'RGBA').save(out);print('size',pad.shape[1],'x',pad.shape[0])
