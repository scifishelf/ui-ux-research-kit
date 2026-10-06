---
name: pipeline-audit
description: Audit a web application's UI development pipeline against versioned criteria and produce an evidence-based gap report and decision list. Use for explicitly requested setup or pipeline audits, not ordinary UI edits; the research contract includes desktop and installed-PWA workflows.
---

# Pipeline audit

This optional module examines development workflows under a desktop/installed-PWA research contract. For general website/webapp product audits and prioritized improvement plans use [web-excellence-audit](../web-excellence-audit/SKILL.md). Research/PWA obligations are not universal product requirements.

Read [INDEX.md](../../INDEX.md), then relevant criteria/references. The complete kit is two levels above this directory. A separately installed skill needs `--kit` pointing to the complete kit.

Identify application/frontend roots, project rules and supported routes. Product decisions take precedence. Audit permission does not independently authorize app changes, installations or deployment; respect existing authorization.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 <skill>/scripts/audit.py \
  --target <app-root> \
  --frontend <relative-frontend> \
  --out <audit-directory> --kind app
```

Inventory is only a hint: a filename, screenshot keyword or hook does not prove effectiveness. The script records selected file paths/hashes and initially marks all criteria unknown. Read project instructions, design contracts, active skills/hooks, CI and applicable PWA/test configuration. Inspect global setup only within authorized scope; exclude secrets and cookies.

Record criterion ID, actual tested scope, status, reason and evidence path/hash using [observations.example.json](references/observations.example.json). Runtime passes need rendered/executed evidence supplied and assessed by the reviewer; this legacy checker only verifies source bindings, not runtime provenance. Use the product audit's stronger evidence contract when applicable. Desktop WebKit emulation does not establish installed-PWA behavior. Stale evidence is unknown.

Rerun with `--observations`. Distinguish normative minimums from stricter product targets. Report every MUST gap. Document intentional surface differences without silently treating them as parity success or defects.

Deliver the gap report and proposed decision list with action, effort and retest. Record only actual accept/defer/reject decisions when requested; keep proposals pending otherwise. Make actions concrete before seeking any necessary decision and continue authorized checks.

Write human-readable reports in the requested language; keep machine keys, IDs and statuses stable. The script's templates are English. Comparative rankings/effect sizes require controlled generations and a blind panel. State source/build scope and open runtime checks; a complete audit report does not imply complete acceptance.
