from dataclasses import dataclass
from compiler.entities.value_format import ValueFormat

@dataclass
class AnnotationConfig:
    key: str
    value_format: ValueFormat




