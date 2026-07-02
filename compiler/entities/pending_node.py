from dataclasses import dataclass, field
from compiler.entities.document_nodes import DocumentNode


@dataclass
class PendingNode:
    start_line_no: int
    indent: int
    document_node: DocumentNode
    lines: list[str] = field(default_factory=list)
    expected_columns: int = 0
