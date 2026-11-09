#!/bin/bash
# One take of the live 12-lead film: pre-warm, then record the rig run.
#   UDID=<ipad sim> APP=<ACLSMED.app> OUT=<raw.mov> ./capture.sh
# The iPad sim must already be turned landscape. Video only (simctl records no audio; the reel adds its own sound).
set -euo pipefail
cd "$(dirname "$0")"
BUNDLE=com.aclsmed.simulator
ARGS=(-uiDemo reel-live-12lead -shell hospital)
SECS=${SECS:-72}
xcrun simctl install "$UDID" "$APP"
DOCS="$(xcrun simctl get_app_container "$UDID" $BUNDLE data)/Documents"
mkdir -p "$DOCS"; cp out/film_cues.json "$DOCS/film_cues.json"
# pre-warm: settle the window in landscape, then quit
xcrun simctl terminate "$UDID" $BUNDLE 2>/dev/null || true
xcrun simctl launch "$UDID" $BUNDLE "${ARGS[@]}" >/dev/null; sleep 10
xcrun simctl terminate "$UDID" $BUNDLE; sleep 2
rm -f "$OUT"
xcrun simctl io "$UDID" recordVideo --codec h264 --force "$OUT" & REC=$!
sleep 2
xcrun simctl launch "$UDID" $BUNDLE "${ARGS[@]}"
sleep "$SECS"
kill -INT $REC; wait $REC || true
xcrun simctl terminate "$UDID" $BUNDLE || true
ls -la "$OUT"
