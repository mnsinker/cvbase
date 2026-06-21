from domains.cv.render.normalize_date import normalize_date


def build_date_range(start_date: str, end_date: str) -> str:

    start_year, start_month = normalize_date(start_date)
    end_year, end_month = normalize_date(end_date)

    return (
        f"{start_year}.{start_month:02d}"
        f" - "
        f"{end_year}.{end_month:02d}"
    )