# Recurring failure: bounded repair automation can finish without repairing the oldest blocker

## Required behavior

The hourly heartbeat covers exactly one 2,803-item Bookto/Newto lane. Every cycle must refresh canonical state, preserve active ownership, and either:

- perform and verify one smallest safe item-specific repair;
- prove fresh production output movement for an actively owned item;
- execute a materially different diagnostic route after repeated identical failure; or
- record a genuinely external manual gate such as login, OAuth, legal consent, or a human checkbox.

Status-only cycles and false PASS receipts are forbidden. Overall completion requires every item to pass scrape, OCR/preprocessing, visual work, learning, independent QA, devices, and final INCLUDE/registry gates, with duplicate claims and portfolio unaccounted both zero.

## Observed recurring symptoms

1. A cycle may run the process checker and runtime binding sync, read state files, and write a receipt while `repair.count=0` and `repair.executed=false`.
2. `status_only=false` is a caller-supplied receipt field, so it may not prove that a repair or materially different diagnosis occurred.
3. Periodic rewrites of `LEARNING_INTAKE_STATE.json` or `VISUAL_WORKER_STATE.json` can change hashes and timestamps without advancing semantic completion counts.
4. Any movement in one lane or output directory may suppress repair of a different, older, independently repairable failure.
5. `PROCESS_STATUS.counts.active_claims=0` can coexist with live scraper child workers and durable CDP target markers. The checker claim model and scraper ownership model are not demonstrably identical.
6. A long-running scrape future writes many files before `SCRAPE_STATE.json` advances because result persistence occurs after the future completes. This is legitimate production movement but complicates stuck-versus-active classification.
7. Receipt validation currently needs review for cross-field invariants. In particular, backlog plus `repair.executed=false` should not be accepted solely because an unrelated progress path changed.

## Already-fixed incidents that must not be proposed as the current root fix without fresh evidence

- Automatic Cloudflare challenge was previously misclassified as a retry-only route signal.
- Canonical Chrome previously used headless mode and was changed to a background, no-startup-window headful process.
- A 30→31 route rotation previously failed to update all NewMac/OldMac assignment and binding artifacts atomically.

These fixes are included as code snapshots and tests because they are part of the failure history, not because they are assumed to remain the current blocker.

## Review questions

1. Which exact condition allows a false or weak cycle PASS?
2. Should movement be evaluated per stage, per item, and per owner rather than as one global boolean?
3. How should scraper target markers, process ancestry, durable locks, and claim receipts be reconciled into one ownership truth?
4. Which receipt fields should be derived by the validator instead of trusted from the caller?
5. What minimal code changes and regression tests guarantee that an actionable oldest blocker cannot be skipped?

## Required response

Provide ranked root causes, exact file/line evidence, unified diffs, failing-before/passing-after tests, application and rollback commands, and a corrected automation prompt. General advice or prompt-only changes are insufficient.
