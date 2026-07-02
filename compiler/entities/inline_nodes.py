from dataclasses import field, dataclass
from typing import Union

"""
InlineNode
    * It represents textual structure.

    * Parent: DocumentNode or InlineNode. 
    * Children: InlineNode only, if allowed to have children.
"""

type InlineNode = Union[Text, Strong, Italic, Strike, Underline, Image, Link, InlineMath, InlineCode]


# -------------------------------------------------------

@dataclass
class Text:
    content: str = ""

@dataclass
class Strong:
    inline_children: list[InlineNode] = field(default_factory=list)

@dataclass
class Italic:
    inline_children: list[InlineNode] = field(default_factory=list)

@dataclass
class Strike:
    inline_children: list[InlineNode] = field(default_factory=list)

@dataclass
class Underline:
    inline_children: list[InlineNode] = field(default_factory=list)

@dataclass
class InlineMath:
    content: str = ""

@dataclass
class InlineCode:
    content: str = ""

@dataclass
class Link:
    url: str = ""
    title: str = ""
    inline_children: list[InlineNode] = field(default_factory=list)

@dataclass
class Image:
    alt: str = ""
    src: str = ""
    title: str = ""

