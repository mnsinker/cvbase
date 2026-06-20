from dataclasses import dataclass

from products.cv.entities.earlier_experience import EarlierExperience
from products.cv.entities.education import Education
from products.cv.entities.experience import Experience
from products.cv.entities.profile import Profile
from products.cv.entities.project import Project
from products.cv.entities.summary import Summary


@dataclass
class Sections:
    profile: Profile
    summary: Summary
    projects: list[Project]
    experiences: list[Experience]
    earlier_experiences: list[EarlierExperience]
    education: Education
