# Bookto Stop-enforcement implementation context

Status: locally implemented and verified on 2026-09-05. This file is a redacted public summary; the exact sanitized diff is in `02_EXACT_PATCH.diff`.

## Scope

The change closes six evidence and lifecycle gaps in a bounded Bookto/Newto automation cycle:

1. A finalized cycle's retry history was reconstructed from mutable auxiliary artifacts.
2. A repair could be accepted from caller-supplied `post_repair_verified=true` without independently derived semantic movement.
3. A manual gate could be reused across cycles because its durable fingerprint was not sealed into the finalized receipt.
4. A live CDP target marker was not bound to the actual scraper worker process that owned it.
5. Canonical progress could change between receipt validation and final readback and be silently absorbed into the finalized receipt.
6. Repeated context compaction emitted an advisory but did not prevent further substantive tool use in the source task.

## Implemented controls

- Finalized receipts now embed a normalized cycle-action record and a SHA-256 seal over the finalized payload. Retry count, route history, and manual-gate fingerprints are read from that sealed evidence. Legacy receipts retain a bounded compatibility path.
- A claimed repair now requires exactly one current action-evidence artifact and independently derived item or aggregate semantic movement. The artifact's own verification boolean no longer proves success.
- Finalization rejects any post-validation change to a configured progress path with `FRESH_STATE_FINALIZATION_PROGRESS_RACE`. A volatile-only readback race remains allowed and is covered by a positive regression scenario.
- Scraper target markers now record `worker_pid`. Ownership reconciliation requires a fresh PASS process report, exactly one PASS scraper-controller role, a live worker PID, a matching live CDP target, and a one-to-one marker/process relationship. Missing, mismatched, duplicate, or unbound ownership fails closed.
- The repeated-compaction hook writes an atomic per-session mandate and a trusted `PreToolUse` hook denies substantive tools after the second compaction. Only bounded handoff-coordination tools remain available. A present but malformed or altered mandate also fails closed.

## Operational observation

The production process checker was refreshed after installation and returned PASS. At that observation point there were two production engines, zero model children, zero active claims, zero scraper workers, and zero target markers. The new ownership reconciliation returned zero duplicate, ambiguous, and unbound claims. No protected screen, controller, queue, browser state, or worker was stopped or restarted.

## System-error separation

The private source transcript contained one `server_overloaded` failure and, later, an HTTP 404 from the Codex response endpoint; later turns in the same task succeeded. That supports a transient backend request failure as the direct cause of the visible system error. The unusually large, repeatedly compacted source task was a recurrence-risk amplifier, not proven as the direct cause. The transcript is intentionally not published because it contains unrelated private conversation data.

The new handoff boundary mitigates the local long-context recurrence path. It cannot prevent an upstream service outage. Official Codex hook behavior is documented at <https://developers.openai.com/codex/hooks>.

## Remote failure separation

One canonical runtime-binding refresh and one distinct direct SSH check both failed while current mesh status reported the remote Mac offline. The local alias and destination were resolved successfully. Therefore the OldMac branch remains `BLOCKED_EXTERNAL` until that peer is online; no alternate host, bypass, repeated retry, or local weakening of the dual-Mac contract was introduced. The existing automation prompt already evaluates local disk liveness after contract integrity and local process PASS, before the remote binding branch, so the remote outage does not erase a completed local assessment.

## Rollback and residual risk

- Local rollback source: `/Users/NEWMAC/.codex/hooks/backups/20260905T073733+0900-stop-evidence-v2`.
- Hook activation should be re-observed in a fresh Codex task or app reload because the currently running task may retain startup state.
- The remote branch cannot be end-to-end verified until the remote Mac returns online.
- A Python language server was unavailable. Ruff, byte compilation, JSON/TOML parsing, unit tests, shell scenarios, targeted scraper tests, and a live process/ownership check were used instead.
- The patch is a sanitized review artifact. Machine paths must be restored to their actual installation roots before any rollback or reproduction.
