# Shared desktop/PWA capture loop

Criteria LOOP-02/03/06/07, PWA-01–05 and MOT-04. Integration templates, not universal installed-PWA automation. The pair checker specifically implements an optional desktop/iOS-PWA study contract.

1. Produce an isolated production build from a clear source state. A commit alone is insufficient for a dirty working tree. Assign immutable `buildId`, `tokenVersion`, `fixtureId` and `runId`; use the same build on both surfaces.
2. Desktop: set route, state, theme, locale, motion and viewport; await fonts/data; capture screenshot, semantic/DOM data and applicable video. [browser.spec.ts](browser.spec.ts) shows an application-specific fixture contract.
3. PWA: install using the supported runtime, then actually launch the Home Screen application. Opening a Safari URL does not launch standalone mode. Check standalone-container login/cookies separately. Expose reviewed read-only diagnostics from [capture-probe.js](capture-probe.js).
4. Use available supported device/simulator adapters to exercise states and the visible software keyboard. [simulator-capture.sh](simulator-capture.sh) records screenshots/video; those alone contain no DOM or reliable application/worker identity.
5. Create manifests using [capture.schema.json](capture.schema.json), recording image SHA-256. Run [parity_check.py](parity_check.py) against the expected build. Check the full state matrix separately. Compare each image with its own platform baseline; compare shared actions/tokens by meaning.
6. Review the complete evidence bundle in fresh context. Corrections require a new build identity and fresh captures. Human review checks actual task completion and brand fit.

`simctl` supports screenshots, video and URLs, but not universally reliable Home Screen installation or PWA DOM extraction. Reuse an existing adapter where available. Preserve simulator/apps/processes outside the assignment.

Distinguish the UI build from the **currently controlling service worker's own immutable build ID**. A registration object or script URL is insufficient. The probe uses a `MessageChannel` handshake; the application/worker must implement this explicit contract.

Synthetic manifests test gate behavior, not installed-PWA compliance. Exercise negative cases for a stale worker and missing PWA capture after integration. Captures establish only the actions actually performed, not general usability or aesthetics.
