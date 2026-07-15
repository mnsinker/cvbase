from pathlib import Path

from compiler.annotations.configs import ANNOTATION_CONFIGS
from compiler.compile_file_to_json import compile_file_to_json
from compiler.entities.annotation_config import AnnotationConfig


def save_file_to_json(file_path: str, output_path: str | Path, annotation_configs: list[AnnotationConfig]|None=None) -> None:
    json_text = compile_file_to_json(file_path, annotation_configs)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json_text, encoding="utf-8")


save_file_to_json(
    file_path="/Users/mnsink/projects/cv-base/knowledge/narratives/job_projects/question_forge_zh.md",
    output_path="/Users/mnsink/projects/cv-base/apps/portfolio_web/content/projects/question-forge/zh.json",
    annotation_configs=ANNOTATION_CONFIGS
)


