"""Developer utility: rebuild hand-timed example; original narrative text supplied by user."""
import json,pathlib
p=pathlib.Path(__file__).resolve().parent
S=[
(0,3.7,'well','A DRIED-UP WELL','THE PARABLE BEGINS','A farmer threw a dead pig into a dried up well.','gold'),
(3.7,7.7,'swarm','80 RATS','ATTRACTED BY THE SMELL','Within minutes, 70 to 80 rats jumped into the well, attracted by the smell.','gold'),
(7.7,10,'feeding','EASY FOOD','THE BAIT IN THE DARK','For them, it was easy food.','gold'),
(10,12.8,'feeding','EVERY LAST BIT','DEVOURED TO THE BONE','They attacked the pig together and ate every last bit of it.','gold'),
(12.8,17.2,'climb','MEAL OVER','THE REAL PROBLEM BEGINS','But the real problem started after the meal was over. When they tried to climb back out,','red'),
(17.2,21.7,'climb','NO GRIP','SHEER VERTICAL STONE','they realized something terrifying. They were trapped.','red'),
(21.7,26.6,'calendar','DAYS PASSED','HUNGER KEPT GROWING','Days passed. The food was gone, but the hunger kept growing.','red'),
(26.6,29.8,'conflict','INTO HELL','DESCENDING INTO MADNESS','And within a few days, the well had turned into hell.','red'),
(29.8,34.9,'conflict','SURVIVAL WAR','NO MERCY IN THE PIT','To survive, the rats started attacking each other. Then they started eating each other.','red'),
(34.9,37.5,'countdown','ONE BY ONE','THE OTHERS VANISHED','One by one, they disappeared.','red'),
(37.5,40.5,'predator','ONLY ONE LEFT','TWO WEEKS IN THE DARK','After about two weeks, only one rat was left.','red'),
(40.5,43.8,'predator','BLOOD RED','A PREDATOR IS BORN','Its eyes had turned blood red.','red'),
(43.8,46.8,'rope','PULLED OUT','THE FARMER RETURNS','Then the farmer came back, lowered a rope into the well, pulled the last rat out,','gold'),
(46.8,48.9,'field','RELEASED','INTO THE GRAIN FIELD','and released it into his field.','gold'),
(48.9,51.6,'field','IT HAD CHANGED','SOMETHING WAS WRONG','The rat had changed.','red'),
(51.6,54.7,'predator','ADDICTED TO BLOOD','NO LONGER ATE GRAIN','It had become addicted to hunting its own kind, so it no longer ate grain.','red'),
(54.7,58.9,'chase','HUNTING ITS OWN','A DANGEROUS NEW INSTINCT','The moment it entered the field, it started hunting other rats like a maniac.','red'),
(58.9,61.4,'title','THE REAL GAME','BEGINS NOW',"That's where the real game begins.",'gold'),
(61.4,64.9,'title','THE DIVIDE TRAP','THE REVEAL','This is called the divide trap.','red'),
(64.9,68,'diagram','AT THE TOP: PEACE','NEVER FIGHT EACH OTHER','The people at the top never fight each other.','gold'),
(68,72.5,'diagram','BELOW: CHAOS','ENGINEERED CONFLICT','They simply create an environment where the people below start fighting each other until they destroy one another.','red'),
(72.5,78.7,'chess',"SOMEONE ELSE'S GAME",'PAWNS ON THE BOARD',"The truth is, many people spend their entire lives trying to defeat others without realizing they've already become part of someone else's game.",'red'),
(78.7,83.7,'escape','BREAK THE CYCLE','LOOK UP BEYOND THE WALLS',"So don't fall into a trap created by someone else.",'gold'),
(83.7,87.8,'escape','STOP FIGHTING INSIDE','LOOK UP BEYOND THE WALLS',"And if you ever find yourself trapped, don't keep fighting inside the trap.",'gold'),
(87.8,90,'escape','FIND THE WAY OUT','YOUR CHOICE CHANGES THE END','Find the way out.','gold')]
scene=[dict(id=f's{i+1:02d}',start=a,end=b,visual=v,title=t,eyebrow=eb,narration=n,accent=c) for i,(a,b,v,t,eb,n,c) in enumerate(S)]
story=dict(name='The Divide Trap — visual allegory',kind='allegory_unverified_not_an_actual_pest_control_method',width=720,height=1280,fps=24,scenes=scene,
            fact_check_note='User-supplied rat parable is not documented scientific evidence; do not present it as a real rodent-behavior experiment.',
            rendering_note='Caption timing per scene is proportional, not word aligned. Verify with real narration before publication.')
(p/'divide_trap.json').write_text(json.dumps(story,indent=2),encoding='utf-8')
print('saved sample',len(scene),'scenes')
