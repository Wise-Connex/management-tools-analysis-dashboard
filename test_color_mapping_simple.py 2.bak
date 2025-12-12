#!/usr/bin/env python3
"""
Simple test to understand the PCA color mapping issue.
"""


def get_original_column_name(display_name, translation_mapping):
    """Simplified version of the function"""
    return translation_mapping.get(display_name, display_name)


def test_color_mapping_issue():
    """Test the color mapping logic to understand the issue"""

    # Simulate the global color map from utils.py
    color_map = {
        "Google Trends": "#1f77b4",  # Blue
        "Bain Usability": "#ff7f0e",  # Orange
        "Harvard Business Review": "#2ca02c",  # Green
        "McKinsey Insights": "#d62728",  # Red
        "BCG Analysis": "#9467bd",  # Purple
        "Google Trends - Market": "#8c564b",  # Brown
        "Bain Usabilidad": "#e377c2",  # Pink
        "Harvard Business Review - Strategy": "#7f7f7f",  # Gray
        "McKinsey Insights - Operations": "#bcbd22",  # Olive
        "BCG Analysis - Growth": "#17becf",  # Cyan
    }

    # Add Spanish translations to color map
    color_map.update(
        {
            "Bain Usabilidad": color_map["Bain Usability"],
            "Harvard Business - Estrategia": color_map["Harvard Business Review"],
            "McKinsey Insights - Operaciones": color_map["McKinsey Insights"],
            "BCG Analysis - Crecimiento": color_map["BCG Analysis"],
        }
    )

    # Simulate translation mapping (this is what gets passed to PCA function)
    translation_mapping = {
        "Google Trends": "google_trends",
        "Bain Usability": "bain_usability",
        "Harvard Business Review": "harvard_business_review",
        "McKinsey Insights": "mckinsey_insights",
        "BCG Analysis": "bcg_analysis",
    }

    print("🔍 TESTING PCA COLOR MAPPING ISSUE")
    print("=" * 50)

    print("\n📋 AVAILABLE COLORS:")
    for source, color in color_map.items():
        print(f"  {source}: {color}")

    print(f"\n📋 TRANSLATION MAPPING:")
    for display, original in translation_mapping.items():
        print(f"  {display} -> {original}")

    print(f"\n🧪 TESTING CURRENT PCA APPROACH:")

    test_sources = [
        "Google Trends",
        "Bain Usability",
        "Harvard Business Review",
        "McKinsey Insights",
        "BCG Analysis",
    ]

    for source in test_sources:
        print(f"\n  Testing: '{source}'")

        # Current PCA approach
        original_source_name = get_original_column_name(source, translation_mapping)
        arrow_color = color_map.get(original_source_name, "#000000")

        print(f"    Display name: {source}")
        print(f"    Original name from translation: '{original_source_name}'")
        print(f"    Color map lookup result: '{arrow_color}'")

        if arrow_color == "#000000":
            print(f"    ❌ PROBLEM: Fallback color (black) used!")
            print(f"    🔍 Looking for '{original_source_name}' in color_map...")
            # Check if the original name exists anywhere
            found = False
            for color_key in color_map.keys():
                if (
                    original_source_name in color_key.lower()
                    or color_key.lower() in original_source_name
                ):
                    print(
                        f"    💡 Partial match found: '{color_key}' -> {color_map[color_key]}"
                    )
                    found = True
                    break
            if not found:
                print(f"    💡 No matches found for '{original_source_name}'")
        else:
            print(f"    ✅ SUCCESS: Color found!")

    print(f"\n🔄 TESTING ALTERNATIVE APPROACH (display name directly):")

    for source in test_sources:
        direct_color = color_map.get(source, "#000000")
        print(f"    '{source}' -> {direct_color}")

        if direct_color == "#000000":
            print(f"    ❌ PROBLEM: Fallback color used")
        else:
            print(f"    ✅ SUCCESS: Color found!")

    print("\n🎯 ANALYSIS:")
    print("✅ Current approach: Uses translation mapping -> database names")
    print("✅ Problem: Database names don't match color_map keys")
    print("✅ Solution: Use display names directly OR fix translation mapping")
    print("✅ Alternative: Update color_map to include database names")


if __name__ == "__main__":
    test_color_mapping_issue()
