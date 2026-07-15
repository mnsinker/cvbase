from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class AnnotationRule:
    key: str
    parser: Callable[..., Any]
