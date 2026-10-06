# Judge validation

Criteria EVAL-02/03. Rubrics are prepared, not panel-validated. Sources: [MT-Bench](https://arxiv.org/abs/2306.05685), [Rubric Artifacts](https://arxiv.org/abs/2609.02942). Text-dialog findings do not validate UI judgments.

1. At least three independent experts rate identical anonymized flow bundles. Report ordinal Krippendorff alpha per dimension and, optionally, ICC with its specified rater model. Calibrate anchors before the main measurement.
2. Separate calibration and holdout tasks; never tune on holdout. B01–B04 versus B05–B06 is only a small pilot split, not broad prospective validation.
3. Give the judge the same permissible evidence, excluding configuration, costs, generator comments and panel scores. Counterbalance pair order; record exact model and settings.
4. Report per-dimension Spearman correlation, MAE, error distribution and false approvals of expert blockers with uncertainty. Correlation alone can hide systematically inflated scores.
5. Possible pilot thresholds to agree beforehand: rho >=0.7, MAE <=0.5 on 0–4 and no observed blocker false approval. These are project decisions, not validated standards. Few blockers and zero observed errors do not establish safety; independence assumptions matter.
6. Until sufficiently broad prospective holdout evidence exists, automate triage only. Accessibility, brand fit and final UX acceptance remain human responsibilities. Revalidate after model/rubric changes.

[analyze.py](../benchmark/scripts/analyze.py) supplies paired differences and exploratory judge correlation/MAE; [reliability.py](../benchmark/scripts/reliability.py) supplies ordinal alpha. Neither replaces a panel, clustered uncertainty estimates or the [study protocol](../benchmark/protocol.md).
