import os
import json
from typing import Any
from confluent_kafka import Consumer, KafkaError, KafkaException


TOPIC = "space.raw.celestrak.tle"


def decode_event(value: bytes) -> dict[str, Any]:
    return json.loads(value.decode("utf-8"))


def build_consumer() -> Consumer:
    return Consumer(
        {
            "bootstrap.servers": os.getenv(
                "SPACEI_KAFKA_BOOTSTRAP_SERVERS",
                "localhost:9092",
            ),
            "group.id": os.getenv(
                "SPACEI_KAFKA_CONSUMER_GROUP",
                "spacei.raw.debug",
            ),
            "auto.offset.reset": "earliest",
        }
    )

def consume_one() -> dict:
    consumer = build_consumer()
    consumer.subscribe([TOPIC])

    try:
        while True:
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise KafkaException(message.error())

            return decode_event(message.value())
    finally:
        consumer.close()


def main() -> None:
    event = consume_one()
    print(event)


if __name__ == "__main__":
    main()
