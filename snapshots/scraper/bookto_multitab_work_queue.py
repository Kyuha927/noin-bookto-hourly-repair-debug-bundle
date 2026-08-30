"""Priority, retry, and failure policy for multi-tab scraping."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from bookto_multitab_assignment import JsonObject, JsonValue
from bookto_multitab_cdp_core import CloudflareChallenge, ImageRouteUnavailable
from bookto_multitab_config import ScrapeError
from bookto_multitab_state import now_iso, read_json

IMAGE_ROUTE_FAILURE_LIMIT = 3


def load_exclusions(config: dict[str, Any], catalog: list[dict[str, Any]]) -> set[str]:
    payload = read_json(Path(config["learned_exclusion_path"]), {})
    prior = {
        (str(row.get("wr_id")), row.get("title"))
        for row in payload.get("rows", [])
        if isinstance(row, dict)
    }
    return {
        row["item_key"]
        for row in catalog
        if row["tab"] == "bookto_novel"
        and (str(row["wr_id"]), row["title"]) in prior
    }


def load_priority(config: dict[str, Any]) -> dict[str, tuple[int, bool]]:
    path = Path(config["priority_path"])
    if not path.is_file():
        return {}
    result: dict[str, tuple[int, bool]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        rank = int(row["external_popularity_rank"] or 10**9)
        result[row["item_key"]] = (rank, bool(row["eligible"]))
    return result


def scrape_priority_key(
    row: dict[str, Any],
    priority: dict[str, tuple[int, bool]],
    attempted_at: Mapping[str, str],
) -> tuple[int, str, int, str, int]:
    rank, eligible = priority.get(row["item_key"], (10**9, False))
    return (
        0 if eligible else 1,
        attempted_at.get(row["item_key"], ""),
        rank,
        row["tab"],
        row["navigation_rank"],
    )


def image_route_probe_item(
    state: dict[str, Any],
    owned_item_keys: set[str] | None = None,
) -> str | None:
    candidates = [
        (str(item.get("updated_at", "")), key)
        for key, item in state.get("items", {}).items()
        if isinstance(item, dict)
        and (owned_item_keys is None or key in owned_item_keys)
        and item.get("status")
        in {"BLOCKED_NEEDS_USER_EXTERNAL_ACTION", "RETRYABLE_EXTERNAL_IMAGE_ROUTE"}
        and str(item.get("error", "")).startswith("IMAGE_ROUTE_UNAVAILABLE:")
    ]
    return min(candidates)[1] if candidates else None


def release_pending_during_image_route(
    pending: list[dict[str, Any]],
    route_probe: str,
) -> list[dict[str, Any]]:
    """Keep one webtoon route probe while releasing independent text work."""
    probe = [row for row in pending if row["item_key"] == route_probe]
    text_work = [
        row
        for row in pending
        if row["source_kind"] == "text" and row["item_key"] != route_probe
    ]
    return probe[:1] + text_work


def apply_image_route_retry_policy(
    previous: Mapping[str, JsonValue] | None,
    current: JsonObject,
) -> JsonObject:
    """Hold one image-gap item after three identical failures."""
    error = current.get("error")
    if (
        current.get("status") != "RETRYABLE_EXTERNAL_IMAGE_ROUTE"
        or not isinstance(error, str)
        or not error.startswith("IMAGE_ROUTE_UNAVAILABLE:")
    ):
        return current
    previous_count = 0
    if (
        previous is not None
        and previous.get("status") == "RETRYABLE_EXTERNAL_IMAGE_ROUTE"
        and previous.get("error") == error
    ):
        stored_count = previous.get("same_failure_count")
        previous_count = (
            stored_count
            if isinstance(stored_count, int)
            and not isinstance(stored_count, bool)
            and stored_count > 0
            else 1
        )
    current_count = current.get("same_failure_count")
    exhausted_count = (
        current_count
        if isinstance(current_count, int)
        and not isinstance(current_count, bool)
        and current_count > 0
        else 1
    )
    attempts = max(previous_count + 1, exhausted_count)
    updated = dict(current)
    updated["same_failure_count"] = attempts
    updated["failure_signature"] = error
    if attempts >= IMAGE_ROUTE_FAILURE_LIMIT:
        updated["status"] = "RECOVERY_REQUIRED"
        updated["error"] = f"ORIGIN_GAP_REPEAT_LIMIT_REACHED:{error}"
    return updated


def failure_record(row: dict[str, Any], error: Exception) -> dict[str, Any]:
    """Map a proved scrape failure without attributing network faults to the user."""
    status: str | None = None
    if isinstance(error, ScrapeError) and str(error).startswith(
        "SOURCE_RECOVERY_REQUIRED:"
    ):
        status = "SOURCE_RECOVERY_REQUIRED"
    if isinstance(error, CloudflareChallenge):
        status = "BLOCKED_NEEDS_USER_EXTERNAL_ACTION"
    if isinstance(error, ImageRouteUnavailable):
        status = "RETRYABLE_EXTERNAL_IMAGE_ROUTE"
    if status is None:
        return {
            "item_key": row["item_key"],
            "title": row["title"],
            "tab": row["tab"],
            "status": "RETRYABLE_ERROR",
            "error": f"{type(error).__name__}:{error}",
            "updated_at": now_iso(),
        }
    record: dict[str, Any] = {
        "item_key": row["item_key"],
        "title": row["title"],
        "tab": row["tab"],
        "status": status,
        "error": str(error),
        "updated_at": now_iso(),
    }
    if isinstance(error, ImageRouteUnavailable) and str(error).startswith(
        "IMAGE_ROUTE_UNAVAILABLE:"
    ):
        record["same_failure_count"] = IMAGE_ROUTE_FAILURE_LIMIT
        record["failure_signature"] = str(error)
    return record
