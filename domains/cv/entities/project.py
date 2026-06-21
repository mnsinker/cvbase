from dataclasses import dataclass

@dataclass
class Project:
    name: str
    label: str
    bullets: list[str]