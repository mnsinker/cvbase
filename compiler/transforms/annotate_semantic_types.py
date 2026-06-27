from compiler.engine.walk_nodes import walk_nodes
from compiler.entities.node import Node
from compiler.entities.semantic_registry import SemanticRegistry


def annotate_semantic_types(roots: list[Node], registry: SemanticRegistry) -> None:
    for node in walk_nodes(roots):
        normalized = node.content.split(":", maxsplit=1)[0].strip().lower()
        node.semantic_type = registry.get(normalized)