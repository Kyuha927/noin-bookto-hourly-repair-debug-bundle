#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

ROOT="/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_20260825/distributed/bookto30-newto30-oldmac-smoke-g1"
LANE_ROOT="/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_20260825"
PROCESS_CHECKER="/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_process_check.sh"
PROCESS_STATUS="$LANE_ROOT/PROCESS_STATUS.json"
NEWMAC_CONFIG="$LANE_ROOT/multitab_config.json"
NEWMAC_ASSIGNMENT="$ROOT/NEWMAC_ASSIGNMENT.json"
OLDMAC_ASSIGNMENT="$ROOT/OLDMAC_ASSIGNMENT.json"
OLDMAC_CONFIG="$ROOT/OLDMAC_multitab_config.json"
PAIR="$ROOT/PAIR_VALIDATION.json"
CATALOG="$LANE_ROOT/CATALOG.json"
PRIORITY="$LANE_ROOT/PRIORITY.jsonl"
REMOTE_ROUTE_SYNC="/Users/NEWMAC/Documents/webtoon/bookto_multitab_remote_route_sync.py"
VALIDATOR="$ROOT/bookto_multitab_newmac_binding_check.sh"
BINDING="$ROOT/NEWMAC_RUNTIME_BINDING.json"
REMOTE_HOST="oldmac"
REMOTE_ROOT="/Users/OLDMAC/Documents/webtoon/bookto30_newto30_alltabs_oldmac_smoke_20260827"
REMOTE_CONFIG="$REMOTE_ROOT/multitab_config.json"
TTL_SECONDS=5400

fail() {
  printf '%s\n' "$1" >&2
  exit 78
}

sha256_file() {
  /usr/bin/shasum -a 256 "$1" | /usr/bin/awk '{print $1}'
}

json_string() {
  /usr/bin/jq -er "$2 | select(type == \"string\" and length > 0)" "$1"
}

json_number() {
  /usr/bin/jq -er "$2 | select(type == \"number\")" "$1"
}

require_files() {
  local path
  for path in "$PROCESS_CHECKER" "$NEWMAC_CONFIG" "$NEWMAC_ASSIGNMENT" \
    "$OLDMAC_ASSIGNMENT" "$OLDMAC_CONFIG" "$OLDMAC_CONFIG.sha256" \
    "$PAIR" "$CATALOG" "$PRIORITY" "$REMOTE_ROUTE_SYNC" "$VALIDATOR"; do
    [[ -r "$path" ]] || fail "NEWMAC_RUNTIME_BINDING_FILE_MISSING:$path"
  done
}

verify_static_pair() {
  local catalog_sha newmac_assignment_sha oldmac_assignment_sha oldmac_config_sha expected_oldmac_config_sha
  [[ "$(json_string "$PAIR" '.status')" == 'PASS' ]] || fail 'NEWMAC_RUNTIME_BINDING_PAIR_NOT_PASS'
  [[ "$(json_number "$PAIR" '.intersection')" -eq 0 \
    && "$(json_number "$PAIR" '.omission')" -eq 0 \
    && "$(json_number "$PAIR" '.active_item_overlap')" -eq 0 ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_OWNERSHIP_NOT_EXCLUSIVE'

  catalog_sha="$(sha256_file "$CATALOG")"
  newmac_assignment_sha="$(sha256_file "$NEWMAC_ASSIGNMENT")"
  oldmac_assignment_sha="$(sha256_file "$OLDMAC_ASSIGNMENT")"
  oldmac_config_sha="$(sha256_file "$OLDMAC_CONFIG")"
  expected_oldmac_config_sha="$(/usr/bin/awk 'NR == 1 {print $1}' "$OLDMAC_CONFIG.sha256")"

  [[ "$catalog_sha" == "$(json_string "$PAIR" '.catalog_sha256')" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_CATALOG_SHA_MISMATCH'
  [[ "$newmac_assignment_sha" == "$(json_string "$PAIR" '.newmac_manifest_sha256')" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_NEWMAC_MANIFEST_SHA_MISMATCH'
  [[ "$oldmac_assignment_sha" == "$(json_string "$PAIR" '.oldmac_manifest_sha256')" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_OLDMAC_MANIFEST_SHA_MISMATCH'
  [[ "$oldmac_config_sha" == "$expected_oldmac_config_sha" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_OLDMAC_CONFIG_SHA_MISMATCH'
  [[ "$(json_string "$NEWMAC_CONFIG" '.assignment_manifest_path')" == "$NEWMAC_ASSIGNMENT" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_NEWMAC_ASSIGNMENT_PATH_MISMATCH'
}

verify_routes_and_item() {
  local domain_suffix bookto_url newto_url item_key
  domain_suffix="$(json_number "$NEWMAC_CONFIG" '.domain_suffix')"
  bookto_url="$(json_string "$NEWMAC_CONFIG" '.base_urls.bookto')"
  newto_url="$(json_string "$NEWMAC_CONFIG" '.base_urls.newto')"
  item_key="$(json_string "$PAIR" '.oldmac_item_key')"

  [[ "$bookto_url" == "https://bookto${domain_suffix}.com" \
    && "$newto_url" == "https://newto${domain_suffix}.com" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_NEWMAC_ROUTE_INVALID'
  [[ "$domain_suffix" -eq "$(json_number "$OLDMAC_CONFIG" '.domain_suffix')" \
    && "$bookto_url" == "$(json_string "$OLDMAC_CONFIG" '.base_urls.bookto')" \
    && "$newto_url" == "$(json_string "$OLDMAC_CONFIG" '.base_urls.newto')" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_OLDMAC_ROUTE_DRIFT'
  [[ "$item_key" == "$(json_string "$OLDMAC_CONFIG" '.runtime_control.item_key')" \
    && "$item_key" == "$(json_string "$OLDMAC_ASSIGNMENT" '.entries[0].item_key')" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_OLDMAC_ITEM_DRIFT'
}

refresh_binding() {
  local checker_output now_epoch expires_at_epoch temporary temporary_sha
  local lane_id generation item_key domain_suffix bookto_url newto_url
  require_files
  verify_static_pair
  verify_routes_and_item

  checker_output="$($PROCESS_CHECKER)" || fail 'NEWMAC_RUNTIME_BINDING_PROCESS_CHECK_FAILED'
  [[ "$(/usr/bin/jq -r '.status // empty' <<< "$checker_output")" == 'PASS' ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_PROCESS_NOT_PASS'

  now_epoch="$(/bin/date +%s)"
  expires_at_epoch="$((now_epoch + TTL_SECONDS))"
  lane_id="$(json_string "$OLDMAC_ASSIGNMENT" '.lane_id')"
  generation="$(json_string "$PAIR" '.generation')"
  item_key="$(json_string "$PAIR" '.oldmac_item_key')"
  domain_suffix="$(json_number "$NEWMAC_CONFIG" '.domain_suffix')"
  bookto_url="$(json_string "$NEWMAC_CONFIG" '.base_urls.bookto')"
  newto_url="$(json_string "$NEWMAC_CONFIG" '.base_urls.newto')"
  temporary="$ROOT/.NEWMAC_RUNTIME_BINDING.json.tmp.$$"
  temporary_sha="$ROOT/.NEWMAC_RUNTIME_BINDING.json.sha256.tmp.$$"
  trap '/bin/rm -f "$temporary" "$temporary_sha"' RETURN

  /usr/bin/jq -n \
    --arg lane_id "$lane_id" --arg generation "$generation" --arg item_key "$item_key" \
    --arg bookto_url "$bookto_url" --arg newto_url "$newto_url" \
    --arg newmac_config_sha "$(sha256_file "$NEWMAC_CONFIG")" \
    --arg oldmac_config_sha "$(sha256_file "$OLDMAC_CONFIG")" \
    --arg newmac_manifest_sha "$(sha256_file "$NEWMAC_ASSIGNMENT")" \
    --arg oldmac_manifest_sha "$(sha256_file "$OLDMAC_ASSIGNMENT")" \
    --arg pair_sha "$(sha256_file "$PAIR")" --arg catalog_sha "$(sha256_file "$CATALOG")" \
    --arg process_status_sha "$(sha256_file "$PROCESS_STATUS")" \
    --arg process_snapshot_sha "$(/usr/bin/jq -r '.snapshot_sha256' <<< "$checker_output")" \
    --argjson now_epoch "$now_epoch" --argjson expires_at_epoch "$expires_at_epoch" \
    --argjson domain_suffix "$domain_suffix" \
    --argjson catalog_total "$(json_number "$PAIR" '.catalog_total')" \
    --argjson newmac_assigned "$(json_number "$PAIR" '.newmac_assigned')" \
    --argjson oldmac_assigned "$(json_number "$PAIR" '.oldmac_assigned')" \
    --argjson intersection "$(json_number "$PAIR" '.intersection')" \
    --argjson omission "$(json_number "$PAIR" '.omission')" \
    --argjson active_item_overlap "$(json_number "$PAIR" '.active_item_overlap')" \
    --argjson production_workers "$(/usr/bin/jq -r '.counts.active_production_workers' <<< "$checker_output")" \
    --argjson model_children "$(/usr/bin/jq -r '.counts.model_children' <<< "$checker_output")" \
    --argjson active_claims "$(/usr/bin/jq -r '.counts.active_claims' <<< "$checker_output")" \
    '{schema_version:"bookto_dual_runtime_binding.v1",lane_id:$lane_id,generation:$generation,source_machine:"NewMac",updated_at_epoch:$now_epoch,expires_at_epoch:$expires_at_epoch,newmac_config_sha256:$newmac_config_sha,oldmac_config_sha256:$oldmac_config_sha,newmac_manifest_sha256:$newmac_manifest_sha,oldmac_manifest_sha256:$oldmac_manifest_sha,pair_validation_sha256:$pair_sha,catalog_sha256:$catalog_sha,process_status_sha256:$process_status_sha,process_snapshot_sha256:$process_snapshot_sha,oldmac_item_key:$item_key,domain_suffix:$domain_suffix,base_urls:{bookto:$bookto_url,newto:$newto_url},counts:{catalog_total:$catalog_total,newmac_assigned:$newmac_assigned,oldmac_assigned:$oldmac_assigned,intersection:$intersection,omission:$omission,active_item_overlap:$active_item_overlap,production_workers:$production_workers,model_children:$model_children,active_claims:$active_claims}}' \
    > "$temporary"
  /usr/bin/jq -e '.schema_version == "bookto_dual_runtime_binding.v1" and .source_machine == "NewMac"' "$temporary" >/dev/null
  /bin/mv -f "$temporary" "$BINDING"
  printf '%s\n' "$(sha256_file "$BINDING")" > "$temporary_sha"
  /bin/mv -f "$temporary_sha" "$BINDING.sha256"
  trap - RETURN
}

verify_local_binding() {
  local expected actual now_epoch
  [[ -r "$BINDING" && -r "$BINDING.sha256" ]] || fail 'NEWMAC_RUNTIME_BINDING_LOCAL_MISSING'
  expected="$(/usr/bin/awk 'NR == 1 {print $1}' "$BINDING.sha256")"
  actual="$(sha256_file "$BINDING")"
  [[ "$expected" =~ ^[0-9a-f]{64}$ && "$expected" == "$actual" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_LOCAL_CHECKSUM_MISMATCH'
  now_epoch="$(/bin/date +%s)"
  (( $(json_number "$BINDING" '.expires_at_epoch') >= now_epoch )) \
    || fail 'NEWMAC_RUNTIME_BINDING_LOCAL_EXPIRED'
  [[ "$(json_string "$BINDING" '.newmac_config_sha256')" == "$(sha256_file "$NEWMAC_CONFIG")" \
    && "$(json_string "$BINDING" '.oldmac_config_sha256')" == "$(sha256_file "$OLDMAC_CONFIG")" \
    && "$(json_string "$BINDING" '.pair_validation_sha256')" == "$(sha256_file "$PAIR")" \
    && "$(json_string "$BINDING" '.catalog_sha256')" == "$(sha256_file "$CATALOG")" \
    && "$(json_string "$BINDING" '.newmac_manifest_sha256')" == "$(sha256_file "$NEWMAC_ASSIGNMENT")" \
    && "$(json_string "$BINDING" '.oldmac_manifest_sha256')" == "$(sha256_file "$OLDMAC_ASSIGNMENT")" ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_LOCAL_STATE_DRIFT'
}

remote_cleanup() {
  local remote_tmp="$1"
  /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "/bin/rm -f '$remote_tmp/NEWMAC_RUNTIME_BINDING.json' '$remote_tmp/NEWMAC_RUNTIME_BINDING.json.sha256' '$remote_tmp/bookto_multitab_newmac_binding_check.sh' '$remote_tmp/bookto_multitab_remote_route_sync.py' '$remote_tmp/CATALOG.json' '$remote_tmp/OLDMAC_ASSIGNMENT.json' '$remote_tmp/PAIR_VALIDATION.json' '$remote_tmp/PRIORITY.jsonl' '$remote_tmp/OLDMAC_multitab_config.json' '$remote_tmp/OLDMAC_multitab_config.json.sha256'; /bin/rmdir '$remote_tmp' 2>/dev/null || true" \
    >/dev/null 2>&1 || true
}

sync_binding() {
  local run_id remote_tmp remote_result remote_status route_result domain_suffix expected_suffix
  refresh_binding
  verify_local_binding
  remote_status="$(/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "'$REMOTE_ROOT/scripts/bookto_multitab_oldmac_control.sh' '$REMOTE_CONFIG' status")" \
    || fail 'NEWMAC_RUNTIME_BINDING_REMOTE_STATUS_PREFLIGHT_FAILED'
  [[ "$(/usr/bin/jq -r '.scraper_processes // -1' <<< "$remote_status")" -eq 0 ]] \
    || fail 'NEWMAC_RUNTIME_BINDING_REMOTE_SCRAPER_ACTIVE'
  domain_suffix="$(json_number "$BINDING" '.domain_suffix')"
  expected_suffix="$((domain_suffix - 1))"
  run_id="$(/bin/date '+%Y%m%dT%H%M%S')-$$"
  remote_tmp="$REMOTE_ROOT/runtime/newmac-binding-sync-$run_id"
  /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" "/bin/mkdir '$remote_tmp'" \
    || fail 'NEWMAC_RUNTIME_BINDING_REMOTE_TEMP_CREATE_FAILED'
  if ! /usr/bin/scp -q "$BINDING" "$BINDING.sha256" "$VALIDATOR" "$REMOTE_ROUTE_SYNC" \
    "$CATALOG" "$OLDMAC_ASSIGNMENT" "$PAIR" "$PRIORITY" "$OLDMAC_CONFIG" \
    "$OLDMAC_CONFIG.sha256" "$REMOTE_HOST:$remote_tmp/"; then
    remote_cleanup "$remote_tmp"
    fail 'NEWMAC_RUNTIME_BINDING_TRANSFER_FAILED'
  fi
  route_result="$(/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "/usr/bin/python3 '$remote_tmp/bookto_multitab_remote_route_sync.py' --root '$REMOTE_ROOT' --stage '$remote_tmp' --expected-suffix '$expected_suffix' --target-suffix '$domain_suffix'")" \
    || { remote_cleanup "$remote_tmp"; fail 'NEWMAC_RUNTIME_BINDING_REMOTE_ROUTE_SYNC_FAILED'; }
  [[ "$(/usr/bin/jq -r '.status // empty' <<< "$route_result")" =~ ^(COMMITTED|NOOP)$ ]] \
    || { remote_cleanup "$remote_tmp"; fail 'NEWMAC_RUNTIME_BINDING_REMOTE_ROUTE_SYNC_NOT_PASS'; }
  if ! /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "/bin/chmod 755 '$remote_tmp/bookto_multitab_newmac_binding_check.sh' && '$remote_tmp/bookto_multitab_newmac_binding_check.sh' '$REMOTE_CONFIG' '$remote_tmp/NEWMAC_RUNTIME_BINDING.json' >/dev/null"; then
    remote_cleanup "$remote_tmp"
    fail 'NEWMAC_RUNTIME_BINDING_REMOTE_PREFLIGHT_FAILED'
  fi
  /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "/bin/mv -f '$remote_tmp/NEWMAC_RUNTIME_BINDING.json' '$REMOTE_ROOT/NEWMAC_RUNTIME_BINDING.json' && /bin/mv -f '$remote_tmp/NEWMAC_RUNTIME_BINDING.json.sha256' '$REMOTE_ROOT/NEWMAC_RUNTIME_BINDING.json.sha256' && /bin/mv -f '$remote_tmp/bookto_multitab_newmac_binding_check.sh' '$REMOTE_ROOT/scripts/bookto_multitab_newmac_binding_check.sh' && /bin/chmod 755 '$REMOTE_ROOT/scripts/bookto_multitab_newmac_binding_check.sh' && /bin/rm -f '$remote_tmp/bookto_multitab_remote_route_sync.py' '$remote_tmp/CATALOG.json' '$remote_tmp/OLDMAC_ASSIGNMENT.json' '$remote_tmp/PAIR_VALIDATION.json' '$remote_tmp/PRIORITY.jsonl' '$remote_tmp/OLDMAC_multitab_config.json' '$remote_tmp/OLDMAC_multitab_config.json.sha256' && /bin/rmdir '$remote_tmp'" \
    || { remote_cleanup "$remote_tmp"; fail 'NEWMAC_RUNTIME_BINDING_REMOTE_INSTALL_FAILED'; }
  remote_result="$(/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "'$REMOTE_ROOT/scripts/bookto_multitab_newmac_binding_check.sh' '$REMOTE_CONFIG' '$REMOTE_ROOT/NEWMAC_RUNTIME_BINDING.json'")" \
    || fail 'NEWMAC_RUNTIME_BINDING_REMOTE_FINAL_CHECK_FAILED'

  /usr/bin/jq -n \
    --arg state 'PASS' --arg local_binding 'PASS' --arg remote_binding "$(/usr/bin/jq -r '.state' <<< "$remote_result")" \
    --arg item_key "$(json_string "$BINDING" '.oldmac_item_key')" \
    --arg binding_sha256 "$(sha256_file "$BINDING")" \
    --argjson domain_suffix "$(json_number "$BINDING" '.domain_suffix')" \
    --argjson expires_at_epoch "$(json_number "$BINDING" '.expires_at_epoch')" \
    --arg route_sync "$([ -n "$route_result" ] && /usr/bin/jq -r '.status' <<< "$route_result")" \
    '{schema_version:1,state:$state,local_binding:$local_binding,remote_binding:$remote_binding,remote_route_sync:$route_sync,oldmac_item_key:$item_key,domain_suffix:$domain_suffix,binding_sha256:$binding_sha256,expires_at_epoch:$expires_at_epoch}'
}

status_binding() {
  local remote_result
  require_files
  verify_static_pair
  verify_routes_and_item
  verify_local_binding
  remote_result="$(/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_HOST" \
    "'$REMOTE_ROOT/scripts/bookto_multitab_newmac_binding_check.sh' '$REMOTE_CONFIG' '$REMOTE_ROOT/NEWMAC_RUNTIME_BINDING.json'")" \
    || fail 'NEWMAC_RUNTIME_BINDING_REMOTE_STATUS_FAILED'
  /usr/bin/jq -n \
    --arg state 'PASS' --arg remote_binding "$(/usr/bin/jq -r '.state' <<< "$remote_result")" \
    --arg binding_sha256 "$(sha256_file "$BINDING")" \
    --arg item_key "$(json_string "$BINDING" '.oldmac_item_key')" \
    --argjson domain_suffix "$(json_number "$BINDING" '.domain_suffix')" \
    '{schema_version:1,state:$state,local_binding:"PASS",remote_binding:$remote_binding,oldmac_item_key:$item_key,domain_suffix:$domain_suffix,binding_sha256:$binding_sha256}'
}

case "${1:-}" in
  refresh) refresh_binding; verify_local_binding; /usr/bin/jq '.' "$BINDING" ;;
  sync) sync_binding ;;
  status) status_binding ;;
  *) printf 'USAGE: %s refresh|sync|status\n' "$0" >&2; exit 2 ;;
esac
