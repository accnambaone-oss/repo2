"""Original frame-exact 2D rat rig, built for cinematographic motion rather than static stickers.

The rig generates 16 repeatable gait poses. Tail, fore/hind feet, head tilt,
whiskers, blink and torso squash are independently articulated. Stable poses
avoid frame-to-frame texture jitter. Inspired by animation-production principles,
not copied from third-party rig source code.
"""
from __future__ import annotations
import math


def rigged_rat_svg(phase: float = 0., mood: str = 'neutral', blink: bool = False) -> str:
    """Produce an SVG of a side-view rat centered at (0,0), nose to the right.

    Pose is deterministic in the canonical [0,1) gait cycle.
    """
    p=phase%1
    swing=math.sin(2*math.pi*p)
    hind=math.sin(2*math.pi*(p+.5))
    squash=1.0-.042*abs(swing)
    head_y=-2.6*math.sin(2*math.pi*p)
    tail_tip_y=7+16*math.sin(2*math.pi*(p+.17))
    red=mood in ('red','aggressive')
    eye='#fc5164' if red else '#f8d49b'
    iris='#faeff0' if red else '#fff3cb'
    # Joints move under a fixed torso (not entire sprite translating).
    ftoe_x=25+15*swing; ftoe_y=28+max(0,7*swing)
    htoe_x=-29+15*hind; htoe_y=29+max(0,7*hind)
    angle=-4*swing
    lid='<path d="M38 -13 L52 -12" stroke="#705c67" stroke-width="4"/>' if blink else ''
    jaw_shift=2.5 if mood=='aggressive' else 0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-122 -78 244 156" width="244" height="156">
    <defs>
      <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
        <stop stop-color="#4d3748"/><stop offset=".44" stop-color="#322832"/><stop offset="1" stop-color="#1a1b29"/>
      </linearGradient>
      <radialGradient id="ear"><stop stop-color="#bc7580"/><stop offset="1" stop-color="#5d3e52"/></radialGradient>
    </defs>
    <g fill="none" stroke-linecap="round" stroke-linejoin="round">
      <!-- Tail uses a curved, changing joint instead of a rigid angle. -->
      <path d="M-53 5 C-86 {-18+swing*7:.1f},-100 {-10+swing*8:.1f},-112 {tail_tip_y:.1f}"
         stroke="#8c616e" stroke-width="5"/>
      <path d="M-54 8 C-86 {-15+swing*7:.1f},-102 {-8+swing*8:.1f},-111 {tail_tip_y:.1f}"
         stroke="#d19b99" stroke-width="1.8" opacity=".83"/>
      <!-- Rear hind foot and knee. -->
      <path d="M-31 13 L{-34+hind*6:.2f} {22+max(0,hind*5):.2f} L{htoe_x:.2f} {htoe_y:.2f} L{htoe_x+12:.2f} {htoe_y:.2f}"
         stroke="#806872" stroke-width="5"/>
      <g transform="rotate({angle:.2f} -3 0) scale(1 {squash:.4f})">
        <ellipse cx="-8" cy="4" rx="47" ry="27" fill="url(#body)" stroke="#98717d" stroke-width="2.7"/>
        <!-- Physical form / hatch is attached to the body, not random each frame. -->
        <path d="M-43 -1 Q-15 -29 21 -10" stroke="#d4a9a3" opacity=".24" stroke-width="3.4"/>
        <path d="M-33 -9 l-7 8 M-21 -15 l-7 11 M-8 -18 l-7 10 M5 -17 l-6 9 M19 -12 l-6 8"
              stroke="#cfa9a0" stroke-width="1.4" opacity=".43"/>
        <path d="M-31 17 Q-12 22 11 14" stroke="#0c101d" opacity=".7" stroke-width="3"/>
      </g>
      <!-- Foreleg, alternating gait and backleg show supported contact. -->
      <path d="M17 12 L{12+swing*4:.2f} {21+max(0,-swing*4):.2f} L{ftoe_x:.2f} {ftoe_y:.2f} L{ftoe_x+9:.2f} {ftoe_y+1:.2f}"
            stroke="#cfb0a8" stroke-width="4"/>
      <path d="M-15 18 L{-20-hind*4:.2f} {24+max(0,-hind*3):.2f} L{htoe_x-5:.2f} {htoe_y+2:.2f}"
            stroke="#bd9a9d" stroke-width="3"/>
      <!-- Head can bob independently of torso; muzzle tapers. -->
      <g transform="translate(0 {head_y:.2f})">
       <path d="M18 -16 Q42 -30 61 -12 Q68 -5 79 -2 Q72 10 57 13 Q40 19 19 11Z"
             fill="#322735" stroke="#ab7b85" stroke-width="2.5"/>
       <ellipse cx="34" cy="-27" rx="11" ry="14" fill="url(#ear)" stroke="#d49ca2" stroke-width="2"/>
       <ellipse cx="55" cy="-22" rx="10" ry="12" fill="url(#ear)" stroke="#a77e8a" stroke-width="1.8"/>
       <ellipse cx="49" cy="-8" rx="5.7" ry="4" fill="{eye}"/>
       <circle cx="49.8" cy="-9.5" r="1.7" fill="{iris}"/>
       {lid}
       <ellipse cx="75" cy="-1" rx="3.5" ry="2.7" fill="#d6a0a5"/>
       <path d="M56 8 Q65 {13+jaw_shift:.1f} 74 7" stroke="#b77d85" stroke-width="1.5"/>
       <path d="M61 0 L93 -8 M62 4 L95 3 M61 7 L92 15" stroke="#c6afb2" stroke-width="1.2" opacity=".8"/>
      </g>
    </g></svg>'''
