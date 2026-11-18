#!/usr/bin/env python3
"""Process every decoded frame of a reference MP4, emit objective metrics & 1s contact sheets."""
import argparse,csv,pathlib,cv2,numpy as np
from PIL import Image,ImageDraw

def main():
    ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--out',required=True);a=ap.parse_args()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(a.video)
    if not cap.isOpened():raise FileNotFoundError(a.video)
    fps=cap.get(cv2.CAP_PROP_FPS);n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev=None;samples=[];peaks=[]
    with (out/'frame_metrics.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['frame','seconds','mean_luma_0_255','mean_b','mean_g','mean_r','mean_change_0_255','potential_change_peak'])
        for i in range(n):
            ok,frame=cap.read()
            if not ok:break
            sm=cv2.resize(frame,(64,114));g=cv2.cvtColor(sm,cv2.COLOR_BGR2GRAY)
            change=float(np.abs(g.astype('float32')-prev.astype('float32')).mean()) if prev is not None else 0
            peak=change>16
            if peak:peaks.append((round(i/fps,3),round(change,2)))
            w.writerow([i,round(i/fps,5),round(float(g.mean()),2),*map(lambda z:round(float(z),2),sm.mean(axis=(0,1))),round(change,3),int(peak)])
            prev=g
            if i%max(1,int(round(fps)))==0:
                img=Image.fromarray(cv2.cvtColor(cv2.resize(frame,(220,391)),cv2.COLOR_BGR2RGB));samples.append((i/fps,img))
    cap.release()
    for page in range(0,len(samples),10):
        group=samples[page:page+10];sheet=Image.new('RGB',(5*220,2*425),(12,14,20));d=ImageDraw.Draw(sheet)
        for j,(t,im) in enumerate(group):
            x=(j%5)*220;y=(j//5)*425
            sheet.paste(im,(x,y+31));d.text((x+8,y+6),f'{t:.1f} s',fill='white')
        sheet.save(out/f'contact_{page//10:02d}.jpg',quality=88)
    print('Frames:',i+1,'Duration:',round((i+1)/fps,3),'High frame-difference timestamps (not necessarily cuts):',peaks[:50])
if __name__=='__main__':main()
