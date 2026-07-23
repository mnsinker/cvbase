import subprocess
from pathlib import Path
from compiler.entities.annotation_config import AnnotationConfig
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.parser.cv_parser import parse_cv
from cv_html.render.renderer import render_cv

OUTPUT_DIR = Path(__file__).parents[2] / "output"
def _write_output(html: str, language: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"cv_{language}.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _open_output(path: str | Path, open_mode) -> None:
    if open_mode == "finder":
        subprocess.run(["open", "-R", str(path)], check=False)
    elif open_mode == "browser":
        subprocess.run(["open", str(path)], check=False)


def build_cv(
        folder_path: str,
        language: str="en",
        annotation_configs: list[AnnotationConfig]|None = CV_ANNOTATIONS,
        open_mode: str | None = "finder"
) -> Path:
    cv = parse_cv(folder_path, language, annotation_configs)
    html = render_cv(cv, language=language)
    output_path = _write_output(html, language)
    _open_output(output_path, open_mode)
    return output_path

build_cv("/Users/mnsink/projects/cv-base/knowledge/career", language="en")
# build_cv("/Users/mnsink/projects/cv-base/knowledge/career", language="zh")
