from apps.cv_html.render.normalize_date import (
    normalize_date,
)


def build_duration(start_date: str, end_date: str) -> str:

    start_year, start_month = normalize_date(start_date)
    end_year, end_month = normalize_date(end_date)

    total_months = (
        (end_year - start_year) * 12
        + (end_month - start_month)
        + 1
    )

    years = total_months // 12
    months = total_months % 12

    # Suppress tiny month tails when years exist
    if years > 0 and months < 4:
        months = 0

    year_text = ""
    if years == 1:
        year_text = "1 yr"
    elif years > 1:
        year_text = f"{years} yrs"

    month_text = ""
    if months == 1:
        month_text = "1 mth"
    elif months > 1:
        month_text = f"{months} mths"

    if year_text and month_text:
        return f"{year_text} & {month_text}"

    if year_text:
        return year_text

    return month_text