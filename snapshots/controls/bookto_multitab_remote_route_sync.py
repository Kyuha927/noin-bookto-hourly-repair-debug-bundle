from __future__ import annotations

import argparse
import hashlib
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class RemoteRouteSyncError(RuntimeError):
    pass


STAGED_FILES = {
    "CATALOG.json": "CATALOG.json",
    "OLDMAC_ASSIGNMENT.json": "OLDMAC_ASSIGNMENT.json",
    "PAIR_VALIDATION.json": "PAIR_VALIDATION.json",
    "PRIORITY.jsonl": "PRIORITY.jsonl",
    "OLDMAC_multitab_config.json": "multitab_config.json",
    "OLDMAC_multitab_config.json.sha256": "multitab_config.json.sha256",
}


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def _object(payload: bytes, code: str) -> dict[str, Any]:
    value = json.loads(payload.decode())
    if not isinstance(value, dict):
        raise RemoteRouteSyncError(f"{code}:OBJECT_REQUIRED")
    return value


def _atomic(path: Path, payload: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def _validate_candidates(
    payloads: dict[Path, bytes], root: Path, target_suffix: int
) -> None:
    config = _object(payloads[root / "multitab_config.json"], "REMOTE_CONFIG")
    expected_bases = {
        route: f"https://{route}{target_suffix}.com" for route in ("bookto", "newto")
    }
    if config.get("domain_suffix") != target_suffix or config.get("base_urls") != expected_bases:
        raise RemoteRouteSyncError("REMOTE_CONFIG_ROUTE_INVALID")
    if config.get("catalog_path") != str(root / "CATALOG.json"):
        raise RemoteRouteSyncError("REMOTE_CONFIG_CATALOG_PATH_DRIFT")
    if config.get("assignment_manifest_path") != str(root / "OLDMAC_ASSIGNMENT.json"):
        raise RemoteRouteSyncError("REMOTE_CONFIG_ASSIGNMENT_PATH_DRIFT")

    config_payload = payloads[root / "multitab_config.json"]
    sidecar = payloads[root / "multitab_config.json.sha256"].decode().strip()
    if sidecar != _sha256(config_payload):
        raise RemoteRouteSyncError("REMOTE_CONFIG_SIDECAR_MISMATCH")
    catalog_payload = payloads[root / "CATALOG.json"]
    assignment_payload = payloads[root / "OLDMAC_ASSIGNMENT.json"]
    pair = _object(payloads[root / "PAIR_VALIDATION.json"], "REMOTE_PAIR")
    if pair.get("status") != "PASS":
        raise RemoteRouteSyncError("REMOTE_PAIR_NOT_PASS")
    if pair.get("catalog_sha256") != _sha256(catalog_payload):
        raise RemoteRouteSyncError("REMOTE_PAIR_CATALOG_SHA_MISMATCH")
    if pair.get("oldmac_manifest_sha256") != _sha256(assignment_payload):
        raise RemoteRouteSyncError("REMOTE_PAIR_ASSIGNMENT_SHA_MISMATCH")

    old_hosts = (
        f"https://bookto{target_suffix - 1}.com".encode(),
        f"https://newto{target_suffix - 1}.com".encode(),
    )
    if any(old in payload for payload in payloads.values() for old in old_hosts):
        raise RemoteRouteSyncError("REMOTE_OLD_ROUTE_REMAINS")


def sync_remote_route(
    root: Path, stage: Path, expected_suffix: int, target_suffix: int
) -> dict[str, Any]:
    root = root.resolve()
    stage = stage.resolve()
    if target_suffix != expected_suffix + 1:
        raise RemoteRouteSyncError("REMOTE_SUFFIX_NOT_EXACT_PLUS_ONE")
    config_path = root / "multitab_config.json"
    current = _object(config_path.read_bytes(), "REMOTE_CURRENT_CONFIG")
    current_suffix = current.get("domain_suffix")
    if current_suffix not in {expected_suffix, target_suffix}:
        raise RemoteRouteSyncError("REMOTE_CURRENT_SUFFIX_DRIFT")
    child_marker = root / "runtime" / "scraper.child.pid"
    if child_marker.is_file():
        try:
            os.kill(int(child_marker.read_text().strip()), 0)
        except (OSError, ValueError):
            pass
        else:
            raise RemoteRouteSyncError("REMOTE_SCRAPER_CHILD_ACTIVE")

    payloads: dict[Path, bytes] = {}
    for staged_name, final_name in STAGED_FILES.items():
        source = stage / staged_name
        if not source.is_file():
            raise RemoteRouteSyncError(f"REMOTE_STAGED_FILE_MISSING:{staged_name}")
        payloads[root / final_name] = source.read_bytes()

    replacements = {
        f"https://bookto{expected_suffix}.com".encode(): f"https://bookto{target_suffix}.com".encode(),
        f"https://newto{expected_suffix}.com".encode(): f"https://newto{target_suffix}.com".encode(),
    }
    source_progress_path = root / "source_progress.json"
    source_progress = source_progress_path.read_bytes()
    for old, new in replacements.items():
        source_progress = source_progress.replace(old, new)
    payloads[source_progress_path] = source_progress

    state_path = root / "SCRAPE_STATE.json"
    state = _object(state_path.read_bytes(), "REMOTE_SCRAPE_STATE")
    catalog = json.loads(payloads[root / "CATALOG.json"].decode())
    state["catalog_sha256"] = hashlib.sha256(
        json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    state["domain_suffix"] = target_suffix
    payloads[state_path] = _json_bytes(state)
    _validate_candidates(payloads, root, target_suffix)
    if current_suffix == target_suffix and all(
        path.is_file() and path.read_bytes() == payload for path, payload in payloads.items()
    ):
        return {
            "schema_version": "bookto_remote_route_sync.v1",
            "status": "NOOP",
            "expected_suffix": expected_suffix,
            "target_suffix": target_suffix,
        }

    run_id = f"{datetime.now().astimezone():%Y%m%dT%H%M%S%z}-{uuid.uuid4().hex[:8]}"
    backup = root / "runtime" / "route_sync_backups" / run_id
    receipt_path = root / "runtime" / "route_sync_receipts" / f"{run_id}.json"
    backup.mkdir(parents=True)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    originals = {path: path.read_bytes() for path in payloads}
    for path, payload in originals.items():
        (backup / path.name).write_bytes(payload)
    try:
        for path, payload in payloads.items():
            _atomic(path, payload)
        readback = {path: path.read_bytes() for path in payloads}
        _validate_candidates(readback, root, target_suffix)
    except (OSError, json.JSONDecodeError, RemoteRouteSyncError):
        for path, payload in originals.items():
            _atomic(path, payload)
        raise

    receipt = {
        "schema_version": "bookto_remote_route_sync.v1",
        "status": "COMMITTED",
        "expected_suffix": expected_suffix,
        "target_suffix": target_suffix,
        "backup_dir": str(backup),
        "files": {
            str(path): {
                "old_sha256": _sha256(originals[path]),
                "new_sha256": _sha256(payloads[path]),
            }
            for path in payloads
        },
    }
    _atomic(receipt_path, _json_bytes(receipt))
    receipt["receipt_path"] = str(receipt_path)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--stage", required=True, type=Path)
    parser.add_argument("--expected-suffix", required=True, type=int)
    parser.add_argument("--target-suffix", required=True, type=int)
    args = parser.parse_args()
    try:
        result = sync_remote_route(
            args.root, args.stage, args.expected_suffix, args.target_suffix
        )
    except (OSError, ValueError, json.JSONDecodeError, RemoteRouteSyncError) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
