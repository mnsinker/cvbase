def scan_delimiters(remaining: str) -> list[DelimiterCandidate]:
    delimiter_candidates: list[DelimiterCandidate] = []
    rules = sorted(DELIMITER_RULES.values(), key=lambda rule: len(rule.opening), reverse=True)

    for start in range(len(remaining)):
        for rule in rules:
            if not remaining.startswith(rule.opening, start):
                continue
            count = 1

            if rule.max_repeat > 1:
                while remaining.startswith(rule.opening, start + count*len(rule.opening)):
                    count += 1

            delimiter_candidates.append(
                DelimiterCandidate(rule=rule, count=count, start=start)
            )
            break # Longest matching opening wins.

    return []
    
    
  ===========================================
  version 1: 
 def scan_delimiters(remaining: str) -> list[DelimiterCandidate]:
    delimiter_candidates: list[DelimiterCandidate] = [] # step 1 分析IO
    # step 2 拿remaining每个字符 vs DELIMITER_RULES 比对
    for start in range(len(remaining)):
        for delimiter in DELIMITER_RULES:
            if matching: # todo 3.1 if matching, 就 append to list
                rule = DELIMITER_RULES[delimiter]
                delimiter_candidates.append(DelimiterCandidate(rule, count, start))
                # todo 3.2: match 成功后, 是否要continue / break
    return delimiter_candidates # step 1

=====================
version 2: 
def scan_delimiters(remaining: str) -> list[DelimiterCandidate]:
    delimiter_candidates: list[DelimiterCandidate] = [] # step 1 分析IO
    # step 2 拿remaining每个字符 vs DELIMITER_RULES 比对
    for start in range(len(remaining)):
        for delimiter in DELIMITER_RULES:
            if remaining.startswith(delimiter, start): # step 3.1 如果 remaining 的"start"点 匹配上了 current delimiter
                count = 1 # todo 4 match上了, 至少count=1, 后续count再作为 DelimiterCandidate 的 param
                rule = DELIMITER_RULES[delimiter]
                delimiter_candidates.append(DelimiterCandidate(rule, count, start))
                break # 3.2 一旦match了, 就不要再往下match其他 delimiter 了, ie. for delimiter loop 结束, for start loop 继续; 所以rules需要按delimiter长度倒序
    return delimiter_candidates # step 1
    
======================
version 3.1
def scan_delimiters(remaining: str) -> list[DelimiterCandidate]:
    delimiter_candidates: list[DelimiterCandidate] = []
    rules = sorted(DELIMITER_RULES.values(), key=lambda delimiter_rule: len(delimiter_rule.opening), reverse=True) # 对应 原3.2

    for start in range(len(remaining)):
        for rule in rules:
            delimiter = rule.opening # 把 opening delimiter 从 rule 里取出来
            if remaining.startswith(delimiter, start):
                count = 1 # todo 4 match上了, 至少count=1, 后续count再作为 DelimiterCandidate 的 param
                # todo 5 匹配上了, 继续匹配, 看能匹配上多少个重复的 delimiter
                next_start = start + len(delimiter)
                while next_start < len(remaining):
                    if remaining.startswith(delimiter, next_start):
                        count += 1
                        next_start += len(delimiter)
                    else:
                        break
                delimiter_candidates.append(DelimiterCandidate(rule, count, start))
                break

    return delimiter_candidates
    
=====================================
version 3.2
def scan_delimiters(remaining: str) -> list[DelimiterCandidate]:
delimiter_candidates: list[DelimiterCandidate] = []
rules = sorted(DELIMITER_RULES.values(), key=lambda delimiter_rule: len(delimiter_rule.opening), reverse=True) # 对应 原3.2

for start in range(len(remaining)):
    for rule in rules:
        delimiter = rule.opening
        if remaining.startswith(delimiter, start):
            count = 1

            while remaining.startswith(delimiter, start + len(rule.opening)*count) and count < rule.max_repeat: # 相当于 startswith 本身就自带指针
                count += 1  # 匹配上了, 就count++, 继续 while loop 匹配?

            delimiter_candidates.append(DelimiterCandidate(rule, count, start))
            break

return delimiter_candidates