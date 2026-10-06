#!/bin/sh
# Capture an ALREADY OPENED installed PWA; no boot, install or navigation.
set -eu
: "${UI_AUDIT_UDID:?Set exact simulator UDID}"
: "${UI_AUDIT_OUT:?Set capture output folder}"
mkdir -p "$UI_AUDIT_OUT"
case "${1:-}" in
  screenshot) xcrun simctl io "$UI_AUDIT_UDID" screenshot "$UI_AUDIT_OUT/pwa.png" ;;
  video) xcrun simctl io "$UI_AUDIT_UDID" recordVideo --codec=h264 "$UI_AUDIT_OUT/pwa.mp4" ;;
  *) printf '%s\n' 'Usage: simulator-capture.sh screenshot|video (stop video with Ctrl-C after interaction)' >&2; exit 2 ;;
esac
