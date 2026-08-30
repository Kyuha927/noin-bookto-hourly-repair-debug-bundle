from __future__ import annotations

import time
from pathlib import Path

from bookto_multitab_assignment import JsonObject
from bookto_multitab_config import ScrapeError
from bookto_multitab_progress import save_progress
from bookto_multitab_state import now_iso, read_json, write_json
from bookto_multitab_work_queue import apply_image_route_retry_policy


def persist_result_behind_merge_barrier(
    config: JsonObject,
    stale_state: JsonObject,
    raw_result: JsonObject,
) -> JsonObject:
    manifest_path = config.get("assignment_manifest_path")
    lock_path = (
        Path(manifest_path).parent / "collect_merge.lock"
        if isinstance(manifest_path, str) and manifest_path
        else None
    )
    if lock_path is not None:
        deadline = time.monotonic() + 600
        while True:
            try:
                lock_path.mkdir()
                break
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise ScrapeError("STATE_OWNERSHIP_BARRIER_TIMEOUT") from None
                time.sleep(0.1)
    try:
        state_path = Path(str(config["state_path"]))
        latest_state = read_json(state_path, {})
        if not isinstance(latest_state, dict):
            raise ScrapeError("CANONICAL_STATE_INVALID")
        merged_state: JsonObject = {**stale_state, **latest_state}
        stale_items = stale_state.get("items")
        latest_items = latest_state.get("items")
        items = {
            **(stale_items if isinstance(stale_items, dict) else {}),
            **(latest_items if isinstance(latest_items, dict) else {}),
        }
        item_key = raw_result.get("item_key")
        if not isinstance(item_key, str) or not item_key:
            raise ScrapeError("SCRAPE_RESULT_ITEM_KEY_INVALID")
        previous = items.get(item_key)
        oldmac_owned = (
            isinstance(previous, dict)
            and previous.get("status") == "PASS"
            and isinstance(previous.get("oldmac_bundle_sha256"), str)
        )
        if not oldmac_owned:
            items[item_key] = apply_image_route_retry_policy(
                previous if isinstance(previous, dict) else None,
                raw_result,
            )
        merged_state["items"] = items
        merged_state["updated_at"] = now_iso()
        write_json(state_path, merged_state)
        catalog_value = read_json(Path(str(config["catalog_path"])), [])
        if not isinstance(catalog_value, list) or any(
            not isinstance(row, dict) for row in catalog_value
        ):
            raise ScrapeError("CANONICAL_CATALOG_INVALID")
        save_progress(config, catalog_value, merged_state)
        return merged_state
    finally:
        if lock_path is not None:
            lock_path.rmdir()
