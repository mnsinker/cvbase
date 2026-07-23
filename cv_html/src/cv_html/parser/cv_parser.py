from pathlib import Path

from compiler.entities.annotation_config import AnnotationConfig
from cv_html.entities.domain import CV
from cv_html.parser.certification_parser import parse_certifications
from cv_html.parser.education_parser import parse_educations
from cv_html.parser.experience_parser import parse_experiences
from cv_html.parser.profile_parser import parse_profiles
from cv_html.parser.project_parser import parse_projects
from cv_html.parser.skill_parser import parse_skills


def parse_cv(cv_path: str|Path, language: str="en", annotation_configs: list[AnnotationConfig]|None = None) -> CV:
    profile = parse_profiles(Path(cv_path) / "profile", language, annotation_configs)[0]
    skills = parse_skills(Path(cv_path)/"skills", language, annotation_configs)
    projects = parse_projects(Path(cv_path) / "projects", language, annotation_configs)
    experiences = parse_experiences(Path(cv_path) / "experiences", language, annotation_configs)
    educations = parse_educations(Path(cv_path) / "education", language, annotation_configs)
    certifications = parse_certifications(Path(cv_path) / "certifications", language, annotation_configs)

    return CV(
        profile=profile,
        skills=skills,
        projects=projects,
        experiences=experiences,
        educations=educations,
        certifications=certifications
    )
