"""Create a standard notebook and execute its Python cells with a local runner.
No Jupyter kernel execution is claimed; the runner is recorded in metadata.
"""
from pathlib import Path
import contextlib,io,json,sys
from generate_evaluation_data import ROOT

def main():
    cells=[]
    def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(keepends=True)})
    def code(s):cells.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(keepends=True)})
    md('''# Evaluation Dashboard Lab: complete solution notebook
**Walid Barakat | Tableau route | Option B: synthetic data**

This notebook documents the data and calculations behind the communication dashboard. It is not the primary dashboard deliverable. The package includes a main Tableau workbook, the optional judge workbook, an offline HTML preview, documentation and preview images.

**Evidence status:** The Python cells below were executed using a local Python cell runner during preparation. Tableau Desktop, a Jupyter kernel and a full browser session were not available for native end-to-end verification. Before submission, open and re-save the Tableau workbooks, test the filters, capture genuine native screenshots and upload the dedicated lab repository to GitHub.

The source is the uploaded *LAB | Evaluation Dashboard Lab(1).pdf*. No real evaluation export was provided, so Option B is used. None of the scores or generic candidates represents a measured commercial model or the current EU tender agent.
''')
    md('''## 1. Requirements and solution approach
The lab asks for clean evaluation data, at least three charts, model/category/date filters, a stakeholder-friendly native dashboard, a screenshot, brief data-source documentation and a README in a dedicated GitHub repository. Reflection and a judge-agreement dashboard are recommended extras.

| Requirement | Solution |
|---|---|
| Overall score distribution | 10-point band histogram |
| Category distribution | Native category-by-score-band heatmap; preview box plot |
| Category comparison | Sorted average-score bars |
| Additional comparison | Candidate-by-category average-score grid |
| Interactive exploration | Model/category/date filters and preview click-to-filter |
| Judge extension | Agreement-by-category bars, gap histogram, rating-pair scatter |

XML validation is structural evidence, not proof that Tableau can load the workbook. See `docs/requirements_traceability.md` for the exact fulfilment status.
''')
    code(r'''from pathlib import Path
import sys, json
import numpy as np
import pandas as pd

here = Path.cwd()
if (here / 'data').is_dir() and (here / 'scripts').is_dir():
    ROOT = here
elif here.name == 'notebooks' and (here.parent / 'data').is_dir():
    ROOT = here.parent
else:
    raise RuntimeError('Run from the extracted lab folder or its notebooks folder.')
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_evaluation_data import generate
from validate_evaluation_data import validate_evaluations
print('Workspace:', ROOT.name)
''')
    md('''## 2. Generate repeatable data
The generator uses seed 42 and a fixed window from 10 July to 7 October 2026. For each of five categories on each day it creates five examples, and evaluates each for four generic candidates. This gives `90 x 5 x 5 x 4 = 9,000` evaluation rows.

Category score shapes and candidate offsets are simulation assumptions. The candidates share the same example IDs, so the structure supports later paired comparisons, although this notebook does not make statistical or causal claims. Judge scores are simulated around each row's quality score and clipped to 0-100.
''')
    code(r'''raw, clean, judges = generate(seed=42, end_date='2026-10-07')
print('Evaluation records:', len(raw))
print('Distinct examples:', raw.example_id.nunique())
print('Date range:', raw.date.min(), 'to', raw.date.max())
print(raw.head().to_string(index=False))
assert raw.equals(pd.read_csv(ROOT / 'data/evaluation_data.csv'))
assert clean.equals(pd.read_csv(ROOT / 'data/evaluation_data_clean.csv'))
print('Generated data match packaged CSVs.')
''')
    md('''## 3. Clean and validate
Scores remain numeric, IDs are unique and dates use YYYY-MM-DD. No source rows require removal because the generated data already meet the validity rules. Genuine 0 and 100 values are retained. With real data, record each rejected row and its reason instead of silently deleting data.

The validator rejects missing values, out-of-range scores, unknown categories/models, duplicate IDs, repeated example/model pairs and invalid dates. Score flags and bins are recalculated independently below.
''')
    code(r'''validate_evaluations(clean)
assert clean.score.between(0, 100).all()
assert (clean.groupby(['category', 'model_version']).size() == 450).all()
assert (clean.groupby('example_id').model_version.nunique() == 4).all()
assert (clean.meets_target == (clean.score >= 80).astype(int)).all()
expected_bins = np.minimum((clean.score // 10).astype(int) * 10, 90)
assert (clean.score_bin == expected_bins).all()
print(clean.dtypes.to_string())
print('No missing critical values or duplicate evaluation IDs. Zero rows removed.')
print('Balance: 450 rows per category/candidate; four candidates per example.')
''')
    md('''## 4. Calculate communication metrics
Use an evaluation-weighted mean across selected rows. Average scores are not sums and are not percentages of correct answers. The 80-point target is illustrative. Score ranges are lower-inclusive/upper-exclusive, except 90-100 includes 100.

The mean of category means equals the global mean only if their record counts are equal. This dataset is balanced; real data might not be. Keep denominators visible and recompute metrics after filters.
''')
    code(r'''category_summary = clean.groupby('category').score.agg(['count','mean','median','min','max']).sort_values('mean', ascending=False)
print(category_summary.round(2).to_string())
print('\nOverall mean:', round(clean.score.mean(), 4))
print('Median:', clean.score.median())
print('Share at or above 80:', f'{clean.meets_target.mean():.2%}')
histogram = clean.groupby('score_range').size()
assert histogram.sum() == len(clean)
print('\nHistogram counts:')
print(histogram.to_string())
''')
    md('''## 5. Candidate comparison
The following grid is an average per category and candidate. Differences are deliberately generated. Do not use them to choose a real vendor or claim a measured improvement.
''')
    code(r'''comparison = clean.pivot_table(index='category', columns='model_version', values='score', aggfunc='mean')
print(comparison.round(2).to_string())
print('\nCounts:')
print(clean.groupby(['category','model_version']).size().unstack().to_string())
''')
    md('''## 6. Optional judge agreement
Agreement is defined by `abs(judge_1_score - judge_2_score) <= 10`, using the rounded scores in the CSV. The threshold is inclusive. A rating gap of exactly 10 counts as agreement, even though a 10-point histogram band places it in 10-20. A trend or correlation shows association and is not sufficient to establish identical ratings or correctness.
''')
    code(r'''difference = (judges.judge_1_score - judges.judge_2_score).abs().round(2)
assert np.allclose(difference, judges.score_difference)
assert (judges.agreement == (difference <= 10).astype(int)).all()
print('Agreement:', f'{judges.agreement.mean():.2%}')
print('Mean absolute gap:', round(judges.score_difference.mean(), 4))
print('Compared rows:', len(judges))
print('Large disagreements:', int((judges.agreement == 0).sum()))
print(judges.groupby('category').agreement.mean().mul(100).round(2).to_string())
assert list((np.array([9.99,10,10.01]) <= 10).astype(int)) == [1,1,0]
''')
    md('''## 7. Verify interactive filter calculations
These calculations provide known counts to check against both dashboards. Select Candidate A, Reasoning and 7 October 2026: five evaluations should remain, and the same five judge pairs should be visible.
''')
    code(r'''checks = {
    'Unfiltered': clean,
    'Candidate A': clean[clean.model_version == 'Candidate A'],
    'Reasoning': clean[clean.category == 'reasoning'],
    'Candidate A + reasoning': clean[(clean.model_version == 'Candidate A') & (clean.category == 'reasoning')],
    'Candidate A + reasoning + 7 October': clean[(clean.model_version == 'Candidate A') & (clean.category == 'reasoning') & (clean.date == '2026-10-07')]
}
expected = [9000,2250,1800,450,5]
for (name, selection), count in zip(checks.items(), expected):
    assert len(selection) == count
    assert judges.evaluation_id.isin(selection.evaluation_id).sum() == count
    print(f'{name}: {len(selection):,}; average {selection.score.mean():.2f}')
''')
    md('''## 8. Rebuild dashboard artifacts
The following calls recreate the HTML and native Tableau workbook files. Re-running them will replace generated files, so preserve a separately verified Tableau edit before rebuilding. The native files use relative CSV paths; TWBX versions embed the CSV. The preview is self-contained and uses no online JavaScript library.
''')
    code(r'''import build_html_dashboard
import build_tableau_workbooks
build_html_dashboard.main()
build_tableau_workbooks.build('quality')
build_tableau_workbooks.build('judge')
print('Tableau application checks and native screenshots still required.')
''')
    md('''## 9. Stakeholder interpretation
The generated data suggest reviewing reasoning examples first, because this category has the lowest simulated average. Instruction following is stronger in the simulation, but its spread still matters. Filter by candidate to see whether a weakness is widespread. Review score-gap cases to clarify ambiguous rubric instructions.

For an EU tender agent, a real rubric could evaluate reasoning about bid/no-bid, source-grounded knowledge, structured output, instruction following and appropriate source/API calls. These mappings are proposals, not claims about current project results. To measure business value, replace synthetic records with held-out real evaluations and track quality alongside cost and review time.

## 10. Submission checklist
- Open and re-save both TWBX files in Tableau Desktop 2026.2 or later.
- Apply filters to all relevant worksheets, including cards, and verify native cross-filter actions.
- Check counts using section 7; reset before capturing screenshots.
- Capture `dashboard_screenshot.png` and the optional `judge_agreement_screenshot.png` from Tableau.
- Review `data_source.md` and personalise `reflection.md`.
- Upload only this lab's contents to a dedicated GitHub repository and submit its actual URL.

## References
1. Uploaded *LAB | Evaluation Dashboard Lab(1).pdf*.
2. [Tableau packaged workbooks](https://help.tableau.com/current/pro/desktop/en-us/save_savework_packagedworkbooks.htm).
3. [Tableau filters](https://help.tableau.com/current/pro/desktop/en-us/filtering.htm).
4. [Tableau filter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm).
5. [Official Tableau document schemas, version requirements and validation limitations](https://github.com/tableau/tableau-document-schemas).
''')
    import os
    os.chdir(ROOT)
    environment={'__name__':'__notebook_cell_runner__'}
    n=0
    for i,cell in enumerate(cells):
        cell['id']=f'cell-{i:03d}'
        if cell['cell_type']=='code':
            n+=1;capture=io.StringIO()
            with contextlib.redirect_stdout(capture):exec(compile(''.join(cell['source']),f'notebook-cell-{i}','exec'),environment)
            cell['execution_count']=n
            if capture.getvalue():cell['outputs']=[{'output_type':'stream','name':'stdout','text':capture.getvalue().splitlines(keepends=True)}]
    notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python','version':sys.version.split()[0]},
        'preparation_execution':{'runner':'Python exec cell runner','jupyter_kernel_verified':False}},'nbformat':4,'nbformat_minor':5}
    out=ROOT/'notebooks/Evaluation_Dashboard_Lab_Solution.ipynb';out.write_text(json.dumps(notebook,indent=1)+'\n')
    print(f'Notebook created: {n} Python code cells executed; Jupyter-kernel execution not verified.')

if __name__=='__main__':main()
