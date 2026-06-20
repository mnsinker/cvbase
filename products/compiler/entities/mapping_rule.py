from dataclasses import dataclass
from products.compiler.entities.unified_ast import UnifiedAST


@dataclass
class MappingRule:
    unified_ast: UnifiedAST
    domain_field: str    # DSL (domain specific language)