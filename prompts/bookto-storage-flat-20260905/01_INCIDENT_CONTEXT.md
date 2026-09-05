# Bookto offload and APFS free-space incident context

Status: sanitized point-in-time evidence prepared on 2026-09-05 (Asia/Seoul).

This public file intentionally excludes credentials, private paths, hostnames, object IDs, transaction IDs, full logs, source content, browser data, and account data. It is evidence for reassessment, not a command or a timeless description of the live system.

## Symptom

The operator sees macOS free space remain nearly flat or move in the wrong direction even while a restore-verified offloader reports successful local deletion. The question is whether this indicates an offloader deletion defect or expected net accounting while other allocations occur.

## BEGIN SANITIZED HANDOFF EVIDENCE

The originating diagnostic task reported the following items as recently verified. The private receipts and logs are deliberately absent from this public packet, so an external reviewer must treat each item as a bounded evidence claim and state how the missing raw artifacts limit certainty.

1. Two offload transactions were active concurrently. Each transaction atomically renamed its source episode to a frozen directory and built a local archive. Until remote restore verification and the deletion commit completed, this temporarily retained roughly two local allocations per transaction.
2. One recent active pair involved approximately 8.5 MiB per episode. Frozen sources plus archives therefore represented roughly 34 MiB of temporary combined local allocation across the two active transactions. These are approximate logical quantities; unique physical APFS allocation was not separately proven.
3. Recent completed transaction receipts reported all required lifecycle gates: remote object presence, size and SHA-256 agreement; remote restore proof; `OFFLOADED_RESTORE_VERIFIED_DELETED`; `LOCAL_DELETE_VERIFIED`; `COMPLETE`; and absence of the local source, frozen directory, and archive.
4. A matched 29-second Data-volume observation recorded `df` available space of 102,502,868 KiB, then 102,501,728 KiB, then 102,510,336 KiB. The start-to-end change was +7,468 KiB, approximately +7.29 MiB. `verified_uploaded_bytes` did not increase during that short window.
5. Canonical visual-learning derivatives, preprocessed data, and images are intentionally retained until the visual worker reports `COMPLETE` and the held/evidence queues are all zero. Offloading a raw source episode therefore does not imply that every related local derivative disappears.
6. Concurrent pipeline writes could offset deletion-driven reclamation, but this remains a hypothesis unless measured over the same interval and accounting layer.
7. The installed offloader source and test hashes differed from the hashes pinned by an automation contract, while the current regression tests passed. This supports a provenance/liveness degradation finding. It does not by itself prove that local deletion failed.
8. A separate remote-Mac SSH/runtime-binding timeout was observed. No evidence currently ties that remote availability failure to local APFS block accounting.

## END SANITIZED HANDOFF EVIDENCE

## Fresh read-only observation made while preparing this packet

One additional matched 30-second sample was collected on the local startup APFS container. No deletion, snapshot change, service restart, trace, reindex, cache cleanup, or workload-control change was performed.

| Counter | 2026-09-05 14:13:59 +09:00 | 2026-09-05 14:14:29 +09:00 | Delta |
|---|---:|---:|---:|
| APFS container unallocated bytes | 112,149,000,192 | 112,144,097,280 | -4,902,912 B (-4.68 MiB) |
| Data volume consumed bytes | 840,000,544,768 | 840,005,447,680 | +4,902,912 B (+4.68 MiB) |
| VM volume consumed bytes | 9,665,966,080 | 9,665,966,080 | 0 B |
| Data-path `df` available | 109,520,512 KiB | 109,515,724 KiB | -4,788 KiB (-4.68 MiB) |

This sample localizes the observed change to the Data volume for that interval, but it did not include matched offloader lifecycle counters or per-writer path allocation. It therefore cannot attribute the increase to the offloader, a producer, logs, databases, temporary staging, snapshots, purgeable-space semantics, clones, or another Data-volume writer.

## Known accounting boundaries

- Remote uploaded bytes are not equivalent to locally freed bytes.
- Logical deletion and path absence are not equivalent to APFS block return.
- File logical size, allocated blocks, unique physical blocks, container free space, volume consumption, purgeable estimates, snapshot retention, and open-deleted allocations are distinct counters.
- Measurements from different windows or accounting layers must not be subtracted to infer a cause.
- A snapshot's existence alone does not prove that it retains the deleted episode's blocks.
- A passing transaction receipt can prove lifecycle behavior for that item without proving positive net free-space movement while unrelated writes continue.

## Unknowns that remain open

- Whether a completed transaction's exact source and staging allocations are reflected as reclaimed blocks in a matched quiet window.
- Whether snapshots, clones/shared extents, purgeable accounting, or open-deleted files retain any material fraction of the relevant blocks.
- The net allocation rate of other Data-volume writers during completed offload boundaries.
- Whether the observed hash drift can cause a future liveness failure even though current deletion regressions pass.
