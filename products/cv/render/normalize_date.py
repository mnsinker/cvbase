from __future__ import annotations
import re


def normalize_date(value: str) -> tuple[int, int]:

    value = value.strip()
    match = re.fullmatch(r"(\d{4})[-./](\d{2})", value)

    if not match:
        raise ValueError(f"Invalid date: {value}")

    return int(match.group(1)), int(match.group(2))
