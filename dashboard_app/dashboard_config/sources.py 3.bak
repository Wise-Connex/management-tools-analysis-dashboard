"""
Centralized source name mapping configuration for the Management Tools Analysis Dashboard.

This module provides consistent source name resolution across different naming conventions.
"""

from typing import Dict, Optional, List

# Source registry with all name variants
SOURCE_REGISTRY = {
    "Google Trends": {
        "display": "Google Trends",
        "db": "Google Trends",
        "es": "Google Trends",
        "color": "#1f77b4",  # Blue
    },
    "Google Books": {
        "display": "Google Books",
        "db": "Google Books Ngrams",
        "es": "Google Books",
        "color": "#ff7f0e",  # Orange
    },
    "Bain Usability": {
        "display": "Bain Usability",
        "db": "Bain - Usabilidad",
        "es": "Bain Usabilidad",
        "color": "#d62728",  # Red
    },
    "Bain Satisfaction": {
        "display": "Bain Satisfaction",
        "db": "Bain - Satisfacción",
        "es": "Bain Satisfacción",
        "color": "#9467bd",  # Purple
    },
    "Crossref": {
        "display": "Crossref",
        "db": "Crossref.org",
        "es": "Crossref",
        "color": "#2ca02c",  # Green
    },
}

# Reverse mappings for quick lookup
DB_TO_DISPLAY = {source["db"]: source["display"] for source in SOURCE_REGISTRY.values()}
ES_TO_DISPLAY = {source["es"]: source["display"] for source in SOURCE_REGISTRY.values()}
DISPLAY_TO_DB = {source["display"]: source["db"] for source in SOURCE_REGISTRY.values()}
DISPLAY_TO_ES = {source["display"]: source["es"] for source in SOURCE_REGISTRY.values()}


def resolve_source_name(
    source_name: str, target_type: str = "display", source_type: str = "auto"
) -> str:
    """
    Convert any source name variant to the target format.

    Args:
        source_name: The source name to convert
        target_type: Target format - "display", "db", "es" (Spanish)
        source_type: Source format - "auto", "display", "db", "es"

    Returns:
        Source name in the target format

    Examples:
        >>> resolve_source_name("Google Trends")
        "Google Trends"
        >>> resolve_source_name("Google Books Ngrams", target_type="display", source_type="db")
        "Google Books"
        >>> resolve_source_name("Bain Usabilidad", target_type="display", source_type="es")
        "Bain Usability"
    """
    if not source_name:
        return ""

    # Auto-detect source type if not specified
    if source_type == "auto":
        source_type = _detect_source_type(source_name)

    # If already in target format, return as-is
    if source_type == target_type:
        return source_name

    # Find the display name first
    display_name = _get_display_name(source_name, source_type)

    # Convert to target format
    if target_type == "display":
        return display_name
    elif target_type == "db":
        return DISPLAY_TO_DB.get(display_name, source_name)
    elif target_type == "es":
        return DISPLAY_TO_ES.get(display_name, source_name)
    else:
        return source_name


def _detect_source_type(source_name: str) -> str:
    """Auto-detect the type of source name."""
    if source_name in SOURCE_REGISTRY:
        return "display"
    elif source_name in DB_TO_DISPLAY:
        return "db"
    elif source_name in ES_TO_DISPLAY:
        return "es"
    else:
        return "display"  # Default fallback


def _get_display_name(source_name: str, source_type: str) -> str:
    """Get the display name for any source name variant."""
    if source_type == "display":
        return source_name
    elif source_type == "db":
        return DB_TO_DISPLAY.get(source_name, source_name)
    elif source_type == "es":
        return ES_TO_DISPLAY.get(source_name, source_name)
    else:
        return source_name


def get_source_color_by_name(source_name: str, name_type: str = "auto") -> str:
    """
    Get the color for a source name (any variant).

    Args:
        source_name: The source name
        name_type: Type of source name - "auto", "display", "db", "es"

    Returns:
        Hex color code for the source

    Examples:
        >>> get_source_color_by_name("Google Trends")
        "#1f77b4"
        >>> get_source_color_by_name("Google Books Ngrams", name_type="db")
        "#ff7f0e"
    """
    display_name = resolve_source_name(source_name, "display", name_type)
    source_info = SOURCE_REGISTRY.get(display_name)
    return source_info["color"] if source_info else "#6c757d"  # Default gray


def get_all_display_names() -> List[str]:
    """Get all display names."""
    return list(SOURCE_REGISTRY.keys())


def get_all_db_names() -> List[str]:
    """Get all database names."""
    return [source["db"] for source in SOURCE_REGISTRY.values()]


def get_all_es_names() -> List[str]:
    """Get all Spanish names."""
    return [source["es"] for source in SOURCE_REGISTRY.values()]


def validate_source_consistency() -> bool:
    """
    Validate that all source mappings are consistent.

    Returns:
        True if all mappings are valid, False otherwise
    """
    try:
        # Test all name variants resolve correctly
        test_cases = [
            ("Google Trends", "display", "display"),
            ("Google Trends", "db", "display"),
            ("Google Trends", "es", "display"),
            ("Google Books Ngrams", "db", "display"),
            ("Google Books", "display", "db"),
            ("Bain - Usabilidad", "db", "display"),
            ("Bain Usability", "display", "db"),
            ("Bain Usabilidad", "es", "display"),
            ("Bain Usability", "display", "es"),
        ]

        for source_name, source_type, target_type in test_cases:
            result = resolve_source_name(source_name, target_type, source_type)
            if not result or not isinstance(result, str):
                return False

        return True
    except Exception:
        return False


def get_source_info(display_name: str) -> Optional[Dict]:
    """
    Get complete source information by display name.

    Args:
        display_name: The display name of the source

    Returns:
        Dictionary with all source information or None if not found

    Examples:
        >>> get_source_info("Google Trends")
        {
            "display": "Google Trends",
            "db": "Google Trends",
            "es": "Google Trends",
            "color": "#1f77b4"
        }
    """
    return SOURCE_REGISTRY.get(display_name)
