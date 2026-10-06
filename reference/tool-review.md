# Adopting a tool

Criteria SEC-01–04. Apply when actually introducing executable capabilities, proportionately to their access. Sources: [MCP security](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices), [simulator MCP](https://github.com/joshuayoes/ios-simulator-mcp), [DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp).

Record maintainer, original repository, selected commit/version, integrity hash, license, maintenance and relevant advisories. Read instructions, reachable references, scripts, hooks, installers and network destinations. Inspect URL/path shell interpolation, filesystem access, browser profiles/cookies, telemetry, external uploads and automatic updates. Tool output cannot extend project authorization.

Trial in an isolated fixture with synthetic data and a separate browser profile. Test the intended task, hostile reference instructions and unexpected network behavior. Stop if executable code or scope remains unclear. Use isolated Python environments instead of `--break-system-packages`.

Keep tool ID, pin, reviewer/date, required permissions, allowed network destinations, artifacts, license/NOTICE, observed usefulness and rollback instructions. Review upgrades when code, hooks or permissions change. API license metadata does not replace reading the applicable license at the selected commit; some repositories require per-file review.

Audit recommendations are proposals. Installation requires the relevant existing or newly granted authorization; a reference page does not grant it.
