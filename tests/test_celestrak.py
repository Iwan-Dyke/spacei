from spacei.celestrak import parse_tle_records


def test_parse_tle_records_from_three_line_text():
    text = """ISS (ZARYA)
1 25544U 98067A   26129.50000000  .00016717  00000+0  10270-3 0  9993
2 25544  51.6396 160.4574 0003907  74.2199  44.4838 15.50000000400000
"""

    records = parse_tle_records(text)

    assert records == [
        {
            "name": "ISS (ZARYA)",
            "norad_id": "25544",
            "line1": "1 25544U 98067A   26129.50000000  .00016717  00000+0  10270-3 0  9993",
            "line2": "2 25544  51.6396 160.4574 0003907  74.2199  44.4838 15.50000000400000",
        }
    ]

def test_parse_multiple_tle_records():
    text = """ISS (ZARYA)
1 25544U 98067A   26129.50000000  .00016717  00000+0  10270-3 0  9993
2 25544  51.6396 160.4574 0003907  74.2199  44.4838 15.50000000400000
CSS (TIANHE)
1 48274U 21035A   26129.50000000  .00010000  00000+0  10000-3 0  9991
2 48274  41.4700 120.0000 0004000  80.0000  40.0000 15.60000000200000
"""

    records = parse_tle_records(text)

    assert [record["norad_id"] for record in records] == ["25544", "48274"]

