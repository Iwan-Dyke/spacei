import os
import json
from typing import Any
from spacei.events import build_event


RAW_TOPIC = "space.raw.celestrak.tle"
NORMALIZED_TOPIC = "space.normalized.orbital_elements"
DEADLETTER_TOPIC = "space.deadletter"

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

def normalize_raw_tle_event(raw_event: dict[str, Any]) -> dict[str, Any]:
    return build_orbital_elements_event(raw_event)

def decode_event(value: bytes) -> dict[str, Any]:
    return json.loads(value.decode("utf-8"))

def encode_event(event: dict[str, Any]) -> bytes:
    return json.dumps(event).encode("utf-8")

def process_raw_message(value: bytes) -> tuple[str, bytes]:
    raw_event = decode_event(value)
    event = normalize_raw_tle_event(raw_event)
    return event["payload"]["norad_id"], encode_event(event)

def build_consumer_config() -> dict[str, str]:
    return {
        "bootstrap.servers": os.getenv(
            "SPACEI_KAFKA_BOOTSTRAP_SERVERS",
            "localhost:9092",
        ),
        "group.id": os.getenv(
            "SPACEI_KAFKA_CONSUMER_GROUP",
            "spacei.normalizer.tle",
        ),
        "auto.offset.reset": "earliest",
    }

def build_producer_config() -> dict[str, str]:
    return {
        "bootstrap.servers": os.getenv(
            "SPACEI_KAFKA_BOOTSTRAP_SERVERS",
            "localhost:9092",
        ),
    }
