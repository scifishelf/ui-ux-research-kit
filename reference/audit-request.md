# Reusable audit request

For GitHub kit retrieval and docs-only local artifacts, use the [copy-ready prompt](audit-prompt-local-docs.md). For an existing complete kit, fill these paths and the report language:

```text
Read <KIT-PATH>/skills/web-excellence-audit/SKILL.md.
Audit the local website/web application at <PROJECT-PATH>.
Save artifacts in <OUTPUT-PATH>. Requested report language: <LANGUAGE>.

Confirm product purpose, audience, frontend, actual stack and startup path.
Choose website/webapp/pwa and verify feature applicability. Define priority
user jobs, success criteria and the state/viewport test matrix.
Use the documented local runtime, render relevant screens, look at screenshots
and perform journeys. Connect runtime findings to actual source locations.
Reuse existing browser/testing capabilities.

Produce an evidenced current-state audit and prioritized action plan.
Each gap needs route/state, reproduction, evidence, concrete steps, affected
files/components, effort, dependencies, acceptance criteria and a retest.
Missing evidence is an investigation task; invent neither defects nor tests.
Recommend skills/tools for observed gaps and the actual stack, with existing
alternatives, original sources, installation options and a measurable pilot.

Deliver REPORT.md, summary.md, gap-report.md, audit.json, action-plan.md/json
and tool-recommendations.json. Set --kit to the complete kit path.
Set report_language in project.json. Write final human-readable Markdown in
the requested language; retain structured keys, IDs and status values.
The Python checker emits English templates and does not translate them.

This assignment covers audit and planning. Respect any separately granted
authorization for implementation or installation; the audit does not extend it.
```

Details: [universal audit workflow](universal-audit.md).
