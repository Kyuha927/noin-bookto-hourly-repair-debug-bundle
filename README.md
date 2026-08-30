# Bookto/Newto hourly repair diagnostic bundle

This public repository is a sanitized, point-in-time diagnostic bundle for a recurring automation failure in `noin-bookto29-newto29-alltabs-hourly-repair`.

The automation is required to repair one real blocker per bounded cycle, but some cycles can finish after refresh/readback/receipt work without repairing an independently repairable blocked item. The bundle is intended for an external WebGPT review of the contract, receipt validator, process ownership model, movement semantics, and scraper control path.

Start with:

1. [`ISSUE.md`](ISSUE.md)
2. [`PROMPT.md`](PROMPT.md)
3. [`metadata/SOURCE_HASHES.tsv`](metadata/SOURCE_HASHES.tsv)
4. `snapshots/automation`, `snapshots/hooks`, `snapshots/process`, `snapshots/scraper`, `snapshots/state`, and `snapshots/receipts`

## Sanitization and scope

- Local usernames are replaced with `/Users/NEWMAC` and `/Users/OLDMAC`.
- Rotating production domains, private IP addresses, internal thread IDs, and machine-specific endpoints are redacted.
- No API keys, cookies, browser profiles, authentication data, source images, OCR text, manuscript text, or queue payloads are included.
- Large state files are represented by bounded summaries. The full 2,803-item catalog and production outputs are deliberately excluded.
- Source hashes in `metadata/SOURCE_HASHES.tsv` identify the exact local source snapshots used before sanitization.
- Sanitized snapshots are evidence and review material, not drop-in production replacements.

## Snapshot caveat

All runtime facts in this repository are historical snapshots. Reviewers must not treat a recorded PID, suffix, URL, count, or item as current production state.
