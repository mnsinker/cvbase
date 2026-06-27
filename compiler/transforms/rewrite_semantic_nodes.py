from compiler.engine.walk_nodes import walk_nodes
from compiler.entities.node import Node
from compiler.entities.unified_ast import UnifiedAST


def rewrite_semantic_nodes(roots: list[Node]) -> None:
    for node in walk_nodes(roots):
        if not node.semantic_type:
            continue
        if node.children:
            continue
        if ":" not in node.content:
            continue

        content_key, content_value = node.content.split(":", maxsplit=1)

        # 1. 处理 node.content:
        node.content = content_key.strip()
        # 2. 处理 node.children:
        child_list = [child.strip() for child in content_value.split(",") if child.strip()]
        node.children.extend([Node(ast_type=UnifiedAST.PARAGRAPH, content=child) for child in child_list])

