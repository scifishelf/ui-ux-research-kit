# Motion examples and recordings

[Interactive demo](demo.html), [pattern catalog](catalog.yaml), [guideline](02-guideline.md), [technology matrix](03-technology-matrix.md). All 14 MP4s demonstrate synthetic desktop states: normal interaction followed by emulated reduced motion. They are not installed-PWA or audited-product recordings.

## Reproduce

Requires Node, the pinned Playwright/Chromium runtime and ffmpeg. Work in a copy of the full kit if capture outputs should stay outside the repository.

```sh
cd motion-patterns
npm install
npx playwright install chromium
npm run capture
```

Installation writes dependencies/lockfiles and may download browser binaries. These commands belong to an explicitly authorized demo setup, not the docs-only target audit. `MOTION_FFMPEG` can select an encoder path. The runner uses a local server, captures all patterns, checks page errors/duplicate IDs/running reduced-mode animations and encodes MP4. It overwrites desktop clips and the [capture record](../report/evidence/motion-capture.json).

The demo package pins its capture runtime separately from the optional reference test loop. Read actual capture versions from the record; dated package metadata is not proof that every integration was tested.

These are component fragments, not complete product journeys. The drag demo shows a move-button alternative; the React drag fragment additionally requires equivalent keyboard/buttons in the actual product. Integrate real state, focus and acceptance behavior. Installed-PWA/real-device validation remains a separate task.
