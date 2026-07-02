from dataclasses import dataclass, field
from typing import Union
from compiler.entities.inline_nodes import InlineNode

"""
DocumentNode
    * It represents document structure. 
    * it participates in the document hierarchy.

    * InlineNode: some can, some cannot have InlineNodes.
    * Children: some can, some cannot have ChildrenNodes.
"""

type DocumentNode = Union["Document", "FrontMatter", "HorizontalRule", "Heading", "Paragraph", "ListItem", "CodeBlock", "QuoteBlock", "MathBlock", "Table", "Row", "Cell"]


@dataclass
class Document:
    document_children: list[DocumentNode] = field(default_factory=list)

@dataclass
class FrontMatter:
    content: dict = field(default_factory=dict)

@dataclass
class HorizontalRule:
    pass

@dataclass
class Heading:
    level: int = 1
    inline_children: list[InlineNode] = field(default_factory=list)
    document_children: list["DocumentNode"] = field(default_factory=list)

@dataclass
class Paragraph:
    inline_children: list[InlineNode] = field(default_factory=list)

@dataclass
class ListItem:
    label: str = ""
    inline_children: list[InlineNode] = field(default_factory=list)
    document_children: list["DocumentNode"] = field(default_factory=list)

@dataclass
class QuoteBlock:
    document_children: list["DocumentNode"] = field(default_factory=list)

@dataclass
class CodeBlock:
    language: str
    content: str = ""

@dataclass
class MathBlock:
    content: str = ""

@dataclass
class Table:
    document_children: list["DocumentNode"] = field(default_factory=list)

@dataclass
class Row:
    document_children: list["DocumentNode"] = field(default_factory=list)

@dataclass
class Cell:
    document_children: list["DocumentNode"] = field(default_factory=list)