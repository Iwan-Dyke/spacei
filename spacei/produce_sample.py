import json
import os
from typing import Any

from confluent_kafka import Producer

from spacei.events import build_event


TOPIC = "space.raw.celestrak.tle"


def build_sample_tle_event() -> dict[str, Any]:
    return build_event(
        event_id="celestrak:tle:25544:2026-05-09T19:00:00Z",
        event_type="tle.observed",
        source="celestrak",
        observed_at="2026-05-09T19:00:00Z",
        payload={
            "norad_id": "25544",
            "name": "ISS (ZARYA)",
            "line1": "1 25544U 98067A   26129.50000000  .00016717  00000+0  10270-3 0  9993",
            "line2": "2 25544  51.6396 160.4574 0003907  74.2199  44.4838 15.50000000400000",
        },
    )


def encode_event(event: dict[str, Any]) -> bytes:
    return json.dumps(event).encode("utf-8")


def main() -> None:
    producer = Producer(
        {
            "bootstrap.servers": os.getenv(
                "SPACEI_KAFKA_BOOTSTRAP_SERVERS",
                "localhost:9092",
            )
        }
    )

    event = build_sample_tle_event()

    producer.produce(
        TOPIC,
        key=event["payload"]["norad_id"],
        value=encode_event(event),
    )
    producer.flush()

    print(f"published {event['event_id']} to {TOPIC}")


if __name__ == "__main__":
    main()
