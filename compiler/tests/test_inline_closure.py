from compiler.engine.delimiter_processor import is_closable
from compiler.entities.delimiter_run import DelimiterRun
from compiler.rules.markdown.inline_node_rules import INLINE_NODE_RULES_BY_OPENING


def test_is_closable_returns_true_when_current_run_matches_rule_closing():
    assert is_closable(
        DelimiterRun("**", 1, 0),
        DelimiterRun("**", 1, 6),
        INLINE_NODE_RULES_BY_OPENING,
    )


def test_is_closable_returns_false_for_different_closing_token():
    assert not is_closable(
        DelimiterRun("*", 1, 0),
        DelimiterRun("**", 1, 6),
        INLINE_NODE_RULES_BY_OPENING,
    )


def test_is_closable_returns_false_for_middle_delimiter():
    assert not is_closable(
        DelimiterRun("[", 1, 0),
        DelimiterRun("](", 1, 5),
        INLINE_NODE_RULES_BY_OPENING,
    )


def test_is_closable_returns_false_for_different_delimiter():
    assert not is_closable(
        DelimiterRun("**", 1, 0),
        DelimiterRun("`", 1, 6),
        INLINE_NODE_RULES_BY_OPENING,
    )
