from compiler.rules.markdown.inline_node_rules import SPLIT_RULES


def validate_split_rules(split_rules):
    for delimiter, rules in split_rules.items():
        keys = list(rules.keys())

        if not keys:
            raise ValueError(f"{delimiter} has empty split rules")

        max_key = max(keys)

        if max_key not in rules:
            raise ValueError(f"{delimiter}: max_key missing strategy")



def validate_compiler_rules():
    validate_split_rules(SPLIT_RULES)