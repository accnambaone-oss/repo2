"""Procedural, royalty-free synthesized ambience / cue track."""
import numpy as np, soundfile as sf

def make_bed(seconds, scenes, sr=24000):
    n=max(1,int(round(seconds*sr)));t=np.arange(n,dtype=np.float32)/sr
    base=.012*np.sin(2*np.pi*55*t)+.008*np.sin(2*np.pi*82.41*t)
    base*=.65+.35*np.sin(2*np.pi*.075*t)**2
    # Deterministic low rumble: integrated noise filtered by box smoother.
    rng=np.random.default_rng(522);noise=rng.normal(0,1,n).astype(np.float32)
    h=np.ones(129,dtype=np.float32)/129
    filt=np.convolve(noise,h,mode='same')
    out=base+.028*filt
    for s in scenes:
        at=int(float(s['start'])*sr)
        if at>=n:continue
        d=min(int(.65*sr),n-at);u=np.arange(d,dtype=np.float32)/sr
        amp=.09 if s.get('accent')=='red' else .054
        hit=amp*np.exp(-9*u)*np.sin(2*np.pi*(91*u+32*u*u))
        out[at:at+d]+=hit
    # Fade in/out to avoid jumps.
    fade=min(int(sr*.3),n//2)
    if fade:out[:fade]*=np.linspace(0,1,fade);out[-fade:]*=np.linspace(1,0,fade)
    return np.clip(out,-.85,.85).astype(np.float32)

def write_bed(path,seconds,scenes):
    sf.write(str(path),make_bed(seconds,scenes),24000)

if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('story');p.add_argument('--out',default='bed.wav');a=p.parse_args()
    story=json.load(open(a.story));write_bed(a.out,story['scenes'][-1]['end'],story['scenes']);print(a.out)
