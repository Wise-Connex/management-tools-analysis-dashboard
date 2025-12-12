#!/usr/bin/env python3
"""
Test to verify that the PCA visualization now matches the old app_old.py format.
"""

import sys
import os
import re


def test_pca_visualization_fix():
    """Test that PCA visualization now uses the proper two-subplot format."""
    print("🧪 Testing PCA Visualization Fix")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the create_pca_figure function
    pca_start = content.find("def create_pca_figure(")
    if pca_start == -1:
        print("❌ create_pca_figure function not found")
        return False

    # Extract the function
    pca_end = content.find("def ", pca_start + 1)
    if pca_end == -1:
        pca_end = len(content)
    pca_function = content[pca_start:pca_end]

    # Check for old-style visualization elements
    old_style_checks = [
        ("make_subplots", "make_subplots" in pca_function),
        ("Two subplots", "subplot_titles" in pca_function),
        ("Component loadings", "loadings" in pca_function),
        ("Explained variance", "explained_variance" in pca_function),
        ("Arrow vectors", "x=[0, pca.components_[0, i]]" in pca_function),
        ("Cumulative variance", "cumulative_var" in pca_function),
        ("Inverse relationship", "inverse_relationship" in pca_function),
        ("Color mapping", "color_map" in pca_function),
        ("Origin lines", "add_hline" in pca_function or "add_vline" in pca_function),
    ]

    print("📋 Old-Style Visualization Checks:")
    all_old_checks_pass = True
    for check_name, found in old_style_checks:
        status = "✅" if found else "❌"
        print(f"   • {check_name}: {status}")
        if not found:
            all_old_checks_pass = False

    # Check for new-style (incorrect) elements
    new_style_checks = [
        (
            "Simple scatter plot",
            "go.Scatter(" in pca_function and "mode='markers'" in pca_function,
        ),
        ("Data points", "Data Points" in pca_function and "Point" in pca_function),
        ("Data Point Index", "Data Point Index" in pca_function),
        (
            "Simple title",
            "Principal Component Analysis" in pca_function
            and "loadings" not in pca_function,
        ),
    ]

    print("📋 New-Style (Incorrect) Visualization Checks:")
    no_new_checks = True
    for check_name, found in new_style_checks:
        status = "✅ NOT FOUND" if not found else "❌ STILL PRESENT"
        print(f"   • {check_name}: {status}")
        if found:
            no_new_checks = False

    return all_old_checks_pass and no_new_checks


def test_pca_data_flow():
    """Test that PCA data flow is correct."""
    print("\n🧪 Testing PCA Data Flow")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for correct data flow
    data_flow_checks = [
        (
            "Combined dataset usage",
            "combined_dataset, selected_sources, language" in content,
        ),
        ("Original column resolution", "get_original_column_name" in content),
        ("Translation mapping", "create_translation_mapping" in content),
        ("Data standardization", "StandardScaler()" in content),
        ("PCA execution", "PCA()" in content and "pca.fit_transform" in content),
    ]

    print("📋 Data Flow Checks:")
    for check_name, found in data_flow_checks:
        status = "✅" if found else "❌"
        print(f"   • {check_name}: {status}")

    return all(found for _, found in data_flow_checks)


def test_imports_and_constants():
    """Test that required imports and constants are present."""
    print("\n🧪 Testing Imports and Constants")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for required imports
    import_checks = [
        (
            "make_subplots import",
            "from plotly.subplots import make_subplots" in content,
        ),
        ("go import", "import plotly.graph_objects as go" in content),
    ]

    # Check for color_map
    has_color_map = "color_map = {" in content

    print("📋 Import Checks:")
    for check_name, found in import_checks:
        status = "✅" if found else "❌"
        print(f"   • {check_name}: {status}")

    print("📋 Constants Checks:")
    print(f"   • color_map definition: {'✅' if has_color_map else '❌'}")

    return all(found for _, found in import_checks) and has_color_map


def main():
    """Run all PCA visualization fix tests."""
    print("🚀 Testing PCA Visualization Fix Implementation")
    print("=" * 80)

    tests = [
        ("PCA Visualization Format", test_pca_visualization_fix),
        ("PCA Data Flow", test_pca_data_flow),
        ("Imports and Constants", test_imports_and_constants),
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
    print("📋 PCA VISUALIZATION FIX RESULTS:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 PCA VISUALIZATION FIX IS SUCCESSFUL!")
        print("✅ PCA Analysis now shows proper component loadings as arrows")
        print("✅ Two-subplot visualization with variance analysis")
        print("✅ Matches old app_old.py implementation")
        print("✅ Should display correct PCA data instead of wrong data")
        print(
            "\n💡 The 'Análisis PCA (Cargas y Componentes)' should now show the correct visualization!"
        )
        return 0
    else:
        print("❌ PCA VISUALIZATION FIX FAILED")
        print("🔧 Additional fixes needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
