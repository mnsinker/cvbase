from dataclasses import dataclass, field
from enum import Enum

from compiler.entities.node import Node



@dataclass
class Metadata:
    career_spine: list[str] = field(default_factory=list)
    advanced_themes: list[str] = field(default_factory=list)
    excluded_visibility: bool = False

@dataclass
class Subsection:
    title: str
    metadata: Metadata = field(default_factory=Metadata)
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Section:
    title: str
    subsection: list[Subsection] = field(default_factory=Subsection)
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Portfolio:
    sections: list[Section] = field(default_factory=list)



class PortfolioField(str, Enum):
    SECTION = "section"
    SUBSECTION = "subsection"


