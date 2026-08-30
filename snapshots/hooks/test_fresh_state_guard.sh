#!/bin/sh
set -eu

fresh_guard_tmp="$(mktemp -d)"
trap 'rm -rf "$fresh_guard_tmp"' EXIT HUP INT TERM

printf '%s\n' '{"hook_event_name":"UserPromptSubmit","session_id":"fixture-session","turn_id":"fixture-old-pattern","prompt":"1시간마다 상태를 확인한다. 현재 완료 913개다. https://IMAGE-HOST.example/REDACTED 의 고정 404를 다시 probe한다. worker PID 83469가 살아 있다고 가정한다. 변화가 없어도 status-only로 보고하고 다음 회차까지 기다린다."}' \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/user_prompt_goal_contract.py \
  > "$fresh_guard_tmp/old-pattern.json"

if ! grep -F '"decision": "block"' "$fresh_guard_tmp/old-pattern.json" >/dev/null; then
  echo 'RED: old fixed-404/stale-PID/status-only automation prompt was accepted' >&2
  cat "$fresh_guard_tmp/old-pattern.json" >&2
  exit 1
fi

grep -F 'FRESH_STATE_CONTRACT_REQUIRED' "$fresh_guard_tmp/old-pattern.json" >/dev/null

contract_root="$fresh_guard_tmp/contracts"
runtime_root="$fresh_guard_tmp/runtime"
receipt_root="$fresh_guard_tmp/receipts"
state_path="$fresh_guard_tmp/state.json"
progress_path="$fresh_guard_tmp/progress.json"
mkdir -p "$contract_root" "$runtime_root" "$receipt_root"
printf '%s\n' '{"status":"PASS"}' > "$state_path"
printf '%s\n' '{"completed":1,"remaining":9}' > "$progress_path"

contract_path="$contract_root/fixture-hourly.json"
/usr/bin/python3 - "$contract_path" "$state_path" "$progress_path" "$receipt_root" <<'PY'
import json
import sys

contract_path, state_path, progress_path, receipt_root = sys.argv[1:]
contract = {
    "schema_version": "global_fresh_state_contract.v1",
    "contract_id": "fixture-hourly",
    "automation_id": "fixture-hourly",
    "refresh_commands": ["/fixture/process-check"],
    "canonical_state_paths": [state_path, progress_path],
    "volatile_state_paths": [state_path],
    "progress_state_paths": [progress_path],
    "receipt_root": receipt_root,
    "state_ttl_seconds": 600,
    "max_receipt_age_seconds": 900,
    "same_failure_limit": 3,
    "max_repairs_per_cycle": 1,
    "require_hash_readback": True,
    "require_progress_movement": True,
    "forbid_status_only": True,
    "require_item_specific_repair_or_escalation": True,
    "require_protected_state_preserved": True,
    "require_duplicate_claims_zero": True,
}
with open(contract_path, "w", encoding="utf-8") as handle:
    json.dump(contract, handle, sort_keys=True)
PY

contract_sha="$(/usr/bin/openssl dgst -sha256 -r "$contract_path" | awk '{print $1}')"
printf '%s  %s\n' "$contract_sha" 'fixture-hourly.json' > "$contract_path.sha256"
export CODEX_FRESH_CONTRACT_ROOT="$contract_root"
export CODEX_FRESH_RUNTIME_ROOT="$runtime_root"

printf '{"hook_event_name":"UserPromptSubmit","session_id":"fixture-session","turn_id":"fixture-valid","prompt":"매 회차 run_id와 atomic receipt를 사용한다. [GLOBAL_FRESH_STATE_CONTRACT_V1 id=fixture-hourly sha256=%s]"}\n' "$contract_sha" \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/user_prompt_goal_contract.py \
  > "$fresh_guard_tmp/valid-prompt.json"

grep -F 'global_fresh_state_guard' "$fresh_guard_tmp/valid-prompt.json" >/dev/null
if grep -F '"decision": "block"' "$fresh_guard_tmp/valid-prompt.json" >/dev/null; then
  echo 'valid runtime-bound prompt was blocked' >&2
  exit 1
fi
PROGRESS_BASELINE="$(/usr/bin/openssl dgst -sha256 -r "$progress_path" | awk '{print $1}')"
export PROGRESS_BASELINE
grep -F "$PROGRESS_BASELINE" "$fresh_guard_tmp/valid-prompt.json" >/dev/null

printf '{"hook_event_name":"UserPromptSubmit","session_id":"fixture-session","turn_id":"fixture-fixed","prompt":"매 회차 run_id를 사용하며 worker PID 83469를 현재값으로 재사용한다. [GLOBAL_FRESH_STATE_CONTRACT_V1 id=fixture-hourly sha256=%s]"}\n' "$contract_sha" \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/user_prompt_goal_contract.py \
  > "$fresh_guard_tmp/fixed-prompt.json"

grep -F 'FRESH_STATE_FIXED_MUTABLE_FACT' "$fresh_guard_tmp/fixed-prompt.json" >/dev/null

printf '{"hook_event_name":"UserPromptSubmit","session_id":"fixture-session","turn_id":"fixture-url","prompt":"매 회차 run_id를 사용하며 https://IMAGE-HOST.example/REDACTED 를 현재 blocker로 재사용한다. [GLOBAL_FRESH_STATE_CONTRACT_V1 id=fixture-hourly sha256=%s]"}\n' "$contract_sha" \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/user_prompt_goal_contract.py \
  > "$fresh_guard_tmp/fixed-url.json"
grep -F 'FRESH_STATE_FIXED_MUTABLE_FACT' "$fresh_guard_tmp/fixed-url.json" >/dev/null

printf '{"hook_event_name":"UserPromptSubmit","session_id":"fixture-session","turn_id":"fixture-counter","prompt":"매 회차 run_id를 사용하며 active_production_workers=6, completed=913을 현재값으로 재사용한다. [GLOBAL_FRESH_STATE_CONTRACT_V1 id=fixture-hourly sha256=%s]"}\n' "$contract_sha" \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/user_prompt_goal_contract.py \
  > "$fresh_guard_tmp/fixed-counter.json"
grep -F 'FRESH_STATE_FIXED_MUTABLE_FACT' "$fresh_guard_tmp/fixed-counter.json" >/dev/null

printf '%s\n' '{"hook_event_name":"UserPromptSubmit","session_id":"fixture-session","turn_id":"fixture-hash","prompt":"매 회차 run_id를 사용한다. [GLOBAL_FRESH_STATE_CONTRACT_V1 id=fixture-hourly sha256=0000000000000000000000000000000000000000000000000000000000000000]"}' \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/user_prompt_goal_contract.py \
  > "$fresh_guard_tmp/hash-mismatch.json"
grep -F 'FRESH_STATE_CONTRACT_HASH_MISMATCH' "$fresh_guard_tmp/hash-mismatch.json" >/dev/null

printf '%s\n' '{"hook_event_name":"Stop","session_id":"fixture-session","turn_id":"fixture-valid","last_assistant_message":"done\n<!-- CODEX_OUTCOME_CHAIN:COMPLETE -->\n<!-- CODEX_GOAL_GATE:PASS -->"}' \
  | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/stop_goal_gate.py \
  > "$fresh_guard_tmp/missing-receipt.json"

grep -F 'FRESH_STATE_RECEIPT_REQUIRED' "$fresh_guard_tmp/missing-receipt.json" >/dev/null

make_receipt() {
  receipt_mode="$1"
  receipt_path="$2"
  RECEIPT_MODE="$receipt_mode" CONTRACT_SHA="$contract_sha" \
    /usr/bin/python3 - "$receipt_path" "$state_path" "$progress_path" <<'PY'
import hashlib
import json
import os
import sys
import time
from pathlib import Path

receipt_path, state_path, progress_path = sys.argv[1:]
mode = os.environ["RECEIPT_MODE"]
now = time.time()

def evidence(path):
    item = Path(path)
    return {
        "path": path,
        "sha256": hashlib.sha256(item.read_bytes()).hexdigest(),
        "mtime_ns": item.stat().st_mtime_ns,
    }

progress_hash = evidence(progress_path)["sha256"]
movement = mode in {
    "pass",
    "retry",
    "forged-before",
    "forged-movement",
    "boolean-duplicate",
    "race-safe",
    "race-safe-forged-before",
    "race-safe-duplicate",
}
repair = mode == "repair"
receipt = {
    "schema_version": (
        "invalid" if mode == "race-safe-invalid-schema"
        else "global_fresh_state_cycle_receipt.v1"
    ),
    "contract_id": "fixture-hourly",
    "contract_sha256": os.environ["CONTRACT_SHA"],
    "canonical_state_observed_at_epoch": now,
    "completed_at_epoch": (
        now - 1000 if mode in {"stale", "race-safe-stale"} else now
    ),
    "state_readback": [evidence(state_path), evidence(progress_path)],
    "movement": movement,
    "movement_evidence": [{
        "path": progress_path,
        "before_sha256": (
            "2" * 64
            if mode in {"forged-before", "race-safe-forged-before"}
            else os.environ["PROGRESS_BASELINE"]
        ),
        "after_sha256": "1" * 64 if mode == "forged-movement" else progress_hash,
    }],
    "backlog_remaining": 9,
    "repair": {
        "count": 1 if repair else 0,
        "executed": repair,
        "item_key": "fixture:item" if repair else "",
        "post_repair_verified": repair,
    },
    "retry": {
        "same_failure_count": 3 if mode == "retry" else 0,
        "diagnostic_route_changed": False,
    },
    "escalation_executed": False,
    "manual_external_gate": False,
    "status_only": False,
    "duplicate_claims": (
        False if mode == "boolean-duplicate"
        else 1 if mode == "race-safe-duplicate"
        else 0
    ),
    "protected_state_preserved": True,
}
if mode.startswith("race-safe"):
    receipt["stop_finalization_protocol"] = "canonical_snapshot_v1"
with open(receipt_path, "w", encoding="utf-8") as handle:
    json.dump(receipt, handle, sort_keys=True)
PY
}

run_stop() {
  receipt_path="$1"
  output_path="$2"
  receipt_sha="$(/usr/bin/openssl dgst -sha256 -r "$receipt_path" | awk '{print $1}')"
  printf '{"hook_event_name":"Stop","session_id":"fixture-session","turn_id":"fixture-valid","last_assistant_message":"cycle result\\n<!-- CODEX_FRESH_STATE_RECEIPT path=\\"%s\\" sha256=\\"%s\\" -->\\n<!-- CODEX_OUTCOME_CHAIN:COMPLETE -->\\n<!-- CODEX_GOAL_GATE:PASS -->"}\n' "$receipt_path" "$receipt_sha" \
    | /usr/bin/python3 /Users/NEWMAC/.codex/hooks/stop_goal_gate.py \
    > "$output_path"
}

make_receipt false-waiting "$receipt_root/false-waiting.json"
run_stop "$receipt_root/false-waiting.json" "$fresh_guard_tmp/false-waiting-stop.json"
grep -F 'FALSE_WAITING_REPAIR_REQUIRED' "$fresh_guard_tmp/false-waiting-stop.json" >/dev/null

make_receipt stale "$receipt_root/stale.json"
run_stop "$receipt_root/stale.json" "$fresh_guard_tmp/stale-stop.json"
grep -F 'FRESH_STATE_RECEIPT_STALE' "$fresh_guard_tmp/stale-stop.json" >/dev/null

touch -t 202001010000 "$state_path"
make_receipt pass "$receipt_root/expired-binding.json"
run_stop "$receipt_root/expired-binding.json" "$fresh_guard_tmp/expired-binding-stop.json"
grep -F 'FRESH_STATE_VOLATILE_STATE_STALE' "$fresh_guard_tmp/expired-binding-stop.json" >/dev/null
touch "$state_path"

make_receipt repair "$receipt_root/repair.json"
run_stop "$receipt_root/repair.json" "$fresh_guard_tmp/repair-stop.json"
grep -F '"continue": true' "$fresh_guard_tmp/repair-stop.json" >/dev/null

printf '%s\n' '{"completed":2,"remaining":8}' > "$progress_path"

make_receipt forged-before "$receipt_root/forged-before.json"
run_stop "$receipt_root/forged-before.json" "$fresh_guard_tmp/forged-before-stop.json"
grep -F 'FRESH_STATE_MOVEMENT_INVALID' "$fresh_guard_tmp/forged-before-stop.json" >/dev/null

make_receipt retry "$receipt_root/retry.json"
run_stop "$receipt_root/retry.json" "$fresh_guard_tmp/retry-stop.json"
grep -F 'FRESH_STATE_RETRY_ESCALATION_REQUIRED' "$fresh_guard_tmp/retry-stop.json" >/dev/null

make_receipt forged-movement "$receipt_root/forged-movement.json"
run_stop "$receipt_root/forged-movement.json" "$fresh_guard_tmp/forged-movement-stop.json"
grep -F 'FRESH_STATE_MOVEMENT_INVALID' "$fresh_guard_tmp/forged-movement-stop.json" >/dev/null

make_receipt boolean-duplicate "$receipt_root/boolean-duplicate.json"
run_stop "$receipt_root/boolean-duplicate.json" "$fresh_guard_tmp/boolean-duplicate-stop.json"
grep -F 'FRESH_STATE_CYCLE_INVARIANT_FAILED' "$fresh_guard_tmp/boolean-duplicate-stop.json" >/dev/null

make_receipt pass "$receipt_root/post-readback-change.json"
printf '%s\n' '{"completed":2,"remaining":8}' > "$progress_path"
run_stop "$receipt_root/post-readback-change.json" "$fresh_guard_tmp/post-readback-change-stop.json"
grep -F 'FRESH_STATE_READBACK_MISMATCH' "$fresh_guard_tmp/post-readback-change-stop.json" >/dev/null

make_receipt race-safe "$receipt_root/race-safe.json"
printf '%s\n' '{"completed":3,"remaining":7}' > "$progress_path"
run_stop "$receipt_root/race-safe.json" "$fresh_guard_tmp/race-safe-stop.json"
if ! grep -F '"continue": true' "$fresh_guard_tmp/race-safe-stop.json" >/dev/null; then
  echo 'RED: canonical mutation between receipt write and Stop validation was rejected' >&2
  cat "$fresh_guard_tmp/race-safe-stop.json" >&2
  exit 1
fi
finalized_receipt="$receipt_root/race-safe.stop-finalized.json"
RACE_SOURCE_SHA="$(/usr/bin/openssl dgst -sha256 -r "$receipt_root/race-safe.json" | awk '{print $1}')"
RACE_PROGRESS_SHA="$(/usr/bin/openssl dgst -sha256 -r "$progress_path" | awk '{print $1}')"
export RACE_SOURCE_SHA RACE_PROGRESS_SHA
/usr/bin/python3 - "$finalized_receipt" "$progress_path" <<'PY'
import json
import os
import sys

finalized_path, progress_path = sys.argv[1:]
with open(finalized_path, encoding="utf-8") as handle:
    finalized = json.load(handle)
seal = finalized["stop_finalization_seal"]
assert seal["protocol"] == "canonical_snapshot_v1"
assert seal["source_receipt_sha256"] == os.environ["RACE_SOURCE_SHA"]
rows = {row["path"]: row for row in finalized["state_readback"]}
assert rows[progress_path]["sha256"] == os.environ["RACE_PROGRESS_SHA"]
assert finalized["duplicate_claims"] == 0
assert finalized["protected_state_preserved"] is True
PY

make_receipt race-safe-forged-before "$receipt_root/race-safe-forged-before.json"
printf '%s\n' '{"completed":4,"remaining":6}' > "$progress_path"
run_stop "$receipt_root/race-safe-forged-before.json" "$fresh_guard_tmp/race-safe-forged-before-stop.json"
grep -F 'FRESH_STATE_MOVEMENT_INVALID' "$fresh_guard_tmp/race-safe-forged-before-stop.json" >/dev/null

make_receipt race-safe-stale "$receipt_root/race-safe-stale.json"
run_stop "$receipt_root/race-safe-stale.json" "$fresh_guard_tmp/race-safe-stale-stop.json"
grep -F 'FRESH_STATE_RECEIPT_STALE' "$fresh_guard_tmp/race-safe-stale-stop.json" >/dev/null

make_receipt race-safe-invalid-schema "$receipt_root/race-safe-invalid-schema.json"
run_stop "$receipt_root/race-safe-invalid-schema.json" "$fresh_guard_tmp/race-safe-invalid-schema-stop.json"
grep -F 'FRESH_STATE_RECEIPT_INVALID' "$fresh_guard_tmp/race-safe-invalid-schema-stop.json" >/dev/null

make_receipt race-safe-duplicate "$receipt_root/race-safe-duplicate.json"
printf '%s\n' '{"completed":5,"remaining":5}' > "$progress_path"
run_stop "$receipt_root/race-safe-duplicate.json" "$fresh_guard_tmp/race-safe-duplicate-stop.json"
grep -F 'FRESH_STATE_CYCLE_INVARIANT_FAILED' "$fresh_guard_tmp/race-safe-duplicate-stop.json" >/dev/null

make_receipt pass "$receipt_root/pass.json"
run_stop "$receipt_root/pass.json" "$fresh_guard_tmp/pass-stop.json"
grep -F '"continue": true' "$fresh_guard_tmp/pass-stop.json" >/dev/null

echo 'fresh-state guard: 22 scenarios passed'
