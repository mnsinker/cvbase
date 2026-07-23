from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
from cv_html.entities.domain import CV
from cv_html.render.utils.build_date_range import build_date_range
from cv_html.render.utils.build_certification_context import build_certification_context
from cv_html.render.utils.build_experience_context import build_experience_context
from cv_html.render.icon_registry import get_link_icon, get_skill_icon
from cv_html.render.icon_renderer import render_icon
from cv_html.render.inline_renderer import render_rich_text

TEMPLATE_DIR = Path(__file__).parent / "templates"
CSS_PATH = (Path(__file__).parent / "templates" / "cv.css")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR)) # initialize render env for Jinja2
env.globals["render_rich_text"] = render_rich_text
env.globals["get_link_icon"] = get_link_icon
env.globals["get_skill_icon"] = get_skill_icon
env.globals["render_icon"] = render_icon

def load_css() -> str:
    return CSS_PATH.read_text(encoding="utf-8")

def load_translations():
    path = Path(__file__).resolve().parents[2] / "config" / "translations.yml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def render_cv(cv: CV, language: str = "en"):
    translations = load_translations()
    translations = translations.get(language, translations["en"])
    template = env.get_template("cv.html")
    certification_contexts = [
        build_certification_context(certification)
        for certification in cv.certifications
    ]

    return template.render(
        cv=cv,
        translations=translations,
        html_lang=language,
        styles=load_css(),
        experience_contexts=[
            build_experience_context(experience)
            for experience in cv.experiences
        ],
        education_date_ranges=[
            build_date_range(education.start_date, education.end_date)
            for education in cv.educations
        ],
        certification_contexts=certification_contexts,
        summary_certification_contexts=[
            context
            for context in certification_contexts
            if context["certification"].show_in_header
        ],
    )
