# Visual coding agents — research notes

English, project-neutral edition of the source-based research module. Source snapshots were retrieved on 2026-10-04/05; see [the register](source-register.md) for dates and claim boundaries. Controlled product experiments, interviews and expert validation have not been conducted.

## Decision and evidence status

Pilot a product-specific design contract with actual visual/interaction feedback, bounded revision and human acceptance. Add design skills individually when they address a demonstrated gap. A visible coding agent has more observation channels; this does not establish reliable self-correction or a causal improvement in aesthetics/usability.

Screenshot-to-code, visually grounded navigation, dialogue feedback and product aesthetics are different research tasks. [Design2Code](https://arxiv.org/abs/2403.03163) combines screenshot-based metrics and human review across 484 pages. [VisualWebArena](https://arxiv.org/abs/2401.13649) examines visually grounded web tasks. [Sketch2Code](https://arxiv.org/abs/2410.16232) shows that interactive clarification does not guarantee continuous improvement. [FronTalk](https://arxiv.org/abs/2601.04203v3) provides a closer multiturn frontend case involving retention failures and web-agent criticism. None establishes an effectiveness ranking for this kit's skills or installed-PWA workflow.

The null hypothesis remains legitimate: a visual/critic loop may add no material benefit beyond a strong design contract and deterministic tests, while increasing costs or introducing incorrect criticism.

| Evidence class | What it supports | What remains unestablished |
| --- | --- | --- |
| Standards/API documentation | Requirements and available mechanisms | Actual product conformance and user experience |
| External research | Failures, feedback mechanisms and judge bias in the studied tasks | Transferable product-specific effect sizes |
| Synthetic examples/tests | Demo behavior and checker invariants | Real product quality and installed-PWA acceptance |
| Pilot proposals | Rubrics, timing, budgets and experiment design | Panel validity, causal benefit and ranking |

Recommendations for 2027 extrapolate testable mechanisms. They are forecasts, not measured future facts or mandatory visual fashions.

## A — Seeing, evaluating and developing consistently

### A1: phases, roles and artifacts

Start with user job, observable success and a design contract. Implement shared components/states, render required surfaces, collect evidence, critique, correct and review. Keep task specifications, tokens, fixtures, build manifests, screenshots/DOM, interaction videos and actual decisions. Human responsibility covers product decisions, conflicts, bounded-loop escalation and final acceptance. These roles do not require separate agents. Fresh criticism avoids relying on generator justifications, but does not guarantee independence. [Reference workflow](../reference/flow.md); LOOP-01/04/05 and UX-01.

### A2: feedback channels and reliability

Combine browser interactions, DOM/accessibility data and images. Accessibility trees help target actions but do not faithfully convey composition, typography or spacing. Pixel regression detects change against an approved baseline, not whether that baseline was good. Vision criticism may locate visible defects or hallucinate them; measure recall on labeled holdout defects rather than assuming reliability.

The source snapshots describe [Playwright MCP](https://github.com/microsoft/playwright-mcp), [DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) and [Safari MCP](https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/). Their browser capabilities do not establish universal installed-iOS-PWA control. Use supported device/simulator adapters and application diagnostics for that scope. LOOP-03/06 and EVAL-03.

### A3: operationalizing aesthetics and UX

UI covers hierarchy, grid, typography, tokens and brand fit. UX covers completion, recovery, states, input/focus and appropriate parity. Motion covers purpose, timing, interruption, reduced mode and runtime quality. The [0–4 rubric](../rubrics/ui-ux-motion.yaml) uses observable anchors and null for unobservable dimensions. Blockers remain separate from aesthetic averages.

[MT-Bench](https://arxiv.org/abs/2306.05685) describes position, verbosity and self-preference bias; [Rubric Artifacts](https://arxiv.org/abs/2609.02942) examines wording effects on text judgments. Transfer to visual review is provisional. LLM judges remain advisory until validated against an independent panel on holdout tasks, including correlation, absolute error and false blocker approval. [Validation plan](../rubrics/validation-plan.md); EVAL-02/03.

### A4: design systems across sessions

Version semantic tokens, reviewed components, states and concise reference implementations together. Explain permitted differences through annotated references instead of conflicting style recipes. Project instructions should link the actual current contract. [DTCG 2025.10](https://www.designtokens.org/tr/2025.10/format/) helps token interchange but does not define layout/state architecture; it is a Community Group Report. Reuse the product's existing system. DS-01–04.

### A5: user jobs and states

Each task needs a start, goal, action, outcome and recovery path. Each applicable state needs a fixture, surface, theme, expected behavior and evidence. Empty states explain a useful next step; loading blocks only dependent actions; errors preserve input and offer suitable recovery. Check overflow, long text, narrow screens, zoom and supported themes explicitly. A happy-path image cannot prove unobserved states. UX-01–04; [state matrix](../reference/state-matrix.yaml).

### A6: desktop/PWA consistency

A shared codebase alone does not prevent stale worker caches or old open clients. Compare immutable build identity, token version, fixture/state, active worker and semantic outcomes. Compare screenshots against separate browser/platform baselines; different layouts may be intentional. [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) explains environment-specific baselines.

Define supported jobs and intentional surface differences before applying parity gates. A desktop-only function may be valid, but cannot silently satisfy a contract requiring it elsewhere. LOOP-02/03/06/07 and PWA-04.

### A7: installed-PWA experience

Prove actual installation and standalone launch. Test safe areas, visible software keyboard, orientation, large text, touch targets, back/resume, deep links and applicable offline/update behavior. Use production worker paths for realistic update tests. [Home Screen web apps](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/) and [safe areas](https://webkit.org/blog/7929/designing-websites-for-iphone-x/) provide mechanisms, not a complete current acceptance test.

Layout/visual viewports can differ; `100dvh` alone does not guarantee a reachable submit action. Test an actual software keyboard. Installation events are not universal, so platform-specific instructions need verification. Offline capabilities follow the actual product contract rather than an assumed full offline implementation. PWA-01–10.

### A8: local feasibility

Browser capture, regression, lint, accessibility checks and encoding can run locally when existing tools support them. Start with one worker and isolate performance measurements from competing load. Optional local vision must be tested for defect recall, rights and measured resource use; model weights are only a memory lower bound. Simulators cannot establish device energy, thermal or haptic behavior. [Resource guide](../reference/local-resources.md); LOCAL-01/02 and PWA-08.

## B — Skills, plugins and tool selection

### B1: capability map

Distinguish context quality (contracts, tokens, design handoffs and design skills), observation (browser/device tools) and checking (accessibility, traces, regression, gates and critique). Each supplies something different. The [18-entry radar](../skill-radar.yaml) keeps dated pins and adoption hypotheses. Inspect existing capabilities first; use the [product registry](../reference/audit-tools.yaml) to tie proposals to actual gaps.

Different coding clients have documented visual channels in the source snapshots. Their effective capability depends on version, available tools and whether the workflow actually renders and exercises states. A product/model name does not establish a quality winner.

### B2: effectiveness versus baseline

No publicly reproduced controlled ranking for this kit's complete desktop/installed-PWA contract is included. Private evaluation references and vendor demos are not reproducible target-product effect sizes. Radar effect sizes stay null.

The [protocol](../benchmark/protocol.md) plans six tasks, five configurations and three repetitions: 90 implementations per client, 270 for three clients. K4−K3 isolates the added visual loop under this design. K5−K4 combines critic and gates and needs dedicated ablations to separate their effects. Raters, surfaces and states are dependent measurements rather than additional generations. EVAL-01/02/05.

### B3: convergent generic design

Rules that ban popular fonts, colors or cards may simply converge on a different repeated default. This is a hypothesis, not a measured prevalence claim. The existing brand and task density take precedence over stylistic prohibitions.

Blind evaluations should separate AI-origin detection, brand fit, usability and cross-product diversity. Include human controls and contemporary templates; report sensitivity/specificity and false labels. No universal validated generic-design metric is supplied. EVAL-04 and DS-04.

### B4: maintenance, permissions and rights

Skills may influence actions; tools may include scripts, hooks, network requests and profile access. Review concrete versions, executable code and relevant permissions before actual adoption, with isolated data and rollback. The simulator-MCP snapshot describes a specific older command-injection issue; avoiding that version is not general security certification.

Treat runtime licenses, assets, model weights and design-reference rights separately. Review telemetry and external queries where used. [Tool review](../reference/tool-review.md); SEC-01–04.

## C — Micro-interactions and motion

### C1: pattern selection

The [14 patterns](../motion-patterns/catalog.yaml) cover press, progress, skeletons, validation, success, dialogs/sheets, context changes, lists, disclosure, drag/snap, selection, optimistic save/undo, offline/update and voice/analysis feedback. Selection follows common task needs and documented mechanisms, not a representative trend survey. Each has purpose, timing, input variants, reduced mode, code and capture status. MOT-01–04.

### C2: timing, easing and springs

Small reactions around 80–180 ms and opening/context changes around 180–280 ms are pilot heuristics. Start feedback immediately; do not delay real results. Explain spring parameters and test interruption rather than claiming a guaranteed duration. Preserve approved product tokens and justified exceptions. [Guideline](../motion-patterns/02-guideline.md); MOT-01/03.

### C3: technology and agent competence

Prefer simple CSS/WAAPI where sufficient. Use View Transitions for a suitable navigation/commit contract, Motion for demonstrated gesture/layout needs and authored Canvas assets only when justified. Browser-source version snapshots do not replace feature detection and runtime tests. Agent competence across technologies has not been measured. [Technology matrix](../motion-patterns/03-technology-matrix.md); MOT-02 and PWA-10.

### C4: accessibility and performance

The source-based WCAG 2.5.8 AA target is 24 CSS px with defined exceptions; 44 CSS px is a stricter product choice. Interaction-animation reduction under WCAG 2.3.3 is AAA and additionally required by this contract. Maintain status, focus and gesture alternatives regardless of animation.

Measure layers, paint and actual traces. The whole-frame budgets at 60/120 Hz are about 16.7/8.3 ms. Field INP/CLS are distinct from local diagnostics and transition duration. ACC-01–04, PERF-01 and PWA-08.

### C5: automated motion review

Video records progression; timestamped state/focus and frame callbacks add diagnostic context. Disabling animations helps stable snapshots but does not test natural motion. Record normal and reduced-mode behavior separately. Compressed 30/60-fps video does not prove 120-Hz displayed-frame quality. Desktop demo clips are technical examples, not usability/effectiveness measurements. MOT-04 and ACC-03.

### C6: disruptive motion and budgets

Motion harms tasks when it delays actions, overproduces frequent work, suggests false success, moves large areas, repeatedly distracts or wastes resources. Agree a bounded budget and explicit exceptions instead of a universal decorative-motion ban. Keep primary controls immediately usable. MOT-01/03; [guideline](../motion-patterns/02-guideline.md).

### C7: desktop/mobile input and haptics

Share state semantics while adapting input: hover is supplemental; touch needs clear press feedback, robust targets and a scrolling/dragging contract. Sheets suit some mobile tasks, not all. Keyboard/insets change available space. Do not promise general iOS-PWA vibration; native switch system feedback is a narrow source-described case needing real-device testing. PWA-07/08 and MOT-02.

## Adoption and open research

Start with one priority journey, actual content, a scoped baseline and reproducible states. Observe and repair evidenced gaps. Introduce a new capability only if existing tooling cannot serve the task. Retest the same flow after implementation and obtain human product/design acceptance.

Further empirical work includes exploratory interviews, controlled generations, blind expert ratings, formative user testing, judge validation and applicable installed-PWA/real-device recordings. There is no universal runner that understands every unknown product, installs/authenticates its PWA and supplies complete user-task evidence automatically.

For routine product audits, use [the universal workflow](../reference/universal-audit.md). For causal tool/method claims, use [the benchmark](../benchmark/README.md). [Validation records](evidence/validation.json) concern package behavior and consistency, not aesthetic or usability effectiveness.
