#!/usr/bin/env python3
"""
MANUAL TRIGGER TEST: Simple Key Findings Generation
==================================================

Simple script to manually trigger Key Findings generation for your specific combinations.
This demonstrates the exact process without complex dependencies.
"""

import sys
import os
import sqlite3
import time
from datetime import datetime

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def check_combination_exists(tool_name, sources, language="es"):
    """Check if combination exists in precomputed database."""
    db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
    
    # Generate sources text (sorted for consistency)
    sources_text = ", ".join(sorted(sources))
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT executive_summary, principal_findings, confidence_score, 
               model_used, computation_timestamp, access_count
        FROM precomputed_findings 
        WHERE tool_name = ? AND sources_text = ? AND language = ? 
        AND is_active = 1
        LIMIT 1
    """, (tool_name, sources_text, language))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "exists": True,
            "executive_summary": result[0] or "",
            "principal_findings": result[1] or "",
            "confidence_score": result[2] or 0.0,
            "model_used": result[3] or "unknown",
            "computation_timestamp": result[4],
            "access_count": result[5] or 0
        }
    else:
        return {"exists": False}


def simulate_dashboard_click(tool_name, sources, language="es"):
    """Simulate clicking Key Findings in the dashboard."""
    print(f"👤 SIMULATING: User clicks 'Key Findings'")
    print(f"   🎯 Tool: {tool_name}")
    print(f"   📊 Sources: {sources}")
    print(f"   🌍 Language: {language}")
    
    start_time = time.time()
    
    # Step 1: Check precomputed database (current implementation)
    print("1️⃣  Checking precomputed findings database...")
    result = check_combination_exists(tool_name, sources, language)
    
    if result["exists"]:
        response_time = int((time.time() - start_time) * 1000)
        print("   ✅ FOUND in precomputed database!")
        print(f"   ⚡ Response time: {response_time}ms")
        print(f"   📊 Executive Summary: {len(result['executive_summary'])} chars")
        print(f"   🔍 Principal Findings: {len(result['principal_findings'])} chars")
        print(f"   🎯 Confidence: {result['confidence_score']}")
        print(f"   🤖 Model: {result['model_used']}")
        print(f"   📅 Computed: {result['computation_timestamp']}")
        print(f"   👁️  Accessed: {result['access_count']} times before")
        
        return {
            "success": True,
            "source": "precomputed_database",
            "response_time_ms": response_time,
            "data": result
        }
    else:
        print("   ❌ NOT FOUND in precomputed database")
        
        # Step 2: Would trigger AI generation (slow, expensive)
        print("2️⃣  Would trigger AI generation...")
        print("   ⚠️  This requires API keys and takes 30-60 seconds")
        print("   💡 To test AI generation, use the comprehensive test script")
        
        response_time = int((time.time() - start_time) * 1000)
        return {
            "success": False,
            "source": "would_generate_ai",
            "response_time_ms": response_time,
            "error": "No precomputed data available - would trigger AI generation"
        }


def main():
    """Run manual trigger tests."""
    print("🎯 MANUAL TRIGGER TEST FOR CALIDAD TOTAL")
    print("=" * 60)
    print("Testing the exact combinations you requested")
    print("=" * 60)
    
    # Test combinations
    test_cases = [
        {
            "name": "Single Source - Google Trends",
            "tool": "Calidad Total",
            "sources": ["Google Trends"],
            "description": "Your first target combination"
        },
        {
            "name": "Multi-Source - All 5 Sources", 
            "tool": "Calidad Total",
            "sources": ["Google Trends", "Google Books", "Bain Usability", "Crossref", "Bain Satisfaction"],
            "description": "Your second target combination"
        }
    ]
    
    # Check overall database status first
    print("📊 DATABASE OVERVIEW")
    print("-" * 40)
    db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM precomputed_findings WHERE is_active = 1")
    total_records = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT tool_name, COUNT(*) as count 
        FROM precomputed_findings 
        WHERE is_active = 1 
        GROUP BY tool_name 
        ORDER BY count DESC
    """)
    tool_counts = cursor.fetchall()
    
    cursor.execute("""
        SELECT tool_name, sources_text, language 
        FROM precomputed_findings 
        WHERE tool_name = 'Calidad Total' AND is_active = 1
        ORDER BY sources_count, language
    """)
    calidad_records = cursor.fetchall()
    
    conn.close()
    
    print(f"Total precomputed records: {total_records}")
    print("Records by tool:")
    for tool_name, count in tool_counts:
        print(f"  • {tool_name}: {count} records")
    
    print(f"\nExisting Calidad Total records ({len(calidad_records)}):")
    for record in calidad_records:
        print(f"  • {record[1]} ({record[2]})")
    
    print("\n" + "=" * 60)
    
    # Test each combination
    successful_tests = 0
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}/{len(test_cases)}: {test_case['name']}")
        print(f"   📝 {test_case['description']}")
        print("-" * 50)
        
        result = simulate_dashboard_click(
            test_case["tool"], 
            test_case["sources"], 
            "es"
        )
        
        if result["success"]:
            successful_tests += 1
            print(f"   ✅ SUCCESS: User would see Key Findings instantly")
        else:
            print(f"   ❌ WOULD FAIL: User would see loading/error")
            print(f"   💡 SOLUTION: Generate precomputed data or configure AI generation")
        
        print()
    
    # Summary
    print("=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Successful tests: {successful_tests}/{len(test_cases)}")
    print(f"❌ Failed tests: {len(test_cases) - successful_tests}/{len(test_cases)}")
    
    if successful_tests == len(test_cases):
        print("\n🎉 ALL TESTS PASSED!")
        print("💡 Your combinations are ready for production")
        print("🚀 Users will get instant Key Findings for these combinations")
    else:
        print(f"\n⚠️  {len(test_cases) - successful_tests} TEST(S) FAILED")
        print("💡 You need to either:")
        print("   1. Generate precomputed data for missing combinations")
        print("   2. Configure AI generation for real-time analysis")
        print("   3. Use the comprehensive test script with API keys")
    
    print("\n🔧 NEXT STEPS:")
    print("1. For immediate results: Populate precomputed database")
    print("2. For dynamic results: Configure API keys and test AI generation")
    print("3. For production: Ensure all 1,302 combinations are precomputed")
    print("4. Monitor: Check dashboard performance and user feedback")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
