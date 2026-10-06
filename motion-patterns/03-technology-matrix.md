# Motion technology matrix

Dated research snapshot: 2026-10-04. Criteria MOT-02, PWA-10, ACC-03 and PERF-01. Agent competence has not been compared empirically; judgments below concern implementation scope.

| Technology | Use | Runtime/fallback | Integration risks | Proposed use |
| --- | --- | --- | --- | --- |
| CSS transitions / WAAPI | Controls, state and small reveals | Immediate reduced-mode fallback | Interruption and focus still need tests | Foundation |
| Same-document View Transitions | Deliberate context/navigation changes | Safari 18.0 source snapshot; feature detection and ordinary navigation | React/router commit timing, back and focus | Flow-specific trial |
| Cross-document View Transitions | Same-origin MPA navigation | Safari 18.2 snapshot; ordinary navigation | Not automatic SPA support | Architecture-specific trial |
| Scroll-driven CSS | Useful scroll-linked hints | Safari 26.0 snapshot; @supports and static fallback | Browser support and reduced mode | Trial for a real purpose |
| Motion for React | Interruptible gestures, layout and springs | Verify actual supported runtimes; reduce CSS/Canvas separately | Hydration, measurement, exit/unmount and JS cost | When CSS is insufficient |
| Rive | Authored interactive illustrations/state machines | Static image/text fallback | Asset authoring, mapping, Canvas accessibility and lifecycle | Defer until justified |
| Lottie Web | Authored icon/status assets | Verify renderer and static end frame | Export, feature compatibility and asset rights | Defer until justified |

Source snapshots: [Safari 18.0](https://webkit.org/blog/15865/webkit-features-in-safari-18-0/), [18.2](https://webkit.org/blog/16301/webkit-features-in-safari-18-2/), [26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/), [View Transitions](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API), [Motion](https://motion.dev/docs/react-transitions), [Rive](https://rive.app/docs/runtimes/web/web-js), [Lottie](https://github.com/airbnb/lottie-web).

Version claims do not replace feature detection and actual device tests. Set the product's supported floor independently. General Vibration API success haptics are not a reliable iOS-PWA foundation; system haptics for native switches are a narrow documented case to test on real devices (sources S19/S14).

To compare agent implementations, hold tasks/assets constant, repeat runs and assess syntax, state correctness, reduced motion, keyboard and measured performance. A smooth demo is not an effectiveness ranking.
