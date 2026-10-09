"""Author Tableau 2026.2 XML with file-based data and package relative CSV paths.

XML/ZIP checks do not prove that Tableau can render it. Open and re-save in
Tableau Desktop before submitting; see docs/tableau_open_and_verify.md.
"""
from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile, ZIP_DEFLATED
import uuid
import pandas as pd
from lxml import etree as E
from generate_evaluation_data import ROOT

USER='http://www.tableausoftware.com/xml/user'
def tag(p,t,text=None,**attrs):
    el=E.SubElement(p,t,**{k.replace('_','-'):str(v) for k,v in attrs.items()})
    if text is not None:el.text=str(text)
    return el
def sid(p):tag(p,'simple-id',uuid='{'+str(uuid.uuid5(uuid.NAMESPACE_URL,E.tostring(p).decode())).upper()+'}')
def formatted(p,content,size=13,color='#edf5ff'):
    f=tag(p,'formatted-text');tag(f,'run',content,fontname='Arial',fontsize=size,fontcolor=color)
def style(p,rules):
    s=tag(p,'style')
    for element,items in rules.items():
        r=tag(s,'style-rule',element=element)
        for key,value in items.items():tag(r,'format',attr=key,value=value)
    return s
def column(name,datatype,role,type_,caption=None):
    e=E.Element('column',name=f'[{name}]',datatype=datatype,role=role,type=type_)
    if caption:e.set('caption',caption)
    if datatype=='real':e.set('default-format','n1')
    if name=='agreement' or name=='meets_target':e.set('default-format','p1')
    return e
def ci(name,agg='None',kind='nominal'):
    suffix={'nominal':'nk','ordinal':'ok','quantitative':'qk'}[kind]
    return {'column':f'[{name}]','name':f'[{agg.lower()}:{name}:{suffix}]',
        'derivation':agg,'pivot':'key','type':kind}
def q(ds,instance):return f'[{ds}].'+instance['name']

def build(kind):
    judge=kind=='judge'
    csv='judge_agreement_data.csv' if judge else 'evaluation_data_clean.csv'
    filename='judge_agreement_dashboard' if judge else 'evaluation_score_dashboard'
    dsname='lab.judges' if judge else 'lab.evaluations'
    caption='Synthetic judge comparisons' if judge else 'Synthetic model evaluations'
    dashboard='Judge Agreement Analysis Dashboard' if judge else 'Model Evaluation Score Dashboard'
    data=pd.read_csv(ROOT/'data'/csv)
    fields={}
    for name in data.columns:
        if name=='date':dt,role,k='date','dimension','quantitative'
        elif name in ['evaluation_id','example_id']:dt,role,k='integer','dimension','nominal'
        elif name in ['score_bin','difference_bin']:dt,role,k='integer','dimension','ordinal'
        elif pd.api.types.is_numeric_dtype(data[name]):dt,role,k='real','measure','quantitative'
        else:dt,role,k='string','dimension','nominal'
        fields[name]=column(name,dt,role,k,name.replace('_',' ').title())
    fields['row_count']=column('row_count','integer','measure','quantitative','Evaluations')
    tag(fields['row_count'],'calculation',**{'class':'tableau','formula':'1'})
    wb=E.Element('workbook',nsmap={'user':USER},version='26.2',**{'original-version':'26.2',
        'source-build':'0.0.0 (0000.0.0.0)','source-platform':'mac'})
    tag(tag(wb,'document-format-change-manifest'),'ManifestByVersion')
    source=tag(tag(wb,'datasources'),'datasource',caption=caption,name=dsname,version='26.2',inline='true')
    conn=tag(source,'connection',**{'class':'textscan','directory':'../data','filename':csv,
        'separator':',','header':'yes','charset':'UTF-8','locale':'en_US'})
    relation=tag(conn,'relation',name=csv,table=f'[{csv}]',type='table')
    cols=tag(relation,'columns',header='yes',**{'separator':',','locale':'en_US'})
    for ordinal,(name,f) in enumerate(fields.items()):
        if name!='row_count':tag(cols,'column',name=name,datatype=f.get('datatype'),ordinal=ordinal)
    metadata=tag(conn,'metadata-records')
    for ordinal,(name,f) in enumerate(fields.items()):
        if name=='row_count':continue
        m=tag(metadata,'metadata-record',**{'class':'column'})
        for k,v in [('remote-name',name),('remote-type',{'real':5,'integer':3,'string':129,'date':7}[f.get('datatype')]),
                    ('local-name',f'[{name}]'),('parent-name',f'[{csv}]'),('remote-alias',name),
                    ('ordinal',ordinal),('local-type',f.get('datatype')),
                    ('aggregation','Sum' if f.get('role')=='measure' else 'Count'),('contains-null','false')]:tag(m,k,v)
    tag(source,'aliases',enabled='yes')
    for f in fields.values():source.append(deepcopy(f))
    filter_instances=[ci('model_version'),ci('category'),ci('date','None','quantitative')]
    def deps(p,instances):
        d=tag(p,'datasource-dependencies',datasource=dsname)
        used=list(dict.fromkeys([i['column'][1:-1] for i in instances]))
        for name in used:d.append(deepcopy(fields[name]))
        for i in {i['name']:i for i in instances}.values():tag(d,'column-instance',**i)
        return d
    def links(p):tag(tag(p,'datasources'),'datasource',caption=caption,name=dsname)
    def filters(p):
        for group,inst in enumerate(filter_instances,1):
            f=tag(p,'filter',column=q(dsname,inst),filter_group=group,
                  **{'class':'quantitative' if group==3 else 'categorical'})
            if group==3:tag(f,'min',f'#{data.date.min()}#');tag(f,'max',f'#{data.date.max()}#')
            else:tag(f,'groupfilter',function='level-members',level=q(dsname,inst))
    shared=tag(tag(wb,'shared-views'),'shared-view',name='Global Lab Filters')
    links(shared);deps(shared,filter_instances);filters(shared)
    worksheets=tag(wb,'worksheets')
    sheet_names=[]
    def sheet(name,x=None,y=None,mark='Bar',color=None,text=None,detail=None,sort=False,ref=None,trend=False):
        sheet_names.append(name)
        w=tag(worksheets,'worksheet',name=name)
        options=tag(w,'layout-options');formatted(tag(options,'title'),name,16)
        table=tag(w,'table');view=tag(table,'view');links(view)
        instances=[i for i in [x,y,color,text,detail,*filter_instances] if i]
        deps(view,instances);filters(view)
        if sort:
            sorts=tag(view,'shelf-sorts')
            tag(sorts,'shelf-sort-v2',dimension_to_sort=q(dsname,y),direction='DESC',
                measure_to_sort_by=q(dsname,x),shelf='rows')
        tag(view,'aggregation',value='true')
        style(table,{'table':{'font-family':'Arial','font-size':'11','color':'#edf5ff',
            'background-color':'#10243d'},'pane':{'background-color':'#10243d'}})
        pane=tag(tag(table,'panes'),'pane',selection_relaxation_option='selection-relaxation-allow')
        tag(tag(pane,'view'),'breakdown',value='auto');tag(pane,'mark',**{'class':mark})
        enc=tag(pane,'encodings')
        for key,inst in [('color',color),('text',text),('lod',detail)]:
            if inst:tag(enc,key,column=q(dsname,inst))
        if trend:tag(pane,'trendline',enabled='true',fit='linear',exclude_intercept='false',
            enable_confidence_bands='false',exclude_color='true',enable_instant_analytics='false',enable_tooltips='false')
        if ref:tag(pane,'reference-line',id='ref1',axis_column=q(dsname,x),value_column=q(dsname,x),
            scope='per-table',label_type='custom',label=ref['label'],z_order=1,formula=ref['formula'],
            tooltip_type='none',enable_instant_analytics='false',**({'value':str(ref['value'])} if 'value' in ref else {}))
        style(pane,{'mark':{'color':'#70c1ff','mark-labels-show':'true' if text else 'false',
            'mark-labels-cull':'true','font-size':'28' if mark=='Text' else '11','size':'0.7'}})
        tag(table,'rows',q(dsname,y) if y else '')
        tag(table,'cols',q(dsname,x) if x else '')
        sid(w)
    count=ci('row_count','Sum','quantitative')
    category=ci('category');model=ci('model_version')
    if judge:
        rate=ci('agreement','Avg','quantitative');gap=ci('score_difference','Avg','quantitative')
        sheet('Agreement Rate',mark='Text',text=rate)
        sheet('Average Score Gap',mark='Text',text=gap)
        sheet('Compared Evaluations',mark='Text',text=count)
        sheet('Agreement by Category',x=rate,y=category,color=rate,text=rate,sort=True)
        sheet('Judge Score Differences',x=ci('difference_range'),y=count)
        sheet('Judge Comparison',x=ci('judge_1_score','Avg','quantitative'),
              y=ci('judge_2_score','Avg','quantitative'),mark='Circle',color=category,
              detail=ci('evaluation_id'),trend=True)
        charts=['Agreement by Category','Judge Score Differences','Judge Comparison']
        kpis=['Agreement Rate','Average Score Gap','Compared Evaluations']
    else:
        score=ci('score','Avg','quantitative')
        sheet('Average Quality Score',mark='Text',text=score)
        sheet('Total Evaluations',mark='Text',text=count)
        sheet('Scores At Or Above 80',mark='Text',text=ci('meets_target','Avg','quantitative'))
        sheet('Score Distribution',x=ci('score_range'),y=count)
        sheet('Scores by Category',x=ci('score_range'),y=category,mark='Square',color=count,text=count)
        sheet('Category Comparison',x=score,y=category,color=score,text=score,sort=True,
              ref={'formula':'average','label':'Average of displayed category means'})
        # This heatmap complements, rather than replaces, the category distribution.
        sheet('Candidate Comparison',x=model,y=category,mark='Square',color=score,text=score)
        charts=['Score Distribution','Scores by Category','Category Comparison','Candidate Comparison']
        kpis=['Average Quality Score','Total Evaluations','Scores At Or Above 80']
    d=tag(tag(wb,'dashboards'),'dashboard',name=dashboard)
    style(d,{'dashboard':{'background-color':'#071527'}})
    tag(d,'size',maxheight='950',maxwidth='1400',minheight='950',minwidth='1400')
    zones=tag(d,'zones');zone_id=0
    def zone(x,y,w,h,**attrs):
        nonlocal zone_id
        zone_id+=1
        return tag(zones,'zone',x=x,y=y,w=w,h=h,id=zone_id,**attrs)
    z=zone(1500,1000,97000,6500,type_v2='text');formatted(z,dashboard+' | Walid Barakat',24)
    z=zone(1500,7500,97000,4500,type_v2='text');formatted(z,
        'SYNTHETIC LAB DATA | '+('Agreement = absolute score difference <= 10 points. Similar ratings do not prove correctness.' if judge else
        'Quality scores: 0-100, higher is better. Target 80 is illustrative. No commercial model claims.'),12,'#ffcc80')
    for i,inst in enumerate(filter_instances):
        zone(1500+i*32000,12500,30000,7000,type_v2='filter',name=charts[0],param=q(dsname,inst),mode='dropdown')
    for i,name in enumerate(kpis):zone(1500+i*32000,20500,30000,12500,name=name,show_title='true')
    if judge:
        positions=[(1500,35000,47000,27500),(50500,35000,48000,27500),(1500,63500,97000,30000)]
    else:
        positions=[(1500,35000,47000,28500),(50500,35000,48000,28500),
                   (1500,65000,47000,28500),(50500,65000,48000,28500)]
    for name,pos in zip(charts,positions):zone(*pos,name=name,show_title='true')
    z=zone(1500,95000,97000,4500,type_v2='text');formatted(z,
        'Use model, category and date filters to explore quality. All records are simulated for this lab; no real model claims.',11,'#adc3dc')
    sid(d)
    windows=tag(wb,'windows',saved_dpi_scale_factor='1.0')
    for name in sheet_names:
        w=tag(windows,'window',name=name,**{'class':'worksheet'})
        tag(w,'cards')
        viewpoint=tag(w,'viewpoint',name=name);tag(viewpoint,'zoom',type='entire-view');sid(w)
    w=tag(windows,'window',name=dashboard,maximized='true',**{'class':'dashboard'})
    vp=tag(w,'viewpoints')
    for name in sheet_names:tag(vp,'viewpoint',name=name)
    tag(w,'active',id=7);sid(w)
    explain=tag(wb,'explain-data',enabled_for_viewer='false',extreme_values_enabled_for_all='false')
    tag(explain,'explanation-types')
    tag(wb,'workbook-optimizer')
    directory=ROOT/'tableau';directory.mkdir(exist_ok=True)
    twb=directory/(filename+'.twb')
    twb.write_bytes(E.tostring(wb,xml_declaration=True,encoding='UTF-8',pretty_print=True))
    # Packaged version changes the connection to its embedded relative path.
    packed=deepcopy(wb);packed.find('.//connection').set('directory','Data')
    with ZipFile(ROOT/(filename+'.twbx'),'w',ZIP_DEFLATED) as z:
        z.writestr(filename+'.twb',E.tostring(packed,xml_declaration=True,encoding='UTF-8',pretty_print=True))
        z.write(ROOT/'data'/csv,'Data/'+csv)
    print(filename+'.twbx',f'({len(sheet_names)} sheets; native application validation pending)')

if __name__=='__main__':
    build('quality');build('judge')
