from dataclasses import dataclass


@dataclass
class Summary:
    intro: str
    built_systems: list[str]
    previous_systems: list[str]
    technical_skills: str
    certifications: str