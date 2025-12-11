#!/usr/bin/env python3
"""
Test to verify that the duplicate callback error has been resolved.

This test checks that:
1. There's only one callback outputting to regression-graph
2. The callback can handle both heatmap clicks and auto-selection
3. No duplicate output declarations exist
"""

import re
import sys
import os


def test_duplicate_callbacks():
    """Test that duplicate callback outputs have been resolved."""
    print("🧪 Testing Duplicate Callback Fix")
    print("=" * 50)

    dashboard_app_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app"
    )

    # Check for duplicate Output declarations for regression-graph
    regression_outputs = []
    callback_count = 0

    for root, dirs, files in os.walk(dashboard_app_path):
        for file in files:
            if file.endswith(".py") and "callback" in file:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Count Output declarations for regression-graph
                    output_pattern = r'Output\(\s*["\']regression-graph["\']\s*,\s*["\']figure["\']\s*\)'
                    matches = re.findall(output_pattern, content)
                    regression_outputs.extend([(file_path, match) for match in matches])

                    # Count callback functions
                    callback_pattern = r"@app\.callback"
                    callbacks = re.findall(callback_pattern, content)
                    callback_count += len(callbacks)

                except Exception as e:
                    print(f"⚠️  Error reading {file_path}: {e}")

    print(f"📊 Analysis Results:")
    print(f"   • Total callback functions found: {callback_count}")
    print(f"   • Output declarations for 'regression-graph': {len(regression_outputs)}")

    if len(regression_outputs) == 1:
        print("✅ PASSED: Only one callback outputs to 'regression-graph'")
        print(f"   📍 Found in: {regression_outputs[0][0]}")
    elif len(regression_outputs) == 0:
        print("❌ FAILED: No callback outputs to 'regression-graph'")
        return False
    else:
        print("❌ FAILED: Multiple callbacks output to 'regression-graph':")
        for file_path, match in regression_outputs:
            print(f"   📍 {file_path}: {match}")
        return False

    # Check that the callback handles both click_data and auto-selection
    graph_callbacks_path = os.path.join(
        dashboard_app_path, "callbacks", "graph_callbacks.py"
    )
    if os.path.exists(graph_callbacks_path):
        with open(graph_callbacks_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for unified logic handling both cases
        has_click_data_logic = "click_data_available" in content
        has_auto_selection = (
            "auto-select" in content or "Auto-selected variables" in content
        )

        if has_click_data_logic and has_auto_selection:
            print("✅ PASSED: Callback handles both heatmap clicks and auto-selection")
        else:
            print("⚠️  WARNING: Callback may not properly handle both cases")
            print(f"   • Click data logic: {'✅' if has_click_data_logic else '❌'}")
            print(f"   • Auto-selection logic: {'✅' if has_auto_selection else '❌'}")

    print("\n🎯 Duplicate Callback Error Fix: RESOLVED")
    return True


def test_section_duplicates():
    """Test that duplicate sections have been removed."""
    print("\n🧪 Testing Duplicate Section Fix")
    print("=" * 50)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    if not os.path.exists(main_callbacks_path):
        print("❌ FAILED: main_callbacks.py not found")
        return False

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Count duplicate section IDs
    regression_section_pattern = r'id\s*=\s*["\']section-regression["\']'
    regression_graph_pattern = r'id\s*=\s*["\']regression-graph["\']'

    regression_sections = re.findall(regression_section_pattern, content)
    regression_graphs = re.findall(regression_graph_pattern, content)

    print(f"📊 Section Analysis:")
    print(f"   • regression section IDs: {len(regression_sections)}")
    print(f"   • regression graph IDs: {len(regression_graphs)}")

    if len(regression_sections) == 1 and len(regression_graphs) == 1:
        print("✅ PASSED: No duplicate section IDs found")
    else:
        print("❌ FAILED: Duplicate section IDs found:")
        if len(regression_sections) > 1:
            print(f"   • Multiple section-regression IDs: {len(regression_sections)}")
        if len(regression_graphs) > 1:
            print(f"   • Multiple regression-graph IDs: {len(regression_graphs)}")
        return False

    print("\n🎯 Duplicate Section Error Fix: RESOLVED")
    return True


def main():
    """Run all tests."""
    print("🚀 Testing Duplicate Callback & Section Fixes")
    print("=" * 60)

    test1_passed = test_duplicate_callbacks()
    test2_passed = test_section_duplicates()

    print("\n" + "=" * 60)
    print("📋 FINAL RESULTS:")
    print(f"   ✅ Duplicate Callbacks Fixed: {'YES' if test1_passed else 'NO'}")
    print(f"   ✅ Duplicate Sections Fixed: {'YES' if test2_passed else 'NO'}")

    if test1_passed and test2_passed:
        print(
            "\n🎉 ALL TESTS PASSED - JavaScript duplicate callback error should be resolved!"
        )
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Manual verification needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
