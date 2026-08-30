"""Resumable pure-CDP scraper for Bookto novels and Newtoki webtoons."""

from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import ExitStack
from pathlib import Path
from typing import Any

from bookto_multitab_assignment import AssignmentError, assigned_catalog
from bookto_multitab_catalog import (
    CatalogError,
    board_specs,
    board_url,
    detail_expression,
    list_expression,
    parse_detail,
    parse_list,
)
from bookto_multitab_cdp_cli import parse_args
from bookto_multitab_cdp_core import (
    AUTOMATIC_CHALLENGE_WAIT_SECONDS,
    CdpError,
    CdpPage,
    CloudflareChallenge,
    ImageRouteUnavailable,
    close_target,
    new_target,
)
from bookto_multitab_config import ScrapeError, load_config
from bookto_multitab_output import write_novel, write_webtoon
from bookto_multitab_progress import save_progress
from bookto_multitab_schedule import image_route_probe_is_due
from bookto_multitab_state import item_key as state_item_key
from bookto_multitab_state import (
    now_iso,
    read_json,
    sha256_bytes,
    write_json,
)
from bookto_multitab_state_persistence import persist_result_behind_merge_barrier
from bookto_multitab_targets import cleanup_orphan_targets, register_background_target
from bookto_multitab_work_queue import (
    failure_record,
    image_route_probe_item,
    load_exclusions,
    load_priority,
    release_pending_during_image_route,
    scrape_priority_key,
)


def scan_catalog(config: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    target = new_target(config["cdp_port"])
    marker = register_background_target(config, target, "__catalog__")
    client = CdpPage(config["cdp_port"], target)
    catalog: list[dict[str, Any]] = []
    try:
        for spec in board_specs(config["base_urls"]):
            rank = 0
            empty_pages = 0
            max_pages = int(config.get("max_list_pages", 500))
            for page in range(1, max_pages + 1):
                client.navigate(
                    board_url(spec, page),
                    automatic_challenge_wait_seconds=AUTOMATIC_CHALLENGE_WAIT_SECONDS,
                )
                payload = client.evaluate(list_expression(spec["board"]))
                rows = parse_list(payload, spec, page)
                if not rows:
                    empty_pages += 1
                    if page == 1 or empty_pages >= 2:
                        if page == 1:
                            raise ScrapeError(f"LIST_EMPTY:{spec['tab']}")
                        break
                    continue
                empty_pages = 0
                for row in rows:
                    rank += 1
                    row["navigation_rank"] = rank
                    row["item_key"] = state_item_key(row)
                    catalog.append(row)
        if len({row["item_key"] for row in catalog}) != len(catalog):
            raise ScrapeError("CATALOG_DUPLICATE_ITEM_KEY")
        state["catalog_complete"] = True
        state["catalog_sha256"] = sha256_bytes(
            json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()
        )
        state["catalog_count"] = len(catalog)
        state["updated_at"] = now_iso()
        write_json(Path(config["catalog_path"]), catalog)
        write_json(Path(config["state_path"]), state)
        save_progress(config, catalog, state)
        return catalog
    finally:
        client.close()
        close_target(config["cdp_port"], target["id"])
        marker.unlink(missing_ok=True)


def scrape_one(
    config: dict[str, Any], row: dict[str, Any], max_chapters: int
) -> dict[str, Any]:
    cleanup = ExitStack()
    try:
        target = new_target(config["cdp_port"])
        cleanup.callback(close_target, config["cdp_port"], target["id"])
        marker = register_background_target(config, target, row["item_key"])
        cleanup.callback(marker.unlink, missing_ok=True)
        client = CdpPage(config["cdp_port"], target)
        cleanup.callback(client.close)
        if row["source_kind"] == "webtoon_images":
            client.enable_network_capture()
        page_state = client.navigate(
            row["url"],
            automatic_challenge_wait_seconds=AUTOMATIC_CHALLENGE_WAIT_SECONDS,
        )
        chapters: list[dict[str, Any]] = []
        detail = {"source_empty": False}
        for attempt in range(4):
            detail = client.evaluate(detail_expression(row["board"]))
            chapters = parse_detail(detail, int(row["wr_id"]))
            if chapters:
                break
            time.sleep(0.5 * (attempt + 1))
        if not chapters:
            if detail.get("source_empty") is True or "연재글이 없습니다" in str(
                page_state.get("body", "")
            ):
                raise ScrapeError(f"SOURCE_RECOVERY_REQUIRED:{row['item_key']}")
            raise ScrapeError(f"CHAPTERS_EMPTY:{row['item_key']}")
        complete = max_chapters <= 0 or len(chapters) <= max_chapters
        selected = chapters if complete else chapters[:max_chapters]
        result = (
            write_novel(config, row, selected, client)
            if row["source_kind"] == "text"
            else write_webtoon(config, row, selected, client)
        )
        if not complete:
            result["status"] = "SMOKE_PARTIAL"
            result["expected_chapter_count"] = len(chapters)
        return {
            "item_key": row["item_key"],
            "title": row["title"],
            "tab": row["tab"],
            **result,
            "updated_at": now_iso(),
        }
    except (
        CloudflareChallenge,
        ImageRouteUnavailable,
        CdpError,
        ScrapeError,
        CatalogError,
        ValueError,
    ) as error:
        return failure_record(row, error)
    finally:
        cleanup.close()


def run(
    config: dict[str, Any],
    phase: str,
    max_items: int,
    tab_filter: str | None,
    item_keys: list[str],
    max_chapters: int,
) -> int:
    cleanup_orphan_targets(config)
    state = read_json(
        Path(config["state_path"]),
        {"schema_version": 1, "generation_id": config["generation_id"], "items": {}},
    )
    state.setdefault("items", {})
    catalog = read_json(Path(config["catalog_path"]), [])
    if phase in {"list", "all"} or not state.get("catalog_complete"):
        catalog = scan_catalog(config, state)
    if phase == "list":
        return 0
    owned_catalog = assigned_catalog(config, catalog)
    excluded = load_exclusions(config, catalog)
    priority = load_priority(config)
    requested = set(item_keys)
    pending = [
        row
        for row in owned_catalog
        if state["items"].get(row["item_key"], {}).get("status")
        not in {"PASS", "SOURCE_RECOVERY_REQUIRED", "RECOVERY_REQUIRED"}
        and row["item_key"] not in excluded
        and (tab_filter is None or row["tab"] == tab_filter)
        and (not requested or row["item_key"] in requested)
    ]
    attempted_at = {
        key: item.get("updated_at", "") for key, item in state["items"].items()
    }
    pending.sort(key=lambda row: scrape_priority_key(row, priority, attempted_at))
    owned_item_keys = {str(row["item_key"]) for row in owned_catalog}
    route_probe = image_route_probe_item(state, owned_item_keys)
    if route_probe is not None and not requested:
        probe_updated_at = str(state["items"][route_probe].get("updated_at", ""))
        due_probe = route_probe if image_route_probe_is_due(probe_updated_at) else ""
        pending = release_pending_during_image_route(pending, due_probe)
    if max_items > 0:
        pending = pending[:max_items]
    workers = max(1, min(int(config.get("workers", 2)), len(pending) or 1))
    with ThreadPoolExecutor(
        max_workers=workers, thread_name_prefix="multitab-cdp"
    ) as executor:
        futures = {
            executor.submit(scrape_one, config, row, max_chapters): row
            for row in pending
        }
        for future in as_completed(futures):
            result = future.result()
            state = persist_result_behind_merge_barrier(config, state, result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        config = load_config(args.config.resolve())
        if args.cleanup_targets:
            print(
                json.dumps(
                    {"cleaned_target_ids": cleanup_orphan_targets(config)},
                    ensure_ascii=False,
                )
            )
            return 0
        return run(
            config,
            args.phase,
            args.max_items,
            args.tab,
            args.item_key,
            args.max_chapters,
        )
    except (
        OSError,
        AssignmentError,
        ScrapeError,
        CatalogError,
        ValueError,
        CdpError,
    ) as error:
        print(
            json.dumps(
                {"status": "FAIL", "error": f"{type(error).__name__}:{error}"},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 78


if __name__ == "__main__":
    raise SystemExit(main())
