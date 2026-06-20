from __future__ import annotations

import shutil
from pathlib import Path

from products.cv.sections_builder.build_sections import (
    build_sections,
)

from products.cv.render.render_header_section import (
    render_header_section,
)

from products.cv.render.render_summary_section import (
    render_summary_section,
)

from products.cv.render.render_projects_section import (
    render_projects_section,
)

from products.cv.render.render_experiences_section import (
    render_experiences_section,
)

from products.cv.render.render_earlier_experiences_section import (
    render_earlier_experiences_section,
)

from products.cv.render.render_education_section import (
    render_education_section,
)


BASE_DIR = Path(__file__).parents[2]
TEMPLATES_DIR = (BASE_DIR/ "products/cv/templates")
OUTPUT_DIR = (BASE_DIR/ "products/cv/output")


def main(markdown_path: str) -> None:

    markdown_path = Path(BASE_DIR / markdown_path)
    markdown = (markdown_path.read_text(encoding="utf-8"))

    stem = markdown_path.stem
    if stem.endswith("_zh"):
        html_lang = "zh-CN"
    elif stem.endswith("_en"):
        html_lang = "en"
    else:
        raise ValueError(f"Filename must end with _zh or _en: {stem}")

    sections = build_sections(markdown)
    template = (TEMPLATES_DIR/ "cv.html").read_text(encoding="utf-8")

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
        .replace("{{html_lang}}", html_lang)
        .replace("{{header}}", header_html)
        .replace("{{summary}}", summary_html)
        .replace("{{projects}}",projects_html)
        .replace("{{experiences}}", experiences_html)
        .replace("{{earlier_experiences}}", earlier_experiences_html)
        .replace("{{education}}", education_html)
    )

    output_path = (OUTPUT_DIR/ f"{stem}.html")
    output_path.write_text(html, encoding="utf-8",)

    print(f"Saved: {output_path}")


if __name__ == "__main__":

    # main("content/views/cv_ai-fde_260613_view_zh.md")
    main("content/views/cv_ai-fde_260613_view_en.md")