#!/usr/bin/env python3
"""Create a deterministic starter shot list from plain narration. This is NOT auto-research."""
import argparse, json, math, pathlib, re, textwrap
VISUALS=[('chase',r'hunt|chase|pursu'),('rope',r'rope|pulled|farmer came back'),('swarm',r'jumped|attracted|crowd|gather'),('feeding',r'food|pig|meal|eating'),('climb',r'climb|escape|trapped|grip'),('calendar',r'days|weeks|time passed'),('conflict',r'fighting|attack|destroy|battle'),('countdown',r'one by one|disappear|remaining'),('predator',r'eyes|blood red|changed'),('field',r'field|grain'),('diagram',r'top|below|environment|manipulat|divide'),('chess',r'game|pawn|someone else'),('escape',r'way out|cycle|find the way'),('well',r'well')]

def split_sentences(text):
    text=re.sub(r'<[^>]+>',' ',text)
    text=re.sub(r'&#x20;',' ',text)
    return [re.sub(r'\s+',' ',s).strip(' \n\"') for s in re.split(r'(?<=[.!?])\s+|\n\s*\n',text) if s.strip()]

def suggest_visual(text):
    for name,pattern in VISUALS:
        if re.search(pattern,text,re.I): return name
    return 'title'

def make_story(text, duration='auto'):
    sent=split_sentences(text)
    if not sent: raise ValueError('No sentences found')
    groups=[]; bucket=[]; words=0
    for s in sent:
        count=len(s.split())
        if bucket and (words+count>22 or len(bucket)>=2):
            groups.append(' '.join(bucket)); bucket=[];words=0
        bucket.append(s);words+=count
    if bucket:groups.append(' '.join(bucket))
    wc=len(text.split()); seconds=max(90,min(600,(wc/150*60)+len(groups)*.22)) if duration=='auto' else float(duration)
    if seconds<=0:raise ValueError('Duration must be positive')
    weights=[max(3.3,len(s.split())/2.65+.20) for s in groups]
    total=sum(weights);scenes=[];t=0.0
    for i,(s,weight) in enumerate(zip(groups,weights)):
        dur=seconds*weight/total;end=seconds if i==len(groups)-1 else t+dur
        title=re.sub(r'[.,!?]','',s).split()
        title=' '.join(title[:min(5,len(title))]).upper()
        scenes.append(dict(id=f's{i+1:02d}',start=round(t,3),end=round(end,3),visual=suggest_visual(s),title=title,eyebrow='THE STORY CONTINUES',narration=s,accent='red' if i>len(groups)*.3 and i<len(groups)*.8 else 'gold'))
        t=end
    return dict(name='New cinematic explainer',width=720,height=1280,fps=24,kind='unverified_allegory_or_fact_check_required',scenes=scenes)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--script',required=True);ap.add_argument('--out',required=True);ap.add_argument('--duration',default='auto');a=ap.parse_args()
    src=pathlib.Path(a.script).read_text(encoding='utf-8');dest=pathlib.Path(a.out);dest.mkdir(parents=True,exist_ok=True)
    plan=make_story(src,a.duration);(dest/'story.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    (dest/'script.txt').write_text(src,encoding='utf-8')
    print('Wrote',dest/'story.json','seconds:',round(plan['scenes'][-1]['end'],2),'scenes:',len(plan['scenes']))
if __name__=='__main__':main()
