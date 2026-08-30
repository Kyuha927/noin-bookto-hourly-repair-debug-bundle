#!/bin/bash
set -euo pipefail
export LC_ALL=C
export LANG=C

if [[ $# -ne 2 ]]; then
  echo "usage: $0 /Users/<newmac> /Users/<oldmac>" >&2
  exit 64
fi

BUNDLE_NEWMAC_HOME=$1
BUNDLE_OLDMAC_HOME=$2
export BUNDLE_NEWMAC_HOME BUNDLE_OLDMAC_HOME

BUNDLE_ROOT=$(cd "$(dirname "$0")/.." && pwd)
WEBTOON_ROOT="$BUNDLE_NEWMAC_HOME/Documents/webtoon"
LANE_ROOT="$WEBTOON_ROOT/bookto29_newto29_alltabs_20260825"
CODEX_ROOT="$BUNDLE_NEWMAC_HOME/.codex"

mkdir -p \
  "$BUNDLE_ROOT/metadata" \
  "$BUNDLE_ROOT/snapshots/automation" \
  "$BUNDLE_ROOT/snapshots/contracts" \
  "$BUNDLE_ROOT/snapshots/hooks" \
  "$BUNDLE_ROOT/snapshots/process" \
  "$BUNDLE_ROOT/snapshots/scraper" \
  "$BUNDLE_ROOT/snapshots/controls" \
  "$BUNDLE_ROOT/snapshots/tests" \
  "$BUNDLE_ROOT/snapshots/state" \
  "$BUNDLE_ROOT/snapshots/receipts"

HASH_FILE="$BUNDLE_ROOT/metadata/SOURCE_HASHES.tsv"
: > "$HASH_FILE"
printf 'sha256\tsanitized_path\tsource_path\n' >> "$HASH_FILE"

sanitize_copy() {
  local source_path=$1
  local relative_path=$2
  local destination="$BUNDLE_ROOT/$relative_path"
  mkdir -p "$(dirname "$destination")"
  perl -0pe '
    BEGIN {
      $newmac = quotemeta($ENV{"BUNDLE_NEWMAC_HOME"});
      $oldmac = quotemeta($ENV{"BUNDLE_OLDMAC_HOME"});
    }
    s/$newmac/\/Users\/NEWMAC/g;
    s/$oldmac/\/Users\/OLDMAC/g;
    s#https://(?:bookto|newto)\d+\.com#https://ROTATING-HOST.example#g;
    s{https?://img[^\s\"]+}{https://IMAGE-HOST.example/REDACTED}g;
    s#socks5://127\.0\.0\.1:\d+#socks5://127.0.0.1:<PORT>#g;
    s#\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b#<PRIVATE-IP>#g;
    s#(target_thread_id\s*=\s*")[^"]+("\s*)#$1<THREAD-ID>$2#g;
    s/\bmacpro\b/NEWMAC_USER/g;
  ' "$source_path" > "$destination"
  local digest
  local display_source
  digest=$(LC_ALL=C /usr/bin/shasum -a 256 "$source_path" | awk '{print $1}')
  if [[ "$source_path" == "$BUNDLE_NEWMAC_HOME"* ]]; then
    display_source="/Users/NEWMAC${source_path#"$BUNDLE_NEWMAC_HOME"}"
  elif [[ "$source_path" == "$BUNDLE_OLDMAC_HOME"* ]]; then
    display_source="/Users/OLDMAC${source_path#"$BUNDLE_OLDMAC_HOME"}"
  else
    display_source=$source_path
  fi
  printf '%s\t%s\t%s\n' "$digest" "$relative_path" "$display_source" >> "$HASH_FILE"
}

record_source_hash() {
  local source_path=$1
  local logical_path=$2
  local digest
  local display_source
  digest=$(LC_ALL=C /usr/bin/shasum -a 256 "$source_path" | awk '{print $1}')
  if [[ "$source_path" == "$BUNDLE_NEWMAC_HOME"* ]]; then
    display_source="/Users/NEWMAC${source_path#"$BUNDLE_NEWMAC_HOME"}"
  elif [[ "$source_path" == "$BUNDLE_OLDMAC_HOME"* ]]; then
    display_source="/Users/OLDMAC${source_path#"$BUNDLE_OLDMAC_HOME"}"
  else
    display_source=$source_path
  fi
  printf '%s\t%s\t%s\n' "$digest" "$logical_path" "$display_source" >> "$HASH_FILE"
}

sanitize_copy "$CODEX_ROOT/automations/noin-bookto29-newto29-alltabs-hourly-repair/automation.toml" snapshots/automation/automation.toml
sanitize_copy "$CODEX_ROOT/hooks/contracts/noin-bookto29-newto29-alltabs-hourly-repair.json" snapshots/contracts/fresh_state_contract.json
sanitize_copy "$CODEX_ROOT/hooks/contracts/noin-bookto29-newto29-alltabs-hourly-repair.json.sha256" snapshots/contracts/fresh_state_contract.json.sha256
sanitize_copy "$CODEX_ROOT/hooks/fresh_state_receipt.py" snapshots/hooks/fresh_state_receipt.py
sanitize_copy "$CODEX_ROOT/hooks/fresh_state_receipt_validation.py" snapshots/hooks/fresh_state_receipt_validation.py
sanitize_copy "$CODEX_ROOT/hooks/test_fresh_state_guard.sh" snapshots/hooks/test_fresh_state_guard.sh

sanitize_copy "$WEBTOON_ROOT/bookto29_newto29_alltabs_process_check.sh" snapshots/process/bookto29_newto29_alltabs_process_check.sh
sanitize_copy "$WEBTOON_ROOT/bookto_process_contract_check.py" snapshots/process/bookto_process_contract_check.py
sanitize_copy "$WEBTOON_ROOT/bookto_process_contract_check.py.sha256" snapshots/process/bookto_process_contract_check.py.sha256
sanitize_copy "$LANE_ROOT/PROCESS_CONTRACT.json" snapshots/process/PROCESS_CONTRACT.json
sanitize_copy "$WEBTOON_ROOT/bookto_singleton.py" snapshots/process/bookto_singleton.py
sanitize_copy "$WEBTOON_ROOT/bookto29_newto29_alltabs_scraper_keepalive.sh" snapshots/process/bookto29_newto29_alltabs_scraper_keepalive.sh

for name in \
  bookto_multitab_cdp.py \
  bookto_multitab_cdp_core.py \
  bookto_multitab_config.py \
  bookto_multitab_output.py \
  bookto_multitab_progress.py \
  bookto_multitab_schedule.py \
  bookto_multitab_state.py \
  bookto_multitab_state_persistence.py \
  bookto_multitab_targets.py \
  bookto_multitab_work_queue.py; do
  sanitize_copy "$WEBTOON_ROOT/$name" "snapshots/scraper/$name"
done

sanitize_copy "$WEBTOON_ROOT/bookto_multitab_rotation.py" snapshots/controls/bookto_multitab_rotation.py
sanitize_copy "$WEBTOON_ROOT/bookto_multitab_rotation_artifacts.py" snapshots/controls/bookto_multitab_rotation_artifacts.py
sanitize_copy "$WEBTOON_ROOT/bookto_multitab_remote_route_sync.py" snapshots/controls/bookto_multitab_remote_route_sync.py
sanitize_copy "$WEBTOON_ROOT/bookto_multitab_newmac_chrome_control.sh" snapshots/controls/bookto_multitab_newmac_chrome_control.sh
sanitize_copy "$LANE_ROOT/distributed/bookto30-newto30-oldmac-smoke-g1/bookto_multitab_runtime_binding.sh" snapshots/controls/bookto_multitab_runtime_binding.sh

sanitize_copy "$WEBTOON_ROOT/test_bookto_multitab_rotation.py" snapshots/tests/test_bookto_multitab_rotation.py
sanitize_copy "$WEBTOON_ROOT/test_bookto_multitab_remote_route_sync.py" snapshots/tests/test_bookto_multitab_remote_route_sync.py
sanitize_copy "$WEBTOON_ROOT/test_bookto_multitab_newmac_chrome_control.sh" snapshots/tests/test_bookto_multitab_newmac_chrome_control.sh
sanitize_copy "$LANE_ROOT/distributed/bookto30-newto30-oldmac-smoke-g1/test_bookto_multitab_runtime_binding_live.sh" snapshots/tests/test_bookto_multitab_runtime_binding_live.sh

sanitize_copy "$LANE_ROOT/PROCESS_STATUS.json" snapshots/state/PROCESS_STATUS.json
sanitize_copy "$LANE_ROOT/LEARNING_INTAKE_STATE.json" snapshots/state/LEARNING_INTAKE_STATE.json
sanitize_copy "$LANE_ROOT/VISUAL_WORKER_STATE.json" snapshots/state/VISUAL_WORKER_STATE.json
sanitize_copy "$LANE_ROOT/ACTIVE_GENERATION.json" snapshots/state/ACTIVE_GENERATION.json
sanitize_copy "$LANE_ROOT/NEWMAC_CHROME_CONTROL.json" snapshots/state/NEWMAC_CHROME_CONTROL.json
sanitize_copy "$LANE_ROOT/multitab_config.json" snapshots/state/multitab_config.json
sanitize_copy "$LANE_ROOT/distributed/bookto30-newto30-oldmac-smoke-g1/NEWMAC_RUNTIME_BINDING.json" snapshots/state/NEWMAC_RUNTIME_BINDING.json
sanitize_copy "$LANE_ROOT/distributed/bookto30-newto30-oldmac-smoke-g1/PAIR_VALIDATION.json" snapshots/state/PAIR_VALIDATION.json

jq '{schema_version,generation_id,catalog_count,updated_at,status_counts:(.items|to_entries|map(.value.status // "UNKNOWN")|sort|group_by(.)|map({key:.[0],value:length})|from_entries),oldest_nonpass:(.items|to_entries|map(select((.value.status // "") != "PASS"))|sort_by(.value.updated_at // "")|.[0:25]|map({item_key:.key,status:.value.status,updated_at:.value.updated_at,error:.value.error}))}' "$LANE_ROOT/SCRAPE_STATE.json" > "$BUNDLE_ROOT/snapshots/state/SCRAPE_STATE.summary.raw.json"
sanitize_copy "$BUNDLE_ROOT/snapshots/state/SCRAPE_STATE.summary.raw.json" snapshots/state/SCRAPE_STATE.summary.json
rm "$BUNDLE_ROOT/snapshots/state/SCRAPE_STATE.summary.raw.json"
record_source_hash "$LANE_ROOT/SCRAPE_STATE.json" snapshots/state/SCRAPE_STATE.summary.json#full-source

jq '{schema,known_ids_count:(.known_ids|length)}' "$LANE_ROOT/WEBTOON_STATE.json" > "$BUNDLE_ROOT/snapshots/state/WEBTOON_STATE.summary.json"
record_source_hash "$LANE_ROOT/WEBTOON_STATE.json" snapshots/state/WEBTOON_STATE.summary.json#full-source

for receipt_name in \
  20260831T033907+0900-7ca06968_global_fresh_state_cycle_receipt.stop-finalized.json \
  20260831T043953+0900-f896a581_global_fresh_state_cycle_receipt.stop-finalized.json \
  20260831T053943+0900-313d7ec9_global_fresh_state_cycle_receipt.stop-finalized.json \
  20260831T070824+0900-20202b0a_global_fresh_state_cycle_receipt.json \
  20260831T071342+0900-fe292947_global_fresh_state_cycle_receipt.json; do
  sanitize_copy "$LANE_ROOT/watchdog_receipts/$receipt_name" "snapshots/receipts/$receipt_name"
done

if rg -n --hidden --glob '!.git/**' \
  '(gh[opusr]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|Authorization:[[:space:]]*Bearer[[:space:]]+[A-Za-z0-9._-]{20,})' \
  "$BUNDLE_ROOT"; then
  echo 'high-confidence secret pattern found; refusing bundle' >&2
  exit 78
fi

echo "bundle generated at $BUNDLE_ROOT"
