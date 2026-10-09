"""Fail explicitly on malformed input; retain valid extremes at 0 and 100."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from generate_evaluation_data import ROOT, CATEGORIES, MODELS

def validate_evaluations(df):
    required = {'evaluation_id', 'example_id', 'category', 'score', 'model_version', 'date'}
    assert required <= set(df.columns), f'Missing columns: {required-set(df.columns)}'
    assert len(df) >= 100, 'At least 100 rows required'
    assert not df[list(required)].isna().any().any(), 'Missing critical data'
    assert df.evaluation_id.is_unique, 'Duplicate evaluation IDs'
    assert pd.to_numeric(df.score, errors='coerce').between(0,100).all(), 'Score outside 0-100'
    assert set(df.category) <= set(CATEGORIES), 'Unexpected category'
    assert set(df.model_version) <= set(MODELS), 'Unexpected model'
    parsed = pd.to_datetime(df.date, format='%Y-%m-%d', errors='coerce')
    assert parsed.notna().all(), 'Invalid date'
    assert (parsed.dt.strftime('%Y-%m-%d') == df.date).all(), 'Non-canonical date'
    assert not df.duplicated(['example_id','model_version']).any(), 'Repeated example/model pair'

def main():
    df=pd.read_csv(ROOT/'data/evaluation_data_clean.csv')
    validate_evaluations(df)
    assert (df.score_bin == np.minimum((df.score//10).astype(int)*10,90)).all()
    assert (df.meets_target == (df.score >= 80).astype(int)).all()
    j=pd.read_csv(ROOT/'data/judge_agreement_data.csv')
    assert j.evaluation_id.is_unique and len(j)==len(df)
    for c in ['judge_1_score','judge_2_score']: assert j[c].between(0,100).all()
    difference=(j.judge_1_score-j.judge_2_score).abs().round(2)
    assert np.allclose(j.score_difference,difference)
    assert (j.agreement==(difference<=10).astype(int)).all()
    for c in ['evaluation_id','example_id','category','model_version','date']:
        assert df[c].equals(j[c]), f'Judge records do not match: {c}'
    balanced=df.groupby(['category','model_version']).size().nunique()==1
    report={'status':'passed','synthetic':True,'evaluation_rows':len(df),'judge_rows':len(j),
        'unique_examples':int(df.example_id.nunique()),'categories':int(df.category.nunique()),
        'models':int(df.model_version.nunique()),'days':int(df.date.nunique()),
        'date_min':df.date.min(),'date_max':df.date.max(),'missing_critical_cells':0,
        'duplicate_evaluation_ids':0,'balanced_category_model_counts':bool(balanced),
        'out_of_range_scores':0,'rows_removed':0,'agreement_rule':'rounded score difference <= 10 points'}
    (ROOT/'docs/data_quality_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
