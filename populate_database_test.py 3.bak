#!/usr/bin/env python3
"""
Script to populate the database with K2 AI analysis for both single-source and multi-source scenarios.
"""

import asyncio
import sys
import json
from datetime import datetime

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

class DatabasePopulator:
    """Populate database with fresh K2 AI analysis."""

    def __init__(self):
        self.db_manager = get_database_manager()
        self.key_findings_service = KeyFindingsService(self.db_manager)

    async def populate_single_source(self):
        """Populate single-source scenario: Benchmarking + Google Trends."""
        print("🎯 POPULATING SINGLE-SOURCE SCENARIO")
        print("=" * 60)
        print("Tool: Benchmarking")
        print("Sources: Google Trends (Single Source)")
        print("Language: Spanish")
        print("Model: Kimi K2 (moonshotai/kimi-k2-instruct)")
        print("=" * 60)

        # Prepare single-source test data
        analysis_data = {
            "tool_name": "Benchmarking",
            "selected_sources": ["Google Trends"],
            "language": "es",
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "data_points_analyzed": 240,
            "temporal_analysis": {
                "trend_direction": "increasing",
                "key_periods": ["1995", "2008", "2015"],
                "overall_growth": "significant"
            },
            "seasonal_analysis": {
                "patterns": ["quarterly", "annual"],
                "volatility": "moderate"
            },
            "fourier_analysis": {
                "dominant_cycles": ["36-month", "12-month"],
                "spectral_power": "concentrated"
            }
        }

        try:
            print("\n🤖 GENERATING SINGLE-SOURCE AI ANALYSIS...")

            # Call the key findings service to generate and save analysis
            result = await self.key_findings_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends"],
                language="es",
                date_range_start="1950-01-01",
                date_range_end="2023-12-31",
                analysis_data=analysis_data
            )

            if result and result.get("success"):
                print("✅ Single-source analysis generated and saved!")
                print(f"📊 Result: {result}")

                # Extract key information
                content = result.get("content", {})
                if content:
                    print(f"\n📋 CONTENT SECTIONS:")
                    sections = ['executive_summary', 'principal_findings', 'strategic_synthesis', 'conclusions']
                    for section in sections:
                        if section in content and content[section]:
                            print(f"✅ {section}: {len(str(content[section]))} characters")

                    # Check for multi-source sections (should be empty)
                    multi_source_sections = ['heatmap_analysis', 'pca_analysis']
                    for section in multi_source_sections:
                        if section in content and content[section]:
                            print(f"⚠️  {section}: {len(str(content[section]))} characters (should be empty for single-source)")
                        else:
                            print(f"✅ {section}: Empty (correct for single-source)")

                return result
            else:
                print(f"❌ Failed to generate single-source analysis: {result}")
                return None

        except Exception as e:
            print(f"❌ Error generating single-source analysis: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def populate_multi_source(self):
        """Populate multi-source scenario: Benchmarking + Multiple Sources."""
        print("\n🎯 POPULATING MULTI-SOURCE SCENARIO")
        print("=" * 60)
        print("Tool: Benchmarking")
        print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
        print("Language: Spanish")
        print("Model: Kimi K2 (moonshotai/kimi-k2-instruct)")
        print("=" * 60)

        # Prepare multi-source test data
        analysis_data = {
            "tool_name": "Benchmarking",
            "selected_sources": ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
            "language": "es",
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "data_points_analyzed": 888,
            "pca_insights": {
                "dominant_patterns": [{"component": 1, "loadings": {"Google Trends": 0.8, "Google Books": 0.7, "Bain Usability": 0.6, "Bain Satisfaction": 0.5, "Crossref": 0.9}}],
                "total_variance_explained": 78.5
            },
            "heatmap_analysis": {"correlation_matrix": "sample_correlation_data"}
        }

        try:
            print("\n🤖 GENERATING MULTI-SOURCE AI ANALYSIS...")

            # Call the key findings service to generate and save analysis
            result = await self.key_findings_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
                language="es",
                date_range_start="1950-01-01",
                date_range_end="2023-12-31",
                analysis_data=analysis_data
            )

            if result and result.get("success"):
                print("✅ Multi-source analysis generated and saved!")
                print(f"📊 Result: {result}")

                # Extract key information
                content = result.get("content", {})
                if content:
                    print(f"\n📋 CONTENT SECTIONS:")
                    sections = ['executive_summary', 'principal_findings', 'strategic_synthesis', 'conclusions']
                    for section in sections:
                        if section in content and content[section]:
                            print(f"✅ {section}: {len(str(content[section]))} characters")

                    # Check for multi-source sections (should have content)
                    multi_source_sections = ['heatmap_analysis', 'pca_analysis']
                    for section in multi_source_sections:
                        if section in content and content[section]:
                            print(f"✅ {section}: {len(str(content[section]))} characters (multi-source content)")
                        else:
                            print(f"⚠️  {section}: Empty (missing multi-source content)")

                return result
            else:
                print(f"❌ Failed to generate multi-source analysis: {result}")
                return None

        except Exception as e:
            print(f"❌ Error generating multi-source analysis: {e}")
            import traceback
            traceback.print_exc()
            return None

    def verify_database_population(self):
        """Verify what was actually stored in the database."""
        print("\n🔍 VERIFYING DATABASE POPULATION")
        print("=" * 60)

        try:
            # Check key findings reports
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # Count entries
                cursor.execute("SELECT COUNT(*) FROM key_findings_reports")
                count = cursor.fetchone()[0]
                print(f"📊 Total reports in database: {count}")

                if count > 0:
                    # Get latest entries
                    cursor.execute("""
                        SELECT tool_name, language, model_used, data_points_analyzed,
                               sources_count, LENGTH(executive_summary) as exec_len,
                               LENGTH(principal_findings) as principal_len,
                               LENGTH(pca_insights) as pca_len,
                               generation_timestamp
                        FROM key_findings_reports
                        ORDER BY generation_timestamp DESC
                        LIMIT 3
                    """)

                    rows = cursor.fetchall()
                    for i, row in enumerate(rows):
                        print(f"\n📋 Report {i+1}:")
                        print(f"   Tool: {row[0]}")
                        print(f"   Language: {row[1]}")
                        print(f"   Model: {row[2]}")
                        print(f"   Data Points: {row[3]}")
                        print(f"   Sources Count: {row[4]}")
                        print(f"   Executive Summary: {row[5]} characters")
                        print(f"   Principal Findings: {row[6]} characters")
                        print(f"   PCA Insights: {row[7] if row[7] else 0} characters")
                        print(f"   Generated: {row[8]}")

                        # Determine analysis type based on sources count
                        analysis_type = "Single-Source" if row[4] == 1 else "Multi-Source"
                        print(f"   Analysis Type: {analysis_type}")

                return count > 0

        except Exception as e:
            print(f"❌ Error verifying database: {e}")
            return False

    async def run_population_tests(self):
        """Run both population tests."""
        print("🚀 STARTING DATABASE POPULATION WITH K2 AI")
        print("=" * 80)

        # Test 1: Single-source
        single_result = await self.populate_single_source()

        # Test 2: Multi-source
        multi_result = await self.populate_multi_source()

        # Verify results
        db_populated = self.verify_database_population()

        print("\n" + "=" * 80)
        print("📊 POPULATION TEST SUMMARY:")
        print(f"✅ Single-Source Test: {'PASSED' if single_result else 'FAILED'}")
        print(f"✅ Multi-Source Test: {'PASSED' if multi_result else 'FAILED'}")
        print(f"✅ Database Population: {'VERIFIED' if db_populated else 'FAILED'}")

        if single_result and multi_result and db_populated:
            print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
            print("Database is now populated with fresh K2 AI analysis.")
        else:
            print("\n⚠️  SOME TESTS FAILED - Check logs above for details.")

        return single_result and multi_result and db_populated

if __name__ == "__main__":
    populator = DatabasePopulator()
    success = asyncio.run(populator.run_population_tests())
    sys.exit(0 if success else 1)