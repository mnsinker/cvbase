from compiler.engine.line_parser import parse_lines
from compiler.engine.node_builder import build_parsed_nodes
from compiler.engine.tree_builder import build_tree
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document
from compiler.annotations.annotation_pass import annotation_pass


def compile_markdown(markdown: str, annotation_configs: list[AnnotationConfig]|None = None) -> Document:

    parsed_lines = parse_lines(markdown)
    parsed_nodes = build_parsed_nodes(parsed_lines)
    document = build_tree(parsed_nodes)

    if annotation_configs:
        document = annotation_pass(document)

    return document