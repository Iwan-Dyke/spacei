from spacei.normalise_tle import build_orbital_elements_event


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
    assert event["source"] == "spacei.normaliser.tle"
    assert event["observed_at"] == "2026-05-10T19:54:16Z"
    assert event["payload"] == {
        "norad_id": "25544",
        "name": "ISS (ZARYA)",
        "epoch": "26130.45717135",
        "line1": raw_event["payload"]["line1"],
        "line2": raw_event["payload"]["line2"],
        "source_event_id": raw_event["event_id"],
    }
