# Requirement fulfilment and remaining evidence

This is a requirements mapping, not an invented grading rubric. The brief does not assign numerical marks or weights.

| Lab requirement | Delivered evidence | Status |
|---|---|---|
| Step 1: choose existing or generated evaluation data | `data_source.md`, seeded generator and raw CSV | Prepared: Option B |
| Step 2: clean/format numeric scores, categories and dates | Clean CSV, `data_quality_report.json`, validator | Passed locally; zero rows removed |
| Step 3: at least 100 rows and suitable fields | 9,000 rows, six core fields plus calculated exports | Passed locally |
| Step 4: connect data to Tableau or Power BI | Native Tableau connections and embedded CSV | File prepared; actual Tableau connection pending |
| Step 5: overall score histogram | Score Distribution in TWBX and HTML | XML structure / preview drawing checked; native rendering pending |
| Step 6: category score distribution | Native heatmap by category and score range; preview box plot | Prepared; native rendering pending |
| Step 7: category comparison | Descending average-score bars; candidate heatmap is additional | Prepared; native sort/labels pending |
| Step 8: model/category/date filters | Three native filters; working JS logic under test doubles | Logic checked; browser and native UI verification pending |
| Step 9: cohesive interactive dashboard | Seven native worksheets, dashboard zones and two preview pages | Prepared; enable/check native cross-filter actions |
| Step 10: titles, score meaning and stakeholder context | Dashboard headings, synthetic badge, cards and interpretation | Prepared and preview reviewed |
| Step 11: test, refine and save | Local data tests, JS checks, XSD/ZIP/reference checks | Passed locally; native application checks pending |
| Required native dashboard file | `evaluation_score_dashboard.twbx`, editable TWB | Delivered; open and re-save after Tableau verification |
| Required dashboard screenshot | `dashboard_preview.png` is supplied as a preview only | **Pending: capture dashboard_screenshot.png from Tableau** |
| Brief data documentation | `data_source.md`, three sentences | Delivered |
| Recommended reflection | `reflection.md`, two paragraphs | Delivered as a suggested reflection to personalise |
| README and descriptive filenames | `README.md`, named folders/files | Delivered |
| Repository contains only this lab | Dedicated-folder package, `.gitignore` | Package prepared; inspect actual repository after upload |
| GitHub-only primary submission | `github_submission.md` | **Pending: create/upload repository and submit actual URL** |
| Optional judge-data preparation | 9,000 paired ratings, difference and agreement flags | Passed locally |
| Optional three judge charts | Agreement by category, gap histogram, rating-pair scatter | Prepared; native rendering pending |
| Optional judge metrics and filters | Agreement, gap, count cards plus three filters | Prepared; native interactions pending |
| Optional dashboard native file/screenshot | `judge_agreement_dashboard.twbx`, labelled preview PNG | File delivered; native screenshot pending |

The supplied previews are not Tableau screenshots. The browser preview is additional evidence and cannot substitute for the mandated native workbook. Native opening/filtering is not claimed from XML validation. The notebook's outputs were generated with a Python cell runner, not a Jupyter kernel.

Source: uploaded *LAB | Evaluation Dashboard Lab(1).pdf*. Validation distinction: [official Tableau document schema guidance](https://github.com/tableau/tableau-document-schemas).
