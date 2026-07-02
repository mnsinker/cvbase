from compiler.engine.build_node_tree import build_node_tree
from compiler.engine.parse_lines import parse_lines

def test_siblings():
    md = """
A
B
"""

    roots = build_node_tree(parse_lines(md))

    assert len(roots) == 2
    assert roots[0].content == "A"
    assert roots[1].content == "B"


def test_indent_child():
    md = """
A
    B
"""

    roots = build_node_tree(parse_lines(md))

    assert len(roots) == 1
    assert roots[0].content == "A"

    assert len(roots[0].children) == 1
    assert roots[0].children[0].content == "B"


def test_indent_grandchild():
    md = """
A
    B
        C
"""

    roots = build_node_tree(parse_lines(md))

    assert roots[0].content == "A"
    assert roots[0].children[0].content == "B"
    assert roots[0].children[0].children[0].content == "C"


def test_indent_pop():
    md = """
A
    B
C
"""

    roots = build_node_tree(parse_lines(md))

    assert len(roots) == 2

    assert roots[0].content == "A"
    assert roots[0].children[0].content == "B"

    assert roots[1].content == "C"