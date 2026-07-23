from compiler.api.query import get_annotation_value, get_node_by_text
from compiler.entities.doc_nodes import DocNode, Document


def is_visible(doc_node: DocNode) -> bool:
    value = get_annotation_value(doc_node, "excluded_visibility")
    return value is not True


def get_visible_node_by_text(document: Document | DocNode, searching_texts: str | list[str]) -> DocNode | None:
    # if str, then wrap it in a list.
    if isinstance(searching_texts, str):
        searching_texts = [searching_texts]

    for t in searching_texts:
        node = get_node_by_text(document, t)
        if node:
            return node
    return None