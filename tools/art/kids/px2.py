# pixelize the rendered SVG kids: magenta cut, box downscale, colour merge, 1-px dark outline
import sys, glob, os, numpy as np
from PIL import Image
D=sys.argv[1];OUT=sys.argv[2];HT=int(sys.argv[3]) if len(sys.argv)>3 else 100
for f in sorted(glob.glob(D+'/src_*.png')):
    A=np.array(Image.open(f).convert('RGB')).astype(int)
    mag=(A[:,:,0]>200)&(A[:,:,2]>200)&(A[:,:,1]<80)
    a=np.dstack([A,np.where(mag,0,255)]).astype(np.uint8);ys,xs=np.where(~mag);a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    im=Image.fromarray(a,'RGBA');w=max(1,round(im.width*HT/im.height))
    # premultiply so magenta never bleeds into edge pixels
    pm=np.array(im).astype(float);al=pm[:,:,3:]/255;pm[:,:,:3]*=al;sm=np.array(Image.fromarray(pm.astype(np.uint8),'RGBA').resize((w,HT),Image.BOX)).astype(float)
    alpha=np.array(im.split()[3].resize((w,HT),Image.BOX)).astype(float)/255
    rgb=np.where(alpha[:,:,None]>0,sm[:,:,:3]/np.maximum(alpha[:,:,None],1e-3),0).clip(0,255).astype(np.uint8)
    q=np.array(Image.fromarray(rgb).quantize(colors=64,method=Image.MEDIANCUT,dither=Image.NONE).convert('RGB'))
    res=np.zeros((HT,w,4),np.uint8);res[:,:,:3]=q;res[:,:,3]=np.where(alpha>.45,255,0)
    pad=np.zeros((HT+2,w+2,4),np.uint8);pad[1:-1,1:-1]=res;m=pad[:,:,3]>0;ring=np.zeros_like(m)
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):ring|=np.roll(np.roll(m,dy,0),dx,1)
    ring&=~m;pad[ring]=(36,22,26,255)
    name=os.path.basename(f)[4:]
    Image.fromarray(pad,'RGBA').save(OUT+'/kid_'+name);print(name,pad.shape[1],pad.shape[0])
