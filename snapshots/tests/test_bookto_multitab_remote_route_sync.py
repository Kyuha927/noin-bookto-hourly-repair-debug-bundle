from __future__ import annotations

import hashlib
import json
from pathlib import Path

from bookto_multitab_remote_route_sync import sync_remote_route


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_remote_route_sync_preserves_progress_and_rebinds_package(tmp_path: Path) -> None:
    root = tmp_path / "remote"
    stage = tmp_path / "stage"
    root.mkdir()
    stage.mkdir()
    catalog = [{"item_key": "newto_fafa:1", "url": "https://ROTATING-HOST.example/item/1"}]
    _write(stage / "CATALOG.json", catalog)
    catalog_sha = hashlib.sha256((stage / "CATALOG.json").read_bytes()).hexdigest()
    assignment = {
        "schema_version": 1,
        "assigned_machine": "OldMac",
        "entries": catalog,
        "catalog_sha256": catalog_sha,
    }
    _write(stage / "OLDMAC_ASSIGNMENT.json", assignment)
    assignment_sha = hashlib.sha256(
        (stage / "OLDMAC_ASSIGNMENT.json").read_bytes()
    ).hexdigest()
    _write(
        stage / "PAIR_VALIDATION.json",
        {
            "status": "PASS",
            "catalog_sha256": catalog_sha,
            "oldmac_manifest_sha256": assignment_sha,
        },
    )
    (stage / "PRIORITY.jsonl").write_text(
        json.dumps(catalog[0]) + "\n", encoding="utf-8"
    )
    config = {
        "schema_version": 1,
        "domain_suffix": 31,
        "base_urls": {"bookto": "https://ROTATING-HOST.example", "newto": "https://ROTATING-HOST.example"},
        "catalog_path": str(root / "CATALOG.json"),
        "assignment_manifest_path": str(root / "OLDMAC_ASSIGNMENT.json"),
    }
    _write(stage / "OLDMAC_multitab_config.json", config)
    config_sha = hashlib.sha256(
        (stage / "OLDMAC_multitab_config.json").read_bytes()
    ).hexdigest()
    (stage / "OLDMAC_multitab_config.json.sha256").write_text(config_sha + "\n")

    old_config = {
        **config,
        "domain_suffix": 30,
        "base_urls": {"bookto": "https://ROTATING-HOST.example", "newto": "https://ROTATING-HOST.example"},
    }
    _write(root / "multitab_config.json", old_config)
    (root / "multitab_config.json.sha256").write_text("old\n")
    _write(root / "CATALOG.json", [{"url": "https://ROTATING-HOST.example/item/1"}])
    _write(root / "OLDMAC_ASSIGNMENT.json", {"entries": []})
    _write(root / "PAIR_VALIDATION.json", {"status": "PASS"})
    (root / "PRIORITY.jsonl").write_text("https://ROTATING-HOST.example/item/1\n")
    _write(
        root / "source_progress.json",
        {"rows": [{"url": "https://ROTATING-HOST.example/item/1", "status": "PASS"}]},
    )
    _write(root / "SCRAPE_STATE.json", {"items": {"newto_fafa:1": {"status": "PASS"}}})

    receipt = sync_remote_route(root, stage, 30, 31)

    progress = json.loads((root / "source_progress.json").read_text())
    state = json.loads((root / "SCRAPE_STATE.json").read_text())
    assert receipt["status"] == "COMMITTED"
    assert progress["rows"][0]["status"] == "PASS"
    assert progress["rows"][0]["url"] == "https://ROTATING-HOST.example/item/1"
    assert state["items"]["newto_fafa:1"]["status"] == "PASS"
    assert state["domain_suffix"] == 31
    assert Path(receipt["backup_dir"]).is_dir()
    assert sync_remote_route(root, stage, 30, 31)["status"] == "NOOP"
