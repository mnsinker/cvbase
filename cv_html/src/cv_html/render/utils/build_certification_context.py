from cv_html.render.utils.format_month import format_month


def build_certification_context(certification):
    return {
        "certification": certification,
        "issue_date": format_month(certification.issue_date)
        if certification.issue_date
        else "",
    }
