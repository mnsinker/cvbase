from compiler.entities.inline_nodes import InlineNode, Text


def extract_inline_text(inline_nodes: list[InlineNode]) -> str: # 1 single doc_node's inline_nodes
    texts: list[str] = []

    for node in inline_nodes:
        if isinstance(node, Text):
            texts.append(node.content)
        else:
            texts.append(
                extract_inline_text(node.inline_children)  # recursive
            )

    return "".join(texts)