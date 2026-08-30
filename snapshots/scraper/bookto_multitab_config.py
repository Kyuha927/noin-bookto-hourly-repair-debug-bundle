"""Validated runtime configuration for the background multi-tab lane."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from bookto_multitab_catalog import BOARD_SPECS
from bookto_multitab_state import read_json


class ScrapeError(RuntimeError):
    """The lane cannot safely continue with the current item or configuration."""


def load_config(path: Path) -> dict[str, Any]:
    config = read_json(path, {})
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ScrapeError("MULTITAB_CONFIG_INVALID")
    if config.get("tabs") != [spec["tab"] for spec in BOARD_SPECS]:
        raise ScrapeError("MULTITAB_TAB_SCOPE_INVALID")
    base_urls = config.get("base_urls")
    if not isinstance(base_urls, dict):
        raise ScrapeError("MULTITAB_BASE_URLS_INVALID")
    bookto = re.fullmatch(r"https://bookto([0-9]+)[.]com", str(base_urls.get("bookto", "")))
    newto = re.fullmatch(r"https://newto([0-9]+)[.]com", str(base_urls.get("newto", "")))
    if not bookto or not newto or bookto.group(1) != newto.group(1):
        raise ScrapeError("MULTITAB_DOMAIN_SUFFIX_MISMATCH")
    if config.get("background_only") is not True:
        raise ScrapeError("MULTITAB_BACKGROUND_ONLY_REQUIRED")
    return config
