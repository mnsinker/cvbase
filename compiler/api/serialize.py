import json
from pathlib import Path

from compiler.annotations.configs import ANNOTATION_CONFIGS
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig


def compile_file_to_json(path: str | Path, annotation_configs: list[AnnotationConfig]|None = None) -> str:
    document = compile_file(path, annotation_configs)
    return json.dumps(document.to_dict(), indent=4, ensure_ascii=False)



def save_file_to_json(file_path: str|Path, output_path: str | Path, annotation_configs: list[AnnotationConfig]|None=None) -> None:
    json_text = compile_file_to_json(file_path, annotation_configs)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json_text, encoding="utf-8")


if __name__ == '__main__':
    save_file_to_json(
        # file_path="/Users/mnsink/projects/cv-base/knowledge/narratives/job_projects/question_forge_zh.md",
        file_path="/Users/mnsink/projects/cv-base/knowledge/career/profile/profile.md",
        output_path="/Users/mnsink/projects/cv-base/knowledge/career/profile/profile.json",
        annotation_configs=ANNOTATION_CONFIGS
    )