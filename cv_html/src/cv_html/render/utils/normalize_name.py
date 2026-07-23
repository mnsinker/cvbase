SPECIAL_NAMES = {
    "cv_base": "CV Base",
    "question_forge": "Question Forge",
    "decision_engine": "AI Decision Engine",
}


def normalize_name(value: str) -> str:

    value = value.strip()

    if value in SPECIAL_NAMES:
        return SPECIAL_NAMES[value]

    return " ".join(
        word.capitalize()
        for word in value.split("_")
    )