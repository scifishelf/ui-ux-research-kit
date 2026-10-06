# Benchmark module

Prepared, not conducted. Read the [protocol](protocol.md), [tasks](tasks.yaml), [configurations](configurations.yaml), [panel/interview guide](panel-guide.md) and [result template](results-template.yaml).

```sh
python3 scripts/generate_plan.py --help
python3 scripts/analyze.py --help
python3 scripts/reliability.py --help
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

`run-plan-primary.csv` contains 90 planned generations for one agent. Analysis CSV uses `task,replicate,surface,configuration,score`, with desktop/pwa surface and one predefined panel aggregate per dimension; optional `client,dimension,judge_score`. Both configurations/surfaces must form complete pairs. Aggregate raters/states by a prespecified rule and retain failures. The script gives pilot statistics, not a full ordinal multilevel analysis.

Reliability CSV uses `sample_id,rater,score,dimension,surface`; one dimension/surface per file; integer scores 0–4 or missing. Ordinal alpha is a point estimate; the study must add suitable clustered confidence intervals. Tests use synthetic fixtures, not product measurements.
