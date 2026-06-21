from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    phone: str
    email: str
    location: str
    desired_position: str = ""
