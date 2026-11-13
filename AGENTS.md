# Notes for Codex / GPT agents

The owner speaks Thai and is not a programmer: reply in Thai, short and plain.

Main project: **Babies & Beasts** (`bb.html`), a pixel-art tower defense played in the browser. The live game is GitHub Pages from `main`: anything merged into `main` goes live at once.

Who does what (owner 2026-11-06, after connecting the repo to GPT):
- **Claude Code** writes the game code (`bb.html`, `tools/`, `CLAUDE.md`) and brings new art into the game.
- **GPT / Codex** makes pictures and animations.

## Rules
- Do not edit `bb.html`, `index.html`, `CLAUDE.md` or `tools/` unless the owner asks for exactly that in this task. Two agents editing the same file at once breaks things.
- Never push to `main` and never merge a pull request. Work on a new branch named `codex/<short-task>` and open a pull request; the owner hands it to Claude to bring into the game.
- Put generated pictures in `art/incoming/<short-task>/`: full-size PNG, not shrunk, not converted to a small pixel grid (Claude's converters do that), plus a short `REPORT_TH.txt` saying which file is which and anything that did not come out right.
- Keep each file under about 10 MB.

## Doing the next job by yourself
If the owner just says "ทำท่าตัวต่อไป" / "ทำงานต่อ" / "next animation" (or a GitHub issue comment asks for it), follow `docs/codex/legends/ANIM_QUEUE.md`: take the first `todo` row, run its prompt with `$game-character-sprites`, push the full run folder on `codex/anim-<key>` and open a pull request. No need to ask the owner to attach or paste anything: the reference picture and the prompt are in the repository.

## Where the briefs are
- `docs/codex/action/CLASS2.md`: class-2 hero designs (archer: dual-pistol gunslinger, great-bow archer), one turnaround each, branch `codex/class2` ("ทำคลาส 2").
- `docs/codex/action/MAPS.md`: map art for the action game (Thai wall pieces, the China map: buildings, village, nature, props, ground; one sheet per row, branch of your own in `../last-signal-pvp-codex`).
- Order when told to keep going until the credits run out: MOBS.md todo rows → MOB_ANIM.md todo rows for those monsters → MAPS.md → FX.md.
- `docs/codex/action/SLASH.md`: sword-combo frames for the new chibi pixel swordsman (4 rows, one picture each: a numbered pose sheet + the character picture attached, both in `art/poses/ref_sketch/`; branch `codex/chibi-slash`; "ทำท่าฟัน" = the first `todo` row, row 1 first and stop).
- `docs/codex/action/FX.md`: skill / attack effects for the action game (20 rows, one 3x2 picture each on PURE GREEN #00FF00 in a vivid black-ink + bright colour style, branch `codex/fx`; "ทำเอฟเฟคต่อ" = the next `todo` row). Switch the folder back to `main` when you stop.
- `docs/codex/action/MOB_ANIM.md`: animation frames for those monsters (45 rows: walk / attack / death per monster, one 3x2 picture each, branch `codex/mob-anim`; "ทำเฟรมมอนต่อ" = the next `todo` row). Switch the folder back to `main` when you stop.
- `docs/codex/action/MOBS.md`: the monster set for the action game `action.html` (queue, one picture per monster, style picture `docs/codex/action/refs/00_STYLE_hero.png`, branch `codex/mobs`; "ทำมอนต่อ" = the next `todo` row).
- `docs/codex/legends/ANIM_QUEUE.md`: animation queue for the new cast (heroes + gods), with the reference picture and prompt file for each.
- `docs/codex/legends/PROMPT.md` and `docs/legends-prompts.html`: all prompts for the new cast (pictures, animations, skill effects).
- `docs/codex/dino/PROMPT.md`: prehistoric armour forms (pictures already in the game).
- `docs/codex/dino_anim/COMMANDS.md`: attack animations of the 5 prehistoric forms in 4 directions, made with the skill `$game-character-sprites` (https://github.com/tachikomared/character-animation-creator-skill).
- `docs/bb-prompts.html`: every picture prompt for the game (kids, tiers, forms, beasts, demons, animations).
- `docs/babies-and-beasts.md`: game design and the owner's decisions.

## Picture rules (all game characters)
- Pixel art, characters face RIGHT unless the task asks for other directions, plain white or see-through background, no text, no watermark.
- Both eyes fully visible (no hair over the eyes). Keep each kid's face, hair and eye colour the same as their gold picture `art/bb/kid_<class>_gold.png`.
- Classes: warrior = Tan, assassin = Nin, hunter = Fah, mage = Ratri, support = Chan, curse = Mok.
- 2026-11-06 the owner replaced the kids with a new cast of legends (gold = heroes, rainbow = gods); their finished pictures are `art/incoming/legends/<key>.png` and are the reference for that character. The kid rules above only apply to old kid tasks.
