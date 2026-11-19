// Builds viewer/data.js (catalog + 2x animation frames) for viewer/index.html: node viewer/build.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const catalog = JSON.parse(readFileSync(join(root, "catalog.json"), "utf8"));

// Catalog ids already in the game (MMORPG client/public/assets/monsters) -> the game's kind.
const IN_GAME = {
  mob_woods_boar: "Baby Boar", mob_vale_blob: "Sliming", mob_forest_tusker_boar: "Boar", mob_coast_crab: "Knight Crab",
  mob_forest_greymane_wolf: "Blue Wolf", mob_forest_bladearm_mantis: "Sharp Mantis", mob_forest_bramble_bear: "Wild Bear"
};

const monsters = catalog.monsters.map((m) => {
  const atlas = JSON.parse(readFileSync(join(root, m.sprite, `${m.id}.atlas.json`), "utf8"));
  const s = atlas.scales["2x"];
  const anims = {};
  for (const [name, dirs] of Object.entries(atlas.animations)) {
    const keys = Object.values(dirs)[0];
    anims[name] = {
      ms: atlas.actions[name]?.delayMs ?? 120,
      f: keys.map((k) => { const f = atlas.frames[k]["2x"]; return [f.p, f.x, f.y, f.w, f.h, f.ox, f.oy]; })
    };
  }
  return {
    id: m.id, kind: m.kind, biome: m.biome, th: m.nameTH, en: m.nameEN, type: m.creatureType, el: m.element, role: m.role,
    aggro: m.aggro, tier: m.tier, size: m.size, h: m.heightWorld, family: m.family, desc: m.descTH,
    issues: m.artIssues || null, fit: m.biomeFit, inGame: IN_GAME[m.id] || null,
    pages: s.pages.map((p) => `../${m.sprite}/${p.file}`), cell: s.cell, anims
  };
});

const biomes = catalog.biomes.map((b) => ({ key: b.key, th: b.nameTH }));
writeFileSync(join(root, "viewer", "data.js"), `window.CATALOG = ${JSON.stringify({ biomes, monsters })};\n`);
console.log(`${monsters.length} monsters -> viewer/data.js`);
