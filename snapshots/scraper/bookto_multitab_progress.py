"""Atomic compatibility progress writer for the multi-tab source lane."""

from __future__ import annotations

from pathlib import Path

from bookto_multitab_assignment import JsonObject
from bookto_multitab_state import now_iso, write_json


class ProgressError(RuntimeError):
    """Progress cannot be derived from the supplied canonical state."""


def save_progress(
    config: JsonObject,
    catalog: list[JsonObject],
    state: JsonObject,
) -> None:
    state_items = state.get("items", {})
    if not isinstance(state_items, dict):
        raise ProgressError("CANONICAL_STATE_ITEMS_INVALID")
    passed_urls = [
        row["url"]
        for row in catalog
        if isinstance(row.get("item_key"), str)
        and isinstance(row.get("url"), str)
        and isinstance(state_items.get(str(row["item_key"])), dict)
        and state_items[str(row["item_key"])].get("status") == "PASS"
    ]
    progress: JsonObject = {
        "schema_version": 2,
        "generation_id": config["generation_id"],
        "updated_at": now_iso(),
        "tabs": config["tabs"],
        "catalog_complete": state.get("catalog_complete", False),
        "rows": catalog,
        "novels": catalog,
        "downloaded_novels": passed_urls,
        "skipped_novels": [],
        "popularity_order_policy": "external_only_site_navigation_rank_v1",
        "bookto_internal_popularity_trusted": False,
    }
    write_json(Path(str(config["progress_path"])), progress)
