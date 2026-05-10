import json

from spacei.events import build_event
from spacei.produce_sample import TOPIC, build_sample_tle_event, encode_event


def test_build_event_envelope_has_required_fields():
    event = build_event(
        event_id="celestrak:tle:25544:2026-05-09T19:00:00Z",
        event_type="tle.observed",
        source="celestrak",
        observed_at="2026-05-09T19:00:00Z",
        payload={"norad_id": "25544"},
    )

    assert event["event_id"] == "celestrak:tle:25544:2026-05-09T19:00:00Z"
    assert event["event_type"] == "tle.observed"
    assert event["source"] == "celestrak"
    assert event["schema_version"] == 1
    assert event["observed_at"] == "2026-05-09T19:00:00Z"
    assert "ingested_at" in event
    assert event["payload"] == {"norad_id": "25544"}


def test_build_sample_tle_event_targets_raw_tle_topic():
    event = build_sample_tle_event()

    assert TOPIC == "space.raw.celestrak.tle"
    assert event["event_type"] == "tle.observed"
    assert event["source"] == "celestrak"
    assert event["payload"]["norad_id"] == "25544"


def test_encode_event_as_json_bytes():
    event = build_sample_tle_event()

    encoded = encode_event(event)

    assert isinstance(encoded, bytes)
    assert json.loads(encoded.decode("utf-8")) == event
