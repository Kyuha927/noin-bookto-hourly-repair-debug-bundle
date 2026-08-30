from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from bookto_multitab_assignment import canonical_entries_sha256
from bookto_multitab_state import atomic_bytes, now_iso, sha256_bytes, write_json


class RotationArtifactError(RuntimeError):
    pass


DUAL_NAMES = {
    "assignment_new": "NEWMAC_ASSIGNMENT.json",
    "assignment_old": "OLDMAC_ASSIGNMENT.json",
    "pair_validation": "PAIR_VALIDATION.json",
    "oldmac_config": "OLDMAC_multitab_config.json",
    "oldmac_config_sidecar": "OLDMAC_multitab_config.json.sha256",
    "source_config_backup": "multitab_config.before_newmac_assignment.json",
}


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def _object(payload: bytes, code: str) -> dict[str, Any]:
    value = json.loads(payload.decode())
    if not isinstance(value, dict):
        raise RotationArtifactError(f"{code}:OBJECT_REQUIRED")
    return value


def discover_dual_paths(config: dict[str, Any]) -> dict[str, Path]:
    value = config.get("assignment_manifest_path")
    if value is None:
        return {}
    if not isinstance(value, str) or not value:
        raise RotationArtifactError("ASSIGNMENT_MANIFEST_PATH_INVALID")
    assignment = Path(value)
    if not assignment.is_absolute() or assignment.name != DUAL_NAMES["assignment_new"]:
        raise RotationArtifactError("ASSIGNMENT_MANIFEST_PATH_UNEXPECTED")
    package = assignment.resolve().parent
    paths = {key: package / name for key, name in DUAL_NAMES.items()}
    if any(not path.is_file() for path in paths.values()):
        raise RotationArtifactError("DUAL_ROUTE_ARTIFACT_MISSING")
    return paths


def _item_keys(value: dict[str, Any], code: str) -> set[str]:
    entries = value.get("entries")
    if not isinstance(entries, list) or any(not isinstance(row, dict) for row in entries):
        raise RotationArtifactError(f"{code}:ENTRIES_INVALID")
    keys = {str(row.get("item_key", "")) for row in entries}
    if "" in keys or len(keys) != len(entries):
        raise RotationArtifactError(f"{code}:ITEM_KEYS_INVALID")
    return keys


def prepare_dual_payloads(
    *,
    config: dict[str, Any],
    paths: dict[str, Path],
    payloads: dict[Path, bytes],
    target_suffix: int,
    new_bases: dict[str, str],
) -> None:
    if "assignment_new" not in paths:
        return
    catalog_path = Path(str(config.get("catalog_path", ""))).resolve()
    if catalog_path not in payloads:
        raise RotationArtifactError("DUAL_CATALOG_PAYLOAD_MISSING")

    source_config = dict(config)
    source_config.pop("assignment_manifest_path", None)
    source_payload = _json_bytes(source_config)
    payloads[paths["source_config_backup"]] = source_payload
    source_sha = sha256_bytes(source_payload)
    catalog_sha = sha256_bytes(payloads[catalog_path])

    manifests: dict[str, dict[str, Any]] = {}
    for key in ("assignment_new", "assignment_old"):
        manifest = _object(payloads[paths[key]], key.upper())
        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise RotationArtifactError(f"{key.upper()}:ENTRIES_INVALID")
        manifest["catalog_sha256"] = catalog_sha
        manifest["config_sha256"] = source_sha
        manifest["entries_sha256"] = canonical_entries_sha256(entries)
        manifests[key] = manifest
        payloads[paths[key]] = _json_bytes(manifest)

    catalog = json.loads(payloads[catalog_path].decode())
    if not isinstance(catalog, list):
        raise RotationArtifactError("DUAL_CATALOG_ARRAY_REQUIRED")
    catalog_keys = {str(row.get("item_key", "")) for row in catalog if isinstance(row, dict)}
    new_keys = _item_keys(manifests["assignment_new"], "NEWMAC_ASSIGNMENT")
    old_keys = _item_keys(manifests["assignment_old"], "OLDMAC_ASSIGNMENT")
    if new_keys & old_keys or new_keys | old_keys != catalog_keys:
        raise RotationArtifactError("DUAL_ASSIGNMENT_PARTITION_DRIFT")

    pair = _object(payloads[paths["pair_validation"]], "PAIR_VALIDATION")
    if pair.get("status") != "PASS":
        raise RotationArtifactError("PAIR_VALIDATION_NOT_PASS")
    pair.update(
        {
            "validated_at": now_iso(),
            "catalog_sha256": catalog_sha,
            "config_sha256": source_sha,
            "newmac_manifest_sha256": sha256_bytes(payloads[paths["assignment_new"]]),
            "oldmac_manifest_sha256": sha256_bytes(payloads[paths["assignment_old"]]),
            "catalog_total": len(catalog_keys),
            "newmac_assigned": len(new_keys),
            "oldmac_assigned": len(old_keys),
            "intersection": 0,
            "omission": 0,
            "active_item_overlap": 0,
        }
    )
    payloads[paths["pair_validation"]] = _json_bytes(pair)

    oldmac_config = _object(payloads[paths["oldmac_config"]], "OLDMAC_CONFIG")
    oldmac_config["domain_suffix"] = target_suffix
    oldmac_config["base_urls"] = new_bases
    oldmac_config["domain_rotation"] = config["domain_rotation"]
    oldmac_payload = _json_bytes(oldmac_config)
    payloads[paths["oldmac_config"]] = oldmac_payload
    payloads[paths["oldmac_config_sidecar"]] = f"{sha256_bytes(oldmac_payload)}\n".encode()


def reconcile_current_dual(config_path: Path, previous_suffix: int) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = _object(config_path.read_bytes(), "MULTITAB_CONFIG")
    target_suffix = int(config.get("domain_suffix", -1))
    if target_suffix != previous_suffix + 1:
        raise RotationArtifactError("RECONCILE_SUFFIX_NOT_EXACT_PLUS_ONE")
    new_bases = config.get("base_urls")
    if not isinstance(new_bases, dict):
        raise RotationArtifactError("RECONCILE_BASE_URLS_INVALID")
    bases = {route: str(new_bases.get(route, "")) for route in ("bookto", "newto")}
    expected = {route: f"https://{route}{target_suffix}.com" for route in bases}
    if bases != expected:
        raise RotationArtifactError("RECONCILE_ROUTE_INVALID")

    paths = discover_dual_paths(config)
    if not paths:
        raise RotationArtifactError("RECONCILE_DUAL_ARTIFACTS_MISSING")
    catalog_path = Path(str(config["catalog_path"])).resolve()
    originals = {path: path.read_bytes() for path in paths.values()}
    payloads = {catalog_path: catalog_path.read_bytes()}
    replacements = {
        f"https://{route}{previous_suffix}.com".encode(): bases[route].encode()
        for route in bases
    }
    for key, path in paths.items():
        if key == "oldmac_config_sidecar":
            continue
        payload = originals[path]
        for old, new in replacements.items():
            payload = payload.replace(old, new)
        payloads[path] = payload
    prepare_dual_payloads(
        config=config,
        paths=paths,
        payloads=payloads,
        target_suffix=target_suffix,
        new_bases=bases,
    )

    run_id = f"{datetime.now().astimezone():%Y%m%dT%H%M%S%z}-{uuid.uuid4().hex[:8]}"
    root = config_path.parent
    backup = root / "supervisor_logs" / "domain_change_backups" / f"{run_id}-dual-reconcile"
    receipt_path = root / "supervisor_logs" / "domain_change_receipts" / f"{run_id}-dual-reconcile.json"
    backup.mkdir(parents=True)
    for path, payload in originals.items():
        atomic_bytes(backup / path.name, payload)
    try:
        for path in paths.values():
            atomic_bytes(path, payloads[path])
    except OSError:
        for path, payload in originals.items():
            atomic_bytes(path, payload)
        raise
    receipt = {
        "schema_version": "bookto_dual_route_reconcile.v1",
        "status": "COMMITTED",
        "previous_suffix": previous_suffix,
        "target_suffix": target_suffix,
        "backup_dir": str(backup),
        "files": {
            str(path): {
                "old_sha256": sha256_bytes(originals[path]),
                "new_sha256": sha256_bytes(payloads[path]),
            }
            for path in paths.values()
        },
        "committed_at": now_iso(),
    }
    write_json(receipt_path, receipt)
    receipt["receipt_path"] = str(receipt_path)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--previous-suffix", required=True, type=int)
    args = parser.parse_args()
    try:
        print(json.dumps(reconcile_current_dual(args.config, args.previous_suffix), ensure_ascii=False))
    except (OSError, ValueError, KeyError, json.JSONDecodeError, RotationArtifactError) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
