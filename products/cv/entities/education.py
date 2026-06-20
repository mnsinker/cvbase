from dataclasses import dataclass


@dataclass
class Education:
    school: str
    degree: str
    start_date: str
    end_date: str
    bullets: list[str]