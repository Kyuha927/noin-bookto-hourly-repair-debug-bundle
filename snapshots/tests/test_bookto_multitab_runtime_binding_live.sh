#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$ROOT/bookto_multitab_runtime_binding.sh"
RESULT="$($SCRIPT sync)"

/usr/bin/jq -e \
  '.state == "PASS" and .local_binding == "PASS" and .remote_binding == "PASS" and (.remote_route_sync == "COMMITTED" or .remote_route_sync == "NOOP") and .oldmac_item_key == "newto_fafa:234356" and .domain_suffix == 31' \
  <<< "$RESULT" >/dev/null

printf 'PASS\n'
