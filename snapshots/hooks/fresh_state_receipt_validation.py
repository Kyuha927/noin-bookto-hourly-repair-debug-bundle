from __future__ import annotations

import re
import time
from typing import Any, NamedTuple

from fresh_state_contract import Contract, GuardError, sha256_bytes


class ReceiptValidationContext(NamedTuple):
    contract: Contract
    progress_baseline: dict[str, str]


def validate_receipt(
    raw: dict[str, Any], context: ReceiptValidationContext
) -> None:
    contract = context.contract
    if raw.get("schema_version") != "global_fresh_state_cycle_receipt.v1":
        raise GuardError("FRESH_STATE_RECEIPT_INVALID", "schema_version")
    if (
        raw.get("contract_id") != contract.contract_id
        or raw.get("contract_sha256") != contract.sha256
    ):
        raise GuardError("FRESH_STATE_RECEIPT_INVALID", "contract identity")
    completed = raw.get("completed_at_epoch")
    observed = raw.get("canonical_state_observed_at_epoch")
    if not isinstance(completed, (int, float)) or not isinstance(
        observed, (int, float)
    ):
        raise GuardError("FRESH_STATE_RECEIPT_INVALID", "timestamps")
    now = time.time()
    if (
        completed < observed
        or completed - observed > contract.state_ttl_seconds
        or now - completed > contract.max_receipt_age_seconds
    ):
        raise GuardError("FRESH_STATE_RECEIPT_STALE", contract.contract_id)
    readback_hashes = _validate_readback(
        raw.get("state_readback"), observed, contract
    )
    movement = validate_movement(raw, readback_hashes, context)
    validate_outcome(raw, contract, movement)


def readback_rows(
    value: Any, contract: Contract
) -> dict[str, tuple[str, int]]:
    if not isinstance(value, list):
        raise GuardError("FRESH_STATE_READBACK_INVALID", "state_readback")
    rows = {
        row.get("path"): row
        for row in value
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if len(rows) != len(value) or set(rows) != {
        str(path) for path in contract.canonical_paths
    }:
        raise GuardError("FRESH_STATE_READBACK_INVALID", "canonical path coverage")
    validated: dict[str, tuple[str, int]] = {}
    for path in contract.canonical_paths:
        row = rows[str(path)]
        row_hash = row.get("sha256")
        row_mtime = row.get("mtime_ns")
        if (
            not isinstance(row_hash, str)
            or not re.fullmatch(r"[0-9a-f]{64}", row_hash)
            or not isinstance(row_mtime, int)
            or isinstance(row_mtime, bool)
        ):
            raise GuardError("FRESH_STATE_READBACK_INVALID", str(path))
        validated[str(path)] = (row_hash, row_mtime)
    return validated


def _validate_readback(
    value: Any, observed: float, contract: Contract
) -> dict[str, str]:
    rows = readback_rows(value, contract)
    hashes: dict[str, str] = {}
    for path in contract.canonical_paths:
        row_hash, row_mtime = rows[str(path)]
        first_mtime = path.stat().st_mtime_ns
        current_hash = sha256_bytes(path.read_bytes())
        second_mtime = path.stat().st_mtime_ns
        if (
            first_mtime != second_mtime
            or second_mtime != row_mtime
            or current_hash != row_hash
        ):
            raise GuardError("FRESH_STATE_READBACK_MISMATCH", str(path))
        if (
            path in contract.volatile_paths
            and observed - (row_mtime / 1_000_000_000) > contract.state_ttl_seconds
        ):
            raise GuardError("FRESH_STATE_VOLATILE_STATE_STALE", str(path))
        hashes[str(path)] = row_hash
    return hashes


def validate_movement(
    raw: dict[str, Any],
    readback_hashes: dict[str, str],
    context: ReceiptValidationContext,
) -> bool:
    value = raw.get("movement_evidence")
    claimed = raw.get("movement")
    contract = context.contract
    if not isinstance(value, list) or not isinstance(claimed, bool):
        raise GuardError("FRESH_STATE_MOVEMENT_INVALID", contract.contract_id)
    rows: dict[str, tuple[str, str]] = {}
    for row in value:
        if not isinstance(row, dict):
            raise GuardError("FRESH_STATE_MOVEMENT_INVALID", contract.contract_id)
        path = row.get("path")
        before = row.get("before_sha256")
        after = row.get("after_sha256")
        if (
            not isinstance(path, str)
            or path in rows
            or not isinstance(before, str)
            or not isinstance(after, str)
            or not re.fullmatch(r"[0-9a-f]{64}", before)
            or not re.fullmatch(r"[0-9a-f]{64}", after)
        ):
            raise GuardError("FRESH_STATE_MOVEMENT_INVALID", contract.contract_id)
        rows[path] = (before, after)
    progress_paths = {str(path) for path in contract.progress_paths}
    if (
        set(rows) != progress_paths
        or set(context.progress_baseline) != progress_paths
        or any(
            rows[path][0] != context.progress_baseline[path]
            for path in progress_paths
        )
        or any(
            rows[path][1] != readback_hashes[path] for path in progress_paths
        )
    ):
        raise GuardError("FRESH_STATE_MOVEMENT_INVALID", contract.contract_id)
    changed = any(before != after for before, after in rows.values())
    if claimed != changed:
        raise GuardError("FRESH_STATE_MOVEMENT_INVALID", contract.contract_id)
    return claimed


def validate_outcome(
    raw: dict[str, Any], contract: Contract, movement: bool
) -> None:
    backlog = raw.get("backlog_remaining")
    repair = raw.get("repair")
    retry = raw.get("retry")
    if (
        type(backlog) is not int
        or backlog < 0
        or not isinstance(repair, dict)
        or not isinstance(retry, dict)
    ):
        raise GuardError("FRESH_STATE_RECEIPT_INVALID", "outcome fields")
    count = repair.get("count")
    executed = repair.get("executed") is True
    if (
        type(count) is not int
        or count < 0
        or count > contract.max_repairs_per_cycle
        or executed != (count == 1)
    ):
        raise GuardError("FRESH_STATE_REPAIR_INVALID", contract.contract_id)
    item_key = repair.get("item_key")
    if executed and (
        repair.get("post_repair_verified") is not True
        or not isinstance(item_key, str)
        or not item_key
    ):
        raise GuardError("FRESH_STATE_REPAIR_INVALID", "verification or item key")
    attempts = retry.get("same_failure_count")
    changed_route = retry.get("diagnostic_route_changed") is True
    if (
        type(attempts) is not int
        or attempts < 0
        or (attempts >= contract.same_failure_limit and not changed_route)
    ):
        raise GuardError("FRESH_STATE_RETRY_ESCALATION_REQUIRED", contract.contract_id)
    escalation = raw.get("escalation_executed") is True
    manual_gate = raw.get("manual_external_gate") is True
    if (
        backlog > 0
        and not movement
        and not executed
        and not escalation
        and not manual_gate
    ):
        raise GuardError("FALSE_WAITING_REPAIR_REQUIRED", contract.contract_id)
    duplicate_claims = raw.get("duplicate_claims")
    if (
        raw.get("status_only") is not False
        or type(duplicate_claims) is not int
        or duplicate_claims != 0
        or raw.get("protected_state_preserved") is not True
    ):
        raise GuardError("FRESH_STATE_CYCLE_INVARIANT_FAILED", contract.contract_id)
