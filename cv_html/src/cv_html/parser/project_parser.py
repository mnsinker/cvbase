from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, FrontMatter
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.entities.domain import Project
from cv_html.entities.inline import LinkNode
from compiler.api.query import get_node_by_type, get_children_text, get_links, get_doc_children, get_inline_children
from compiler.api.transform import frontmatter_to_dict
from cv_html.filter.file_filter import filter_language_files
from cv_html.filter.visibility_filter import get_visible_node_by_text
from cv_html.parser.inline_converter import convert_rich_text


def parse_project(document: Document) -> Project:
    # 1. parse metadata
    metadata = frontmatter_to_dict(get_node_by_type(document, FrontMatter))
    name = metadata.get("name", "")
    start_date = metadata.get("start_date", "")
    end_date = metadata.get("end_date", "")
    order = int(metadata.get("order", ""))
    show_project = str(metadata.get("show_project", True)).strip().lower() == "true"

    # 2. parse labels
    labels_node = get_visible_node_by_text(document, ["Label", "Labels"])
    labels = get_children_text(labels_node) if labels_node else []

    # 3. parse links
    links_node = get_visible_node_by_text(document, ["Link", "Links"])
    links = get_links(links_node) if links_node else []
    links = [LinkNode(title=link.get("title"), url=link.get("url")) for link in links]

    # 4. parse bullets
    bullet_parent = get_visible_node_by_text(document, ["Bullet", "Bullets"])
    bullet_doc_nodes = get_doc_children(bullet_parent) if bullet_parent else []
    bullet_inline_nodes = [inline_nodes for doc_node in bullet_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
    bullets = [convert_rich_text(bullet_inlines) for bullet_inlines in bullet_inline_nodes]

    # 5. parse descriptions
    desc_parent = get_visible_node_by_text(document, ["Description", "Descriptions"])
    desc_doc_nodes = get_doc_children(desc_parent) if desc_parent else []
    desc_inline_nodes = [inline_nodes for doc_node in desc_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
    descriptions = [convert_rich_text(desc_inlines) for desc_inlines in desc_inline_nodes]

    return Project(
        name=name,
        labels=labels,
        links=links,
        start_date=start_date,
        end_date=end_date,
        descriptions=descriptions,
        bullets=bullets,
        order=order,
        show_project=show_project,
    )

def parse_projects(folder_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None=None) -> list[Project]:
    files = filter_language_files(folder_path, language)
    documents = [compile_file(file, annotation_configs) for file in files]
    documents = [remove_nodes_by_annotation_key(doc, "excluded_visibility") for doc in documents]
    projects = [parse_project(doc) for doc in documents]
    sorted_projects = sorted(projects, key=lambda p : p.order)
    return sorted_projects


print(parse_projects("/Users/mnsink/projects/cv-base/knowledge/career/projects"))
