#!/usr/bin/env python3
"""
Test to identify and fix duplicate PCA sections.
"""

import sys
import os
import re


def find_duplicate_pca_sections():
    """Find all instances of PCA section creation with duplicate IDs."""
    print("🧪 Finding Duplicate PCA Sections")
    print("=" * 60)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all section-pca-analysis IDs
    section_pattern = r'id="section-pca-analysis"'
    sections = [
        (m.start(), m.end(), content[m.start() : m.end() + 50])
        for m in re.finditer(section_pattern, content)
    ]

    print(f"📋 Found {len(sections)} sections with id='section-pca-analysis':")
    for i, (start, end, context) in enumerate(sections, 1):
        line_num = content[:start].count("\n") + 1
        print(f"   {i}. Line {line_num}: {context}")

    # Check for other similar IDs
    similar_ids = [
        'id="section-pca-error"',
        'id="section-pca-no-data"',
        'id="section-pca"',
    ]

    for similar_id in similar_ids:
        matches = list(re.finditer(similar_id, content))
        if matches:
            print(f"📋 Found {len(matches)} sections with {similar_id}:")
            for i, match in enumerate(matches, 1):
                line_num = content[: match.start()].count("\n") + 1
                print(f"   {i}. Line {line_num}")

    return len(sections)


def check_pca_logic_structure():
    """Check the structure of PCA logic for duplication."""
    print("\n🧪 Checking PCA Logic Structure")
    print("=" * 60)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find PCA analysis function calls
    pca_calls = re.findall(r"perform_comprehensive_pca_analysis\([^)]+\)", content)
    print(f"📋 Found {len(pca_calls)} calls to perform_comprehensive_pca_analysis")

    # Find PCA figure creation calls
    pca_figures = re.findall(r"create_pca_figure\([^)]+\)", content)
    print(f"📋 Found {len(pca_figures)} calls to create_pca_figure")

    # Check for duplicated code blocks
    if len(pca_calls) > 1:
        print("❌ Multiple calls to perform_comprehensive_pca_analysis detected")
        print("   This suggests duplicate logic")

    if len(pca_figures) > 1:
        print("❌ Multiple calls to create_pca_figure detected")
        print("   This suggests duplicate logic")

    # Find conditional blocks that might contain duplication
    if_statements = re.findall(r'if pca_results\.get\("success"\):', content)
    print(f"📋 Found {len(if_statements)} conditional blocks checking PCA success")

    return len(pca_calls) <= 1 and len(pca_figures) <= 1


def main():
    """Run all duplicate section tests."""
    print("🚀 Testing for Duplicate PCA Sections")
    print("=" * 80)

    tests = [
        ("Find Duplicate PCA Sections", find_duplicate_pca_sections),
        ("Check PCA Logic Structure", check_pca_logic_structure),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            if test_name == "Find Duplicate PCA Sections":
                # For this test, we expect some duplicates to be found (to be fixed)
                test_result = test_func() >= 1  # Should find at least one
            else:
                test_result = test_func()
            results.append((test_name, test_result))
            print(f"\n{test_name}: {'✅ PASSED' if test_result else '❌ FAILED'}")
        except Exception as e:
            print(f"\n{test_name}: ❌ ERROR - {e}")
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("📋 DUPLICATE PCA SECTIONS ANALYSIS:")
    print("=" * 80)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")

    print("\n" + "=" * 80)
    if all(result for _, result in results):
        print("🎉 DUPLICATE ANALYSIS COMPLETE!")
        print("✅ Identified duplicate PCA sections")
        print("✅ Manual cleanup may be needed")
        return 0
    else:
        print("❌ DUPLICATE ANALYSIS FAILED")
        print("🔧 Manual review needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
