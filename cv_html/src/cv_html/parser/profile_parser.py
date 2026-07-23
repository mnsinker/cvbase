from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, FrontMatter
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.entities.domain import Profile
from cv_html.entities.inline import LinkNode
from compiler.api.query import get_node_by_type, get_links, get_doc_children, get_inline_children
from compiler.api.transform import frontmatter_to_dict
from cv_html.filter.file_filter import filter_language_files
from cv_html.filter.visibility_filter import get_visible_node_by_text
from cv_html.parser.inline_converter import convert_rich_text


def parse_profile(document: Document) -> Profile:
    # 1. parse metadata
    metadata = frontmatter_to_dict(get_node_by_type(document, FrontMatter))
    name = metadata.get("name", "")
    phone = metadata.get("phone", "")
    email = metadata.get("email", "")
    location = metadata.get("location", "")
    desired_positions = metadata.get("desired_positions", "").strip().split(",")

    # 2. parse links
    links_node = get_visible_node_by_text(document, ["Link", "Links"])
    links = get_links(links_node) if links_node else []
    links = [LinkNode(title=link.get("title"), url=link.get("url")) for link in links]

    # 3. parse summary
    summary_parent = get_visible_node_by_text(document, ["Summary", "Summaries"])
    summary_doc_nodes = get_doc_children(summary_parent)
    summary_inline_nodes = [inline_nodes for doc_node in summary_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
    summaries = [convert_rich_text(summary_inlines) for summary_inlines in summary_inline_nodes]

    return Profile(
        name=name,
        phone=phone,
        email=email,
        location=location,
        links=links,
        desired_positions=desired_positions,
        summaries=summaries,
    )

def parse_profiles(folder_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None=None) -> list[Profile]:
    files = filter_language_files(folder_path, language)
    documents = [compile_file(file, annotation_configs) for file in files]
    documents = [remove_nodes_by_annotation_key(doc, "excluded_visibility") for doc in documents]
    profiles = [parse_profile(doc) for doc in documents]
    return profiles


