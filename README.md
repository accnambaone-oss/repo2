# Cinematic SVG Explainers

A portable Agent Skill plus runnable, original Python/CairoSVG/FFmpeg motion-graphics engine. Makes native portrait investigative video from a JSON shot plan. No paid APIs, cloud generation, or third-party footage.

**What is actually implemented**: moving SVG-derived layered compositions, title/caption timing, parallax and push-in, vignettes and particles, per-scene visuals, timeline transitions, original procedural music/SFX, FFmpeg MP4 export, optional voice mux, optional local Kokoro synthesis, contact sheets, black/frozen/pop-frame checks, and adaptive-script planning. **What is not automated**: credible online research, creative film direction, perfect word-level forced alignment, human editorial QA, or guaranteed full render speed on weak hardware. The included visual engine is a configurable starting point, not a fully automated replacement for professional animation.

For a copy-and-run agent instruction prompt see `references/MASTER_PROMPT.md`.

## Installation

Python 3.10+, FFmpeg on PATH, suitable fonts, and enough free storage. On Windows install FFmpeg (e.g. `winget install Gyan.FFmpeg`) and Python, then open PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/doctor.py
```

Linux/macOS: `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`, install FFmpeg via OS package manager.

For Claude Code skill discovery extract the folder so `~/.claude/skills/cinematic-svg-explainers/SKILL.md` exists. For OpenCode use `<project>/.opencode/skills/cinematic-svg-explainers/SKILL.md` or global `~/.config/opencode/skills/cinematic-svg-explainers/SKILL.md`. To use command-line scripts, `cd` to the installed skill directory; no external plugin needed.

## Visual draft / test

```bash
python scripts/render.py examples/divide_trap.json --out out/preview.mp4 --start 0 --seconds 6 --scale .5
python scripts/qa.py out/preview.mp4 --out out/qa_preview
```

## Full 90-second EXAMPLE (no TTS installed)

```bash
python scripts/render.py examples/divide_trap.json --out out/divide_trap_instrumental.mp4
python scripts/qa.py out/divide_trap_instrumental.mp4 --out out/qa
```

This render includes original instrumental texture/SFX, **but no spoken narration**. It is a preview, not the complete VO version.

## Full example WITH local Kokoro

```bash
pip install kokoro-onnx soundfile
# Download kokoro-v1.0.onnx and voices-v1.0.bin from the official Kokoro ONNX release.
python scripts/voice.py examples/divide_trap.json --model models/kokoro-v1.0.onnx --voices models/voices-v1.0.bin --output out/voice.wav --synced-story out/synced.json
python scripts/render.py out/synced.json --out out/divide_trap_narrated.mp4 --audio out/voice.wav
python scripts/qa.py out/divide_trap_narrated.mp4 --out out/qa_narrated
```

**Voice length governs the end time** after synchronization. Because per-scene TTS duration differs from word-count projections, the narrated runtime may not be exactly 90 s. Change scene prose/pacing and regenerate if required. Interpolated subtitle chunks are not yet word-perfect; force align or correct manually.

## Generate a NEW short from a script

```bash
python scripts/make_project.py --script examples/divide_trap.txt --out out/my_story --duration auto
# Edit out/my_story/story.json: set custom visuals, titles, narrative reveals, scene durations, palette.
python scripts/render.py out/my_story/story.json --out out/my_story/draft.mp4 --scale .5
```

`--duration auto` infers length from an approximate 150 WPM (clamped to 90-600 s); `--duration 180` sets requested duration. It gives a first-pass plan, not finished directing.

## Limitations and operational notes

- Renderer is CPU-oriented and streams raw frames to FFmpeg without storing all frames; at 720x1280 long films still take computation and disk space. Test `--scale .5` first on an older laptop; choose full scale only for final.
- Video frame timing is deterministic. Audio is synthesized at 24 kHz, exported AAC in final MP4. FFmpeg provides faststart H.264 encoding. Subtitle timing before forced alignment is **estimated**.
- Original example adapts a *supplied fictional rat-well parable*; not research evidence for real rodent training or pest control. Do not present it as a documented event.
- External image/video APIs are never used. Optional Kokoro model files must be acquired once by the user; they are not bundled here and dependencies may require an internet connection to install.
- Cite verified third-party claims in footage and project research log. Never fake credits.
- Original code is under MIT (see LICENSE). No code, binaries, reference imagery, or datasets were copied from the linked repositories.

## V2 — articulated animation and actual upstream Hanif skill

The first preview failed because it used one flattened illustration per scene and a slow camera push. The default renderer is now `scripts/motion_engine.py` with **independently moving subjects** (falling pig trajectory, staggered falling rats, breathing/squash, articulated rat gait, swarms, fleeing/chasing, rising rope, drawing hierarchy connectors, advancing staircase and typed text reveals). `scripts/rigs.py` has a new original frame-exact 16-pose rat rig. The overly saturated glow from incorrect alpha blending has been corrected.

Try the stronger motion comparison before committing to a full reel:

```powershell
python scripts/render.py examples/active_motion_demo.json --out out/active_demo.mp4 --scale .5
python scripts/action_strip.py examples/active_motion_demo.json --at 8.0 --frames 12 --out out/chase_strip.jpg
```

The QA strip compares every 1/24-second frame and verifies deterministic random-access output. The still preview is a technical motion demo, **not a fully polished imitation of the supplied film**. It has generated instrumental cues only; supply Kokoro/recorded audio for a narrated deliverable. Runtime remains CPU-sensitive at 720p.

**Important — original upstream skill:** This ZIP provides the Hanif integration and an original upstream installer, **not a pre-bundled mirror of Hanif's GitHub source**. Install the actual MIT-licensed JS skill (Node 20+ and npm required, in addition to FFmpeg):

```powershell
# Run from this folder inside a project; GitHub access required once.
py scripts/install_upstream_skills.py --target .opencode/skills --npm
# Or use --target .claude/skills for Claude Code.
```

Offline mode using a manually obtained GitHub checkout:

```powershell
py scripts/install_upstream_skills.py --from-directory "C:\Users\You\Downloads\claude-animation-skill-main" --target .opencode/skills --npm
```

Read [integrations/HANIF_ANIMATION.md](integrations/HANIF_ANIMATION.md) for what is integrated and what remains a separate renderer. The original Hanif Node Canvas `film.mjs` is the preferred path for hand-drawn/watercolour characters; the independent Python renderer is lightweight SVG motion graphics. Neither one is a one-click guarantee of production-quality work without shot design, timing, and QA.
