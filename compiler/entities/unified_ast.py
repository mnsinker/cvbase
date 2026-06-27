from enum import Enum


class UnifiedAST(str, Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"

    PARAGRAPH = "paragraph"
    BULLET = "bullet"

    CODE_BLOCK = "code_block"
    IMAGE = "image"

    BLANK_LINE = "blank_line"
    EOF = "eof"
