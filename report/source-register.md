# Source register

Dated source snapshots; inspect original documents before relying on changed APIs or tool versions. Scope statements limit each claim.

| ID | Source | Type | Retrieved | Scope |
| --- | --- | --- | --- | --- |
| S01 | [Design2Code](https://arxiv.org/abs/2403.03163) | Research | 2026-10-04 | 484 web pages; screenshot-to-code with automated and human evaluation. Not a product-PWA study. |
| S02 | [VisualWebArena](https://arxiv.org/abs/2401.13649) | Research | 2026-10-04 | Visually grounded web tasks and observed agent failures. Not a UI design skill evaluation. |
| S03 | [Sketch2Code](https://arxiv.org/abs/2410.16232) | Research | 2026-10-04 | Interactive prototyping; clarification does not reliably produce continuous improvement. |
| S04 | [MT-Bench / LLM-as-Judge](https://arxiv.org/abs/2306.05685) | Research | 2026-10-04 | Position, verbosity and self-preference bias. Agreement on text conversations does not validate UI judgments. |
| S05 | [Rubric Artifacts](https://arxiv.org/abs/2609.02942) | Research | 2026-10-04 | Rubric wording can affect text judgments. Transfer to UI judges is a hypothesis to test. |
| S06 | [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Vendor source code | 2026-10-04 | Aesthetic direction and product-specific design; effect size in the target product is unknown. |
| S07 | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Vendor source code | 2026-10-04 | Accessibility snapshots, browser control and screenshots. A tree alone does not show aesthetics. |
| S08 | [Playwright Visual comparisons](https://playwright.dev/docs/test-snapshots) | Vendor documentation | 2026-10-04 | Browser/OS-specific baselines and screenshots captured under fixed conditions. |
| S09 | [Playwright Emulation](https://playwright.dev/docs/emulation) | Vendor documentation | 2026-10-04 | Device profiles emulate viewport, input and user agent; they do not replace an installed PWA. |
| S10 | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Vendor source code | 2026-10-04 | Traces, screenshots, network and console. Review telemetry and optional CrUX queries separately. |
| S11 | [Safari MCP](https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/) | Vendor documentation | 2026-10-04 | Local safaridriver --mcp with Safari DOM, screenshots, network and interactions. No documented standalone-iOS automation. |
| S12 | [Safari 27.0](https://webkit.org/blog/18325/webkit-features-for-safari-27-0/) | Vendor documentation | 2026-10-04 | Release article covering Safari MCP and animation improvements. Verify support in the actual runtime. |
| S13 | [Safari 26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) | Vendor documentation | 2026-10-04 | Scroll-driven animations; no guarantee of equal performance on all phones. |
| S14 | [Safari 18.0](https://webkit.org/blog/15865/webkit-features-in-safari-18-0/) | Vendor documentation | 2026-10-04 | Same-document View Transitions; system haptic feedback for native checkbox-switch controls. |
| S15 | [Safari 18.2](https://webkit.org/blog/16301/webkit-features-in-safari-18-2/) | Vendor documentation | 2026-10-04 | Cross-document View Transitions; SPA routing requires separate integration. |
| S16 | [iOS Home Screen Web Apps](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/) | Vendor documentation | 2026-10-04 | Manifest, Home Screen web apps and user-initiated push permissions. Not a complete current support test. |
| S17 | [Safe Areas](https://webkit.org/blog/7929/designing-websites-for-iphone-x/) | Vendor documentation | 2026-10-04 | Safe-area insets and viewport-fit; test current devices and installed mode separately. |
| S18 | [Viewport and keyboard](https://developer.chrome.com/blog/viewport-resize-behavior/) | Vendor documentation | 2026-10-04 | Software keyboards and visual/layout viewport behavior; actual runtime testing remains necessary. |
| S19 | [Vibration API](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API) | API reference | 2026-10-04 | Vibration API availability is limited; it is not a reliable basis for general iOS-PWA haptics. |
| S20 | [beforeinstallprompt](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeinstallprompt_event) | API reference | 2026-10-04 | Installation events are not universal; iOS guidance needs its own verified path. |
| S21 | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Standard | 2026-10-04 | Normative contrast, focus and status requirements, among others; AA is the kit target. |
| S22 | [Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) | Standard guidance | 2026-10-04 | Nonessential interaction motion can be disabled; additionally required by the kit's project contract. |
| S23 | [Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | Standard guidance | 2026-10-04 | 24 CSS px with spacing rules/exceptions; the kit's 44 CSS px product target is stricter. |
| S24 | [Modal Dialog APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Implementation guidance | 2026-10-04 | Initial focus, tab cycle, Escape and focus return; choose initial focus carefully for long content. |
| S25 | [Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) | Standard guidance | 2026-10-04 | Dragging needs an operable alternative unless a defined exception applies. |
| S26 | [axe-core](https://github.com/dequelabs/axe-core) | Vendor source code | 2026-10-04 | Automated accessibility testing is incomplete; review incomplete results manually. |
| S27 | [INP](https://web.dev/articles/inp) | Vendor documentation | 2026-10-04 | Good INP is at most 200 ms at field p75; distinguish field metrics from laboratory diagnostics. |
| S28 | [CLS](https://web.dev/articles/cls) | Vendor documentation | 2026-10-04 | Good CLS is at most 0.1; reserve space for media and loading states. |
| S29 | [Performante CSS-Animation](https://web.dev/articles/animations-guide) | Vendor documentation | 2026-10-04 | CSS/WAAPI animation mechanisms; documentation does not establish optimal product timing. |
| S30 | [Motion Accessibility](https://motion.dev/docs/react-accessibility) | Vendor documentation | 2026-10-04 | Reduced motion in React; CSS, Canvas and direct gestures require separate handling. |
| S31 | [Motion Transitions](https://motion.dev/docs/react-transitions) | Vendor documentation | 2026-10-04 | Springs, duration and physics parameters; distance/velocity affect actual timing. |
| S32 | [Rive Web](https://rive.app/docs/runtimes/web/web-js) | Vendor documentation | 2026-10-04 | WASM/Canvas runtime for authored assets and state machines; application lifecycle integration required. |
| S33 | [Lottie Web](https://github.com/airbnb/lottie-web) | Vendor source code | 2026-10-04 | Exported motion assets; treat runtime and asset licenses separately. |
| S34 | [Design Tokens 2025.10](https://www.designtokens.org/tr/2025.10/format/) | Specification | 2026-10-04 | Interchange format, not a W3C standard. Tokens alone define neither layout nor UX. |
| S35 | [Impeccable](https://github.com/pbakaus/impeccable) | Provider source code | 2026-10-04 | Design instructions, criticism, browser iteration and deterministic detectors; external product effect unmeasured. |
| S36 | [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Provider source code | 2026-10-04 | Design knowledge and system selection/generation; formulaic style selection is a risk. |
| S37 | [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | Vendor source code | 2026-10-04 | React Best Practices and Web Design Guidelines; code review does not replace visual inspection. |
| S38 | [Design Extractor](https://github.com/imehr/design-extractor) | Provider source code | 2026-10-04 | DOM/token extraction and replica iteration; similarity is not independent usability evidence. |
| S39 | [Figma MCP](https://developers.figma.com/docs/figma-mcp-server/) | Vendor documentation | 2026-10-04 | Design context, variables, components and Code Connect; add permissions and product states. |
| S40 | [iOS Simulator MCP](https://github.com/joshuayoes/ios-simulator-mcp) | Provider source code | 2026-10-04 | idb/simctl and UI control. The README describes command injection fixed before version 1.3.3. |
| S41 | [MobileBuildMCP / XcodeBuildMCP](https://github.com/getsentry/MobileBuildMCP) | Provider source code | 2026-10-04 | Successor to XcodeBuildMCP; build/simulator tools may exceed a web-only PWA's needs. |
| S42 | [Claude Code Chrome](https://code.claude.com/docs/en/chrome) | Vendor documentation | 2026-10-04 | Browser inspection integration; record actual client/tool versions and capabilities. |
| S43 | [Codex Browser](https://developers.openai.com/codex/app/browser) | Vendor documentation | 2026-10-04 | Shared browser view and visual interactions; use controlled test access. |
| S44 | [Cursor Browser](https://cursor.com/docs/agent/browser) | Vendor documentation | 2026-10-04 | Screenshots, interactions and UI correction; no established direct quality ranking. |
| S45 | [MLX-VLM](https://github.com/Blaizzy/mlx-vlm) | Provider source code | 2026-10-04 | Local vision inference on Apple Silicon. Validate model-weight license and task suitability separately. |
| S46 | [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices) | Protocol documentation | 2026-10-04 | Authorization, token handling and trust boundaries; no security certification of a server. |
| S47 | [Agent Browser](https://github.com/vercel-labs/agent-browser) | Vendor source code | 2026-10-04 | CLI browser control with element references; trial as an alternative to MCP. |
| S48 | [View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) | API reference | 2026-10-04 | Transitions do not define routing/focus semantics; use feature detection. |
| S49 | [Impeccable evaluation reference](https://github.com/pbakaus/impeccable/blob/main/CLAUDE.md) | Provider source code | 2026-10-04 | References a private evaluation repository; not publicly reproducible effect-size evidence. |
| S50 | [FronTalk](https://arxiv.org/abs/2601.04203v3) | Research | 2026-10-04 | Multiturn frontend instructions, forgetting and web-agent criticism; not evidence for design skills or iOS PWAs. |
| S51 | [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | Primary usability guidance | 2026-10-05 | General usability heuristics; verify actual usability in the target product. |
| S52 | [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) | Vendor documentation | 2026-10-05 | Public indexable web pages; not required for internal web applications. |
| S53 | [Webflow Design Trends 2026](https://webflow.com/blog/web-design-trends-2026) | Vendor trend observations | 2026-10-05 | Visual examples and art direction; neither a representative market standard nor causal usability evidence. |
| S54 | [Web Vitals](https://web.dev/articles/vitals) | Vendor documentation | 2026-10-05 | Field p75 LCP <=2.5s, INP <=200ms and CLS <=0.1; separate field measurements from laboratory tests. |
| S55 | [Skills CLI](https://github.com/vercel-labs/skills) | Vendor documentation | 2026-10-05 | CLI skill selection and project installation; no effectiveness evidence. |

Machine-readable register: [sources.yaml](sources.yaml).
