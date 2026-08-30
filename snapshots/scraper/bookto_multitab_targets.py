"""Durable ownership receipts for background CDP targets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bookto_multitab_cdp_core import close_target
from bookto_multitab_config import ScrapeError
from bookto_multitab_state import now_iso, read_json, write_json


def _target_marker_dir(config: dict[str, Any]) -> Path:
    return Path(config["state_path"]).parent / "runtime" / "scraper_targets"


def register_background_target(
    config: dict[str, Any], target: dict[str, Any], item_key: str
) -> Path:
    marker = _target_marker_dir(config) / f"{target['id']}.json"
    write_json(
        marker,
        {
            "schema": "bookto_multitab_background_target_v1",
            "target_id": target["id"],
            "cdp_port": config["cdp_port"],
            "item_key": item_key,
            "created_at": now_iso(),
        },
    )
    return marker


def cleanup_orphan_targets(config: dict[str, Any]) -> list[str]:
    marker_dir = _target_marker_dir(config)
    if not marker_dir.is_dir():
        return []
    cleaned: list[str] = []
    for marker in sorted(marker_dir.glob("*.json")):
        receipt = read_json(marker, {})
        target_id = str(receipt.get("target_id", "")) if isinstance(receipt, dict) else ""
        if (
            receipt.get("schema") != "bookto_multitab_background_target_v1"
            or target_id != marker.stem
            or int(receipt.get("cdp_port", -1)) != int(config["cdp_port"])
        ):
            raise ScrapeError(f"BACKGROUND_TARGET_RECEIPT_INVALID:{marker}")
        close_target(int(config["cdp_port"]), target_id)
        marker.unlink()
        cleaned.append(target_id)
    return cleaned
