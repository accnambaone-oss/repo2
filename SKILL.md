---
name: cinematic-svg-explainers
description: Produce evidence-aware, emotionally paced vertical investigative motion-graphic films (90-600 s) entirely with locally generated SVG illustrations, layered parallax, kinetic typography, Kokoro narration, procedural SFX, subtitles, FFmpeg, and frame-by-frame QA. Use when asked for dark explainer reels, narrated allegories, symbolic documentaries, or code-rendered shorts without paid image/video APIs.
---

# Cinematic SVG Explainers — a production skill

You are the director, researcher, screenwriter, storyboard artist, sound editor, motion designer, and final technical reviewer. Your responsibility is a finished video, NOT just a suggested prompt. Every shot must advance meaning or emotion, every transition must be motivated, and the render must pass QA. This skill is original; see `references/REPOSITORIES.md` for comparative inspirations.

## Mandatory: install and USE the Hanif animation skill for drawn character work

This bundle includes a first-class **upstream installer and editorial integration**, not a copied upstream source tree. Read `integrations/HANIF_ANIMATION.md`. Online installation: `python scripts/install_upstream_skills.py --target .claude/skills --npm` (or `.opencode/skills`). Then read **the original** `claude-animation/SKILL.md`, its character + detail references, and use its real `film.mjs` harness whenever hand-drawn animation is the output. `@napi-rs/canvas`, Node 20+, FFmpeg are free local runtime prerequisites. Do not claim the Hanif renderer ran if it was not installed.

For the lightweight Python backend, use **actor-level** motion via `scripts/motion_engine.py` and independently articulated rat character from `scripts/rigs.py` (16 gait poses, ear/eye, head, feet, tail). Never use `--legacy-static` as a deliverable. Generate the action strip: `python scripts/action_strip.py examples/divide_trap.json --at 5 --out out/swarm_strip.jpg`. It checks random-access frame determinism. When a scene reads as a static poster, rewrite it with keyframed actors and pose changes.

## Start here

1. Read `README.md`, `references/DIRECTING.md`, `references/FACT_CHECK.md`, and `analysis/REFERENCE_BREAKDOWN.md` when replicating the uploaded sample's language.
2. Decide if the material is an **allegory**, a **verified real story**, or an **unverified claim**. Do not invent source citations or present an allegory as proven behavioral science. Research externally where the environment allows; log every factual claim with title, author, URL, publication date, access date, exact supporting sentence, and confidence. If offline, clearly mark verification pending.
3. Rewrite or use supplied script, preserving its intent. Design a hook in 0-2 seconds, escalating discoveries, a major reinterpretation at ~2/3, constructive AND destructive applications if relevant, and a surprising practical payoff. Choose 90-600 s *adaptively* rather than padding. No repetitive filler. Keep voice around 135-175 spoken words/minute, adjusting for emotion and pauses. Script length and actual generated audio govern the final duration.
4. Build shot plan: every shot has start/end, narrative purpose, protagonist/prop focus, scale, angle/perspective, foreground/background depth, motion curve, palette, narration, title, visual metaphor, transition, sound cue, expected reveal and next hook. Prefer 2-7 s shot groups; a visual scene may contain several micro-beats.
5. Run `python scripts/doctor.py`. Create a project with `python scripts/make_project.py --script examples/divide_trap.txt --out work/divide-trap --duration 90` (or `--duration auto`). Inspect/edit `work/divide-trap/story.json`. For the hand-authored example, render `examples/divide_trap.json` directly.
6. Voice: OPTIONAL for a visual draft; REQUIRED for deliverable with narration. Install `pip install kokoro-onnx soundfile`, obtain legal Kokoro v1 ONNX models yourself, then `python scripts/voice.py examples/divide_trap.json --model models/kokoro-v1.0.onnx --voices models/voices-v1.0.bin --output work/voice.wav --synced-story work/synced.json`. This uses actual per-scene TTS durations; it does not claim word-accurate alignment. For word accuracy, use a forced-aligner and audit manually; do not label interpolated timing as forced alignment. If `voice.py` unavailable, supply your recorded `voice.wav` and hand-adjust the shot plan.
7. Render sample keyframes or short range FIRST: `python scripts/render.py examples/divide_trap.json --out work/sample.mp4 --start 0 --seconds 6 --scale .5`. Inspect for composition/safe areas and artifacts. Then full: `python scripts/render.py work/synced.json --out work/final.mp4 --audio work/voice.wav`. Where audio not supplied, it renders an instrumental/sfx track; label it **no narration**.
8. Run `python scripts/qa.py work/final.mp4 --out work/qa`. Examine contact sheet AND full-frame outliers. Fix composition, clipping, unreadable labels, punctuation, low contrast, accidental text overlaps, gaps or audio spikes. Re-render until resolved. Do not claim a render passed if it did not.
9. Export `final.mp4`, `story.json`, script, research log, contact sheet, sound notes, and citations/end-credit frames for verified claims. A source bibliography in the project alone is not enough if user requested end credits; make final scenes with readable sources.

## Required style / editing rules

- Vertical native 720x1280, 24 fps by default. Do not crop horizontal video into portrait. Keep 120 px top and 190 px bottom as caution zones for social UI; keep primary captions ~950-1060 px in the 1280-px canvas; inspect final platform.
- Visual grammar: layered vector silhouettes + real animating properties, purpose-built compositions, color as narrative meaning, contrasting scales, moving light cones, dust, vignette, reveal cuts, diagram and icon transformations, camera pushes 1-7%, punch cuts only on big semantic changes, restrained but meaningful motion during holds.
- Underlying engine: original Python + CairoSVG/Pillow + FFmpeg (`scripts/render.py`); no Three.js, Remotion, paid API or web service required to render. If a project already has Remotion, it may be used as a separate advanced renderer without copying third-party code.
- Timing: if voice exists, audio-first. Confirm each sentence's audible entrance/exit against the picture, and cut on semantic words. Do not automatically slow or speed voice aggressively to force a 90-second limit.
- Subtitles: max 2 lines, 3-7 words per chunk, high contrast, emphasis on exactly one or two meaningful words; never overload with titles and captions competing for attention. Template's captions are **estimated** in-scene; audit/fix for publication or replace timing with verified forced alignment.
- Sound: voice front-and-center, music/ambience lower, transients controlled, no copyrighted samples. Film silence is an intentional design tool. Use the built-in synthesizer, but improve its motif and mix for production.
- Avoid generically "cinematic, 8K, ultra quality" prompts as shot directions; instead specify exact visual cause/effect and reveal.
- Do not disclose an unverified parable as an actual pest-control method. User's rat story depicts biologically unsupported training claims; label a narrative allegory unless sourced.

## Project schema

`story.json` has `width`, `height`, `fps`, optional `tone`, `scenes` with `id`, `start`, `end`, `visual`, `title`, `eyebrow`, `narration`, `accent`, optionally `caption_chunks` and `reveal`. The renderer requires scenes contiguous starting at 0, and supports visuals `well`, `swarm`, `feeding`, `climb`, `calendar`, `conflict`, `countdown`, `predator`, `rope`, `field`, `chase`, `diagram`, `chess`, `escape`, `title`. Additional scene types require adding vector symbol drawings in `scripts/art.py`; don't silently turn every scene into a generic title card.

## Production checklist / stop criteria

- [ ] Narrative claims classified and major facts verified; source/caveat cards when needed
- [ ] Hook and frame-1 visual question, tension change every ~3-8 s, end payoff
- [ ] Exact continuity: rat count only *illustrative*; no false chart-like numbers
- [ ] Narration actually generated or provided and checked; no fake placeholder TTS
- [ ] Frames rendered, representative contact sheet inspected, QA report produced
- [ ] Audio level, text safe area, readability, and 90-600 s target checked
- [ ] Final paths/commands are accurate; report partial failures honestly

## QA evidence threshold

Do not label a video as completed professional motion graphics if subjects do not move to express the described action, if captions outpace narration, or if the only motion is a Ken Burns zoom. The supplied 2026 first preview failed that threshold. Treat improved Python previews as technical proofs of articulated movement, not as a fully matched commercial aesthetic. One more **Hanif JS rendering** pass is recommended for premium hand-drawn shots.

## Files

- `README.md` — install/quickstart and platform paths
- `scripts/make_project.py` — adaptive plan from script
- `scripts/art.py` — original SVG illustration engine
- `scripts/rigs.py` — actual multi-joint animated 2D rat poses
- `scripts/motion_engine.py` — actor-by-actor kinetic engine
- `scripts/action_strip.py` — 12-frame action-strip verification
- `scripts/install_upstream_skills.py` — GitHub/or offline installation of original Hanif animation skill
- `integrations/HANIF_ANIMATION.md` — exact Hanif installation and directing workflow
- `scripts/render.py` — animated, composited local MP4 renderer
- `scripts/voice.py` — optional Kokoro narration + scene-duration sync
- `scripts/audio.py` — synthesized atmosphere + cue track
- `scripts/qa.py` — full-frame signal checks + storyboard contact sheet
- `scripts/doctor.py` — dependency and environment checks
- `examples/divide_trap.json` — hand-directed full sample
- `analysis/REFERENCE_BREAKDOWN.md` — timecoded shot critique from uploaded MP4
- `references/` — research, editorial, creative and repository comparisons
