#!/usr/bin/env python3
"""Frame-exact visual QA for deterministic local animations.

Produces a still sheet and contact-action strip from the actual programmatic
renderer and tests random-access determinism. This is more useful than testing
whether the FFmpeg exit code is zero.
"""
from __future__ import annotations
import argparse,bisect,hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from render import Animator,validate_story


def analyze(story,scale=.5,at=1.6,frames=12,output=Path('out/action_strip.jpg')):
    validate_story(story)
    w=round(story.get('width',720)*scale/2)*2
    h=round(story.get('height',1280)*scale/2)*2
    fps=story.get('fps',24)
    director=Animator(story,w,h)
    times=[max(0,at+i/fps) for i in range(frames)]
    actual=[director.frame(t) for t in times]
    # Render out of order to catch unintended frame-order dependent random jitter.
    alternate=Animator(story,w,h)
    order=list(range(frames))[::-1]
    reordered={j:hashlib.sha256(alternate.frame(times[j]).tobytes()).hexdigest() for j in order}
    stable=all(hashlib.sha256(actual[j].tobytes()).hexdigest()==reordered[j] for j in range(frames))
    differ=[]
    for a,b in zip(actual,actual[1:]):
        aa=np.asarray(a,dtype=np.int16);bb=np.asarray(b,dtype=np.int16)
        differ.append(round(float(np.mean(np.abs(aa-bb))),5))
    thumbw=round(w*.52);thumbh=round(h*.52)
    cols=min(6,frames);rows=math.ceil(frames/cols)
    sheet=Image.new('RGB',(thumbw*cols,(thumbh+30)*rows),(238,238,238));d=ImageDraw.Draw(sheet)
    for i,im in enumerate(actual):
        x=(i%cols)*thumbw;y=(i//cols)*(thumbh+30)
        sheet.paste(im.resize((thumbw,thumbh)),(x,y+29));d.text((x+8,y+7),f'frame {i:02}  {times[i]:.3f}s',fill=(10,15,25))
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);sheet.save(output,quality=90)
    report={'timestamp':at,'frames':frames,'fps':fps,'deterministic':stable,'mean_frame_abs_difference':differ,'active_frame_pairs':sum(v>.01 for v in differ),'action_strip':str(output)}
    (output.parent/(output.stem+'.json')).write_text(json.dumps(report,indent=2),encoding='utf8')
    return report


def main():
    p=argparse.ArgumentParser();p.add_argument('story');p.add_argument('--at',type=float,default=1.6);p.add_argument('--frames',type=int,default=12);p.add_argument('--scale',type=float,default=.5);p.add_argument('--out',default='out/action_strip.jpg');a=p.parse_args()
    story=json.loads(Path(a.story).read_text(encoding='utf8'))
    report=analyze(story,a.scale,a.at,a.frames,Path(a.out));print(json.dumps(report,indent=2))
    if not report['deterministic']:
        sys.exit('FAILED: same timeline timestamp drew differently out of order')

if __name__=='__main__':main()
