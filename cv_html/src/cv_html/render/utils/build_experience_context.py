from cv_html.render.utils.build_date_range import build_date_range
from cv_html.render.utils.build_duration import build_duration


def build_experience_context(experience):

    return {
        "experience": experience,
        "date_range": build_date_range(
            experience.start_date,
            experience.end_date,
        ),
        "duration": build_duration(
            experience.start_date,
            experience.end_date,
        ),
    }
