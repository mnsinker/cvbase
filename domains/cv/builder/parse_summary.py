from __future__ import annotations

import re

from domains.cv.entities.summary import (
    Summary,
)


SUMMARY_ALIASES = {
    "built systems": "built systems",
    "已构建系统": "built systems",
    "previously modeled across": "previously modeled across",
    "曾建模领域": "previously modeled across",
    "technical skills": "technical skills",
    "技术技能": "technical skills",
    "certifications": "certifications",
    "专业认证": "certifications",
}


def parse_summary(
    content: str,
) -> Summary:

    sections: dict[str, list[str]] = {}

    current_section = "intro"

    sections[current_section] = []

    for line in content.splitlines():

        match = re.fullmatch(
            r"##\s+(.+)",
            line.strip(),
        )

        if match:

            raw_heading = (
                match.group(1)
                .strip()
                .lower()
            )
            current_section = SUMMARY_ALIASES.get(
                raw_heading,
                raw_heading,
            )

            sections[current_section] = []

            continue

        sections[current_section].append(
            line
        )

    intro_lines = [
        line.strip()
        for line in sections.get(
            "intro",
            [],
        )
        if line.strip()
    ]

    intro = ""

    if intro_lines:
        intro = "\n".join(
            intro_lines
        )

    built_systems = _extract_bullets(
        sections.get(
            "built systems",
            [],
        )
    )

    previous_systems = _extract_bullets(
        sections.get(
            "previously modeled across",
            [],
        )
    )

    technical_skills = "\n".join(
        sections.get(
            "technical skills",
            [],
        )
    ).strip()

    certifications = "\n".join(
        sections.get(
            "certifications",
            [],
        )
    ).strip()

    return Summary(
        intro=intro,
        built_systems=built_systems,
        previous_systems=previous_systems,
        technical_skills=technical_skills,
        certifications=certifications,
    )


def _extract_bullets(lines: list[str]) -> list[str]:

    bullets: list[str] = []

    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())

    return bullets


if __name__ == "__main__":

    result = parse_summary(
        """
专注于信息系统、决策系统与知识系统建模的 AI 工程师。

## 已构建系统

- 信息建模
- 决策建模

## 曾建模领域

- 金融系统
- 运营系统

## 技术技能

Python、JavaScript

## 专业认证

PMP
"""
    )

    print("built_systems:", result.built_systems)
    print("previous_systems:", result.previous_systems)
    print("technical_skills:", repr(result.technical_skills))
    print("certifications:", repr(result.certifications))
