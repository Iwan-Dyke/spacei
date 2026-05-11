import os
import json
from typing import Any
from spacei.events import build_event
from confluent_kafka import Consumer, KafkaError, KafkaException, Producer


RAW_TOPIC = "space.raw.celestrak.tle"
NORMALIZED_TOPIC = "space.normalized.orbital_elements"
DEADLETTER_TOPIC = "space.deadletter"


def build_consumer() -> Consumer:
    return Consumer(build_consumer_config())


def build_producer() -> Producer:
    return Producer(build_producer_config())


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

def build_deadletter_event(raw_value: bytes, error: Exception) -> dict[str, Any]:
    return build_event(
        event_id="deadletter:spacei.normalizer.tle",
        event_type="message.deadlettered",
        source="spacei.normalizer.tle",
        observed_at="",
        payload={
            "raw_value": raw_value.decode("utf-8", errors="replace"),
            "error_type": type(error).__name__,
            "error_message": str(error),
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

def process_raw_message_or_deadletter(value: bytes) -> tuple[str, str, bytes]:
    try:
        key, normalized_value = process_raw_message(value)
        return NORMALIZED_TOPIC, key, normalized_value
    except Exception as error:
        event = build_deadletter_event(value, error)
        return DEADLETTER_TOPIC, "spacei.normalizer.tle", encode_event(event)

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

def run_normalizer() -> None:
    consumer = build_consumer()
    producer = build_producer()
    consumer.subscribe([RAW_TOPIC])

    try:
        while True:
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise KafkaException(message.error())

            topic, key, value = process_raw_message_or_deadletter(message.value())
            producer.produce(topic, key=key, value=value)
            producer.poll(0)
    finally:
        producer.flush()
        consumer.close()

def main() -> None:
    run_normalizer()

if __name__ == "__main__":
    main()
