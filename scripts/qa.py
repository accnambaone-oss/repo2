#!/usr/bin/env python3
"""Full-video pixel checks and sample-sheet export. Report flags REQUIRE visual inspection."""
import argparse, json, pathlib, subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont

def analyze(path,out):
    cap=cv2.VideoCapture(str(path));fps=cap.get(cv2.CAP_PROP_FPS);n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if not cap.isOpened() or not fps:raise ValueError('Cannot decode video')
    prev=None;blacks=[];whites=[];frozen=[];pops=[];samples=[];dur=n/fps
    period=max(1,int(n/36));hist={}
    for i in range(n):
        ok,fr=cap.read()
        if not ok:break
        gray=cv2.cvtColor(cv2.resize(fr,(64,114)),cv2.COLOR_BGR2GRAY)
        mean=float(np.mean(gray))
        if mean<7:blacks.append(round(i/fps,2))
        if mean>248:whites.append(round(i/fps,2))
        if prev is not None:
            diff=float(np.mean(cv2.absdiff(prev,gray)))
            if diff<.035:frozen.append(round(i/fps,2))
            if diff>56:pops.append(round(i/fps,2))
        prev=gray
        if i%period==0:
            im=Image.fromarray(cv2.cvtColor(cv2.resize(fr,(180,320)),cv2.COLOR_BGR2RGB));samples.append((i/fps,im))
    cap.release();out.mkdir(parents=True,exist_ok=True)
    cw,ch=180,351;cols=6;rows=(len(samples)+cols-1)//cols
    page=Image.new('RGB',(cols*cw,rows*ch),(18,20,27));d=ImageDraw.Draw(page)
    for j,(t,im) in enumerate(samples):
        x=(j%cols)*cw;y=(j//cols)*ch
        page.paste(im,(x,y+28));d.text((x+8,y+7),f'{t:.1f} s',fill='white')
    page.save(out/'contact_sheet.jpg',quality=90)
    report=dict(video=str(path),width=w,height=h,fps=fps,frames=n,duration_seconds=round(dur,3),
                black_frames=len(blacks),black_times=blacks[:50],white_frames=len(whites),white_times=whites[:50],
                near_identical_consecutive_frames=len(frozen),near_identical_times=frozen[:50],
                abrupt_global_changes=len(pops),abrupt_change_times=pops[:70],
                warning='Detectors are heuristics; intentional cuts/dark backgrounds may be flagged. A passing report does NOT verify narration, content, captions, or facts.')
    (out/'qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2));print('CONTACT SHEET',out/'contact_sheet.jpg')

def main():
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--out',required=True);a=p.parse_args();analyze(pathlib.Path(a.video),pathlib.Path(a.out))
if __name__=='__main__':main()
