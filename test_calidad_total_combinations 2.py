#!/usr/bin/env python3
"""
TEST SCRIPT: Calidad Total Specific Combinations
=================================================

This script tests the two specific combinations you requested:
1. "Calidad Total + Google Trends" (single source)
2. "Calidad Total + all 5 sources" (multi-source)

It demonstrates how to trigger AI generation for these specific test cases
and shows the current database status before and after testing.
"""

import asyncio
import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Add dashboard_app to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

# Import required modules
from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.key_findings_service import KeyFindingsService
from dashboard_app.database import get_database_manager
from dashboard_app.key_findings.unified_ai_service import get_unified_ai_service


class CalidadTotalCombinationTester:
    """Test specific Calidad Total combinations with detailed logging."""
    
    def __init__(self):
        self.precomputed_db = get_precomputed_db_manager()
        self.main_db = get_database_manager()
        
        # Target combinations for testing
        self.test_combinations = [
            {
                "name": "Single Source - Google Trends",
                "tool": "Calidad Total",
                "sources": ["Google Trends"],
                "language": "es",
                "description": "Most common single-source analysis"
            },
            {
                "name": "Multi-Source - All 5 Sources",
                "tool": "Calidad Total", 
                "sources": ["Google Trends", "Google Books", "Bain Usability", "Crossref", "Bain Satisfaction"],
                "language": "es",
                "description": "Comprehensive multi-source analysis"
            }
        ]
    
    def check_current_status(self):
        """Check current database status for target combinations."""
        print("🔍 CURRENT DATABASE STATUS")
        print("=" * 60)
        
        # Get overall statistics
        stats = self.precomputed_db.get_statistics()
        print(f"📊 Precomputed Database: {stats['total_findings']} total records")
        print(f"📊 By Language: {stats['findings_by_language']}")
        print(f"📊 By Type: {stats['findings_by_type']}")
        
        # Check specific Calidad Total combinations
        print(f"\n🎯 CALIDAD TOTAL SPECIFIC STATUS:")
        tool_name = "Calidad Total"
        
        with self.precomputed_db.get_connection() as conn:
            cursor = conn.execute('''
                SELECT sources_text, language, analysis_type, access_count, 
                       last_accessed, computation_timestamp
                FROM precomputed_findings 
                WHERE tool_name = ? AND is_active = 1
                ORDER BY sources_count, language
            ''', (tool_name,))
            
            existing_records = cursor.fetchall()
            
            if existing_records:
                print(f"  Existing Calidad Total records ({len(existing_records)}):")
                for record in existing_records:
                    print(f"    • {record['sources_text']} ({record['language']}) - {record['analysis_type']}")
                    print(f"      Accessed: {record['access_count']} times, Last: {record['last_accessed']}")
            else:
                print("  ❌ No Calidad Total records found")
        
        # Check target combinations specifically
        print(f"\n🎯 TARGET COMBINATIONS STATUS:")
        for combo in self.test_combinations:
            sources_text = ", ".join(combo["sources"])
            hash_value = self.precomputed_db.generate_combination_hash(
                combo["tool"], combo["sources"], combo["language"]
            )
            
            result = self.precomputed_db.get_combination_by_hash(hash_value)
            status = "✅ EXISTS" if result else "❌ MISSING"
            print(f"  {status}: {combo['name']}")
            print(f"    Sources: {sources_text}")
            print(f"    Hash: {hash_value}")
            if result:
                print(f"    Has executive summary: {bool(result.get('executive_summary'))}")
                print(f"    Confidence: {result.get('confidence_score', 'N/A')}")
            print()
    
    async def test_key_findings_generation(self, force_refresh=True):
        """Test AI generation for target combinations."""
        print("🧪 TESTING KEY FINDINGS GENERATION")
        print("=" * 60)
        
        # Initialize Key Findings Service
        try:
            # Get AI service (you may need to configure API keys)
            ai_service = get_unified_ai_service()
            
            # Initialize Key Findings Service
            kf_service = KeyFindingsService(
                db_manager=self.main_db,
                groq_api_key=os.getenv("GROQ_API_KEY"),
                openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
                config={"cache_ttl": 3600}  # 1 hour for testing
            )
            
            print("✅ Key Findings Service initialized")
            
        except Exception as e:
            print(f"❌ Failed to initialize Key Findings Service: {e}")
            print("💡 Make sure API keys are configured in environment variables:")
            print("   - GROQ_API_KEY")
            print("   - OPENROUTER_API_KEY")
            return
        
        # Test each combination
        for i, combo in enumerate(self.test_combinations, 1):
            print(f"\n🧪 TEST {i}/{len(self.test_combinations)}: {combo['name']}")
            print(f"   📝 {combo['description']}")
            print(f"   🎯 Tool: {combo['tool']}")
            print(f"   📊 Sources: {combo['sources']}")
            print(f"   🌍 Language: {combo['language']}")
            
            start_time = time.time()
            
            try:
                # Generate Key Findings
                result = await kf_service.generate_key_findings(
                    tool_name=combo["tool"],
                    selected_sources=combo["sources"],
                    language=combo["language"],
                    force_refresh=force_refresh,
                    source_display_names=combo["sources"]
                )
                
                response_time = int((time.time() - start_time) * 1000)
                
                if result["success"]:
                    print(f"   ✅ SUCCESS!")
                    print(f"   🚀 Source: {result['source']}")
                    print(f"   ⚡ Response Time: {result['response_time_ms']}ms")
                    print(f"   📊 Cache Hit: {result['cache_hit']}")
                    
                    # Analyze the content
                    data = result["data"]
                    print(f"   📋 Executive Summary: {len(data.get('executive_summary', ''))} chars")
                    print(f"   🔍 Principal Findings: {len(data.get('principal_findings', ''))} chars")
                    print(f"   📈 PCA Analysis: {len(data.get('pca_analysis', ''))} chars")
                    print(f"   🎯 Confidence Score: {data.get('confidence_score', 'N/A')}")
                    print(f"   🤖 Model Used: {data.get('model_used', 'N/A')}")
                    print(f"   📊 Data Points: {data.get('data_points_analyzed', 'N/A')}")
                    
                    # Show preview of executive summary
                    exec_summary = data.get('executive_summary', '')
                    if exec_summary:
                        preview = exec_summary[:200] + "..." if len(exec_summary) > 200 else exec_summary
                        print(f"   📄 Preview: {preview}")
                    
                else:
                    print(f"   ❌ FAILED: {result.get('error', 'Unknown error')}")
                    print(f"   ⏱️  Response Time: {result['response_time_ms']}ms")
                
            except Exception as e:
                print(f"   ❌ EXCEPTION: {e}")
                response_time = int((time.time() - start_time) * 1000)
                print(f"   ⏱️  Response Time: {response_time}ms")
            
            print("-" * 60)
    
    def show_database_after_test(self):
        """Show database status after testing."""
        print("\n📊 DATABASE STATUS AFTER TESTING")
        print("=" * 60)
        
        # Check if new records were created
        tool_name = "Calidad Total"
        
        with self.precomputed_db.get_connection() as conn:
            cursor = conn.execute('''
                SELECT sources_text, language, analysis_type, access_count,
                       computation_timestamp, executive_summary
                FROM precomputed_findings 
                WHERE tool_name = ? AND is_active = 1
                ORDER BY computation_timestamp DESC
            ''', (tool_name,))
            
            records = cursor.fetchall()
            
            print(f"📈 Calidad Total records after test: {len(records)}")
            
            for record in records:
                print(f"\n  📋 {record['sources_text']} ({record['language']}) - {record['analysis_type']}")
                print(f"     Computed: {record['computation_timestamp']}")
                print(f"     Accessed: {record['access_count']} times")
                has_content = bool(record['executive_summary'])
                print(f"     Has Content: {'✅' if has_content else '❌'}")
        
        # Show overall statistics
        stats = self.precomputed_db.get_statistics()
        print(f"\n📊 Overall Database: {stats['total_findings']} total records")
        print(f"📊 By Language: {stats['findings_by_language']}")
        print(f"📊 By Type: {stats['findings_by_type']}")
    
    def generate_test_report(self):
        """Generate a comprehensive test report."""
        print("\n📋 TEST REPORT SUMMARY")
        print("=" * 60)
        
        print("🎯 TARGET COMBINATIONS TESTED:")
        for i, combo in enumerate(self.test_combinations, 1):
            sources_text = ", ".join(combo["sources"])
            print(f"  {i}. {combo['name']}")
            print(f"     Tool: {combo['tool']}")
            print(f"     Sources: {sources_text}")
            print(f"     Language: {combo['language']}")
            print(f"     Description: {combo['description']}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print("  1. If tests succeeded: Your combinations are now ready for production")
        print("  2. If tests failed: Check API key configuration and data availability")
        print("  3. To clear cache: Set force_refresh=True in future tests")
        print("  4. To test other languages: Change 'language' parameter to 'en'")
        
        print(f"\n🔧 NEXT STEPS:")
        print("  1. Configure API keys if not already done:")
        print("     export GROQ_API_KEY='your-groq-key'")
        print("     export OPENROUTER_API_KEY='your-openrouter-key'")
        print("  2. Run this script again to test AI generation")
        print("  3. Check the dashboard to verify Key Findings work")
        print("  4. Monitor performance and content quality")


async def main():
    """Main test execution."""
    print("🎯 CALIDAD TOTAL COMBINATION TESTER")
    print("=" * 70)
    print("Testing specific combinations for Key Findings generation")
    print("=" * 70)
    
    tester = CalidadTotalCombinationTester()
    
    # Step 1: Check current status
    tester.check_current_status()
    
    # Step 2: Test AI generation (comment out if no API keys)
    print("\n" + "=" * 70)
    print("⚠️  NOTE: AI generation requires API keys")
    print("   If you see initialization errors, configure API keys first")
    print("=" * 70)
    
    await tester.test_key_findings_generation(force_refresh=True)
    
    # Step 3: Show final status
    tester.show_database_after_test()
    
    # Step 4: Generate report
    tester.generate_test_report()
    
    print("\n" + "=" * 70)
    print("🎉 TEST COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
