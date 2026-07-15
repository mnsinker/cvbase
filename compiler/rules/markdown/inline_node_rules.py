from compiler.entities.inline_nodes import Italic, Strong, Strike, Underline, InlineMath, InlineCode, Link, Image, Text, \
    ALL_INLINE_NODES
from compiler.entities.node_rules import InlineNodeRule

SPLIT_RULES = {
    "*": {
        1: [1],  # appearance_count : [how to split]
        2: [2],
        3: [2,1]
    },
}

# ---------------------------------------

INLINE_NODE_RULES = [
    InlineNodeRule(
        node_type=Strong,
        opening="**",
        closing="**",
        excluded_inline_children={Image}
    ),
    InlineNodeRule(
        node_type=Italic,
        opening="*",
        closing="*",
        excluded_inline_children={Image}
    ),
    InlineNodeRule(
        node_type=Strike,
        opening="~~",
        closing="~~",
        excluded_inline_children={Image}
    ),
    InlineNodeRule(
        node_type=Underline,
        opening="<u>",
        closing="</u>",
        excluded_inline_children={Image}
    ),
    InlineNodeRule(
        node_type=InlineCode,
        opening="`",
        closing="`",
        excluded_inline_children=ALL_INLINE_NODES-{Text}
    ),
    InlineNodeRule(
        node_type=InlineMath,
        opening="$",
        closing="$",
        excluded_inline_children=ALL_INLINE_NODES-{Text}
    ),
    InlineNodeRule(
        node_type=Link,
        opening="[",
        middle="](",
        closing=")",
        attribute_extractors={
            "url": lambda attr_txt: attr_txt.split('"', maxsplit=1)[0].strip(),
            "title": lambda attr_txt: (attr_txt.split('"', 1)[1].strip().strip('"')
                                if '"' in attr_txt else "")
        },
        excluded_inline_children={Image}
    ),
    InlineNodeRule(
        node_type=Image,
        opening="![",
        middle="](",
        closing=")",
        attribute_extractors={
            "src": lambda attr_txt: attr_txt.split('"', maxsplit=1)[0].strip(),
            "title": lambda attr_txt: (attr_txt.split('"', 1)[1].strip().strip('"')
                                if '"' in attr_txt else "")
        },
        excluded_inline_children={Image, Link, InlineCode, InlineMath}
    )
]

SORTED_INLINE_NODE_RULES = sorted(INLINE_NODE_RULES, key=lambda rule: len(rule.opening), reverse=True)
INLINE_NODE_RULES_BY_OPENING = {rule.opening: rule for rule in INLINE_NODE_RULES}
MIDDLE_DELIMITERS = {"](", }

SORTED_DELIMITERS = []
for rule in SORTED_INLINE_NODE_RULES:
    SORTED_DELIMITERS.append(rule.opening)
    SORTED_DELIMITERS.append(rule.closing)
    if rule.middle:
        SORTED_DELIMITERS.append(rule.middle)
SORTED_DELIMITERS = sorted(set(SORTED_DELIMITERS), key=len, reverse=True)
