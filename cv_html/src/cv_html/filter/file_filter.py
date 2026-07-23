from pathlib import Path


def filter_language_files(folder_path: str|Path, language: str) -> list[Path]:
    folder_path = Path(folder_path)
    return list(folder_path.glob(f"*.{language}.md"))
