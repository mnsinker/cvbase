import re
from dataclasses import dataclass, field
from typing import Pattern, Callable, Any
from compiler.entities.doc_nodes import DocNode, ALL_DOC_NODES
from compiler.entities.inline_nodes import InlineNode, ALL_INLINE_NODES
from compiler.entities.parsed_line import ParsedLine


@dataclass
class DocNodeRule:
    # ---------- Grammar ----------
    node_type: type[DocNode]
    opening_patterns: list[Pattern] = field(default_factory=list)
    closing_patterns: list[Pattern] = field(default_factory=list)
    predicates: list[Callable[[ParsedLine], bool]] = field(default_factory=list)
    order: int = 0

    # ---------- Construction ----------
    attribute_extractors: dict[str, Callable[[re.Match],Any]] = field(default_factory=dict) # extract fields from the opening line
    inline_content: Callable[[re.Match], Any] | None = None

    # ---------- Runtime ----------
    stateful_append: Callable[..., None] | None = None  # None = stateless
    allow_inline: bool = False

    # ---------- Hierarchy ----------
    excluded_doc_children: set[type[DocNode]] = field(default_factory=lambda: set(ALL_DOC_NODES))

    @property
    def allowed_doc_children(self) -> set[type[DocNode]]:
        return ALL_DOC_NODES - self.excluded_doc_children # default = not allowed

# ===========================================================================

@dataclass
class InlineNodeRule:
    # ---------- Grammar ----------
    node_type: type[InlineNode]
    opening: str
    closing: str
    middle: str | None = None

    # ---------- Construction ----------
    attribute_extractors: dict[str, Callable[...,Any]] = field(default_factory=dict)

    # ---------- Hierarchy ----------
    excluded_inline_children: set[type[InlineNode]] = field(default_factory=lambda: set(ALL_INLINE_NODES))

    @property
    def allowed_inline_children(self) -> set[type[DocNode]]: # allowed_inline_children
        return ALL_INLINE_NODES - self.excluded_inline_children  # default = not allowed

