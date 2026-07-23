from pathlib import Path
from compiler.annotations.configs import ANNOTATION_CONFIGS
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
        document = annotation_pass(document, annotation_configs)

    return document


def compile_file(path: str | Path, annotation_configs: list[AnnotationConfig]|None = None) -> Document:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'File not found: {path}')

    markdown = path.read_text(encoding='utf-8')
    return compile_markdown(markdown, annotation_configs)


def compile_folder(folder: str | Path, annotation_configs: list[AnnotationConfig]|None = None) -> list[Document]:
    return [
        compile_file(md_path, annotation_configs)
        for md_path in sorted(Path(folder).glob("*.md"))
    ]


