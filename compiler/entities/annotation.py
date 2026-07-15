from dataclasses import dataclass
from typing import Any


@dataclass
class Annotation:
    key: str
    values: Any

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "values": self.values,
        }