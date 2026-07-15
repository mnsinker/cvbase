from compiler.compile_markdown import compile_markdown
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, Heading, Paragraph
from compiler.entities.inline_nodes import Text
from compiler.entities.value_format import ValueFormat


def test_compile_markdown_returns_document_for_empty_input():
    document = compile_markdown("")

    assert isinstance(document, Document)
    assert document.doc_children == []


def test_compile_markdown_compiles_heading_and_paragraph_tree():
    document = compile_markdown("# Title\nBody")

    assert isinstance(document, Document)
    assert len(document.doc_children) == 1
    heading = document.doc_children[0]
    assert isinstance(heading, Heading)
    assert heading.inline_children == [Text(content="Title")]
    assert len(heading.doc_children) == 1
    assert isinstance(heading.doc_children[0], Paragraph)
    assert heading.doc_children[0].inline_children == [Text(content="Body")]


def test_compile_markdown_applies_annotation_pass_when_config_is_supplied():
    config = AnnotationConfig(key="career_spine", value_format=ValueFormat.LIST)

    document = compile_markdown("Career Spine: craft, leadership", annotation_config=config)

    assert document.doc_children == []
    assert len(document.annotations) == 1
    assert document.annotations[0].key == "career_spine"
    assert document.annotations[0].value == ["craft", "leadership"]
