from __future__ import annotations

import re

from products.cv.entities.education import Education


def parse_education(
    education_markdown: str,
) -> Education:

    lines = [
        line.strip()
        for line in education_markdown.splitlines()
        if line.strip()
    ]

    if len(lines) < 3:

        raise ValueError(
            "Education section requires:\n"
            "school\n"
            "degree\n"
            "date range"
        )

    school = lines[0]
    degree = lines[1]

    date_line = lines[2]

    date_match = re.fullmatch(
        r"(\d{4}[.-]\d{2})\s*(?:to|—|–|-)\s*(\d{4}[.-]\d{2})",
        date_line,
    )

    if not date_match:

        raise ValueError(
            f"Unable to parse education date range:\n{date_line}"
        )

    start_date = (
        date_match
        .group(1)
        .replace(".", "-")
    )

    end_date = (
        date_match
        .group(2)
        .replace(".", "-")
    )

    bullets: list[str] = []

    for line in lines[3:]:

        if line.startswith("-"):

            bullets.append(
                line.removeprefix("-")
                .strip()
            )

    return Education(
        school=school,
        degree=degree,
        start_date=start_date,
        end_date=end_date,
        bullets=bullets,
    )


if __name__ == "__main__":

    education = parse_education(
        """
Michigan State University

Bachelor in Finance

2005.05 - 2007.12

- Graduating a 4-year university in 2 years
- Graduated with High Honor
"""
    )

    print(education)