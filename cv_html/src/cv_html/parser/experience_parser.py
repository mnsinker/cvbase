from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, FrontMatter
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.entities.domain import Experience
from cv_html.parser.inline_converter import convert_rich_text
from compiler.api.query import get_node_by_type, get_children_text, get_doc_children, get_inline_children
from compiler.api.transform import frontmatter_to_dict
from cv_html.filter.file_filter import filter_language_files
from cv_html.filter.visibility_filter import get_visible_node_by_text


def parse_experience(document: Document) -> Experience:
    # 1. parse metadata
    metadata = frontmatter_to_dict(get_node_by_type(document, FrontMatter))

    company = metadata.get("company", "")
    department = metadata.get("department", "")
    show_department = str(metadata.get("show_department", True)).strip().lower() not in ("false" or "")

    role = metadata.get("role", "")
    start_date = metadata.get("start_date", "")
    end_date = metadata.get("end_date", "")
    is_other = str(metadata.get("is_other", False)).strip().lower() == "true"


    # 2. parse bullets
    bullet_parent = get_visible_node_by_text(document, ["Bullet", "Bullets"])
    bullet_doc_nodes = get_doc_children(bullet_parent) if bullet_parent else []
    bullet_inline_nodes = [inline_nodes for doc_node in bullet_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
    bullets = [convert_rich_text(bullet_inlines) for bullet_inlines in bullet_inline_nodes]

    # 3. parse descriptions
    desc_parent = get_visible_node_by_text(document, ["Description", "Descriptions"])
    desc_doc_nodes = get_doc_children(desc_parent)
    desc_inline_nodes = [inline_nodes for doc_node in desc_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
    descriptions = [convert_rich_text(desc_inlines) for desc_inlines in desc_inline_nodes]

    # 4. parse labels
    labels_node = get_visible_node_by_text(document, ["Label", "Labels"])
    labels = get_children_text(labels_node) if labels_node else []

    return Experience(
        company=company,
        department=department,
        role=role,
        start_date=start_date,
        end_date=end_date,
        descriptions = descriptions,
        labels=labels,
        bullets=bullets,
        show_department=show_department,
        is_other=is_other,
    )

def parse_experiences(folder_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None=None) -> list[Experience]:
    files = filter_language_files(folder_path, language)
    documents = [compile_file(file, annotation_configs) for file in files]
    documents = [remove_nodes_by_annotation_key(doc, "excluded_visibility") for doc in documents]
    experiences = [parse_experience(doc) for doc in documents]
    sorted_experiences = sorted(experiences, key=lambda e: e.start_date, reverse=True)
    return sorted_experiences


print(parse_experiences("/Users/mnsink/projects/cv-base/knowledge/career/experiences"))



