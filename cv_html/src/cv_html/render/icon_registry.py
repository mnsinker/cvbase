"""Resolve frontend icon names to static SVG asset paths."""

ICON_REGISTRY = {
    "bot": "bot.svg",
    "file-text": "file-text.svg",
    "brain-circuit": "brain-circuit.svg",
    "code-xml": "code-xml.svg",
    "sparkles": "sparkles.svg",
}

LINK_ICON_REGISTRY = {
    "Portfolio": "portfolio.svg",
    "Explore": "explore.svg",
    "Live Demo": "live-demo.svg",
    "GitHub": "github.svg",
}

LINK_ICON_ALIASES = {
    "Github": "GitHub",
    "探索": "Explore",
    "查看详情": "Explore",
    "了解项目": "Explore",
    "在线体验": "Live Demo",
}

ASSET_PATH = "../assets/icons"
def _asset_path(filename: str) -> str:
    return f"{ASSET_PATH}/{filename}"

def resolve_icon(icon_name: str | None) -> str:
    """Return a skill SVG asset path, defaulting to sparkles."""
    normalized_name = icon_name.strip().lower() if icon_name else ""
    return _asset_path(ICON_REGISTRY.get(normalized_name, ICON_REGISTRY["sparkles"]))

def get_skill_icon(icon_name: str | None) -> str:
    """Compatibility wrapper for skill templates."""
    return resolve_icon(icon_name)

def get_link_icon(title: str) -> str:
    """Return a project/profile link SVG asset path, or an empty string."""
    icon_name = LINK_ICON_ALIASES.get(title, title)
    filename = LINK_ICON_REGISTRY.get(icon_name)
    return _asset_path(filename) if filename else ""
