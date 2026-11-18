#!/usr/bin/env python3
"""Dependency check without installing anything."""
import shutil, sys, importlib.util, subprocess
print('Python', sys.version.split()[0])
for pkg in ['PIL','cairosvg','numpy','soundfile','cv2','kokoro_onnx']:
    print(f'{pkg:14}', 'OK' if importlib.util.find_spec(pkg) else 'MISSING' + (' (optional)' if pkg=='kokoro_onnx' else ''))
for app in ['ffmpeg','ffprobe']:
    path=shutil.which(app)
    print(f'{app:14}', path or 'MISSING')
    if path:
        r=subprocess.run([path,'-version'],capture_output=True,text=True)
        print(' '*15,(r.stdout or r.stderr).splitlines()[0][:75])
