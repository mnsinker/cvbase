from typing import Any
from dataclasses import dataclass, field, is_dataclass, fields
from compiler.entities.annotation import Annotation
from compiler.entities.inline_nodes import InlineNode
"""
DocumentNode
    * It represents document structure. 
    * it participates in the document hierarchy.

    * InlineNode: some can, some cannot have InlineNodes.
    * Children: some can, some cannot have ChildrenNodes.
"""

@dataclass
class DocNode:
    annotations: list[Annotation] = field(default_factory=list)
    inline_children: list[InlineNode] = field(default_factory=list)
    doc_children: list["DocNode"] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = {"type": self.__class__.__name__}
        for f in fields(self):
            values = getattr(self, f.name)
            result[f.name] = self._serialize(values)
        return result

    @staticmethod
    def _serialize(values) -> Any:
        if isinstance(values, list):
            return [DocNode._serialize(v) for v in values]
        if hasattr(values, "to_dict"):
            return values.to_dict()
        return values

# -----------------------------------------------------------------

@dataclass
class Document(DocNode):
    pass # inline_children not allowed

@dataclass
class FrontMatter(DocNode): # no inheritance
    content: list[str] = field(default_factory=list)

@dataclass
class HorizontalRule(DocNode):
    pass # annotation, inline_children, document_children are not allowed

@dataclass
class Heading(DocNode):
    level: int = 1

@dataclass
class Paragraph(DocNode):
    pass

@dataclass
class ListItem(DocNode):
    label: str = ""

@dataclass
class QuoteBlock(DocNode):
    pass # inline_children not allowed

@dataclass
class CodeBlock(DocNode):
    language: str = ""
    content: list[str] = field(default_factory=list)
    # inline_children, document_children are not allowed

@dataclass
class MathBlock(DocNode):
    content: list[str] = field(default_factory=list)
    # inline_children, document_children are not allowed

@dataclass
class Table: # todo
    doc_children: list["DocNode"] = field(default_factory=list)

@dataclass
class Row:
    doc_children: list["DocNode"] = field(default_factory=list)

@dataclass
class Cell:
    doc_children: list["DocNode"] = field(default_factory=list)

ALL_DOC_NODES = {Document, FrontMatter, Heading, Paragraph, ListItem, QuoteBlock, CodeBlock, MathBlock, Table, Row, Cell, HorizontalRule}
