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

## Where the briefs are
- `docs/codex/dino/PROMPT.md`: prehistoric armour forms (pictures already in the game).
- `docs/codex/dino_anim/COMMANDS.md`: attack animations of the 5 prehistoric forms in 4 directions, made with the skill `$game-character-sprites` (https://github.com/tachikomared/character-animation-creator-skill).
- `docs/bb-prompts.html`: every picture prompt for the game (kids, tiers, forms, beasts, demons, animations).
- `docs/babies-and-beasts.md`: game design and the owner's decisions.

## Picture rules (all game characters)
- Pixel art, characters face RIGHT unless the task asks for other directions, plain white or see-through background, no text, no watermark.
- Both eyes fully visible (no hair over the eyes). Keep each kid's face, hair and eye colour the same as their gold picture `art/bb/kid_<class>_gold.png`.
- Classes: warrior = Tan, assassin = Nin, hunter = Fah, mage = Ratri, support = Chan, curse = Mok.
