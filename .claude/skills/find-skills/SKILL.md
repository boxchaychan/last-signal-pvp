---
name: find-skills
description: Choose by itself which Claude skills a job needs, use the ones already installed, and offer a safe install when one is really missing. Use at the start of any new or multi-step job (a new character, moves, effects, a new game system, a new kind of file), without being asked, and whenever the owner says "หาสกิล", "มีสกิลไหม", "ติดตั้งสกิล", "find skills", "install a skill", asks what skills exist, or brings a skill / plugin name or link, even without the word "skill" (for example "มีตัวช่วยทำ VFX ไหม").
---

# Find skills

The owner is not a programmer and watches token cost. Answer in short, plain Thai, and spend as little as possible: stop at the first step that answers the question.

## Choosing on your own
The owner wants the right skills picked without having to name them (owner 2026-11-22: "มันจะเลือกสกิลที่เราจำเป็นต้องใช้เอง").
- At the start of a new or multi-step job, read the skill list in this session, pick only the ones this job needs, load them and get on with the work. Tell the owner in one line which ones you picked. Do not stop to ask.
- Skip this for a quick question or a one-line fix, and do it once per job: loading skills that are not needed costs tokens.
- Search the catalog (step 3) only when a clear part of the job has no skill and a skill would really change the result. Installing is always the owner's press on the card, so carry on with the work meanwhile.

## 1. Name the need
Turn the request into 2 to 4 short English keywords (the catalog is in English). "ทำเอฟเฟกต์พิกเซล" becomes `pixel`, `vfx`, `sprite`.

## 2. Look at what is already here
Most answers end here, and a skill already in hand costs nothing to install.
- The skill list in this session.
- `.claude/skills/` in this project and `~/.claude/skills/` on the PC.
- `ListSkills` and `ListPlugins` with the keywords (load them with `ToolSearch` if they are deferred).

If one fits, say its name and what it does, and offer to use it now.

## 3. Search the catalog
Only if step 2 found nothing: run `SearchSkills`, then `SearchPlugins`, with the same keywords. Plugin results are long, so send one search with all the keywords rather than several.

Rank what comes back by:
1. It does the job asked for, judged from its description and skill names, not from a matching word.
2. Small beats big. A pack of 36 skills to get one adds clutter, so say how many skills come with it.
3. Publisher: Anthropic or a named partner before `community`.
4. `reach`: `contained` before `privileged`, because a privileged plugin can do more on the machine. Say so if the best match is privileged.

## 4. Offer it
Show at most 3 choices, one line each: what it does, who made it, how many skills it brings. Then render the install card with `SuggestSkills` or `SuggestPluginInstall` (`trigger: "user_asked"`). The owner presses the button; a card alone installs nothing, so never say it is installed yet.

After the owner says they pressed it, confirm with `ListPlugins` / `ListSkills`. If it is on but not usable yet, suggest opening a new chat.

## A link or a name from outside the catalog
Skills can carry scripts that run on the owner's PC, so read before installing. Fetch the `SKILL.md` and list any scripts, then tell the owner in plain words what it does and anything risky (runs commands, sends data out, asks for keys, downloads more code). Install only after the owner says yes to that specific source. Do not run an install command for a source the owner did not name, and never paste an API key into one.

## Nothing fits
Say so plainly, and offer to build a small one with `skill-creator`. Project skills go in `.claude/skills/<name>/SKILL.md`.
