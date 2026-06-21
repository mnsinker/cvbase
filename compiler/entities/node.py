from dataclasses import dataclass, field

from compiler.entities.unified_ast import UnifiedAST


@dataclass
class Node:
    type: UnifiedAST
    content: str = ""
    children: list[Node] = field(default_factory=list)
