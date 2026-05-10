from spacei.events import build_event


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
