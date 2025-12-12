#!/usr/bin/env python3
"""
Hash utilities with canonical source name mapping for key findings review.
Ensures consistency between database population and dashboard retrieval.
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from pathlib import Path

# Canonical source name mapping - all variations map to standard form
CANONICAL_SOURCE_NAMES = {
    # English variations
    "google trends": "Google Trends",
    "google_trends": "Google Trends",
    "Google Trends": "Google Trends",
    "GoogleTrends": "Google Trends",
    "google books": "Google Books",
    "google_books": "Google Books",
    "Google Books": "Google Books",
    "GoogleBooks": "Google Books",
    "Google Books Ngrams": "Google Books",
    "bain usability": "Bain Usability",
    "bain_usability": "Bain Usability",
    "Bain Usability": "Bain Usability",
    "BainUsability": "Bain Usability",
    "Bain - Usability": "Bain Usability",
    "bain satisfaction": "Bain Satisfaction",
    "bain_satisfaction": "Bain Satisfaction",
    "Bain Satisfaction": "Bain Satisfaction",
    "BainSatisfaction": "Bain Satisfaction",
    "Bain - Satisfaction": "Bain Satisfaction",
    "crossref": "Crossref",
    "Crossref": "Crossref",
    "CrossRef": "Crossref",
    "Crossref.org": "Crossref",
    "crossref.org": "Crossref",
    # Spanish variations (map to English canonical)
    "bain usabilidad": "Bain Usability",
    "bain_usabilidad": "Bain Usability",
    "Bain Usabilidad": "Bain Usability",
    "BainUsabilidad": "Bain Usability",
    "Bain - Usabilidad": "Bain Usability",
    "bain satisfacción": "Bain Satisfaction",
    "bain_satisfacción": "Bain Satisfaction",
    "Bain Satisfacción": "Bain Satisfaction",
    "BainSatisfacción": "Bain Satisfaction",
    "Bain - Satisfacción": "Bain Satisfaction",
}

# Source ID mapping for consistency
SOURCE_ID_MAPPING = {
    "Google Trends": 1,
    "Google Books": 2,
    "Bain Usability": 3,
    "Crossref": 4,
    "Bain Satisfaction": 5,
}

# Database name mapping
DB_NAME_MAPPING = {
    "Google Trends": "Google Trends",
    "Google Books": "Google Books Ngrams",
    "Bain Usability": "Bain - Usabilidad",
    "Crossref": "Crossref.org",
    "Bain Satisfaction": "Bain - Satisfacción",
}


def normalize_source_name(source_name: str) -> str:
    """
    Normalize any source name variation to canonical form.

    Args:
        source_name: Source name (can be any variation)

    Returns:
        Canonical source name
    """
    if not source_name:
        return ""

    # Convert to lowercase and normalize spacing
    normalized = source_name.lower().strip()

    # Remove special characters and normalize
    normalized = normalized.replace("-", " ").replace("_", " ")
    normalized = " ".join(normalized.split())  # Normalize multiple spaces

    # Map to canonical name
    return CANONICAL_SOURCE_NAMES.get(normalized, source_name)


def normalize_tool_name(tool_name: str) -> str:
    """
    Normalize tool name for consistent hashing.

    Args:
        tool_name: Tool name

    Returns:
        Normalized tool name
    """
    if not tool_name:
        return ""

    # Convert to lowercase, replace spaces and dashes with underscores
    normalized = tool_name.lower().replace(" ", "_").replace("-", "_")
    return normalized


def generate_combination_hash(
    tool_name: str, selected_sources: List[str], language: str
) -> str:
    """
    Generate consistent hash for tool+sources+language combination.

    Args:
        tool_name: Management tool name
        selected_sources: List of data sources
        language: Language code (es/en)

    Returns:
        Consistent hash string
    """
    # Normalize inputs
    tool_name_norm = normalize_tool_name(tool_name)

    # Normalize and sort source names
    source_names = sorted(
        [normalize_source_name(source) for source in selected_sources]
    )

    # Create combination data
    combination_data = {
        "tool": tool_name_norm,
        "sources": source_names,
        "language": language.lower().strip(),
    }

    # Generate consistent hash
    hash_input = json.dumps(combination_data, sort_keys=True)
    hash_hex = hashlib.md5(hash_input.encode()).hexdigest()[:10]

    # Create readable hash with normalized names
    source_part = "_".join([name.lower().replace(" ", "_") for name in source_names])

    return f"{tool_name_norm}_{source_part}_{language}_{hash_hex}"


def verify_hash_consistency(
    tool_name: str, selected_sources: List[str], language: str
) -> Dict[str, Any]:
    """
    Verify hash generation consistency and test variations.

    Args:
        tool_name: Management tool name
        selected_sources: List of data sources
        language: Language code

    Returns:
        Verification results
    """
    results = {"original_hash": "", "variations": [], "consistent": True, "issues": []}

    # Generate original hash
    original_hash = generate_combination_hash(tool_name, selected_sources, language)
    results["original_hash"] = original_hash

    # Test variations
    test_variations = [
        # Source order variations
        selected_sources[::-1] if len(selected_sources) > 1 else selected_sources,
        # Case variations
        [s.upper() for s in selected_sources],
        [s.lower() for s in selected_sources],
        # Dash variations
        [s.replace(" ", " - ") for s in selected_sources],
        # Mixed variations
        [s.replace(" ", "_") for s in selected_sources],
    ]

    for i, variation in enumerate(test_variations):
        try:
            variation_hash = generate_combination_hash(tool_name, variation, language)
            is_consistent = variation_hash == original_hash

            results["variations"].append(
                {
                    "variation": variation,
                    "hash": variation_hash,
                    "consistent": is_consistent,
                }
            )

            if not is_consistent:
                results["consistent"] = False
                results["issues"].append(f"Variation {i + 1} produces different hash")

        except Exception as e:
            results["variations"].append(
                {"variation": variation, "error": str(e), "consistent": False}
            )
            results["consistent"] = False
            results["issues"].append(f"Variation {i + 1} failed: {e}")

    return results


def test_hash_generation():
    """Test hash generation with various combinations."""
    test_cases = [
        {
            "tool": "Benchmarking",
            "sources": ["Google Trends", "Bain Usability"],
            "language": "es",
        },
        {"tool": "Calidad Total", "sources": ["Crossref"], "language": "es"},
        {
            "tool": "Gestión de Procesos",
            "sources": ["Bain Usability"],
            "language": "es",
        },
        {
            "tool": "Benchmarking",
            "sources": ["Google Trends", "Bain - Usability"],  # Dash variation
            "language": "es",
        },
        {
            "tool": "Benchmarking",
            "sources": ["Google Trends", "Bain - Usabilidad"],  # Spanish variation
            "language": "es",
        },
    ]

    print("🔑 Testing Hash Generation Consistency")
    print("=" * 60)

    all_consistent = True

    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i + 1}:")
        print(f"Tool: {test_case['tool']}")
        print(f"Sources: {test_case['sources']}")
        print(f"Language: {test_case['language']}")

        results = verify_hash_consistency(
            test_case["tool"], test_case["sources"], test_case["language"]
        )

        print(f"Original Hash: {results['original_hash']}")
        print(f"Consistent: {'✅' if results['consistent'] else '❌'}")

        if results["issues"]:
            print("Issues:")
            for issue in results["issues"]:
                print(f"  - {issue}")

        if not results["consistent"]:
            all_consistent = False
            print("Variation Results:")
            for var in results["variations"]:
                print(f"  {var['variation']} → {var.get('hash', 'ERROR')}")

    print(f"\n{'=' * 60}")
    print(
        f"Overall Result: {'✅ ALL TESTS PASSED' if all_consistent else '❌ SOME TESTS FAILED'}"
    )

    return all_consistent


if __name__ == "__main__":
    test_hash_generation()
