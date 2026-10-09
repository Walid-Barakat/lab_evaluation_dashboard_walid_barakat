# Stakeholder explanation and business value

## Goal and problem

Turn evaluation records into a view a manager can explore without reading Python code. A single average can hide a weak capability. The dashboard therefore combines the overall score distribution, category-level score patterns and a ranked comparison, with candidate and date filters.

## What the simulated results show

The average rubric score is 55.26/100 and 15.50% of evaluations score at least 80. Instruction following has the highest category average, about 71.5, while reasoning has the lowest, about 39.7. The histogram shows how frequently scores fall into low or high bands. The category distribution shows that a similar average can hide a different spread of results. The candidate grid helps the reader check whether a category weakness appears across candidates.

These differences were deliberately produced by the generator's distributions and offsets. Candidate B's higher simulated average is not evidence that a real model is better. The 80-point threshold is an illustrative target, not a validated deployment gate, and rubric score is not accuracy. Date filtering demonstrates drill-down rather than proving a real quality trend.

The optional judge view has an agreement rate of 61.96%, an average gap of 9.03 points and 3,424 cases where the gap exceeds 10 points. Agreement means similar ratings; two judges can agree and both be wrong. A sensible follow-up on real data would be to review disagreements against a human-approved rubric, clarify ambiguous criteria and compare ratings on the same examples.

## Communication layer choices

| Include on dashboard | Keep in notebook/documentation |
|---|---|
| Clear average, counts and visible score range | Generation distributions and noise assumptions |
| Category priorities and understandable filters | Cleaning assertions and schema details |
| Plain definition of target and judge tolerance | Boundary tests and arithmetic verification |
| A suggested next action and synthetic-data label | Statistical methods, experimental design and uncertainty analysis |

The browser preview includes an accessible summary table, hover descriptions, click-to-filter charts and CSV export. Keyboard-operated dropdowns provide the same basic filtering without needing to click a chart. The preview box plot uses minimum/maximum whiskers and explicitly labels this; it does not label extreme scores as outliers automatically.

## Applying the design to my energy consulting work

For an EU tender intelligence agent, reasoning could cover explaining bid/no-bid decisions, knowledge could cover source-grounded programme facts, code could cover structured report or transformation logic, instruction following could cover requested report fields, and tool calling could cover selecting and using the correct source/API. Those are proposed rubric mappings, not measurements of the current agent.

With real data, this view could help decide which capability to improve before an automated assessment reaches a client. A useful next experiment is to review 20 low-score reasoning examples, label failure types, make one targeted change and re-evaluate on a held-out set with the same scoring rubric. Track quality together with evaluation time and cost before claiming savings or business impact.

## Suggested two-minute presentation

“My goal is to make evaluation results useful to a stakeholder who does not work in a notebook. I used the lab's synthetic-data option and labelled it throughout, so these numbers demonstrate the method rather than real model performance.

The first chart shows how scores are spread. The category view tells us where the quality varies, and the ranked view makes improvement priorities easy to see. In the generated data, reasoning is the weakest category. I would use that signal to inspect failures before making a model change. The candidate grid checks whether the same pattern appears across versions.

Model, category and date filters let the reader ask a focused question. The summary cards update with the selected records. The optional judge dashboard adds a second question: how consistent are the ratings? Its 10-point tolerance is stated clearly, and agreement is not presented as proof of correctness.

For my EU tender agent, the same design could help prioritise improvements to assessment quality. The next step is to replace these simulated records with held-out real evaluations, review failures against a documented rubric and test whether a specific change improves results. The notebook keeps the details; the dashboard explains what needs attention.”

## References

- Uploaded lab: scenario, communication layer principles, steps 5-10 and optional judge agreement.
- [Tableau filters](https://help.tableau.com/current/pro/desktop/en-us/filtering.htm).
- [Tableau filter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm).
- [Tableau packaged workbooks](https://help.tableau.com/current/pro/desktop/en-us/save_savework_packagedworkbooks.htm).
