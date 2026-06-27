from __future__ import annotations

from pathlib import Path

from domains.cv.entities.summary import Summary
from apps.cv_html.render.render_bullets import (
    render_bullets,
)
from apps.cv_html.render.render_markdown import render_markdown

TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)

SUMMARY_TITLES = {
    "en": {
        "summary_title": "Summary",
        "built_systems_title": "Built Systems",
        "previous_systems_title": "Previously Modeled Across",
        "technical_skills_title": "Technical Skills",
        "certifications_title": "Certifications",
    },
    "zh-CN": {
        "summary_title": "个人简介",
        "built_systems_title": "已构建系统",
        "previous_systems_title": "曾建模领域",
        "technical_skills_title": "技术技能",
        "certifications_title": "专业认证",
    },
}


def render_summary_section(
    summary: Summary,
    lang: str = "en",
) -> str:

    template = (
        TEMPLATES_DIR
        / "summary_section.html"
    ).read_text()

    titles = SUMMARY_TITLES.get(
        lang,
        SUMMARY_TITLES["en"],
    )

    built_systems_html = render_bullets(
        summary.built_systems,
    )
    previous_systems_html = render_bullets(
        summary.previous_systems,
    )

    return (
        template
        .replace("{{summary_title}}", titles["summary_title"])
        .replace(
            "{{intro}}",
            render_markdown(summary.intro),
        )
        .replace("{{built_systems_title}}", titles["built_systems_title"])
        .replace(
            "{{built_systems}}",
            built_systems_html,
        )
        .replace("{{previous_systems_title}}", titles["previous_systems_title"])
        .replace(
            "{{previous_systems}}",
            previous_systems_html,
        )
        .replace("{{technical_skills_title}}", titles["technical_skills_title"])
        .replace(
            "{{technical_skills}}",
            summary.technical_skills,
        )
        .replace("{{certifications_title}}", titles["certifications_title"])
        .replace(
            "{{certifications}}",
            summary.certifications,
        )
    )


if __name__ == "__main__":

    summary = Summary(
        name="Jieni Zhang",
        intro=(
            "AI engineer focused on "
            "modeling implicit systems."
        ),
        built_systems=[
            "Information Modeling",
            "Decision Modeling",
            "Knowledge Modeling",
        ],
        previous_systems=[
            "Financial Systems",
            "Operational Systems",
            "Workflow Systems",
        ],
        technical_skills=(
            "Python, JavaScript, SQL, "
            "NumPy, Pandas, Kibana"
        ),
        certifications="PMP",
    )

    html = render_summary_section(
        summary
    )

    print(
        html
    )
