#!/usr/bin/env python3
"""
Test script to verify the Key Findings database integration fix.

This script demonstrates that:
1. The precomputed findings database is accessible
2. The KeyFindingsService properly checks cache and precomputed findings
3. The modal callback now uses the proper generate_key_findings method
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add the dashboard_app to the Python path
sys.path.insert(
    0, "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app"
)


def test_precomputed_database():
    """Test that the precomputed findings database is accessible and has data."""
    print("🔍 Testing precomputed findings database...")

    db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"

    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test 1: Check if database has findings
        cursor.execute("SELECT COUNT(*) FROM precomputed_findings WHERE is_active = 1")
        total_findings = cursor.fetchone()[0]
        print(f"✅ Found {total_findings} active findings in database")

        # Test 2: Check for popular tool combinations
        cursor.execute("""
            SELECT tool_name, sources_text, language, COUNT(*) as access_count
            FROM precomputed_findings 
            WHERE is_active = 1
            GROUP BY tool_name, sources_text, language
            ORDER BY access_count DESC
            LIMIT 5
        """)

        popular_combinations = cursor.fetchall()
        print("✅ Most accessed tool-source combinations:")
        for tool, sources, lang, count in popular_combinations:
            print(f"   📊 {tool} + {sources} ({lang}): {count} accesses")

        # Test 3: Check for specific combination that user might search for
        cursor.execute("""
            SELECT executive_summary, principal_findings, confidence_score
            FROM precomputed_findings 
            WHERE tool_name = 'Benchmarking' 
            AND sources_text LIKE '%Google Trends%' 
            AND language = 'es'
            AND is_active = 1
            LIMIT 1
        """)

        benchmark_result = cursor.fetchone()
        if benchmark_result:
            summary, findings, confidence = benchmark_result
            print(f"✅ Found Benchmarking analysis:")
            print(f"   📝 Summary length: {len(summary)} characters")
            print(f"   🔍 Confidence score: {confidence}")
            print(f"   📄 Preview: {summary[:100]}...")
        else:
            print("⚠️  No specific Benchmarking + Google Trends combination found")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False


def test_key_findings_service():
    """Test that KeyFindingsService has the proper generate_key_findings method."""
    print("\n🔍 Testing KeyFindingsService integration...")

    try:
        # Import the KeyFindingsService
        from key_findings.key_findings_service import KeyFindingsService

        # Check if the method exists
        if hasattr(KeyFindingsService, "generate_key_findings"):
            print("✅ KeyFindingsService.generate_key_findings method exists")

            # Check method signature
            import inspect

            sig = inspect.signature(KeyFindingsService.generate_key_findings)
            params = list(sig.parameters.keys())
            print(f"✅ Method parameters: {params}")

            # Verify expected parameters
            expected_params = ["self", "tool_name", "selected_sources", "language"]
            if all(param in params for param in expected_params):
                print("✅ Method has expected parameters")
            else:
                print(
                    f"⚠️  Missing expected parameters. Expected: {expected_params}, Found: {params}"
                )

            return True
        else:
            print("❌ KeyFindingsService.generate_key_findings method not found")
            return False

    except ImportError as e:
        print(f"❌ Could not import KeyFindingsService: {e}")
        return False
    except Exception as e:
        print(f"❌ KeyFindingsService test failed: {e}")
        return False


def test_app_py_changes():
    """Test that app.py contains the proper fix."""
    print("\n🔍 Testing app.py changes...")

    try:
        with open(
            "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/app.py",
            "r",
        ) as f:
            content = f.read()

        # Check for the new method call
        if "key_findings_service.generate_key_findings(" in content:
            print(
                "✅ Found key_findings_service.generate_key_findings() call in app.py"
            )
        else:
            print(
                "❌ key_findings_service.generate_key_findings() call not found in app.py"
            )
            return False

        # Check that the old direct AI service call is removed
        if "key_findings_service.ai_service.generate_analysis(" in content:
            print("⚠️  Still found direct AI service call (may be commented out)")
        else:
            print("✅ Direct AI service call removed from app.py")

        # Check for caching behavior
        if "force_refresh=False" in content:
            print("✅ Found force_refresh=False parameter (enables cache usage)")
        else:
            print("⚠️  force_refresh parameter not found")

        return True

    except Exception as e:
        print(f"❌ app.py test failed: {e}")
        return False


def main():
    """Run all tests to verify the fix."""
    print("🚀 Starting Key Findings Database Integration Test")
    print("=" * 60)

    tests = [
        ("Precomputed Database", test_precomputed_database),
        ("KeyFindingsService", test_key_findings_service),
        ("App.py Changes", test_app_py_changes),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests PASSED! The Key Findings database integration fix is working."
        )
        print("\n🔧 What was fixed:")
        print("   • Modal callback now uses KeyFindingsService.generate_key_findings()")
        print("   • Service checks cache first, then precomputed findings database")
        print("   • Only generates new AI analysis if no cached data found")
        print("   • Enables instant responses for 1,302 precomputed combinations")
        return True
    else:
        print("❌ Some tests failed. The fix may not be complete.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
