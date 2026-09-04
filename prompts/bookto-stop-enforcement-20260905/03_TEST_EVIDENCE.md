# Verification evidence

All results below were freshly observed after the implementation changes on 2026-09-05. Paths are sanitized.

| Gate | Result |
|---|---|
| Fresh-state semantic, cycle-evidence, and ownership unit tests | PASS, 25 tests |
| Fresh-state end-to-end shell scenarios | PASS, 23 scenarios |
| Repeated-compaction handoff tests | PASS, 12 tests |
| Target-marker PID binding and orphan-cleanup scraper tests | PASS, 2 selected tests; 21 deselected |
| Ruff on all changed Python files | PASS |
| Python byte compilation | PASS |
| Hook JSON and Codex TOML parsing | PASS |
| Fresh production process checker | PASS |
| Fresh live ownership reconciliation | PASS: claims 0, duplicates 0, ambiguous 0, scraper workers 0, unbound workers 0 |

Representative commands:

```sh
/bin/bash /Users/NEWMAC/.codex/hooks/test_fresh_state_guard.sh
/Users/NEWMAC/.local/bin/uv run python /Users/NEWMAC/.codex/hooks/test_fresh_state_semantics.py
/Users/NEWMAC/.local/bin/uv run python /Users/NEWMAC/.codex/hooks/test_fresh_state_cycle_evidence.py
/Users/NEWMAC/.local/bin/uv run python /Users/NEWMAC/.codex/hooks/test_fresh_state_ownership.py
/Users/NEWMAC/.local/bin/uv run --script /Users/NEWMAC/Documents/noin/tools/test_force_context_handoff_hook.py
/Users/NEWMAC/Documents/webtoon/bookto29_newto29_alltabs_process_check.sh
```

The targeted scraper test used its declared runtime dependencies and selected these two cases:

```text
background_target_marker_binds_to_scraper_worker_pid
orphan_cleanup_closes_only_receipted_background_targets
```

The first attempted shell invocation lacked the file's executable bit, and the first multi-file `unittest` invocation used filesystem paths where module names were expected. Both were invocation errors, not product failures; the documented interpreter entry points above were then used. Static inspection also found import ordering and one unused test import, which were corrected before the final green run.

No language-server result is claimed. The installed environment did not contain the configured Python language server, and it was not installed as part of this production repair.
