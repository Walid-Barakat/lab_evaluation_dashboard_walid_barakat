# Data dictionary

| Field | Meaning and rule |
|---|---|
| evaluation_id | Unique integer for each example/candidate evaluation; count it, do not sum it |
| example_id | A shared prompt/example identifier; repeated once per candidate |
| category | reasoning, knowledge, code, instruction_following or tool_calling |
| score | Simulated rubric score from 0 to 100, rounded to two decimals; higher is better |
| model_version | Candidate A/B/C/D, generic simulated names |
| date | Evaluation date in YYYY-MM-DD, fixed synthetic window |
| score_bin | Lower edge of the 10-point band; values 0, 10, ..., 90 |
| score_range | Readable band label, sorted lexically with padded initial zero |
| meets_target | 1 if score >= 80, otherwise 0; average this field to obtain the illustrative target rate |
| judge_1_score, judge_2_score | Two simulated 0-100 ratings for the same evaluation row |
| score_difference | Absolute difference of the exported rounded judge scores, rounded to two decimals |
| agreement | 1 if score_difference <= 10, otherwise 0; mean is agreement rate |
| difference_bin, difference_range | Gap histogram bands using the same boundary conventions as score bands |

All intervals are lower-inclusive and upper-exclusive, except the final 90-100 interval includes 100. The judge agreement threshold is inclusive. Generated rows have no missing values, duplicated evaluation IDs or invalid dates. The four candidates share each example ID, and every category/candidate combination has 450 rows. This structure allows controlled comparisons in a future real evaluation design, but the present scores remain synthetic.

The published source CSVs, rather than screenshots or rounded dashboard labels, are authoritative for arithmetic checks. `docs/summary_metrics.json` and `data/*_summary.csv` provide independent Python aggregate exports.
