from dataclasses import dataclass, field

class CVInlineNode:
    """ Base class for inline content representation. """
    pass

@dataclass
class TextNode(CVInlineNode):
    text: str

@dataclass
class StrongNode(CVInlineNode):
    inline_children: list[CVInlineNode] = field(default_factory=list)

@dataclass
class ItalicNode(CVInlineNode):
    inline_children: list[CVInlineNode] = field(default_factory=list)

@dataclass
class LinkNode(CVInlineNode):
    title: str
    url: str

# --------------------------------------

@dataclass
class RichText:
    nodes: list[CVInlineNode] = field(default_factory=list)