# Changelog

## 2.0 — motion/rig and Hanif integration, 2026-11-18
- Corrected failure mode from initial static slideshow-like preview. Now actor-level motion is the default; explicit `--legacy-static` is diagnostic only.
- New original `rigs.py`: 16-phase character gait, independent tail/head/foot motion, facial state, blink and body deformation.
- New active-motion scene demo and 12-consecutive-frame action-strip generator with random-access deterministic checks.
- Fixed alpha compositing for landscape glows: saturated oversized sunrise artifact no longer appears.
- Added Windows/macOS font fallbacks.
- Added upstream installer for original buildwithhanif/claude-animation-skill; Node dependencies installed on request, MIT license copied when downloaded. Original source not mirrored within ZIP.
- Added test coverage for motion and installer (9 tests total).

## 1.0 — baseline
- Story parser, example plan, narration helper, Python art renderer, sound, FFmpeg, contact sheets and static QA.
