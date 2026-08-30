"""Cycle-receipt validation for fresh-state automation stops."""

from __future__ import annotations

import json
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Final

from fresh_state_contract import Contract, GuardError, load_mapping, sha256_bytes
from fresh_state_receipt_validation import (
    ReceiptValidationContext,
    readback_rows,
    validate_movement,
    validate_outcome,
    validate_receipt,
)

RECEIPT_RE = re.compile(
    r'<!--\s*CODEX_FRESH_STATE_RECEIPT\s+path="(?P<path>[^"]+)"\s+'
    r'sha256="(?P<sha>[0-9a-f]{64})"\s*-->'
)
FINALIZATION_PROTOCOL: Final = "canonical_snapshot_v1"
FINALIZATION_ATTEMPTS: Final = 8


def validate_receipt_marker(
    message: str, contract: Contract, progress_baseline: dict[str, str]
) -> None:
    """Validate the receipt marker, file identity, freshness, and cycle outcome."""
    marker = RECEIPT_RE.search(message)
    if marker is None:
        raise GuardError("FRESH_STATE_RECEIPT_REQUIRED", contract.contract_id)
    receipt_path = Path(marker.group("path")).resolve()
    if contract.receipt_root not in receipt_path.parents:
        raise GuardError("FRESH_STATE_RECEIPT_PATH_INVALID", str(receipt_path))
    data = receipt_path.read_bytes()
    if sha256_bytes(data) != marker.group("sha"):
        raise GuardError("FRESH_STATE_RECEIPT_HASH_MISMATCH", str(receipt_path))
    raw = load_mapping(receipt_path)
    protocol_enabled = (
        raw.get("stop_finalization_protocol") == FINALIZATION_PROTOCOL
    )
    context = ReceiptValidationContext(contract, progress_baseline)
    try:
        validate_receipt(raw, context)
        finalized = raw
    except GuardError as exc:
        readback_race = exc.code == "FRESH_STATE_READBACK_MISMATCH"
        if not protocol_enabled or not readback_race:
            raise
        receipt_rows = readback_rows(raw.get("state_readback"), contract)
        receipt_hashes = {path: row[0] for path, row in receipt_rows.items()}
        receipt_movement = validate_movement(raw, receipt_hashes, context)
        validate_outcome(raw, contract, receipt_movement)
        for _attempt in range(FINALIZATION_ATTEMPTS):
            snapshot = []
            for path in contract.canonical_paths:
                first_mtime = path.stat().st_mtime_ns
                content = path.read_bytes()
                second_mtime = path.stat().st_mtime_ns
                if first_mtime != second_mtime:
                    break
                snapshot.append(
                    {
                        "path": str(path),
                        "sha256": sha256_bytes(content),
                        "mtime_ns": second_mtime,
                    }
                )
            else:
                hashes = {row["path"]: row["sha256"] for row in snapshot}
                movement_rows = [
                    {
                        "path": str(path),
                        "before_sha256": progress_baseline[str(path)],
                        "after_sha256": hashes[str(path)],
                    }
                    for path in contract.progress_paths
                ]
                observed = time.time()
                candidate = dict(raw)
                candidate.update(
                    {
                        "canonical_state_observed_at_epoch": observed,
                        "completed_at_epoch": observed,
                        "state_readback": snapshot,
                        "movement_evidence": movement_rows,
                        "movement": any(
                            row["before_sha256"] != row["after_sha256"]
                            for row in movement_rows
                        ),
                    }
                )
                try:
                    validate_receipt(candidate, context)
                except GuardError as finalization_error:
                    retryable = (
                        finalization_error.code == "FRESH_STATE_READBACK_MISMATCH"
                    )
                    if retryable:
                        continue
                    raise
                finalized = candidate
                break
        else:
            raise GuardError(
                "FRESH_STATE_FINALIZATION_BUSY", contract.contract_id
            ) from exc
    if not protocol_enabled:
        return
    finalized_path = receipt_path.with_name(
        f"{receipt_path.stem}.stop-finalized{receipt_path.suffix}"
    )
    sealed = dict(finalized)
    sealed["stop_finalization_seal"] = {
        "protocol": FINALIZATION_PROTOCOL,
        "source_receipt_path": str(receipt_path),
        "source_receipt_sha256": marker.group("sha"),
        "linearized_at_epoch": finalized["canonical_state_observed_at_epoch"],
    }
    encoded = (json.dumps(sealed, sort_keys=True) + "\n").encode()
    with tempfile.NamedTemporaryFile(
        "wb", dir=finalized_path.parent, delete=False
    ) as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    os.replace(temporary, finalized_path)
