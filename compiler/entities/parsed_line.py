from dataclasses import dataclass
from compiler.entities.unified_ast import UnifiedAST


@dataclass
class ParsedLine:
    line_no: int
    raw: str

    ast_type: UnifiedAST
    content: str
    indent: int