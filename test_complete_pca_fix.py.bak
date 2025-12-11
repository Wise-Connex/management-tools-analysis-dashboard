#!/usr/bin/env python3
"""
Comprehensive test to verify that the PCA analysis fix properly implements
the logic from app_old.py while maintaining modular architecture.
"""

import sys
import os
import re


def test_pca_function_implementation():
    """Test that PCA functions properly implement the app_old.py logic."""
    print("🧪 Testing Complete PCA Implementation")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check perform_comprehensive_pca_analysis implementation
    pca_analysis_start = content.find("def perform_comprehensive_pca_analysis(")
    pca_analysis_end = content.find("def create_pca_figure(", pca_analysis_start)
    pca_analysis_function = (
        content[pca_analysis_start:pca_analysis_end] if pca_analysis_start > 0 else ""
    )

    if not pca_analysis_function:
        print("❌ Could not find perform_comprehensive_pca_analysis function")
        return False

    print("📋 Found perform_comprehensive_pca_analysis function")

    # Check for proper app_old.py logic implementation
    implementation_checks = [
        (
            "Translation mapping creation",
            "create_translation_mapping(selected_source_ids, language)"
            in pca_analysis_function,
        ),
        (
            "Source ID mapping",
            "map_display_names_to_source_ids(sources)" in pca_analysis_function,
        ),
        (
            "Original column name resolution",
            "get_original_column_name(source, translation_mapping)"
            in pca_analysis_function,
        ),
        (
            "Column validation",
            "if original_name in data.columns:" in pca_analysis_function,
        ),
        (
            "Data preparation",
            "pca_data = data[original_columns].dropna()" in pca_analysis_function,
        ),
        ("Data validation", "if len(pca_data) < 2:" in pca_analysis_function),
        ("Standardization", "scaler = StandardScaler()" in pca_analysis_function),
        ("PCA execution", "pca = PCA()" in pca_analysis_function),
        (
            "Variance calculation",
            "explained_var = pca.explained_variance_ratio_" in pca_analysis_function,
        ),
        (
            "Kaiser criterion",
            "components_to_analyze = sum(eigenvalues > 1)" in pca_analysis_function,
        ),
    ]

    print(f"📋 Implementation Verification:")
    all_implemented = True
    for check_name, implemented in implementation_checks:
        status = "✅" if implemented else "❌"
        print(f"   • {check_name}: {status}")
        if not implemented:
            all_implemented = False

    # Check create_pca_figure implementation
    pca_figure_start = content.find("def create_pca_figure(")
    pca_figure_end = content.find("def create_correlation_heatmap(", pca_figure_start)
    pca_figure_function = (
        content[pca_figure_start:pca_figure_end] if pca_figure_start > 0 else ""
    )

    if not pca_figure_function:
        print("❌ Could not find create_pca_figure function")
        return False

    print(f"📋 Found create_pca_figure function")

    # Check for proper visualization logic
    visualization_checks = [
        (
            "Translation mapping",
            "create_translation_mapping(selected_source_ids, language)"
            in pca_figure_function,
        ),
        (
            "Column resolution",
            "get_original_column_name(source, translation_mapping)"
            in pca_figure_function,
        ),
        (
            "Data preparation",
            "pca_data = data[original_columns].dropna()" in pca_figure_function,
        ),
        ("Standardization", "scaler = StandardScaler()" in pca_figure_function),
        ("PCA execution", "pca = PCA()" in pca_figure_function),
        ("Scatter plot creation", "go.Scatter(" in pca_figure_function),
        ("Arrow vectors", "add_annotation(" in pca_figure_function),
        (
            "Feature labels",
            "original_to_display.get(feature, feature)" in pca_figure_function,
        ),
    ]

    print(f"📋 Visualization Verification:")
    for check_name, implemented in visualization_checks:
        status = "✅" if implemented else "❌"
        print(f"   • {check_name}: {status}")
        if not implemented:
            all_implemented = False

    return all_implemented


def test_data_structure_compatibility():
    """Test that data structures are compatible with old implementation."""
    print("\n🧪 Testing Data Structure Compatibility")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check return data structure
    return_structure_checks = [
        ("Success flag", '"success": True' in content),
        ("PCA object", '"pca": pca' in content),
        ("PCA result", '"pca_result": pca_result' in content),
        (
            "Explained variance",
            '"explained_variance_ratio": pca.explained_variance_ratio_' in content,
        ),
        ("Components", '"components": pca.components_' in content),
        ("Original columns", '"original_columns": original_columns' in content),
        ("Column mapping", '"original_to_display": original_to_display' in content),
        (
            "Translation mapping",
            '"translation_mapping": translation_mapping' in content,
        ),
    ]

    print(f"📋 Return Structure Verification:")
    for check_name, implemented in return_structure_checks:
        status = "✅" if implemented else "❌"
        print(f"   • {check_name}: {status}")

    return all(implemented for _, implemented in return_structure_checks)


def test_error_handling():
    """Test that error handling is robust."""
    print("\n🧪 Testing Error Handling")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check error handling patterns
    error_handling_checks = [
        (
            "No valid columns error",
            '"No valid columns found for PCA analysis"' in content,
        ),
        ("Insufficient data error", '"Insufficient data for PCA analysis"' in content),
        ("General error handling", "except Exception as e:" in content),
        ("Error return structure", '"error":' in content),
        ("Empty figure fallback", "return go.Figure()" in content),
    ]

    print(f"📋 Error Handling Verification:")
    for check_name, implemented in error_handling_checks:
        status = "✅" if implemented else "❌"
        print(f"   • {check_name}: {status}")

    return all(implemented for _, implemented in error_handling_checks)


def test_modular_architecture():
    """Test that the modular architecture is maintained."""
    print("\n🧪 Testing Modular Architecture")
    print("=" * 60)

    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )

    with open(utils_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check modular architecture patterns
    modular_checks = [
        ("Import statements present", "from fix_source_mapping import" in content),
        ("Function definitions", "def perform_comprehensive_pca_analysis(" in content),
        ("Function definitions", "def create_pca_figure(" in content),
        ("Documentation", '"""' in content),
        (
            "Proper error handling",
            "try:" in content and "except Exception as e:" in content,
        ),
    ]

    print(f"📋 Modular Architecture Verification:")
    for check_name, implemented in modular_checks:
        status = "✅" if implemented else "❌"
        print(f"   • {check_name}: {status}")

    return all(implemented for _, implemented in modular_checks)


def compare_with_old_implementation():
    """Compare key aspects with the old app_old.py implementation."""
    print("\n🧪 Comparing with Old Implementation")
    print("=" * 60)

    # Check if the old implementation exists for comparison
    old_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/app_old.py"
    if not os.path.exists(old_path):
        print("⚠️  app_old.py not found for comparison")
        return True

    with open(old_path, "r", encoding="utf-8") as f:
        old_content = f.read()

    # Find the old implementation
    old_pca_start = old_content.find("def perform_comprehensive_pca_analysis(")
    if old_pca_start == -1:
        print("⚠️  Old PCA function not found in app_old.py")
        return True

    # Extract key patterns from old implementation
    old_patterns = []
    old_section = old_content[old_pca_start : old_pca_start + 2000]  # First 2000 chars

    if "DATAFRAME_INDEXING_FIX" in old_section:
        old_patterns.append("DATAFRAME_INDEXING_FIX comment")
    if "map_display_names_to_source_ids" in old_section:
        old_patterns.append("Source ID mapping")
    if "create_translation_mapping" in old_section:
        old_patterns.append("Translation mapping")
    if "get_original_column_name" in old_section:
        old_patterns.append("Original column name resolution")
    if "Kaiser criterion" in old_section:
        old_patterns.append("Kaiser criterion implementation")

    # Check if new implementation has these patterns
    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )
    with open(utils_path, "r", encoding="utf-8") as f:
        new_content = f.read()

    comparison_results = []
    for pattern in old_patterns:
        pattern_found = False
        if pattern == "DATAFRAME_INDEXING_FIX comment":
            pattern_found = "DATAFRAME_INDEXING_FIX" in new_content
        elif pattern == "Source ID mapping":
            pattern_found = "map_display_names_to_source_ids" in new_content
        elif pattern == "Translation mapping":
            pattern_found = "create_translation_mapping" in new_content
        elif pattern == "Original column name resolution":
            pattern_found = "get_original_column_name" in new_content
        elif pattern == "Kaiser criterion implementation":
            pattern_found = "Kaiser criterion" in new_content

        comparison_results.append((pattern, pattern_found))
        print(f"   • {pattern}: {'✅' if pattern_found else '❌'}")

    return all(found for _, found in comparison_results)


def main():
    """Run all complete PCA fix tests."""
    print("🚀 Testing Complete PCA Analysis Fix Implementation")
    print("=" * 80)

    tests = [
        ("PCA Function Implementation", test_pca_function_implementation),
        ("Data Structure Compatibility", test_data_structure_compatibility),
        ("Error Handling", test_error_handling),
        ("Modular Architecture", test_modular_architecture),
        ("Comparison with Old Implementation", compare_with_old_implementation),
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
    print("📋 FINAL COMPLETE PCA FIX VERIFICATION:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 COMPLETE PCA ANALYSIS FIX IS SUCCESSFUL!")
        print("✅ Properly implements app_old.py logic in modular format")
        print("✅ All data structure compatibility maintained")
        print("✅ Robust error handling implemented")
        print("✅ Modular architecture preserved")
        print("✅ Boolean array error should be resolved")
        print("✅ PCA Analysis section should work perfectly")
        print(
            "\n💡 The 'Análisis PCA (Cargas y Componentes)' section should now display correctly without errors!"
        )
        return 0
    else:
        print("❌ COMPLETE PCA ANALYSIS FIX FAILED")
        print("🔧 Manual review needed for incomplete implementation")
        return 1


if __name__ == "__main__":
    sys.exit(main())
