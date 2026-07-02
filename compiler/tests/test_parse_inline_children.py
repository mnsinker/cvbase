import pytest
from compiler.engine.parse_inline_children import parse_inline_children
from compiler.entities.document_nodes import Paragraph
from compiler.entities.inline_nodes import (
    Text,
    Strong,
    Italic,
    Strike,
    Underline,
    InlineCode,
    InlineMath,
    Link,
    Image,
)

def test_plain_text():
    children = parse_inline_children(Paragraph(),"hello world")
    assert len(children) == 1
    assert isinstance(children[0], Text)
    assert children[0].content == "hello world"

def test_strong():
    children = parse_inline_children(Paragraph(),"**hello**")
    assert len(children) == 1

    strong = children[0]
    assert isinstance(strong, Strong)
    assert len(strong.inline_children) == 1
    assert isinstance(strong.inline_children[0], Text)
    assert strong.inline_children[0].content == "hello"

def test_text_then_strong():
    children = parse_inline_children(Paragraph(),"abc **hello**")
    assert len(children) == 2
    assert isinstance(children[0], Text)
    assert isinstance(children[1], Strong)

def test_nested_italic():
    children = parse_inline_children(Paragraph(),"**hello *world***")
    strong = children[0]
    assert isinstance(strong, Strong)
    assert isinstance(strong.inline_children[0], Text)
    assert isinstance(strong.inline_children[1], Italic)

def test_link():
    children = parse_inline_children(Paragraph(),"[OpenAI](https://openai.com)")
    link = children[0]
    assert isinstance(link, Link)
    assert link.url == "https://openai.com"
    assert len(link.inline_children) == 1
    assert isinstance(link.inline_children[0], Text)
    assert (link.inline_children[0].content == "OpenAI")

def test_image():
    children = parse_inline_children(Paragraph(), "![logo](logo.png)")
    image = children[0]
    assert isinstance(image, Image)
    assert image.src == "logo.png"
    assert image.alt == "logo"

def test_escape():
    children = parse_inline_children(Paragraph(),r"\**hello**")
    assert len(children) == 1
    assert isinstance(children[0], Text)

def test_unclosed_strong():
    children = parse_inline_children(Paragraph(),"**hello")
    assert len(children) == 1
    assert isinstance(children[0], Text)