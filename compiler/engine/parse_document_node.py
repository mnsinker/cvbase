import re
from typing import Tuple
from compiler.entities.parser_context import ParserContext
from compiler.entities.document_nodes import DocumentNode, Heading, FrontMatter, ListItem, HorizontalRule, Paragraph, \
    QuoteBlock, CodeBlock, MathBlock, Table, Row, Cell


def _parse_frontmatter(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    if ctx.line_no == 1 and ctx.raw.strip() == "---":
        return FrontMatter(), ""
    return None, ctx.raw

def _parse_horizontal_rule(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    if ctx.raw.strip() == "---":
        return HorizontalRule(), ""
    return None, ctx.raw

# -----------------------------------------------

def _parse_heading(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    match = re.match(r"^(#{1,6})\s+(.*)$", ctx.raw)
    if not match:
        return None, ctx.raw
    level = len(match.group(1))
    remaining = match.group(2)
    return Heading(level=level), remaining

def _parse_paragraph(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    return Paragraph(), ctx.raw

def _parse_bullet_list_item(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    match = re.match(r"^([-+*✓])\s+(.*)$", ctx.raw)
    if not match:
        return None, ctx.raw
    label = match.group(1)
    remaining = match.group(2)
    return ListItem(label=label), remaining

def _parse_ordered_list_item(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    match = re.match(r"^(\d+|[A-Za-z])\.\s+(.*)$", ctx.raw)
    if not match:
        return None, ctx.raw
    label = match.group(1)
    remaining = match.group(2)
    return ListItem(label=label), remaining

ICON_LIST_LABELS = {"✅", "👉", "⭐️", "📌"}
def _parse_icon_list_item(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    stripped = ctx.raw.strip()
    for icon in ICON_LIST_LABELS:
        if stripped.startswith(icon + " "):
            remaining = stripped.removeprefix(icon).strip()
            return ListItem(label=icon),remaining
    return None, ctx.raw

LIST_ITEM_PARSERS = [_parse_bullet_list_item, _parse_ordered_list_item, _parse_icon_list_item]
def _parse_list_item(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    for parser_func in LIST_ITEM_PARSERS:
        list_item_node, remaining = parser_func(ctx)
        if list_item_node is not None:
            return list_item_node, remaining
    return None, ctx.raw

# ----------------------------------------------------

def _parse_quote_block(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    stripped = ctx.raw.lstrip()
    if stripped.startswith("> "):
        remaining = stripped.removeprefix("> ")
        return QuoteBlock(), remaining
    return None, ctx.raw

def _parse_code_block(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    if ctx.raw.startswith("```") and not ctx.raw.startswith("```math"):
        language = ctx.raw.removeprefix("```")
        return CodeBlock(language=language), ""
    return None, ctx.raw

def _parse_math_block(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    if ctx.raw.strip() == "$$" or ctx.raw.startswith("```math"):
        return MathBlock(), ""
    return None, ctx.raw


# ----------------------------------------------------------

def _parse_table(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    stripped = ctx.raw.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None, ctx.raw
    return Table(), stripped

def _parse_row(ctx: ParserContext) -> Tuple[DocumentNode | None, list[str]]:
    stripped = ctx.raw.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None, []
    remaining = stripped[1:-1]
    cell_contents = [cell.strip() for cell in remaining.split("|")]
    return Row(), cell_contents

def _parse_cell(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    stripped = ctx.raw.strip()
    match = re.match(r"^|(.+)|$", stripped)
    if not match:
        return None, ctx.raw
    remaining = stripped[1:-2]
    return Cell(), ctx.raw

# ------------------------------------------------------------

DOCUMENT_NODE_PARSERS = [
    _parse_frontmatter,
    _parse_horizontal_rule,

    _parse_heading,
    _parse_list_item,

    _parse_quote_block,
    _parse_code_block,
    _parse_math_block,

    _parse_paragraph,
]

def parse_document_node(ctx: ParserContext) -> Tuple[DocumentNode | None, str]:
    for parser_func in DOCUMENT_NODE_PARSERS:
        document_node, remaining = parser_func(ctx)
        if document_node is not None:
            return document_node, remaining
    return _parse_paragraph(ctx)
