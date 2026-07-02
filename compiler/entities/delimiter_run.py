from dataclasses import dataclass


@dataclass
class DelimiterRun:
    delimiter: str
    count: int