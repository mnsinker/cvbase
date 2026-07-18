from __future__ import annotations


ICON_SVGS = {
    "Explore": """
<svg
    class="project-link-icon"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
>
    <circle cx="12" cy="12" r="10"></circle>
    <polygon points="16 8 14 14 8 16 10 10 16 8"></polygon>
</svg>
""".strip(),

    "Live Demo": """
<svg
    class="project-link-icon"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
>
    <circle cx="12" cy="12" r="10"></circle>
    <polygon points="10 8 16 12 10 16 10 8"></polygon>
</svg>
""".strip(),

    "GitHub": """
<svg
    class="project-link-icon"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
>
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3.28-.36 6.72-1.61 6.72-7A5.4 5.4 0 0 0 19.3 3.75 5 5 0 0 0 19.16 0S18-.36 15 1.48a13.38 13.38 0 0 0-7 0C5-.36 3.84 0 3.84 0a5 5 0 0 0-.14 3.75A5.4 5.4 0 0 0 2.28 7.5c0 5.42 3.44 6.67 6.72 7A4.8 4.8 0 0 0 8 18v4"></path>
    <path d="M8 19c-3 .92-3-1.5-4-2"></path>
</svg>
""".strip(),
}


ICON_ALIASES = {
    "查看详情": "Explore",
    "了解项目": "Explore",
    "在线体验": "Live Demo",
}


def render_project_links(
    links: list[dict[str, str]],
) -> str:

    if not links:
        return ""

    rendered_links: list[str] = []

    for link in links:

        label = link["label"]

        icon_key = ICON_ALIASES.get(
            label,
            label,
        )

        icon_html = ICON_SVGS.get(
            icon_key,
            "",
        )

        rendered_links.append(
            f"""
<a
    class="project-link"
    href="{link["url"]}"
    target="_blank"
    rel="noopener noreferrer"
>
    {icon_html}
    <span>{label}</span>
</a>
""".strip()
        )

    separator = (
        '<span class="project-link-separator" '
        'aria-hidden="true">|</span>'
    )

    return f"\n{separator}\n".join(
        rendered_links
    )