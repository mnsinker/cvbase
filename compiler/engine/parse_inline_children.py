import re
from typing import Tuple
from compiler.entities.document_nodes import DocumentNode
from compiler.entities.inline_nodes import InlineNode, Image, Text, Strong, Italic, Link, Underline, Strike, InlineMath, \
    InlineCode
from compiler.rules.markdown_rule import DOCNODE_INLINENODE_RULES, INLINENODE_INLINENODE_RULES


def _detect_strong(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    """ return:
            - inline_node
            - inline_content stripped of token symbols (eg. hello, not **hello**)
            - consumed_len: len(**hello**) = 9   """

    opening_token = closing_token = "**"
    i = len(opening_token)
    while i < len(remaining):
        # skip escaped characters "\\"
        if remaining[i] == "\\":
            i += 2
            continue
        if remaining.startswith(closing_token, i):
            content = remaining[len(opening_token):i].strip()
            consumed_len = i+len(closing_token)
            return Strong(), content, consumed_len
        i += 1
    return None, None, None

def _detect_italic(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = closing_token = "*"
    i = len(opening_token)
    while i < len(remaining):
        if remaining[i] == "\\":
            i += 2
            continue
        if remaining.startswith(closing_token, i):
            content = remaining[len(opening_token):i].strip()
            consumed_len = i + len(closing_token)
            return Italic(), content, consumed_len
        i += 1
    return None, None, None

def _detect_strike(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = "~~"
    closing_token = "~~"
    i = len(opening_token)
    while i < len(remaining):
        if remaining[i] == "\\":
            i += 2
            continue
        if remaining.startswith(closing_token, i):
            content = remaining[len(opening_token):i].strip()
            consumed_len = i + len(closing_token)
            return Strike(), content, consumed_len
        i += 1
    return None, None, None

def _detect_underline(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = "<u>"
    closing_token = "</u>"
    i = len(opening_token)
    while i < len(remaining):
        if remaining[i] == "\\":
            i += 2
            continue
        if remaining.startswith(closing_token, i):
            content = remaining[len(opening_token):i].strip()
            consumed_len = i + len(closing_token)
            return Underline(), content, consumed_len
        i += 1
    return None, None, None

def _detect_inline_math(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = closing_token = "$"
    i = len(opening_token)
    while i < len(remaining):
        if remaining[i] == "\\":
            i += 2
            continue
        if remaining.startswith(closing_token, i):
            content = remaining[len(opening_token):i].strip()
            consumed_len = i + len(closing_token)
            return InlineMath(), content, consumed_len
        i += 1
    return None, None, None

def _detect_inline_code(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = closing_token = "`"
    opening_len = len(opening_token)

    i = opening_len
    while i < len(remaining):
        if remaining[i] == "\\":
            i += 2
            continue
        if remaining.startswith(closing_token, i):
            content = remaining[opening_len:i].strip()
            consumed_len = i + len(closing_token)
            return InlineCode(), content, consumed_len
        i += 1
    return None, None, None

def _detect_link(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = "["
    middle_token = "]("
    closing_token = ")"
    opening_len = len(opening_token)
    middle_len = len(middle_token)
    closing_len = len(closing_token)

    i = len(opening_token)
    matched_middle = False
    middle_pos = None

    while i < len(remaining):
        # skip escaped characters "\\"
        if remaining[i] == "\\":
            i += 2
            continue
        if not matched_middle:
            if remaining.startswith(middle_token, i):
                matched_middle = True
                middle_pos = i
                i += middle_len
                continue
        else:
            if remaining.startswith(closing_token, i):
                consumed_len = i + closing_len

                # label
                label_content = remaining[opening_len:middle_pos]

                # url + optional title
                url_and_title = remaining[middle_pos + middle_len:i].strip()
                url = url_and_title
                title = ""

                title_match = re.match(r'^(.*?)\s+"(.*)"$', url_and_title)
                if title_match:
                    url = title_match.group(1).strip()
                    title = title_match.group(2)

                return Link(url=url, title=title), label_content, consumed_len  # ⭐️
        i += 1
    return None, None, None

def _detect_image(remaining: str) -> Tuple[InlineNode|None, str|None, int|None]:
    opening_token = "!["
    middle_token = "]("
    closing_token = ")"
    opening_len = len(opening_token)
    middle_len = len(middle_token)
    closing_len = len(closing_token)

    i = len(opening_token)
    matched_middle = False
    middle_pos = None

    while i < len(remaining):
        # skip escaped characters "\\"
        if remaining[i] == "\\":
            i += 2
            continue
        if not matched_middle:
            if remaining.startswith(middle_token, i):
                matched_middle = True
                middle_pos = i
                i += middle_len
                continue
        else:
            if remaining.startswith(closing_token, i):
                consumed_len = i + closing_len
                # alt
                alt = remaining[opening_len:middle_pos]
                # src + optional title
                src_and_title = remaining[middle_pos + middle_len:i].strip()
                src = src_and_title
                title = ""
                title_match = re.match(r'^(.*?)\s+"(.*)"$', src_and_title)
                if title_match:
                    src = title_match.group(1).strip()
                    title = title_match.group(2)
                return Image(alt=alt, src=src, title=title), None, consumed_len  # ⭐️
        i += 1
    return None, None, None


INLINE_TOKEN_DETECTORS = [
    ("**", _detect_strong), # return -> inline_node, matched_len
    ("*", _detect_italic),
    ("~~", _detect_strike),
    ("<u>", _detect_underline),

    ("![", _detect_image),
    ("[", _detect_link),

    ("$", _detect_inline_math),
    ("`", _detect_inline_code),
]

def _detect_first_inline_token(remaining: str) -> Tuple[str, InlineNode|None, str|None, str]:
    for start in range(len(remaining)):
        for token, detector in INLINE_TOKEN_DETECTORS:

            if remaining.startswith(token, start):
                inline_node, inline_content, consumed_len = detector(remaining[start:]) # ⭐️
                if inline_node is not None:
                    left = remaining[:start]
                    right = remaining[start+consumed_len : ]
                    return left, inline_node, inline_content, right

    return "", None, "", ""

def parse_inline_children(node: DocumentNode | InlineNode, remaining: str|None) -> list[InlineNode]:
    if type(node) not in DOCNODE_INLINENODE_RULES and type(node) not in INLINENODE_INLINENODE_RULES:
        return []

    inline_children: list[InlineNode] = []
    left, inline_node, inline_content, right = _detect_first_inline_token(remaining)

    # 0. handle no inline_node
    if inline_node is None:
        if remaining:
            inline_children.append(Text(remaining))
            return inline_children
        return []

    # 1. handle left
    if left:
        inline_children.append(Text(left))

    # 2. handle inline
    inline_node.inline_children.extend(parse_inline_children(inline_node, inline_content))
    inline_children.append(inline_node)

    # 3. handle right
    inline_children.extend(parse_inline_children(node, right))

    return inline_children