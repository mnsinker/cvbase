from dataclasses import dataclass, field
from math import inf
from cv_html.entities.inline import RichText, LinkNode


@dataclass
class Profile:
    name: str
    phone: str
    email: str
    location: str

    links: list[LinkNode] = field(default_factory=list)
    desired_positions: list[str] = field(default_factory=list)
    summaries: list[RichText] = field(default_factory=list)




@dataclass
class SkillCategory:
    title: str
    icon: str = ""
    bullets: list[RichText] = field(default_factory=list)



@dataclass
class Project:
    name: str
    labels: list[str]

    start_date: str
    end_date: str = ""

    order: int|float = inf
    links: list[LinkNode] = field(default_factory=list)
    descriptions: list[RichText] = field(default_factory=list)
    bullets: list[RichText] = field(default_factory=list)
    show_project: bool = True

@dataclass
class Experience:
    company: str
    department: str = ""
    show_department: bool = True

    role: str = ""
    start_date: str = ""
    end_date: str = ""

    links: list[LinkNode] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    descriptions: list[RichText] = field(default_factory=list)

    bullets: list[RichText] = field(default_factory=list)
    is_other: bool = False



@dataclass
class Education:
    school: str
    degree: str
    start_date: str = ""
    end_date: str = ""
    bullets: list[RichText] = field(default_factory=list)

@dataclass
class Certification:
    name: str
    issuer: str = ""
    issue_date: str = ""
    expiry_date: str = ""
    credential_id: str = ""
    links: list[LinkNode] = field(default_factory=list)
    show_in_header: bool = False



@dataclass
class CV:
    profile: Profile
    skills: list[SkillCategory]

    projects: list[Project]
    experiences: list[Experience]

    educations: list[Education]
    certifications: list[Certification]
