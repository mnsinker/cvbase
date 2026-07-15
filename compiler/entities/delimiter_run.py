from dataclasses import dataclass


@dataclass(slots=True)
class DelimiterRun:
    delimiter: str
    count: int
    start: int