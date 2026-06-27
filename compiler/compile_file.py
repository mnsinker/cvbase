from pathlib import Path
from compiler.compile_markdown import compile_markdown
from compiler.entities.node import Node
from compiler.entities.semantic_registry import SemanticRegistry


def compile_file(path: Path, registry: SemanticRegistry | None = None) -> list[Node]:
    markdown = path.read_text()
    return compile_markdown(markdown, registry)