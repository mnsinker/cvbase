from cv_html.render.utils.normalize_date import normalize_date


def format_month(value: str) -> str:
    year, month = normalize_date(value)
    return f"{year:04d}.{month:02d}"
