from dataclasses import dataclass, field
from compiler.entities.document_nodes import DocumentNode
from compiler.entities.inline_nodes import InlineNode


@dataclass
class ParsedNode:
    line_no: int
    indent: int

    document_node: DocumentNode
