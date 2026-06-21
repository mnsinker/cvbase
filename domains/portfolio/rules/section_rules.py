from compiler.entities.mapping_rule import MappingRule
from compiler.entities.unified_ast import UnifiedAST
from domains.portfolio.domain.entities import PortfolioField


PORTFOLIO_MAPPING_RULES = (
    MappingRule(unified_ast=UnifiedAST.H1, domain_field=PortfolioField.SECTION),
    MappingRule(unified_ast=UnifiedAST.H2, domain_field=PortfolioField.SUBSECTION),
)