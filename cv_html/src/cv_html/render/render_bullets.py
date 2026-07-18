from __future__ import annotations

from pathlib import Path

from cv_html.render.render_markdown import render_markdown


TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)


def render_bullets(
    bullets: list[str],
) -> str:

    bullet_template = (
        TEMPLATES_DIR
        / "bullet.html"
    ).read_text()

    rendered_bullets: list[str] = []

    for bullet in bullets:
        if bullet.strip() == "--":
            continue

        bullet_html = (
            bullet_template
            .replace(
                "{{bullet_text}}",
                render_markdown(
                    bullet,
                ),
            )
        )

        rendered_bullets.append(
            bullet_html
        )

    return "\n".join(
        rendered_bullets
    )
