from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, FrontMatter
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.entities.domain import Education
from compiler.api.query import get_node_by_type, get_doc_children, get_inline_children
from compiler.api.transform import frontmatter_to_dict
from cv_html.filter.file_filter import filter_language_files
from cv_html.filter.visibility_filter import get_visible_node_by_text
from cv_html.parser.inline_converter import convert_rich_text


def parse_education(document: Document) -> Education:
    # 1. parse metadata
    metadata = frontmatter_to_dict(get_node_by_type(document, FrontMatter))
    school = metadata.get("school", "")
    degree = metadata.get("degree", "")
    start_date = metadata.get("start_date", "")
    end_date = metadata.get("end_date", "")


    # 2. parse bullets
    bullet_parent = get_visible_node_by_text(document, ["Bullet", "Bullets"])
    bullet_doc_nodes = get_doc_children(bullet_parent) if bullet_parent else []
    bullet_inline_nodes = [inline_nodes for doc_node in bullet_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
    bullets = [convert_rich_text(bullet_inlines) for bullet_inlines in bullet_inline_nodes]

    return Education(
        school=school,
        degree=degree,
        start_date=start_date,
        end_date=end_date,
        bullets=bullets,
    )

def parse_educations(folder_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None=None) -> list[Education]:
    files = filter_language_files(folder_path, language)
    documents = [compile_file(file, annotation_configs) for file in files]
    documents = [remove_nodes_by_annotation_key(doc, "excluded_visibility") for doc in documents]
    educations = [parse_education(doc) for doc in documents]
    sorted_educations = sorted(educations, key=lambda e: e.start_date, reverse=True)
    return sorted_educations

