from __future__ import annotations
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    __import__("sys").path.insert(0, str(Path(__file__).resolve().parent.parent))

from cv_html.builder.build_sections import build_sections
from cv_html.render.render_header_section import render_header_section
from cv_html.render.render_summary_section import render_summary_section
from cv_html.render.render_projects_section import render_projects_section
from cv_html.render.render_experiences_section import render_experiences_section
from cv_html.render.render_earlier_experiences_section import render_earlier_experiences_section
from cv_html.render.render_education_section import render_education_section


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent.parent

TEMPLATES_DIR = PACKAGE_DIR / "templates"
OUTPUT_DIR = PROJECT_DIR / "output"


def main(markdown_path: str) -> None:

    markdown_path = Path(markdown_path)
    markdown = (markdown_path.read_text(encoding="utf-8"))

    stem = markdown_path.stem
    if stem.endswith("_zh"):
        html_lang = "zh-CN"
    elif stem.endswith("_en"):
        html_lang = "en"
    else:
        raise ValueError(f"Filename must end with _zh or _en: {stem}")

    sections = build_sections(markdown)
    template = (TEMPLATES_DIR / "cv.html").read_text(encoding="utf-8")
    styles = (TEMPLATES_DIR / "cv.css").read_text(encoding="utf-8")

    header_html = (
        render_header_section(sections.profile)
    )

    summary_html = render_summary_section(sections.summary, html_lang)
    projects_html = render_projects_section(sections.projects, html_lang)
    experiences_html = render_experiences_section(sections.experiences, html_lang)
    earlier_experiences_html = render_earlier_experiences_section(sections.earlier_experiences, html_lang)
    education_html = render_education_section(sections.education, html_lang)

    html = (
        template
        .replace("{{styles}}", styles)
        .replace("{{html_lang}}", html_lang)
        .replace("{{header}}", header_html)
        .replace("{{summary}}", summary_html)
        .replace("{{projects}}",projects_html)
        .replace("{{experiences}}", experiences_html)
        .replace("{{earlier_experiences}}", earlier_experiences_html)
        .replace("{{education}}", education_html)
    )

    output_path = (OUTPUT_DIR/ f"{stem}.html")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8",)

    print(f"Saved: {output_path}")


if __name__ == "__main__":

    main("/Users/mnsink/projects/cv-base/knowledge/products/cv/output_consolidated/cv_ai-fde_260613_view_en.md")
