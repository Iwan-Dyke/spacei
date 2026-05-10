from spacei.ingest_celestrak import build_tle_observed_event


def test_build_tle_observed_event_from_record():
    record = {
        "name": "ISS (ZARYA)",
        "norad_id": "25544",
        "line1": "1 25544U 98067A   26130.45717135  .00006413  00000+0  12369-3 0  9992",
        "line2": "2 25544  51.6310 126.8685 0007459  43.7479 316.4100 15.49173700565900",
    }

    event = build_tle_observed_event(
        record,
        observed_at="2026-05-10T20:33:00Z",
    )

    assert event["event_id"] == "celestrak:tle:25544:2026-05-10T20:33:00Z"
    assert event["event_type"] == "tle.observed"
    assert event["source"] == "celestrak"
    assert event["schema_version"] == 1
    assert event["observed_at"] == "2026-05-10T20:33:00Z"
    assert "ingested_at" in event
    assert event["payload"] == record
