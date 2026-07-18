from dataclasses import dataclass, field


@dataclass
class Project:
    name: str
    label: str
    links: list[dict[str, str]] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)