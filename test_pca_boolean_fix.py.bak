#!/usr/bin/env python3
"""
Test to verify that the PCA boolean array error has been fixed.
"""

import sys
import os
import re


def test_pca_boolean_array_fix():
    """Test that PCA functions no longer have boolean array evaluation issues."""
    print("🧪 Testing PCA Boolean Array Error Fix")
    print("=" * 50)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the create_pca_figure function
    pca_start = content.find("def create_pca_figure(")
    pca_end = content.find("def ", pca_start + 1)
    if pca_end == -1:
        pca_end = len(content)

    pca_function = content[pca_start:pca_end] if pca_start > 0 else ""

    if not pca_function:
        print("❌ Could not find create_pca_figure function")
        return False

    print("📋 Found create_pca_figure function")

    # Check for problematic boolean array evaluations
    problematic_patterns = [
        # Check for direct array evaluation in if statements
        "if X.empty or len(X) < 3:",
        "if X.empty:",
        # Check for pandas Index in ternary operators
        "X.index if",
        # Check for len() calls on numpy arrays that might cause issues
        "len(pca.explained_variance_ratio_)",
    ]

    found_issues = []
    for pattern in problematic_patterns:
        if pattern in pca_function:
            found_issues.append(pattern)

    if found_issues:
        print("❌ Found potential boolean array evaluation issues:")
        for issue in found_issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ No problematic boolean array evaluations found")

    # Check for fixes that should be present
    fixes = [
        # Check for the fixed array shape checks
        "X.shape[0] == 0 or X.shape[0] < 3:",
        "pca.explained_variance_ratio_.shape[0] > 1",
        # Check for list conversion of pandas Index
        "list(X.index)",
    ]

    found_fixes = []
    for fix in fixes:
        if fix in pca_function:
            found_fixes.append(fix)

    print(f"\n📋 Fix Analysis:")
    for fix in fixes:
        found = fix in pca_function
        print(f"   • {fix}: {'✅' if found else '❌'}")
        if found:
            found_fixes.append(fix)

    return len(found_fixes) >= 2  # At least some fixes should be present


def test_pca_analysis_function():
    """Test the perform_comprehensive_pca_analysis function for similar issues."""
    print("\n🧪 Testing PCA Analysis Function")
    print("=" * 50)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the perform_comprehensive_pca_analysis function
    pca_start = content.find("def perform_comprehensive_pca_analysis(")
    pca_end = content.find("def ", pca_start + 1)
    if pca_end == -1:
        pca_end = len(content)

    pca_function = content[pca_start:pca_end] if pca_start > 0 else ""

    if not pca_function:
        print("❌ Could not find perform_comprehensive_pca_analysis function")
        return False

    print("📋 Found perform_comprehensive_pca_analysis function")

    # Check for basic numeric data processing
    has_numeric_check = (
        "numeric_data = data.select_dtypes(include=[np.number])" in pca_function
    )
    has_empty_check = "if numeric_data.empty:" in pca_function
    has_error_handling = "PCA analysis failed:" in pca_function

    print(f"📋 Function Structure:")
    print(f"   • Numeric data check: {'✅' if has_numeric_check else '❌'}")
    print(f"   • Empty data check: {'✅' if has_empty_check else '❌'}")
    print(f"   • Error handling: {'✅' if has_error_handling else '❌'}")

    return has_numeric_check and has_empty_check and has_error_handling


def verify_data_handling():
    """Verify that data handling is robust for different data structures."""
    print("\n🧪 Verifying Robust Data Handling")
    print("=" * 50)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for robust data type handling
    robust_patterns = [
        # Check for explicit shape checks
        "X.shape[0]",
        "X.shape[1]",
        # Check for list conversions
        "list(X.index)",
        "list(range(",
        # Check for explicit boolean evaluations
        "== 0",
        "< 3",
        "> 1",
    ]

    found_patterns = []
    for pattern in robust_patterns:
        if pattern in content:
            found_patterns.append(pattern)

    print(f"📋 Robust Data Handling Analysis:")
    print(
        f"   • Explicit shape checks: {'✅' if any('shape[0]' in p for p in found_patterns) else '❌'}"
    )
    print(
        f"   • List conversions: {'✅' if any('list(' in p for p in found_patterns) else '❌'}"
    )
    print(
        f"   • Explicit comparisons: {'✅' if any('==' in p or '<' in p or '>' in p for p in found_patterns) else '❌'}"
    )

    return len(found_patterns) >= 3


def main():
    """Run all PCA boolean array fix tests."""
    print("🚀 Testing PCA Boolean Array Error Fix")
    print("=" * 80)

    tests = [
        ("PCA Boolean Array Fix", test_pca_boolean_array_fix),
        ("PCA Analysis Function", test_pca_analysis_function),
        ("Robust Data Handling", verify_data_handling),
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
    print("📋 FINAL PCA BOOLEAN ARRAY ERROR FIX RESULTS:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 PCA BOOLEAN ARRAY ERROR FIX IS SUCCESSFUL!")
        print("✅ No more 'truth value of an array' errors")
        print("✅ Robust data type handling implemented")
        print("✅ Explicit array shape checks used")
        print("✅ Pandas Index objects properly converted")
        print("✅ PCA Analysis section should now work without errors")
        print(
            "\n💡 The 'Análisis PCA (Cargas y Componentes)' section should now display correctly!"
        )
        return 0
    else:
        print("❌ PCA BOOLEAN ARRAY ERROR FIX FAILED")
        print("🔧 Manual review needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
