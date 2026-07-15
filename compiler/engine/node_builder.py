import re
from typing import Iterator
from compiler.engine.inline_parser import parse_inline_children
from compiler.entities.doc_nodes import DocNode
from compiler.entities.node_rules import DocNodeRule
from compiler.entities.parsed_line import ParsedLine
from compiler.entities.parsed_node import ParsedNode
from compiler.rules.markdown.doc_node_rules import SORTED_DOC_NODE_RULES, DOC_NODE_RULES_BY_TYPE

""" stateful + inline """

def _match_predicates(pl: ParsedLine, rule: DocNodeRule) -> bool:
    return all(predicate(pl) for predicate in rule.predicates)

def _match_opening_patterns(pl: ParsedLine, rule: DocNodeRule) -> re.Match | None:
    for pattern in rule.opening_patterns:
        match = pattern.match(pl.content)
        if match:
            return match
    return None

def _lookup_rule(node: DocNode) -> DocNodeRule:
    return DOC_NODE_RULES_BY_TYPE[type(node)]

def _is_closing(node: DocNode, pl: ParsedLine) -> bool:
    rule = _lookup_rule(node)
    return any(pattern.match(pl.content) for pattern in rule.closing_patterns)



def build_doc_node(rule: DocNodeRule, match: re.Match) -> DocNode:
    # 1. extract attributes
    attributes = {attr_name: attr_value(match) for attr_name, attr_value in rule.attribute_extractors.items()}
    # 2. build doc_node
    document_node = rule.node_type(**attributes)
    # 3. add inline_children
    if rule.allow_inline and rule.inline_content:
        document_node.inline_children = parse_inline_children(rule.inline_content(match))

    return document_node


def build_parsed_nodes(lines: Iterator[ParsedLine]) -> Iterator[ParsedNode]:
    stateful_stack: list [DocNode] = []
    for pl in lines:
        # 1. handle stateful in stack
        if stateful_stack:
            current_state = stateful_stack[-1]
            if _is_closing(current_state, pl):
                stateful_stack.pop()
                yield ParsedNode(line_no=pl.line_no, indent=pl.indent, doc_node=current_state)
                continue
            rule = _lookup_rule(current_state)
            rule.stateful_append(current_state, pl)
            continue

        # 2. handle normal doc_node
        for rule in SORTED_DOC_NODE_RULES:
            # 2.1 match
            if not _match_predicates(pl, rule):
                continue
            match = _match_opening_patterns(pl, rule)
            if match is None:
                continue

            # 2.2 build doc_node
            doc_node = build_doc_node(rule, match)

            # 2.3 check whether this node is stateful
            if rule.stateful_append is not None:
                stateful_stack.append(doc_node)
                break
            yield ParsedNode(line_no=pl.line_no, indent=pl.indent, doc_node=doc_node)
            break