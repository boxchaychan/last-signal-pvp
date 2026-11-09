# pixelfx sprite sheets -> game fx/<key>.png + fx/manifest.json entries (w,h,ox,oy,fps,n,cols,ax,ay,land).
# 1) git clone https://github.com/patch-gg/pixelfx (MIT, notice in vendor/pixelfx)
# 2) in that clone: node tools/render.mjs <ids> --sheet --no-actor --fps 10|12|15 --out <dir>
# 3) python3 tools/art/pixelfx_import.py <dir> fx   (edit the list L below to add effects)
# Crops empty space, drops empty wind-up frames, keeps at most N frames (fading the cut), quantizes to 200 colours.
# Anchor: c = centre of the ink, g = x centre + ground line. land = seconds until the effect hits the ground.
import json,sys,os,numpy as np
from PIL import Image
SRC,DST=sys.argv[1],sys.argv[2]
# key: (id, anchor mode c=centre g=ground, max frames, playback fps)
L={'slash2':('melee/double-slash','c',13,18),'flurry':('melee/dagger-flurry','c',15,18),'smash':('melee/hammer-smash','g',20,20),
 'spark':('impacts/hit-spark','c',9,18),'critx':('impacts/crit-hit','c',15,18),'boom':('explosions/small-explosion','g',30,20),
 'parry':('impacts/parry','c',16,18),'tstop':('arcane/time-stop','c',44,15),'starfall':('arcane/star-fall','g',31,15),
 'healaoe':('holy/heal-aoe','g',36,15),'feather':('holy/feather-burst','c',37,15),'hex':('shadow/hex-sigil','c',51,16),
 'mburst':('arcane/mana-burst','c',23,15),'quake':('nature/quake','g',30,15),'darkx':('shadow/dark-explosion','c',30,12),
 'pillar':('holy/holy-pillar','g',30,12),'firering':('fire/fire-ring','g',30,10),
 'pmeteor':('fire/meteor','g',46,15)}   # owner 2026-11-09: the mage's meteor (falls in, explodes, smokes)
ONLY=sys.argv[3:]   # optional keys: import just these
man=json.load(open(os.path.join(DST,'manifest.json')))
tot=0
for key,(fid,mode,maxn,pfps) in L.items():
  if ONLY and key not in ONLY: continue
  name=fid.split('/')[1];j=json.load(open(os.path.join(SRC,fid,name+'.json')));m=j['meta']['pixelfx']
  im=np.array(Image.open(os.path.join(SRC,fid,name+'.png')).convert('RGBA'));fw,fh=m['frameSize'];cols=m['columns'];n=min(m['frames'],maxn)
  fr=[im[(i//cols)*fh:(i//cols)*fh+fh,(i%cols)*fw:(i%cols)*fw+fw] for i in range(m['frames'])]
  # drop empty wind-up frames at the start (hits should show at once), then keep at most maxn
  s0=[f[:,:,3].astype(float).sum() for f in fr];mx=max(s0);st=0
  while st<len(fr)-1 and s0[st]<mx*.03:st+=1
  fr=fr[st:st+maxn];n=len(fr)
  A=np.stack([f[:,:,3] for f in fr]).astype(float)
  # when the effect lands: the frame with the most ink in the bottom fifth (used for star-fall damage timing)
  bt=[(f[int(fh*.8):,:,3].astype(float)).sum() for f in fr];land=int(np.argmax(bt))
  # fade the last frames out if the effect was cut short
  if m['frames']-st>maxn:
    for k in range(min(5,n)):fr[n-1-k]=fr[n-1-k].copy();fr[n-1-k][:,:,3]=(fr[n-1-k][:,:,3]*(k+1)/6).astype(np.uint8)
  S=A.sum(0);ys,xs=np.where(S>0);x0,x1,y0,y1=max(0,xs.min()-2),min(fw,xs.max()+3),max(0,ys.min()-2),min(fh,ys.max()+3)
  W=S[y0:y1,x0:x1];yy,xx=np.mgrid[y0:y1,x0:x1];tw=W.sum()
  cx=(W*xx).sum()/tw
  if mode=='c':cy=(W*yy).sum()/tw
  else:
    rows=W.sum(1);cum=np.cumsum(rows)/rows.sum();cy=y0+int(np.searchsorted(cum,.93))
  w,h=x1-x0,y1-y0;C=min(8,n);R=(n+C-1)//C
  sheet=Image.new('RGBA',(w*C,h*R),(0,0,0,0))
  for i,f in enumerate(fr):sheet.paste(Image.fromarray(f[y0:y1,x0:x1]),((i%C)*w,(i//C)*h))
  q=sheet.quantize(colors=200,method=Image.Quantize.FASTOCTREE)
  out=os.path.join(DST,key+'.png');q.save(out,optimize=True);sz=os.path.getsize(out);tot+=sz
  man[key]={'w':int(w),'h':int(h),'ox':int(m['pivot'][0]-x0),'oy':int(m['pivot'][1]-y0),'fps':pfps,'n':int(n),'cols':C,'ax':int(round(cx-x0)),'ay':int(round(cy-y0)),'land':round(land/pfps,2),'src':'pixelfx '+fid}
  print(key,'skip',st,'land %.2fs'%(land/pfps),'n',n,'frame',w,h,'anchor',man[key]['ax'],man[key]['ay'],'%dKB'%(sz//1024))
json.dump(man,open(os.path.join(DST,'manifest.json'),'w'),separators=(',',':'))
print('total KB',tot//1024)
