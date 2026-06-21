from dataclasses import dataclass


@dataclass
class Experience:
    company: str
    role: str
    start_date: str
    end_date: str
    bullets: list[str]
