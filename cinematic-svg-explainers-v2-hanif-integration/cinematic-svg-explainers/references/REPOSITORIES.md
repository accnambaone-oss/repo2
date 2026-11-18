# Comparison of the requested GitHub repositories

Reviewed publicly available main branch READMEs and mromidev `SKILL.md` on Nov 18, 2026. These repositories were **not copied** into this ZIP (no direct Git network access in the build container); this is an independently authored skill.

**artemnovitckii/claude-animation-skills**
https://github.com/artemnovitckii/claude-animation-skills

The README currently advertises eleven skills: 3D cartoon (`zach-d-films` / `zach-3d-films`), stick figures, minimalist graphics, map route, breakdown, graph, low-poly, Minecraft, Kurzgesagt-style space, Dan Koe-style line art and others. Example-first workflows use simple specs, local rendering (three.js + kit/HyperFrames and/or FFmpeg; depending on skill), voice/timings for selected long skills, contact sheets and safe-area checks. Strong takeaway: narrowly scoped reusable motion patterns, installation discipline and predictable artifact tests. It does **not** by itself make a 90-600-second dark narrated documentary with fact-checking and custom layered well imagery.

**mromidev/claude-animated-shorts**
https://github.com/mromidev/claude-animated-shorts

The README and SKILL.md describe ~55-70 s story shorts with 2D billboard characters in 3D illustrated towns, three.js inside Remotion, word-timed narration, composed sound, detailed camera/movement and multi-round still-frame QA. Includes reference style reports, a bridge example, scene machinery, and audio scripts. Strong takeaway: shot table + camera ownership, voice-first timing, staged QA, renderer packaging, visual comparison, final sound mix. This project specifically specifies **no captions or labels**, while the uploaded user video prominently has bold headings and highlighted subtitles: this is a key mismatch. It also has heavier GPU/Chromium/Remotion demands than a light SVG workflow.

**Our original custom skill**

Targets the actual uploaded video more closely: 2D silhouette/vector art + pseudo-depth parallax, chronological catastrophe → emotional reversal → hierarchy/chess metaphor → positive final exit, amber/red palette, built-in typographic system, highlighted sentence-chunk captions, no web APIs, FFmpeg CPU renderer, 90-600 s adaptation, optional Kokoro ONNX voice, QA and source framework. It prioritizes practical compatibility with a weaker laptop and Windows.

**Important difference**: Neither of those projects alone is the packaged contents of this ZIP. No license is claimed over their assets/code; links are attribution for *approach* only. Their future versions may differ. If users install them separately, keep separate skill names and dependencies.

**buildwithhanif/claude-animation-skill (newly requested; MIT)**
https://github.com/buildwithhanif/claude-animation-skill

Real JavaScript/Node Canvas animated drawing with textured surfaces, anatomy-aware characters, a film harness (`sheet`, `strip`, `verify`, `render`), deterministic seeded texture, motivated acting and audio cues. Its `SKILL.md` lives under `plugins/claude-animation/skills/claude-animation/` and requires Node 20+, `@napi-rs/canvas`, FFmpeg. This additional upstream is provided through `scripts/install_upstream_skills.py` and integrated via `integrations/HANIF_ANIMATION.md`; its original source is NOT embedded in the ZIP. The Python backend now implements original articulated rat poses, motion-specific scene design, deterministic action-strip QA and properly composited backgrounds. Avoid equating the original author\'s sophisticated hand-painted examples with the Python motion-demo artwork.
