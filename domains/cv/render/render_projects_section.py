from __future__ import annotations

from pathlib import Path

from domains.cv.entities.project import (
    Project,
)
from domains.cv.render.render_bullets import (
    render_bullets,
)
from domains.cv.render.normalize_name import (
    normalize_name,
)


TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)

SECTION_TITLES = {
    "en": "Projects",
    "zh-CN": "项目经历",
}


def render_projects_section(
    projects: list[Project],
    lang: str = "en",
) -> str:

    section_template = (
        TEMPLATES_DIR
        / "projects_section.html"
    ).read_text()

    card_template = (
        TEMPLATES_DIR
        / "project_card.html"
    ).read_text()

    project_cards: list[str] = []

    for project in projects:

        project_card = (
            card_template
            .replace(
                "{{project_name}}",
                normalize_name(project.name),
            )
            .replace(
                "{{project_label}}",
                project.label,
            )
            .replace(
                "{{bullets_html}}",
                render_bullets(
                    project.bullets,
                ),
            )
        )

        project_cards.append(
            project_card
        )

    return (
        section_template
        .replace(
            "{{section_title}}",
            SECTION_TITLES.get(lang, SECTION_TITLES["en"]),
        )
        .replace(
            "{{project_cards}}",
            "\n".join(
                project_cards
            ),
        )
    )


if __name__ == "__main__":

    projects = [
        Project(
            name="Question Forge",
            label="Information Modeling",
            bullets=[
                "PDF to Question Object",
                "VLM Extraction",
            ],
        ),
        Project(
            name="Decision Engine",
            label="Decision Modeling",
            bullets=[
                "Policy Layer",
                "Feedback Loop",
            ],
        ),
    ]

    html = render_projects_section(
        projects
    )

    print(
        html
    )
