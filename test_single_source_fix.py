#!/usr/bin/env python3
"""
Test the single-source fix
"""

import sys
import os
sys.path.append('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

# Set environment variables
os.environ['GROQ_API_KEY'] = 'test_key'
os.environ['OPENROUTER_API_KEY'] = 'test_key'

# Test from dashboard_app directory
from key_findings.data_aggregator import DataAggregator
import pandas as pd

def test_single_source_fix():
    """Test the single-source data collection fix"""

    print("Testing single-source fix...")
    print("=" * 50)

    try:
        # Create test data
        test_data = pd.DataFrame({
            'Google Trends': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55] * 24  # 240 rows
        })

        print(f"✅ Test data shape: {test_data.shape}")
        print(f"✅ Test data columns: {test_data.columns.tolist()}")

        # Initialize aggregator
        aggregator = DataAggregator()

        # Test with numeric source IDs (old way - should fail)
        print("\nTesting with numeric source IDs (old way)...")
        result_old = aggregator.extract_single_source_insights(test_data, [1])
        print(f"Result with numeric IDs: {result_old}")

        # Test with display names (new way - should work)
        print("\nTesting with display names (new way)...")
        result_new = aggregator.extract_single_source_insights(test_data, ['Google Trends'])
        print(f"Result with display names: {result_new}")

        # Check if error is present
        has_error_old = 'error' in result_old
        has_error_new = 'error' in result_new

        print(f"\n✅ Old method has error: {has_error_old}")
        print(f"✅ New method has error: {has_error_new}")

        if has_error_old and not has_error_new:
            print("\n🎉 SUCCESS: Fix is working correctly!")
            print("✅ Numeric IDs fail as expected")
            print("✅ Display names work correctly")
            return True
        else:
            print("\n❌ ISSUE: Fix may not be working properly")
            return False

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_single_source_fix()
    sys.exit(0 if success else 1)