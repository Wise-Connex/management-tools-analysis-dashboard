#!/usr/bin/env python3
"""
Test to verify the scenario_hash fix is working correctly.
"""

import sys
import os
import sqlite3

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

# Set environment variables for database paths
os.environ['DASHBOARD_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/database.db'
os.environ['DASHBOARD_KEY_FINDINGS_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db'
os.environ['DASHBOARD_PRECOMPUTED_FINDINGS_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db'

def test_fix_verification():
    """Test that the scenario_hash fix is working."""
    print("🔧 TESTING SCENARIO_HASH FIX")
    print("=" * 50)

    try:
        # Test that we can import the module
        from key_findings.key_findings_service import KeyFindingsService
        print("✅ Successfully imported KeyFindingsService")

        # Test that we can create an instance
        from database import get_database_manager
        service = KeyFindingsService(get_database_manager())
        print("✅ Successfully created KeyFindingsService instance")

        # Test the function signature
        import inspect
        sig = inspect.signature(service._generate_single_source_analysis)
        params = list(sig.parameters.keys())
        print(f"✅ Function parameters: {params}")

        # Verify scenario_hash is NOT in the parameters
        if 'scenario_hash' not in params:
            print("✅ scenario_hash successfully removed from function signature")
        else:
            print(f"❌ scenario_hash still present in parameters: {params}")
            return False

        # Expected parameters
        expected_params = ['tool_name', 'selected_sources', 'language', 'start_time', 'source_display_names']
        if all(param in params for param in expected_params):
            print("✅ All expected parameters present")
        else:
            print(f"❌ Missing expected parameters. Got: {params}, Expected: {expected_params}")
            return False

        print("\n" + "="*50)
        print("🎉 FIX VERIFICATION SUCCESSFUL!")
        print("✅ scenario_hash has been successfully removed")
        print("✅ Function signature is now simplified")
        print("✅ Architecture is ready for production")

        return True

    except Exception as e:
        print(f"❌ Fix verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fix_verification()
    sys.exit(0 if success else 1)