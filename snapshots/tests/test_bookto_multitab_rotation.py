from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import bookto_multitab_rotation as rotation
from bookto_multitab_assignment import canonical_entries_sha256
from bookto_multitab_cdp_core import RetryableCloudflareChallenge


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_lane(root: Path) -> Path:
    catalog = [
        {"item_key": "bookto_novel:1", "url": "https://ROTATING-HOST.example/bbs/board.php?wr_id=1"},
        {"item_key": "newto_fafa:2", "url": "https://ROTATING-HOST.example/bbs/board.php?wr_id=2"},
    ]
    catalog_sha = hashlib.sha256(
        json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    config = {
        "schema_version": 1,
        "generation_id": "bookto29-newto29-g1",
        "cdp_port": 9240,
        "catalog_path": str(root / "CATALOG.json"),
        "progress_path": str(root / "source_progress.json"),
        "priority_path": str(root / "PRIORITY.jsonl"),
        "state_path": str(root / "SCRAPE_STATE.json"),
        "workers": 2,
    }
    package = root / "distributed" / "bookto29-newto29-oldmac-smoke-g1"
    package.mkdir(parents=True)
    _write_json(package / "multitab_config.before_newmac_assignment.json", config)
    source_config_sha = hashlib.sha256(
        (json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest()
    new_entries = [catalog[0]]
    old_entries = [catalog[1]]
    new_manifest = {
        "schema_version": 1,
        "lane_id": root.name,
        "generation": "bookto29-newto29-oldmac-smoke-g1",
        "created_at": "2026-08-30T00:00:00+09:00",
        "assigned_machine": "NewMac",
        "catalog_sha256": "",
        "config_sha256": source_config_sha,
        "entries": new_entries,
        "entries_sha256": canonical_entries_sha256(new_entries),
    }
    old_manifest = {
        **new_manifest,
        "assigned_machine": "OldMac",
        "entries": old_entries,
        "entries_sha256": canonical_entries_sha256(old_entries),
    }
    config["assignment_manifest_path"] = str(package / "NEWMAC_ASSIGNMENT.json")
    _write_json(root / "multitab_config.json", config)
    _write_json(root / "CATALOG.json", catalog)
    catalog_file_sha = hashlib.sha256((root / "CATALOG.json").read_bytes()).hexdigest()
    new_manifest["catalog_sha256"] = catalog_file_sha
    old_manifest["catalog_sha256"] = catalog_file_sha
    _write_json(package / "NEWMAC_ASSIGNMENT.json", new_manifest)
    _write_json(package / "OLDMAC_ASSIGNMENT.json", old_manifest)
    new_sha = hashlib.sha256((package / "NEWMAC_ASSIGNMENT.json").read_bytes()).hexdigest()
    old_sha = hashlib.sha256((package / "OLDMAC_ASSIGNMENT.json").read_bytes()).hexdigest()
    _write_json(
        package / "PAIR_VALIDATION.json",
        {
            "schema_version": 1,
            "status": "PASS",
            "validated_at": "2026-08-30T00:00:00+09:00",
            "generation": "bookto29-newto29-oldmac-smoke-g1",
            "catalog_sha256": catalog_file_sha,
            "config_sha256": source_config_sha,
            "newmac_manifest_sha256": new_sha,
            "oldmac_manifest_sha256": old_sha,
            "catalog_total": 2,
            "newmac_assigned": 1,
            "oldmac_assigned": 1,
            "oldmac_item_key": "newto_fafa:2",
            "intersection": 0,
            "omission": 0,
            "active_item_overlap": 0,
        },
    )
    oldmac_config = {
        **config,
        "assignment_manifest_path": "/remote/OLDMAC_ASSIGNMENT.json",
        "catalog_path": "/remote/CATALOG.json",
        "base_urls": {"bookto": "https://ROTATING-HOST.example", "newto": "https://ROTATING-HOST.example"},
        "domain_suffix": 29,
    }
    _write_json(package / "OLDMAC_multitab_config.json", oldmac_config)
    oldmac_sha = hashlib.sha256((package / "OLDMAC_multitab_config.json").read_bytes()).hexdigest()
    (package / "OLDMAC_multitab_config.json.sha256").write_text(oldmac_sha + "\n")
    _write_json(root / "source_progress.json", {"rows": catalog, "novels": catalog})
    (root / "PRIORITY.jsonl").write_text(
        json.dumps({"item_key": "bookto_novel:1", "url": catalog[0]["url"]}) + "\n"
        + json.dumps({"item_key": "newto_fafa:2", "url": catalog[1]["url"]}) + "\n",
        encoding="utf-8",
    )
    _write_json(
        root / "SCRAPE_STATE.json",
        {
            "catalog_sha256": catalog_sha,
            "items": {
                "bookto_novel:1": {
                    "status": "RETRYABLE_ERROR",
                    "error": "CdpError:SITE_ROUTE_UNAVAILABLE:https://ROTATING-HOST.example/x",
                }
            },
        },
    )
    return root / "multitab_config.json"


def test_domain_rotation_is_exactly_one_suffix_and_never_skips() -> None:
    assert rotation.next_base_urls(
        {"bookto": "https://ROTATING-HOST.example", "newto": "https://ROTATING-HOST.example"}, 29, 30
    ) == {"bookto": "https://ROTATING-HOST.example", "newto": "https://ROTATING-HOST.example"}

    with pytest.raises(rotation.RotationError, match="SUFFIX_MUST_INCREMENT_BY_ONE"):
        rotation.next_base_urls(
            {"bookto": "https://ROTATING-HOST.example", "newto": "https://ROTATING-HOST.example"}, 29, 31
        )


def test_rotation_accepts_reproducible_off_host_retirement_redirect() -> None:
    current_rounds = [
        {
            route: {
                "base_url": f"https://{route}29.com",
                "status": "wrong_host",
                "evidence": "https://t.me/newtokinews",
            }
            for route in rotation.ROUTES
        }
        for _ in range(2)
    ]
    next_probes = {
        route: {
            "base_url": f"https://{route}30.com",
            "status": "reachable",
            "evidence": f"https://{route}30.com/",
        }
        for route in rotation.ROUTES
    }

    rotation._validate_probes(current_rounds, next_probes)


def test_probe_route_classifies_setup_timeout_and_closes_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = {"id": "target-1"}
    closed: list[tuple[int, str]] = []
    monkeypatch.setattr(rotation, "new_target", lambda _port: target)

    def fail_page(_port: int, _target: dict[str, str]) -> object:
        raise rotation.CdpError("CDP_TIMEOUT:Page.enable")

    monkeypatch.setattr(rotation, "CdpPage", fail_page)
    monkeypatch.setattr(
        rotation,
        "close_target",
        lambda port, target_id: closed.append((port, target_id)),
    )

    result = rotation.probe_route(9240, "https://ROTATING-HOST.example")

    assert result == {
        "base_url": "https://ROTATING-HOST.example",
        "status": "retryable",
        "evidence": "CDP_TIMEOUT:Page.enable",
    }
    assert closed == [(9240, "target-1")]


def test_probe_route_accepts_host_specific_automatic_cloudflare(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = {"id": "target-1"}
    closed: list[tuple[int, str]] = []
    monkeypatch.setattr(rotation, "new_target", lambda _port: target)

    class ChallengePage:
        def __init__(self, _port: int, _target: dict[str, str]) -> None:
            pass

        def navigate(self, url: str) -> dict[str, str]:
            raise RetryableCloudflareChallenge(
                f"CLOUDFLARE_AUTO_CHALLENGE_RETRYABLE:{url}"
            )

        def close(self) -> None:
            pass

    monkeypatch.setattr(rotation, "CdpPage", ChallengePage)
    monkeypatch.setattr(
        rotation,
        "close_target",
        lambda port, target_id: closed.append((port, target_id)),
    )

    result = rotation.probe_route(9240, "https://ROTATING-HOST.example")

    assert result == {
        "base_url": "https://ROTATING-HOST.example",
        "status": "cloudflare",
        "evidence": "CLOUDFLARE_AUTO_CHALLENGE_RETRYABLE:https://ROTATING-HOST.example/",
    }
    assert closed == [(9240, "target-1")]


def test_rotation_rewrites_active_state_atomically_and_clears_stale_route_error(
    tmp_path: Path,
) -> None:
    config_path = _make_lane(tmp_path)

    def fake_probe(port: int, base_url: str) -> dict[str, str]:
        assert port == 9240
        status = "unavailable" if "29.com" in base_url else "cloudflare"
        return {"base_url": base_url, "status": status, "evidence": status}

    receipt = rotation.migrate(
        config_path,
        expected_suffix=29,
        target_suffix=30,
        probe=fake_probe,
        pause=lambda _: None,
    )

    config = json.loads(config_path.read_text(encoding="utf-8"))
    catalog = json.loads((tmp_path / "CATALOG.json").read_text(encoding="utf-8"))
    state = json.loads((tmp_path / "SCRAPE_STATE.json").read_text(encoding="utf-8"))
    active_bytes = b"".join(
        (tmp_path / name).read_bytes()
        for name in ("multitab_config.json", "CATALOG.json", "source_progress.json", "PRIORITY.jsonl", "SCRAPE_STATE.json")
    )
    package = tmp_path / "distributed" / "bookto29-newto29-oldmac-smoke-g1"
    new_manifest = json.loads((package / "NEWMAC_ASSIGNMENT.json").read_text())
    old_manifest = json.loads((package / "OLDMAC_ASSIGNMENT.json").read_text())
    pair = json.loads((package / "PAIR_VALIDATION.json").read_text())
    oldmac_config = json.loads((package / "OLDMAC_multitab_config.json").read_text())

    assert receipt["status"] == "COMMITTED"
    assert receipt["old_suffix"] == 29
    assert receipt["new_suffix"] == 30
    assert config["base_urls"] == {
        "bookto": "https://ROTATING-HOST.example",
        "newto": "https://ROTATING-HOST.example",
    }
    assert config["background_only"] is True
    assert config["workers"] == 4
    assert b"bookto29.com" not in active_bytes
    assert b"newto29.com" not in active_bytes
    assert state["items"]["bookto_novel:1"]["status"] == "PENDING_ROUTE_REFRESH"
    assert "SITE_ROUTE_UNAVAILABLE" not in state["items"]["bookto_novel:1"].get("error", "")
    assert state["catalog_sha256"] == hashlib.sha256(
        json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    assert Path(receipt["backup_dir"]).is_dir()
    assert new_manifest["catalog_sha256"] == hashlib.sha256(
        (tmp_path / "CATALOG.json").read_bytes()
    ).hexdigest()
    assert pair["newmac_manifest_sha256"] == hashlib.sha256(
        (package / "NEWMAC_ASSIGNMENT.json").read_bytes()
    ).hexdigest()
    assert pair["oldmac_manifest_sha256"] == hashlib.sha256(
        (package / "OLDMAC_ASSIGNMENT.json").read_bytes()
    ).hexdigest()
    assert new_manifest["entries"][0]["url"].startswith("https://ROTATING-HOST.example/")
    assert old_manifest["entries"][0]["url"].startswith("https://ROTATING-HOST.example/")
    assert oldmac_config["domain_suffix"] == 30
    assert oldmac_config["base_urls"] == config["base_urls"]
