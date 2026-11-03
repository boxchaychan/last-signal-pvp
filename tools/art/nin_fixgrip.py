# usage: python3 nin_fixgrip.py <folder holding purple_raw.png red_raw.png made by gptpx.py ... noline>
# Nin purple/red: GPT drew the dagger blade coming out of the sleeve under the wrist. Move it so it leaves the fist.
# modes: revm (game) = reverse grip, blade from the bottom of the fist, mirrored to curve toward the body; rev0 = no mirror; reva = mirrored along the blade; flip = blade up out of the top (ring removed); rot = blade out to the side
import sys, numpy as np, colorsys
from PIL import Image
D=sys.argv[1]
def cls(p):
  r,g,b,al=[int(v) for v in p]
  if al==0:return '.'
  h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255);L=(r+g+b)/3
  if L<38:return 'k'
  if s<.18 and L>95:return 'g'
  if r>g+40 and r>b+40 and L>110 and g>90:return 's'
  if r>g+60 and b>g+40:return 'p'
  if r>g+70 and r>b+50:return 'r'
  return 'd'
def blade(a,rows,side,stop):
  # cells of the blade: per row, from the outer side inwards until a stop class or a gap
  cells={}
  W=a.shape[1]
  for y in rows:
    xs=range(W) if side=='L' else range(W-1,-1,-1);on=False
    for x in xs:
      c=cls(a[y,x])
      if not on:
        if c!='.':on=True
        else:continue
      if c=='.' or c in stop:break
      cells[(x,y)]=a[y,x].copy()
  return cells
def fix(a,rows,side,stop,ring,y_end,dx,mode='flip'):
  B=blade(a,rows,side,stop)
  for (x,y) in B:a[y,x]=0
  x0,y0,x1,y1=ring
  for y in (range(y0,y1+1) if not mode.startswith('rev') else []):
    for x in range(x0,x1+1):
      if cls(a[y,x])!='s':a[y,x]=0
  top=min(y for _,y in B);bx=round(np.mean([x for x,y in B if y==top]))
  for (x,y),v in B.items():
    if mode=='flip':ny=y_end-(y-top);nx=x+dx
    elif mode.startswith('rev'):
      u,w=x-bx,y-top
      if mode=='reva':u,w=((-w,-u) if side=='L' else (w,u))   # mirror across the blade's own line: tip hooks the other way
      if mode=='revm':u=-u
      nx,ny=bx+dx+u,y_end+w
    else:  # turn 90 degrees about the base so the curve keeps GPT's direction
      u,w=x-bx,y-top
      if side=='L':nx,ny=bx+dx-w,y_end+u
      else:nx,ny=bx+dx+w,y_end-u
    if 0<=ny<a.shape[0] and 0<=nx<a.shape[1] and cls(a[ny,nx])!='s':a[ny,nx]=v
def outline(a):
  h,w=a.shape[:2];pad=np.zeros((h+2,w+2,4),np.uint8);pad[1:-1,1:-1]=a;al=pad[:,:,3]>0
  ring=np.zeros_like(al)
  for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):ring|=np.roll(np.roll(al,dy,0),dx,1)
  ring&=~al;pad[ring]=(26,18,22,255);return pad
# purple: blade rows 64-77 (left side), stop at the purple cuff; ring x11-18 y52-57; blade base goes to row 56, 5 cells right
M=sys.argv[2] if len(sys.argv)>2 else "revm"  # revm = used in the game (owner: curve toward the body like gold Nin)
a=np.array(Image.open(D+'purple_raw.png').convert('RGBA'))
fix(a,range(64,78),'L','p',(11,52,18,57),*((64,6) if M.startswith('rev') else (56,5)),M)
Image.fromarray(outline(a),'RGBA').save(D+'purple_'+M+'.png')
# red: left blade rows 78-89 stop at red cuff, ring x17-23 y67-72, base to row 70, 4 right
#      right blade rows 79-89 scanned from the right, ring x68-73 y67-72, base to row 70, 3 left
a=np.array(Image.open(D+'red_raw.png').convert('RGBA'))
fix(a,range(78,90),'L','r',(17,67,23,72),*((78,5) if M.startswith('rev') else (70,4)),M)
fix(a,range(79,90),'R','r',(68,67,73,72),*((78,-4) if M.startswith('rev') else (70,-3)),M)
Image.fromarray(outline(a),'RGBA').save(D+'red_'+M+'.png')
