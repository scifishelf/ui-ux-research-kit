# Motion guideline and budget

Criteria MOT-01–04, ACC-03, PERF-01 and PWA-08. Catalog timings are pilot starting points, not established optima. Preserve the product's existing semantic motion tokens and approved exceptions.

Give direct feedback at the next render where feasible. Never delay an action or result for animation. Small reactions often start around 80–180 ms; opening/context changes around 180–280 ms; exits can be shorter. Distance and context matter; on small screens reduce travel as well as duration. Spinner lifetime, undo availability and request time are not transition durations.

Use ease-out for arrival, ease-in for exit and bounded ease-in-out for reversible state changes. Linear easing fits continuous progress. `cubic-bezier(.2,0,0,1)` is an explicit example decision. Maintain shared semantic tokens; hover is supplemental for a fine pointer.

A spring follows `m*x'' + c*x' + k*x = 0`. With m=1, k=380 and c=38, damping ratio `c/(2*sqrt(k*m))` is about 0.97, near critical damping. This is a snap starting point, not a native-device replica. Velocity, distance and rest thresholds affect duration; physics parameters do not guarantee a fixed time. See [Motion transitions](https://motion.dev/docs/react-transitions).

Sequence trigger → local feedback → result. Avoid primary-action stagger chains, accept input during transitions, reverse without teleporting and set focus without animation timeouts. Announce actual states rather than frame-by-frame values.

Suggested budget, agreed before a pilot: one dominant movement plus necessary local feedback per action; main controls immediately interactive; total list stagger <=120 ms; no idle spatial loops without a purpose; no decorative Canvas runtime by default in dense task interfaces. Measure bytes in the actual build. Document justified exceptions with owner/purpose; test reduced mode and task/performance impact.

Reduced motion removes large translation, zoom, parallax and layout springs. A short fade may suit some contexts; immediate end states are a safer default for controls. Test CSS, transition pseudo-elements, JavaScript, video and Canvas separately. MotionConfig alone does not cover all mechanisms. Change the OS preference during a session and retest.

60/120 Hz provide about 16.7/8.3 ms for the **whole frame**, not JavaScript alone. Prefer transform/opacity, then inspect layers, paint, rasterization and energy. requestAnimationFrame sampling indicates callback delays, not displayed frames. A 30/60-fps recording cannot validate 120-Hz display quality. INP ends at the next paint, not at animation completion.
