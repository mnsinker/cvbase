from math import inf
from compiler.entities.node import Node
from compiler.entities.parsed_line import ParsedLine
from compiler.entities.unified_ast import UnifiedAST

def _get_heading_level(ast_type: UnifiedAST) -> int | float:
    if ast_type == UnifiedAST.H1:
        return 1
    if ast_type == UnifiedAST.H2:
        return 2
    if ast_type == UnifiedAST.H3:
        return 3
    return inf


def _is_parent(current_line: ParsedLine, previous_line: ParsedLine) -> bool:
    if _get_heading_level(previous_line.ast_type) < _get_heading_level(current_line.ast_type):
        return True
    if previous_line.indent < current_line.indent:
        return True
    if previous_line.ast_type != UnifiedAST.BULLET and current_line.ast_type == UnifiedAST.BULLET:
        return True
    return False


def build_node_tree(parsed_lines: list[ParsedLine]) -> list[Node]:
    roots: list[Node] = []
    stack: list[tuple[ParsedLine, Node]] = [] # 因为需要 line.indent 的信息, 所以把 ParsedLine 加进去

    for current_line in parsed_lines:
        # 0. 过滤掉 blank line
        if current_line.ast_type == UnifiedAST.BLANK_LINE:
            continue

        # 1. find parent:
        current_node = Node(ast_type=current_line.ast_type, content=current_line.content)
        while stack:
            previous_line = stack[-1][0]
            if _is_parent(current_line, previous_line):
                break
            stack.pop() # if not current's parent, then pop.

        # 2. append to tree
        if stack:
            stack[-1][1].children.append(current_node)
        else:
            roots.append(current_node)

        # 3. append to stack
        stack.append((current_line, current_node))

    return roots
