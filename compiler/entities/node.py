from dataclasses import dataclass, field

from compiler.entities.unified_ast import UnifiedAST


@dataclass
class Node:
    ast_type: UnifiedAST

    semantic_type: str | None = None
    tags: list[str] = field(default_factory=list)

    content: str = ""
    children: list["Node"] = field(default_factory=list)
