from compiler.engine.line_parser import parse_lines


def test_parse_lines_preserves_raw_content_indent_and_line_numbers():
    lines = list(parse_lines("# Title\n  indented\n\n\tmixed"))

    assert [line.line_no for line in lines] == [1, 2, 3, 4]
    assert [line.raw for line in lines] == ["# Title", "  indented", "", "\tmixed"]
    assert [line.indent for line in lines] == [0, 2, 0, 1]
    assert [line.content for line in lines] == ["# Title", "indented", "", "mixed"]


def test_parse_lines_returns_no_items_for_empty_markdown():
    assert list(parse_lines("")) == []
