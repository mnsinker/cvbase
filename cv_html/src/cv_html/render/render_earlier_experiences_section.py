from __future__ import annotations
from pathlib import Path
from cv_html.entities.earlier_experience import EarlierExperience
from cv_html.render.build_date_range import build_date_range


TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)

SECTION_TITLES = {
    "en": "Earlier Experience",
    "zh-CN": "早期经历",
}


def render_earlier_experiences_section(
    earlier_experiences: list[
        EarlierExperience
    ],
    lang: str = "en",
) -> str:

    section_template = (
        TEMPLATES_DIR
        / "earlier_experiences_section.html"
    ).read_text()

    bullet_template = (
        TEMPLATES_DIR
        / "earlier_experience_bullet.html"
    ).read_text()

    bullets: list[str] = []

    for experience in (
        earlier_experiences
    ):

        date_range = (
            build_date_range(
                experience.start_date,
                experience.end_date,
            )
        )

        bullet_html = (
            bullet_template
            .replace(
                "{{company}}",
                experience.company,
            )
            .replace(
                "{{role}}",
                experience.role,
            )
            .replace(
                "{{date_range}}",
                date_range,
            )
        )

        bullets.append(
            bullet_html
        )

    return (
        section_template
        .replace(
            "{{section_title}}",
            SECTION_TITLES.get(lang, SECTION_TITLES["en"]),
        )
        .replace(
            "{{earlier_experience_bullets}}",
            "\n".join(
                bullets
            ),
        )
    )




if __name__ == "__main__":

    earlier_experiences = [
        EarlierExperience(
            company="Thomas Cook Group",
            role="Director Product Mgt",
            start_date="2021-04",
            end_date="2021-08",
        ),
        EarlierExperience(
            company="Doro Financial",
            role="Product Manager",
            start_date="2015-12",
            end_date="2016-03",
        ),
    ]

    html = (
        render_earlier_experiences_section(
            earlier_experiences
        )
    )

    print(
        html
    )
