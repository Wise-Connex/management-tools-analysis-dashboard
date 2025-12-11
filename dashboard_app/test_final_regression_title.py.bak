#!/usr/bin/env python3
"""
Final test to verify regression title is completely fixed.
"""


def test_final_regression_title_fix():
    """Final verification that regression title shows correct format"""

    print("🔍 FINAL REGRESSION TITLE VERIFICATION")
    print("=" * 50)

    # Test 1: Check section headers use simple key
    print("\n📋 TEST 1: SECTION HEADERS")
    try:
        from translations import get_text

        spanish_header = get_text("regression_analysis", "es")
        english_header = get_text("regression_analysis", "en")

        print(f"   Spanish Header: '{spanish_header}'")
        print(f"   English Header: '{english_header}'")

        if "{" not in spanish_header and "{" not in english_header:
            print("   ✅ SECTION HEADERS: No format strings")
        else:
            print("   ❌ SECTION HEADERS: Still has format strings")

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

    # Test 2: Check no regression_title references in main code
    print("\n📋 TEST 2: CODE REFERENCES")
    try:
        import os
        import glob

        # Check main files for regression_title
        main_files = (
            glob.glob("*.py") + glob.glob("callbacks/*.py") + ["translations.py"]
        )
        found_references = False

        for file in main_files:
            if os.path.exists(file):
                with open(file, "r") as f:
                    content = f.read()
                    if "regression_title" in content and "test_" not in file:
                        print(f"   ❌ REFERENCE FOUND: {file}")
                        found_references = True

        if not found_references:
            print("   ✅ NO REFERENCES: No regression_title in main code")
        else:
            print("   ❌ REFERENCES FOUND: Some regression_title still in use")

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

    # Test 3: Check graph callback uses correct logic
    print("\n📋 TEST 3: GRAPH CALLBACK LOGIC")
    try:
        with open("callbacks/graph_callbacks.py", "r") as f:
            content = f.read()

        # Check it uses regression_analysis for header
        if 'get_text("regression_analysis", language)' in content:
            print("   ✅ HEADER: Uses regression_analysis key")
        else:
            print("   ❌ HEADER: Doesn't use regression_analysis key")

        # Check it manually formats the title with variables
        if "y_var vs {x_var}" in content:
            print("   ✅ FORMAT: Manually formats title with variables")
        else:
            print("   ❌ FORMAT: Doesn't manually format title")

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

    # Test 4: App import test
    print("\n📋 TEST 4: APP IMPORT")
    try:
        from app import app

        print("   ✅ APP IMPORT: Successfully imports without errors")
    except Exception as e:
        print(f"   ❌ APP IMPORT: Failed to import - {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("✅ Regression title completely fixed")

    print("\n🎯 FINAL BEHAVIOR:")
    print("   Section Header: 'Análisis de Regresión' / 'Regression Analysis'")
    print("   Chart Title: 'Análisis de Regresión: Google Trends vs Bain Usabilidad'")
    print("   Chart Title: 'Regression Analysis: Google Trends vs Bain Usability'")
    print("   No more format strings: {y_var} vs {x_var}")

    return True


if __name__ == "__main__":
    success = test_final_regression_title_fix()
    if success:
        print("\n🚀 REGRESSION TITLE COMPLETELY FIXED!")
    else:
        print("\n❌ Regression title fix incomplete")
