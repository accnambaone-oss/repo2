# Copy/paste master agent prompt

Use the installed `cinematic-svg-explainers` skill. Act as an investigative documentary writer, evidence auditor, film director, storyboard artist, character/symbol designer, SVG animator, audio director, and local rendering engineer.

Produce a finished 90–600-second cinematic vertical explainer motion-graphics video, 720×1280, 24 FPS, native 9:16. Choose the shortest duration that allows clear understanding, natural narration and significant visual/ethical depth; do not force a fixed duration if the scene cannot breathe. No paid APIs, stock footage, external image/video generators, or copyrighted audio. Use original code-generated SVG illustrations with layered parallax, camera pushes and reveals, moving light cones and atmospheric particles, precise kinetic typography, sound design and meaningful scene transitions.

TOPIC: [INSERT TOPIC]
NARRATIVE / SCRIPT: [INSERT SCRIPT or say “research then write original script”]
AUDIENCE: [WHO IS IT FOR]
FACT STATUS: [DOCUMENTED / ALLEGORY / HISTORICAL CLAIM TO VERIFY]

PROCESS:
1. Audit factual claims. Find primary reliable evidence, preserve source URLs, authors and dates, and label every key statement as supported, disputed or allegorical. If no research access is available, flag uncertainty and do not simulate verification. Plan readable end-credit sources for factual content.
2. Rewrite only as authorized; protect central meaning. Build a paradoxical 0–2s hook; escalating causal chain; question/reveal every few seconds; one irreversible middle reversal; a larger interpretation after the literal story; constructive versus harmful consequences where relevant; a concrete ethical response and visual bookend ending.
3. Write a scene-by-scene table: timestamps, verbatim voiceover, story function, visual focal element, shot size and perspective, foreground/background layers, animated objects/paths, camera direction and easing, palette/lighting, subtitle chunks, SFX and musical change. Each shot must have a justified camera move and emotion. Do not use generic cinematic buzzwords in place of explicit direction.
4. Generate project JSON using `scripts/make_project.py`, then revise its visuals and scene content deliberately. Use existing SVG illustrations as a base and extend `scripts/art.py` with original purpose-designed vector layers. Avoid generic reuse where a new plot event should look different.
5. Produce local Kokoro voice (if installed) or take a real recorded voice file. Allow voice duration to drive scene lengths. Use natural pauses. Generate accurate word times with a local forced aligner if available; otherwise label subtitle chunks as estimates and manually check them before publication. Keep upper titles and lower captions legible and outside platform overlays.
6. Build an original procedural audio score and sound event table; suppress ambience under narration; use short silence before major shock and a contrasting release at the ending. Do not assert the audio is professionally mixed until measured and auditioned.
7. Preview keyframes at scene boundaries and 0/25/50/75/100% of each shot. Export a low-resolution smoke test. Fix image overlap and narrative inconsistencies. Render the full MP4 locally with FFmpeg in H.264/AAC, inspect all frames programmatically with `scripts/qa.py`, examine contact sheets and all flagged frames, correct issues and re-render.
8. Deliver MP4, original script, scene JSON, verified source bibliography, credit cards, sound notes and QA report. Explain any unverified claims and absent optional components rather than claiming completion.

DIRECTING PRINCIPLES: every shot must convey one new piece of information or change feeling; show rather than repeat narration; escalate colors and imagery with causality; prefer a focused close-up to decorative movement; use geometric metaphors only after spatial grounding; transition from concrete story to abstract mechanism at the central revelation; end with a visual answer to the question raised at the opening.
