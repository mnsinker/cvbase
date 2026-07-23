from compiler.engine.delimiter_processor import scan_delimiters, normalize_delimiters, is_closable, is_opening
from compiler.entities.delimiter_match import DelimiterMatch
from compiler.entities.delimiter_run import DelimiterRun
from compiler.entities.inline_nodes import InlineNode, Text
from compiler.rules.markdown.inline_node_rules import INLINE_NODE_RULES_BY_OPENING, SPLIT_RULES, \
    MIDDLE_DELIMITERS, SORTED_DELIMITERS


def _build_delimiter_match(opening:DelimiterRun, closing:DelimiterRun, remaining:str, rule_map:dict) -> DelimiterMatch:
    opening_delimiter = opening.delimiter * opening.count
    rule = rule_map[opening_delimiter]
    # 1. left
    left = remaining[:opening.start]

    # 2. inline_node & inline_content & attribute content if middle
    inline_node = rule.node_type()
    raw_content = remaining[opening.start+len(opening_delimiter) : closing.start]
    if rule.middle:
        inline_content, attribute_text = raw_content.rsplit(rule.middle, maxsplit=1)
        for attribute, extractor in rule.attribute_extractors.items():
            setattr(inline_node, attribute, extractor(attribute_text))
    else:
        inline_content = raw_content

    # 3. right
    right = remaining[closing.start+len(closing.delimiter):]
    return DelimiterMatch(left, inline_node, inline_content, right)



def _find_first_inline(remaining: str) -> DelimiterMatch | None:
    """ return: DelimiterMatch(left, inline_node, inline_content, right) """
    # ⭐️ 1. scan
    delimiter_runs = scan_delimiters(remaining, SORTED_DELIMITERS)
    # ⭐️ 2. normalize (split repeat delimiters)
    delimiter_runs = normalize_delimiters(delimiter_runs, SPLIT_RULES)
    # ⭐️ 3. pair
    stack: list[DelimiterRun] = []
    match: DelimiterMatch | None = None
    for run in delimiter_runs:
        # 1. deal with middle delimiter
        if run.delimiter in MIDDLE_DELIMITERS:
            continue

        # 2. deal with opening delimiter: 1st opening delimiter
        if not stack:
            if is_opening(run, INLINE_NODE_RULES_BY_OPENING):
                stack.append(run)
            continue

        # 3. deal with closing delimiter: check & match
        last_run = stack[-1]
        if is_closable(last_run, run, INLINE_NODE_RULES_BY_OPENING):
            stack.pop()
            match = _build_delimiter_match(last_run, run, remaining, INLINE_NODE_RULES_BY_OPENING)
            if not stack:
                return match
            continue

        stack.append(run)
        continue

    return match


def parse_inline_children(remaining: str) -> list[InlineNode]:
    if not remaining:
        return []

    inline_children: list[InlineNode] = []
    delimiter_match = _find_first_inline(remaining)

    # 0. handle no inline_node
    if delimiter_match is None:
        return [Text(content=remaining)]

    # 1. handle left
    if delimiter_match.left:
        inline_children.append(Text(content=delimiter_match.left))

    # 2. handle inline - recursive
    delimiter_match.inline_node.inline_children.extend(parse_inline_children(delimiter_match.inline_content))
    inline_children.append(delimiter_match.inline_node)

    # 3. handle right - recursive
    inline_children.extend(parse_inline_children(delimiter_match.right))

    return inline_children