from __future__ import annotations

import re

from products.cv.entities.experience import Experience


def parse_experiences(
    markdown: str,
) -> list[Experience]:

    blocks = re.split(
        r"(?m)^##\s+",
        markdown,
    )

    experiences: list[Experience] = []

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if len(lines) < 3:
            continue

        company = re.sub(
            r"^##\s+",
            "",
            lines[0],
        ).strip()

        role = lines[1]

        start_date = ""
        end_date = ""

        bullets: list[str] = []

        for line in lines[2:]:

            date_match = re.fullmatch(
                r"(\d{4}-\d{2})\s+to\s+(\d{4}-\d{2})",
                line,
                flags=re.IGNORECASE,
            )

            if date_match:

                start_date = (
                    date_match.group(1)
                )

                end_date = (
                    date_match.group(2)
                )

                continue

            if line.startswith("-"):

                bullets.append(
                    line.removeprefix("-")
                    .strip()
                )

        experiences.append(
            Experience(
                company=company,
                role=role,
                start_date=start_date,
                end_date=end_date,
                bullets=bullets,
            )
        )

    return experiences

if __name__ == '__main__':
    experiences = parse_experiences(
       """
       ## Nike Icon Studio
Senior Operation Tech
2025-09 to 2025-12

- bullet1
- bullet2

## Nike Martech
Digital Product Manager
2025-01 to 2025-05

- bullet3
- bullet4
"""
    )
    print(experiences)