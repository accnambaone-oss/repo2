#!/usr/bin/env python3
"""CPU-friendly original animated SVG portrait renderer; uses FFmpeg pipe (no image sequence)."""
import argparse, bisect, io, json, math, os, pathlib, random, subprocess, sys, tempfile
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg
from art import art_svg
from audio import write_bed

COLOR={'red':'#f05260','gold':'#efc16e','blue':'#77c6ea'}

def font_path(bold=False,condensed=False):
    paths=['/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf',
          'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
          '/Library/Fonts/Arial.ttf']
    for p in paths:
        if pathlib.Path(p).exists():return p
    return None

@lru_cache(maxsize=24)
def font(sz,bold=False):
    p=font_path(bold)
    return ImageFont.truetype(p,sz) if p else ImageFont.load_default()

def clamp(a,lo=0,hi=1):return min(hi,max(lo,a))
def smooth(t):
    t=clamp(t);return t*t*(3-2*t)

def validate_story(story):
    scenes=story.get('scenes')
    if not scenes:raise ValueError('No scenes in story')
    if abs(float(scenes[0]['start']))>.001:raise ValueError('First scene must start at 0')
    for i,s in enumerate(scenes):
        if s.get('visual') is None:raise ValueError(f'Missing visual at scene {i}')
        if float(s['end'])<=float(s['start']):raise ValueError(f'Non-positive duration at scene {i}')
        if i and abs(float(s['start'])-float(scenes[i-1]['end']))>.02:
            raise ValueError(f'Gap/overlap between scenes {i-1} and {i}')
    if int(story.get('fps',24))<=0:raise ValueError('FPS must be positive')

def chunks(text,maxwords=5):
    words=text.strip().split()
    if not words:return ['']
    return [' '.join(words[i:i+maxwords]) for i in range(0,len(words),maxwords)]

def title_lines(draw,title,max_width,sz):
    ff=font(sz,False);words=title.upper().split();lines=[];curr=''
    for word in words:
        candidate=(curr+' '+word).strip()
        if curr and draw.textbbox((0,0),candidate,font=ff)[2]>max_width:
            lines.append(curr);curr=word
        else:curr=candidate
    if curr:lines.append(curr)
    return lines[:3]

def center_text(d,y,text,f,fill,width):
    bb=d.textbbox((0,0),text,font=f,stroke_width=0)
    x=(width-(bb[2]-bb[0]))//2
    d.text((x,y),text,fill=fill,font=f)

class Animator:
    def __init__(self,story,w,h):
        self.story=story;self.w=w;self.h=h;self.sx=w/720;self.sy=h/1280
        self.scenes=story['scenes'];self.ends=[float(s['end']) for s in self.scenes]
        self.art_cache={};self.overlay=Image.new('RGBA',(w,h),(0,0,0,0))
        ov=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(ov)
        # Gentle edge shading, fixed: atmospheric depth is kept independent of title layer.
        for i in range(5):
            x=int(w*i/12);y=int(h*i/15)
            alpha=16 if i<5 else 8
            d.rectangle((x,y,w-x,h-y),outline=(0,0,0,alpha),width=max(1,round(11*self.sx)))
        self.overlay=ov
    def asset(self,index):
        if index not in self.art_cache:
            png=cairosvg.svg2png(bytestring=art_svg(self.scenes[index]).encode('utf-8'),output_width=self.w,output_height=self.h)
            self.art_cache[index]=Image.open(io.BytesIO(png)).convert('RGBA')
        return self.art_cache[index]
    def image(self,index,t):
        scene=self.scenes[index];dur=float(scene['end'])-float(scene['start'])
        q=clamp((t-float(scene['start']))/dur)
        source=self.asset(index)
        zoom=1.013+0.053*smooth(q)
        if scene['visual'] in ['chase','conflict']:zoom=1.035+0.063*smooth(q)
        sw=round(self.w*zoom);sh=round(self.h*zoom)
        big=source.resize((sw,sh),Image.Resampling.BILINEAR)
        drift=round((8*math.sin(q*math.pi)*self.sx)*(1 if index%2 else -1))
        x=(self.w-sw)//2+drift;y=(self.h-sh)//2+round(7*q*self.sy)
        canvas=Image.new('RGBA',(self.w,self.h),(6,9,18,255));canvas.alpha_composite(big,(x,y));canvas.alpha_composite(self.overlay)
        return canvas
    def draw_overlay(self,canvas,index,t):
        s=self.scenes[index];local=t-float(s['start']);dur=float(s['end'])-float(s['start']);q=clamp(local/dur)
        d=ImageDraw.Draw(canvas,'RGBA');acc=COLOR.get(s.get('accent','gold'),COLOR['gold'])
        accent=(240,74,85,255) if s.get('accent')=='red' else (246,197,108,255)
        # Deterministic floating spores: brief simulated physical atmosphere.
        seed=153+index*74
        rng=random.Random(seed)
        for i in range(33):
            x=rng.randrange(self.w);y0=rng.randrange(self.h)
            phase=rng.random()*6.28;r=1+int(rng.random()*2.4*self.sx)
            y=int((y0-17*t+4*math.sin(t*.7+phase))%self.h)
            a=80 if i%4 else 120
            d.ellipse((x-r,y-r,x+r,y+r),fill=(240,177,85,a if s.get('accent')=='gold' else 70))
        # Header blocks, with purposeful breathing room, cut-in ease and emphasis.
        top=round(125*self.sy);reveal=smooth(min(local/.4,1))*smooth(min((dur-local)/.3,1))
        ttl=str(s.get('title','')).upper();header_size=round((46 if len(ttl)<25 else 37 if len(ttl)<40 else 30)*self.sy)
        lines=title_lines(d,ttl,round(self.w*.86),header_size)
        if len(lines)>1 and len(lines[-1])<4: header_size=max(22,header_size-3)
        badge_h=round((95+max(0,len(lines)-1)*43)*self.sy)
        left=int(self.w*.07);right=int(self.w*.93)
        d.rounded_rectangle((left,top,right,top+badge_h),radius=round(13*self.sx),fill=(3,5,12,round(194*reveal)))
        for j,line in enumerate(lines):
            center_text(d,top+round((10+j*44)*self.sy),line,font(header_size),(*((241,240,233)),round(255*reveal)),self.w)
        if s.get('eyebrow'):
            eb=str(s['eyebrow']).upper()
            if len(eb)>38:eb=eb[:37]+'…'
            center_text(d,top+round((23+len(lines)*47)*self.sy),eb,font(round(18*self.sy),True),(*accent[:3],round(235*reveal)),self.w)
        d.rounded_rectangle((round(240*self.sx),top+badge_h-3,round(480*self.sx),top+badge_h),radius=1,fill=(*accent[:3],round(220*reveal)))
        # Controlled language rhythm: estimated chunks, not a forced aligner.
        segs=s.get('caption_chunks') or chunks(s.get('narration',''),5)
        if segs:
            k=min(len(segs)-1,int(clamp(q,0,.99999)*len(segs)))
            line=str(segs[k]);max_chars=55
            if len(line)>max_chars:line=line[:max_chars-1]+'…'
            f=font(round(26*self.sy),True)
            bb=d.textbbox((0,0),line,font=f);tw=bb[2]-bb[0]
            pad=round(17*self.sx);cx=self.w//2;cy=round(1011*self.sy)
            d.rounded_rectangle((max(10,cx-tw//2-pad),cy-12,min(self.w-10,cx+tw//2+pad),cy+round(50*self.sy)),radius=round(10*self.sx),fill=(3,7,17,220),outline=(*accent[:3],170),width=max(1,round(self.sx)))
            center_text(d,cy,line,f,(247,245,235,255),self.w)
        # Progress keyline discreetly tracks total movie (no accidental TikTok UI mimic).
        total=self.ends[-1]
        d.rectangle((0,self.h-round(7*self.sy),round(self.w*clamp(t/total)),self.h),fill=(*accent[:3],200))
        return canvas
    def frame(self,t):
        i=min(len(self.scenes)-1,bisect.bisect_right(self.ends,t))
        frame=self.image(i,t)
        # Short motivated transition on shot change. Cross-dissolve from preceding card.
        border=float(self.scenes[i]['start'])
        if i>0 and 0<=t-border<.15:
            prev=self.image(i-1,max(0,border-.015))
            frame=Image.blend(prev,frame,smooth((t-border)/.15))
        frame=self.draw_overlay(frame,i,t)
        return frame.convert('RGB')

# Production renderer: actor-level motion; the previous flattened-SVG renderer is
# kept only for diagnostics and is NOT the default.
LegacyStaticAnimator = Animator
from motion_engine import MotionDirector
class Animator:
    def __init__(self,story,w,h):
        self.story=story
        self.ends=[float(s['end']) for s in story['scenes']]
        self.director=MotionDirector(story,w,h)
    def frame(self,t):
        i=min(len(self.ends)-1,bisect.bisect_right(self.ends,t))
        return self.director.frame(i,t)

def render(args):
    p=pathlib.Path(args.story)
    story=json.loads(p.read_text(encoding='utf-8'));validate_story(story)
    scale=float(args.scale)
    if not (.15<=scale<=2):raise ValueError('--scale must be within .15 to 2')
    w=round(int(story.get('width',720))*scale/2)*2;h=round(int(story.get('height',1280))*scale/2)*2
    fps=int(story.get('fps',24));full_end=float(story['scenes'][-1]['end'])
    start=float(args.start);duration=min(full_end-start,float(args.seconds) if args.seconds is not None else full_end-start)
    if start<0 or duration<=0:raise ValueError('Invalid video range')
    frame_count=int(round(duration*fps));anim=LegacyStaticAnimator(story,w,h) if args.legacy_static else Animator(story,w,h)
    out=pathlib.Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='svg_motion_') as td:
        bed=pathlib.Path(td)/'bed.wav'
        write_bed(bed,full_end,story['scenes'])
        # Input order: 0 raw rgb pipe, 1 bed, 2 optional voice.
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y', '-f','rawvideo','-pixel_format','rgb24',
             '-video_size',f'{w}x{h}','-framerate',str(fps),'-i','pipe:0',
             '-ss',str(start),'-t',str(duration),'-i',str(bed)]
        if args.audio:
            if not pathlib.Path(args.audio).exists():raise FileNotFoundError(args.audio)
            cmd += ['-ss',str(start),'-t',str(duration),'-i',args.audio,
                    '-filter_complex','[1:a]volume=0.64[bg];[2:a]volume=1.0[vo];[bg][vo]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94[mix]',
                    '-map','0:v:0','-map','[mix]']
        else:cmd+=['-map','0:v:0','-map','1:a:0']
        cmd+=['-c:v','libx264','-pix_fmt','yuv420p','-preset',args.preset,'-crf',str(args.crf),
              '-c:a','aac','-b:a','160k','-ar','44100','-movflags','+faststart','-t',str(duration),str(out)]
        print(f'Rendering {frame_count} frames {w}x{h}@{fps} to {out}',flush=True)
        if not args.audio:print('NOTICE: no voice supplied; render has SFX/ambience only.',flush=True)
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for k in range(frame_count):
                frame=anim.frame(start+k/fps)
                proc.stdin.write(frame.tobytes())
                if k and k%max(fps*5,1)==0:print(f' {k}/{frame_count} frames',flush=True)
            proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace');return_code=proc.wait()
            if return_code:raise RuntimeError('FFmpeg failed: '+err[-2000:])
        except Exception:
            if proc.poll() is None:proc.kill()
            raise
        print('Exported',out,'bytes:',out.stat().st_size,flush=True)

def main():
    ap=argparse.ArgumentParser(description='Code-rendered SVG documentary')
    ap.add_argument('story');ap.add_argument('--out',required=True);ap.add_argument('--audio')
    ap.add_argument('--start',type=float,default=0);ap.add_argument('--seconds',type=float);ap.add_argument('--scale',type=float,default=1)
    ap.add_argument('--preset',default='veryfast',choices=['ultrafast','superfast','veryfast','faster','fast','medium','slow'])
    ap.add_argument('--crf',type=int,default=19);ap.add_argument('--legacy-static',action='store_true',help='Old flattened-scene renderer; not recommended');render(ap.parse_args())
if __name__=='__main__':main()
