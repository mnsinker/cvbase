from compiler.transforms.annotate_semantic_types import annotate_semantic_types
from compiler.engine.build_node_tree import build_node_tree
from compiler.engine.parse_lines import parse_lines
from domains.portfolio.semantic_registry import PORTFOLIO_SEMANTIC_REGISTRY


def test_annotate_semantic_types():
    md = """
Career Spine: 
    information-modeling, workflow
Advanced Themes: 
    automation, ai-systems
Excluded Themes: 
    true
"""

    roots = build_node_tree(parse_lines(md))
    annotate_semantic_types(roots, PORTFOLIO_SEMANTIC_REGISTRY)

    assert roots[0].semantic_type == "career_spine"
    assert roots[1].semantic_type == "advanced_themes"
    assert roots[0].children[0].content == "information-modeling, workflow"
    assert roots[0].children[0].semantic_type is None
