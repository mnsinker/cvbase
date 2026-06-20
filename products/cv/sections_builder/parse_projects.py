from __future__ import annotations

import re

from products.cv.entities.project import Project


def parse_projects(
    markdown: str,
) -> list[Project]:

    project_blocks = re.split(
        r"(?m)^##\s+",
        markdown,
    )

    projects: list[Project] = []

    for block in project_blocks:

        block = block.strip()

        if not block:
            continue

        lines = block.splitlines()

        name = lines[0].strip()

        label = ""

        bullets: list[str] = []

        for line in lines[1:]:

            line = line.strip()

            if not line:
                continue

            if not label and not line.startswith("-"):
                label = line
                continue

            if line.startswith("-"):
                bullets.append(
                    line.removeprefix("-").strip()
                )

        projects.append(
            Project(
                name=name,
                label=label,
                bullets=bullets,
            )
        )

    return projects

if __name__ == '__main__':
    proj = parse_projects(
        """## question_forge
Information Modeling

- aaa
- bbb

## decision_engine
Decision Modeling

- ccc
- ddd"""
)

    print(proj)