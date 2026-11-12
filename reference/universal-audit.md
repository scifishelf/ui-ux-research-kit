# Auditing local websites and web applications

Version 0.3.0. Start with [web-excellence-audit](../skills/web-excellence-audit/SKILL.md). Static HTML, client frontends, server-rendered applications and CMS projects are supported. Stack discovery is heuristic; it neither requires React nor proposes a replacement stack. The agent performs the actual UI review; Python inventories files, reconciles evidence and builds the plan.

## Profiles and scope

| Profile | Focus | Typical features to confirm |
| --- | --- | --- |
| `website` | Understanding, orientation, offer, contact/conversion | Public metadata, media, forms |
| `webapp` | Task completion, editing, status and recovery | Async states, forms, critical actions |
| `pwa` | Tasks in installed mode | Installation, safe areas, worker/offline behavior |

The [31 product criteria](../criteria/product/catalog.yaml) are distinct from the [45 pipeline/research criteria](../criteria/catalog.yaml).

A profile is not a style recipe. Audience, purpose, brand and real material guide art direction and density. Sources: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [Web Vitals](https://web.dev/articles/vitals).

## Usage

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/web-excellence-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --out /tmp/webapp-ui-ux-audit
```

The first run supplies inventory hints and investigation tasks. `--target` is the repository root. Multiple frontends, including framework packages nested below another, require explicit `--frontend <relative-path>`. The script neither installs tools nor starts/modifies the app.

Prepare a real configuration from [project.example.json](project.example.json) as `project.json` in the run directory; unknown keys are rejected. Do not adopt its synthetic routes or feature decisions without checking them.

- `profile`: confirmed `website`, `webapp` or `pwa`.
- `frontend`: relative folder, `.` for root or `auto` for discovery.
- `audience`: actual audience and usage context; required for acceptance.
- `journeys`: at least one priority job with ID, route, task, observable success and states (default `default`). Optional journey `features` narrow applicability; omission conservatively includes all project features.
- `viewports`: required dimensions; defaults are 1440x900 and 390x844. Record supported browsers/OS, language and themes in `REPORT.md`.
- `features`: `true` present, `false` verified exclusion, `null` unresolved, which blocks acceptance. `service_worker` and `offline` are checked only in the `pwa` profile. Give the reason for every `false` in `REPORT.md`. Do not introduce dark mode, offline promises or dragging simply to satisfy an audit.
- `available_capabilities`: capabilities actually available from [audit-tools.yaml](audit-tools.yaml). A file's existence does not prove working integration. Not part of the tested scope fingerprint.
- `report_language`: agent-authored report language, default English. It is presentation metadata and excluded from the tested scope fingerprint. The checker emits English prose; the agent translates final Markdown while preserving machine contracts.

Explicit CLI frontend/profile options override configuration values. Review startup commands before execution. Missing backend, login, data or runtime tools leave that scope open; continue independent checks. Use isolated test data for writing flows.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/web-excellence-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --project /tmp/webapp-ui-ux-audit/project.json \
  --out /tmp/webapp-ui-ux-audit
```

For output inside the target, `--out` must be the whole run directory including any kit copy. Both inventory and Git-status binding exclude it.

## Evidence contract

Copy `observations.template.json` to `observations.json`. A template containing findings is preserved; a new empty template receives a next-template filename. Keep its `target`, `source_inventory_hash` and `scope_hash` from the actually tested baseline.

Evidence, inventory, Git working-tree (including uncommitted and untracked content) or tested-scope changes downgrade old observations to `unknown`. Fresh hashes alone do not renew a test: rerun the baseline and retest; findings are not carried over. In a Git target, ignored files and skipped directories are outside the binding; anything else the app or a test runner writes counts as a change, hence the baseline after startup. Restore such test data before the final run. `source_inventory_hash` covers selected text files and Git identity, not a complete build. Limits are 1200 files (`--max-files`) and depth 8, with dependencies, builds, data and secrets excluded. `inventory_limits.skipped_directories` in `audit.json` lists omitted directories; inspect relevant ones separately. Record the actual running build as `runtime.build_id`; a commit alone does not identify a running server.

For each criterion:

- `status`: `pass`, `fail` or `unknown`. `not_applicable` follows only from profile and `features`; an observation cannot waive an applicable criterion.
- `scope` and `reason`: actual routes, states, inputs, themes, conditions, finding and limits.
- `observed_at`: timezone-aware actual test time; default maximum age seven days; a longer `--max-age-days` blocks acceptance.
- `evidence`: relative path, SHA-256, kind and, to tie the artifact to its journey/state/viewport, `locator`. Use `root: target` for source; `root: evidence` for artifacts under explicit `--evidence-root`, which lies outside the target or in a subdirectory of `--out`. Traversal, symlinks, empty and secret files are rejected, as is a `screenshot` or `video` without an image or video file extension. Runtime criteria need a runtime artifact under `root: evidence`, not source alone.
- `runtime`: provenance of the first runtime evidence entry, at a configured viewport and state; further artifacts name their journey/state/viewport in `locator`. URL, route, state, browser/version, viewport, build ID and `capture_kind` (`desktop-browser`, `mobile-simulator`, `installed-pwa-simulator` or `real-device`). Browser device emulation counts as `desktop-browser`; a simulator runs the mobile OS with its own browser and software keyboard. A pass needs `real-device` or `installed-pwa-simulator` with standalone/fullscreen `display_mode` for installed-PWA criteria, and any non-desktop kind for `RESP-03`.
- `coverage` for runtime `pass`: actually tested journey/state/viewport combinations. The criterion's `matrix` sets what a pass must cover: `states` every journey/state/viewport, `journeys` every journey at every viewport, `device` every journey once on the device (record the device's own viewport), `none` nothing. Journey `features` narrow it; combinations outside the configuration are rejected. Partial coverage is `unknown`; a reproduced failure can establish `fail` in a smaller scope. Never list untested combinations. Conditions a criterion's `test` names beyond the matrix (zoom, 320 px reflow, themes) belong in `scope`; while untested, the criterion stays `unknown`.
- `remediation` for `fail`: concrete title, implementation steps and measurable acceptance; `scope` and `reason` carry route/state and reproduction. Optional: `affected_files` (must exist in the target), effort, owner role and dependencies. Dependencies reference action IDs such as `ACT-A11Y-01` and must be acyclic.

See the [synthetic example](../skills/web-excellence-audit/references/observations.example.json) and [schema](../skills/web-excellence-audit/references/observations.schema.json). They are not runtime evidence. The checker rejects unknown keys in the envelope, findings, evidence, runtime, remediation and pass coverage.

`SPEED-01` needs evidence of kind `field-data` and, instead of `runtime` and `coverage`, `field_metrics`: source, measurement window, `percentile: 75`, mobile/desktop `lcp_ms`, `inp_ms` and `cls`. Missing field data remains unknown; local trace findings go into `REPORT.md`. A Lighthouse score is not field INP evidence.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/web-excellence-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --project /tmp/webapp-ui-ux-audit/project.json \
  --observations /tmp/webapp-ui-ux-audit/observations.json \
  --evidence-root /tmp/webapp-ui-ux-audit/evidence \
  --out /tmp/webapp-ui-ux-audit
```

## Action plan and acceptance

Deliver `REPORT.md`, `summary.md`, `gap-report.md`, `audit.json`, `action-plan.md/json`, `tool-recommendations.json`, `project.json`, `observations.json` and the evidence directory. The agent writes final human-readable reports in the requested language; JSON keys/IDs/status values stay English. `REPORT.md` is agent-authored: scope and tested matrix (browsers/OS, language, themes), reasons for excluded features, strengths and unmapped judgments per [product critique](../rubrics/product-critic.md) dimension, capability recommendations with their review status, and every open criterion with its blocker and what was attempted.

Priorities: P0 required evidence and critical blockers; P1 core tasks, accessibility and responsiveness; P2 content, structure and speed; P3 art direction and interaction quality; P4 regression and continued evaluation. These catalog priorities apply to evidenced gaps; an open MUST check is always P0, any other open check P4. Dependencies take precedence. S/M/L estimates are provisional.

Every evidenced gap answers: what happens on which route, which artifact proves it, which component causes it (once verified), what changes, what prerequisite exists, how acceptance is measured and what flow is retested. Unknown criteria create investigations, not invented defects. A list such as “improve UX / install a design skill” is insufficient.

Known MUST gaps and missing required evidence block approval. Human reviewers assess brand fit, readability, hierarchy and interaction feel with actual content. Appropriate target users test priority jobs against agreed outcomes.

## Skill and tool proposals

Use [audit-tools.yaml](audit-tools.yaml) for capability mapping and [skill-radar.yaml](../skill-radar.yaml) for sources and dated pins. Automatic design/code proposals require observed deficiencies; open checks prompt testing capabilities. Reuse available capabilities first; an omitted capability means “check availability,” not proof that it is absent.

Distinguish skills, browser/MCP tools, libraries and evaluation methods. Installation examples are unpinned project proposals. Before adoption review existing alternatives, original source, selected commit/version, license and dynamically loaded rules. Non-Node products may use a separate audit harness. Apply [tool review](tool-review.md) to actual adoption.

A trial names a key screen or flow, baseline and retest. Compare product results and effort. Popularity, demonstrations and skill descriptions do not establish universal effectiveness.
