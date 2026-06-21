from enum import Enum


class UnifiedAST(str, Enum):
    H1 = "h1"
    H2 = "h2"

    PARAGRAPH = "paragraph"
    BULLET = "bullet"

    BLANK_LINE = "blank_line"
    EOF = "eof"
