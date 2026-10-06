# UI/UX Research Kit — index

Version 0.3.0 · Updated 2026-10-06 · English resources · Language-independent audit reports

Start with [README.md](README.md) for WHY, prerequisites, HOWTO and deliverables. Load only the files relevant to the next task.

## Product audits

| Task | Entry point |
| --- | --- |
| Audit locally using GitHub; save only under docs | [Copy-ready prompt](reference/audit-prompt-local-docs.md) |
| Use an existing local kit | [Audit request](reference/audit-request.md), [web-excellence-audit](skills/web-excellence-audit/SKILL.md) |
| Define scope, profiles and evidence | [Universal audit workflow](reference/universal-audit.md), [project example](reference/project.example.json) |
| Evaluate product and visual quality | [31 product criteria](criteria/product/catalog.yaml), [product critique](rubrics/product-critic.md) |
| Capture findings | [Synthetic observations](skills/web-excellence-audit/references/observations.example.json), [schema](skills/web-excellence-audit/references/observations.schema.json) |
| Recommend useful skills | [Capability registry](reference/audit-tools.yaml), [radar](skill-radar.yaml), [tool review](reference/tool-review.md) |

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/web-excellence-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --out /tmp/webapp-ui-ux-audit
```

Confirm frontend/profile, define jobs and states, then perform runtime checks. The Python inventory does not start or judge the UI. Deliver `REPORT.md`, `summary.md`, `gap-report.md`, `audit.json`, `action-plan.md/json` and `tool-recommendations.json`. The agent writes final Markdown in the requested language; machine contracts remain English.

## Optional development and research module

| Task | Resources |
| --- | --- |
| Audit the development pipeline | [pipeline-audit](skills/pipeline-audit/SKILL.md), [45 criteria](criteria/catalog.yaml), [category guide](criteria/README.md) |
| Set up a visual feedback workflow | [Flow](reference/flow.md), [agent design instructions](reference/CLAUDE-design-block.md), [component contract](reference/component-contract.md), [state matrix](reference/state-matrix.yaml) |
| Bind desktop/PWA evidence | [Capture loop](reference/loop/README.md), [manifest schema](reference/loop/capture.schema.json), [parity checker](reference/loop/parity_check.py), [CI gates](reference/ci-gates.md) |
| Configure runtime and local resources | [Environment](reference/environment.yaml), [resource guide](reference/local-resources.md) |
| Review UI, UX and motion | [Rubric](rubrics/ui-ux-motion.yaml), [critic](rubrics/critic.md), [output schema](rubrics/critic-output.schema.json), [validation plan](rubrics/validation-plan.md) |
| Explore motion | [14 patterns](motion-patterns/catalog.yaml), [interactive demo](motion-patterns/demo.html), [guideline](motion-patterns/02-guideline.md), [technology matrix](motion-patterns/03-technology-matrix.md) |
| Compare methods empirically | [Benchmark](benchmark/README.md), [protocol](benchmark/protocol.md), [tasks](benchmark/tasks.yaml), [configurations](benchmark/configurations.yaml), [90 planned runs](benchmark/run-plan-primary.csv), [panel/interviews](benchmark/panel-guide.md) |
| Inspect source evidence | [Research notes](report/research-notes.md), [source register](report/source-register.md), [source data](report/sources.yaml), [repository pins](report/evidence/repository-pins.json), [package pins](report/evidence/package-versions.json) |

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/pipeline-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --frontend . \
  --out /tmp/pipeline-audit
python3 reference/loop/parity_check.py desktop.json pwa.json \
  --expected-build BUILD_ID
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s benchmark/tests -v
python3 benchmark/scripts/validate_kit.py --schemas
shasum -a 256 -c MANIFEST.sha256
```

Audit scripts need Python 3.10+ and the standard library. Full schema validation additionally uses `jsonschema` in an existing or isolated environment. YAML data uses JSON-compatible YAML 1.2; skill frontmatter uses ordinary YAML. Category files are exact subsets of the canonical pipeline catalog.

## Interpretation

- Stable IDs: 31 product and 45 pipeline/research criteria. MUST/SHOULD/MAY are project obligations, not universal legal conclusions.
- 55 sources retain retrieval dates and scope limits. Trend observations are neither standards nor causal evidence.
- Radar assessments describe adoption hypotheses, not measured rankings. Repository/package pins are dated snapshots requiring review before use.
- The 14 desktop videos demonstrate synthetic interactions and reduced-motion handling. They do not validate a product, installed PWA or high-refresh display performance.
- Interviews, controlled product generations and expert/judge validation remain pending. Record actual agent/model revisions for any experiment.
- Proposed decisions remain pending until an actual decision is made. Existing authorization still applies.

GitHub source: [scifishelf/ui-ux-research-kit](https://github.com/scifishelf/ui-ux-research-kit). The public repository name reflects both UI and UX. It starts with a clean release history. [MANIFEST.sha256](MANIFEST.sha256) covers distributed files, excluding Git metadata and itself.
