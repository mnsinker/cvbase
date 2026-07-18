from __future__ import annotations

from pathlib import Path

from cv_html.entities.experience import Experience
from cv_html.render.build_date_range import build_date_range
from cv_html.render.build_duration import build_duration
from cv_html.render.render_bullets import (
    render_bullets,
)


TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)

SECTION_TITLES = {
    "en": "Experience",
    "zh-CN": "工作经历",
}


def render_experiences_section(
    experiences: list[Experience],
    lang: str = "en",
) -> str:

    section_template = (
        TEMPLATES_DIR
        / "experiences_section.html"
    ).read_text()

    card_template = (
        TEMPLATES_DIR
        / "experience_card.html"
    ).read_text()

    experience_cards: list[str] = []

    for experience in experiences:

        date_range = build_date_range(
            experience.start_date,
            experience.end_date,
        )

        experience_card = (
            card_template
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
            .replace(
                "{{duration}}",
                build_duration(
                    experience.start_date,
                    experience.end_date,
                ),
            )
            .replace(
                "{{bullets_html}}",
                render_bullets(
                    experience.bullets,
                ),
            )
        )

        experience_cards.append(
            experience_card
        )

    return (
        section_template
        .replace(
            "{{section_title}}",
            SECTION_TITLES.get(lang, SECTION_TITLES["en"]),
        )
        .replace(
            "{{experience_cards}}",
            "\n".join(
                experience_cards
            ),
        )
    )


if __name__ == "__main__":

    experiences = [
        Experience(
            company="Nike Icon Studio",
            role="Senior Operation Tech",
            start_date="2025-09",
            end_date="2025-12",
            bullets=[
                "Built EQ protocol",
                "Built workflow governance",
            ],
        ),
        Experience(
            company="Nike Martech",
            role="Digital Product Manager",
            start_date="2025-01",
            end_date="2025-05",
            bullets=[
                "Led product roadmap",
                "Managed stakeholder alignment",
            ],
        ),
    ]

    html = render_experiences_section(
        experiences
    )

    print(
        html
    )
