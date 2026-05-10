import json
from typing import Any


def decode_event(value: bytes) -> dict[str, Any]:
    return json.loads(value.decode("utf-8"))
