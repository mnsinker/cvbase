from compiler.entities.parsed_line import ParsedLine
from compiler.entities.unified_ast import UnifiedAST

def _detect_unified_ast(raw: str) -> UnifiedAST:
    # blank line
    if not raw.strip():
        return UnifiedAST.BLANK_LINE

    # h3
    if raw.startswith("### "):
        return UnifiedAST.H3

    # h2
    if raw.startswith("## "):
        return UnifiedAST.H2

    # h1
    if raw.startswith("# "):
        return UnifiedAST.H1

    # bullet
    stripped = raw.lstrip()
    if stripped.startswith("- "):
        return UnifiedAST.BULLET

    if stripped.startswith("* "):
        return UnifiedAST.BULLET

    # image
    if raw.strip().startswith("!["):
        return UnifiedAST.IMAGE

    # paragraph
    return UnifiedAST.PARAGRAPH



def _detect_content(raw: str, ast_type: UnifiedAST) -> str:
    if ast_type == UnifiedAST.H1:
        return raw[2:].strip()

    if ast_type == UnifiedAST.H2:
        return raw[3:].strip()

    if ast_type == UnifiedAST.H3:
        return raw[4:].strip()

    if ast_type == UnifiedAST.BULLET:
        stripped = raw.lstrip()
        if stripped.startswith("* "):
            return stripped[2:].strip()
        if stripped.startswith("- "):
            return stripped[2:].strip()
        if stripped.startswith("+ "):
            return stripped[2:].strip()

    return raw.strip()



def _detect_indent(raw: str) -> int:
    expanded_text = raw.expandtabs(4)
    return len(expanded_text) - len(expanded_text.lstrip(" "))




def _parse_line(line_no: int, raw: str) -> ParsedLine:
    ast_type = _detect_unified_ast(raw)
    content = _detect_content(raw, ast_type)
    indent = _detect_indent(raw)
    return ParsedLine(line_no=line_no, raw=raw, ast_type=ast_type, content=content, indent=indent)



def parse_lines(markdown: str) -> list[ParsedLine]:
    return [
        _parse_line(line_no, line)
        for line_no, line in enumerate(
            markdown.splitlines(),
            start=1
        )
    ]


