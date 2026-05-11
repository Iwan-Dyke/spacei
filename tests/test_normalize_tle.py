from spacei.normalize_tle import (
    DEADLETTER_TOPIC,
    NORMALIZED_TOPIC,
    RAW_TOPIC,
    build_orbital_elements_event,
    decode_event,
    encode_event,
    normalize_raw_tle_event,
    process_raw_message,
    build_consumer_config,
    build_producer_config,
)

def test_build_orbital_elements_event_from_tle_observed_event():
    raw_event = {
        "event_id": "celestrak:tle:25544:2026-05-10T19:54:16Z",
        "event_type": "tle.observed",
        "source": "celestrak",
        "schema_version": 1,
        "observed_at": "2026-05-10T19:54:16Z",
        "ingested_at": "2026-05-10T19:54:17Z",
        "payload": {
            "name": "ISS (ZARYA)",
            "norad_id": "25544",
            "line1": "1 25544U 98067A   26130.45717135  .00006413  00000+0  12369-3 0  9992",
            "line2": "2 25544  51.6310 126.8685 0007459  43.7479 316.4100 15.49173700565900",
        },
    }

    event = build_orbital_elements_event(raw_event)

    assert event["event_id"] == "orbital-elements:25544:2026-05-10T19:54:16Z"
    assert event["event_type"] == "orbital_elements.updated"
    assert event["source"] == "spacei.normalizer.tle"
    assert event["observed_at"] == "2026-05-10T19:54:16Z"
    assert event["payload"] == {
        "norad_id": "25544",
        "name": "ISS (ZARYA)",
        "epoch": "26130.45717135",
        "line1": raw_event["payload"]["line1"],
        "line2": raw_event["payload"]["line2"],
        "source_event_id": raw_event["event_id"],
    }

def test_normalizer_topics_match_design_decisions():
    assert RAW_TOPIC == "space.raw.celestrak.tle"
    assert NORMALIZED_TOPIC == "space.normalized.orbital_elements"
    assert DEADLETTER_TOPIC == "space.deadletter"


def test_normalize_raw_tle_event_returns_orbital_elements_event():
    raw_event = {
        "event_id": "celestrak:tle:25544:2026-05-10T19:54:16Z",
        "event_type": "tle.observed",
        "source": "celestrak",
        "schema_version": 1,
        "observed_at": "2026-05-10T19:54:16Z",
        "ingested_at": "2026-05-10T19:54:17Z",
        "payload": {
            "name": "ISS (ZARYA)",
            "norad_id": "25544",
            "line1": "1 25544U 98067A   26130.45717135  .00006413  00000+0  12369-3 0  9992",
            "line2": "2 25544  51.6310 126.8685 0007459  43.7479 316.4100 15.49173700565900",
        },
    }

    event = normalize_raw_tle_event(raw_event)

    assert event["event_type"] == "orbital_elements.updated"
    assert event["source"] == "spacei.normalizer.tle"
    assert event["payload"]["source_event_id"] == raw_event["event_id"]


def test_normalizer_codec_round_trips_event():
    event = {
        "event_id": "orbital-elements:25544:2026-05-10T19:54:16Z",
        "event_type": "orbital_elements.updated",
        "source": "spacei.normalizer.tle",
        "schema_version": 1,
        "observed_at": "2026-05-10T19:54:16Z",
        "ingested_at": "2026-05-10T19:54:17Z",
        "payload": {"norad_id": "25544"},
    }

    encoded = encode_event(event)

    assert isinstance(encoded, bytes)
    assert decode_event(encoded) == event


def test_process_raw_message_returns_key_and_encoded_normalized_event():
    raw_event = {
        "event_id": "celestrak:tle:25544:2026-05-10T19:54:16Z",
        "event_type": "tle.observed",
        "source": "celestrak",
        "schema_version": 1,
        "observed_at": "2026-05-10T19:54:16Z",
        "ingested_at": "2026-05-10T19:54:17Z",
        "payload": {
            "name": "ISS (ZARYA)",
            "norad_id": "25544",
            "line1": "1 25544U 98067A   26130.45717135  .00006413  00000+0  12369-3 0  9992",
            "line2": "2 25544  51.6310 126.8685 0007459  43.7479 316.4100 15.49173700565900",
        },
    }

    key, value = process_raw_message(encode_event(raw_event))

    event = decode_event(value)

    assert key == "25544"
    assert event["event_type"] == "orbital_elements.updated"
    assert event["payload"]["norad_id"] == "25544"

def test_build_consumer_config_uses_local_defaults(monkeypatch):
    monkeypatch.delenv("SPACEI_KAFKA_BOOTSTRAP_SERVERS", raising=False)
    monkeypatch.delenv("SPACEI_KAFKA_CONSUMER_GROUP", raising=False)

    config = build_consumer_config()

    assert config == {
        "bootstrap.servers": "localhost:9092",
        "group.id": "spacei.normalizer.tle",
        "auto.offset.reset": "earliest",
    }

def test_build_producer_config_uses_local_defaults(monkeypatch):
    monkeypatch.delenv("SPACEI_KAFKA_BOOTSTRAP_SERVERS", raising=False)

    config = build_producer_config()

    assert config == {
        "bootstrap.servers": "localhost:9092"
    }
