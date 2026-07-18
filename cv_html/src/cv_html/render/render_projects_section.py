from __future__ import annotations

from pathlib import Path

from cv_html.entities.project import (
    Project,
)
from cv_html.render.render_bullets import (
    render_bullets,
)
from cv_html.render.normalize_name import (
    normalize_name,
)

from cv_html.render.render_project_links import (
    render_project_links,
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
                "{{project_links}}",
                render_project_links(
                    project.links,
                ),
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
            links=[
                {
                    "label": "Explore",
                    "url": "https://example.com/question-forge",
                },
                {
                    "label": "Live Demo",
                    "url": "https://example.com/question-forge/demo",
                },
            ],
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
