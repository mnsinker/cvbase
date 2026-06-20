from products.compiler.entities.mapping_rule import MappingRule
from products.compiler.entities.unified_ast import UnifiedAST
from products.portfolio.domain.entities import PortfolioField


PORTFOLIO_MAPPING_RULES = (
    MappingRule(unified_ast=UnifiedAST.H1, domain_field=PortfolioField.SECTION),
    MappingRule(unified_ast=UnifiedAST.H2, domain_field=PortfolioField.SUBSECTION),
)