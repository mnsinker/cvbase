from compiler.engine.delimiter_processor import scan_delimiters
from compiler.rules.markdown.inline_node_rules import SORTED_DELIMITERS


def test_scan_delimiters_finds_known_delimiters_in_source_order():
    runs = scan_delimiters("a **bold** and `code`", SORTED_DELIMITERS)

    assert [(run.delimiter, run.count, run.start) for run in runs] == [
        ("**", 1, 2),
        ("**", 1, 8),
        ("`", 1, 15),
        ("`", 1, 20),
    ]

def test_scan_delimiters_prefers_longest_matching_delimiter():
    runs = scan_delimiters(
        "![alt](src) [text](url)",
        SORTED_DELIMITERS,
    )

    assert [(run.delimiter, run.count, run.start) for run in runs] == [
        ("![", 1, 0),
        ("](", 1, 5),
        (")", 1, 10),
        ("[", 1, 12),
        ("](", 1, 17),
        (")", 1, 22),
    ]


def test_scan_delimiters_coalesces_repeated_single_character_delimiters():
    runs = scan_delimiters("***text***", SORTED_DELIMITERS)

    assert [(run.delimiter, run.count, run.start) for run in runs] == [
        ("**", 1, 0),
        ("*", 1, 2),
        ("**", 1, 7),
        ("*", 1, 9),
    ]

def test_scan_delimiters_scans_opening_middle_and_closing():
    runs = scan_delimiters("[text](url)", SORTED_DELIMITERS)

    assert [run.delimiter for run in runs] == [
        "[",
        "](",
        ")",
    ]


def test_scan_delimiters_returns_empty_for_plain_text():
    assert scan_delimiters("abcdef", SORTED_DELIMITERS) == []


def test_scan_delimiters_scans_delimiter_at_beginning():
    runs = scan_delimiters("**abc", SORTED_DELIMITERS)

    assert [(run.delimiter, run.count, run.start) for run in runs] == [
        ("**", 1, 0),
    ]


def test_scan_delimiters_scans_delimiter_at_end():
    runs = scan_delimiters("abc**", SORTED_DELIMITERS)

    assert [(run.delimiter, run.count, run.start) for run in runs] == [
        ("**", 1, 3),
    ]


def test_scan_delimiters_scans_only_known_delimiters():
    assert scan_delimiters("abc@@@def", SORTED_DELIMITERS) == []
