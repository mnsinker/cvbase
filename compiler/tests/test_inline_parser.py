from compiler.engine.inline_parser import parse_inline_children
from compiler.entities.inline_nodes import InlineCode, Italic, Strong, Text, InlineMath, Link, Image


def test_parse_inline_children_returns_single_text_node_without_delimiters():
    children = parse_inline_children("plain text")

    assert children == [Text(content="plain text")]


def test_parse_inline_children_parses_single_character_inline_node():
    children = parse_inline_children("before *em* after")

    assert isinstance(children[0], Text)
    assert children[0].content == "before "
    assert isinstance(children[1], Italic)
    assert children[1].inline_children == [Text(content="em")]
    assert children[2] == Text(content=" after")


def test_parse_inline_children_parses_code_span():
    children = parse_inline_children("use `x = 1` now")

    assert children[0] == Text(content="use ")
    assert isinstance(children[1], InlineCode)
    assert children[1].inline_children == [Text(content="x = 1")]
    assert children[2] == Text(content=" now")


def test_parse_inline_children_parses_strong_without_leaking_delimiter_text():
    children = parse_inline_children("before **strong** after")

    assert children[0] == Text(content="before ")
    assert isinstance(children[1], Strong)
    assert children[1].inline_children == [Text(content="strong")]
    assert children[2] == Text(content=" after")

def test_parse_inline_children_parses_inline_math():
    children = parse_inline_children("before $x+y$ after")

    assert children[0] == Text(content="before ")
    assert isinstance(children[1], InlineMath)
    assert children[1].inline_children == [Text(content="x+y")]
    assert children[2] == Text(content=" after")

def test_parse_inline_children_parses_nested_inline_code_inside_strong():
    children = parse_inline_children("**before `code` after**")

    assert len(children) == 1
    assert isinstance(children[0], Strong)

    assert children[0].inline_children == [
        Text(content="before "),
        InlineCode(
            inline_children=[
                Text(content="code")
            ]
        ),
        Text(content=" after"),
    ]

def test_parse_inline_children_parses_nested_strong_inside_italic():
    children = parse_inline_children("*before **strong** after*")

    assert len(children) == 1
    assert isinstance(children[0], Italic)

    assert children[0].inline_children == [
        Text(content="before "),
        Strong(
            inline_children=[
                Text(content="strong")
            ]
        ),
        Text(content=" after"),
    ]

def test_parse_inline_children_parses_multiple_inline_nodes():
    children = parse_inline_children(
        "A *italic* B `code` C **strong** D"
    )

    assert children == [
        Text(content="A "),
        Italic(
            inline_children=[
                Text(content="italic")
            ]
        ),
        Text(content=" B "),
        InlineCode(
            inline_children=[
                Text(content="code")
            ]
        ),
        Text(content=" C "),
        Strong(
            inline_children=[
                Text(content="strong")
            ]
        ),
        Text(content=" D"),
    ]

def test_parse_inline_children_parses_link():
    children = parse_inline_children(
        "before [OpenAI](https://openai.com) after"
    )

    assert children[0] == Text(content="before ")

    assert isinstance(children[1], Link)
    assert children[1].url == "https://openai.com"
    assert children[1].inline_children == [
        Text(content="OpenAI")
    ]

    assert children[2] == Text(content=" after")

def test_parse_inline_children_parses_image():
    children = parse_inline_children(
        "before ![Logo](logo.png) after"
    )

    assert children[0] == Text(content="before ")

    assert isinstance(children[1], Image)
    assert children[1].src == "logo.png"
    assert children[1].inline_children == [
        Text(content="Logo")
    ]

    assert children[2] == Text(content=" after")

def test_parse_inline_children_parses_strong_inside_link():
    children = parse_inline_children(
        "[**OpenAI**](https://openai.com)"
    )

    assert isinstance(children[0], Link)

    assert children[0].inline_children == [
        Strong(
            inline_children=[
                Text(content="OpenAI")
            ]
        )
    ]

def test_parse_inline_children_parses_link_inside_strong():
    children = parse_inline_children(
        "**Visit [OpenAI](https://openai.com)**"
    )

    assert isinstance(children[0], Strong)

    assert children[0].inline_children == [
        Text(content="Visit "),
        Link(
            url="https://openai.com",
            inline_children=[
                Text(content="OpenAI")
            ]
        ),
    ]


def test_parse_inline_children_parses_empty_strong():
    children = parse_inline_children("****")

    assert children == [Text(content="****")]


def test_parse_inline_children_parses_empty_link():
    children = parse_inline_children("[](https://openai.com)")

    assert children == [
        Link(
            url="https://openai.com",
            inline_children=[],
        )
    ]


def test_parse_inline_children_parses_empty_image():
    children = parse_inline_children("![](logo.png)")

    assert children == [
        Image(
            src="logo.png",
            inline_children=[],
        )
    ]


def test_parse_inline_children_parses_multiple_adjacent_links():
    children = parse_inline_children("[a](u1)[b](u2)")

    assert len(children) == 2
    assert isinstance(children[0], Link)
    assert children[0].url == "u1"
    assert isinstance(children[1], Link)
    assert children[1].url == "u2"


def test_parse_inline_children_parses_multiple_adjacent_images():
    children = parse_inline_children("![a](a.png)![b](b.png)")

    assert len(children) == 2
    assert isinstance(children[0], Image)
    assert children[0].src == "a.png"
    assert isinstance(children[1], Image)
    assert children[1].src == "b.png"


def test_parse_inline_children_parses_link_followed_by_strong():
    children = parse_inline_children("[a](u)**b**")

    assert len(children) == 2
    assert isinstance(children[0], Link)
    assert isinstance(children[1], Strong)


def test_parse_inline_children_parses_strong_followed_by_link():
    children = parse_inline_children("**a**[b](u)")

    assert len(children) == 2
    assert isinstance(children[0], Strong)
    assert isinstance(children[1], Link)


def test_parse_inline_children_parses_image_inside_link():
    children = parse_inline_children("[![logo](logo.png)](https://openai.com)")

    assert len(children) == 1
    assert isinstance(children[0], Link)
    assert children[0].inline_children == [
        Image(
            src="logo.png",
            inline_children=[
                Text(content="logo")
            ]
        )
    ]


def test_parse_inline_children_parses_link_inside_image_alt():
    children = parse_inline_children("![go to [OpenAI](u)](logo.png)")

    assert len(children) == 1
    assert isinstance(children[0], Image)
    assert children[0].inline_children == [
        Text(content="go to "),
        Link(
            url="u",
            inline_children=[
                Text(content="OpenAI")
            ]
        ),
    ]
