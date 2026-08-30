"""Fail-closed +1 domain rotation for the four-tab Bookto/Newto lane."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import uuid
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from bookto_multitab_cdp_core import (
    CdpError,
    CdpPage,
    CloudflareChallenge,
    RetryableCloudflareChallenge,
    close_target,
    new_target,
)
from bookto_multitab_rotation_artifacts import (
    RotationArtifactError,
    discover_dual_paths,
    prepare_dual_payloads,
)
from bookto_multitab_state import atomic_bytes, now_iso, sha256_bytes, write_json


class RotationError(RuntimeError):
    """A domain rotation invariant failed; active state must remain unchanged."""


Probe = Callable[[int, str], dict[str, str]]
ROUTES = ("bookto", "newto")
ACTIVE_KEYS = ("catalog_path", "progress_path", "priority_path", "state_path")


def _expected_base(route: str, suffix: int) -> str:
    return f"https://{route}{suffix}.com"


def next_base_urls(
    current: dict[str, str], expected_suffix: int, target_suffix: int
) -> dict[str, str]:
    if target_suffix != expected_suffix + 1:
        raise RotationError("SUFFIX_MUST_INCREMENT_BY_ONE")
    expected = {route: _expected_base(route, expected_suffix) for route in ROUTES}
    if current != expected:
        raise RotationError("CURRENT_SUFFIX_COMPARE_AND_SWAP_MISMATCH")
    return {route: _expected_base(route, target_suffix) for route in ROUTES}


def probe_route(port: int, base_url: str) -> dict[str, str]:
    target = new_target(port)
    client: CdpPage | None = None
    try:
        try:
            client = CdpPage(port, target)
            state = client.navigate(f"{base_url}/")
        except (CloudflareChallenge, RetryableCloudflareChallenge) as error:
            return {"base_url": base_url, "status": "cloudflare", "evidence": str(error)}
        except CdpError as error:
            status = "unavailable" if str(error).startswith("SITE_ROUTE_UNAVAILABLE:") else "retryable"
            return {"base_url": base_url, "status": status, "evidence": str(error)}
        href = str(state.get("href", ""))
        expected_host = base_url.removeprefix("https://")
        if not re.match(rf"^https://{re.escape(expected_host)}(?:/|$)", href):
            return {"base_url": base_url, "status": "wrong_host", "evidence": href}
        return {"base_url": base_url, "status": "reachable", "evidence": href}
    finally:
        if client is not None:
            client.close()
        close_target(port, target["id"])


def _validate_probes(
    current_rounds: list[dict[str, dict[str, str]]], next_probes: dict[str, dict[str, str]]
) -> None:
    if len(current_rounds) != 2 or any(
        round_result[route]["status"] not in {"unavailable", "wrong_host"}
        for round_result in current_rounds
        for route in ROUTES
    ):
        raise RotationError("CURRENT_ROUTE_NOT_REPRODUCIBLY_UNAVAILABLE")
    if any(next_probes[route]["status"] not in {"reachable", "cloudflare"} for route in ROUTES):
        raise RotationError("NEXT_SUFFIX_NOT_REACHABLE")


def _active_paths(config_path: Path, config: dict[str, Any]) -> dict[str, Path]:
    paths = {"config": config_path}
    for key in ACTIVE_KEYS:
        value = config.get(key)
        if not isinstance(value, str):
            raise RotationError(f"ACTIVE_PATH_MISSING:{key}")
        paths[key] = Path(value).resolve()
    paths.update(discover_dual_paths(config))
    if any(not path.is_file() for path in paths.values()):
        raise RotationError("ACTIVE_FILE_MISSING")
    return paths


def _host_suffixes(payloads: list[bytes]) -> dict[str, set[int]]:
    result = {route: set() for route in ROUTES}
    pattern = re.compile(rb"https://(bookto|newto)([0-9]+)[.]com")
    for payload in payloads:
        for route, suffix in pattern.findall(payload):
            result[route.decode()].add(int(suffix))
    return result


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def _prepare_payloads(
    config_path: Path, expected_suffix: int, target_suffix: int
) -> tuple[dict[Path, bytes], dict[Path, bytes], dict[str, str], dict[str, str]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise RotationError("MULTITAB_CONFIG_INVALID")
    paths = _active_paths(config_path, config)
    originals = {path: path.read_bytes() for path in paths.values()}
    observed = _host_suffixes([payload for path, payload in originals.items() if path != config_path])
    if observed != {route: {expected_suffix} for route in ROUTES}:
        raise RotationError(f"ACTIVE_SUFFIX_SET_MISMATCH:{observed}")
    current = config.get("base_urls") or {
        route: _expected_base(route, expected_suffix) for route in ROUTES
    }
    if not isinstance(current, dict):
        raise RotationError("MULTITAB_BASE_URLS_INVALID")
    old_bases = {route: str(current.get(route, "")) for route in ROUTES}
    new_bases = next_base_urls(old_bases, expected_suffix, target_suffix)
    replacements = {
        old_bases[route].encode(): new_bases[route].encode() for route in ROUTES
    }

    payloads: dict[Path, bytes] = {}
    for key, path in paths.items():
        if key in {"config", "oldmac_config_sidecar"}:
            continue
        payload = originals[path]
        for old, new in replacements.items():
            payload = payload.replace(old, new)
        payloads[path] = payload

    catalog = json.loads(payloads[paths["catalog_path"]].decode())
    state = json.loads(payloads[paths["state_path"]].decode())
    for item in state.get("items", {}).values():
        if isinstance(item, dict) and "SITE_ROUTE_UNAVAILABLE" in str(item.get("error", "")):
            item.pop("error", None)
            item["status"] = "PENDING_ROUTE_REFRESH"
            item["route_refresh"] = {
                "from_suffix": expected_suffix,
                "to_suffix": target_suffix,
                "updated_at": now_iso(),
            }
    state["catalog_sha256"] = hashlib.sha256(
        json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    state["domain_suffix"] = target_suffix
    payloads[paths["state_path"]] = _json_bytes(state)

    config["base_urls"] = new_bases
    config["domain_suffix"] = target_suffix
    config["background_only"] = True
    config["workers"] = 4
    config["domain_rotation"] = {
        "policy": "exact_plus_one_after_two_background_probes_v1",
        "updated_at": now_iso(),
    }
    payloads[config_path] = _json_bytes(config)
    prepare_dual_payloads(
        config=config,
        paths=paths,
        payloads=payloads,
        target_suffix=target_suffix,
        new_bases=new_bases,
    )
    post = _host_suffixes(list(payloads.values()))
    if post != {route: {target_suffix} for route in ROUTES}:
        raise RotationError(f"POST_ROTATION_SUFFIX_SET_MISMATCH:{post}")
    return originals, payloads, old_bases, new_bases


def _assert_inactive(root: Path) -> None:
    child_path = root / "runtime" / "scraper.child.pid"
    if not child_path.is_file():
        return
    try:
        child_pid = int(child_path.read_text(encoding="utf-8").strip())
        os.kill(child_pid, 0)
    except (OSError, ValueError):
        return
    raise RotationError(f"SCRAPER_CHILD_ACTIVE:{child_pid}")


def migrate(
    config_path: Path,
    expected_suffix: int,
    target_suffix: int,
    probe: Probe = probe_route,
    pause: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    root = config_path.parent
    lock = root / "runtime" / "domain_change.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise RotationError("DUPLICATE_DOMAIN_CHANGE_SUPPRESSED") from error
    try:
        _assert_inactive(root)
        originals, payloads, old_bases, new_bases = _prepare_payloads(
            config_path, expected_suffix, target_suffix
        )
        port = int(json.loads(originals[config_path])["cdp_port"])
        current_rounds = [
            {route: probe(port, old_bases[route]) for route in ROUTES}
        ]
        pause(0.75)
        current_rounds.append({route: probe(port, old_bases[route]) for route in ROUTES})
        next_probes = {route: probe(port, new_bases[route]) for route in ROUTES}
        _validate_probes(current_rounds, next_probes)

        run_id = f"{datetime.now().astimezone():%Y%m%dT%H%M%S%z}-{uuid.uuid4().hex[:8]}"
        backup_dir = root / "supervisor_logs" / "domain_change_backups" / run_id
        receipt_path = root / "supervisor_logs" / "domain_change_receipts" / f"{run_id}.json"
        backup_dir.mkdir(parents=True)
        for path, payload in originals.items():
            atomic_bytes(backup_dir / path.name, payload)
        receipt: dict[str, Any] = {
            "run_id": run_id,
            "status": "PREPARED",
            "old_suffix": expected_suffix,
            "new_suffix": target_suffix,
            "old_base_urls": old_bases,
            "new_base_urls": new_bases,
            "current_probe_rounds": current_rounds,
            "next_probes": next_probes,
            "background_only": True,
            "workers": 4,
            "backup_dir": str(backup_dir),
            "files": {
                str(path): {
                    "old_sha256": sha256_bytes(originals[path]),
                    "new_sha256": sha256_bytes(payloads[path]),
                }
                for path in originals
            },
        }
        write_json(receipt_path, receipt)
        try:
            for path, payload in payloads.items():
                atomic_bytes(path, payload)
            check = _host_suffixes([path.read_bytes() for path in payloads])
            if check != {route: {target_suffix} for route in ROUTES}:
                raise RotationError(f"READBACK_SUFFIX_SET_MISMATCH:{check}")
        except (OSError, RotationError):
            for path, payload in originals.items():
                atomic_bytes(path, payload)
            receipt["status"] = "ROLLED_BACK"
            write_json(receipt_path, receipt)
            raise
        receipt["status"] = "COMMITTED"
        receipt["committed_at"] = now_iso()
        receipt["receipt_path"] = str(receipt_path)
        write_json(receipt_path, receipt)
        return receipt
    finally:
        lock.rmdir()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--expected-suffix", required=True, type=int)
    parser.add_argument("--target-suffix", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        receipt = migrate(args.config, args.expected_suffix, args.target_suffix)
    except (
        OSError,
        ValueError,
        json.JSONDecodeError,
        RotationArtifactError,
        RotationError,
    ) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
