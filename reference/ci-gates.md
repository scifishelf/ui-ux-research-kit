# CI and review gates

Criteria LOOP-05/06, PWA-01/04/08, ACC-01/03 and EVAL-03. Integration requires project-specific adapters; the examples are not a ready-made CI job.

Use existing typecheck/lint/unit checks, token rules, required browser/viewport states, axe, reduced motion and separate visual baselines. Successful states also need screenshots for visual review; failure-only capture is insufficient. `trace: on-first-retry` with zero retries supplies no retry trace; use `trace: on` for an explicit evidence run.

For an installed-iOS-PWA contract, use a macOS runner or documented local capture job. Linux CI does not provide an iOS simulator. Required status/artifact checks enforce review more reliably than shell configuration alone. At release include applicable real-device, offline and N-to-N+1 update tests.

The parity checker verifies one pair's identity, image hashes, installed-mode provenance and semantic/token equality. Check route/state coverage separately. Unknown MUST criteria block acceptance.

```sh
python3 reference/loop/parity_check.py "$CAPTURE_DESKTOP" "$CAPTURE_PWA" \
  --expected-build "$REVIEW_BUILD_ID" \
  --out "$CAPTURE_GATE_JSON"
```

Variables identify absolute artifact paths for a single run. Preserve existing project build/test rules. Examine the same build without deploying production. Missing runtime/keyboard evidence is unknown, not a successful skip.
