"""Embed both datasets. The preview runs offline without a server or CDN."""
import pandas as pd
from generate_evaluation_data import ROOT

def main():
    template=(ROOT/'scripts/dashboard_template.html').read_text()
    for token,filename in [('__DATA__','evaluation_data_clean.csv'),('__JUDGES__','judge_agreement_data.csv')]:
        template=template.replace(token,pd.read_csv(ROOT/'data'/filename).to_json(orient='records',force_ascii=True))
    out=ROOT/'evaluation_dashboard.html'
    out.write_text(template,encoding='utf-8')
    print(out.name)

if __name__=='__main__':main()
