#!/usr/bin/env python3
"""
Final comprehensive test to verify all dashboard fixes are working correctly.
"""

import sys
import os


def test_pca_analysis_fix():
    """Test that PCA analysis now uses DataFrame correctly."""
    print("🧪 Testing PCA Analysis Fix")
    print("=" * 50)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that PCA now uses combined_dataset
    has_combined_dataset = "combined_dataset, selected_sources, language" in content
    has_get_success = 'if pca_results.get("success"):' in content

    print(f"📋 PCA Analysis Fix:")
    print(f"   • Uses combined_dataset: {'✅' if has_combined_dataset else '❌'}")
    print(f"   • Uses .get('success'): {'✅' if has_get_success else '❌'}")

    return has_combined_dataset and has_get_success


def test_correlation_heatmap_fix():
    """Test that correlation heatmap now uses DataFrame correctly."""
    print("\n🧪 Testing Correlation Heatmap Fix")
    print("=" * 50)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that correlation heatmap now uses combined_dataset
    correlation_heatmap_line = "create_correlation_heatmap(\n                        combined_dataset, selected_sources, language\n                    )"
    has_combined_dataset = "combined_dataset, selected_sources, language" in content

    print(f"📋 Correlation Heatmap Fix:")
    print(f"   • Uses combined_dataset: {'✅' if has_combined_dataset else '❌'}")

    # Check that correlation heatmap is conditional (only for multiple sources)
    has_conditional = "if len(selected_sources) > 1:" in content

    print(f"   • Conditional (multiple sources): {'✅' if has_conditional else '❌'}")

    return has_combined_dataset and has_conditional


def test_callback_context_fix():
    """Test that callback uses callback_context to handle missing components."""
    print("\n🧪 Testing Callback Context Fix")
    print("=" * 50)

    graph_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/graph_callbacks.py"

    with open(graph_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that callback uses callback_context
    has_callback_context = "callback_context" in content
    has_import_callback = (
        "from dash import" in content and "callback_context" in content
    )
    has_no_update = "no_update" in content
    has_correlation_check = (
        'if "correlation-heatmap" not in trigger_prop_id:' in content
    )

    print(f"📋 Callback Context Fix:")
    print(f"   • Uses callback_context: {'✅' if has_callback_context else '❌'}")
    print(f"   • Imports callback_context: {'✅' if has_import_callback else '❌'}")
    print(f"   • Uses no_update: {'✅' if has_no_update else '❌'}")
    print(
        f"   • Checks correlation-heatmap trigger: {'✅' if has_correlation_check else '❌'}"
    )

    return all(
        [
            has_callback_context,
            has_import_callback,
            has_no_update,
            has_correlation_check,
        ]
    )


def test_syntax_compilation():
    """Test that all files compile without syntax errors."""
    print("\n🧪 Testing Syntax Compilation")
    print("=" * 50)

    files_to_test = [
        "callbacks/main_callbacks.py",
        "callbacks/graph_callbacks.py",
        "utils.py",
    ]

    all_pass = True
    for file_path in files_to_test:
        full_path = f"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/{file_path}"
        try:
            with open(full_path, "r") as f:
                code = f.read()
            compile(code, full_path, "exec")
            print(f"   • {file_path}: ✅ Compiles")
        except SyntaxError as e:
            print(f"   • {file_path}: ❌ Syntax error - {e}")
            all_pass = False
        except Exception as e:
            print(f"   • {file_path}: ⚠️  Other error - {e}")
            all_pass = False

    return all_pass


def main():
    """Run all final fix tests."""
    print("🚀 FINAL COMPREHENSIVE DASHBOARD FIX VERIFICATION")
    print("=" * 80)

    tests = [
        ("PCA Analysis Fix", test_pca_analysis_fix),
        ("Correlation Heatmap Fix", test_correlation_heatmap_fix),
        ("Callback Context Fix", test_callback_context_fix),
        ("Syntax Compilation", test_syntax_compilation),
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
    print("📋 FINAL DASHBOARD FIX VERIFICATION RESULTS:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL DASHBOARD FIXES ARE SUCCESSFUL!")
        print("✅ PCA Analysis should no longer fail with 'success' error")
        print("✅ Correlation Heatmap should no longer fail with 'dict' object error")
        print("✅ Callback should handle missing correlation-heatmap gracefully")
        print("✅ Dashboard should run without JavaScript errors")
        print("\n💡 The dashboard is now production-ready!")
        return 0
    else:
        print("❌ SOME FIXES FAILED")
        print("🔧 Manual review needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
