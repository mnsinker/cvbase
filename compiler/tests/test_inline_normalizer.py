from compiler.engine.delimiter_processor import normalize_delimiters
from compiler.entities.delimiter_run import DelimiterRun
from compiler.rules.markdown.inline_node_rules import SPLIT_RULES


def test_normalize_delimiters_splits_single_star_runs_by_rule():
    normalized = normalize_delimiters([DelimiterRun("*", 3, 4)], SPLIT_RULES)

    assert [(run.delimiter, run.count, run.start) for run in normalized] == [
        ("*", 2, 4),
        ("*", 1, 6),
    ]


def test_normalize_delimiters_keeps_runs_without_split_rule():
    run = DelimiterRun("~", 2, 3)

    assert normalize_delimiters([run], SPLIT_RULES) == [run]


def test_normalize_delimiters_handles_quotient_and_remainder():
    normalized = normalize_delimiters([DelimiterRun("*", 5, 0)], SPLIT_RULES)

    assert [(run.delimiter, run.count, run.start) for run in normalized] == [
        ("*", 2, 0),
        ("*", 1, 2),
        ("*", 2, 3),
    ]


def test_normalize_delimiters_returns_empty_input():
    assert normalize_delimiters([], SPLIT_RULES) == []


def test_normalize_delimiters_keeps_middle_delimiter():
    run = DelimiterRun("](", 1, 3)

    assert normalize_delimiters([run], SPLIT_RULES) == [run]


def test_normalize_delimiters_keeps_closing_parenthesis():
    run = DelimiterRun(")", 1, 10)

    assert normalize_delimiters([run], SPLIT_RULES) == [run]
