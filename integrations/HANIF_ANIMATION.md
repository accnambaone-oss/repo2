# Hanif animation skill — first-class integration

Original upstream: https://github.com/buildwithhanif/claude-animation-skill
License: MIT per upstream README and `LICENSE`. The upstream skill runs using Node.js 20+, `@napi-rs/canvas` and FFmpeg; it does not use a paid API. Its **original source files are not included** in this ZIP because the builder had no GitHub download access. The integration below **installs the actual upstream skill** from GitHub or an offline checkout. Do not confuse the independently authored `scripts/rigs.py` with upstream JavaScript source.

## Install the original upstream alongside our custom skill

From the root of this ZIP:

```powershell
# Claude Code (inside your project):
py scripts/install_upstream_skills.py --target .claude/skills --npm
# OpenCode (inside your project):
py scripts/install_upstream_skills.py --target .opencode/skills --npm
```

If offline, download/extract the upstream GitHub repository on another machine and provide its path:

```powershell
py scripts/install_upstream_skills.py --from-directory "D:\Downloads\claude-animation-skill-main" --target .opencode/skills --npm
```

To avoid rewriting an existing skill, installer refuses to overwrite unless `--force` is explicitly supplied. It keeps the upstream LICENSE and a source pointer; you own the responsibility for honoring all upstream license conditions when redistributing it.

## How the two skills cooperate

**Pipeline A (Python SVG / CPU-friendly):** `cinematic-svg-explainers/SKILL.md` → story.json → `scripts/render.py`. This now includes *its own* animated multi-joint rat rig, independently moving actors, text reveals, particles, counts, escape steps, background texture and timeline QA. It **does not** call Hanif's Node library at runtime; the Hanif work influenced new, original features and checks.

**Pipeline B (Hanif JS hand-drawn):** the separately installed `claude-animation/SKILL.md` → `references/detail.md`, `references/motion.md`, `references/characters.md` → `templates/film-template.mjs` → `lib/film.mjs` (`sheet`, `strip`, `verify`, `render`) → its `scripts/music.mjs` and `scripts/sound.mjs`. Use this when the user specifically requests paper texture, hand-painted looks, watercolor, complex rig acting, sketch reveals, or true sequential 2D character animation. It is independently authored by buildwithhanif and is NOT a drop-in renderer for Python `story.json`.

**Editorial bridge:** Both paths can use the same shot breakdown and voice timing. For each beat specify the action's START pose, contact, END pose, camera, palette, and sound cue. For Hanif export one JavaScript film using the official template, with timecoded acts generated from our story beat sheet. Use FFmpeg to merge a Hanif-rendered animated segment into a Python motion-graphics edit where required; this is an edit, not a runtime code import.

## Production gate — specifically addresses the bad baseline preview

- Reject a scene made solely of one flattened illustration with a continuous digital zoom.
- Visible purposeful moving parts must change pose or position on-screen (falling, reaching, chewing, running, climbing, rotating diagram connectors, animated numerical counters).
- Rig at least head, tail, feet and eye states independently for narrative animals, not just moving a single image.
- Three material layers: base, stable texture, edge; grain must be deterministic, not animated random static.
- Render start/middle/end frames **and** a 12-consecutive-frame action strip at every contact/impact.
- Verify that the same timestamp produces identical frames whether rendered in sequence or out of order.
- Inspect output at phone scale for character silhouettes, captions, safe area, and nonzero actual foreground motion; fix weak scenes.
- Sound effects should be tied to contact/reveal timestamps, not a constant generic track.

## Specific upstream contributions (reviewed November 18, 2026)

- Hanif: `frame(ctx,t)` deterministic animation approach, posed characters, material/detail bible, texture, `sheet` / `strip` / `verify` QA, and audio cue discipline.
- Artem: discrete reusable graphical-animation types, measured frame/safe-area checks.
- Mromidev: emotionally directed shot timing, richer spatial storytelling, animation QA and combined audio.

Do not copy reference frames or claim to have run upstream code before the upstream dependency has been installed and tested. All previews in this package use the custom Python backend only.
