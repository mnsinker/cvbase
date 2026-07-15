from typing import Iterator
from compiler.entities.parsed_line import ParsedLine


def parse_lines(markdown: str) -> Iterator[ParsedLine]:
    return (
            ParsedLine(
                raw=line,
                line_no=i,
                indent=(indent := len(line)-len(line.lstrip())),
                content=line[indent:]
            )
            for i, line in enumerate(markdown.splitlines(), start=1)
        )
