from pathlib import Path
import argparse
import sys
import json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.llm import (
    get_client,
    get_model,
)


def resolve_schema() -> Path:
    return ROOT / "architecture" / "project_schema.md"


def resolve_output(project_name: str) -> Path:
    return (
        ROOT
        / "content"
        / "views"
        / "portfolio_views"
        / f"{project_name}_portfolio_en.json"
    )


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_prompt(
    schema_text: str,
    source_text: str,
) -> str:

    return f"""
Convert the source markdown into Portfolio JSON.

Follow the schema exactly.

Return JSON only.

Do not explain.

Do not wrap JSON in markdown.

Do not output any text before or after the JSON.

# Schema

{schema_text}

# Source

{source_text}
""".strip()


def generate_portfolio_json(
    prompt: str,
) -> dict:

    client = get_client()

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    content = response.choices[0].message.content

    return json.loads(content)


def write_output(
    output_path: Path,
    data: dict,
) -> None:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )



def main(
    source: str,
) -> None:

    source_path = Path(source)
    if not source_path.exists():
        raise FileNotFoundError(f"Missing source:\n{source_path}")

    project_name = source_path.stem

    output_path = resolve_output(
        project_name
    )

    schema_path = resolve_schema()

    schema_text = read_file(
        schema_path
    )

    source_text = read_file(
        source_path
    )

    prompt = build_prompt(
        schema_text=schema_text,
        source_text=source_text,
    )

    portfolio_json = generate_portfolio_json(
        prompt
    )

    write_output(
        output_path,
        portfolio_json,
    )

    print(
        f"Generated: {output_path}"
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "source",
        help="Project markdown file",
    )

    args = parser.parse_args()

    main(args.source)