"""Auditable summaries using row-weighted means and evaluation counts."""
import json
import pandas as pd
from generate_evaluation_data import ROOT

def main():
    df=pd.read_csv(ROOT/'data/evaluation_data_clean.csv')
    j=pd.read_csv(ROOT/'data/judge_agreement_data.csv')
    cat=df.groupby('category').score.agg(['count','mean','median','min','max']).sort_values('mean',ascending=False)
    cat.to_csv(ROOT/'data/category_summary.csv')
    df.groupby(['category','model_version']).score.agg(['count','mean','median']).to_csv(ROOT/'data/model_category_summary.csv')
    df.groupby('score_range').size().rename('evaluation_count').to_csv(ROOT/'data/score_distribution.csv')
    j.groupby('category').agg(evaluation_count=('agreement','size'),agreement_rate=('agreement','mean'),
        average_difference=('score_difference','mean')).to_csv(ROOT/'data/judge_category_summary.csv')
    stats={'synthetic':True,'evaluations':len(df),'average_score':round(float(df.score.mean()),4),
        'median_score':round(float(df.score.median()),4),'target_rate':round(float(df.meets_target.mean()),6),
        'target_score':80,'strongest_category':cat.index[0],'weakest_category':cat.index[-1],
        'agreement_rate':round(float(j.agreement.mean()),6),'average_judge_difference':round(float(j.score_difference.mean()),4),
        'best_simulated_candidate':df.groupby('model_version').score.mean().idxmax(),
        'dates':[df.date.min(),df.date.max()]}
    (ROOT/'docs/summary_metrics.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
