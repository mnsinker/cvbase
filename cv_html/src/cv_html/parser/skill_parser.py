from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.api.transform import frontmatter_to_dict
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, FrontMatter
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.entities.domain import SkillCategory
from compiler.api.query import get_text, get_doc_children, get_inline_children, get_node_by_type
from cv_html.filter.file_filter import filter_language_files
from cv_html.parser.inline_converter import convert_rich_text


def parse_skill_categories(document: Document) -> list[SkillCategory]:
    # 0. parse metadata & get icons
    metadata = frontmatter_to_dict(get_node_by_type(document, FrontMatter))
    icons = [icon.strip() for icon in metadata.get("icons", "").split(",") if icon.strip()]
    print(icons)

    skill_categories = []
    i = 0
    for node in document.doc_children:
        # 1. handle title
        title = get_text(node).strip()
        if not title:
            continue
        # 2. handle bullets
        bullet_doc_nodes = get_doc_children(node) if node else []
        bullet_inline_nodes = [inline_nodes for doc_node in bullet_doc_nodes if (inline_nodes := get_inline_children(doc_node))]
        bullets = [convert_rich_text(bullet_inlines) for bullet_inlines in bullet_inline_nodes]
        if not bullets:
            continue
        # 3. append
        skill_categories.append(SkillCategory(
            title=title,
            icon=icons[i].strip() if i < len(icons) else "",
            bullets=bullets)
        )
        i += 1
    return skill_categories

def parse_skills(folder_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None=None) -> list[SkillCategory]:
    files = filter_language_files(folder_path, language)
    documents = [compile_file(file, annotation_configs) for file in files]
    documents = [remove_nodes_by_annotation_key(doc, "excluded_visibility") for doc in documents]
    skills = []
    for doc in documents:
        skills.extend(parse_skill_categories(doc))
    return skills

print(parse_skills("/Users/mnsink/projects/cv-base/knowledge/career/skills"))