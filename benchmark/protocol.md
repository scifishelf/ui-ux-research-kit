# Controlled benchmark protocol

Prepared, not conducted. Criteria EVAL-01–05, LOOP-07 and PWA-08. Package/script tests do not constitute product or effectiveness measurements.

## Design and sample size

Six tasks B01–B06 × five cumulative configurations K1–K5 × at least three fresh generations = **90 implementations per agent**. Two surfaces produce 180 surface evaluations. Three clients yield 270 implementations/540 surface evaluations. Three raters yield 1620 ratings, not independent generations; states are dependent observations too.

Prespecify exactly one pinned skill for K3. Two additional single-skill arms add 36 implementations per primary agent. Budget combinations and critic/gate ablations separately. K4−K3 estimates the added visual loop under this contract; K5−K4 bundles critic and gates and cannot isolate their effects. K5S/K5G are optional dedicated ablations.

Three repetitions are a pilot minimum, not a power guarantee. Six tasks limit generalizability. Use pilot variance and the smallest meaningful change to freeze main-study sample planning; add task holdouts/repetitions when needed.

## Controls and execution

Keep base repository, approved tokens/assets, prompt, seed, data, runtime snapshots, tool permissions, time and cost ceilings equal. Use fresh isolated sessions/checkouts per generation; do not recycle winning code. Randomize order in task blocks. Client/model/provider changes require a new block.

K1–K3 receive no rendered feedback, including automatically integrated browser output. Evaluators still render every result on required surfaces. K4/K5 get the same evidence matrix and at most three revisions. Retain failed builds and explicitly record failure outcomes instead of silently replacing runs.

Compare quality under equal time/cost ceilings; optionally compare equal revision counts with extra critic/tool costs separately. Save first draft, post-loop and post-human-review as separate stages. Human review must not become an uncontrolled design service available only to K5.

## Measures and analysis

Prespecify expert UX score and completed-job proportion per surface as possible primary outcomes. Secondary/exploratory measures include UI/motion ratings, state coverage, token violations, parity, PWA checks, automated/manual accessibility, reduced motion, trace jank, costs and interventions.

Report paired task/replicate differences, mean/median change and explicitly defined standardization: `d_z = mean(paired differences) / SD(paired differences)`. It is not independent-sample Cohen's d. Use task-cluster bootstrap intervals, acknowledging instability with six clusters. A main study needs a suitable mixed-effects model for tasks, generations, raters and dependent surfaces. Prespecify contrasts K2−K1, K3−K2, K4−K3, K5−K4 and multiplicity handling, such as Holm.

Report ordinal Krippendorff alpha per dimension; optional ICC requires an explicit rater model. Validate LLM judges separately against panel judgments with calibration/holdout separation, Spearman, MAE and false blocker approvals.

AI detection is not quality. Include human-built controls, current templates and varied brands. Record AI/human/uncertain, confidence and brand fit separately; report sensitivity, specificity and false AI labels. Compare layout/type patterns across products for convergent generic design. No validated universal generic-design score is supplied.

For selected leading systems, formative usability testing may use 5–8 participants per task with counterbalancing. Record success, errors, time and task-level SEQ; apply system-level SUS or UEQ correctly. Document repeated measures and selection rules. Small convenience samples do not justify population or significance claims.

## Reproducibility and budget

The scripts generate a randomized plan, check pairs, compute pilot deltas/d_z/cluster intervals and ordinal alpha. Record client, exact model, skill commit/hash, prompt hash, kit version, fixtures, tool versions, build ID, seed and all artifacts. A retrieved pin is not a tested installation.

A planning ceiling of 30 minutes means up to 45 agent-hours for 90 runs or 135 for 270, plus rendering, failures and reviews. A hypothetical USD 3/run ceiling gives USD 270/810, **not a current price or consumption estimate**. Record actual billed tokens and separately budget interviews/panel work.
