#!/usr/bin/env bash
set -euo pipefail

CHECKER="/Users/NEWMAC/Documents/webtoon/bookto_process_contract_check.py"
CHECKER_SHA256="/Users/NEWMAC/Documents/webtoon/bookto_process_contract_check.py.sha256"
CONTRACT="/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_20260825/PROCESS_CONTRACT.json"

expected_checker_sha256="$(/usr/bin/awk 'NR == 1 { print $1 }' "$CHECKER_SHA256")"
expected_checker_name="$(/usr/bin/awk 'NR == 1 { print $2 }' "$CHECKER_SHA256")"
actual_checker_sha256="$(/usr/bin/openssl dgst -sha256 "$CHECKER" | /usr/bin/awk '{ print $NF }')"
if [[ -z "$expected_checker_sha256" \
  || "$expected_checker_name" != "${CHECKER##*/}" \
  || "$actual_checker_sha256" != "$expected_checker_sha256" ]]; then
  printf '%s\n' 'PROCESS_CHECKER_INTEGRITY_ERROR' >&2
  exit 3
fi

exec /Users/NEWMAC/.local/bin/uv run --script "$CHECKER" --contract "$CONTRACT"
