# Open, verify and finish in Tableau

## Why this step remains

Tableau Desktop is not installed in the preparation environment. The files were authored programmatically and checked against Tableau's published 2026.2 XML schema, along with workbook references, CSV packaging and ZIP integrity. Tableau explains that syntactic validation does not guarantee a workbook will open. Accordingly, native connection, rendering, filter behaviour and screenshots are still pending.

## Main route

1. Use Tableau Desktop 2026.2 or later. Earlier versions cannot reliably open this version's XML. Consult [the official schema version guidance](https://github.com/tableau/tableau-document-schemas).
2. Open `evaluation_score_dashboard.twbx`. If the packaged CSV needs locating, use Data > the data source > Edit Connection and select `data/evaluation_data_clean.csv` from the extracted solution folder. Alternatively, open `tableau/evaluation_score_dashboard.twb` while keeping `data/` alongside `tableau/`.
3. In the Data Source preview, verify **9,000 rows**, numeric score values, a date field, category/model dimensions and evaluation ID as a dimension. There are no null or invalid scores in the provided data.
4. Open **Model Evaluation Score Dashboard**. Check the three summary cards and four charts. The native category distribution is a category-by-score-range heatmap, while the HTML preview uses a box plot. Both show the distribution; the lab's required comparison is the ranked category bar chart.
5. For each model/category/date filter, choose **Apply to Worksheets > All Using This Data Source**. Confirm it applies to all seven worksheets, including the three cards. The source includes shared filter groups, but their actual behaviour has not been verified in Tableau.
6. Configure the date filter as **Range of Dates**. Use 10 July to 7 October 2026 for the unfiltered default.
7. Enable category cross-filtering: on the **Category Comparison** dashboard object choose **Use as Filter**. Alternatively, Dashboard > Actions > Add Action > Filter; source = Category Comparison, target = the other charts and cards, Run action = Select, Clearing selection = Show all values, Selected fields = category to category. Do the same for Scores by Category if useful.
8. Check that **Category Comparison** sorts descending and labels averages, not sums. Its reference line is the average of displayed category means. On the balanced default data this equals the overall mean; with real or uneven data, replace it with a properly row-weighted benchmark or clearly keep the existing label.
9. Format score axes to a fixed range **0-100**, format percentages to one decimal place and counts to whole numbers. Ensure bars begin at zero. Increase text-card mark font size to about 28 if the generated default is too small.
10. The native histogram uses `score_range`, ordered as **00-10, 10-20, ..., 90-100**. The final band includes score 100; other bands exclude their upper boundary. Its equivalent numeric `score_bin` field contains 0, 10, ..., 90.
11. If a filter or card is not displaying correctly, use the rebuild recipe below. Save the verified file with **File > Save As > Tableau Packaged Workbook (.twbx)** using `evaluation_score_dashboard.twbx`.
12. Export or capture the verified dashboard as **dashboard_screenshot.png**. This must be a real Tableau view. Keep the `dashboard_preview.png` file separate; it is not native submission evidence.

## Optional judge dashboard

Open `judge_agreement_dashboard.twbx`. Verify 9,000 compared evaluations, mean agreement **61.96%** and mean absolute score gap **9.03 points**. Apply model/category/date filters to all six worksheets. Agreement is a mean of the 0/1 indicator, not its sum. Judge Comparison must keep evaluation ID on Detail so the plot displays individual rating pairs rather than only five category averages. A generated trend line is included; it indicates association, not necessarily equality of ratings. Export **judge_agreement_screenshot.png** after testing.

## Manual rebuild recipe if Tableau rejects generated XML

Connect through **Text File** to the supplied clean CSV. Make evaluation ID and example ID dimensions, category/model strings and date a Date. Create `Row Count = 1` if a record count field is unavailable.

| Worksheet | Columns | Rows | Marks / encoding |
|---|---|---|---|
| Score Distribution | score_range | SUM(Row Count) | Bar, ordered ascending by score band |
| Scores by Category | score_range | category | Square; SUM(Row Count) on Color and Label |
| Category Comparison | AVG(score) | category | Bar; AVG(score) on Label; descending sort |
| Candidate Comparison | model_version | category | Square; AVG(score) on Color and Label |
| Average Quality Score | none | none | AVG(score) on Text |
| Total Evaluations | none | none | SUM(Row Count) on Text |
| Scores At Or Above 80 | none | none | AVG(meets_target) on Text, formatted percent |

Create a 1400 x 950 dashboard and add all seven worksheets. Put model, category and range-of-date filter cards above the charts and apply to all sheets. Use a navy background and readable pale-blue labels. Add a visible synthetic-data label. Set category charts to Use as Filter and reset all selections before saving.

For the judge CSV, create `Row Count = 1`; use category vs AVG(agreement), difference_range vs SUM(Row Count), and AVG(judge_1_score) vs AVG(judge_2_score) with evaluation_id on Detail. Add cards for AVG(agreement), AVG(score_difference) and SUM(Row Count). Apply all filters and save the optional TWBX.

## Exact interaction checks

| Selection | Expected evaluation count |
|---|---:|
| All models, all categories, full date range | 9,000 |
| Candidate A only | 2,250 |
| Reasoning only | 1,800 |
| Candidate A + reasoning | 450 |
| Candidate A + reasoning + 7 October 2026 only | 5 |
| Reset all filters | 9,000 |

Confirm every chart and card changes, no irrelevant model remains visible, empty selections are understandable, and the optional judge count matches the quality dashboard for the same filter. Take the screenshots only after these checks.

Sources: [Tableau filters](https://help.tableau.com/current/pro/desktop/en-us/filtering.htm), [filter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm), [packaged workbooks](https://help.tableau.com/current/pro/desktop/en-us/save_savework_packagedworkbooks.htm), [schema validation](https://github.com/tableau/tableau-document-schemas).
