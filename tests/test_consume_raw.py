import json
from spacei.consume_raw import decode_event


def test_decode_event_from_json_bytes():
    expected = {
        "event_id": "test-id",
        "event_type": "tle.observed",
        "source": "celestrak",
        "schema_version": 1,
        "observed_at": "2026-05-09T19:00:00Z",
        "ingested_at": "2026-05-10T18:39:49Z",
        "payload": {"norad_id": "25544"},
    }

    encoded = json.dumps(expected).encode("utf-8")

    assert decode_event(encoded) == expected
