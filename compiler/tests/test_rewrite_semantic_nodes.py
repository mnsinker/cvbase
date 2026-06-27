from compiler.entities.node import Node
from compiler.entities.unified_ast import UnifiedAST
from compiler.transforms.rewrite_semantic_nodes import rewrite_semantic_nodes


def test_rewrite_semantic_nodes():
    node = Node(
        ast_type=UnifiedAST.PARAGRAPH,
        semantic_type="career_spine",
        content="Career Spine: systems, governance"
    )

    rewrite_semantic_nodes([node])

    assert node.content == "Career Spine"
    assert len(node.children) == 2
    assert node.children[0].content == "systems"
    assert node.children[1].content == "governance"