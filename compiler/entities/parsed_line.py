from dataclasses import dataclass


@dataclass
class ParsedLine:
    line_no: int
    raw: str

    content: str # raw[indent : ]  ie. stripped of indent
    indent: int = 0
