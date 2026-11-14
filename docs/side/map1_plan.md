# Side game, map 1 plan (owner 2026-11-14: "ทำแมพไปก่อน เอาสวยๆ ทำให้สว่างกว่านี้หน่อย · วางแผนแมพก่อนสร้างจริง อะไรอยู่ตรงไหน แบบไหน กว้างเท่าไหร่")
Layout sketch: `docs/side/map1_plan.png` (scale 1:4). NOT built yet: waiting for the owner's OK.

Name: ป่าตะวันรอน (golden-hour forest). Size 3,200 x 1,100 world px (~4 phone screens wide, ~2.5 tall; now 2,400 x ~700).
Light: brighter than the current dusk: warm golden-hour sky (blue -> peach), light only slightly tinted, sun glow + light rays, fireflies / pollen;
dusk stays as `&mood=dusk`.

Zones left -> right:
1. Camp, 0-500, safe: spawn point, warp portal (back / later town), campfire, a hut and fence (the tribe game's PixelLab objects), signpost, later a shop NPC.
2. Mushroom meadow, 500-1300, Lv 1-2: flat ground + 3 low platforms (one rope), ~7 shrooms.
3. Wolf hill, 1300-2100, Lv 2-4: ground rising in 3 steps, platforms up to tier 2, 2 ropes, ~8 wolves + goblins.
4. Ruins, 2100-2800, Lv 4-5: broken stone platforms (grey tiles), tier 3 with a treasure chest at the top, 2 ropes, ~5 skeletons.
5. Boar den, 2800-3200, Lv 6: flat arena, 3 boar guards + a boss (big boar, red ground warnings), warp portal to map 2.
Tiers: ground ~1000, tier 1 ~800, tier 2 ~640, tier 3 ~470-560.
New: climbing ropes (up / down while touching a rope), stepped ground, parallax: far mountains (bg.png), mid trees, near foreground bushes over the hero's feet.
Art: reuse (map30 tiles / tree / bg, tribe hut / fire / fence, monsters); ropes, signpost, chest, portal glow, light rays drawn in code. Free, no PixelLab.
