from compiler.engine.line_parser import parse_lines
from compiler.engine.node_builder import build_parsed_nodes
from compiler.entities.doc_nodes import CodeBlock, FrontMatter, Heading, HorizontalRule, ListItem, Paragraph
from compiler.entities.inline_nodes import Strong, Text


def _nodes(markdown: str):
    return list(build_parsed_nodes(parse_lines(markdown)))


def test_build_parsed_nodes_builds_headings_with_inline_children():
    [node] = _nodes("# Hello **world**")

    assert node.line_no == 1
    assert node.indent == 0
    assert isinstance(node.doc_node, Heading)
    assert node.doc_node.level == 1
    assert node.doc_node.inline_children[0] == Text(content="Hello ")
    assert isinstance(node.doc_node.inline_children[1], Strong)
    assert node.doc_node.inline_children[1].inline_children == [Text(content="world")]


def test_build_parsed_nodes_builds_list_items_and_paragraphs():
    nodes = _nodes("- item\nplain")

    assert isinstance(nodes[0].doc_node, ListItem)
    assert nodes[0].doc_node.label == "-"
    assert nodes[0].doc_node.inline_children == [Text(content="item")]
    assert isinstance(nodes[1].doc_node, Paragraph)
    assert nodes[1].doc_node.inline_children == [Text(content="plain")]


def test_build_parsed_nodes_builds_front_matter_only_at_first_line():
    [front_matter, rule] = _nodes("---\ntitle: Test\n---\n---")

    assert isinstance(front_matter.doc_node, FrontMatter)
    assert front_matter.doc_node.content == ["title: Test"]
    assert isinstance(rule.doc_node, HorizontalRule)


def test_build_parsed_nodes_builds_fenced_code_block():
    [node] = _nodes("```python\nprint('x')\n```")

    assert isinstance(node.doc_node, CodeBlock)
    assert node.doc_node.language == "python"
    assert node.doc_node.content == ["print('x')"]
