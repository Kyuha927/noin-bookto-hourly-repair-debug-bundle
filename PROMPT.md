# Prompt for WebGPT

Act as an independent SRE, automation, and Python debugging reviewer.

Analyze this repository in full:

https://github.com/Kyuha927/noin-bookto-hourly-repair-debug-bundle

The concrete defect is described in `ISSUE.md`. Begin with `README.md`, `ISSUE.md`, and `metadata/SOURCE_HASHES.tsv`, then inspect the contract, automation prompt, receipt validator, process checker, scraper ownership code, current sanitized state summaries, the five recent receipts, and regression tests.

Your task is not to suggest generic troubleshooting. Determine why an hourly repair automation that explicitly forbids status-only cycles can repeatedly finish without repairing the oldest independently actionable blocker.

Required analysis:

1. Reconstruct the five supplied cycles chronologically and classify each as actual repair, active production movement, materially different escalation, manual external gate, or status-only behavior.
2. Identify the exact false-PASS or weak-PASS code path. Do not trust caller-supplied booleans such as `movement`, `status_only`, `protected_state_preserved`, or `post_repair_verified` without checking whether the validator derives them from evidence.
3. Separate process health from item ownership. Reconcile process ancestry, singleton locks, scraper child workers, CDP target markers, model children, and claim receipts.
4. Replace global hash movement with stage-specific and item-specific semantic movement. Timestamp-only or equivalent rewrites must not count as progress.
5. Define the safe decision when one item is actively producing files but an older different item is blocked.
6. Ensure three identical no-progress failures force a materially different diagnostic route.
7. Do not repeat the already-fixed Cloudflare classification, headless Chrome, or dual-Mac rotation changes unless fresh repository evidence proves a regression.

Deliverables:

- ranked root causes with exact repository file and line references;
- a minimal state-machine design;
- unified diffs for every required code and contract change;
- regression tests that fail before and pass after the fix;
- exact application, validation, and rollback commands;
- a shorter corrected automation prompt that states each invariant once;
- residual risks and any single missing artifact required for certainty.

Hard constraints:

- Treat every PID, suffix, route, item, count, and timestamp in the repository as a historical snapshot.
- Do not propose broad recursive discovery, `pkill`, name-based termination, deletion of queues/profiles/partial outputs, or production Playwright/curl bypasses.
- Do not claim to have executed local commands. Return exact patches and tests for the primary operator to apply and verify.
- A prompt-only rewrite is not a complete fix if enforcement code still permits false receipts.
