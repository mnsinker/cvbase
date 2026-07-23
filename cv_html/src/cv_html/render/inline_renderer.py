from cv_html.entities.inline import TextNode, StrongNode, ItalicNode, LinkNode, CVInlineNode, RichText

# step 3. render different type of inline nodes
def render_inline_node(node: CVInlineNode) -> str:
    if isinstance(node, TextNode):
        return node.text
    if isinstance(node, StrongNode):
        return f"<strong>{render_inline_children(node.inline_children)}</strong>"
    if isinstance(node, ItalicNode):
        return f"<em>{render_inline_children(node.inline_children)}</em>"
    if isinstance(node, LinkNode):
        return f'<a href="{node.url}">{node.title}</a>'
    raise ValueError(f"Unsupported cv inline node: {type(node)}")

# step 2. call render nodes + join results
def render_inline_children(inline_nodes: list[CVInlineNode]) -> str:
    return "".join(render_inline_node(inline_node) for inline_node in inline_nodes)

# step 1. entrance
def render_rich_text(rich_text: RichText) -> str:
    return render_inline_children(rich_text.nodes)
