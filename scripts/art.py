"""Original inline SVG art factory. All geometry originates in code, not external media."""
from __future__ import annotations
import math, random

NAVY='#0b0f1b'; RED='#ec3948'; GOLD='#f4c86c'; PAPER='#e7e8ed'

def rat(x,y,s=1,eye='gold',flip=False):
    c=RED if eye=='red' else GOLD
    tr=f'translate({x:.1f} {y:.1f}) scale({-s if flip else s:.3f} {s:.3f})'
    return f'''<g transform="{tr}">
    <path d="M-26 8 Q-73 -6 -83 14" fill="none" stroke="#a27274" stroke-width="2"/>
    <ellipse cx="0" cy="0" rx="31" ry="19" fill="#151321" stroke="#996e74" stroke-width="1.8"/>
    <path d="M18 -8 Q38 -19 48 -6 L55 2 42 13 17 9Z" fill="#1b1821" stroke="#a77477" stroke-width="1.5"/>
    <circle cx="29" cy="-19" r="9" fill="#32202b" stroke="#a77477" stroke-width="1.4"/>
    <circle cx="43" cy="-15" r="8" fill="#3b2632" stroke="#a77477" stroke-width="1.4"/>
    <ellipse cx="38" cy="-2" rx="4" ry="3" fill="{c}"/>
    <path d="M47 3 L67 -4 M47 5 L67 5 M47 6 L66 13 M-10 16 L-16 30 M10 16 L16 30" stroke="#9c797b" stroke-width="1.3" fill="none"/>
    </g>'''

def person(x,y,scale=1,color=GOLD,arms='down'):
    arm='<path d="M-16 -28 L-31 -5 M16 -28 L31 -5"/>' if arms=='down' else '<path d="M-16 -28 L-31 -53 M16 -28 L31 -53"/>'
    return f'''<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round">
    <circle cx="0" cy="-73" r="12"/><path d="M0 -60 L0 3 M0 3 L-18 34 M0 3 L18 34"/>{arm}</g>'''

def pig(x,y):
    return f'''<g transform="translate({x} {y})" stroke="#d8a5a0" stroke-width="3" fill="#7a4656">
    <ellipse cx="0" cy="0" rx="107" ry="47"/><ellipse cx="95" cy="-9" rx="47" ry="36"/>
    <path d="M62 -43 l-8 -27 28 16 M93 -45 l24 -18 -2 31"/>
    <ellipse cx="128" cy="-1" rx="17" ry="12" fill="#d99a99"/>
    <path d="M-67 35 L-60 66 M-5 44 L-2 72 M59 35 L70 63"/><circle cx="100" cy="-17" r="4" fill="#f3cfbc"/>
    </g>'''

def brick_wall():
    rows=[]
    for j in range(16):
        y=138+j*60
        for i in range(7):
            x=-54+i*119+(60 if j%2 else 0)
            rows.append(f'<rect x="{x}" y="{y}" width="113" height="54" rx="2" fill="{["#182133","#1d273a","#20293a"][j%3]}" stroke="#30374a" stroke-width="2" opacity=".54"/>')
    return ''.join(rows)

def ring(count,eye='gold',center_y=730,rx=245,ry=130):
    rng=random.Random(29+count)
    parts=[]
    for i in range(count):
        a=2*math.pi*i/count
        parts.append(rat(360+rx*math.cos(a),center_y+ry*math.sin(a),.43+(i%3)*.055,eye,flip=math.cos(a)<0))
    return ''.join(parts)

def crowd(bottom_y=820,color=RED):
    return ''.join(person(88+i*91,bottom_y+(i%2)*12,.68,color,arms='up' if i%3==0 else 'down') for i in range(7))

def background(visual):
    wall=visual in {'well','swarm','feeding','climb','calendar','countdown','predator','rope','escape','conflict'}
    background_color='#0a0d17'
    grad='#3f0e17' if visual in {'conflict','countdown','predator','chase'} else '#25263e'
    return f'''<defs>
    <radialGradient id="warm" cx="55%" cy="38%" r="70%"><stop stop-color="{grad}"/><stop offset=".7" stop-color="#101424"/><stop offset="1" stop-color="{background_color}"/></radialGradient>
    <linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fae1a9" stop-opacity=".17"/><stop offset="1" stop-color="#faf0c0" stop-opacity=".015"/></linearGradient>
    <radialGradient id="pit"><stop stop-color="#36151d"/><stop offset="1" stop-color="#060710"/></radialGradient>
    </defs><rect width="720" height="1280" fill="url(#warm)"/>
    {brick_wall() if wall else ''}
    {('<path d="M255 160 L465 160 705 1020 15 1020Z" fill="url(#shaft)"/>' if wall else '')}
    <rect x="0" y="0" width="720" height="1280" fill="#060812" opacity=".15"/>'''

def well_base(pit=True):
    return '<ellipse cx="360" cy="797" rx="302" ry="136" fill="url(#pit)" stroke="#657083" stroke-width="6"/>' if pit else ''

def art_svg(scene):
    v=scene.get('visual','title'); eye='red' if scene.get('accent')=='red' else 'gold'
    items=[]
    if v=='well':
        items+=['<circle cx="575" cy="322" r="127" fill="#efb765" opacity=".12"/>','<path d="M0 784 Q300 701 720 757 V1280 H0Z" fill="#080a10"/>',
                '<path d="M192 690 L192 556 L351 476 517 556 L517 693" fill="none" stroke="#b98d5a" stroke-width="15"/>',
                '<ellipse cx="357" cy="782" rx="177" ry="58" fill="#01030a" stroke="#7b808c" stroke-width="10"/>',
                person(103,720,1.3, '#c7ab75')]
        items.append(pig(302,560))
    elif v in {'swarm','feeding','calendar','climb','countdown','rope'}:
        items.append(well_base())
        if v=='swarm':
            for i in range(17):
                items.append(rat(127+(i*73)%470,233+i*31,.6,'gold',flip=i%2==0))
            items+=['<path d="M130 215 Q210 550 315 765 M550 215 Q455 550 415 752" stroke="#c5b96b" opacity=".23" stroke-width="4" fill="none"/>']
        elif v=='feeding':
            items.append(pig(333,769));items.append(ring(15,'gold',771,227,97))
        elif v=='climb':
            for i in range(7):
                items.append(rat(105 if i%2 else 616,850-96*i,.62,'red',flip=i%2==0))
            items+=['<path d="M0 220 L720 220" stroke="#dfe2ef" stroke-width="12" opacity=".7"/>']
        elif v=='calendar':
            items.append(ring(19,'red',797,244,117))
            items+=['<path d="M320 760 h88 M344 732 v58" stroke="#f0dba8" opacity=".8" stroke-width="6"/>']
        elif v=='countdown':
            for i in range(16):
                x=88+i%4*181;y=450+(i//4)*137
                if i<12:items.append(f'<path d="M{x-20} {y-20} l40 40 m0 -40 l-40 40" stroke="#e93444" stroke-width="5"/>')
                else: items.append(rat(x,y,.55,'red'))
        elif v=='rope':
            items+=['<path d="M345 125 L350 775" stroke="#f6d79e" stroke-width="10" stroke-dasharray="15 10"/>',rat(354,758,.9,'red')]
    elif v=='conflict':
        for i in range(12):
            x=145+(i%3)*216;y=417+(i//3)*137
            items.append(rat(x,y,.68,'red',flip=i%2==0))
            if i%2==0:items.append(f'<path d="M{x+33} {y-30} l75 53" stroke="#ee3444" stroke-width="8"/>')
    elif v=='predator':
        items+=['<ellipse cx="360" cy="724" rx="238" ry="271" fill="#120c16" stroke="#e33b4d" stroke-width="5"/>',
                '<circle cx="245" cy="488" r="80" fill="#170b16" stroke="#d94753" stroke-width="5"/>',
                '<circle cx="485" cy="488" r="80" fill="#170b16" stroke="#d94753" stroke-width="5"/>',
                '<path d="M202 672 Q285 624 359 694 Q432 625 521 672" fill="none" stroke="#83454d" stroke-width="5"/>',
                '<ellipse cx="284" cy="656" rx="46" ry="18" fill="#f22c41"/><ellipse cx="436" cy="656" rx="46" ry="18" fill="#f22c41"/>',
                '<path d="M200 714 L45 671 M200 728 L42 729 M520 714 L685 671 M520 728 L682 729" stroke="#c4a19d" stroke-width="4"/>']
    elif v=='field':
        items+=['<circle cx="530" cy="293" r="115" fill="#ead4a1" opacity=".76"/>',
                '<path d="M0 895 Q340 827 720 903 V1280 H0" fill="#302325"/>',
                person(170,716,1.8,'#efd09b')]
        for i in range(12):items.append(f'<path d="M{30+i*62} 897 v-140 l-16 -23 m16 23 l16 -18" fill="none" stroke="#c5ac67" stroke-width="4"/>')
        items.append(rat(471,864,1.35,'red'))
    elif v=='chase':
        items+=['<ellipse cx="285" cy="780" rx="310" ry="160" fill="#8d1329" opacity=".2"/>',
                 rat(297,794,1.55,'red')]
        items.extend([rat(493+i*64,841-i*10,.79,'gold',flip=False) for i in range(3)])
        for i in range(10):items.append(f'<path d="M{40+i*36} {600+i*30} h85" stroke="#e23445" stroke-width="3" opacity=".35"/>')
    elif v=='diagram':
        items+=['<rect x="78" y="425" width="565" height="21" fill="#efc267"/>',
                person(242,403,1.2,GOLD),person(475,403,1.2,GOLD),
                '<path d="M225 312 L151 770 M480 312 L586 770 M365 446 V771" stroke="#cfb373" stroke-width="3" stroke-dasharray="12 12" opacity=".75"/>',
                '<rect x="56" y="765" width="610" height="241" rx="16" fill="#4a101c" stroke="#ef3a4b" stroke-width="3"/>',crowd(892)]
    elif v=='chess':
        for j in range(7):
            for i in range(7):
                x=45+i*92;y=507+j*68
                items.append(f'<path d="M{x} {y} l95 0 l0 68 l-95 0Z" fill="{["#3a3c50","#101522"][(i+j)%2]}" opacity=".9"/>')
        items += [person(280,585,1.2,RED),person(444,585,1.2,RED),
                  '<path d="M245 505 L177 315 L543 315 L480 505" fill="none" stroke="#bda06c" stroke-width="4"/>']
    elif v=='escape':
        items+=['<path d="M110 185 L610 185 L610 1038 L110 1038Z" fill="#252e3c" stroke="#6d6875" stroke-width="12"/>',
                '<path d="M236 185 L484 185 650 1040 70 1040Z" fill="url(#shaft)"/>',
                person(358,875,1.7,GOLD,'up')]
        for i in range(11):
            y=902-i*55
            items.append(f'<rect x="{304+(i%2)*8}" y="{y}" width="108" height="10" fill="#f9d478" opacity="{.6+i*.033}"/>')
        items += ['<ellipse cx="359" cy="170" rx="173" ry="35" fill="#ffedba"/>']
    else:
        items+=['<circle cx="360" cy="628" r="230" fill="none" stroke="#e3b566" stroke-width="3" opacity=".6"/>',
                '<path d="M360 375 L600 791 120 791Z" fill="none" stroke="#e6bc69" stroke-width="4"/>',
                '<path d="M360 333 V855 M106 632 H614" stroke="#ed4f55" stroke-width="4" opacity=".6"/>']
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1280" viewBox="0 0 720 1280">{background(v)}{"".join(items)}</svg>'
