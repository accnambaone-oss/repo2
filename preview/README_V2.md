# Updated kinetic-animation proof (Python backend)

`active_motion_demo_v2.mp4`: 17.2 s at 360×640, 24 fps. Five shots: pig throw, falling swarm, running chase, diagram connectors, animated escape. Procedural audio only (no voiceover). Rendered from `examples/active_motion_demo.json` using `scripts/motion_engine.py`, not Hanif's uninstalled Node runtime.

`swarm_12_frame_action_strip.jpg` and `chase_12_frame_action_strip.jpg`: 12 consecutive frames at 24fps; the corresponding JSON metrics are written by `scripts/action_strip.py`. These represent real independent motion, with deterministic random-access results (tested).

The original `8s_motion_test_360p_instrumental.mp4` is the **rejected static baseline** and should not be presented as the new result.
