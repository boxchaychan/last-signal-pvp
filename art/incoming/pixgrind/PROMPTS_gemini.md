# เกมเก็บเลเวลพิกเซล 3D (ตัวเดียวเปลี่ยนอาวุธ): คำสั่งให้ Gemini (ฟรี)

ลำดับงาน (owner 2026-11-26): 1 แมพสวย -> 2 ท่าลื่น -> 3 เอฟเฟกต์ฟันแรงๆ

วิธีใช้: เปิด Gemini เลือก "สร้างรูปภาพ" ถ้าเลือกสัดส่วนได้ให้เลือก 16:9 (แนวนอน)
วางคำสั่งภาษาอังกฤษ "ข้อ A, B หรือ C" แล้วต่อด้วย "ก้อนกลาง" ทั้งก้อน ได้รูปแล้วส่งมาเป็นไฟล์แนบ (ไม่ต้องวางในแชท)
ลองได้หลายข้อ แล้วเลือกรูปที่ชอบที่สุด 1 รูป = ภาพเป้าหมาย ผมจะทำชุดชิ้นส่วนแมพให้เข้ากับรูปนั้น

---

## ก้อนกลาง (ใส่ต่อท้ายทุกข้อของแมพ)
บอกแค่มุมกล้อง ความคม และขนาดตัวละคร ส่วนรูปทรงแมพให้ Gemini คิดเอง (ฉบับแรกบังคับหน้าผา + บันได + น้ำ จนทุกข้อออกมาเหมือนกัน)

```
MAP RULES: one gameplay screenshot of an original pixel-art action RPG where a hero fights packs of monsters to gain levels. Camera: high three-quarter top-down view, about 45 degrees down, straight on, landscape 16:9. Crisp pixel art at a low native resolution (about 640 x 360, hard square pixels), every pixel placed on purpose, clean outlines, a limited palette built around the colours named in PLACE, one clear light direction. Open ground with room to fight. One small adventurer in the middle for scale, about one sixth of the image height. No UI, no text, no logo, no watermark, no frame. Original design, not copied from any existing game.
```

แต่ละข้อมีของตัวเอง: ไอเดีย สีหลัก แสง เวลา และจุดเด่น 1 อย่าง (ไม่มีน้ำตก วิหาร สะพาน เป็นค่าเริ่มต้นอีกแล้ว)

## A. ป่าเห็ดยักษ์เรืองแสง ยามพลบค่ำ
```
PLACE: a forest floor of giant mushrooms at dusk. Huge mushroom caps form the canopy, some glowing soft cyan and pink from underneath, thick twisting roots make natural low walls and paths, a moss carpet, tiny glowing spores floating, small puddles reflecting the glow. Palette: deep violet, teal, cyan glow, warm pink accents. Light: the last orange sunset light from one side, cool glow everywhere else. Landmark: one ancient mushroom far bigger than the rest, with a hollow doorway in its stem.
```

## B. ทุ่งหญ้าสีทอง ลมแรง ยามบ่ายคล้อย
```
PLACE: a wide golden grassland on a windy late afternoon. Tall grass bending in waves, patches of red and white wildflowers, low flat rocks, a few lone wind-bent trees, a dirt track winding through. Palette: gold, ochre, sage green, sky-blue shadows. Light: low warm sun, long shadows, grass tips glowing. Landmark: the huge half-buried rib cage and skull of an ancient giant beast, grass growing through the bones.
```

## C. ที่ราบสูงหิมะ ใต้แสงออโรร่า ตอนกลางคืน
```
PLACE: a snowy highland at night under an aurora. Deep snow with trails of footprints, snow-loaded pine trees, blue ice rocks, a frozen lake with white cracks, wind blowing loose snow. Palette: white, pale blue, navy shadows, green and magenta aurora light, one warm orange campfire. Landmark: a ring of tall standing stones with frosted carvings.
```

## D. ชายหาดเกาะเขตร้อน ตอนเที่ยง
```
PLACE: a tropical island beach at noon. White sand, turquoise shallow water with waves and foam rolling in, coral rocks, leaning coconut palms, crabs, shells, a line of seaweed. Palette: white sand, turquoise, coral pink, lush green. Light: bright high sun, short sharp shadows. Landmark: a wrecked wooden ship lying on its side half in the sand.
```

## E. ที่ของคุณเอง หรือรูปแมพเกมที่ชอบ
- พิมพ์บอก: สถานที่ เวลา สี จุดเด่น 1 อย่าง ผมจะเขียนข้อ PLACE ให้
- ถ้ามีรูปแมพเกมที่ชอบ ส่งมาให้ผมดู (แค่ดูว่าชอบแสง สี มุมแบบไหน ไม่ลอก และไม่เก็บรูปไว้ในโปรเจกต์) ทางนี้ตรงใจที่สุด

---

## ตัวละคร: นักผจญภัย (ตัวเดียว เปลี่ยนอาวุธ)

ขนาดในเกม: ตัวสูง 64 พิกเซล (หัวถึงเท้า ไม่นับอาวุธ) บนแมพกว้าง 640 x สูง 360 พิกเซล = ประมาณ 1/6 ของความสูงจอ
(ขนาดใกล้ซุสพิกเซลในเกมผู้รับพร ที่สูง 60) 1 พิกเซลของตัว = 1 พิกเซลของแมพ ตัวกับแมพคมเท่ากัน
ตัว 64 ต้องเป็นรูปทรงใหญ่ๆ ชัดๆ: หัวโต (ราว 3 หัว) สีเป็นก้อน 5 สี ไม่มีลายเล็กหรือสายเส้นบางที่จะหายตอนย่อ

แบบที่ผมออกแบบ:
- แว่นกันลมทองเหลืองดันขึ้นไว้บนหัว = สัญลักษณ์นักผจญภัย มองเห็นแต่ไกล
- ผ้าคลุมไหล่สั้นมีฮู้ดสีแดง (ฮู้ดพับลง ยาวแค่อก) = สีเด่นที่สุด แดงตัดกับแมพทุกแบบ (ม่วง ทอง หิมะ ทะเล)
- เสื้อสีครีมพับแขนถึงศอก เสื้อกั๊กหนังสีน้ำตาล ถุงมือหนังตัดนิ้ว
- เข็มขัดกว้าง มีกระเป๋าย่ามเล็กข้างสะโพก และกระติกน้ำ
- กางเกงสีกรมท่า รองเท้าบูทหนังสูง พับขอบ
- มือว่างทั้งสองข้าง กำไว้เหมือนจับด้าม (อาวุธจะใส่ทีหลัง)
- สี 5 ก้อน: แดง ครีม น้ำตาล กรมท่า ทอง

วิธีสั่ง: วางข้อ 1 หรือ 2 แล้วต่อด้วย "ก้อนกลางตัวละคร" ถ้ามีภาพแมพเป้าหมายที่เลือกแล้ว แนบไปด้วย
ได้รูปแล้ว ผมจะตัดพื้นขาวและทดลองย่อเป็น 64 พิกเซลให้ดูก่อน (ฟรี)

## ก้อนกลางตัวละคร
```
HERO RULES: one original adventurer hero for a pixel-art action RPG seen from a high three-quarter top-down camera; if a map picture is attached, match its palette and light. Cute but cool game style: about 3 heads tall with a big readable face, thick clean dark outline, flat bright colours with soft cel shading. Built from BIG simple shapes and 5 clear colour blocks so it still reads when shrunk to 64 pixels tall: no tiny details, no thin straps, no patterns, no text. The hero changes weapons, so draw NO weapon and NO shield: both hands clearly visible, a little apart from the body, closed as if gripping a handle; nothing covers the arms. Three views on one pure white sheet, same size, feet on one line: front view seen a little from above (like the game camera), side view facing right, back view. Standing idle pose, full body head to feet, no ground, no shadow.
```

## 1. นักผจญภัยหญิง
```
CHARACTER: a cheerful, determined young woman adventurer. Chestnut hair in a short high ponytail with a few loose strands, bright eyes, brass goggles pushed up on her forehead. A short RED hooded capelet (hood down) that ends at the chest, leaving the arms free. Cream shirt with sleeves rolled to the elbows, a brown leather vest, brown fingerless leather gloves. A wide belt with a gold buckle, a small satchel on the left hip and a water flask. Dark navy trousers tucked into tall brown boots with folded tops.
```
(ต่อด้วยก้อนกลางตัวละคร)

## 2. นักผจญภัยชาย
```
CHARACTER: a cheerful, determined young man adventurer. Messy short brown hair, bright eyes, brass goggles pushed up on his forehead. A short RED hooded capelet (hood down) that ends at the chest, leaving the arms free. Cream shirt with sleeves rolled to the elbows, a brown leather vest, brown fingerless leather gloves. A wide belt with a gold buckle, a small satchel on the left hip and a water flask. Dark navy trousers tucked into tall brown boots with folded tops. Slightly broader shoulders.
```
(ต่อด้วยก้อนกลางตัวละคร)

ทางที่เสียเครดิต (เฉพาะเมื่อคุณสั่ง "เจน"): PixelLab แบบธรรมดาวาดตัวนี้เป็นพิกเซล 64 ตรงๆ 1 เครดิตต่อรูป
