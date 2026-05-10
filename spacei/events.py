from datetime import UTC, datetime
from typing import Any


def build_event(
    *,
    event_id: str,
    event_type: str,
    source: str,
    observed_at: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "source": source,
        "schema_version": 1,
        "observed_at": observed_at,
        "ingested_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "payload": payload,
    }
