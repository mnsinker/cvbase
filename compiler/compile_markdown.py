from compiler.engine.build_node_tree import build_node_tree
from compiler.engine.parse_lines import parse_lines
from compiler.entities.node import Node
from compiler.entities.semantic_registry import SemanticRegistry
from compiler.transforms.annotate_semantic_types import annotate_semantic_types
from compiler.transforms.rewrite_semantic_nodes import rewrite_semantic_nodes


def compile_markdown(markdown: str, registry: SemanticRegistry | None = None) -> list[Node]:

    roots = build_node_tree(parse_lines(markdown))

    if registry:
        annotate_semantic_types(roots, registry)
        rewrite_semantic_nodes(roots)

    return roots