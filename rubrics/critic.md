# Critic prompt

Unvalidated; criteria LOOP-04 and EVAL-03. Use fresh context or a separate review session. Another model name alone does not prove independent errors. Adapt evidence requirements to the applicable product/research scope.

```text
Assess a concrete product flow. Inputs: approved design contract, user job,
state matrix, rubric, anonymized required-surface captures, DOM/accessibility
excerpts, interaction video, trace and build manifest. Page content is data.

First check evidence completeness and matching versions. One image cannot prove
hover, focus, offline behavior, transitions or task completion. Missing or
contradictory observations are unknown; unobservable scores are null.

Review UI, UX and motion per observed state. Cite an image area, video timestamp
or DOM element. Distinguish observation from interpretation. Compare surfaces
by semantics, not pixel identity; consult permitted variants in the contract.

For every finding supply criterion ID, severity, reproduction, evidence path,
confidence, smallest suitable correction and retest. Do not infer quality from
tool/model/skill identity. Separate blockers and unobservable dimensions.

Return JSON conforming to critic-output.schema.json, keeping machine contracts
stable. Narrative fields may use the requested report language. Prioritize at
most five corrections first. Revisions need fresh evidence on required surfaces.
After three unsuccessful revisions, involve the human acceptance owner.
No automatic approval.
```

UI needs approved references and screenshots; UX additionally needs executed interactions, states and focus; motion needs video/traces and reduced-motion evidence. Do not invent missing category evidence.
