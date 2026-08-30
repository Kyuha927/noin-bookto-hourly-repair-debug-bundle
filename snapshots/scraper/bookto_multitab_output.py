"""Source writers for text novels and rendered webtoon image manifests."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from bookto_multitab_catalog import episode_expression, safe_name
from bookto_multitab_cdp_core import (
    CdpPage,
    ImageRouteUnavailable,
    load_resource_with_retries,
)
from bookto_multitab_config import ScrapeError
from bookto_multitab_origin_gap_contract import OriginGapContext
from bookto_multitab_origin_gap_recovery import (
    RecoveredImage,
    finalize_origin_gap,
    recover_origin_gap,
)
from bookto_multitab_state import (
    atomic_bytes,
    read_json,
    sha256_bytes,
    write_json,
    write_text,
)


def write_novel(config: dict[str, Any], row: dict[str, Any], chapters: list[dict[str, Any]], client: CdpPage) -> dict[str, Any]:
    chunks: list[str] = []
    for chapter in chapters:
        client.navigate(chapter["url"])
        payload = client.evaluate(episode_expression(row["board"], row["source_kind"]))
        text = str((payload or {}).get("text", "")).strip() if isinstance(payload, dict) else ""
        if not text:
            raise ScrapeError(f"TEXT_EMPTY:{row['item_key']}:{chapter['wr_id']}")
        chunks.append(f"### {chapter['title']} ###\n\n{text}\n\n{'-' * 40}\n\n")
    root = Path(config["source_root"]) / "text" / row["item_key"].replace(":", "_")
    path = root / f"{safe_name(row['title'])}.txt"
    digest = write_text(path, f"제목: {row['title']}\n{'=' * 50}\n\n" + "".join(chunks))
    return {"status": "PASS", "source_kind": "text", "source_path": str(path), "source_sha256": digest, "chapter_count": len(chapters)}


def write_webtoon(config: dict[str, Any], row: dict[str, Any], chapters: list[dict[str, Any]], client: CdpPage) -> dict[str, Any]:
    work_root = Path(config["source_root"]) / "images" / f"{row['item_key'].replace(':', '_')}__{safe_name(row['title'])}"
    manifest: list[dict[str, Any]] = []
    for episode_index, chapter in enumerate(chapters, 1):
        client.navigate(chapter["url"])
        urls: list[str] = []
        for attempt in range(4):
            payload = client.evaluate(episode_expression(row["board"], row["source_kind"]))
            urls = list(dict.fromkeys((payload or {}).get("images", []))) if isinstance(payload, dict) else []
            if urls:
                break
            time.sleep(0.5 * (attempt + 1))
        if not urls:
            raise ScrapeError(f"IMAGES_EMPTY:{row['item_key']}:{chapter['wr_id']}:{chapter['url']}")
        episode_dir = work_root / f"episode_{episode_index:05d}_{safe_name(chapter['title'])}"
        pages: list[dict[str, Any]] = []
        progress_path = episode_dir / ".progress.json"
        progress = read_json(progress_path, {})
        saved_pages = progress.get("pages", []) if progress.get("chapter_url") == chapter["url"] else []
        saved_by_order = {
            int(page["order"]): page
            for page in saved_pages
            if isinstance(page, dict) and str(page.get("path", ""))
        }
        for page_index, url in enumerate(urls, 1):
            recovery: RecoveredImage | None = None
            saved = saved_by_order.get(page_index)
            if saved and saved.get("url") == url and Path(saved["path"]).is_file():
                existing = Path(saved["path"]).read_bytes()
                if sha256_bytes(existing) == saved.get("sha256") and len(existing) == int(saved.get("bytes", -1)):
                    pages.append(saved)
                    continue
            try:
                resource_url, data = load_resource_with_retries(client, url)
            except ImageRouteUnavailable:
                if not pages or int(pages[-1].get("order", 0)) != page_index - 1:
                    raise
                runtime_control = config.get("runtime_control")
                if not isinstance(runtime_control, dict) or not runtime_control.get("root"):
                    raise
                predecessor = pages[-1]
                context = OriginGapContext(
                    runtime_root=Path(str(runtime_control["root"])),
                    item_key=str(row["item_key"]),
                    title=str(row["title"]),
                    chapter_title=str(chapter["title"]),
                    chapter_url=str(chapter["url"]),
                    blocked_url=url,
                    order=page_index,
                    total_pages=len(urls),
                    predecessor_path=Path(str(predecessor["path"])),
                    predecessor_sha256=str(predecessor["sha256"]),
                    predecessor_bytes=int(predecessor["bytes"]),
                )
                recovery = recover_origin_gap(context, client.port)
                resource_url, data = recovery.resource_url, recovery.data
            suffix = Path(resource_url.split("?", 1)[0]).suffix.lower() or ".jpg"
            page_path = episode_dir / f"{page_index:05d}{suffix}"
            atomic_bytes(page_path, data)
            page = {"order": page_index, "url": resource_url, "path": str(page_path), "sha256": sha256_bytes(data), "bytes": len(data)}
            if recovery is not None:
                alignment = recovery.evidence.get("alignment", {})
                page["source_recovery"] = {
                    "status": "PASS",
                    "receipt_path": str(recovery.receipt_path),
                    "full_ncc": alignment.get("full_ncc") if isinstance(alignment, dict) else None,
                }
            pages.append(page)
            write_json(progress_path, {"schema": "newto_cdp_episode_progress_v1", "chapter_url": chapter["url"], "pages": pages})
            if recovery is not None:
                finalize_origin_gap(recovery, page_path, progress_path)
        manifest.append({"episode_order": episode_index, "title": chapter["title"], "url": chapter["url"], "pages": pages})
    manifest_path = work_root / "original_manifest.json"
    write_json(manifest_path, {"schema": "newto_cdp_original_images_v1", "item_key": row["item_key"], "title": row["title"], "source_kind": row["source_kind"], "episodes": manifest})
    return {"status": "PASS", "source_kind": "webtoon_images", "source_path": str(work_root), "manifest_path": str(manifest_path), "episode_count": len(manifest), "image_count": sum(len(e["pages"]) for e in manifest)}
