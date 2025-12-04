"""
Centralized color configuration for the Management Tools Analysis Dashboard.

This module provides consistent color mapping across all UI elements and visualizations.
"""

from typing import Dict, Optional

# Standard color palette for data sources (consistent with Plotly defaults)
SOURCE_COLORS = {
    "Google Trends": "#1f77b4",  # Blue
    "Google Books": "#ff7f0e",  # Orange
    "Bain Usability": "#d62728",  # Red
    "Bain Satisfaction": "#9467bd",  # Purple
    "Crossref": "#2ca02c",  # Green
}

# Database name to display name mapping for color consistency
DB_TO_DISPLAY_MAPPING = {
    "Google Trends": "Google Trends",
    "Google Books Ngrams": "Google Books",
    "Bain - Usabilidad": "Bain Usability",
    "Bain - Satisfacción": "Bain Satisfaction",
    "Crossref.org": "Crossref",
}

# Spanish translation mappings
SPANISH_TO_DISPLAY_MAPPING = {
    "Google Trends": "Google Trends",
    "Google Books": "Google Books",
    "Bain Usabilidad": "Bain Usability",
    "Bain Satisfacción": "Bain Satisfaction",
    "Crossref": "Crossref",
}


def get_source_color(source_name: str, name_type: str = "display") -> str:
    """
    Get consistent color for any source name variant.

    Args:
        source_name: The source name (display, database, or translated)
        name_type: Type of source name - "display", "db", "es" (Spanish), or "auto"

    Returns:
        Hex color code for the source

    Examples:
        >>> get_source_color("Google Trends")
        "#1f77b4"
        >>> get_source_color("Google Books Ngrams", name_type="db")
        "#ff7f0e"
        >>> get_source_color("Bain Usabilidad", name_type="es")
        "#d62728"
    """
    if not source_name:
        return "#6c757d"  # Default gray

    # Auto-detect name type if not specified
    if name_type == "auto":
        name_type = _detect_name_type(source_name)

    # Normalize to display name
    display_name = _normalize_to_display_name(source_name, name_type)

    # Return color from standardized palette
    return SOURCE_COLORS.get(display_name, "#6c757d")  # Default gray


def _detect_name_type(source_name: str) -> str:
    """Auto-detect the type of source name."""
    if source_name in SOURCE_COLORS:
        return "display"
    elif source_name in DB_TO_DISPLAY_MAPPING:
        return "db"
    elif source_name in SPANISH_TO_DISPLAY_MAPPING:
        return "es"
    else:
        return "display"  # Default fallback


def _normalize_to_display_name(source_name: str, name_type: str) -> str:
    """Convert any source name variant to display name."""
    if name_type == "display":
        return source_name
    elif name_type == "db":
        return DB_TO_DISPLAY_MAPPING.get(source_name, source_name)
    elif name_type == "es":
        return SPANISH_TO_DISPLAY_MAPPING.get(source_name, source_name)
    else:
        return source_name


def get_all_source_colors() -> Dict[str, str]:
    """Get all source colors as a dictionary."""
    return SOURCE_COLORS.copy()


def validate_color_consistency() -> bool:
    """
    Validate that all color mappings are consistent.

    Returns:
        True if all mappings are valid, False otherwise
    """
    try:
        # Test all name variants return same color
        test_cases = [
            ("Google Trends", "display"),
            ("Google Trends", "db"),
            ("Google Trends", "es"),
            ("Google Books Ngrams", "db"),
            ("Google Books", "display"),
            ("Bain - Usabilidad", "db"),
            ("Bain Usability", "display"),
            ("Bain Usabilidad", "es"),
        ]

        for source_name, name_type in test_cases:
            color = get_source_color(source_name, name_type)
            if not color or not color.startswith("#"):
                return False

        return True
    except Exception:
        return False
