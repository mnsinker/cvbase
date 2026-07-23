from pathlib import Path
from compiler.annotations.annotation_transform import remove_nodes_by_annotation_key
from compiler.api.compile import compile_file
from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.doc_nodes import Document, FrontMatter
from config.annotation_configs import CV_ANNOTATIONS
from cv_html.entities.domain import Certification
from cv_html.entities.inline import LinkNode
from compiler.api.query import get_node_by_type, get_links
from compiler.api.transform import frontmatter_to_dict
from cv_html.filter.file_filter import filter_language_files
from cv_html.filter.visibility_filter import get_visible_node_by_text


def parse_certification(document: Document) -> Certification:
    # 1. parse metadata
    metadata = frontmatter_to_dict(get_node_by_type(document, FrontMatter))
    name = metadata.get("name", "")
    issuer = metadata.get("issuer", "")
    issue_date = metadata.get("issue_date", "")
    expiry_date = metadata.get("expiry_date", "")
    credential_id = metadata.get("credential_id", "")
    show_in_header = str(metadata.get("show_in_header", False)).lower() == "true"

    # 2. parse links
    links_node = get_visible_node_by_text(document, ["Link", "Links"])
    links = get_links(links_node) if links_node else []
    links = [LinkNode(title=link.get("title"), url=link.get("url")) for link in links]

    return Certification(
        name=name,
        issuer=issuer,
        issue_date=issue_date,
        expiry_date=expiry_date,
        credential_id=credential_id,
        links=links,
        show_in_header=show_in_header,
    )

def parse_certifications(folder_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None=None) -> list[Certification]:
    files = filter_language_files(folder_path, language)
    documents = [compile_file(file, annotation_configs) for file in files]
    documents = [remove_nodes_by_annotation_key(doc, "excluded_visibility") for doc in documents]
    certificates = [parse_certification(doc) for doc in documents]
    sorted_certificates = sorted(certificates, key=lambda e: e.issue_date, reverse=True)
    return sorted_certificates
