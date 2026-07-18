from __future__ import annotations

import re

from cv_html.entities.earlier_experience import (
    EarlierExperience,
)


def parse_earlier_experiences(
    markdown: str,
) -> list[EarlierExperience]:


    earlier_experiences: list[
        EarlierExperience
    ] = []

    for line in markdown.splitlines():

        line = line.strip()

        if not line:
            continue

        match = re.fullmatch(
            r"\s*-\s+(.+?)[,，]\s*(.+?)\s+\|\s+(\d{4}-\d{2})\s*(?:to|－|-|—)\s*(\d{4}-\d{2})",
            line,
        )

        if not match:
            continue

        earlier_experiences.append(
            EarlierExperience(
                company=match.group(1),
                role=match.group(2),
                start_date=match.group(3),
                end_date=match.group(4),
            )
        )

    return earlier_experiences

if __name__ == "__main__":
    early_experiences = parse_earlier_experiences(
        """
        # Experience

## Nike

Senior Engineer
2024-01 to 2025-01

- aaa

## Earlier Experience

- Meituan, Product Manager | 2019-01 to 2021-01
- Thomas Cook, Business Analyst | 2017-01 to 2019-01"""
    )
    print(early_experiences)
