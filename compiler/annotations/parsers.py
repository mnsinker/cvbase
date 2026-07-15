from compiler.annotations.matcher import match_annotation
from compiler.annotations.text_extractor import _extract_inline_text
from compiler.engine.walk_nodes import walk_nodes
from compiler.entities.annotation import Annotation
from compiler.entities.annotation_rule import AnnotationRule
from compiler.entities.doc_nodes import DocNode


def _parse_string(annotation_subtree: list[DocNode]) -> str:
    """ Parse annotation value as a string. """
    # case 1: single line
    annotation_node = annotation_subtree[0]
    annotation_line_text = _extract_inline_text(annotation_node.inline_children)
    _, _, values = annotation_line_text.partition(":")
    values = values.strip()
    if values:
        return values

    # case 2. mult lines
    return "\n".join(
        _extract_inline_text(value_node.inline_children)
        for value_node in annotation_subtree[1:] # value_nodes
    )


def _parse_bool(annotation_subtree: list[DocNode]) -> bool:
    annotation_node = annotation_subtree[0]
    text = _extract_inline_text(annotation_node.inline_children)
    _, _, value = text.partition(":")
    return False if value.strip().lower() == "false" else True


def _parse_list(annotation_subtree: list[DocNode]) -> list[str]:
    # case 1. single line
    annotation_node = annotation_subtree[0]
    annotation_line_text = _extract_inline_text(annotation_node.inline_children)
    _, _, values = annotation_line_text.partition(":")
    values = values.strip()
    if values:
        values = values.split(",")
        return [value.strip() for value in values if value.strip()]

    # case 2. multi lines
    return [
        _extract_inline_text(value_node.inline_children)
        for value_node in annotation_subtree[1:]
    ]



def parse_annotation(node: DocNode, rules: dict[str, AnnotationRule]) -> Annotation|None:
    rule = match_annotation(node, rules)

    if rule is None: # no annotation
       return None

    annotation_subtree = list(walk_nodes(node))
    values = rule.parser(annotation_subtree)
    annotation = Annotation(key=rule.key, values=values)

    return annotation
