from __future__ import annotations

from pathlib import Path

from domains.cv.entities.education import Education
from apps.cv_html.render.build_date_range import build_date_range
from apps.cv_html.render.render_bullets import (
    render_bullets,
)


TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)

SECTION_TITLES = {
    "en": "Education",
    "zh-CN": "教育背景",
}


def render_education_section(
    education: Education,
    lang: str = "en",
) -> str:

    section_template = (
        TEMPLATES_DIR
        / "education_section.html"
    ).read_text()

    card_template = (
        TEMPLATES_DIR
        / "education_card.html"
    ).read_text()

    card_html = (
        card_template
        .replace(
            "{{date_range}}",
            build_date_range(
                education.start_date,
                education.end_date,
            ),
        )
        .replace(
            "{{school}}",
            education.school,
        )
        .replace(
            "{{degree}}",
            education.degree,
        )
        .replace(
            "{{bullets_html}}",
            render_bullets(
                education.bullets,
            ),
        )
    )

    return (
        section_template
        .replace(
            "{{section_title}}",
            SECTION_TITLES.get(lang, SECTION_TITLES["en"]),
        )
        .replace(
            "{{education_cards}}",
            card_html,
        )
    )


if __name__ == "__main__":

    education = Education(
        school="University of Queensland",
        degree="Bachelor of Information Technology",
        start_date="2010-01",
        end_date="2013-12",
        bullets=[
            "GPA 3.8",
            "Dean's List",
        ],
    )

    html = render_education_section(
        education
    )

    print(
        html
    )
