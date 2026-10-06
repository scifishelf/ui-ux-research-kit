# Release notes

## 0.3.0 — 2026-10-06

- Name: **UI/UX Research Kit**; the clean public repository is `scifishelf/ui-ux-research-kit`.
- English documentation, skills, criteria, source descriptions, tool registry, scripts and motion demonstrations.
- Explicit report-language preference for agent-authored human-readable deliverables. Python templates remain English; structured contracts are language independent.
- Public distribution contains reusable methods and synthetic examples. Project-specific audits, presentations, private evidence, internal tooling and personal machine details have been removed.
- English machine vocabulary: `requirement`, `test`, `passing`, `action`, `effort`, `platforms`, `category`, `research_evidence`, `sources`; levels are MUST/SHOULD/MAY.
- Action-plan outputs are now `action-plan.md` and `action-plan.json`. Stable criterion IDs and observation schema version 1 are retained.

### Migration from 0.2.0

Update consumers of the German catalog keys and action-plan filenames. Recreate the audit baseline with the new version and configuration before recording fresh observations. Existing reports describe their original scope and are not renewed by translating them. `report_language` is a presentation preference; changing it alone does not change the tested product scope.

The product audit introduced in 0.2.0 supports website, webapp and optional PWA profiles. The optional pipeline/research module remains separate.
