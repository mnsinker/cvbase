from compiler.entities.document_nodes import Document, FrontMatter, Heading, Paragraph, ListItem, QuoteBlock, CodeBlock, MathBlock, Table, Row, Cell, HorizontalRule
from compiler.entities.inline_nodes import Text, Strong, Italic, Strike, Underline, Image, Link, InlineMath, InlineCode

ALL_DOCUMENT_NODES = {Document, FrontMatter, Heading, Paragraph, ListItem, QuoteBlock, CodeBlock, MathBlock, Table, Row, Cell, HorizontalRule}
ALL_INLINE_NODES = {Text, Strong, Italic, Strike, Underline, Image, Link, InlineMath, InlineCode}

"""
which node may contain which nodes.
"""
DOCNODE_DOCNODE_RULES: dict[type, set[type]] = {
    Document: ALL_DOCUMENT_NODES,

    Heading: ALL_DOCUMENT_NODES - {FrontMatter},
    Paragraph: set(),
    ListItem: ALL_DOCUMENT_NODES - {FrontMatter, Heading, HorizontalRule},

    Table: {Row},
    Row: {Cell},
    Cell: ALL_DOCUMENT_NODES - {FrontMatter},

    CodeBlock: set(),
    MathBlock: set(),
    QuoteBlock: ALL_DOCUMENT_NODES - {FrontMatter},

    HorizontalRule: set(),
    FrontMatter: set(),
}

INLINENODE_INLINENODE_RULES: dict[type, set[type]] = {
    Text: set(),
    Strong: ALL_INLINE_NODES - {Image},
    Italic: ALL_INLINE_NODES - {Image},
    Strike: ALL_INLINE_NODES - {Image},
    Underline: ALL_INLINE_NODES - {Image},
    Link: ALL_INLINE_NODES - {Image},
    Image: set(),
    InlineMath: set(),
    InlineCode: set(),
}

DOCNODE_INLINENODE_RULES: dict[type, set[type]] = {
    Heading: ALL_INLINE_NODES,
    Paragraph: ALL_INLINE_NODES,
    ListItem: ALL_INLINE_NODES,
}

# -----------------------------------------------

STATEFUL_NODES = { # node that requires incremental construction
    FrontMatter,
    QuoteBlock,
    CodeBlock,
    MathBlock,
    Table,
    Row,
}

INTERNAL_HIERARCHY_NODES = {
    Table,
    Row,
}



def is_document_child_allowed(parent, child) -> bool:
    allowed = DOCNODE_DOCNODE_RULES.get(type(parent), set())
    return type(child) in allowed

def are_document_children_allowed(parent, children) -> bool:
    return all(is_document_child_allowed(parent, child) for child in children)

def is_inline_child_allowed(parent, child) -> bool:
    allowed = DOCNODE_INLINENODE_RULES.get(type(parent), set())
    return type(child) in allowed

def are_inline_children_allowed(parent, children) -> bool:
    return all(is_inline_child_allowed(parent, child) for child in children)