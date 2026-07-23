from typing import Any
from dataclasses import field, dataclass, is_dataclass, fields

"""
InlineNode
    * It represents textual structure.

    * Parent: DocumentNode or InlineNode. 
    * Children: InlineNode only, if allowed to have children.
"""

@dataclass
class InlineNode:
    inline_children: list["InlineNode"] = field(default_factory=list)
    def to_dict(self) -> dict:
        result = {"type": self.__class__.__name__}
        for f in fields(self):
            values = getattr(self, f.name)
            result[f.name] = self._serialize(values)
        return result
    @staticmethod
    def _serialize(values) -> Any:
        if isinstance(values, list):
            return [InlineNode._serialize(v) for v in values]
        if hasattr(values, "to_dict"):
            return values.to_dict()
        return values

# -------------------------------------------------------

@dataclass
class Text(InlineNode):
    content: str = ""

@dataclass
class Strong(InlineNode):
    pass

@dataclass
class Italic(InlineNode):
    pass

@dataclass
class Strike(InlineNode):
    pass

@dataclass
class Underline(InlineNode):
    pass

@dataclass
class InlineMath(InlineNode):
    pass

@dataclass
class InlineCode(InlineNode):
    pass

@dataclass
class Link(InlineNode):
    url: str = ""

@dataclass
class Image(InlineNode):
    src: str = ""

ALL_INLINE_NODES = {Text, Strong, Italic, Strike, Underline, Image, Link, InlineMath, InlineCode}
