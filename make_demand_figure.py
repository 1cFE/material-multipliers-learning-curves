#!/usr/bin/env python3
"""Reproducible, wholly hypothetical FOAK/NOAK demand illustration.

Python 3 + Pillow. No empirical fusion estimates or external datasets.
"""
from pathlib import Path
from html import escape
import csv
import json
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FIGS, DATA = ROOT/'figs', ROOT/'data'
FIGS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)
W, H, SCALE = 1200, 1270, 3
INK, MUTED, GRID = '#18354A', '#596875', '#DEE5E9'
FONT_DIR = Path('/System/Library/Fonts/Supplemental')
if not (FONT_DIR / 'Arial.ttf').exists():
    FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
REG = FONT_DIR / ('Arial.ttf' if (FONT_DIR/'Arial.ttf').exists() else 'DejaVuSans.ttf')
BOLD = FONT_DIR / ('Arial Bold.ttf' if (FONT_DIR/'Arial Bold.ttf').exists() else 'DejaVuSans-Bold.ttf')
DESIGNS = [
    dict(id='A', label='Lower starting cost', foak=110, floor=65, rate=.20, color='#147D77'),
    dict(id='B', label='Higher start, faster learning', foak=220, floor=35, rate=.20, color='#2C66A2'),
    dict(id='C', label='Higher start, slower learning', foak=220, floor=35, rate=.15, color='#BA562E'),
]
MW, CF, YEARS = 100, .90, 20
CONTRACT_MWH = MW * CF * 8760 * YEARS

def cost(d, n):
    return max(d['floor'], d['foak']*(1-d['rate'])**math.log2(n))

def willingness(n):
    return 240 if n <= 4 else 140 if n <= 16 else 80

def rows_for(d):
    total = 0.0
    rows = []
    for n in range(1,4097):
        c, p = cost(d,n), willingness(n)
        topup=max(0,c-p)
        support=topup*CONTRACT_MWH
        total+=support
        rows.append(dict(scenario=d['id'], plant=n, lcoe_usd_per_mwh=c,
                         willingness_usd_per_mwh=p, additional_support_usd_per_mwh=topup,
                         contracted_mwh=CONTRACT_MWH, plant_contract_support_usd=support,
                         cumulative_contract_support_usd=total))
    return rows

class Scene:
    def __init__(self):
        self.im=Image.new('RGB',(W*SCALE,H*SCALE),'white')
        self.draw=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hypothetical FOAK to NOAK costs and demand support">','<rect width="100%" height="100%" fill="white"/>']
    def text(self,x,y,t,size=18,color=INK,bold=False,anchor='start'):
        self.svg.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,DejaVu Sans,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}">{escape(t)}</text>')
        self.draw.text((x*SCALE,y*SCALE),t,font=ImageFont.truetype(str(BOLD if bold else REG),round(size*SCALE)),fill=color,anchor={'start':'ls','middle':'ms','end':'rs'}[anchor])
    def line(self,pts,color=GRID,width=1,dash=None):
        xy=' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)
        dashattr=f' stroke-dasharray="{dash[0]},{dash[1]}"' if dash else ''
        self.svg.append(f'<polyline points="{xy}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"{dashattr}/>')
        if not dash:
            self.draw.line([(round(x*SCALE),round(y*SCALE)) for x,y in pts],fill=color,width=max(1,round(width*SCALE)),joint='curve')
            return
        phase=0.0
        for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
            length=math.hypot(x1-x0,y1-y0); pos=0.0
            while pos<length-1e-8:
                cycle=phase%sum(dash); visible=cycle<dash[0]
                distance=(dash[0]-cycle) if visible else sum(dash)-cycle
                step=min(length-pos,max(distance,1e-7))
                if visible:
                    a,b=pos/length,(pos+step)/length
                    self.draw.line([((x0+(x1-x0)*a)*SCALE,(y0+(y1-y0)*a)*SCALE),((x0+(x1-x0)*b)*SCALE,(y0+(y1-y0)*b)*SCALE)],fill=color,width=max(1,round(width*SCALE)))
                pos+=step; phase+=step
    def rect(self,x,y,w,h,fill):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
        self.draw.rectangle((x*SCALE,y*SCALE,(x+w)*SCALE,(y+h)*SCALE),fill=fill)
    def circle(self,x,y,r,color,fill='white',width=2):
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{color}" stroke-width="{width}" fill="{fill}"/>')
        self.draw.ellipse(((x-r)*SCALE,(y-r)*SCALE,(x+r)*SCALE,(y+r)*SCALE),fill=fill,outline=color,width=round(width*SCALE))
    def save(self):
        self.im.save(FIGS/'fig1_demand_support.png',dpi=(300,300))
        (FIGS/'fig1_demand_support.svg').write_text('\n'.join(self.svg+['</svg>'])+'\n')


def main():
    allrows=[]; summary=[]
    for d in DESIGNS:
        rows=rows_for(d); allrows+=rows
        comp=next(r['plant'] for r in rows if r['lcoe_usd_per_mwh']<=80)
        mature=next(r['plant'] for r in rows if r['lcoe_usd_per_mwh']<=d['floor'])
        failure=next((r['plant'] for r in rows if r['additional_support_usd_per_mwh']>0),None)
        d.update(rows=rows, competitive=comp,mature=mature,stop=None if failure is None else failure-1)
        summary.append(dict(scenario=d['id'],description=d['label'],foak_usd_per_mwh=d['foak'],
                            assumed_noak_floor_usd_per_mwh=d['floor'],total_lcoe_learning_rate=d['rate'],
                            last_unassisted_plant=d['stop'] or 'no stall',first_competitive_plant=comp,
                            first_plant_at_assumed_noak_floor=mature,
                            additional_contract_support_usd=rows[comp-1]['cumulative_contract_support_usd']))
    for name,rows in [('fig1_plant_costs_and_support.csv',allrows),('fig1_scenario_summary.csv',summary)]:
        with (DATA/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    market=[dict(first_plant=1,last_plant=4,maximum_price_usd_per_mwh=240),dict(first_plant=5,last_plant=16,maximum_price_usd_per_mwh=140),dict(first_plant=17,last_plant='unlimited in this model',maximum_price_usd_per_mwh=80)]
    with (DATA/'fig1_demand_assumptions.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=market[0].keys());w.writeheader();w.writerows(market)
    s=Scene()
    s.text(65,48,'A lower NOAK cost may never be achieved',32,bold=True)
    s.text(65,81,'Hypothetical costs and demand. Each design faces the same market independently.',19,MUTED)
    for i,d in enumerate(DESIGNS):
        x=65+i*370
        s.rect(x,109,345,93,'#F4F7F8');s.rect(x,109,5,93,d['color'])
        s.text(x+15,135,f"{d['id']}  {d['label']}",18,d['color'],True)
        s.text(x+15,161,f"${d['foak']} FOAK → ${d['floor']} mature NOAK",18)
        s.text(x+15,185,f"{d['rate']:.0%} cost reduction per doubling",16,MUTED)
    s.text(65,240,'1  Limited early demand can stop deployment',24,bold=True)
    left,right,top,bottom=100,925,285,630
    x=lambda n:left+(right-left)*math.log2(n)/12
    y=lambda c:bottom-(bottom-top)*c/260
    s.text(left,274,'Electricity cost / customer willingness to pay ($/MWh)',16,MUTED)
    for v in [0,40,80,120,160,200,240]:
        s.line([(left,y(v)),(right,y(v))]);s.text(left-12,y(v)+6,str(v),16,MUTED,anchor='end')
    for n in [1,4,16,64,256,1024,4096]:
        s.line([(x(n),top),(x(n),bottom)],'#EDF0F2')
        s.text(x(n),bottom+25,'1 (FOAK)' if n==1 else f'{n:,}',16,MUTED,anchor='middle')
    # Demand steps are placed between integer plant commitments.
    market_pts=[(x(1),y(240)),(x(4.5),y(240)),(x(4.5),y(140)),(x(16.5),y(140)),(x(16.5),y(80)),(right,y(80))]
    s.line(market_pts,'#78848D',2.5)
    s.text(x(1.12),y(240)-13,'4 buyers at $240',15,MUTED)
    s.line([(x(13),y(140)),(x(21),y(140)-29),(x(23),y(140)-29)],'#78848D',1.3)
    s.text(x(24),y(140)-24,'12 more at $140',15,MUTED)
    s.text(x(65),y(80)-13,'Broad market at $80',16,MUTED)
    for d in DESIGNS:
        # Evaluate continuous curve only for display; support uses discrete plants.
        points=[(x(2**(12*i/1200)),y(cost(d,2**(12*i/1200)))) for i in range(1201)]
        if d['stop']:
            stop=d['stop']; cut=int(math.log2(stop)/12*1200)
            s.line(points[:cut+1],d['color'],3.7)
            s.line(points[cut:],d['color'],3.3,(8,6))
            s.circle(x(stop),y(cost(d,stop)),6,d['color'],d['color'])
        else:s.line(points,d['color'],3.7)
    # Distinct failure labels refer to the last financeable plant.
    c=DESIGNS[2];cx,cy=x(c['stop']),y(cost(c,c['stop']))
    s.line([(cx,cy-8),(cx,cy-45),(cx+45,cy-45)],c['color'],1.5)
    s.text(cx+50,cy-40,'C stops after 4',18,c['color'],True)
    b=DESIGNS[1];bx,by=x(b['stop']),y(cost(b,b['stop']))
    s.line([(bx+7,by),(bx+40,604),(bx+116,604)],b['color'],1.5)
    s.text(bx+121,610,'B stops after 16',18,b['color'],True)
    s.text(right+16,y(65)+4,'A: $65',20,DESIGNS[0]['color'],True)
    s.text(right+16,y(35)+4,'B / C: $35',20,INK,True)
    s.text(right+16,y(35)+27,'Assumed NOAK',15,MUTED)
    s.text((left+right)/2,685,'Cumulative plants built (log scale; each doubling adds production experience)',17,MUTED,anchor='middle')
    s.line([(100,718),(143,718)],INK,3.5);s.text(154,724,'Deployable without additional support',17)
    s.line([(555,718),(598,718)],INK,3.3,(8,6));s.text(610,724,'Unrealized path after demand runs out',17)
    s.text(65,786,'2  Demand support can make the stalled paths feasible',24,bold=True)
    left,right,top,bottom=100,925,840,1092
    x2=lambda n:left+(right-left)*math.log2(n)/7
    y2=lambda bn:bottom-(bottom-top)*bn/12.5
    s.text(left,823,'Cumulative additional contract support ($ billions, undiscounted)',16,MUTED)
    for v in [0,3,6,9,12]:
        s.line([(left,y2(v)),(right,y2(v))]);s.text(left-12,y2(v)+6,str(v),16,MUTED,anchor='end')
    for n in [1,4,16,64,128]:
        s.line([(x2(n),top),(x2(n),bottom)],'#EDF0F2');s.text(x2(n),bottom+26,str(n),16,MUTED,anchor='middle')
    for d in DESIGNS:
        if d['id']=='A':continue
        pts=[(x2(r['plant']),y2(r['cumulative_contract_support_usd']/1e9)) for r in d['rows'][:128]]
        s.line(pts,d['color'],3.7)
        n=d['competitive']; total=d['rows'][n-1]['cumulative_contract_support_usd']/1e9
        s.circle(x2(n),y2(total),5,d['color'],d['color'])
        if d['id']=='B':
            s.line([(x2(n),y2(total)-7),(x2(n),y2(total)-40),(x2(n)+66,y2(total)-40)],d['color'],1.5)
            s.text(x2(n)+74,y2(total)-36,'Competitive at plant 24',17,d['color'],True)
        else:
            s.text(x2(n)-12,y2(total)-15,'Competitive at plant 75',17,d['color'],True,anchor='end')
    s.text(right+16,y2(11.196)+6,'C: $11.2bn',21,DESIGNS[2]['color'],True)
    s.text(right+16,y2(.4466)+5,'B: $0.45bn',21,DESIGNS[1]['color'],True)
    s.text((left+right)/2,1147,'Cumulative plants built with the required demand support',17,MUTED,anchor='middle')
    s.text(65,1193,'A needs no contract-price top-up. Support ends before B or C reaches its NOAK floor.',18,bold=True)
    s.text(65,1222,'Each plant: 100 MW net, 90% capacity factor, 20-year flat-price contract. Constant 2025 dollars.',16,MUTED)
    s.text(65,1248,'Chosen total-LCOE learning curves stop at an assumed floor. These are illustrations, not fusion forecasts.',16,MUTED)
    s.save()
    expected=[(3,6,None,0),(24,302,16,.4466065705720344),(75,2541,4,11.196068355992967)]
    for d,(comp,mature,stop,bn) in zip(DESIGNS,expected):
        assert (d['competitive'],d['mature'],d['stop'])==(comp,mature,stop)
        assert math.isclose(d['rows'][comp-1]['cumulative_contract_support_usd']/1e9,bn,abs_tol=1e-10)
        assert all(cost(d,n+1)<=cost(d,n) for n in range(1,4096))
        assert all(r['additional_support_usd_per_mwh']==0 for r in d['rows'][comp-1:])
    funded=[r['plant'] for r in DESIGNS[2]['rows'] if r['additional_support_usd_per_mwh']>0]
    assert funded==[5,6]+list(range(17,75))
    (DATA/'fig1_model_validation.json').write_text(json.dumps(dict(all_checks_passed=True,contracted_mwh_per_plant=CONTRACT_MWH,scenarios=summary,scenario_C_support_plants=funded),indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
