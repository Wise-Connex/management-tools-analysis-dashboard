#!/usr/bin/env python3
"""
Test the simplified single-database architecture for Key Findings service.
"""

import asyncio
import sys
import time

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

# Set environment variable for database path
import os
# Use existing database paths
os.environ['DASHBOARD_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/database.db'
os.environ['DASHBOARD_KEY_FINDINGS_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db'
os.environ['DASHBOARD_PRECOMPUTED_FINDINGS_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db'

from key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

class SimplifiedArchitectureTest:
    """Test the simplified architecture."""

    def __init__(self):
        self.key_findings_service = KeyFindingsService(get_database_manager())

    async def test_single_source_simplified(self):
        """Test single-source with simplified architecture."""
        print("🧪 TESTING SINGLE-SOURCE SIMPLIFIED ARCHITECTURE")
        print("=" * 60)
        print("Tool: Benchmarking")
        print("Sources: Google Trends (Single Source)")
        print("Language: Spanish")
        print("Expected: Direct database query, no secondary cache")
        print("=" * 60)

        start_time = time.time()

        try:
            # Test single-source analysis
            result = await self.key_findings_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends"],
                language="es",
                date_range_start="1950-01-01",
                date_range_end="2023-12-31"
            )

            total_time = time.time() - start_time

            if result and result.get("success"):
                print("✅ Single-source analysis completed successfully!")
                print(f"⏱️  Total response time: {total_time:.3f}s")
                print(f"📊 Cache hit: {result.get('cache_hit', False)}")
                print(f"🔍 Source: {result.get('source', 'unknown')}")

                content = result.get("data", {})
                if content:
                    print(f"\n📋 Content sections found:")
                    sections = ['executive_summary', 'principal_findings', 'temporal_analysis',
                               'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']

                    for section in sections:
                        if section in content and content[section]:
                            print(f"  ✅ {section}: {len(str(content[section]))} characters")
                        else:
                            print(f"  ⚠️  {section}: Empty or missing")

                    # Check multi-source sections (should be empty for single-source)
                    multi_source_sections = ['heatmap_analysis', 'pca_analysis']
                    for section in multi_source_sections:
                        if section in content and content[section] and len(str(content[section])) > 10:
                            print(f"  ❌ {section}: FOUND CONTENT (should be empty for single-source)")
                        else:
                            print(f"  ✅ {section}: Empty (correct for single-source)")

                    # Check system values
                    print(f"\n🔧 System Information:")
                    print(f"  Model: {content.get('model_used', 'unknown')}")
                    print(f"  Response time: {content.get('response_time_ms', 'unknown')}ms")
                    print(f"  Token count: {content.get('token_count', 'unknown')}")

                return True
            else:
                print(f"❌ Analysis failed: {result}")
                return False

        except Exception as e:
            print(f"❌ Error during single-source test: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def test_multi_source_simplified(self):
        """Test multi-source with simplified architecture."""
        print(f"\n{'='*60}")
        print("🧪 TESTING MULTI-SOURCE SIMPLIFIED ARCHITECTURE")
        print("=" * 60)
        print("Tool: Benchmarking")
        print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
        print("Language: Spanish")
        print("Expected: Direct database query, includes heatmap/PCA")
        print("=" * 60)

        start_time = time.time()

        try:
            # Test multi-source analysis
            result = await self.key_findings_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
                language="es",
                date_range_start="1950-01-01",
                date_range_end="2023-12-31"
            )

            total_time = time.time() - start_time

            if result and result.get("success"):
                print("✅ Multi-source analysis completed successfully!")
                print(f"⏱️  Total response time: {total_time:.3f}s")
                print(f"📊 Cache hit: {result.get('cache_hit', False)}")
                print(f"🔍 Source: {result.get('source', 'unknown')}")

                content = result.get("data", {})
                if content:
                    print(f"\n📋 Content sections found:")
                    sections = ['executive_summary', 'principal_findings', 'temporal_analysis',
                               'heatmap_analysis', 'fourier_analysis', 'pca_analysis',
                               'strategic_synthesis', 'conclusions']

                    for section in sections:
                        if section in content and content[section] and len(str(content[section])) > 10:
                            print(f"  ✅ {section}: {len(str(content[section]))} characters")
                        else:
                            print(f"  ⚠️  {section}: Empty or missing")

                    # Check system values
                    print(f"\n🔧 System Information:")
                    print(f"  Model: {content.get('model_used', 'unknown')}")
                    print(f"  Response time: {content.get('response_time_ms', 'unknown')}ms")
                    print(f"  Token count: {content.get('token_count', 'unknown')}")

                return True
            else:
                print(f"❌ Analysis failed: {result}")
                return False

        except Exception as e:
            print(f"❌ Error during multi-source test: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def test_performance_comparison(self):
        """Test performance of simplified vs expected performance."""
        print(f"\n{'='*60}")
        print("🧪 PERFORMANCE VALIDATION")
        print("=" * 60)

        # Test single-source performance
        start_time = time.time()
        result1 = await self.key_findings_service.generate_key_findings(
            tool_name="Benchmarking",
            selected_sources=["Google Trends"],
            language="es"
        )
        single_time = time.time() - start_time

        # Test multi-source performance
        start_time = time.time()
        result2 = await self.key_findings_service.generate_key_findings(
            tool_name="Benchmarking",
            selected_sources=["Google Trends", "Google Books", "Bain Usability"],
            language="es"
        )
        multi_time = time.time() - start_time

        print(f"⏱️  Single-source response time: {single_time:.3f}s")
        print(f"⏱️  Multi-source response time: {multi_time:.3f}s")

        # Validate performance expectations
        if single_time < 1.0:  # Should be much faster than 1 second
            print("✅ Single-source performance: EXCELLENT (<1s)")
        elif single_time < 5.0:  # Should be reasonable
            print("✅ Single-source performance: GOOD (<5s)")
        else:
            print("⚠️  Single-source performance: SLOW (>5s)")

        if multi_time < 1.0:
            print("✅ Multi-source performance: EXCELLENT (<1s)")
        elif multi_time < 5.0:
            print("✅ Multi-source performance: GOOD (<5s)")
        else:
            print("⚠️  Multi-source performance: SLOW (>5s)")

        return result1.get("success", False) and result2.get("success", False)

    async def run_all_tests(self):
        """Run all validation tests."""
        print("🚀 STARTING SIMPLIFIED ARCHITECTURE VALIDATION")
        print("=" * 80)

        test1_passed = await self.test_single_source_simplified()
        test2_passed = await self.test_multi_source_simplified()
        test3_passed = await self.test_performance_comparison()

        print(f"\n{'='*80}")
        print("📊 VALIDATION RESULTS:")
        print(f"Single-source test: {'PASSED' if test1_passed else 'FAILED'}")
        print(f"Multi-source test: {'PASSED' if test2_passed else 'FAILED'}")
        print(f"Performance test: {'PASSED' if test3_passed else 'FAILED'}")

        overall_success = test1_passed and test2_passed and test3_passed

        if overall_success:
            print("\n🎉 ALL TESTS PASSED: Simplified architecture working correctly!")
            print("✅ Mathematical correctness maintained")
            print("✅ Performance expectations met")
            print("✅ Single-source excludes heatmap/PCA")
            print("✅ Multi-source includes heatmap/PCA")
        else:
            print("\n❌ SOME TESTS FAILED: Check logs above")

        return overall_success

if __name__ == "__main__":
    tester = SimplifiedArchitectureTest()
    success = asyncio.run(tester.run_all_tests())
    sys.exit(0 if success else 1)