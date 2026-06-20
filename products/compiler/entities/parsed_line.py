from dataclasses import dataclass
from products.compiler.entities.unified_ast import UnifiedAST


@dataclass
class ParsedLine:
    unified_ast: UnifiedAST
    data: str
    indent: int