#!/usr/bin/env python3
"""Rebuild the PNG/SVG figures and CSVs relative to this file.

Requires Python 3 and Pillow. SVG geometry is written directly, with the same
coordinates rendered into 300 dpi PNGs by Pillow. Figure 2 contains sourced cases;
Figures 3–5 are chosen illustrations or screening scenarios; Figure 6 contains
four published IRENA endpoints. Component scenario ranges are not data.
"""
from pathlib import Path
from html import escape
import csv
import json
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FIGS, DATA = ROOT / 'figs', ROOT / 'data'
FIGS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)
INK, MUTED, GRID = '#18354A', '#586777', '#E2E7EB'
COLORS = ('#176A8A', '#C6612C', '#66794B')
IRENA_URL = 'https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_Summary_2025.pdf'
FONT_CANDIDATES = [
    ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
    ('/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'),
]
FONTS = next((pair for pair in FONT_CANDIDATES if all(Path(x).exists() for x in pair)), None)
SCALE = 3

class Figure:
    def __init__(self, number, kind, title, subtitle):
        self.image = Image.new('RGB', (1000*SCALE, 600*SCALE), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600">', '<rect width="1000" height="600" fill="white"/>']
        self.text(100, 29, f'FIGURE {number}  /  {kind}', 14, MUTED, bold=True)
        self.text(100, 67, title, 28, bold=True)
        self.text(100, 95, subtitle, 18, MUTED)

    def font(self, size, bold=False):
        if FONTS:
            return ImageFont.truetype(FONTS[int(bold)], round(size*SCALE))
        return ImageFont.load_default(size=round(size*SCALE))

    def text(self, x, y, label, size=16, color=INK, anchor='start', bold=False, rotate=None):
        svg_rotate = f' transform="rotate({rotate} {x} {y})"' if rotate else ''
        weight = 'bold' if bold else 'normal'
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Arial,DejaVu Sans,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{svg_rotate}>{escape(label)}</text>')
        font = self.font(size, bold)
        if rotate:
            bbox = font.getbbox(label)
            w, h = bbox[2]-bbox[0]+12*SCALE, bbox[3]-bbox[1]+12*SCALE
            layer = Image.new('RGBA', (w, h), (255,255,255,0))
            ImageDraw.Draw(layer).text((6*SCALE-bbox[0],6*SCALE-bbox[1]),label,font=font,fill=color)
            layer = layer.rotate(-rotate, expand=True)
            self.image.paste(layer,(round(x*SCALE-layer.width/2),round(y*SCALE-layer.height/2)),layer)
        else:
            self.draw.text((round(x*SCALE),round(y*SCALE)),label,font=font,fill=color,
                           anchor={'start':'ls','middle':'ms','end':'rs'}[anchor])

    def line(self, points, color=GRID, width=1, dash=None):
        pts = ' '.join(f'{x:.3f},{y:.3f}' for x,y in points)
        attr = f' stroke-dasharray="{dash[0]},{dash[1]}"' if dash else ''
        self.svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{attr}/>')
        if not dash:
            self.draw.line([(round(x*SCALE),round(y*SCALE)) for x,y in points],fill=color,width=round(width*SCALE),joint='curve')
        else:
            phase = 0.0
            for (x0,y0),(x1,y1) in zip(points,points[1:]):
                length=math.hypot(x1-x0,y1-y0)
                if not length: continue
                pos=0.0
                while pos<length-1e-9:
                    cycle=phase % sum(dash)
                    visible=cycle<dash[0]
                    left=(dash[0]-cycle) if visible else (sum(dash)-cycle)
                    step=min(length-pos,left if left>1e-9 else 1e-6)
                    if visible:
                        a,b=pos/length,(pos+step)/length
                        self.draw.line([(round((x0+(x1-x0)*a)*SCALE),round((y0+(y1-y0)*a)*SCALE)),(round((x0+(x1-x0)*b)*SCALE),round((y0+(y1-y0)*b)*SCALE))],fill=color,width=round(width*SCALE))
                    pos+=step
                    phase+=step

    def rect(self,x,y,w,h,color):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
        self.draw.rectangle((round(x*SCALE),round(y*SCALE),round((x+w)*SCALE),round((y+h)*SCALE)),fill=color)

    def dot(self,x,y,r,color):
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
        self.draw.ellipse(((x-r)*SCALE,(y-r)*SCALE,(x+r)*SCALE,(y+r)*SCALE),fill=color)

    def footer(self, line):
        self.text(70,578,line,17,MUTED)

    def save(self,stem):
        (FIGS/f'{stem}.svg').write_text('\n'.join(self.svg+['</svg>'])+'\n',encoding='utf-8')
        self.image.save(FIGS/f'{stem}.png',dpi=(300,300))
        print(f'Wrote {stem}.png + .svg')


def write_csv(name,rows):
    with (DATA/name).open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def curve_axes(fig,xlabel,ylabel):
    left,right,top,bottom=100,750,145,435
    x=lambda d:left+(right-left)*d/8
    y=lambda v:bottom-(bottom-top)*v/105
    for value in range(0,101,20):
        fig.line([(left,y(value)),(right,y(value))])
        fig.text(left-15,y(value)+5,str(value),18,MUTED,anchor='end')
    fig.line([(left,top),(left,bottom),(right,bottom)],'#AAB5BF')
    for value in range(9):
        fig.line([(x(value),bottom),(x(value),bottom+4)],'#AAB5BF')
        fig.text(x(value),bottom+23,str(value),18,MUTED,anchor='middle')
    fig.text((left+right)/2,500,xlabel,19,anchor='middle')
    fig.text(33,(top+bottom)/2,ylabel,19,anchor='middle',rotate=-90)
    return x,y


def figure1():
    records=json.loads((DATA/'fig2_source_inputs.json').read_text(encoding='utf-8'))['cases']
    fig=Figure(2,'SOURCED EXAMPLES','Material multipliers in manufactured products',
               "Each ratio retains its source's cost and material boundaries")
    left,right,top,bottom=490,895,137,466
    x=lambda m:left+(right-left)*math.log10(m)/2
    for tick in (1,2,5,10,20,50,100):
        fig.line([(x(tick),top),(x(tick),bottom)],GRID,1)
        fig.text(x(tick),bottom+26,f'{tick}×',18,MUTED,anchor='middle')
    rows=[]
    for record,y in zip(records,(176,289,402)):
        numerator=record['finished_value']
        material=record['material_price']
        m=numerator/material
        display=f'{m:.1f}' if m<10 else f'{m:.0f}'
        color=record['figure_color']
        fig.text(65,y-9,record['figure_label'],22,bold=True)
        fig.text(65,y+17,record['figure_basis'],18,MUTED)
        fig.text(65,y+42,record['figure_source'],16,MUTED)
        fig.line([(left,y),(x(m),y)],color,3)
        fig.dot(x(m),y,6,color)
        fig.rect(x(m)+11,y-17,68,31,'white')
        fig.text(x(m)+17,y+8,f'≈ {display}×',23,color,bold=True)
        rows.append({'case_id':record['case_id'],
                     'technology':record['technology'],
                     'period':record['period'],
                     'finished_cost_or_price':f'{numerator:.12g}',
                     'material_benchmark_value':f'{material:.12g}',
                     'value_units':record['value_units'],
                     'material_multiplier':f'{m:.10f}',
                     'display_multiplier':f'approximately {display}x',
                     'material_value_share_percent':'',
                     'numerator_boundary':record['numerator_boundary'],
                     'material_boundary':record['material_boundary'],
                     'evidence_status':record['evidence_status'],
                     'formula':record['formula'],
                     'source_urls':' | '.join(source['url'] for source in record['sources']),
                     'source_locations':' | '.join(source['location'] for source in record['sources']),
                     'limitations':record['limitations']})
    fig.text((left+right)/2,532,'Cost-to-material ratio (logarithmic scale)',18,anchor='middle')
    fig.footer('Different accounting boundaries. These ratios do not measure removable cost.')
    fig.save('fig2_multiplier_calibration')
    write_csv('fig2_multiplier_calibration.csv',rows)


def figure2():
    fig=Figure(3,'CHOSEN COST SCENARIOS','A floor limits the gains from learning',
               'Same 20% residual learning rate; three different fixed engineering floors')
    x,y=curve_axes(fig,'Cumulative production doublings from the reference','Unit cost index (starts at 100)')
    rows=[]
    for floor,color,dash in zip((10,40,70),COLORS,(None,(9,5),(3,4))):
        costs=[(i/20,floor+(100-floor)*0.8**(i/20)) for i in range(161)]
        fig.line([(x(0),y(floor)),(x(8),y(floor))],color,1,(2,4))
        fig.text(x(0)+12,y(floor)-7,f'Floor {floor}',16,color)
        fig.line([(x(d),y(c)) for d,c in costs],color,3,dash)
        endpoint=costs[-1][1]
        fig.dot(x(8),y(endpoint),4,color)
        fig.text(775,y(endpoint)-3,f'{floor}% floor',21,color,bold=True)
        fig.text(775,y(endpoint)+24,f'Cost {endpoint:.1f}',19,color)
        rows.extend({'doublings':f'{d:.2f}','floor_index':floor,'initial_cost_index':100,
                     'residual_learning_rate':0.2,'cost_index':f'{c:.8f}',
                     'evidence_status':'calculated_chosen_scenario'} for d,c in costs)
    fig.footer('Illustrative curves. Learning applies to cost above the floor; total cost falls more slowly.')
    fig.save('fig3_cost_floors')
    write_csv('fig3_cost_floors.csv',rows)


COMPONENTS = [
    {'component':'HTS magnet','m_min':10,'m_max':100,'r_min':0.10,'r_max':0.20,'region':'A',
     'boundary':'Qualified conductor, winding, joints and supporting structure; refrigerator separate',
     'levels':'cross-industry; cross-fusion; concept-specific',
     'criterion':'Repeated deposition and magnet fabrication retain specified current, stress tolerance and protection',
     'experience_unit':'Qualified tape length or comparable magnet assemblies, modeled separately',
     'source':'https://www.sbir.gov/awards/214121'},
    {'component':'IMG pulser assembly','m_min':10,'m_max':100,'r_min':0.10,'r_max':0.20,'region':'A',
     'boundary':'Capacitors, switches, enclosure, interconnections, assembly and acceptance test',
     'levels':'cross-industry; cross-fusion; concept-specific',
     'criterion':'Repeat brick and module fabrication with demonstrated pulse specification and service life',
     'experience_unit':'Compatible bricks or modules; operating pulses do not count as new production',
     'source':'https://www.nature.com/articles/s41598-024-67774-4'},
    {'component':'IFE laser driver','m_min':10,'m_max':100,'r_min':0.05,'r_max':0.20,'region':'B',
     'boundary':'Pump diodes, gain medium, optics, cooling and optical assembly; target system separate',
     'levels':'cross-industry; cross-fusion; concept-specific',
     'criterion':'Repeat diode and optical assembly with required wavelength, pulse energy, efficiency and life',
     'experience_unit':'Qualified pump components or comparable beamline modules, modeled separately',
     'source':'https://lasers.llnl.gov/sites/lasers/files/2023-11/haefner-ILT-IFE-workshop-2022-1.pdf'},
    {'component':'First-wall or divertor assembly','m_min':10,'m_max':100,'r_min':0.00,'r_max':0.10,'region':'C',
     'boundary':'Armor, heat sink, coolant joints and qualification; replacement costs retained separately',
     'levels':'concept-specific; cross-fusion; cross-industry feedstocks',
     'criterion':'Joining and inspection improvements preserve heat-flux and lifetime requirements',
     'experience_unit':'Qualified assemblies, including manufactured replacements',
     'source':'https://www.iter.org/machine/divertor'},
    {'component':'Vacuum-vessel assembly','m_min':3,'m_max':30,'r_min':0.00,'r_max':0.10,'region':'D',
     'boundary':'Defined sector, ports, welds, inspection and required cooling or shielding; field joints separate',
     'levels':'cross-industry; concept-specific; whole-plant',
     'criterion':'Repeat forming, welding and metrology retain load, confinement and assembly tolerances',
     'experience_unit':'Compatible sectors and operations; site integration modeled separately',
     'source':'https://www.iter.org/machine/vacuum-vessel'},
    {'component':'Conventional steam balance of plant','m_min':2,'m_max':10,'r_min':0.00,'r_max':0.05,'region':'E',
     'boundary':'Conventional turbine-generator and ordinary heat exchange; site and novel sCO2 excluded',
     'levels':'cross-industry; whole-plant',
     'criterion':'Additional supplier improvement beyond maturity already represented in present prices',
     'experience_unit':'Compatible equipment against existing qualified supplier production',
     'source':'https://www.gti.energy/step-demo/step-demo-project/'},
    {'component':'Helium cryogenic equipment','m_min':3,'m_max':30,'r_min':0.00,'r_max':0.10,'region':'D',
     'boundary':'Compressor, cold-box and refrigerator package; site distribution and installation separate',
     'levels':'cross-industry; cross-fusion; concept-specific',
     'criterion':'Repeat helium equipment and integration maintain temperature, transient-load and efficiency requirements',
     'experience_unit':'Qualified helium equipment; LNG volume not automatically transferable',
     'source':'https://www.iter.org/machine/supporting-systems/cryogenics'},
    {'component':'Tritium-processing subsystem','m_min':10,'m_max':100,'r_min':0.00,'r_max':0.10,'region':'C',
     'boundary':'One specified extraction, separation, storage or detritiation function; breeding blanket and fuel inventory excluded',
     'levels':'cross-fusion; concept-specific; cross-industry subcomponents',
     'criterion':'Repeat qualified process assemblies preserve throughput, purity, inventory control and containment',
     'experience_unit':'Compatible process subsystems or operations, not generic complete fuel cycles',
     'source':'https://www.iter.org/machine/supporting-systems/fuelling'},
]


def figure3():
    fig=Figure(4,'AUTHOR-CHOSEN SCREENING BANDS','Component scenarios to test',
               'Illustrative assumptions for eight component classes')
    left,right,top,bottom=105,680,140,440
    x=lambda m:left+(right-left)*math.log10(m)/math.log10(130)
    y=lambda r:bottom-(bottom-top)*r/25
    for m in (1,3,10,30,100):
        fig.line([(x(m),top),(x(m),bottom)])
        fig.text(x(m),bottom+27,f'{m}×',20,MUTED,anchor='middle')
    for rate in (0,5,10,15,20,25):
        fig.line([(left,y(rate)),(right,y(rate))])
        fig.text(left-13,y(rate)+6,f'{rate}%',19,MUTED,anchor='end')
    fig.line([(left,top),(left,bottom),(right,bottom)],'#AAB5BF')
    fig.text((left+right)/2,509,'Assumed material multiplier M (log scale)',20,anchor='middle')
    fig.text(28,(top+bottom)/2,'Residual learning per doubling',20,anchor='middle',rotate=-90)
    groups=[
        ('A',10,100,10,20,'#176A8A',None,'HTS magnet / IMG','10–100×; 10–20%',178,20),
        ('B',10,100,5,20,'#C6612C',(9,5),'IFE laser driver','10–100×; 5–20%',244,15),
        ('C',10,100,0,10,'#66794B',None,'Wall / tritium processing','10–100×; 0–10%',310,10),
        ('D',3,30,0,10,'#775583',(7,4),'Vessel / helium cryo','3–30×; 0–10%',376,7.5),
        ('E',2,10,0,5,'#586777',None,'Steam BOP','2–10×; 0–5%',442,5),
    ]
    # Very light tinted regions retain overlap; colored boundaries carry the exact limits.
    for key,lo,hi,rl,rh,color,dash,label,band,ly,edge_rate in groups:
        rx,ry,rw,rh_px=x(lo),y(rh),x(hi)-x(lo),y(rl)-y(rh)
        fig.svg.append(f'<rect x="{rx:.3f}" y="{ry:.3f}" width="{rw:.3f}" height="{rh_px:.3f}" fill="{color}" fill-opacity="0.045"/>')
        layer=Image.new('RGBA',fig.image.size,(255,255,255,0))
        ImageDraw.Draw(layer).rectangle((round(rx*SCALE),round(ry*SCALE),round((rx+rw)*SCALE),round((ry+rh_px)*SCALE)),fill=tuple(int(color[i:i+2],16) for i in (1,3,5))+(11,))
        fig.image=Image.alpha_composite(fig.image.convert('RGBA'),layer).convert('RGB')
        fig.draw=ImageDraw.Draw(fig.image)
    for key,lo,hi,rl,rh,color,dash,label,band,ly,edge_rate in groups:
        fig.line([(x(lo),y(rl)),(x(lo),y(rh)),(x(hi),y(rh)),(x(hi),y(rl)),(x(lo),y(rl))],color,3,dash)
        # Leader starts on the region boundary and has no point marker.
        fig.line([(x(hi),y(edge_rate)),(697,ly-7),(718,ly-7)],color,1.3)
        fig.text(729,ly,label,20,color,bold=True)
        fig.text(729,ly+25,band,19,color)
    fig.footer('Chosen scenarios, not estimates. Include zero learning; production growth is a separate input.')
    fig.save('fig4_component_plane')
    rows=[]
    for item in COMPONENTS:
        for case in ('screening_band','no_learning_comparator'):
            rows.append({'component':item['component'],'scenario':case,'region_id':item['region'],
                'material_multiplier_min':item['m_min'],'material_multiplier_max':item['m_max'],
                'residual_lr_min':item['r_min'] if case=='screening_band' else 0,
                'residual_lr_max':item['r_max'] if case=='screening_band' else 0,
                'evidence_status':'chosen_scenario','numerical_source':'author_selected_assumption',
                'rate_applies_to':'cost above separately justified engineering floor',
                'account_boundary':item['boundary'],'supply_chain_levels':item['levels'],
                'criterion_to_test':item['criterion'],'experience_unit':item['experience_unit'],
                'reference_production_Q0':'must be specified separately',
                'accessible_doublings_D':'log2(Q/Q0); not estimated here',
                'engineering_floor':'must be justified separately',
                'plant_cost_share':'must be specified separately',
                'mechanism_source_url':item['source']})
    write_csv('fig4_component_plane.csv',rows)


def figure4():
    magnet_share,tape_share,qratio,pratio=.30,.80,.75,.80
    tape=qratio*pratio
    magnet=tape_share*tape+(1-tape_share)
    plant=(1-magnet_share)+magnet_share*magnet
    fig=Figure(5,'CALCULATED EXAMPLE','From tape saving to plant saving',
               'Three cost accounts, each normalized to its own initial value of 100')
    left,right,top,bottom=245,805,150,462
    x=lambda v:left+(right-left)*v/110
    for v in (0,20,40,60,80,100):
        fig.line([(x(v),top),(x(v),bottom)])
        fig.text(x(v),490,str(v),18,MUTED,anchor='middle')
    rows=[]
    for name,new,cy in (('Tape bill',100*tape,205),('Magnet cost',100*magnet,315),('Plant capital',100*plant,425)):
        fig.text(222,cy+6,name,23,anchor='end',bold=True)
        for case,value,offset,color in (('Before',100,-20,'#B5C1CB'),('After',new,20,COLORS[0])):
            fig.rect(left,cy+offset-13,x(value)-left,26,color)
            fig.text(x(value)+10,cy+offset+7,f'{value:g}',20,bold=True)
            rows.append({'account':name,'case':case,'cost_index':f'{value:.8f}',
                         'initial_cost_index':100,'scenario_reduction_fraction':f'{1-new/100:.8f}',
                         'evidence_status':'calculated_chosen_scenario',
                         'normalization':'each account independently normalized to own baseline'})
        fig.text(872,cy+1,f'{100-new:g}%',24,anchor='middle',bold=True)
        fig.text(872,cy+27,'saving',19,anchor='middle')
    for lx,color,label in ((590,'#B5C1CB','Before'),(735,COLORS[0],'After')):
        fig.rect(lx,123,18,15,color)
        fig.text(lx+27,139,label,18,MUTED)
    fig.text((left+right)/2,531,'Cost index (own baseline = 100)',20,anchor='middle')
    fig.footer('Chosen inputs: magnets = 30% of plant capital; tape = 80% of magnet cost. Each baseline = 100.')
    fig.save('fig5_rebco_cost_shares')
    write_csv('fig5_rebco_cost_shares.csv',rows)
    inputs={'initial_magnet_share_of_plant_capital':magnet_share,'initial_tape_share_of_magnet_cost':tape_share,
            'tape_quantity_ratio':qratio,'tape_price_per_meter_ratio':pratio}
    outputs={'tape_bill_ratio':tape,'magnet_cost_ratio':magnet,'plant_capital_ratio':plant,
             'magnet_cost_reduction':1-magnet,'plant_capital_reduction':1-plant}
    write_csv('rebco_worked_example.csv',[{'parameter':key,'value':f'{value:.8f}',
              'evidence_status':'chosen_assumption' if key in inputs else 'calculated_scenario_result'}
              for key,value in {**inputs,**outputs}.items()])


def figure5():
    records=[('Solar PV',2010,0.417),('Solar PV',2024,0.043),('CSP',2010,0.402),('CSP',2024,0.092)]
    values={(technology,year):value*1000 for technology,year,value in records}
    fig=Figure(6,'OBSERVED ENDPOINTS','Solar PV and CSP both became cheaper',
               'Global weighted-average LCOE for newly commissioned plants')
    left,right,top,bottom=150,800,160,440
    x=lambda v:left+(right-left)*v/460
    for v in (0,100,200,300,400):
        fig.line([(x(v),top),(x(v),bottom)])
        fig.text(x(v),470,str(v),19,MUTED,anchor='middle')
    fig.line([(left,bottom),(right,bottom)],'#AAB5BF')
    colors={2010:'#B5C1CB',2024:COLORS[0]}
    for technology,center in (('Solar PV',235),('CSP',365)):
        fig.text(130,center+6,technology,23,anchor='end',bold=True)
        for year,offset in ((2010,-23),(2024,23)):
            value=values[technology,year]
            fig.rect(left,center+offset-15,x(value)-left,30,colors[year])
            fig.text(x(value)+9,center+offset+7,f'{value:.0f}',22,bold=True)
        decline=1-values[technology,2024]/values[technology,2010]
        fig.text(882,center-3,f'{decline:.0%}',28,anchor='middle',bold=True)
        fig.text(882,center+25,'lower',20,anchor='middle')
    for year,lx in ((2010,625),(2024,750)):
        fig.rect(lx,123,18,15,colors[year])
        fig.text(lx+26,140,str(year),18,MUTED)
    fig.text((left+right)/2,517,'Levelized cost of electricity (2024 USD/MWh)',21,anchor='middle')
    fig.footer('Source: IRENA (2025), Table S1. Cohort endpoints; PV and CSP can provide different services.')
    fig.save('fig6_pv_csp_endpoints')
    write_csv('fig6_pv_csp_endpoints.csv',[{'technology':technology,'year':year,
          'lcoe_2024_usd_per_kwh':f'{value:.3f}','lcoe_2024_usd_per_mwh':f'{value*1000:.0f}',
          'evidence_status':'published_observation','source':'IRENA (2025), executive summary, Table S1, p. 4',
          'source_url':IRENA_URL} for technology,year,value in records])


if __name__=='__main__':
    import runpy
    runpy.run_path(str(ROOT/'make_demand_figure.py'), run_name='__main__')
    figure1()
    figure2()
    figure3()
    figure4()
    figure5()
