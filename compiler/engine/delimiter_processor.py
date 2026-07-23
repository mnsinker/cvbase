from compiler.entities.delimiter_run import DelimiterRun


def scan_delimiters(remaining: str, sorted_delimiters: list[str]) -> list[DelimiterRun]:
    delimiter_runs: list[DelimiterRun] = []
    start = 0
    while start < len(remaining):
        matched = False
        # 1. scan delimiter
        for delimiter in sorted_delimiters:
            # 1.1 if delimiter is not matched, then continue (outer loop continues, ie continue match next char)
            if not remaining.startswith(delimiter, start):
                continue

            # 1.2 if delimiter is matched, then:
            # 1) count=1
            # 2) check whether next char is the same as previous char
            count = 1
            while remaining.startswith(delimiter, start + len(delimiter)*count):
                count += 1

            delimiter_runs.append(DelimiterRun(delimiter, count, start))
            start += len(delimiter)*count
            matched = True
            break

        if not matched:
            start += 1

    return delimiter_runs


def normalize_delimiters(runs: list[DelimiterRun], split_rules: dict) -> list[DelimiterRun]:
    normalized_runs = []
    for run in runs:
        count = run.count

        # CASE: need split
        split_options = split_rules.get(run.delimiter)
        # no split rule - fallback: keep original
        if not split_options:
            normalized_runs.append(run)
            continue

        # choose the largest strategy key
        max_key = max(split_options.keys())
        chosen_split = split_options.get(max_key)

        group_num, remainder = divmod(count, max_key)
        # 1 handel quotient
        split_plan = chosen_split * group_num
        # 2 handel remainder
        if remainder:
            split_plan.append(remainder)

        # build runs
        start = run.start
        for split_num in split_plan:
            normalized_runs.append(
                DelimiterRun(
                    delimiter=run.delimiter,
                    count=split_num,
                    start=start
                )
            )
            start += split_num * len(run.delimiter)

    return normalized_runs



def is_closable(last_run, current_run, rule_map) -> bool:
    opening_token = last_run.delimiter * last_run.count
    rule = rule_map[opening_token]
    if not rule:
        return False
    return current_run.delimiter == rule.closing

def is_opening(run:DelimiterRun, rule_map) -> bool:
    token = run.delimiter * run.count
    return token in rule_map

