# Evaluation Dashboard Lab

**Student:** Walid Barakat  
**Chosen BI tool:** Tableau, workbook format 2026.2  
**Data option:** Option B, reproducible synthetic evaluations  
**Status:** Package generated and structurally tested. Tableau application checks, native screenshots and GitHub upload remain to be completed.

The dashboard communicates quality gaps across reasoning, knowledge, code, instruction following and tool calling. It contains score bands, category distributions, category rankings, a candidate comparison, model/category/date filters and summary cards. The optional dashboard shows agreement between two simulated judges.

## Start here

1. Open `evaluation_dashboard.html` in Safari, Chrome or Firefox for the self-contained browser preview. No server, credentials, API call or internet connection is needed for charts or filtering.
2. Open `evaluation_score_dashboard.twbx` in Tableau Desktop **2026.2 or later**. Follow `docs/tableau_open_and_verify.md`. XML schema validation is not proof that Tableau will open or render a workbook correctly.
3. Open `judge_agreement_dashboard.twbx` for the optional extra. Validate both workbooks in Tableau and re-save them.
4. Capture `dashboard_screenshot.png` and `judge_agreement_screenshot.png` **from Tableau**. The supplied `*_preview.png` files are labelled preview renders from the chart code, not screenshots from Tableau.
5. Follow `docs/github_submission.md` and submit the dedicated repository URL. The lab requires GitHub as the primary submission.

## File map

| File/folder | Purpose |
|---|---|
| `evaluation_score_dashboard.twbx` | Main packaged Tableau workbook and embedded clean CSV |
| `judge_agreement_dashboard.twbx` | Optional packaged judge-agreement workbook and embedded CSV |
| `tableau/*.twb` | Editable XML workbook sources; refer to the adjacent `data/` folder |
| `evaluation_dashboard.html` | Offline interactive browser preview with two dashboard pages |
| `dashboard_preview.png`, `judge_agreement_preview.png` | Visual previews, explicitly not native BI screenshots |
| `Evaluation_Dashboard_Lab_Solution.pdf` | Solution report, findings and submission requirements |
| `notebooks/Evaluation_Dashboard_Lab_Solution.ipynb` | Data preparation, calculations, audit checks and reproducible lab solution |
| `data/` | Raw/clean synthetic CSVs, judge ratings and audited summary exports |
| `scripts/` | Data generation, validation, summaries and dashboard builders |
| `tests/` | Negative-data checks and dashboard JavaScript logic checks |
| `data_source.md` | Required brief source description |
| `reflection.md` | Suggested student reflection to review and personalise |
| `docs/` | Step-by-step Tableau guide, requirements mapping, validation evidence and submission checklist |
| `requirements.txt` | Python dependencies for regeneration |

## Reproduce the solution

From the extracted project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_evaluation_data.py
python scripts/validate_evaluation_data.py
python scripts/summarize_evaluations.py
python scripts/build_html_dashboard.py
python scripts/build_tableau_workbooks.py
python scripts/validate_tableau_structure.py
python -m unittest discover -s tests -p 'test_*.py'
```

The schema check downloads Tableau's official 2026.2 schema; all other listed data/dashboard steps work locally. To run the JavaScript logic tests and regenerate preview PNGs, install Node 20+ and `npm install --no-save @napi-rs/canvas`, then run `node tests/test_dashboard_logic.cjs`. These tests execute the dashboard code with DOM test doubles; they do not claim browser or Tableau end-to-end coverage. Exclude `node_modules/` from GitHub.

For Windows, activate with `.venv\Scripts\activate` instead. The notebook is a standard nbformat-4 document; its included outputs were produced by executing cells with a Python runner, not by a Jupyter kernel. Open it in VS Code or Jupyter and run the cells yourself.

## Data and interpretation

There are 9,000 evaluation rows, 2,250 examples, four generic candidates and 90 days from 10 July to 7 October 2026. Every example is evaluated for all four candidates. All names, scores, model differences and judge differences are simulated. Balanced category/model counts make the default comparison easy to read, but none of these numbers establishes real model superiority, real business impact or deployment readiness.

The global mean is **55.26/100**; **15.50%** meet an illustrative score threshold of 80. Reasoning is the weakest simulated category and instruction following is the strongest. Judges agree within 10 points on **61.96%** of rows. These are outputs of the generator, not external evidence. See `docs/interpretation_and_business_value.md` for the suggested stakeholder explanation and an energy-consulting application.

## Sources

- Uploaded assignment: *LAB | Evaluation Dashboard Lab(1).pdf*, requirements, steps 1-11 and optional judge-agreement extension.
- [Tableau packaged workbooks](https://help.tableau.com/current/pro/desktop/en-us/save_savework_packagedworkbooks.htm).
- [Tableau filters](https://help.tableau.com/current/pro/desktop/en-us/filtering.htm).
- [Tableau filter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm).
- [Official Tableau document schemas and validation limitations](https://github.com/tableau/tableau-document-schemas).

No GitHub repository was created or published during package preparation. Do not claim complete submission until the native checks, screenshots and repository upload are done.
