# Reflection

Suggested student reflection. Review and personalise after checking the dashboards in Tableau.

I organised the dashboard around questions a stakeholder can answer without reading my code: how scores are spread, which categories need attention and whether a candidate's performance changes across categories. The cards provide a quick overview, while filters help a manager narrow the view. I included plain score definitions, sample counts, a visible synthetic-data label and a short suggested action. I kept statistical methods, generation assumptions and detailed checks in the notebook and documentation. I also distinguished a rubric score from accuracy and judge agreement from correctness.

The biggest limitation is the simulated data. The weaker reasoning scores and candidate differences were built into the generator, so I cannot use them to justify purchasing or deploying a real model. Next time, I would use evaluation exports from my EU tender agent, apply a documented human-reviewed rubric, keep the same examples across candidates, and ask a non-technical reader whether the dashboard makes the next decision clear. I would then verify the workbook's actual filters in Tableau, capture the required screenshots and submit only after checking the repository contents.
