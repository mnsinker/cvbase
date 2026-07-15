import re
from compiler.entities.node_rules import DocNodeRule
from compiler.entities.doc_nodes import FrontMatter, Heading, Paragraph, ListItem, CodeBlock, \
    MathBlock, HorizontalRule

# ===================================================

DOC_NODE_RULES = [
    DocNodeRule(
        node_type=FrontMatter,
        order=1000,
        opening_patterns=[re.compile(r"^---\s*$")],
        closing_patterns=[re.compile(r"^---\s*$")],
        predicates=[lambda pl: pl.line_no == 1],
        stateful_append=lambda node, pl: node.content.append(pl.content),
        attribute_extractors={}
    ),
    DocNodeRule(
        node_type=HorizontalRule,
        order=900,
        opening_patterns=[re.compile(r"^---\s*$")],
    ),
    DocNodeRule(
        node_type=Heading,
        order=800,
        opening_patterns=[re.compile(r"^(?P<opening>#{1,6})\s+(?P<content>.*)$")],
        allow_inline=True,
        excluded_doc_children={FrontMatter},
        attribute_extractors={"level": lambda m: len(m.group("opening"))},
        inline_content=lambda m: m.group("content")
    ),
    DocNodeRule(
        node_type=ListItem,
        order=700,
        opening_patterns=[
            re.compile(r"^(?P<label>[-+*✓])\s+(?P<content>.*)$"),
            re.compile(r"^(?P<label>\d+|[A-Za-z])\.\s+(?P<content>.*)$"),
            re.compile(r"^(?P<label>[✅👉⭐️📌])\s+(?P<content>.*)$")
        ],
        allow_inline=True,
        excluded_doc_children={FrontMatter, Heading, HorizontalRule},
        attribute_extractors={"label": lambda m: m.group("label")},
        inline_content=lambda m: m.group("content")
    ),
    # NodeRule( # todo (v2)
    #     node_type=QuoteBlock,
    #     order=690,
    #     opening_patterns=[re.compile(r"^>\s+(.*)$")],
    #     excluded_children={FrontMatter, Row, Cell},
    #     stateful_append=lambda node, pl: node.document_children.append(pl),
    # ),
    DocNodeRule(
        node_type=CodeBlock,
        order=680,
        opening_patterns=[re.compile(r"^```(?!math)(?P<language>.*)$")],
        closing_patterns=[re.compile(r"^```\s*$")],
        stateful_append=lambda node, pl: node.content.append(pl.content),
        attribute_extractors={
            "language": lambda m: m.group("language").strip(),
        }
    ),
    DocNodeRule(
        node_type=MathBlock,
        order=670,
        opening_patterns=[
            re.compile(r"^\$\$\s*$"),
            re.compile(r"^```math\s*$")
        ],
        closing_patterns=[
            re.compile(r"^\$\$\s*$"),
            re.compile(r"^```\s*$"),
        ],
        stateful_append=lambda node, pl: node.content.append(pl.content),
        attribute_extractors={}
    ),
    # DocNodeRule(# todo (v2)
    #     node_type=Table,
    #     order=590,
    #     opening_patterns=[re.compile(r"^\|.*\|$")],
    #     stateful_append=lambda node, item: node.document_children.append(item), # item = child_node
    #     excluded_doc_children=ALL_DOCUMENT_NODES - {Row},
    # ),
    DocNodeRule(
        node_type=Paragraph,
        opening_patterns=[re.compile(r"^(?P<content>.*)$")], # fallback
        order=0,
        allow_inline=True,
        excluded_doc_children={FrontMatter, Heading, HorizontalRule},
        inline_content=lambda m: m.group("content")
    ),
]

SORTED_DOC_NODE_RULES = sorted(DOC_NODE_RULES, key=lambda rule: rule.order, reverse=True)
DOC_NODE_RULES_BY_TYPE = {rule.node_type: rule for rule in DOC_NODE_RULES}
