from __future__ import annotations
import re


SECTION_ALIASES = {
    "profile": "profile",
    "基本信息": "profile",
    "个人信息": "profile",
    "summary": "summary",
    "个人简介": "summary",
    "projects": "projects",
    "项目经历": "projects",
    "experience": "experience",
    "工作经历": "experience",
    "earlier experience": "earlier experience",
    "早期经历": "earlier experience",
    "education": "education",
    "教育背景": "education",
}


def normalize_heading(
    heading: str,
) -> str:
    key = heading.strip().lower()
    return SECTION_ALIASES.get(
        key,
        key,
    )


def extract_md_sections(markdown: str) -> dict[str, str]:

    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in markdown.splitlines():
        match = re.fullmatch(r"#\s+(.+)", line)

        if match:
            current_section = normalize_heading(
                match.group(1)
            )
            sections[current_section] = []
            continue

        if current_section:
            sections[current_section].append(line)

    return {
        section_name: "\n".join(lines).strip()
        for section_name, lines in sections.items()
    }


if __name__ == "__main__":

    sections = extract_md_sections(
        """
# 基本信息

张洁妮

# 个人简介

AI 工程师

# 项目经历

Project Content

# 工作经历

Experience Content

# 早期经历

Earlier Content

# 教育背景

Education Content
"""
    )

    print(
        sections.keys()
    )
