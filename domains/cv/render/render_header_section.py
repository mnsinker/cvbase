from __future__ import annotations

from pathlib import Path

from domains.cv.entities.profile import Profile

TEMPLATES_DIR = (
    Path(__file__).parent.parent
    / "templates"
)


def render_header_section(
    profile: Profile,
) -> str:
    template = (
        TEMPLATES_DIR
        / "header_section.html"
    ).read_text()

    desired_position_html = ""
    if profile.desired_position:
        desired_position_html = (
            f"Desired Position: {profile.desired_position}"
        )

    return (
        template
        .replace(
            "{{name}}",
            profile.name,
        )
        .replace(
            "{{desired_position}}",
            desired_position_html,
        )
        .replace(
            "{{phone}}",
            profile.phone,
        )
        .replace(
            "{{email}}",
            profile.email,
        )
        .replace(
            "{{location}}",
            profile.location,
        )
    )
