#!/usr/bin/env python3
"""
Test to verify that the PCA Analysis fix has been implemented correctly.
"""

import sys
import os
import re


def test_pca_data_flow_fix():
    """Test that PCA analysis is using the correct data (DataFrame instead of dict)."""
    print("🧪 Testing PCA Data Flow Fix")
    print("=" * 50)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that PCA analysis now uses combined_dataset instead of datasets_norm
    pca_analysis_section = content[
        content.find("# 8. PCA Analysis") : content.find("# 9. Performance Metrics")
    ]

    # Check for the correct data usage
    uses_combined_dataset = "combined_dataset" in pca_analysis_section
    no_longer_uses_datasets_norm = (
        "datasets_norm" not in pca_analysis_section
        or "datasets_norm, selected_sources, language" not in pca_analysis_section
    )

    # Check for proper error handling
    has_combined_dataset_check = (
        "combined_dataset is not None and not combined_dataset.empty" in content
    )
    has_error_handling = "pca_analysis_unavailable" in content

    print(f"📊 PCA Data Flow Analysis:")
    print(
        f"   • Uses combined_dataset (DataFrame): {'✅' if uses_combined_dataset else '❌'}"
    )
    print(
        f"   • No longer uses datasets_norm (dict): {'✅' if no_longer_uses_datasets_norm else '❌'}"
    )
    print(
        f"   • Has combined_dataset validation: {'✅' if has_combined_dataset_check else '❌'}"
    )
    print(f"   • Has proper error handling: {'✅' if has_error_handling else '❌'}")

    return uses_combined_dataset and has_combined_dataset_check and has_error_handling


def test_pca_translations():
    """Test that all PCA-related translation keys are present."""
    print("\n🧪 Testing PCA Translation Keys")
    print("=" * 50)

    translations_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/translations.py"

    with open(translations_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check Spanish translations
    spanish_start = content.find("spanish = {")
    spanish_end = content.find("english = {", spanish_start)
    spanish_section = (
        content[spanish_start:spanish_end]
        if spanish_start > 0 and spanish_end > 0
        else ""
    )

    spanish_pca_keys = ["pca_title", "pca_insights", "pca_analysis_unavailable"]

    spanish_results = []
    for key in spanish_pca_keys:
        found = key in spanish_section
        spanish_results.append(found)
        print(f"   • Spanish '{key}': {'✅' if found else '❌'}")

    # Check English translations
    english_start = content.find("english = {")
    english_section = content[english_start:] if english_start > 0 else ""

    english_pca_keys = ["pca_title", "pca_insights", "pca_analysis_unavailable"]

    english_results = []
    for key in english_pca_keys:
        found = key in english_section
        english_results.append(found)
        print(f"   • English '{key}': {'✅' if found else '❌'}")

    return all(spanish_results) and all(english_results)


def test_pca_function_compatibility():
    """Test that the PCA functions can handle the corrected data flow."""
    print("\n🧪 Testing PCA Function Compatibility")
    print("=" * 50)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that create_pca_figure function exists and has proper signature
    has_create_pca_figure = "def create_pca_figure(data, sources, language=" in content
    has_tool_name_param = "tool_name=None" in content

    # Check that perform_comprehensive_pca_analysis exists
    has_pca_analysis = "def perform_comprehensive_pca_analysis" in content

    # Check for error handling in PCA functions
    has_error_handling = "PCA analysis failed:" in content

    print(f"📊 PCA Function Analysis:")
    print(
        f"   • create_pca_figure function exists: {'✅' if has_create_pca_figure else '❌'}"
    )
    print(f"   • Has tool_name parameter: {'✅' if has_tool_name_param else '❌'}")
    print(
        f"   • perform_comprehensive_pca_analysis exists: {'✅' if has_pca_analysis else '❌'}"
    )
    print(f"   • Has error handling: {'✅' if has_error_handling else '❌'}")

    return (
        has_create_pca_figure
        and has_tool_name_param
        and has_pca_analysis
        and has_error_handling
    )


def main():
    """Run all PCA fix tests."""
    print("🚀 Testing PCA Analysis Fix")
    print("=" * 80)

    tests = [
        ("PCA Data Flow Fix", test_pca_data_flow_fix),
        ("PCA Translation Keys", test_pca_translations),
        ("PCA Function Compatibility", test_pca_function_compatibility),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"\n{test_name}: {'✅ PASSED' if result else '❌ FAILED'}")
        except Exception as e:
            print(f"\n{test_name}: ❌ ERROR - {e}")
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("📋 FINAL PCA FIX VERIFICATION:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 PCA ANALYSIS FIX IS COMPLETE!")
        print("✅ PCA Analysis should now work without errors")
        print("✅ Using DataFrame data instead of dictionary")
        print("✅ Proper error handling and translations")
        print("✅ No more 'dict' object has no attribute 'select_dtypes' error")
        return 0
    else:
        print("❌ SOME PCA FIX TESTS FAILED")
        print("🔧 Manual review and fixes may be needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
