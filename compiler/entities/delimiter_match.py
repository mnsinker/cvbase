from dataclasses import dataclass
from compiler.entities.inline_nodes import InlineNode


@dataclass(slots=True)
class DelimiterMatch:
    left: str | None
    inline_node: InlineNode | None
    inline_content: str | None
    right: str | None