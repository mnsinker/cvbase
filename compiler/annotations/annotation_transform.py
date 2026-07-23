from compiler.entities.doc_nodes import DocNode, Document


def _remove_nodes_by_annotation_key(parent: DocNode, node: DocNode, annotation_key: str) -> None:
    for annotation in node.annotations:
        if annotation.key == annotation_key:
            parent.doc_children.remove(node)
            return
    for child in list(node.doc_children):
        _remove_nodes_by_annotation_key(node, child, annotation_key)


def remove_nodes_by_annotation_key(document: Document, annotation_key: str) -> Document | None:
    # 1. deal with document
    # remove the entire document, if document contains the specified annotation_key.
    for annotation in document.annotations:
        if annotation.key == annotation_key:
            return None

    # 2. deal with other doc_nodes
    for node in list(document.doc_children):
        _remove_nodes_by_annotation_key(document, node, annotation_key)
    return document