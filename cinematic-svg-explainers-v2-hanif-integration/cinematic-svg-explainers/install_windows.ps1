# Run from the extracted folder in a PowerShell session with Python and FFmpeg installed.
$ErrorActionPreference = "Stop"
py -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe scripts\doctor.py
Write-Host "Now copy this entire directory to .claude/skills/cinematic-svg-explainers or .opencode/skills/cinematic-svg-explainers (relative to project)."
Write-Host "Visual draft: .\.venv\Scripts\python.exe scripts\render.py examples\divide_trap.json --out out\test.mp4 --seconds 6 --scale .5"
