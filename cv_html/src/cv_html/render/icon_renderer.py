"""Load registered SVG assets into the rendered HTML document."""

from html import escape
from pathlib import Path


ICON_DIR = Path(__file__).resolve().parents[3] / "assets" / "icons"


def render_icon(icon_path: str, css_class: str) -> str:
    """Return a registered SVG asset with its presentation class attached."""
    if not icon_path:
        return ""

    asset_path = ICON_DIR / Path(icon_path).name
    svg = asset_path.read_text(encoding="utf-8")
    return svg.replace(
        "<svg ",
        f'<svg class="{escape(css_class, quote=True)}" aria-hidden="true" ',
        1,
    )
