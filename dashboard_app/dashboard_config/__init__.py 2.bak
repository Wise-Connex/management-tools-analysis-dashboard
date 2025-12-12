"""
Configuration package for the Management Tools Analysis Dashboard.

This package provides centralized configuration for colors, URLs, and source names
to ensure consistency across all dashboard components.
"""

# Import color configuration
try:
    from .colors import (
        SOURCE_COLORS,
        get_source_color,
        get_all_source_colors,
        validate_color_consistency,
    )
except ImportError:
    # Fallback for direct execution
    from colors import (
        SOURCE_COLORS,
        get_source_color,
        get_all_source_colors,
        validate_color_consistency,
    )

# Import URL configuration
try:
    from .urls import (
        DASHBOARD_URL,
        COMPANY_URL,
        get_dashboard_url,
        get_company_url,
        get_source_url,
        get_citation_url,
        get_ris_url,
        validate_url_consistency,
        get_all_urls,
    )
except ImportError:
    # Fallback for direct execution
    from urls import (
        DASHBOARD_URL,
        COMPANY_URL,
        get_dashboard_url,
        get_company_url,
        get_source_url,
        get_citation_url,
        get_ris_url,
        validate_url_consistency,
        get_all_urls,
    )

# Import source name configuration
try:
    from .sources import (
        SOURCE_REGISTRY,
        resolve_source_name,
        get_source_color_by_name,
        get_all_display_names,
        get_all_db_names,
        get_all_es_names,
        validate_source_consistency,
        get_source_info,
    )
except ImportError:
    # Fallback for direct execution
    from sources import (
        SOURCE_REGISTRY,
        resolve_source_name,
        get_source_color_by_name,
        get_all_display_names,
        get_all_db_names,
        get_all_es_names,
        validate_source_consistency,
        get_source_info,
    )

# Package version and metadata
__version__ = "1.0.0"
__author__ = "Management Tools Analysis Team"
__description__ = "Centralized configuration for dashboard consistency"


# Convenience function to validate all configurations
def validate_all_configurations() -> bool:
    """
    Validate all configuration modules are working correctly.

    Returns:
        True if all configurations are valid, False otherwise
    """
    try:
        return (
            validate_color_consistency()
            and validate_url_consistency()
            and validate_source_consistency()
        )
    except Exception:
        return False


# Re-export commonly used functions for convenience
__all__ = [
    # Colors
    "SOURCE_COLORS",
    "get_source_color",
    "get_all_source_colors",
    "validate_color_consistency",
    # URLs
    "DASHBOARD_URL",
    "COMPANY_URL",
    "get_dashboard_url",
    "get_company_url",
    "get_source_url",
    "get_citation_url",
    "get_ris_url",
    "validate_url_consistency",
    "get_all_urls",
    # Sources
    "SOURCE_REGISTRY",
    "resolve_source_name",
    "get_source_color_by_name",
    "get_all_display_names",
    "get_all_db_names",
    "get_all_es_names",
    "validate_source_consistency",
    "get_source_info",
    # Validation
    "validate_all_configurations",
]
