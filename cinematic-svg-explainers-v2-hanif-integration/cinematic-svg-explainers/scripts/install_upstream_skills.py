#!/usr/bin/env python3
"""Install the original upstream GitHub skills beside this original custom skill.

Ships no mirrored third-party source. Online mode clones the authoritative repository
and copies its installed skill; offline mode reads a user-provided local checkout.
Requires explicit invocation; does not mutate an agent installation by default.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

HANIF_URL='https://github.com/buildwithhanif/claude-animation-skill.git'
HANIF_SUBDIR=Path('plugins/claude-animation/skills/claude-animation')


def locate_skill(checkout: Path) -> Path:
    checkout=Path(checkout)
    nested=checkout/HANIF_SUBDIR
    if (nested/'SKILL.md').exists() and (nested/'lib'/'film.mjs').exists():
        return nested
    if (checkout/'SKILL.md').exists() and (checkout/'lib'/'film.mjs').exists():
        return checkout
    raise FileNotFoundError(f'Cannot locate the original Hanif skill with lib/film.mjs under {checkout}')


def install_from_checkout(checkout: Path, target: Path, force: bool=False) -> Path:
    source=locate_skill(checkout)
    dest=Path(target).expanduser().resolve()/'claude-animation'
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        if not force:
            raise FileExistsError(f'{dest} already exists. Pass --force to replace this upstream skill only.')
        shutil.rmtree(dest)
    shutil.copytree(source,dest,ignore=shutil.ignore_patterns('node_modules','.git','.DS_Store','out'))
    # Original license belongs to root of upstream checkout.
    license_file=Path(checkout)/'LICENSE'
    if license_file.exists() and license_file.resolve()!= (source/'LICENSE').resolve():
        shutil.copy2(license_file,dest/'UPSTREAM_LICENSE')
    (dest/'UPSTREAM_SOURCE.txt').write_text(f'{HANIF_URL}\nOriginal upstream skill installed by script. Check its LICENSE.\n',encoding='utf8')
    return dest


def main():
    p=argparse.ArgumentParser(description='Install original buildwithhanif/claude-animation-skill alongside the local SVG explainer skill.')
    p.add_argument('--target',default='.claude/skills',help='Target skills directory, e.g. .opencode/skills or .claude/skills')
    p.add_argument('--from-directory',type=Path,help='Offline mode: GitHub checkout or extracted folder')
    p.add_argument('--force',action='store_true')
    p.add_argument('--npm',action='store_true',help='Run npm install in installed Hanif skill after copying')
    args=p.parse_args()
    if args.from_directory:
        installed=install_from_checkout(args.from_directory,Path(args.target),args.force)
    else:
        if not shutil.which('git'):
            p.error('Git is missing. Install Git or pass --from-directory with a downloaded checkout.')
        with tempfile.TemporaryDirectory(prefix='hanif_upstream_') as tmp:
            checkout=Path(tmp)/'src'
            subprocess.run(['git','clone','--depth','1',HANIF_URL,str(checkout)],check=True)
            installed=install_from_checkout(checkout,Path(args.target),args.force)
    print('Hanif animation installed:',installed)
    print('Source:',HANIF_URL)
    print('Requires Node 20+, npm, and ffmpeg. Read original SKILL.md before using.')
    if args.npm:
        if not shutil.which('npm'):
            p.error('npm not found. Install Node.js 20+ then run npm install inside the installed skill.')
        subprocess.run(['npm','install'],cwd=installed,check=True)
        print('npm dependencies installed.')

if __name__=='__main__':main()
