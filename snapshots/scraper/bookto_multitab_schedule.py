"""Scheduling policy for the Bookto/Newtoki scrape lane."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Final


IMAGE_ROUTE_PROBE_INTERVAL: Final = timedelta(minutes=5)


def image_route_probe_is_due(
    updated_at: str,
    current_time: datetime | None = None,
) -> bool:
    """Return whether the one external-image probe may run again."""
    try:
        previous_time = datetime.fromisoformat(updated_at)
    except ValueError:
        return True
    observed_time = current_time or datetime.now().astimezone()
    if previous_time.tzinfo is None or observed_time.tzinfo is None:
        return True
    return observed_time - previous_time >= IMAGE_ROUTE_PROBE_INTERVAL
