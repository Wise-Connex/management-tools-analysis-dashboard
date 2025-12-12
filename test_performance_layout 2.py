#!/usr/bin/env python3
"""
Test to verify the new Performance section layout and styling.
"""

import sys
import os
import re


def verify_performance_section_layout():
    """Verify the new Performance section has proper layout and no cache content."""
    print("🧪 Testing New Performance Section Layout")
    print("=" * 60)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that cache content has been removed from performance section
    perf_start = content.find("# 9. Performance Metrics section")
    perf_end = content.find("return html.Div(content)", perf_start)
    perf_section = (
        content[perf_start:perf_end] if perf_start > 0 and perf_end > 0 else ""
    )

    has_cache_content = (
        any(
            keyword in perf_section
            for keyword in [
                "Cache Entries",
                "Cache Size",
                "processed_data_cache",
                "cache_max_size",
                "cache_stats",
            ]
        )
        if perf_section
        else False
    )

    # Check for new layout elements
    has_cards_layout = (
        "card border-primary" in content and "card border-success" in content
    )
    has_icons = "fas fa-tachometer-alt" in content and "fas fa-info-circle" in content
    has_gradient_bg = "linear-gradient" in content
    has_proper_styling = "shadow-sm" in content and "border-primary" in content

    # Check for three main sections
    has_database_card = "Database Statistics" in content
    has_analysis_card = "Current Analysis" in content
    has_performance_card = "System Performance" in content

    print(f"📊 Layout Analysis:")
    print(f"   • Cache content removed: {'✅' if not has_cache_content else '❌'}")
    print(f"   • Card-based layout: {'✅' if has_cards_layout else '❌'}")
    print(f"   • Icons added: {'✅' if has_icons else '❌'}")
    print(f"   • Gradient background: {'✅' if has_gradient_bg else '❌'}")
    print(f"   • Proper styling: {'✅' if has_proper_styling else '❌'}")

    print(f"\n📊 Content Cards:")
    print(f"   • Database Statistics card: {'✅' if has_database_card else '❌'}")
    print(f"   • Current Analysis card: {'✅' if has_analysis_card else '❌'}")
    print(f"   • System Performance card: {'✅' if has_performance_card else '❌'}")

    # Check for proper data points (no cache-related)
    has_proper_metrics = all(
        metric in content
        for metric in [
            "Total Records",
            "Keywords",
            "Data Sources",
            "Selected Tool",
            "Data Points",
        ]
    )

    print(f"   • Proper metrics: {'✅' if has_proper_metrics else '❌'}")

    # Check for responsive layout (just check for g-3 utility)
    has_responsive_layout = "g-3" in content

    print(f"   • Responsive layout: {'✅' if has_responsive_layout else '❌'}")

    all_checks = [
        not has_cache_content,
        has_cards_layout,
        has_icons,
        has_gradient_bg,
        has_proper_styling,
        has_database_card,
        has_analysis_card,
        has_performance_card,
        has_proper_metrics,
        has_responsive_layout,
    ]

    return all(all_checks)


def test_performance_section_content():
    """Test that the performance section shows relevant information."""
    print("\n🧪 Testing Performance Section Content")
    print("=" * 60)

    main_callbacks_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/callbacks/main_callbacks.py"

    with open(main_callbacks_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the performance section
    perf_start = content.find("# 9. Performance Metrics section")
    perf_end = content.find("return html.Div(content)", perf_start)
    perf_section = (
        content[perf_start:perf_end] if perf_start > 0 and perf_end > 0 else ""
    )

    if not perf_section:
        print("❌ Performance section not found")
        return False

    # Check for key features
    features = [
        ("Performance metrics title", "performance_metrics" in perf_section),
        ("Database statistics", "Total Records" in perf_section),
        ("Current analysis info", "Selected Tool" in perf_section),
        ("System info", "Dashboard:" in perf_section),
        ("Fallback error handling", "except Exception" in perf_section),
        ("Real-time update note", "real-time" in perf_section.lower()),
    ]

    print(f"📋 Content Features:")
    for feature_name, found in features:
        print(f"   • {feature_name}: {'✅' if found else '❌'}")

    return all(found for _, found in features)


def main():
    """Run the tests."""
    print("🚀 Testing New Performance Section Design")
    print("=" * 80)

    tests = [
        ("Performance Section Layout", verify_performance_section_layout),
        ("Performance Section Content", test_performance_section_content),
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
    print("📋 FINAL PERFORMANCE SECTION RESULTS:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 NEW PERFORMANCE SECTION DESIGN IS EXCELLENT!")
        print("✅ Cache content completely removed")
        print("✅ Beautiful card-based layout with colors")
        print("✅ Icons and proper styling added")
        print("✅ Three informative sections")
        print("✅ Responsive Bootstrap 5 grid")
        print("✅ Gradient background and shadows")
        print("✅ Real-time performance metrics")
        print("✅ Error handling and fallback")
        return 0
    else:
        print("❌ SOME PERFORMANCE SECTION TESTS FAILED")
        print("🔧 Review needed for layout or content issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
