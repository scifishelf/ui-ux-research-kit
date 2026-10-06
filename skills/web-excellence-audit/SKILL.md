---
name: web-excellence-audit
description: Audit a local website or web application using source code and rendered user journeys, then deliver an evidenced current state and prioritized action plan with concrete steps, acceptance criteria and suitable skill recommendations. Use for requested UI/UX or product audits; add PWA checks only for an applicable profile.
---

# Web excellence audit

Produce an actionable path to outstanding visual and functional quality. Audit authorization covers analysis and planning; respect separately granted implementation/installation permission without extending it.

The complete kit is two levels above this skill directory. Read [the universal workflow](../../reference/universal-audit.md). For a separately installed skill, locate the complete kit from the assignment and pass `--kit`; criteria and registries are not duplicated inside the skill.

1. **Understand the product.** Read target/project rules. Identify frontend, stack, startup path, audience and priority user jobs. Select the actual frontend in a monorepo. Confirm website/webapp/pwa and feature applicability in project configuration. For an explicit development-setup audit, additionally use [pipeline-audit](../pipeline-audit/SKILL.md).
2. **Create a baseline.** Run `scripts/audit.py --target <app-root> --project <project.json> --out <run-directory> --kit <kit-root>`. Respect the requested artifact destination. For docs-only audits, place all persistent output and kit copies inside the whole `--out` directory. Inventory/source inspection does not prove rendered quality.
3. **See and use the product.** Review startup commands and use the existing local runtime/browser tools under their operating rules. Render relevant journeys, states and viewports; actually inspect screenshots and perform interactions. Check DOM/accessibility, console/network and suitable traces, plus manual keyboard/screen-reader behavior. Record unavailable runtime checks as investigations while continuing independent work. Use an actual suitable runtime for installed PWA and software-keyboard checks.
4. **Record concrete findings.** Complete the generated observation template using the [evidence contract](../../reference/universal-audit.md#evidence-contract) and [schema](references/observations.schema.json). A pass covers the configured matrix; partial tests stay unknown. Each fail needs reproduction, route/state, evidence, actual source location, reasoned change, steps, effort, acceptance and retest. Verify the source cause; invent no files or defects. Retest after source/scope changes before rebinding observations.
5. **Deliver the plan.** Apply [product critique](../../rubrics/product-critic.md) to actual screens and flows. Rerun with `--observations` and `--evidence-root`; review `action-plan.md` for dependencies and product-specific completeness. Prioritize required evidence/blockers, core flows, structure/speed, visual distinction and regression. State estimates and uncertainty; an average score does not establish excellence.
6. **Recommend suitable capabilities.** Read [the registry](../../reference/audit-tools.yaml) and relevant radar entries. Reuse existing capabilities. Bind additional design/code skills to observed gaps, React rules to the actual stack. Include source, project installation option, reviewed pin/license, pilot and retest. Distinguish skills, tools and methods. Popularity is not quality evidence.

Record the requested report language in `project.json` as `report_language` (English default). Write `REPORT.md` and final Markdown reports in any language the agent supports. The checker emits English templates and records the preference; it does not translate. Translate prose after the final run while preserving evidence, uncertainty, JSON keys, IDs, statuses, paths and commands.

Deliver `REPORT.md`, `summary.md`, `gap-report.md`, `audit.json`, `action-plan.md/json` and `tool-recommendations.json` with build/scope provenance. If no target is supplied, prepare the invocation rather than inventing a product. An audit can have open criteria; acceptance needs missing evidence and human design/user review.
