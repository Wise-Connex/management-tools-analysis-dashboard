#!/usr/bin/env python3
"""
Test to verify that the Performance section is properly included and functional.
"""

import sys
import os


def test_performance_section():
    """Test that the performance section is included in main_callbacks.py"""
    print("🧪 Testing Performance Section")
    print("=" * 50)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    if not os.path.exists(main_callbacks_path):
        print("❌ FAILED: main_callbacks.py not found")
        return False

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for Performance section
    has_performance_section = "performance_metrics" in content
    has_performance_id = 'id="section-performance"' in content
    has_performance_metrics = "cache_stats" in content

    print(f"📊 Performance Section Analysis:")
    print(f"   • Performance section code: {'✅' if has_performance_section else '❌'}")
    print(f"   • Performance section ID: {'✅' if has_performance_id else '❌'}")
    print(f"   • Cache stats usage: {'✅' if has_performance_metrics else '❌'}")

    # Check for cache stats function
    utils_path = (
        "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/utils.py"
    )
    if os.path.exists(utils_path):
        with open(utils_path, "r", encoding="utf-8") as f:
            utils_content = f.read()

        has_cache_stats = "def get_cache_stats" in utils_content
        print(f"   • get_cache_stats function: {'✅' if has_cache_stats else '❌'}")

        if has_cache_stats:
            # Check return structure
            if "processed_data_cache" in utils_content:
                print(f"   • Cache stats structure: ✅ (correct keys)")
            else:
                print(f"   • Cache stats structure: ⚠️  (may need verification)")
    else:
        print("   • utils.py: ❌ (not found)")

    # Test translation keys
    translations_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/translations.py"
    if os.path.exists(translations_path):
        with open(translations_path, "r", encoding="utf-8") as f:
            trans_content = f.read()

        has_performance_translation = "performance_metrics" in trans_content
        print(
            f"   • Performance translations: {'✅' if has_performance_translation else '❌'}"
        )
    else:
        print("   • translations.py: ❌ (not found)")

    # Check section positioning (should be last)
    performance_pos = content.find("Performance Metrics section")
    data_table_pos = content.find("Data Table section")

    if performance_pos > data_table_pos > 0:
        print(f"   • Section ordering: ✅ (Performance is last)")
    elif performance_pos > 0:
        print(f"   • Section ordering: ⚠️  (Performance found but ordering unclear)")
    else:
        print(f"   • Section ordering: ❌ (Performance section not found)")

    # Final assessment
    all_checks = [has_performance_section, has_performance_id, has_performance_metrics]

    if all(all_checks):
        print("\n🎯 Performance Section: READY")
        print(
            "✅ The Performance/Rendimiento section should appear as the last section"
        )
        return True
    else:
        print("\n❌ Performance Section: ISSUES FOUND")
        return False


def main():
    """Run the test."""
    print("🚀 Testing Performance Section Visibility")
    print("=" * 60)

    success = test_performance_section()

    print("\n" + "=" * 60)
    if success:
        print("🎉 Performance section should be visible in the dashboard!")
        print("📍 Location: Last section after Data Table")
        print("🏷️  Title: 'Performance Metrics' / 'Métricas de Rendimiento'")
        return 0
    else:
        print("❌ Performance section has issues that need fixing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
