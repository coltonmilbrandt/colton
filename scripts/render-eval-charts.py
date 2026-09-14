"""Render dependency-free, downloadable SVG figures from the article's reported results."""
from pathlib import Path
from html import escape
OUT = Path(__file__).resolve().parents[1] / 'assets/images/evals'
TEAL = '#83ddd0'
BLUE = '#9db8da'
def text(x,y,value,size=24,color='#eaf2fb',extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(value)}</text>'
def line(x1,y1,x2,y2,color='#30465e',extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" {extra}/>'
def circle(x,y,r,color):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'
def save(name,title,desc,h,body):
    (OUT/name).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{h}" viewBox="0 0 800 {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><radialGradient id="glow" cx="100%" cy="0%" r="100%"><stop stop-color="#244f60"/><stop offset="1" stop-color="#122339"/></radialGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#adc7dc" opacity=".12"/></pattern></defs>
<rect width="800" height="{h}" rx="18" fill="url(#glow)"/><rect width="800" height="{h}" rx="18" fill="url(#grid)"/>
<g font-family="Arial, sans-serif">{body}</g></svg>''')
# Batching instruction: tiles are aggregate counts, then before/after pairs per metric.
b=text(40,48,'01 / WHEN THE SCORE FOOLS YOU',20,TEAL,'letter-spacing="2"')
b+=text(40,99,'Same model. One sentence. 0 of 18 to 6 of 6.',32,extra='font-weight="700"')
def tiles(y,total,passed,pitch=48,size=36):
 result=''
 for i in range(total):
  xx=40+i*pitch
  if i<passed:
   result+=f'<rect x="{xx}" y="{y}" width="{size}" height="{size}" rx="7" fill="{TEAL}"/>'
  else:
   result+=f'<rect x="{xx}" y="{y}" width="{size}" height="{size}" rx="7" fill="#352f43" stroke="#df9ea9"/>'+line(xx+size*.3,y+size*.3,xx+size*.7,y+size*.7,'#df9ea9','stroke-width="2"')+line(xx+size*.7,y+size*.3,xx+size*.3,y+size*.7,'#df9ea9','stroke-width="2"')
 return result
b+=text(40,153,'Runs that batched every search · three reasoning settings',23,BLUE)+text(752,153,'0 / 18',26,extra='text-anchor="end" font-weight="700"')+tiles(174,18,0,40,30)
b+=text(40,255,'Runs that batched every search · one added instruction',23,BLUE)+text(752,255,'6 / 6',26,extra='text-anchor="end" font-weight="700"')+tiles(276,6,6)
b+=line(40,343,760,343)
b+=text(40,384,'SIX-SCENARIO RUN · BEFORE → AFTER THE INSTRUCTION',19,BLUE,'letter-spacing="1"')
def pair(y,label,before,after):
 return text(40,y,label,24,BLUE)+text(560,y,before,26,BLUE,'text-anchor="end"')+text(600,y,'→',26,BLUE,'text-anchor="middle"')+text(760,y,after,26,TEAL,'text-anchor="end" font-weight="700"')
b+=pair(432,'Candidate · scenarios passed','5 / 6','6 / 6')
b+=pair(478,'Candidate · model round trips / turn','5.3','4.0')
b+=pair(524,'Candidate · median turn','12.6 s','8.0 s')
b+=pair(570,'Reference · median turn','10.6 s','7.8 s')
b+=text(40,624,'Multi-item probe: 3 runs × 2 asks per condition · single-run contract results',21,BLUE)
save('batching-instruction.svg','When the score fools you: same model, one sentence, 0 of 18 to 6 of 6','Across three reasoning settings, zero of eighteen runs batched every search into one response. With one added sentence, six of six did. On the six-scenario run the candidate went from five of six passes to six of six, from 5.3 to 4.0 model round trips per turn, and from a 12.6 to an 8.0 second median turn. The reference model median turn fell from 10.6 to 7.8 seconds.',660,b)
# Aggregate count tiles: no invented run order or per-scenario identities.
b=text(40,48,'02 / RELIABILITY UNDER REPETITION',20,TEAL,'letter-spacing="2"')
b+=text(40,99,'An early pass wasn’t the finish line.',32,extra='font-weight="700"')
b+=text(40,153,'Initial candidate',24,BLUE)+text(752,153,'6 / 6 passed',26,extra='text-anchor="end" font-weight="700"')+tiles(174,6,6)
b+=line(40,239,760,239)
b+=text(40,280,'Repeated gate · candidate',24,BLUE)+text(752,280,'12 / 15',26,extra='text-anchor="end" font-weight="700"')+tiles(301,15,12)
b+=text(40,382,'Repeated gate · reference',24,BLUE)+text(752,382,'15 / 15',26,extra='text-anchor="end" font-weight="700"')+tiles(403,15,15)
b+=text(40,490,'Each tile = one run · grouped by outcome, not run order',21,BLUE)
save('repeated-tests.svg','Repeated testing exposed three failures','Initial candidate: six of six passed. In a separate repeated gate the candidate passed twelve of fifteen and the reference fifteen of fifteen. Tiles are grouped by outcome and do not show run order.',520,b)
# Each metric has its own labeled zero-based scale, plus precise source values.
b=text(40,48,'03 / LATER PROTOTYPE',20,TEAL,'letter-spacing="2"')
b+=text(40,94,'Two gains. A different configuration.',32,extra='font-weight="700"')
def metric(y,title,change,vref,vnew,maximum,ref,new,end):
 xx=lambda v:40+v/maximum*720
 s=text(40,y,title,23,BLUE)+text(760,y,change,32,TEAL,'text-anchor="end" font-weight="700"')
 s+=text(40,y+48,'Prototype '+new,25,TEAL)+text(760,y+48,'Reference '+ref,25,BLUE,'text-anchor="end"')
 s+=line(40,y+95,760,y+95)+line(xx(vnew),y+95,xx(vref),y+95,'#598c9e','stroke-width="5"')
 s+=circle(xx(vref),y+95,9,BLUE)+circle(xx(vnew),y+95,13,TEAL)+circle(xx(vnew),y+95,5,'#122339')
 s+=text(40,y+139,'0',20,BLUE)+text(760,y+139,end,20,BLUE,'text-anchor="end"')
 return s
b+=metric(153,'COST / TURN','≈92% lower',.041,.0031,.05,'$0.041','$0.0031','$0.05')
b+=line(40,320,760,320)
b+=metric(367,'MEDIAN LATENCY','≈36% lower',13.7,8.7,15,'13.7 s','8.7 s','15 seconds')
save('prototype-tradeoffs.svg','Prototype cost and latency comparisons','Approximate cost per turn: prototype $0.0031, reference $0.041. Median latency: prototype 8.7 seconds, reference 13.7 seconds. Multiple configuration changes prevent attributing the gains to batching alone.',541,b)
# A lead graphic summarizes the evaluation story without combining the experiments.
b=text(40,48,'MINDYCART / EVALUATION FIELD NOTES',20,TEAL,'letter-spacing="2"')
b+=text(40,108,'What a passing score can miss.',38,extra='font-weight="700"')
b+=text(40,148,'Different tests. Different product decisions.',24,BLUE)
b+=line(40,181,760,181)
b+=text(40,222,'FIRST SIGNAL',19,BLUE,'letter-spacing="1"')+text(430,222,'REPEATED GATE',19,BLUE,'letter-spacing="1"')
b+=text(40,290,'6/6',64,TEAL,'font-weight="700"')+text(430,290,'12/15',64,TEAL,'font-weight="700"')
b+=text(40,326,'candidate scenarios passed',21,BLUE)+text(430,326,'candidate runs passed',21,BLUE)
b+=line(365,249,397,249,BLUE,'stroke-width="2"')+f'<path d="M389 242 L397 249 L389 256" fill="none" stroke="{BLUE}" stroke-width="2"/>'
for i in range(6):
 b+=f'<rect x="{40+i*43}" y="352" width="31" height="31" rx="6" fill="{TEAL}"/>'
for i in range(15):
 xx=430+(i%5)*43; yy=352+(i//5)*43
 b+=f'<rect x="{xx}" y="{yy}" width="31" height="31" rx="6" fill="{TEAL if i<12 else "#352f43"}" stroke="{TEAL if i<12 else "#df9ea9"}"/>'
 if i>=12:b+=line(xx+9,yy+9,xx+22,yy+22,'#df9ea9','stroke-width="2"')+line(xx+22,yy+9,xx+9,yy+22,'#df9ea9','stroke-width="2"')
b+=text(40,509,'A promising start earned another test—not a release.',25)
b+=text(40,547,'Separate test sets · tiles grouped by outcome',20,BLUE)
save('article-lead.svg','A passing score was only the beginning','Initial candidate passed six of six scenarios. In a separate repeated gate it passed twelve of fifteen runs. Tiles are grouped by outcome, not chronology. A promising start earned further testing, not a release.',580,b)
