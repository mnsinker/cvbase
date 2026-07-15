from typing import Iterator
from compiler.engine.node_builder import _lookup_rule
from compiler.entities.doc_nodes import DocNode, Heading, ListItem, Document
from compiler.entities.parsed_node import ParsedNode

""" recover ownership """
def _is_parent(previous: ParsedNode, current: ParsedNode) -> bool:
    # 0. children grammar constraint
    parent_rule = _lookup_rule(previous.doc_node)
    if type(current.doc_node) not in parent_rule.allowed_doc_children:
        return False

    # 1. heading hierarchy
    if isinstance(previous.doc_node, Heading):
        # 1.1 heading vs heading
        if isinstance(current.doc_node, Heading):
            return previous.doc_node.level < current.doc_node.level
        # 1.2 heading vs others
        return True

    # 2. indent hierarchy
    if current.indent - previous.indent >= 4:
        return True

    # 3. list hierarchy
    if not isinstance(previous.doc_node, ListItem) and isinstance(current.doc_node, ListItem):
        return True

    return False

def build_tree(parsed_nodes: Iterator[ParsedNode]) -> Document:
    stack: list[ParsedNode] = []
    roots: list[DocNode] = []

    for current in parsed_nodes:
        # 0. first node
        if not stack:
            roots.append(current.doc_node)
            stack.append(current)
            continue

        # 1. find parent
        while stack:
            previous = stack[-1]
            if _is_parent(previous, current):
                break
            stack.pop()

        # 2. parent found or stack is emptied
        if stack:   # 2.1 if stack is not empty
            stack[-1].doc_node.doc_children.append(current.doc_node)
            stack.append(current)
        else:       # 2.2 if stack is empty
            roots.append(current.doc_node)
            stack.append(current)

    return Document(doc_children=roots)