from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import FrontMatter, Document


def frontmatter_to_dict(frontmatter: FrontMatter) -> dict[str, str]:
    metadata: dict[str, str] = {}

    if frontmatter is None:
        return metadata

    for line in frontmatter.content:
        line = line.strip()
        if not line: # skip empty line
            continue
        if ":" not in line: # skip invalid line
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def compile_file_with_transforms(path: str|Path, annotation_configs: list[AnnotationConfig], annotation_key: str) -> Document:
    document = compile_file(path, annotation_configs)
    remove_nodes_by_annotation_key(document, annotation_key)
    return document

