"""Build the small facial and hand patches from the supplied Zeus artwork."""
from PIL import Image, ImageDraw
from pathlib import Path
P = Path(__file__).parent
base = Image.open(P / 'source.png').convert('RGBA')
for label in ('blink','focused','shout'):
    # Facial features stay on the original face, without replacing its outline.
    crop = base.crop((112,120,209,173)).resize((388,212), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(crop)
    def p(x, y): return ((x-112)*4, (y-120)*4)
    def shape(box): return (*p(*box[:2]),*p(*box[2:]))
    skin = base.getpixel((151,150))
    dark = (28,16,12,255)
    for x in (133,190):
        draw.rounded_rectangle(shape((x-10,130,x+10,155)),radius=9,fill=skin)
        if label=='blink':
            draw.arc(shape((x-8,134,x+8,149)),192,348,fill=dark,width=12)
        else:
            eye = (x-7,133,x+7,151) if label=='focused' else (x-7,129,x+7,151)
            draw.ellipse(shape(eye),fill=dark)
    if label=='shout':
        draw.ellipse(shape((145,153,181,171)),fill=skin)
        draw.ellipse(shape((150,151,176,171)),fill=dark)
        draw.ellipse(shape((156,163,171,169)),fill=(225,112,91,255))
    crop.resize((97,53),Image.Resampling.LANCZOS).save(P / f'face-{label}.png')
# Use the supplied open hand with the green fringe cleaned and a leftward orientation.
palm=Image.open(P/'palm.png').convert('RGBA')
for y in range(palm.height):
    for x in range(palm.width):
        r,g,b,a=palm.getpixel((x,y))
        if g>max(r,b)+15:
            palm.putpixel((x,y),(r,min(g,max(r,b)),b,a if g<max(r,b)+65 else 0))
palm=palm.resize((53,46),Image.Resampling.LANCZOS).rotate(126,Image.Resampling.BICUBIC,expand=True)
palm.save(P/'hand-open.png')
fist=Image.open(P/'fist.png').convert('RGBA')
for y in range(fist.height):
    for x in range(fist.width):
        r,g,b,a=fist.getpixel((x,y))
        if g>max(r,b)+15:
            fist.putpixel((x,y),(r,min(g,max(r,b)),b,a if g<max(r,b)+65 else 0))
fist=fist.resize((36,34),Image.Resampling.LANCZOS).rotate(-49,Image.Resampling.BICUBIC,expand=True)
fist.save(P/'hand-grip.png')
