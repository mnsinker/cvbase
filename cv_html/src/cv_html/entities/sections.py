from dataclasses import dataclass

from cv_html.entities.earlier_experience import EarlierExperience
from cv_html.entities.education import Education
from cv_html.entities.experience import Experience
from cv_html.entities.profile import Profile
from cv_html.entities.project import Project
from cv_html.entities.summary import Summary


@dataclass
class Sections:
    profile: Profile
    summary: Summary
    projects: list[Project]
    experiences: list[Experience]
    earlier_experiences: list[EarlierExperience]
    education: Education
