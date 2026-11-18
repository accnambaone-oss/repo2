"""Keyframed vector motion graphics: individually animated subjects, NOT static cards.

Each shot has foreground actors, independent trajectories, staged entrances,
animated graphical data/typography, dynamic overlays, and a moving camera.
All original sprite geometry is rendered from SVG once, then transformed per frame.
No paid services and no stock/video assets.
"""
from __future__ import annotations
import io, math, random, os, pathlib
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from art import rat, pig, person
from rigs import rigged_rat_svg

W0,H0=720,1280
INK=(9,12,24,255); GOLD=(240,188,108,255); RED=(242,75,91,255)

def clamp(x, a=0., b=1.): return max(a,min(b,x))
def smooth(x):
    x=clamp(x); return x*x*(3.-2*x)
def ease_out(x):return 1-(1-clamp(x))**3
def sub(q,a,b):return smooth((q-a)/max(.0001,b-a))
def wave(x):return math.sin(x*2*math.pi)
def mix(a,b,t):return a+(b-a)*t

@lru_cache(maxsize=64)
def fnt(size, bold=False):
    options=[os.environ.get('MOTION_FONT_PATH'),
        '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf',
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
        '/Library/Fonts/Arial Bold.ttf' if bold else '/Library/Fonts/Arial.ttf']
    for path in options:
        if path and pathlib.Path(path).exists():
            return ImageFont.truetype(path,max(8,size))
    return ImageFont.load_default(size=max(8,size))

class MotionDirector:
    """Frame compositor with real independent 2D animation.

    New scene types are authored in `actors()` instead of baking an illustration
    to a single flattened SVG. The animated objects are drawn each frame.
    """
    def __init__(self,story,w,h):
        self.story=story;self.w=w;self.h=h;self.scenes=story['scenes'];self.k=w/720
        self.sprite_cache={};self.background_cache={}
        self.bounds={'pig':(-130,-90,280,184),'rat':(-100,-70,191,126),'red_rat':(-100,-70,191,126),'person':(-60,-115,120,175), 'bones':(-120,-50,240,100)}

    def X(self,x):return round(x*self.k)
    def Y(self,y):return round(y*self.h/1280)
    def xy(self,x,y):return self.X(x),self.Y(y)

    def sprite(self,name):
        if name not in self.sprite_cache:
            x,y,bw,bh=self.bounds[name]
            if name=='pig':body=pig(0,0)
            elif name in ('rat','red_rat'):body=rat(0,0,1.,'red' if name=='red_rat' else 'gold')
            elif name=='person':body=person(0,0,1.,'#ecc783','up')
            else:body='''<g fill="none" stroke="#eddfbe" stroke-width="7" stroke-linecap="round">
            <path d="M-76 8 L77 8 M-69 -4v25 M-52 -16v45 M-34 -22v53 M-16 -27v59 M2 -26v56 M20 -23v56 M38 -17v53 M56 -10v43"/>
            <circle cx="83" cy="8" r="19" fill="#ddd2b4" stroke="none"/><path d="M89 8 L107 11"/>
            </g>'''
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh}" viewBox="{x} {y} {bw} {bh}">{body}</svg>'
            raw=cairosvg.svg2png(bytestring=svg.encode(),output_width=max(1,self.X(bw)),output_height=max(1,self.Y(bh)))
            self.sprite_cache[name]=Image.open(io.BytesIO(raw)).convert('RGBA')
        return self.sprite_cache[name]

    @lru_cache(maxsize=96)
    def rigged_rat_image(self,step,mood,blink):
        svg=rigged_rat_svg(step/16,mood,blink)
        raw=cairosvg.svg2png(bytestring=svg.encode(),output_width=max(1,self.X(244)),output_height=max(1,self.Y(156)))
        return Image.open(io.BytesIO(raw)).convert('RGBA')

    def paste_rat(self,c,x,y,sc=.7,angle=0.,alpha=255,flip=False,seconds=0.,mood='neutral',pace=2.8):
        step=int((seconds*pace%1)*16)%16
        blink=(int(seconds*1.6)%23==0 and seconds%1<.10)
        src=self.rigged_rat_image(step,mood,blink)
        self.paste_image(c,src,x,y,sc,angle,alpha,flip)

    def paste_sprite(self,c,name,x,y,sc=1.,angle=0.,alpha=255,flip=False):
        src=self.sprite(name)
        self.paste_image(c,src,x,y,sc,angle,alpha,flip)

    def paste_image(self,c,src,x,y,sc=1.,angle=0.,alpha=255,flip=False):
        if alpha<=0 or sc<=0:return
        sc=max(.025,min(4.,sc))
        destw=max(2,round(src.width*sc));desth=max(2,round(src.height*sc))
        if destw>src.width*8 or desth>src.height*8:return
        img=src.resize((destw,desth),Image.Resampling.BICUBIC) if sc!=1 else src
        if flip:img=img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if abs(angle)>.3:img=img.rotate(angle,Image.Resampling.BICUBIC,expand=True)
        if alpha<254:
            img=img.copy();img.putalpha(img.getchannel('A').point(lambda a:round(a*alpha/255)))
        px,py=self.xy(x,y)
        c.alpha_composite(img,(round(px-img.width*.50),round(py-img.height*.50))) if self._inside(px,py,img) else self._clip_paste(c,img,px,py)

    def _inside(self,px,py,img):return px-img.width*.5>=0 and py-img.height*.5>=0 and px+img.width*.5<=self.w and py+img.height*.5<=self.h
    def _clip_paste(self,c,img,px,py):
        x=round(px-img.width/2);y=round(py-img.height/2)
        l=max(0,-x);t=max(0,-y);r=min(img.width,self.w-x);b=min(img.height,self.h-y)
        if r>l and b>t:c.alpha_composite(img.crop((l,t,r,b)),(max(0,x),max(0,y)))

    def line(self,d,pts,color,width=2):d.line([self.xy(*p) for p in pts],fill=color,width=max(1,self.X(width)),joint='curve')
    def oval(self,d,b,fill=None,outline=None,width=2):d.ellipse((*self.xy(b[0],b[1]),*self.xy(b[2],b[3])),fill=fill,outline=outline,width=max(1,self.X(width)))
    def poly(self,d,pts,fill):d.polygon([self.xy(*p) for p in pts],fill=fill)
    def rect(self,d,b,fill,outline=None,width=1,radius=0):
        b=(*self.xy(b[0],b[1]),*self.xy(b[2],b[3]));rad=self.X(radius)
        if rad:d.rounded_rectangle(b,fill=fill,outline=outline,width=max(1,self.X(width)),radius=rad)
        else:d.rectangle(b,fill=fill,outline=outline,width=max(1,self.X(width)))

    def background(self,v):
        key='outside' if v=='well' else 'field' if v in ('field','chase') else 'abstract' if v in ('diagram','chess','escape','title') else 'shaft'
        if key in self.background_cache:return self.background_cache[key].copy()
        c=Image.new('RGBA',(self.w,self.h),INK); ink=Image.new('RGBA',(self.w,self.h),(0,0,0,0));d=ImageDraw.Draw(ink,'RGBA')
        if key=='outside':
            # dusk outside the well, depth in landscape silhouette, editable vector objects
            # A restrained golden disc with layered alpha glows; never overwrite opacity into RGB.
            for j in range(7,0,-1):
                self.oval(d,(507-j*18,378-j*18,507+j*18,378+j*18),(244,157,77,max(3,26-j*3)),None)
            self.oval(d,(452,321,562,431),(240,181,113,180),None)
            self.poly(d,[(0,817),(130,780),(340,796),(515,720),(720,758),(720,1280),(0,1280)],(48,34,45,255))
            self.poly(d,[(0,936),(213,865),(450,924),(720,834),(720,1280),(0,1280)],(17,18,31,255))
            self.line(d,[(520,660),(520,460),(475,420)],(165,125,93,255),7)
            for p in [[(520,535),(557,509)],[(520,505),(483,485)],[(520,570),(559,554)]]:self.line(d,p,(165,125,93,210),4)
            self.line(d,[(287,820),(287,666),(390,602),(498,663),(498,826)],(207,158,89,255),11)
            self.poly(d,[(280,663),(390,594),(505,660)],(26,23,31,255))
            self.oval(d,(260,795,524,898),(13,15,26,255),(138,152,165,255),8)
            self.rect(d,(274,851,510,936),(39,39,52,255),(100,112,129,255),3)
            self.line(d,[(274,879),(510,879)],(94,105,120,200),2)
        elif key=='shaft':
            self.rect(d,(0,0,720,1280),(12,18,32,255))
            for row in range(19):
                y=160+row*59
                for col in range(8):
                    x=col*104-33+(52 if row%2 else 0)
                    self.rect(d,(x,y,x+99,y+54),(32+(row%4)*3,39+(col%3)*3,55+(row%3)*4,255),(53,63,83,160),2)
            self.poly(d,[(258,0),(460,0),(680,1007),(50,1007)],(193,191,166,19))
            self.poly(d,[(311,0),(405,0),(546,1007),(180,1007)],(221,211,168,13))
            self.oval(d,(-44,873,765,1143),(8,8,20,255),(98,111,130,230),5)
            self.oval(d,(75,915,647,1074),(41,11,25,255),None)
        elif key=='field':
            self.oval(d,(396,181,680,465),(225,163,96,230))
            self.poly(d,[(0,844),(90,800),(180,822),(286,775),(410,827),(600,779),(720,817),(720,1280),(0,1280)],(50,45,40,255))
            self.poly(d,[(0,970),(250,915),(496,962),(720,929),(720,1280),(0,1280)],(28,30,26,255))
            for i in range(31):
                x=20+i*24;y=925+17*math.sin(i*1.3)
                self.line(d,[(x,y),(x+3,y-103),(x-9,y-124)],(173,145,85,165),3)
                self.line(d,[(x+3,y-103),(x+17,y-134)],(173,145,85,100),2)
        else:
            for col in range(11):
                self.line(d,[(col*72,-40),(col*72,1278)],(36,47,68,65),1)
            for row in range(20):self.line(d,[(0,row*75),(720,row*75)],(36,47,68,65),1)
            self.oval(d,(80,195,640,905),None,(49,70,94,120),3)
        c.alpha_composite(ink)
        # Deterministic fine-grain surface; stable across frames and does not shimmer.
        self.background_cache[key]=c
        return c.copy()

    def camera(self,c,q,v):
        # independent actors are primary motion; camera is supportive and restrained
        zoom=1+.015*smooth(q)
        if v in ('predator','chase','conflict'):zoom=1+.04*smooth(q)
        if v in ('swarm','climb'):zoom=1+.02*q
        if zoom<1.002:return c
        zw,zh=round(self.w*zoom),round(self.h*zoom)
        im=c.resize((zw,zh),Image.Resampling.BILINEAR)
        dx=round(self.X(5)*math.sin(q*math.pi));dy=round(self.Y(4)*math.sin(q*math.pi))
        x=(zw-self.w)//2+dx;y=(zh-self.h)//2+dy
        return im.crop((x,y,x+self.w,y+self.h))

    def actors(self,c,s,q,seconds):
        v=s.get('visual','title');d=ImageDraw.Draw(c,'RGBA')
        if v=='well':
            # A farmer throws the pig into the well: a genuine curved animated arc.
            x=115-16*q;y=775
            self.paste_sprite(c,'person',x,y,1.13,angle=-12*wave(sub(q,.1,.6)))
            a=sub(q,.18,.88)
            px=mix(205,390,a);py=mix(640,827,a)-175*math.sin(a*math.pi)
            self.paste_sprite(c,'pig',px,py,mix(.70,.37,a),angle=-90*a,alpha=255 if a<.96 else round(255*(1-sub(a,.95,1))))
            self.oval(d,(270,814,520,884),None,(239,198,129,110+round(105*math.sin(a*math.pi))),3)
        elif v=='swarm':
            # Falling rat positions are staggered and count itself is continuously animated.
            for i in range(27):
                delay=.04+.55*(i/26);t=sub(q,delay,min(.99,delay+.36))
                x0=75+(i*131)%569;x1=155+(i*91)%411
                x=mix(x0,x1,t)+16*math.sin(i*1.6+seconds*2)*math.sin(t*math.pi)
                y=mix(90+(i*31)%190,945,t*t)
                sc=mix(.72,.44,t)
                self.paste_rat(c,x,y,sc,angle=mix(-18,75,t) if i%2 else mix(32,-70,t),alpha=round(255*(1-sub(t,.9,1))),seconds=seconds+i*.13,pace=3.5)
                if .06<t<.94:self.line(d,[(x,y-50),(x-17,y-155)],(226,178,96,60),2)
            count=round(mix(0,80,sub(q,0,.8)))
            self.big_number(d,f'{count:02d}',(350,395),'RATS ENTERED',RED if q>.7 else GOLD)
        elif v=='feeding':
            done=sub(q,.25,.87)
            self.paste_sprite(c,'pig',356,955,sc=.64*(1-.80*done),angle=0,alpha=round(255*(1-done)))
            self.paste_sprite(c,'bones',356,955,sc=.85,alpha=round(255*done))
            for i in range(18):
                a=i/18*math.tau+q*math.tau*.72
                rad=mix(206,132,sub(q,.0,.7));x=360+rad*math.cos(a);y=963+rad*.41*math.sin(a)
                self.paste_rat(c,x,y,.34+(i%3)*.045,angle=15*math.sin(a*2),flip=math.cos(a)<0,seconds=seconds+i*.17,pace=4)
        elif v=='climb':
            for i in range(12):
                t=(q*1.55+(i%4)*.19)%1
                ascent=t/.62 if t<.62 else 1-(t-.62)/.38
                ascend=clamp(ascent)
                x=70+(i%2)*578+24*math.sin(i*2.4+q*4)
                y=955-550*ascend-(i//2)*11
                self.paste_rat(c,x,y,.55,angle=75 if i%2 else -75,flip=i%2==0,seconds=seconds+i*.13,mood='red',pace=3.7)
                if t>.62:self.line(d,[(x,y-65),(x,y-15)],(255,81,92,105),3)
            if q>.72:self.big_number(d,'TRAPPED',(360,503),'NO WAY OUT',RED,size=56)
        elif v=='calendar':
            day=1+round(13*sub(q,0,.93))
            self.big_number(d,f'DAY {day:02d}',(360,490),'TIME PASSES',RED,size=65)
            for j in range(6):
                x=110+(j%3)*230;y=730+(j//3)*140
                self.rect(d,(x,y,x+116,y+120),(28,32,49,195),(225,122,121,140),2,8)
                self.line(d,[(x+5,y+36),(x+111,y+36)],(216,73,84,200),3)
                if j/6<q:self.line(d,[(x+25,y+63),(x+91,y+98)],RED,5)
        elif v=='conflict':
            for j in range(12):
                x=90+(j%4)*165;y=465+(j//4)*198
                rush=math.sin(q*math.tau*2+j*2.7)
                self.paste_rat(c,x+38*rush,y+12*abs(rush),.66,angle=-25*rush,flip=j%2==0,seconds=seconds+j*.11,mood='aggressive',pace=5.2)
                if rush>.65:self.line(d,[(x+41,y-24),(x+97,y+25)],RED,3)
        elif v=='countdown':
            num=max(1,round(mix(80,1,sub(q,.0,1.0))))
            self.big_number(d,str(num).zfill(2),(360,482),'REMAINING',RED,size=132)
            visible=max(1,round(22*(1-sub(q,.0,.92))))
            for i in range(visible):
                self.paste_rat(c,100+(i%5)*126,694+(i//5)*91,.40,alpha=round(255*(1-sub(q,.7,.97))),seconds=seconds+i*.12,mood='red')
        elif v=='predator':
            inhale=1+.055*math.sin(seconds*3.8)
            self.paste_rat(c,355,710,2.25*inhale,angle=2.5*math.sin(seconds*2),seconds=seconds,mood='aggressive',pace=1.2)
            for x in (293,408):
                p=.6+.4*(.5+.5*math.sin(seconds*9))
                self.oval(d,(x-45,659-38,x+45,659+38),(231,30,48,round(25*p)),None)
        elif v=='rope':
            drop=sub(q,.05,.49)
            bottom=mix(80,950,drop)
            self.line(d,[(355,0),(355,bottom)],(246,208,140,245),8)
            if q>.48:
                rising=sub(q,.48,.98)
                self.paste_rat(c,361,mix(900,175,rising),.74,angle=-90,seconds=seconds,mood='red')
        elif v=='field':
            self.paste_sprite(c,'person',135,788,1.27)
            rat_x=mix(280,490,sub(q,.04,.92))
            self.paste_rat(c,rat_x,876+7*math.sin(seconds*9),.97,angle=12*math.sin(seconds*7),seconds=seconds,mood='red',pace=4.5)
            for i in range(12):
                x=35+i*60
                self.line(d,[(x,1034),(x+16*math.sin(seconds*2+i),950),(x-11,933)],(240,190,94,128),2)
        elif v=='chase':
            for i in range(3):
                x=610-410*sub(q,.11*i,.80+min(.18,.1*i))
                self.paste_rat(c,x,858+i*38,.56,flip=True,seconds=seconds+i*.21,pace=5.6)
            predator_x=mix(100,565,sub(q,.08,.99))
            self.paste_rat(c,predator_x,820+22*math.sin(seconds*9),1.05,angle=6*math.sin(seconds*11),seconds=seconds,mood='red',pace=6)
            for i in range(7):
                y=740+i*50
                x=80+(i%3)*42
                self.line(d,[(x,y),(x-90+130*q,y)],(246,69,78,round(90*(1-q))),4)
        elif v=='diagram':
            self.big_number(d,'THE SYSTEM',(360,318),'WHO BENEFITS?',GOLD,size=59)
            self.rect(d,(130,410,600,490),(28,35,53,255),(234,192,102,230),3,10)
            self.line(d,[(360,490),(360,590)],(238,188,104,255),5)
            self.oval(d,(310,550,410,650),(203,162,92,255))
            for j in range(6):
                tx=105+j*101;ty=820+26*(j%2)
                p=sub(q,.1+j*.08,.42+j*.08)
                self.line(d,[(360,600),(mix(360,tx,p),mix(600,ty,p))],(230,67,80,180),3)
                self.paste_sprite(c,'person',tx,mix(1020,ty,p),.54,alpha=round(255*p))
        elif v=='chess':
            for row in range(6):
                for col in range(6):
                    x=105+col*86;y=585+row*70
                    self.rect(d,(x,y,x+86,y+70),(47,48,66,235) if (col+row)%2 else (18,21,35,240))
            a=sub(q,.06,.86)
            self.paste_sprite(c,'person',220+175*a,570+90*a,1.33,angle=4*math.sin(seconds*5))
            self.paste_sprite(c,'person',545-130*a,570+180*a,1.0)
            self.line(d,[(125,460),(570,460)],(236,186,103,200),3)
        elif v=='escape':
            self.rect(d,(150,207,570,1065),(24,29,44,255),(157,150,133,185),7)
            n=round(12*sub(q,.08,.82))
            for j in range(n):
                yy=1020-j*62
                self.rect(d,(270+9*(j%2),yy,435+9*(j%2),yy+12),(241,196,104,235))
            py=mix(1030,285,sub(q,.12,.89))
            self.paste_sprite(c,'person',363,py,.81)
            light=sub(q,.5,1)
            self.oval(d,(195,105,525,250),(246,219,152,round(30+225*light)))
        else:
            phase=seconds*1.2
            for j in range(8):
                a=math.tau*j/8+phase*.3
                r=mix(225,175,sub(q,.2,.85))
                self.oval(d,(360+r*math.cos(a)-11,665+r*math.sin(a)-11,360+r*math.cos(a)+11,665+r*math.sin(a)+11),RED if j%2 else GOLD)
            self.line(d,[(360,400),(360,950)],(235,190,102,105),4)

    def big_number(self,d,text,xy,subtitle,color,size=92):
        f=fnt(self.X(size),True);p=self.xy(*xy)
        b=d.textbbox((0,0),text,font=f);tw=b[2]-b[0]
        d.text((p[0]-tw/2,p[1]-self.Y(38)),text,fill=color,font=f,stroke_width=max(1,self.X(2)),stroke_fill=(18,19,30,255))
        sf=fnt(self.X(23),True);bb=d.textbbox((0,0),subtitle,font=sf)
        d.text((p[0]-(bb[2]-bb[0])/2,p[1]+self.Y(64)),subtitle,fill=(235,223,208,235),font=sf)

    def floating_particles(self,c,t,idx):
        d=ImageDraw.Draw(c,'RGBA');rng=random.Random(idx*701+45)
        for j in range(27):
            x=rng.randrange(720);y=(rng.randrange(1280)-t*(21+j%5*7)+j*23)%1280
            r=(1+j%3)
            self.oval(d,(x-r,y-r,x+r,y+r),(242,182,92,65+(j%3)*20))

    def typography(self,c,s,q,duration):
        d=ImageDraw.Draw(c,'RGBA');ttl=str(s.get('title','')).upper();accent=RED if s.get('accent')=='red' else GOLD
        if ttl:
            # KINETIC TYPE: per-character reveal, overshoot-free entrance, tracking and underline wipe.
            enter=sub(q,0,min(.18,.6/max(1,duration)))
            reveal=max(0,min(len(ttl),int(len(ttl)*sub(q,0,.22))+1))
            text=ttl[:reveal]
            fs=self.X(49 if len(ttl)<20 else 36)
            ff=fnt(fs,False)
            if d.textbbox((0,0),ttl,font=ff)[2]>self.X(640):ff=fnt(self.X(31),False)
            bb=d.textbbox((0,0),ttl,font=ff);full_w=bb[2]-bb[0]
            top=self.Y(135-21*(1-enter));left=(self.w-full_w)/2
            self.rect(d,(48,115,672,215),(3,7,16,190),radius=10)
            d.text((left,top),text,font=ff,fill=(242,241,235,round(255*enter)))
            eye=str(s.get('eyebrow','')).upper();ef=fnt(self.X(19),True)
            eb=d.textbbox((0,0),eye,font=ef);ew=eb[2]-eb[0]
            if q>.16:d.text(((self.w-ew)/2,self.Y(201)),eye,font=ef,fill=(*accent[:3],round(255*sub(q,.16,.3))))
            self.rect(d,(244,245,244+232*sub(q,.13,.33),250),accent)
        segs=s.get('caption_chunks')
        if not segs:
            words=str(s.get('narration','')).strip().split();segs=[' '.join(words[i:i+5]) for i in range(0,len(words),5)]
        if segs:
            j=min(len(segs)-1,math.floor(q*len(segs)));local=clamp(q*len(segs)-j)
            line=str(segs[j]);ff=fnt(self.X(29),True)
            while d.textbbox((0,0),line,font=ff)[2]>self.X(611) and ff.size>self.X(19):ff=fnt(ff.size-1,True)
            bb=d.textbbox((0,0),line,font=ff);tw=bb[2]-bb[0]
            cc=sub(local,0,.15)
            y=self.Y(1052+19*(1-cc));x=(self.w-tw)/2
            self.rect(d,((x-18)/self.k,(y-self.Y(13))/(self.h/1280),(x+tw+18)/self.k,(y+self.Y(51))/(self.h/1280)),(5,8,18,round(224*cc)),(*accent[:3],round(130*cc)),1,8)
            d.text((x,y),line,font=ff,fill=(255,252,245,round(255*cc)))

    def frame(self,index,t):
        s=self.scenes[index];v=s.get('visual','title');start=float(s['start']);end=float(s['end'])
        dur=end-start;q=clamp((t-start)/dur)
        c=self.background(v)
        # Animated foreground illustration and diagram independently layered over background.
        self.actors(c,s,q,t)
        self.floating_particles(c,t,index)
        c=self.camera(c,q,v)
        self.typography(c,s,q,dur)
        d=ImageDraw.Draw(c,'RGBA');accent=RED if s.get('accent')=='red' else GOLD
        self.rect(d,(0,1271,720*(t/max(.001,float(self.scenes[-1]['end']))),1280),(*accent[:3],230))
        return c.convert('RGB')
