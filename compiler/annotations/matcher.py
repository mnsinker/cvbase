from compiler.utils.text_extractor import extract_inline_text
from compiler.entities.annotation_rule import AnnotationRule
from compiler.entities.doc_nodes import DocNode


def _normalize_annotation_key(text: str) -> str:
    return (
        text.removesuffix(":")
            .replace("-", "_")
            .replace(" ", "_")
            .lower()
            .strip()
    )

def match_annotation(node: DocNode, rules: dict[str, AnnotationRule]) -> AnnotationRule|None:
    if not node.inline_children:
        return None

    text = extract_inline_text(node.inline_children)
    key, _, _ = text.partition(":")
    normalized_key = _normalize_annotation_key(key)

    return rules.get(normalized_key)
