#!/usr/bin/env python3
"""Local Kokoro TTS; synthesize each narration scene and retime project to true clip lengths.

Important: subtitle word positions remain estimated; use a forced aligner for accurate karaoke text.
"""
import argparse, json, pathlib, numpy as np, soundfile as sf

def make_voice(args):
    try:from kokoro_onnx import Kokoro
    except ImportError as e:raise SystemExit('Install optional local Kokoro: pip install kokoro-onnx soundfile') from e
    for path in [args.model,args.voices]:
        if not pathlib.Path(path).exists():raise FileNotFoundError('Missing Kokoro model file: '+path)
    story=json.loads(pathlib.Path(args.story).read_text(encoding='utf-8'))
    tts=Kokoro(args.model,args.voices);segments=[];sr=None
    for i,scene in enumerate(story['scenes']):
        narr=scene.get('narration','').strip()
        if narr:
            samples,rate=tts.create(narr,voice=args.voice,speed=args.speed,lang=args.lang)
            clip=np.asarray(samples,dtype=np.float32).reshape(-1)
        else:rate=24000;clip=np.zeros(int(rate*.20),dtype=np.float32)
        if sr is None:sr=rate
        if rate!=sr:raise RuntimeError('TTS returned inconsistent sample rates')
        segments.append(clip)
        print(f'{i+1}/{len(story["scenes"])} {len(clip)/sr:.2f}s: {narr[:48]}',flush=True)
    gap=max(0.0,args.pause);all_samples=[];t=0.0
    for scene,clip in zip(story['scenes'],segments):
        scene['start']=round(t,4)
        dur=len(clip)/sr+gap
        t+=dur;scene['end']=round(t,4)
        all_samples.append(clip)
        if gap:all_samples.append(np.zeros(int(round(gap*sr)),dtype=np.float32))
    combined=np.concatenate(all_samples) if all_samples else np.array([],dtype=np.float32)
    target=pathlib.Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    sf.write(str(target),combined,sr)
    story['narration_status']='kokoro_tts_generated_scene_synced_not_forced_aligned'
    story['duration_notice']='Video length follows synthesized narration rather than nominal target.'
    synced=pathlib.Path(args.synced_story);synced.parent.mkdir(parents=True,exist_ok=True)
    synced.write_text(json.dumps(story,indent=2),encoding='utf-8')
    print('Wrote',target,round(len(combined)/sr,2),'seconds; synchronized story',synced)

def main():
    p=argparse.ArgumentParser();p.add_argument('story');p.add_argument('--model',required=True);p.add_argument('--voices',required=True)
    p.add_argument('--voice',default='af_sarah');p.add_argument('--speed',type=float,default=1.0);p.add_argument('--lang',default='en-us')
    p.add_argument('--pause',type=float,default=.30);p.add_argument('--output',required=True);p.add_argument('--synced-story',required=True)
    make_voice(p.parse_args())
if __name__=='__main__':main()
