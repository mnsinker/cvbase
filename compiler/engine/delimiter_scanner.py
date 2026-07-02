from compiler.entities.delimiter_run import DelimiterRun
"""
@dataclass
class DelimiterRun:
    delimiter: str
    count: int
"""
RUN_DELIMITER = {"*", "~"}
STRUCTURED_DELIMITER = {
"[",
"![",
"<u>",
"$",
"`",
"}",
}

def scan_delimiter_run(remaining: str) -> DelimiterRun:
    delimiter = ""
    count = 0
    return DelimiterRun(delimiter=delimiter, count=count)