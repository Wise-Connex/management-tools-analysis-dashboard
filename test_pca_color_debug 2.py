#!/usr/bin/env python3
"""
Test script to debug PCA color mapping issues.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard_app.utils import color_map, get_original_column_name
from dashboard_app.translations import get_text


def test_pca_color_debug():
    """Debug PCA color mapping to understand the issue"""

    print("🔍 Debugging PCA color mapping...")
    print("=" * 50)

    # Test with typical source names
    test_sources = [
        "Google Trends",
        "Bain Usability",
        "Harvard Business Review",
        "McKinsey Insights",
        "BCG Analysis",
    ]

    print("\n📋 AVAILABLE COLOR MAP:")
    for source, color in color_map.items():
        print(f"  {source}: {color}")

    print(f"\n🔍 TOTAL COLORS AVAILABLE: {len(color_map)}")

    print("\n🧪 TESTING COLOR LOOKUPS:")

    # Test direct lookup (what PCA currently does)
    for source in test_sources:
        print(f"\n  Testing source: '{source}'")

        # Simulate what happens in PCA function
        translation_mapping = {
            "Google Trends": "google_trends",
            "Bain Usability": "bain_usability",
            "Harvard Business Review": "harvard_business_review",
            "McKinsey Insights": "mckinsey_insights",
            "BCG Analysis": "bcg_analysis",
        }

        # Current PCA approach
        original_source_name = get_original_column_name(source, translation_mapping)
        arrow_color = color_map.get(original_source_name, "#000000")

        print(f"    Display name: {source}")
        print(
            f"    Translation mapping: {translation_mapping.get(source, 'NOT FOUND')}"
        )
        print(f"    Original source name: {original_source_name}")
        print(f"    Color map lookup: {arrow_color}")

        if arrow_color == "#000000":
            print(f"    ⚠️  FALLBACK COLOR USED (black)")
        else:
            print(f"    ✅ COLOR FOUND: {arrow_color}")

    # Test alternative approach - use display name directly
    print(f"\n🔄 TESTING ALTERNATIVE APPROACH (display name directly):")
    for source in test_sources:
        direct_color = color_map.get(source, "#000000")
        print(f"    '{source}' -> {direct_color}")

        if direct_color == "#000000":
            print(f"    ⚠️  FALLBACK COLOR USED")
        else:
            print(f"    ✅ COLOR FOUND: {direct_color}")

    print("\n🎯 SUMMARY:")
    print("✅ Current approach uses translation mapping")
    print("✅ Alternative approach uses display names directly")
    print("✅ Need to verify which approach matches other visualizations")


if __name__ == "__main__":
    test_pca_color_debug()
