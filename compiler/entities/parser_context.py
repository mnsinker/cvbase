from dataclasses import dataclass
from compiler.entities.pending_node import PendingNode


@dataclass
class ParserContext:
    raw: str
    line_no: int
    pending_node: PendingNode | None = None