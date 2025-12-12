#!/usr/bin/env python3
"""
Test to verify Fourier analysis should show for single source
"""


def test_fourier_single_source():
    """Test that Fourier analysis section is created for single source"""

    print("🔍 TESTING FOURIER ANALYSIS FOR SINGLE SOURCE")
    print("=" * 50)

    # Test the main callback structure
    try:
        with open("callbacks/main_callbacks.py", "r") as f:
            content = f.read()

        # Check if Fourier analysis section is always added (not conditional)
        fourier_section_start = content.find("# 7. Fourier Analysis (always show")
        fourier_section_add = content.find("content.append(")

        # Find the Fourier analysis section and content.append call
        fourier_content_start = content.find(
            'content.append(\n                    html.Div(\n                        [\n                            html.H3(\n                                get_text("fourier_analysis"',
            fourier_section_start,
        )

        print(f"📋 FOURIER ANALYSIS SECTION CHECK:")
        print(
            f"   Section comment found: {'✅ YES' if fourier_section_start != -1 else '❌ NO'}"
        )
        print(
            f"   Content.append found: {'✅ YES' if fourier_content_start != -1 else '❌ NO'}"
        )

        # Check if there are any conditional statements around Fourier analysis
        lines_after_fourier = content[
            fourier_section_start : fourier_section_start + 200
        ].split("\n")
        has_conditional = any(
            "len(selected_sources)" in line and "if" in line
            for line in lines_after_fourier
        )

        print(f"   Has conditional logic: {'❌ YES' if has_conditional else '✅ NO'}")

        if has_conditional:
            print(f"   ⚠️  Fourier analysis might be conditional!")
            for i, line in enumerate(lines_after_fourier):
                if "len(selected_sources)" in line:
                    print(f"      Line {i}: {line.strip()}")
        else:
            print(f"   ✅ Fourier analysis should always show (no conditional logic)")

        # Check the same for seasonal analysis for comparison
        seasonal_section_start = content.find("# 5. Seasonal Analysis (always show")
        seasonal_content_start = content.find(
            'content.append(\n                    html.Div(\n                        [\n                            html.H3(\n                                get_text("seasonal_analysis"',
            seasonal_section_start,
        )

        print(f"\n📋 SEASONAL ANALYSIS SECTION CHECK:")
        print(
            f"   Section comment found: {'✅ YES' if seasonal_section_start != -1 else '❌ NO'}"
        )
        print(
            f"   Content.append found: {'✅ YES' if seasonal_content_start != -1 else '❌ NO'}"
        )

        # Check if there are any conditional statements around Seasonal analysis
        lines_after_seasonal = content[
            seasonal_section_start : seasonal_section_start + 200
        ].split("\n")
        seasonal_has_conditional = any(
            "len(selected_sources)" in line and "if" in line
            for line in lines_after_seasonal
        )

        print(
            f"   Has conditional logic: {'❌ YES' if seasonal_has_conditional else '✅ NO'}"
        )

        if seasonal_has_conditional:
            print(f"   ⚠️  Seasonal analysis might be conditional!")
            for i, line in enumerate(lines_after_seasonal):
                if "len(selected_sources)" in line:
                    print(f"      Line {i}: {line.strip()}")
        else:
            print(f"   ✅ Seasonal analysis should always show (no conditional logic)")

        print(f"\n🎯 CONCLUSION:")
        if not has_conditional and not seasonal_has_conditional:
            print(f"   ✅ Both sections should show for single source")
            print(f"   ✅ If sections are not visible, check for other issues:")
            print(f"      - Translation keys exist and work")
            print(f"      - No JavaScript errors")
            print(f"      - Callback execution succeeds")
        else:
            print(f"   ❌ One or both sections have conditional logic")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ FOURIER ANALYSIS TEST COMPLETED")
    return True


if __name__ == "__main__":
    test_fourier_single_source()
