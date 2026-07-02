from compiler.engine.parse_lines import parse_lines
from compiler.entities.unified_ast import UnifiedAST


def test_heading():
    md1 = "# Heading Test 1"
    parsed_line = parse_lines(md1)

    assert parsed_line[0].ast_type == UnifiedAST.H1
    assert parsed_line[0].content == "Heading Test 1"

def test_paragraph():
    md1 = "hello world"
    parsed_line = parse_lines(md1)
    assert parsed_line[0].ast_type == UnifiedAST.PARAGRAPH

def test_indent():
    md1 = """
    A
        B
    """
    parsed_lines = parse_lines(md1)
    assert parsed_lines[0].indent == 0
    assert parsed_lines[1].indent == 4

def test_code_block1():
    md_without_indent = """
Flow
```json
Exam Paper.pdf
↓
Question(stem, diagram, options, difficulty_level)
↓
Question Search | AI Question Generation | Personalized Practice
```
    """
    parsed_lines = parse_lines(md_without_indent)
    assert parsed_lines[2].ast_type == UnifiedAST.CODE_BLOCK