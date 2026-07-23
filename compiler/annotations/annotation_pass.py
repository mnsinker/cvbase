from compiler.annotations.rule_builder import build_annotation_rules
from compiler.annotations.parsers import parse_annotation
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.annotation_rule import AnnotationRule
from compiler.entities.doc_nodes import Document, DocNode


def _annotate_node(node: DocNode, parent: Document | DocNode, rules: dict[str, AnnotationRule]) -> None:
    annotation = parse_annotation(node, rules)
    if annotation:
        parent.annotations.append(annotation)
        return

    for child in list(node.doc_children):
        _annotate_node(child, node, rules)     # recursive



def annotation_pass(document: Document, annotation_configs: list[AnnotationConfig]) -> Document:
    rules = build_annotation_rules(annotation_configs)

    for child in list(document.doc_children):
        _annotate_node(child, document, rules)
    return document
