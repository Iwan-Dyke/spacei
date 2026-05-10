from typing import Any

from spacei.events import build_event


def build_orbital_elements_event(raw_event: dict[str, Any]) -> dict[str, Any]:
    payload = raw_event["payload"]
    observed_at = raw_event["observed_at"]

    return build_event(
        event_id=f"orbital-elements:{payload['norad_id']}:{observed_at}",
        event_type="orbital_elements.updated",
        source="spacei.normalizer.tle",
        observed_at=observed_at,
        payload={
            "norad_id": payload["norad_id"],
            "name": payload["name"],
            "epoch": payload["line1"][18:32].strip(),
            "line1": payload["line1"],
            "line2": payload["line2"],
            "source_event_id": raw_event["event_id"],
        },
    )
