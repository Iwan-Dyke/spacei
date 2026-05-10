import os
from typing import Any
from datetime import UTC, datetime
from confluent_kafka import Producer
from spacei.events import build_event
from spacei.produce_sample import TOPIC, encode_event
from spacei.celestrak import fetch_celestrak_tles, parse_tle_records


def build_tle_observed_event(
    record: dict[str, Any],
    *,
    observed_at: str,
) -> dict[str, Any]:
    return build_event(
        event_id=f"celestrak:tle:{record['norad_id']}:{observed_at}",
        event_type="tle.observed",
        source="celestrak",
        observed_at=observed_at,
        payload=record,
    )

def current_observed_at() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def main() -> None:
    observed_at = current_observed_at()
    records = parse_tle_records(fetch_celestrak_tles())

    producer = Producer(
        {
            "bootstrap.servers": os.getenv(
                "SPACEI_KAFKA_BOOTSTRAP_SERVERS",
                "localhost:9092",
            )
        }
    )

    for record in records:
        event = build_tle_observed_event(record, observed_at=observed_at)
        producer.produce(
            TOPIC, 
            key=record["norad_id"],
            value=encode_event(event),
        )

    producer.flush()
    print(f"published {len(records)} CelesTrak TLE records to {TOPIC}")

if __name__ == "__main__":
    main()
