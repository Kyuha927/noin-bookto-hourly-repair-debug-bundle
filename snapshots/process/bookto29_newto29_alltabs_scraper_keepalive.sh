#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_20260825"
CONFIG="$ROOT/multitab_config.json"
PYTHONPATH_VALUE="/Users/NEWMAC/Documents/webtoon"
LOG="$ROOT/supervisor_logs/scraper.log"
LOCK="$ROOT/runtime/scraper.singleton.lock"
CHILD_PID="$ROOT/runtime/scraper.child.pid"
BACKGROUND_GATE="/Users/NEWMAC/.local/bin/agent-background-computer-use-gate"
ROTATOR="/Users/NEWMAC/Documents/webtoon/bookto_multitab_rotation.py"
mkdir -p "$ROOT/supervisor_logs" "$ROOT/runtime"
if [[ "${BOOKTO_SCRAPER_KERNEL_LOCK_HELD:-}" != "1" ]]; then
  export BOOKTO_SCRAPER_KERNEL_LOCK_HELD=1
  exec /usr/bin/python3 /Users/NEWMAC/Documents/webtoon/bookto_singleton.py \
    "$LOCK" /bin/bash "$0"
fi
cleanup() {
  if [[ -f "$CHILD_PID" ]]; then
    child_pid="$(<"$CHILD_PID")"
    if kill -0 "$child_pid" 2>/dev/null; then
      kill -TERM "$child_pid" 2>/dev/null || true
      wait "$child_pid" 2>/dev/null || true
    fi
  fi
  PYTHONPATH="$PYTHONPATH_VALUE" /usr/bin/python3 /Users/NEWMAC/Documents/webtoon/bookto_multitab_cdp.py \
    --config "$CONFIG" --cleanup-targets >> "$LOG" 2>&1 || true
  rm -f "$CHILD_PID"
}
trap cleanup EXIT

while :; do
  set +e
  gate_output="$($BACKGROUND_GATE 2>&1)"
  gate_rc=$?
  set -e
  if ! jq -e '.state == "IDLE" or .state == "ACTIVE" or .state == "UNKNOWN"' <<< "$gate_output" >/dev/null 2>&1; then
    gate_output='{"decision":"DENY_FOREGROUND","state":"UNKNOWN"}'
  fi
  printf '%s background_gate_rc=%s background_gate=%s enforced_mode=BACKGROUND_ONLY\n' "$(date -Is)" "$gate_rc" "$gate_output" >> "$LOG"
  if ! jq -e '.background_only == true and .workers == 4' "$CONFIG" >/dev/null; then
    printf '%s BLOCKED_BACKGROUND_OR_PARALLEL_CONFIG_INVARIANT\n' "$(date -Is)" >> "$LOG"
    sleep 300
    continue
  fi
  printf '%s scraper_cycle_start\n' "$(date -Is)" >> "$LOG"
  set +e
  PYTHONPATH="$PYTHONPATH_VALUE" /usr/bin/python3 /Users/NEWMAC/Documents/webtoon/bookto_multitab_cdp.py \
    --config "$CONFIG" --phase scrape --max-items 4 >> "$LOG" 2>&1 &
  child_pid=$!
  printf '%s\n' "$child_pid" > "$CHILD_PID"
  wait "$child_pid"
  rc=$?
  rm -f "$CHILD_PID"
  set -e
  printf '%s scraper_cycle_exit=%s\n' "$(date -Is)" "$rc" >> "$LOG"
  rotation_failed=0
  if jq -e '.items | to_entries[] | select((.value.error // "") | contains("SITE_ROUTE_UNAVAILABLE"))' "$ROOT/SCRAPE_STATE.json" >/dev/null 2>&1; then
    current_suffix="$(jq -r '.domain_suffix' "$CONFIG")"
    next_suffix="$((current_suffix + 1))"
    printf '%s exact_plus_one_probe current=%s target=%s\n' "$(date -Is)" "$current_suffix" "$next_suffix" >> "$LOG"
    set +e
    rotation_output="$(PYTHONPATH="$PYTHONPATH_VALUE" /usr/bin/python3 "$ROTATOR" \
      --config "$CONFIG" --expected-suffix "$current_suffix" --target-suffix "$next_suffix" 2>&1)"
    rotation_rc=$?
    set -e
    printf '%s domain_rotation_rc=%s result=%s\n' "$(date -Is)" "$rotation_rc" "$rotation_output" >> "$LOG"
    if [[ "$rotation_rc" -eq 0 ]]; then
      continue
    fi
    rotation_failed=1
  fi
  if jq -e '.items | to_entries[] | select((.value.status == "RETRYABLE_EXTERNAL_IMAGE_ROUTE" or .value.status == "BLOCKED_NEEDS_USER_EXTERNAL_ACTION") and ((.value.error // "") | startswith("IMAGE_ROUTE_UNAVAILABLE:")))' "$ROOT/SCRAPE_STATE.json" >/dev/null 2>&1; then
    printf '%s waiting_for_external_image_route_one_item_probe\n' "$(date -Is)" >> "$LOG"
    sleep 30
  elif jq -e '.items | to_entries[] | select(.value.status == "BLOCKED_NEEDS_USER_EXTERNAL_ACTION")' "$ROOT/SCRAPE_STATE.json" >/dev/null 2>&1; then
    printf '%s cloudflare_blocker_preserved_other_backlog_continues\n' "$(date -Is)" >> "$LOG"
    sleep 30
  elif [[ "$rotation_failed" -eq 1 ]]; then
    sleep 300
  else
    sleep 30
  fi
done
