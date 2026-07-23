from typing import Iterator
from compiler.entities.doc_nodes import Document, DocNode
from compiler.entities.inline_nodes import InlineNode


def walk_doc_nodes(node: Document | DocNode) -> Iterator[DocNode]:
    # 1. handle normal DocumentNode (i.e. as long as it's not Document)
    if not isinstance(node, Document):
        yield node

    # 2. yield node's child
    for child in node.doc_children:
        yield from walk_doc_nodes(child)


def walk_inline_nodes(node: DocNode | InlineNode) -> Iterator[InlineNode]:
    for inline_node in node.inline_children:
        yield inline_node
        yield from walk_inline_nodes(inline_node)