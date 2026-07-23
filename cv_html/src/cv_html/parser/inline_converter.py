from compiler.api.query import get_text
from cv_html.entities.inline import RichText, TextNode, StrongNode, ItalicNode, LinkNode, CVInlineNode
from compiler.entities.inline_nodes import (
    InlineNode as CompilerInlineNode,
    Text as CompilerTextNode,
    Strong as CompilerStrongNode,
    Italic as CompilerItalicNode,
    Link as CompilerLinkNode,
)

def convert_inline_node(inline_node: CompilerInlineNode) -> CVInlineNode:
    if isinstance(inline_node, CompilerTextNode):
        return TextNode(text=inline_node.content)
    if isinstance(inline_node, CompilerStrongNode):
        return StrongNode(inline_children=[convert_inline_node(child) for child in inline_node.inline_children])  # recursive
    if isinstance(inline_node, CompilerItalicNode):
        return ItalicNode(inline_children=[convert_inline_node(child) for child in inline_node.inline_children])  # recursive
    if isinstance(inline_node, CompilerLinkNode):
        return LinkNode(title=get_text(inline_node), url=inline_node.url)
    raise ValueError(f"Unsupported compiler inline node: {type(inline_node)}")


def convert_rich_text(inline_nodes: list[CompilerInlineNode]) -> RichText:
    return RichText(nodes=[convert_inline_node(inline_node) for inline_node in inline_nodes])