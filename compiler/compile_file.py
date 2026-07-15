from pathlib import Path
from compiler.compile_markdown import compile_markdown
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document


def compile_file(path: str, annotation_config: list[AnnotationConfig]|None = None) -> Document:
    try:
        markdown = Path(path).read_text()
    except:
        raise FileNotFoundError(f"Please provide valid file path. File {path} not found")

    return compile_markdown(markdown, annotation_config)