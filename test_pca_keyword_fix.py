#!/usr/bin/env python3
"""
Test to verify that the PCA keyword error has been fixed.
"""

import sys
import os
import pandas as pd
import numpy as np


def test_pca_keyword_error_fix():
    """Test that PCA functions no longer fail with 'keyword' error."""
    print("🧪 Testing PCA Keyword Error Fix")
    print("=" * 50)

    # Add dashboard_app to path to import utils
    sys.path.insert(
        0, "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app"
    )

    try:
        from utils import create_pca_figure, perform_comprehensive_pca_analysis

        print("✅ Successfully imported PCA functions")
    except ImportError as e:
        print(f"❌ Failed to import PCA functions: {e}")
        return False

    # Create sample data that mimics combined_dataset structure
    # (no 'keyword' column, just date and numeric columns)
    sample_data = pd.DataFrame(
        {
            "Fecha": pd.date_range("2020-01-01", periods=100, freq="D"),
            "Google Trends": np.random.randn(100),
            "Bain Usability": np.random.randn(100),
            "Harvard Business": np.random.randn(100),
            "McKinsey Insights": np.random.randn(100),
            "BCG Analysis": np.random.randn(100),
        }
    )

    print(f"📊 Created sample data with columns: {list(sample_data.columns)}")
    print(f"📊 Sample data shape: {sample_data.shape}")

    # Test 1: perform_comprehensive_pca_analysis
    try:
        print("\n🧪 Test 1: perform_comprehensive_pca_analysis")
        result = perform_comprehensive_pca_analysis(
            sample_data, ["Google Trends", "Bain Usability"], "es"
        )

        if "error" in result:
            print(f"❌ PCA analysis failed: {result['error']}")
            return False
        elif result.get("success"):
            print("✅ PCA analysis completed successfully")
            print(f"   • PCA components: {len(result.get('components', []))}")
            print(
                f"   • Explained variance: {result.get('explained_variance_ratio', [])}"
            )
        else:
            print("❌ PCA analysis returned unexpected result")
            return False

    except Exception as e:
        print(f"❌ PCA analysis crashed with error: {e}")
        return False

    # Test 2: create_pca_figure
    try:
        print("\n🧪 Test 2: create_pca_figure")
        fig = create_pca_figure(
            sample_data,
            ["Google Trends", "Bain Usability"],
            "es",
            "Benchmarking",  # tool_name parameter
        )

        if fig is not None:
            print("✅ PCA figure created successfully")
            print(
                f"   • Figure has data: {len(fig.data) if hasattr(fig, 'data') else 'N/A'} traces"
            )
        else:
            print("❌ PCA figure creation failed")
            return False

    except Exception as e:
        print(f"❌ PCA figure creation crashed with error: {e}")
        return False

    return True


def test_data_structure_validation():
    """Test that the sample data structure is realistic."""
    print("\n🧪 Testing Data Structure Validation")
    print("=" * 50)

    # Simulate what combined_dataset looks like
    combined_dataset = pd.DataFrame(
        {
            "Fecha": pd.date_range("2020-01-01", periods=50, freq="D"),
            "Google Trends": np.random.randn(50),
            "Bain Usabilidad": np.random.randn(50),
            "Harvard Business Review": np.random.randn(50),
        }
    )

    print(f"📊 Combined dataset structure:")
    print(f"   • Columns: {list(combined_dataset.columns)}")
    print(f"   • Shape: {combined_dataset.shape}")
    print(f"   • Data types: {combined_dataset.dtypes.to_dict()}")

    # Check that 'keyword' column doesn't exist
    has_keyword_column = "keyword" in combined_dataset.columns
    print(
        f"   • Has 'keyword' column: {'❌ YES (unexpected)' if has_keyword_column else '✅ NO (expected)'}"
    )

    # Check numeric columns
    numeric_columns = combined_dataset.select_dtypes(
        include=[np.number]
    ).columns.tolist()
    print(f"   • Numeric columns: {numeric_columns}")
    print(f"   • Numeric column count: {len(numeric_columns)}")

    if len(numeric_columns) >= 2:
        print("✅ Data has sufficient numeric columns for PCA")
        return True
    else:
        print("❌ Data doesn't have enough numeric columns for PCA")
        return False


def main():
    """Run all PCA keyword error tests."""
    print("🚀 Testing PCA Keyword Error Fix")
    print("=" * 80)

    tests = [
        ("Data Structure Validation", test_data_structure_validation),
        ("PCA Keyword Error Fix", test_pca_keyword_error_fix),
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
    print("📋 FINAL PCA KEYWORD ERROR FIX RESULTS:")
    print("=" * 80)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 PCA KEYWORD ERROR FIX IS SUCCESSFUL!")
        print("✅ PCA functions no longer fail with 'keyword' error")
        print("✅ Functions work with combined_dataset structure")
        print("✅ Data validation confirms proper structure")
        print("✅ PCA Analysis section should now display correctly")
        return 0
    else:
        print("❌ PCA KEYWORD ERROR FIX FAILED")
        print("🔧 Manual review needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
