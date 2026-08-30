#!/bin/bash
set -euo pipefail

CONTROL="/Users/NEWMAC/Documents/webtoon/bookto_multitab_newmac_chrome_control.sh"
CONFIG="/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_20260825/NEWMAC_CHROME_CONTROL.json"

[[ -x "$CONTROL" ]]
[[ -r "$CONFIG" && -r "${CONFIG}.sha256" ]]

expected_sha="$(awk 'NR == 1 {print $1}' "${CONFIG}.sha256")"
actual_sha="$(shasum -a 256 "$CONFIG" | awk '{print $1}')"
[[ "$expected_sha" == "$actual_sha" ]]

launch_json="$("$CONTROL" "$CONFIG" print-command)"
jq -e '
  .status == "PASS"
  and .background_only == true
  and .chrome_mode == "background_headful"
  and .cdp_port == 9240
  and .proxy_server == "socks5://127.0.0.1:<PORT>"
  and (.argv | index("--no-startup-window")) != null
  and ([.argv[] | select(startswith("--headless"))] | length) == 0
  and (.argv | index("--remote-debugging-port=9240")) != null
  and (.argv | index("--proxy-server=socks5://127.0.0.1:<PORT>")) != null
  and (.argv | index("--user-data-dir=/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_20260825/chrome_profile")) != null
' >/dev/null <<<"$launch_json"

bash -n "$CONTROL"
printf 'PASS newmac Chrome control contract\n'
