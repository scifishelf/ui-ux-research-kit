# Local audit prompt — GitHub kit, docs-only artifacts

Give this prompt to a coding agent in the local product's working directory. Set `REPORT LANGUAGE` to any language supported by the agent. GitHub supplies the kit; the target analysis happens locally. Newly saved artifacts, including the kit archive, stay inside the run directory.

## Copy-ready prompt

```text
Perform a complete UI/UX audit of the currently opened local project using
the UI/UX Research Kit.

KIT SOURCE
https://github.com/scifishelf/ui-ux-research-kit

REPORT LANGUAGE
English. Replace this with the requested language, if specified by the user.
Write REPORT.md and final human-readable Markdown deliverables in that language.
Keep JSON keys, criterion IDs, status values, paths and commands unchanged.
Record the chosen language as report_language in project.json.
The Python checker produces English templates; translate their prose as needed
after the final checker run, preserving evidence, uncertainty and meaning.

PREPARE THE KIT
- Record the target project's initial working-tree state.
- Create ./docs/ui-ux-audit/<run-id>/ using a unique run ID.
  Preserve all existing files and changes.
- Resolve a source revision and download the complete kit as a source archive
  into this run directory; extract it into kit/. Record source revision and
  kit version. Use read-only repository/download access. Do not create another
  Git repository or .git directory in the target project.
- Read the kit's README.md, skills/web-excellence-audit/SKILL.md and
  reference/universal-audit.md. The complete kit is needed: skills, criteria,
  references and scripts must stay together.
- If GitHub is unavailable, use an existing complete local copy and record
  its provenance/revision. If none is available, identify the missing prerequisite
  without claiming that a kit audit has been performed.

GOAL
Establish the actual current state and produce a prioritized, concrete action
plan for outstanding visual design, intuitive usability and reliable behavior.
Include additional skill/tool recommendations relevant to evidenced gaps.

LOCAL WORKING RULES
- Analyze only the local target product. GitHub access is for obtaining the kit.
- Save all persistent audit artifacts within ./docs/ui-ux-audit/<run-id>/:
  archive, kit copy, report, configuration, observations, screenshots, traces
  and research data. This directory is the only permitted persistent change.
- Do not modify application code, project configuration or kit contents.
- No commits, branches, stashes, tags, git add, pushes, deployments or publication.
  Use Git only for read-only inspection.
- Do not install dependencies, skills or plugins, modify lockfiles or change
  global settings. Recommend installations without executing them.
- Prevent persistent files outside the audit directory, including bytecode,
  build outputs and browser profiles. Use PYTHONDONTWRITEBYTECODE=1 for Python.
- Reuse available local runtime/browser tools. Start the application only if
  its persistent outputs can stay inside the audit directory. Stop processes
  you started after the audit; preserve pre-existing processes.
- Preserve user and production data. Exercise writing flows only with isolated
  test data stored inside the audit directory. Otherwise mark the flow untested.
- Do not upload source or audit data to additional external services.
  Exclude secrets and personal data from evidence.

EXECUTION
1. Identify purpose, audience, frontend, actual stack and startup path.
   Choose and justify website, webapp or pwa; confirm feature applicability.
2. Define priority user jobs, observable success, relevant states and viewports.
3. Inspect source and actually rendered views. Look at screenshots and perform
   user journeys. Review visuals, content, navigation, forms, error handling,
   responsiveness, accessibility, motion and performance. Continue independent
   checks if runtime capabilities are missing; identify unresolved areas.
4. Invoke the checker with the complete kit's absolute path as --kit and the
   whole run directory as --out. The checker excludes --out from inventory;
   this must exclude the kit copy and all research artifacts together.
   Bind observations to the tested sources and scope using the evidence contract.
5. Evidence deficiencies with route, state, reproduction and actual source
   locations. Missing checks are unknown. Do not invent tests, results or defects.
6. Compare the final working tree with the recorded initial state. Verify that
   no changes arose outside the run directory. Do not reset existing changes.
   Document unexpected changes instead of applying a blanket reset or clean.

REPORT AND ACTION PLAN
Create ./docs/ui-ux-audit/<run-id>/REPORT.md plus the kit's reports and structured
data in the same directory, following the requested report-language preference.

Include:
- executive summary and key findings;
- target, tested scope, working-tree/build identity, kit revision, methods and limits;
- strengths and evidenced weaknesses;
- prioritized actions with concrete steps, affected files/components, effort,
  dependencies, acceptance criteria and retests;
- suitable skill/tool proposals tied to findings, existing alternatives,
  original sources, installation options and a verifiable pilot;
- missing evidence and required follow-up checks;
- the final comparison with the initial working-tree state.

Do not implement proposed improvements or installations.
This assignment covers analysis, audit and documentation only.
Finish by naming the report path, key actions and remaining verification gaps.
```

See [universal workflow](universal-audit.md) for profiles/evidence and [audit request](audit-request.md) for an existing local kit and a custom output folder.
