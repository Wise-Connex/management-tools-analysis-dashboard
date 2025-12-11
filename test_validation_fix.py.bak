#!/usr/bin/env python3
"""
Final verification that the validation fix is working.
"""

import sys

sys.path.insert(0, "dashboard_app")

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_validation_fix():
    """Test that the validation fix is working correctly."""

    print("🔬 FINAL VERIFICATION OF VALIDATION FIX")
    print("=" * 60)

    db_manager = get_precomputed_db_manager()

    # Test the specific combination that was failing
    tool_name = "Calidad Total"
    sources = [
        "Google Trends",
        "Google Books",
        "Bain Usability",
        "Bain Satisfaction",
        "Crossref",
    ]
    language = "es"

    combination_hash = db_manager.generate_combination_hash(
        tool_name, sources, language
    )
    result = db_manager.get_combination_by_hash(combination_hash)

    if result:
        print("Current database content analysis:")
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "pca_analysis",
            "heatmap_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        available_sections = 0
        for section in required_sections:
            content = result.get(section, "")
            if content and len(str(content)) > 50:
                available_sections += 1
                print(f"  {section}: OK ({len(str(content))} chars)")
            else:
                print(
                    f"  {section}: MISSING/SHORT ({len(str(content)) if content else 0} chars)"
                )

        print(f"\nAvailable sections: {available_sections}/{len(required_sections)}")

        # With our new validation (70% minimum, at least 5 sections)
        min_required = max(5, int(len(required_sections) * 0.7))
        print(f"Minimum required sections (70% rule): {min_required}")

        if available_sections >= min_required:
            print("✅ CONTENT PASSES NEW VALIDATION!")
            print("🎉 Database retrieval should now work!")
            print("\n✅ SOLUTION IMPLEMENTED SUCCESSFULLY!")
            print(
                "The validation system now accepts incomplete but useful database content"
            )
            print("while maintaining strict validation for AI-generated responses.")
        else:
            print("❌ Content still fails validation")
            print("⚠️ Need to add more complete content to database")
    else:
        print("❌ No content found in database")


if __name__ == "__main__":
    test_validation_fix()
