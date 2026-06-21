from dataclasses import dataclass

from domains.cv.entities.earlier_experience import EarlierExperience
from domains.cv.entities.education import Education
from domains.cv.entities.experience import Experience
from domains.cv.entities.profile import Profile
from domains.cv.entities.project import Project
from domains.cv.entities.summary import Summary


@dataclass
class Sections:
    profile: Profile
    summary: Summary
    projects: list[Project]
    experiences: list[Experience]
    earlier_experiences: list[EarlierExperience]
    education: Education
