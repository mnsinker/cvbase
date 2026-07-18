from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    phone: str
    email: str
    location: str

    portfolio: str
    github: str

    desired_position: str = ""
