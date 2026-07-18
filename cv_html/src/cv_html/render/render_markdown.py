from __future__ import annotations

import re


def render_markdown(
    text: str,
) -> str:

    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        text,
    )

    text = re.sub(
        r"\*(.+?)\*",
        r"<em>\1</em>",
        text,
    )

    return text