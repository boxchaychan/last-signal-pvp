# Pose guide sheets for GPT (owner 2026-11-13: "การวาดเราให้ GPT วาดไง ใช้ของให้ถูกที่" = GPT draws, our tools pose / join / check).
# We design the move as a colour-coded stick figure (one colour per limb, chibi proportions), one pose per cell; GPT gets this sheet
# + the character picture and draws the character in every cell in that pose. Because WE made the guide, we know for every cell
# where the feet, the head and the weapon should be (poses.json): the cutter can line frames up without guessing.
#   python3 tools/art/pose_guide.py -> art/incoming/dogcat/pose/slash8_guide.png (1536x1024, 4x2 cells) + slash8_poses.json
import json, math
from PIL import Image, ImageDraw, ImageFont
O = 'art/incoming/dogcat/pose/'; CW, CH = 384, 512; GY = 440
COL = dict(head=(250, 210, 60), torso=(60, 110, 230), armF1=(230, 50, 50), armF2=(250, 140, 40), armB1=(150, 70, 200), armB2=(240, 120, 200),
           legF1=(40, 170, 70), legF2=(150, 220, 60), legB1=(20, 140, 150), legB2=(90, 210, 230), sword=(120, 120, 130))
#        lean  armF(up,fore)  sword  armB(up,fore)  legF(up,low)  legB(up,low)  hip dx,dy     angles: 0 = right, 90 = down
POSES = [( 0,  ( 60, -50), -125, ( 150,  95), ( 80, 95), (100, 95),   0,  0),      # 0 stand, sword on the shoulder
         (-8,  (-70,-110), -150, (120,  60), ( 72,100), (108,100),  -4,  6),      # 1 lifts it
         (-14, (-110,-85), -100, (130,  40), ( 70,102), (112,102),  -8, 10),      # 2 wound up, sword high behind
         ( 8,  (-60, -45),  -70, (140,  90), ( 62, 98), (116,104),   8,  6),      # 3 swing starts, step forward
         ( 18, ( 15,   5),   15, (150, 110), ( 55, 95), (124,108),  22,  8),      # 4 HIT: arm and sword straight ahead
         ( 20, ( 50,  40),   48, (140, 100), ( 56, 96), (124,108),  24, 10),      # 5 follow-through, sword low
         ( 8,  ( 70,  10),  -35, (125,  80), ( 70, 96), (110,100),  10,  4),      # 6 pulls back
         ( 0,  ( 60, -50), -125, (115,  70), ( 80, 95), (100, 95),   0,  0)]      # 7 stand again
def pt(p, ang, l): return (p[0] + math.cos(math.radians(ang)) * l, p[1] + math.sin(math.radians(ang)) * l)
def joints(pose):
    lean, aF, sw, aB, lF, lB, dx, dy = pose; hip = (CW * .36 + dx, GY - 78 + dy); neck = pt(hip, -90 + lean, 62); head = pt(neck, -90 + lean * .6, 66)
    J = dict(hip=hip, neck=neck, head=head); sh = pt(hip, -90 + lean, 52)
    J['elbF'] = pt(sh, aF[0], 40); J['handF'] = pt(J['elbF'], aF[1], 36); J['tip'] = pt(J['handF'], sw, 96)
    J['elbB'] = pt(sh, aB[0], 38); J['handB'] = pt(J['elbB'], aB[1], 32)
    J['kneeF'] = pt(hip, lF[0], 36); J['footF'] = (pt(J['kneeF'], lF[1], 40)[0], GY); J['kneeB'] = pt(hip, lB[0], 36); J['footB'] = (pt(J['kneeB'], lB[1], 40)[0], GY); J['sh'] = sh
    return J
def draw(d, J, ox, oy):
    def seg(a, b, c, w=16): d.line((ox + J[a][0], oy + J[a][1], ox + J[b][0], oy + J[b][1]), fill=(20, 20, 24), width=w + 6); d.line((ox + J[a][0], oy + J[a][1], ox + J[b][0], oy + J[b][1]), fill=COL[c], width=w)
    seg('sh', 'elbB', 'armB1'); seg('elbB', 'handB', 'armB2'); seg('hip', 'kneeB', 'legB1'); seg('kneeB', 'footB', 'legB2')
    seg('hip', 'neck', 'torso', 40); seg('hip', 'kneeF', 'legF1'); seg('kneeF', 'footF', 'legF2')
    h = J['head']; d.ellipse((ox + h[0] - 69, oy + h[1] - 69, ox + h[0] + 69, oy + h[1] + 69), fill=(20, 20, 24)); d.ellipse((ox + h[0] - 64, oy + h[1] - 64, ox + h[0] + 64, oy + h[1] + 64), fill=COL['head'])
    d.polygon([(ox + h[0] + 64, oy + h[1] + 6), (ox + h[0] + 92, oy + h[1] + 16), (ox + h[0] + 60, oy + h[1] + 30)], fill=COL['head'], outline=(20, 20, 24))    # the nose shows the facing
    seg('handF', 'tip', 'sword', 8); seg('sh', 'elbF', 'armF1'); seg('elbF', 'handF', 'armF2')
if __name__ == '__main__':
    im = Image.new('RGB', (CW * 4, CH * 2), (255, 255, 255)); d = ImageDraw.Draw(im); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30); out = []
    for i, p in enumerate(POSES):
        ox, oy = i % 4 * CW, i // 4 * CH; J = joints(p); d.rectangle((ox, oy, ox + CW - 1, oy + CH - 1), outline=(190, 190, 190)); d.line((ox + 12, oy + GY + 12, ox + CW - 12, oy + GY + 12), fill=(150, 150, 150), width=3)
        draw(d, J, ox, oy); d.text((ox + 12, oy + 8), str(i + 1), fill=(90, 90, 90), font=F); out.append({k: [round(v[0]), round(v[1])] for k, v in J.items()})
    im.save(O + 'slash8_guide.png'); json.dump({'cell': [CW, CH], 'grid': [4, 2], 'ground': GY, 'hit': 4, 'poses': out}, open(O + 'slash8_poses.json', 'w')); print('ok')
