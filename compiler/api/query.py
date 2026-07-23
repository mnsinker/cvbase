from compiler.engine.walk_nodes import walk_doc_nodes, walk_inline_nodes
from compiler.utils.text_extractor import extract_inline_text
from compiler.entities.doc_nodes import DocNode
from compiler.entities.inline_nodes import InlineNode, Link
from typing import TypeVar, Any
T = TypeVar("T", bound=DocNode)


def get_text(node: DocNode | InlineNode) -> str:
    if node is None:
        return ""
    if isinstance(node, InlineNode):
        return extract_inline_text([node]).strip()
    return extract_inline_text(node.inline_children).strip()  # recursive

def get_children_text(node: DocNode) -> list[str]:
    if node is None:
        return []
    return [text for child in node.doc_children if (text:=get_text(child))]

def get_node_by_type(node: DocNode, searching_type: type[T]) -> T | None:
    if node is None:
        return None
    if isinstance(node, searching_type):
        return node
    for child in node.doc_children:
        result_node = get_node_by_type(child, searching_type)
        if result_node:
            return result_node
    return None

def get_node_by_text(node: DocNode | InlineNode, searching_text: str) -> DocNode | None:
    if node is None:
        return None
    current_text = get_text(node).rstrip(":").lower()
    if searching_text.lower().strip() == current_text:
        return node
    for child in getattr(node, "doc_children", []):
        doc_node = get_node_by_text(child, searching_text)  # recursive
        if doc_node:
            return doc_node
    return None

def get_annotation_value(node: DocNode, searching_key: str) -> Any:
    for annotation in getattr(node, "annotations", []):
        if annotation.key == searching_key:
            return annotation.values
    return None


def get_links(node: DocNode) -> list[dict[str, str]]:
    if node is None:
        return []
    links = []
    for doc_node in walk_doc_nodes(node):
        for inline_node in walk_inline_nodes(doc_node):
            if isinstance(inline_node, Link):
                links.append({"title": get_text(inline_node), "url": inline_node.url})
    return links


def get_doc_children(node: DocNode) -> list[DocNode]:
    if node is None:
        return []
    return node.doc_children


def get_inline_children(node: DocNode) -> list[InlineNode]:
    if node is None:
        return []
    return node.inline_children



