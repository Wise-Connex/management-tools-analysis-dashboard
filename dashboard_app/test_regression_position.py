#!/usr/bin/env python3
"""
Test script to verify that regression analysis comes right after correlation heatmap
in both English and Spanish versions for multiple sources.
"""


def test_regression_position():
    """Test that regression section is positioned correctly after correlation heatmap"""

    print("🔍 TESTING REGRESSION ANALYSIS POSITION")
    print("=" * 50)

    try:
        # Read the main callback file to verify section order
        with open("callbacks/main_callbacks.py", "r") as f:
            content = f.read()

        # Find the order of sections
        sections = [
            ("Temporal 2D", "temporal_analysis_2d"),
            ("Mean Analysis", "mean_analysis_title"),
            ("Temporal 3D", "temporal_3d_title"),
            ("Correlation Heatmap", "correlation_heatmap_title"),
            ("Seasonal Analysis", "seasonal_analysis"),
            ("Fourier Analysis", "fourier_analysis"),
            ("Regression Analysis", "regression_title"),
            ("PCA Analysis", "pca_title"),
            ("Data Table", "data_table_title"),
        ]

        # Find positions of each section
        positions = {}
        for section_name, translation_key in sections:
            pos = content.find(translation_key)
            if pos != -1:
                positions[section_name] = pos

        # Sort by position to get the actual order
        sorted_sections = sorted(positions.items(), key=lambda x: x[1])

        print("📋 CURRENT SECTION ORDER:")
        for i, (section_name, position) in enumerate(sorted_sections, 1):
            print(f"   {i}. {section_name}")

        # Check if regression comes right after correlation heatmap
        correlation_pos = positions.get("Correlation Heatmap", -1)
        regression_pos = positions.get("Regression Analysis", -1)
        seasonal_pos = positions.get("Seasonal Analysis", -1)

        print(f"\n🔍 POSITION ANALYSIS:")
        print(f"   Correlation Heatmap position: {correlation_pos}")
        print(f"   Regression Analysis position: {regression_pos}")
        print(f"   Seasonal Analysis position: {seasonal_pos}")

        # Verify correct order
        if correlation_pos < regression_pos < seasonal_pos:
            print("✅ CORRECT ORDER: Correlation → Regression → Seasonal")
        elif correlation_pos < seasonal_pos < regression_pos:
            print("❌ INCORRECT ORDER: Correlation → Seasonal → Regression")
            print("   REGRESSION SHOULD COME RIGHT AFTER CORRELATION HEATMAP")
        else:
            print("⚠️  UNEXPECTED ORDER DETECTED")

        # Check conditional logic
        print(f"\n🔍 CONDITIONAL LOGIC CHECK:")
        correlation_section = (
            content[correlation_pos : correlation_pos + 500]
            if correlation_pos != -1
            else ""
        )
        regression_section = (
            content[regression_pos : regression_pos + 300]
            if regression_pos != -1
            else ""
        )

        if "if len(selected_sources) > 1:" in correlation_section:
            print("   ✅ Correlation Heatmap: Has conditional for multiple sources")
        else:
            print("   ❌ Correlation Heatmap: Missing conditional")

        if "if len(selected_sources) > 1:" in regression_section:
            print("   ✅ Regression Analysis: Has conditional for multiple sources")
        else:
            print("   ❌ Regression Analysis: Missing conditional")

        # Test translations
        try:
            from translations import get_text

            print(f"\n🔍 TRANSLATION VERIFICATION:")
            spanish_regression = get_text("regression_title", "es")
            english_regression = get_text("regression_title", "en")

            print(f"   Spanish Regression: {spanish_regression}")
            print(f"   English Regression: {english_regression}")

            if (
                "regresión" in spanish_regression.lower()
                or "regression" in english_regression.lower()
            ):
                print("   ✅ Translations working correctly")
            else:
                print("   ❌ Translation issues detected")

        except Exception as e:
            print(f"   ❌ Translation test failed: {e}")

        print(f"\n🎯 EXPECTED BEHAVIOR FOR 2+ SOURCES:")
        print("   1. Temporal Analysis 2D (always)")
        print("   2. Mean Analysis (always)")
        print("   3. Temporal Analysis 3D (2+ sources)")
        print("   4. Correlation Heatmap (2+ sources)")
        print("   5. Regression Analysis (2+ sources) ← RIGHT AFTER HEATMAP")
        print("   6. Seasonal Analysis (always)")
        print("   7. Fourier Analysis (always)")
        print("   8. PCA Analysis (2+ sources)")
        print("   9. Data Table (always)")

        if correlation_pos < regression_pos < seasonal_pos:
            print(f"\n✅ REGRESSION POSITION: CORRECT")
            print(
                f"✅ Regression analysis is positioned right after correlation heatmap"
            )
            return True
        else:
            print(f"\n❌ REGRESSION POSITION: INCORRECT")
            print(f"❌ Regression analysis should come right after correlation heatmap")
            return False

    except Exception as e:
        print(f"❌ Error testing regression position: {e}")
        return False


if __name__ == "__main__":
    test_regression_position()
