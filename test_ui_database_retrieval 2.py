#!/usr/bin/env python3
"""
Test script to verify UI Key Findings button retrieves data from database instead of making AI queries.
"""

import asyncio
import sys
import time
import logging
from datetime import datetime

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.key_findings_service import KeyFindingsService
from key_findings.database_manager import KeyFindingsDBManager
import config as app_config

# Configure logging to see database vs AI activity
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UITester:
    """Test UI Key Findings functionality to verify database retrieval."""

    def __init__(self):
        # Initialize services
        self.db_manager = KeyFindingsDBManager('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/database.db')
        self.kf_service = KeyFindingsService(
            db_manager=self.db_manager,
            groq_api_key=app_config.config.get("groq_api_key"),
            openrouter_api_key=app_config.config.get("openrouter_api_key"),
            config=app_config.config
        )

    async def test_single_source_database_retrieval(self):
        """Test single source analysis database retrieval."""

        print("🧪 Testing Single Source Database Retrieval")
        print("=" * 60)
        print("Tool: Benchmarking")
        print("Sources: Google Trends (single source)")
        print("Language: Spanish")
        print("=" * 60)

        start_time = time.time()

        try:
            # Test single source analysis
            result = await self.kf_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends"],  # Single source
                language="es",
                force_refresh=False  # This should trigger database lookup first
            )

            end_time = time.time()
            response_time = (end_time - start_time) * 1000

            print(f"✅ Analysis completed in {response_time:.2f}ms")
            print(f"Success: {result.get('success', False)}")
            print(f"Source: {result.get('source', 'unknown')}")

            if result.get('success'):
                content = result.get('content', {})

                print(f"\\n📊 Retrieved {len(content)} sections:")
                for section in content.keys():
                    if content[section]:
                        section_length = len(str(content[section]))
                        print(f"  ✅ {section}: {section_length} chars")

                # Check if this came from database
                if result.get('source') == 'precomputed_findings':
                    print("\\n🎯 DATABASE RETRIEVAL CONFIRMED!")
                    print("✅ Data was retrieved from precomputed findings database")
                    print("✅ No AI query was made")
                    return True
                else:
                    print(f"\\n⚠️ Data source: {result.get('source')}")
                    print("⚠️ This appears to be a fresh AI generation")
                    return False
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"❌ Error during single source test: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def test_multi_source_database_retrieval(self):
        """Test multi-source analysis database retrieval."""

        print("\\n🧪 Testing Multi-Source Database Retrieval")
        print("=" * 60)
        print("Tool: Benchmarking")
        print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
        print("Language: Spanish")
        print("=" * 60)

        start_time = time.time()

        try:
            # Test multi-source analysis
            result = await self.kf_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],  # 5 sources
                language="es",
                force_refresh=False  # This should trigger database lookup first
            )

            end_time = time.time()
            response_time = (end_time - start_time) * 1000

            print(f"✅ Analysis completed in {response_time:.2f}ms")
            print(f"Success: {result.get('success', False)}")
            print(f"Source: {result.get('source', 'unknown')}")

            if result.get('success'):
                content = result.get('content', {})

                print(f"\\n📊 Retrieved {len(content)} sections:")
                for section in content.keys():
                    if content[section]:
                        section_length = len(str(content[section]))
                        print(f"  ✅ {section}: {section_length} chars")

                # Check if this came from database
                if result.get('source') == 'precomputed_findings':
                    print("\\n🎯 DATABASE RETRIEVAL CONFIRMED!")
                    print("✅ Data was retrieved from precomputed findings database")
                    print("✅ No AI query was made")
                    return True
                else:
                    print(f"\\n⚠️ Data source: {result.get('source')}")
                    print("⚠️ This appears to be a fresh AI generation")
                    return False
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"❌ Error during multi-source test: {e}")
            import traceback
            traceback.print_exc()
            return False

    def verify_database_contents(self):
        """Verify what's actually in the database."""

        print("\\n🔍 Verifying Database Contents")
        print("=" * 60)

        try:
            # Check what's in key_findings_reports
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT id, tool_name, selected_sources, language, confidence_score FROM key_findings_reports ORDER BY id")
            reports = cursor.fetchall()

            print(f"📋 Found {len(reports)} reports in database:")
            for report in reports:
                id, tool_name, selected_sources, language, confidence_score = report
                sources = eval(selected_sources) if selected_sources else []
                print(f"  ID {id}: {tool_name} | {len(sources)} sources | {language} | Confidence: {confidence_score}")

            # Check history
            cursor.execute("SELECT scenario_hash, change_type, change_timestamp FROM key_findings_history")
            history = cursor.fetchall()
            print(f"\\n📜 Found {len(history)} history entries:")
            for entry in history:
                scenario_hash, change_type, timestamp = entry
                print(f"  {change_type}: {scenario_hash[:16]}... | {timestamp}")

            # Check cache statistics
            cursor.execute("SELECT * FROM cache_statistics")
            stats = cursor.fetchall()
            print(f"\\n📊 Found {len(stats)} cache statistics:")
            for stat in stats:
                print(f"  Date: {stat[1]} | Requests: {stat[2]} | Hits: {stat[3]} | Misses: {stat[4]}")

            return True

        except Exception as e:
            print(f"❌ Error verifying database: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    tester = UITester()

    print("🚀 Starting UI Database Retrieval Testing")
    print("=" * 80)

    # Step 1: Verify database contents
    tester.verify_database_contents()

    # Step 2: Test single source database retrieval
    single_success = asyncio.run(tester.test_single_source_database_retrieval())

    # Step 3: Test multi-source database retrieval
    multi_success = asyncio.run(tester.test_multi_source_database_retrieval())

    # Summary
    print("\\n" + "=" * 80)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"Single Source Database Retrieval: {'✅ PASSED' if single_success else '❌ FAILED'}")
    print(f"Multi-Source Database Retrieval: {'✅ PASSED' if multi_success else '❌ FAILED'}")

    if single_success and multi_success:
        print("\\n🎉 ALL TESTS PASSED!")
        print("✅ Database retrieval is working correctly")
        print("✅ UI Key Findings button retrieves precomputed data")
        print("✅ No unnecessary AI queries are being made")
    else:
        print("\\n⚠️ Some tests failed - check logs above")

    sys.exit(0 if (single_success and multi_success) else 1)

print("\\n" + "="*60)
print("🧪 UI Database Retrieval Testing Complete!")
print("="*60)
print("This test verifies that:")
print("• Key Findings button retrieves from database")
print("• Precomputed findings are used correctly")
print("• No unnecessary AI queries are made")
print("• Both single and multi-source work properly")
print("="*60)