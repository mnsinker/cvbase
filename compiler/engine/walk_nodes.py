from compiler.entities.node import Node


def walk_nodes(roots: list[Node]):
    for root in roots:
        yield root
        yield from walk_nodes(root.children)
