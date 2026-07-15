from compiler.annotations.configs import ANNOTATION_CONFIGS
from compiler.annotations.rule_builder import build_annotation_rules
from compiler.annotations.parsers import parse_annotation
from compiler.entities.annotation_rule import AnnotationRule
from compiler.entities.doc_nodes import Document, DocNode


def _visit(node: DocNode, parent: Document | DocNode, rules: dict[str, AnnotationRule]) -> None:
    annotation = parse_annotation(node, rules)
    if annotation:
        parent.annotations.append(annotation)
        parent.doc_children.remove(node)
        return

    for child in list(node.doc_children):
        _visit(child, node, rules)




def annotation_pass(document: Document) -> Document:
    rules = build_annotation_rules(ANNOTATION_CONFIGS)

    for child in list(document.doc_children):
        _visit(child, document, rules)
    return document
