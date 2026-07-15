from compiler.engine.tree_builder import build_tree
from compiler.entities.doc_nodes import Document, Heading, ListItem, Paragraph
from compiler.entities.parsed_node import ParsedNode


def test_build_tree_returns_document_with_root_nodes():
    nodes = [
        ParsedNode(line_no=1, indent=0, doc_node=Heading(level=1)),
        ParsedNode(line_no=2, indent=0, doc_node=Heading(level=1)),
    ]

    document = build_tree(iter(nodes))

    assert isinstance(document, Document)
    assert document.doc_children == [nodes[0].doc_node, nodes[1].doc_node]


def test_build_tree_nests_content_under_heading():
    heading = Heading(level=1)
    paragraph = Paragraph()

    document = build_tree(
        iter(
            [
                ParsedNode(line_no=1, indent=0, doc_node=heading),
                ParsedNode(line_no=2, indent=0, doc_node=paragraph),
            ]
        )
    )

    assert document.doc_children == [heading]
    assert heading.doc_children == [paragraph]


def test_build_tree_nests_indented_list_items():
    parent = ListItem(label="-")
    child = ListItem(label="-")

    document = build_tree(
        iter(
            [
                ParsedNode(line_no=1, indent=0, doc_node=parent),
                ParsedNode(line_no=2, indent=2, doc_node=child),
            ]
        )
    )

    assert document.doc_children == [parent]
    assert parent.doc_children == [child]
