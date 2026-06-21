from __future__ import annotations
from domains.cv.entities.sections import Sections
from domains.cv.sections_builder.extract_md_sections import extract_md_sections
from domains.cv.sections_builder.parse_projects import parse_projects
from domains.cv.sections_builder.parse_experiences import parse_experiences
from domains.cv.sections_builder.parse_earlier_experiences import parse_earlier_experiences
from domains.cv.sections_builder.parse_education import parse_education
from domains.cv.sections_builder.parse_summary import parse_summary
from domains.cv.sections_builder.parse_profile import parse_profile


def build_sections(markdown: str) -> Sections:
    raw_sections = extract_md_sections(markdown)

    return Sections(
        profile=parse_profile(raw_sections.get("profile", "")),
        summary=parse_summary(raw_sections.get("summary", "")),
        projects=parse_projects(raw_sections.get("projects","")),
        experiences=parse_experiences(raw_sections.get("experience",    "")),
        earlier_experiences=parse_earlier_experiences(raw_sections.get("earlier experience","")),
        education=parse_education(raw_sections.get("education", "")),
    )


if __name__ == "__main__":
    markdown_test = """
# Summary

AI Engineer

# Projects

## Question Forge

Information Modeling

- aaa
- bbb

# Experience

## Nike

Senior Engineer

2024-01 to 2025-01

- bullet1

## Earlier Experience

### Meituan

Product Manager

2019-01 to 2021-01

# Education

University of Queensland

Bachelor of Information Technology

2010-01 to 2013-12

- GPA 3.8
"""

    sections = build_sections(
        markdown_test
    )

    print(
        sections
    )
