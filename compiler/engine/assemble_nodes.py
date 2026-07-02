import re
from compiler.engine.parse_document_node import parse_document_node
from compiler.engine.parse_inline_children import parse_inline_children
from compiler.entities.parsed_node import ParsedNode
from compiler.entities.pending_node import PendingNode
from compiler.rules.markdown_rule import STATEFUL_NODES


def _detect_indent(raw: str) -> int:
    expanded_text = raw.expandtabs(4)
    return len(expanded_text) - len(expanded_text.lstrip(" "))


def parse_nodes(markdown: str):
    stack = []
    for line_no, line in enumerate(markdown.splitlines(), start=1):
        if stack:
            current_pending = stack[-1]
            if is_end_symbol(current_pending, line):
                document_node = finish_pending_node(current_pending)
                stack.pop()
                yield ParsedNode(line_no=current_pending.start_line_no, indent=current_pending.indent, document_node=document_node)
                continue
            stack[-1].lines.append(line)
            continue
        # ------------------------------------------------
        indent = _detect_indent(line)
        document_node, remaining = parse_document_node(line, line_no)

        if type(document_node) in STATEFUL_NODES:
            stack.append(PendingNode(start_line_no=line_no, indent=indent, document_node=document_node, lines=[]))
            continue
        # --------------------------------------------------
        inline_children = parse_inline_children(document_node, remaining)
        document_node.inline_children.extend(inline_children)

        """
        document_children = parse_internal_children(document_node)
        document_node.document_children.extend(document_children)
        """

        yield ParsedNode(line_no=line_no, indent=indent, document_node=document_node)





