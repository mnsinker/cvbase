import json

from compiler.annotations.configs import ANNOTATION_CONFIGS
from compiler.compile_file import compile_file
from compiler.entities.annotation_config import AnnotationConfig


def compile_file_to_json(path: str, annotation_configs: list[AnnotationConfig]|None = None) -> str:
    document = compile_file(path, annotation_configs)
    return json.dumps(document.to_dict(), indent=4, ensure_ascii=False)




