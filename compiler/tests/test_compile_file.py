from compiler.compile_file import compile_file
from compiler.entities.doc_nodes import Heading
from compiler.entities.inline_nodes import Text


def test_compile_file_reads_markdown_from_path(tmp_path):
    path = tmp_path / "source.md"
    path.write_text("# From file\n", encoding="utf-8")

    document = compile_file(path)

    assert len(document.doc_children) == 1
    assert isinstance(document.doc_children[0], Heading)
    assert document.doc_children[0].inline_children == [Text(content="From file")]
