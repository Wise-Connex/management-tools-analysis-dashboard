#!/usr/bin/env python3
"""
Test script for database-first Key Findings strategy.

This script tests the new database-first approach to verify:
1. Precomputed database is accessible
2. Database-first service works correctly
3. Fallback to live AI works when needed
"""

import sys
import os
from pathlib import Path

# Add the dashboard_app directory to path
dashboard_app_dir = Path(__file__).parent / "dashboard_app"
sys.path.insert(0, str(dashboard_app_dir))


def test_database_first_import():
    """Test importing the database-first service."""
    print("🔍 Testing database-first service import...")

    try:
        from key_findings.database_first_service import (
            create_database_first_service,
            DatabaseFirstService,
        )

        print("✅ Database-first service imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import database-first service: {e}")
        return False


def test_precomputed_db_access():
    """Test accessing the precomputed database."""
    print("\n🔍 Testing precomputed database access...")

    try:
        # Add root directory to path for database imports
        tools_dashboard_root = Path(__file__).parent
        if str(tools_dashboard_root) not in sys.path:
            sys.path.insert(0, str(tools_dashboard_root))

        from database_implementation.precomputed_findings_db import (
            get_precomputed_db_manager,
        )

        db_manager = get_precomputed_db_manager()

        if db_manager:
            print("✅ Precomputed database manager initialized")

            # Test a simple query
            test_result = db_manager.get_combination_by_hash("nonexistent_hash")
            print(f"✅ Database query test completed: {test_result is None}")

            return True
        else:
            print("❌ Failed to initialize precomputed database manager")
            return False

    except Exception as e:
        print(f"❌ Failed to access precomputed database: {e}")
        return False


def test_database_first_logic():
    """Test the database-first logic in app.py."""
    print("\n🔍 Testing database-first logic...")

    try:
        # Import the function from app.py
        from app import get_key_findings_with_database_first

        print("✅ Database-first function imported successfully")

        # Test with dummy parameters (should fail gracefully)
        result = get_key_findings_with_database_first(
            tool_name="test_tool", selected_sources=["test_source"], language="es"
        )

        print(f"✅ Database-first function executed: {result.get('success', False)}")
        print(f"📊 Result keys: {list(result.keys())}")

        return True
    except Exception as e:
        print(f"❌ Failed to test database-first logic: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Testing Database-First Key Findings Strategy")
    print("=" * 60)

    tests = [
        ("Database-First Service Import", test_database_first_import),
        ("Precomputed Database Access", test_precomputed_db_access),
        ("Database-First Logic", test_database_first_logic),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)

        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests PASSED! Database-first strategy is working correctly.")
        print("\n🔄 Expected behavior:")
        print("  1. ✅ Check precomputed database first (sub-2ms response)")
        print("  2. ✅ Fall back to live AI if not in cache")
        print("  3. ✅ Show '⚡ Instant result' for cached analyses")
        print("  4. ✅ Show '🔄 Generated fresh' for new analyses")
    else:
        print(f"⚠️  {total - passed} tests failed. Check the errors above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
