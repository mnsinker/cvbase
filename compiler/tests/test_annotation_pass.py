from compiler.annotations.annotation_pass import annotation_pass
from compiler.entities.doc_nodes import Document, Paragraph
from compiler.entities.inline_nodes import Text


def paragraph(text: str, children=None) -> Paragraph:
    return Paragraph(
        inline_children=[Text(content=text)],
        doc_children=children or [],
    )


def test_annotation_pass_extracts_single_line_list_annotation():
    annotation_node = paragraph("Career Spine: craft, leadership")
    document = Document(doc_children=[annotation_node, paragraph("Visible")])

    result = annotation_pass(document)

    assert result is document
    assert document.doc_children == [paragraph("Visible")]
    assert len(document.annotations) == 1
    assert document.annotations[0].key == "career_spine"
    assert document.annotations[0].value == ["craft", "leadership"]


def test_annotation_pass_extracts_multiline_list_annotation_from_subtree():
    annotation_node = paragraph(
        "Career Spine:",
        children=[paragraph("craft"), paragraph("leadership")],
    )
    document = Document(doc_children=[annotation_node])

    annotation_pass(document)

    assert document.doc_children == []
    assert len(document.annotations) == 1
    assert document.annotations[0].value == ["craft", "leadership"]


def test_annotation_pass_extracts_boolean_annotation():
    annotation_node = paragraph("Excluded Visibility: false")
    document = Document(doc_children=[annotation_node])

    annotation_pass(document)

    assert document.doc_children == []
    assert len(document.annotations) == 1
    assert document.annotations[0].key == "excluded_visibility"
    assert document.annotations[0].value is False


def test_annotation_pass_extracts_adjacent_annotations():
    first = paragraph("Career Spine: craft")
    second = paragraph("Excluded Visibility: false")
    document = Document(doc_children=[first, second])

    annotation_pass(document)

    assert document.doc_children == []
    assert [annotation.key for annotation in document.annotations] == [
        "career_spine",
        "excluded_visibility",
    ]
