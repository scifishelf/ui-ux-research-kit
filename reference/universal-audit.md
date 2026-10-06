# Auditing local websites and web applications

Version 0.3.0. Start with [web-excellence-audit](../skills/web-excellence-audit/SKILL.md). Static HTML, client frontends, server-rendered applications and CMS projects are supported. Stack discovery is heuristic; it neither requires React nor proposes a replacement stack. The agent performs the actual UI review; Python inventories files, reconciles evidence and builds the plan.

## Profiles and scope

| Profile | Focus | Applicable additions |
| --- | --- | --- |
| `website` | Understanding, orientation, offer, contact/conversion | Public metadata, media, forms |
| `webapp` | Task completion, editing, status and recovery | Async states, forms, critical actions |
| `pwa` | Tasks in installed mode | Installation, safe areas, worker/offline behavior |

The [31 product criteria](../criteria/product/catalog.yaml) are distinct from the [45 pipeline/research criteria](../criteria/catalog.yaml). A general website audit does not require an installed PWA, local vision model or randomized skill experiment. Use the benchmark module when making comparative effectiveness claims.

A profile is not a style recipe. Audience, purpose, brand and real material guide art direction and density. Separate technical standards, product quality goals and trend references. Sources: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [Web Vitals](https://web.dev/articles/vitals), [2026 visual examples](https://webflow.com/blog/web-design-trends-2026). Outlooks for 2027 remain hypotheses.

## Usage

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/web-excellence-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --out /tmp/webapp-ui-ux-audit
```

The first run supplies inventory hints and investigation tasks. Multiple frontends require explicit `--frontend <relative-path>`. The script neither installs tools nor starts/modifies the app.

Prepare a real configuration using [project.example.json](project.example.json). Do not adopt its synthetic routes or feature decisions without checking them.

- `profile`: confirmed `website`, `webapp` or `pwa`.
- `frontend`: relative folder, `.` for root or `auto` for discovery.
- `audience`: actual audience and usage context.
- `journeys`: at least one priority job with ID, route, task, observable success and states. Optional journey `features` narrow applicability; omission conservatively includes all project features.
- `viewports`: required dimensions; defaults are 1440x900 and 390x844. Record supported browsers/OS, language and themes in the test log. Theme variants can be explicit states.
- `features`: `true` present, `false` verified exclusion, `null` unresolved. Document reasons. Do not introduce dark mode, offline promises or dragging simply to satisfy an audit.
- `available_capabilities`: capabilities actually available from [audit-tools.yaml](audit-tools.yaml). A file's existence does not prove working integration.
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

Evidence, inventory, Git working-tree or tested-scope changes downgrade old observations to `unknown`. Fresh hashes alone do not renew a test. `source_inventory_hash` covers selected text files and Git identity, not a complete build. Limits are 1200 files, depth 8 and 4 MB per file, with dependencies, builds, data and secrets excluded. Inspect relevant omissions separately. Record the actual running build as `runtime.build_id`; a commit alone does not identify a running server.

For each criterion:

- `status`: `pass`, `fail`, `unknown` or justified `not_applicable`.
- `scope` and `reason`: actual routes, states, inputs, themes, conditions, finding and limits.
- `observed_at`: timezone-aware actual test time; default maximum age seven days, configurable with `--max-age-days`.
- `evidence`: relative path, SHA-256, kind and locator. Use `root: target` for source; `root: evidence` for artifacts under explicit `--evidence-root`. Traversal, symlinks and secret files are rejected. Runtime criteria need a runtime artifact, not source alone.
- `runtime`: URL, route, state, browser/version, viewport, build ID and capture kind. Installed-PWA criteria require real device/simulator provenance and standalone/fullscreen mode.
- `coverage` for runtime `pass`: actually tested journey/state/viewport combinations. The required matrix comes from configuration and applicability. Partial coverage is `unknown`; a reproduced failure can establish `fail` in a smaller scope. Never list untested combinations.
- `remediation` for `fail`: concrete title, implementation steps and measurable acceptance. Actual `affected_files`, effort, owner role and dependencies may be supplied. Dependencies reference action IDs such as `ACT-A11Y-01` and must be acyclic.

See the [synthetic example](../skills/web-excellence-audit/references/observations.example.json) and [schema](../skills/web-excellence-audit/references/observations.schema.json). They are not runtime evidence.

`SPEED-01` additionally needs `field_metrics`: source, measurement window, `percentile: 75`, mobile/desktop `lcp_ms`, `inp_ms` and `cls`. Missing field data remains unknown; local trace-based improvements can still be planned. A Lighthouse score is not field INP evidence.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/web-excellence-audit/scripts/audit.py \
  --target /absolute/path/to/webapp \
  --project /tmp/webapp-ui-ux-audit/project.json \
  --observations /tmp/webapp-ui-ux-audit/observations.json \
  --evidence-root /tmp/webapp-ui-ux-audit/evidence \
  --out /tmp/webapp-ui-ux-audit
```

## Action plan and acceptance

Deliver `REPORT.md`, `summary.md`, `gap-report.md`, `audit.json`, `action-plan.md/json`, `tool-recommendations.json` and the bound observation template. The agent writes final human-readable reports in the requested language; JSON keys/IDs/status values stay English.

Priorities: P0 required evidence and critical blockers; P1 core tasks, accessibility and responsiveness; P2 content, structure and speed; P3 art direction and interaction quality; P4 regression and continued evaluation. Dependencies take precedence. S/M/L estimates are provisional.

Every evidenced gap answers: what happens on which route, which artifact proves it, which component causes it, what changes, what prerequisite exists, how acceptance is measured and what flow is retested. Unknown criteria create investigations, not invented defects. A list such as “improve UX / install a design skill” is insufficient.

Known MUST gaps and missing required evidence block approval. Human reviewers assess brand fit, readability, hierarchy and interaction feel with actual content. Appropriate target users test priority jobs against agreed outcomes. Required study depth depends on the product; a controlled skill experiment is not mandatory for every audit.

## Skill and tool proposals

Use [audit-tools.yaml](audit-tools.yaml) for capability mapping and [skill-radar.yaml](../skill-radar.yaml) for sources and dated pins. Automatic design/code proposals require observed deficiencies; open checks prompt testing capabilities. Reuse available capabilities first; an omitted capability means “check availability,” not proof that it is absent.

Distinguish skills, browser/MCP tools, libraries and evaluation methods. Installation examples are unpinned project proposals. Before adoption review existing alternatives, original source, selected commit/version, license and dynamically loaded rules. Non-Node products may use a separate audit harness. Apply [tool review](tool-review.md) to actual adoption.

A trial names a key screen or flow, baseline and retest. Compare product results and effort. Popularity, demonstrations and skill descriptions do not establish universal effectiveness.
