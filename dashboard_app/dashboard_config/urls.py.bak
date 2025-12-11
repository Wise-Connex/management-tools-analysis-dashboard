"""
Centralized URL configuration for the Management Tools Analysis Dashboard.

This module provides consistent URL management across all components.
"""

from typing import Dict, Optional

# Dashboard and company URLs
DASHBOARD_URL = "https://tempo.solidum360.com/"
COMPANY_URL = "https://solidum360.com/"

# URL configurations for different contexts
URL_CONFIGS = {
    "dashboard": {
        "base": DASHBOARD_URL,
        "citation": DASHBOARD_URL.rstrip("/"),  # Remove trailing slash for citations
        "display": DASHBOARD_URL,
    },
    "company": {
        "base": COMPANY_URL,
        "display": COMPANY_URL,
    },
}


def get_dashboard_url(context: str = "base") -> str:
    """
    Get dashboard URL for different contexts.

    Args:
        context: Context for URL usage - "base", "citation", "display"

    Returns:
        Appropriate dashboard URL for the context

    Examples:
        >>> get_dashboard_url()
        "https://tempo.solidum360.com/"
        >>> get_dashboard_url("citation")
        "https://tempo.solidum360.com"
        >>> get_dashboard_url("display")
        "https://tempo.solidum360.com/"
    """
    return URL_CONFIGS["dashboard"].get(context, DASHBOARD_URL)


def get_company_url(context: str = "base") -> str:
    """
    Get company URL for different contexts.

    Args:
        context: Context for URL usage - "base", "display"

    Returns:
        Appropriate company URL for the context

    Examples:
        >>> get_company_url()
        "https://solidum360.com/"
        >>> get_company_url("display")
        "https://solidum360.com/"
    """
    return URL_CONFIGS["company"].get(context, COMPANY_URL)


def get_source_url(language: str = "en") -> str:
    """
    Get formatted source URL for graph footers.

    Args:
        language: Language code - "en" or "es"

    Returns:
        Formatted source URL with appropriate label

    Examples:
        >>> get_source_url("en")
        "Source: https://tempo.solidum360.com/"

        >>> get_source_url("es")
        "Fuente: https://tempo.solidum360.com/"
    """
    try:
        from translations import get_text

        source_label = get_text("source", language)
    except ImportError:
        # Fallback for direct testing
        source_label = "Source" if language == "en" else "Fuente"

    dashboard_url = get_dashboard_url("display")

    return f"{source_label}: {dashboard_url}"


def get_citation_url() -> str:
    """
    Get URL formatted for academic citations.

    Returns:
        URL without trailing slash for citation formats

    Examples:
        >>> get_citation_url()
        "https://tempo.solidum360.com"
    """
    return get_dashboard_url("citation")


def get_ris_url() -> str:
    """
    Get URL formatted for RIS file generation.

    Returns:
        URL with trailing slash for RIS format

    Examples:
        >>> get_ris_url()
        "https://tempo.solidum360.com/"
    """
    return get_dashboard_url("base")


def validate_url_consistency() -> bool:
    """
    Validate that all URL configurations are consistent.

    Returns:
        True if all URLs are valid, False otherwise
    """
    try:
        # Test all URL functions return valid results
        urls_to_test = [
            get_dashboard_url(),
            get_dashboard_url("citation"),
            get_dashboard_url("display"),
            get_company_url(),
            get_citation_url(),
            get_ris_url(),
            get_source_url("en"),
            get_source_url("es"),
        ]

        for url in urls_to_test:
            if not url or not url.startswith("https://"):
                return False

        return True
    except Exception:
        return False


def get_all_urls() -> Dict[str, str]:
    """Get all configured URLs as a dictionary."""
    return {
        "dashboard_base": get_dashboard_url(),
        "dashboard_citation": get_citation_url(),
        "dashboard_display": get_dashboard_url("display"),
        "company_base": get_company_url(),
        "company_display": get_company_url("display"),
        "ris_format": get_ris_url(),
    }
