from typing import Iterator
from compiler.entities.doc_nodes import Document, DocNode


def walk_nodes(node: Document | DocNode) -> Iterator[DocNode]:
    # 1. handle normal DocumentNode (ie. as long as it's not Document)
    if not isinstance(node, Document):
        yield node

    # 2. yield node's child
    for child in node.doc_children:
        yield from walk_nodes(child)
