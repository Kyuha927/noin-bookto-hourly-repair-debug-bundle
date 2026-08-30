#!/bin/bash
set -euo pipefail
export LC_ALL=C
export LANG=C

[[ $# -eq 2 && "$1" == /* ]] || {
  printf 'USAGE: %s /absolute/NEWMAC_CHROME_CONTROL.json print-command|status|ensure|reconcile|run|supervise\n' "$0" >&2
  exit 2
}

CONFIG="$1"
MODE="$2"
SCRIPT="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
[[ -r "$CONFIG" && -r "${CONFIG}.sha256" ]] || {
  printf 'NEWMAC_CHROME_CONFIG_OR_CHECKSUM_MISSING\n' >&2
  exit 78
}
expected_sha="$(awk 'NR == 1 {print $1}' "${CONFIG}.sha256")"
actual_sha="$(shasum -a 256 "$CONFIG" | awk '{print $1}')"
[[ "$expected_sha" =~ ^[0-9a-f]{64}$ && "$expected_sha" == "$actual_sha" ]] || {
  printf 'NEWMAC_CHROME_CONFIG_CHECKSUM_MISMATCH\n' >&2
  exit 78
}

jq_string() {
  jq -er "$1 | select(type == \"string\" and length > 0)" "$CONFIG"
}

[[ "$(jq -er '.schema_version' "$CONFIG")" == "1" ]] || exit 78
ROOT="$(jq_string '.root')"
CHROME_PATH="$(jq_string '.chrome_path')"
CHROME_MODE="$(jq_string '.chrome_mode')"
CHROME_PROFILE="$(jq_string '.chrome_profile')"
CHROME_SCREEN="$(jq_string '.chrome_screen')"
KEEPALIVE_SCREEN="$(jq_string '.keepalive_screen')"
PROXY_SERVER="$(jq_string '.proxy_server')"
CPU_GUARD="$(jq_string '.cpu_guard')"
BACKGROUND_GATE="$(jq_string '.background_gate')"
SCRAPER_LOCK="$(jq_string '.scraper_lock')"
SCRAPER_CHILD_PID="$(jq_string '.scraper_child_pid')"
SCRAPER_TARGETS_DIR="$(jq_string '.scraper_targets_dir')"
SCRAPER_KEEPALIVE="$(jq_string '.scraper_keepalive')"
CDP_PORT="$(jq -er '.cdp_port | select(type == "number")' "$CONFIG")"
STATE="$ROOT/NEWMAC_CHROME_CONTROL_STATE.json"
LOG="$ROOT/supervisor_logs/newmac_chrome_control.log"
ENSURE_LOCK="$ROOT/runtime/newmac_chrome_control.lock"

[[ "$ROOT" == /Users/NEWMAC/Documents/webtoon/* ]]
[[ "$CHROME_PROFILE" == "$ROOT"/* ]]
[[ "$SCRAPER_LOCK" == "$ROOT"/* && "$SCRAPER_CHILD_PID" == "$ROOT"/* ]]
[[ "$SCRAPER_TARGETS_DIR" == "$ROOT"/* ]]
[[ "$PROXY_SERVER" =~ ^socks5://127[.]0[.]0[.]1:([0-9]+)$ ]]
PROXY_PORT="${BASH_REMATCH[1]}"
[[ -x "$CHROME_PATH" && -x "$CPU_GUARD" && -x "$BACKGROUND_GATE" ]]
[[ -x "$SCRAPER_KEEPALIVE" && -x "$SCRIPT" ]]
[[ "$CHROME_MODE" == "background_headful" ]]
mkdir -p "$ROOT/runtime" "$ROOT/supervisor_logs" "$CHROME_PROFILE" "$SCRAPER_TARGETS_DIR"

chrome_argv=(
  "$CHROME_PATH"
  --no-startup-window
  --disable-gpu
  "--remote-debugging-port=$CDP_PORT"
  --remote-allow-origins=\*
  "--user-data-dir=$CHROME_PROFILE"
  "--proxy-server=$PROXY_SERVER"
  --no-first-run
  --no-default-browser-check
)

screen_count() {
  { screen -ls 2>/dev/null || true; } |
    awk -v name="$1" '$1 ~ ("^[0-9]+[.]" name "$") {count++} END {print count + 0}'
}

listener_pids() {
  lsof -nP -iTCP:"$CDP_PORT" -sTCP:LISTEN -t 2>/dev/null | sort -u
}

listener_count() {
  listener_pids | awk 'NF {count++} END {print count + 0}'
}

listener_pid() {
  listener_pids | head -1
}

proxy_alive() {
  /usr/bin/python3 - "$PROXY_PORT" <<'PY'
import socket
import sys

connection = socket.create_connection(("127.0.0.1", int(sys.argv[1])), timeout=2)
connection.close()
PY
}

cdp_alive() {
  /usr/bin/python3 - "$CDP_PORT" <<'PY'
import http.client
import json
import sys

try:
    connection = http.client.HTTPConnection("127.0.0.1", int(sys.argv[1]), timeout=2)
    connection.request("GET", "/json/version")
    response = connection.getresponse()
    payload = json.loads(response.read().decode("utf-8"))
    connection.close()
    raise SystemExit(0 if response.status == 200 and str(payload.get("Browser", "")).startswith("Chrome/") else 1)
except (OSError, ValueError, json.JSONDecodeError):
    raise SystemExit(1)
PY
}

argv_matches() {
  [[ "$(listener_count)" -eq 1 ]] || return 1
  local pid command
  pid="$(listener_pid)"
  command="$(ps -p "$pid" -o command= 2>/dev/null || true)"
  [[ "$command" == *"--remote-debugging-port=$CDP_PORT"* ]]
  [[ "$command" == *"--user-data-dir=$CHROME_PROFILE"* ]]
  [[ "$command" == *"--proxy-server=$PROXY_SERVER"* ]]
  [[ "$command" == *"--no-startup-window"* ]]
  [[ "$command" != *"--headless"* ]]
}

write_state() {
  local state="$1" action="$2" temporary
  temporary="$ROOT/.NEWMAC_CHROME_CONTROL_STATE.json.tmp.$$"
  jq -n \
    --arg state "$state" --arg action "$action" \
    --arg updated_at "$(date '+%Y-%m-%dT%H:%M:%S%z')" \
    --arg listener_pid "$(listener_pid 2>/dev/null || true)" \
    --arg proxy_server "$PROXY_SERVER" \
    --arg chrome_mode "$CHROME_MODE" \
    --argjson cdp_port "$CDP_PORT" \
    --argjson listeners "$(listener_count)" \
    --argjson chrome_screens "$(screen_count "$CHROME_SCREEN")" \
    --argjson keepalive_screens "$(screen_count "$KEEPALIVE_SCREEN")" \
    '{schema_version:1,state:$state,action:$action,updated_at:$updated_at,cdp_port:$cdp_port,proxy_server:$proxy_server,chrome_mode:$chrome_mode,listeners:$listeners,listener_pid:$listener_pid,chrome_screens:$chrome_screens,keepalive_screens:$keepalive_screens,background_only:true}' \
    >"$temporary"
  mv -f "$temporary" "$STATE"
}

status() {
  local state="DRIFT"
  if proxy_alive && cdp_alive && argv_matches \
    && [[ "$(screen_count "$CHROME_SCREEN")" -eq 1 ]] \
    && [[ "$(screen_count "$KEEPALIVE_SCREEN")" -eq 1 ]]; then
    state="PASS"
  fi
  write_state "$state" "status_read"
  jq '.' "$STATE"
  [[ "$state" == "PASS" ]]
}

launch_once() {
  local gate_output
  proxy_alive
  "$CPU_GUARD" >>"$LOG" 2>&1
  gate_output="$("$BACKGROUND_GATE" 2>&1)" || return 78
  printf '%s\n' "$gate_output" >>"$LOG"
  jq -e '.state == "IDLE"' <<<"$gate_output" >/dev/null
  [[ "$(listener_count)" -eq 0 ]]
  [[ "$(screen_count "$CHROME_SCREEN")" -eq 0 ]]
  screen -dmS "$CHROME_SCREEN" "$SCRIPT" "$CONFIG" run
  for _attempt in {1..40}; do
    if cdp_alive && argv_matches; then
      return 0
    fi
    sleep 0.5
  done
  return 78
}

ensure_once() {
  local count
  count="$(listener_count)"
  [[ "$count" -le 1 ]]
  [[ "$(screen_count "$CHROME_SCREEN")" -le 1 ]]
  if [[ "$count" -eq 0 ]]; then
    launch_once
  else
    argv_matches
  fi
}

ensure_keepalive() {
  [[ "$(screen_count "$KEEPALIVE_SCREEN")" -le 1 ]]
  if [[ "$(screen_count "$KEEPALIVE_SCREEN")" -eq 0 ]]; then
    screen -dmS "$KEEPALIVE_SCREEN" "$SCRIPT" "$CONFIG" supervise
  fi
}

with_lock() {
  mkdir "$ENSURE_LOCK" 2>/dev/null || return 75
  local rc
  set +e
  (set -e; "$@")
  rc=$?
  set -e
  rmdir "$ENSURE_LOCK" 2>/dev/null || true
  return "$rc"
}

ensure() {
  if ! with_lock ensure_once; then
    status || true
    return 78
  fi
  ensure_keepalive
  sleep 1
  status
}

close_browser() {
  /usr/bin/python3 - "$CDP_PORT" <<'PY'
import http.client
import json
import sys
import websocket

port = int(sys.argv[1])
connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
connection.request("GET", "/json/version")
response = connection.getresponse()
payload = json.loads(response.read().decode("utf-8"))
connection.close()
browser_url = payload["webSocketDebuggerUrl"]
socket = websocket.create_connection(browser_url, timeout=5, suppress_origin=True)
socket.send(json.dumps({"id": 1, "method": "Browser.close"}))
try:
    socket.recv()
except websocket.WebSocketConnectionClosedException:
    pass
finally:
    socket.close()
PY
}

reconcile_locked() {
  proxy_alive
  [[ "$(listener_count)" -eq 1 ]]
  local old_pid old_command controller_pid controller_command keepalive_pid keepalive_command
  old_pid="$(listener_pid)"
  old_command="$(ps -p "$old_pid" -o command=)"
  [[ "$old_command" == *"--remote-debugging-port=$CDP_PORT"* ]]
  [[ "$old_command" == *"--user-data-dir=$CHROME_PROFILE"* ]]

  controller_pid="$(jq -er '.pid | select(type == "number")' "$SCRAPER_LOCK")"
  controller_command="$(ps -p "$controller_pid" -o command=)"
  [[ "$controller_command" == *"bookto_singleton.py $SCRAPER_LOCK /bin/bash $SCRAPER_KEEPALIVE"* ]]
  keepalive_pid="$(ps -axo pid=,ppid=,command= | awk -v parent="$controller_pid" -v script="$SCRAPER_KEEPALIVE" '$2 == parent && $3 == "/bin/bash" && index($0, script) {print $1}')"
  [[ "$keepalive_pid" =~ ^[0-9]+$ ]]
  keepalive_command="$(ps -p "$keepalive_pid" -o command=)"
  [[ "$keepalive_command" == "/bin/bash $SCRAPER_KEEPALIVE" ]]
  kill -STOP "$controller_pid" "$keepalive_pid"
  trap "kill -CONT $keepalive_pid $controller_pid 2>/dev/null || true" EXIT INT TERM
  sleep 1

  if [[ -r "$SCRAPER_CHILD_PID" ]]; then
    local child_pid
    child_pid="$(sed -n '1p' "$SCRAPER_CHILD_PID")"
    if [[ "$child_pid" =~ ^[0-9]+$ ]] && kill -0 "$child_pid" 2>/dev/null; then
      return 78
    fi
  fi
  [[ -z "$(find "$SCRAPER_TARGETS_DIR" -maxdepth 1 -type f -name '*.json' -print -quit 2>/dev/null)" ]]

  close_browser
  for _attempt in {1..30}; do
    [[ "$(listener_count)" -eq 0 ]] && break
    sleep 0.5
  done
  [[ "$(listener_count)" -eq 0 ]]
  launch_once
  ensure_keepalive
  kill -CONT "$keepalive_pid" "$controller_pid"
  trap - EXIT INT TERM
}

reconcile() {
  with_lock reconcile_locked
  sleep 1
  status
}

supervise() {
  while :; do
    set +e
    ensure_once >>"$LOG" 2>&1
    rc=$?
    status >>"$LOG" 2>&1
    set -e
    [[ "$rc" -eq 0 ]] || sleep 30
    sleep 30
  done
}

print_command() {
  printf '%s\n' "${chrome_argv[@]}" |
    jq -Rsc --arg proxy "$PROXY_SERVER" --arg mode "$CHROME_MODE" --argjson port "$CDP_PORT" \
      '{status:"PASS",background_only:true,chrome_mode:$mode,cdp_port:$port,proxy_server:$proxy,argv:(split("\n")[:-1])}'
}

case "$MODE" in
  print-command) print_command ;;
  status) status ;;
  ensure) ensure ;;
  reconcile) reconcile ;;
  run) exec "${chrome_argv[@]}" ;;
  supervise) supervise ;;
  *) printf 'NEWMAC_CHROME_MODE_INVALID:%s\n' "$MODE" >&2; exit 2 ;;
esac
