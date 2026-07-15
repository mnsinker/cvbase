from dataclasses import dataclass
from compiler.entities.doc_nodes import DocNode


@dataclass
class ParsedNode:
    line_no: int
    indent: int

    doc_node: DocNode
