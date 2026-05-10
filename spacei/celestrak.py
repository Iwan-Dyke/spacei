from typing import Any


def parse_tle_records(text: str) -> list[dict[str, Any]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    records = []

    for index in range(0, len(lines), 3):
        name = lines[index]
        line1 = lines[index + 1]
        line2 = lines[index + 2]

        records.append(
                {
                    "name": name,
                    "norad_id": line1[2:7],
                    "line1": line1,
                    "line2": line2,
                }
            )

    return records
