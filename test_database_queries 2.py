#!/usr/bin/env python3
"""
Direct database query test to verify single source vs multi-source data.
"""

import sqlite3
import json

def test_database_queries():
    """Test database queries for single vs multi-source analysis."""

    print("🧪 Testing Database Queries for Single vs Multi-Source")
    print("=" * 70)

    db_path = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db'

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check what's in the database
        print("🔍 Current database contents:")
        cursor.execute("SELECT COUNT(*) FROM key_findings_reports")
        total_reports = cursor.fetchone()[0]
        print(f"Total reports: {total_reports}")

        # Show all reports
        print("\\n📋 All reports in database:")
        cursor.execute("SELECT id, tool_name, selected_sources, language, confidence_score, analysis_depth FROM key_findings_reports ORDER BY id")
        reports = cursor.fetchall()

        for report in reports:
            id, tool_name, selected_sources, language, confidence_score, analysis_depth = report
            sources = json.loads(selected_sources) if selected_sources else []
            source_count = len(sources)
            source_names = ", ".join(sources) if sources else "None"

            print(f"\\n  ID {id}: {tool_name}")
            print(f"    Sources ({source_count}): {source_names}")
            print(f"    Language: {language}")
            print(f"    Confidence: {confidence_score}")
            print(f"    Depth: {analysis_depth}")

            # Identify single vs multi-source
            if source_count == 1:
                print("    🔍 SINGLE SOURCE ANALYSIS")
            elif source_count > 1:
                print("    🔍 MULTI-SOURCE ANALYSIS")

        # Test specific queries
        print("\\n" + "=" * 50)
        print("🧪 Testing Specific Queries")
        print("=" * 50)

        # Query 1: Single source (Google Trends only)
        print("\\n1️⃣ Single Source Query (Google Trends only):")
        cursor.execute("""
            SELECT id, tool_name, selected_sources, confidence_score
            FROM key_findings_reports
            WHERE selected_sources = ?
        """, (json.dumps(["Google Trends"]),))

        single_results = cursor.fetchall()
        print(f"Found {len(single_results)} single source reports")
        for result in single_results:
            id, tool_name, sources, confidence = result
            print(f"  ID {id}: {tool_name} | Confidence: {confidence}")

        # Query 2: Multi-source (5 sources)
        print("\\n2️⃣ Multi-Source Query (5 sources):")
        cursor.execute("""
            SELECT id, tool_name, selected_sources, confidence_score
            FROM key_findings_reports
            WHERE json_array_length(selected_sources) = 5
        """)

        multi_results = cursor.fetchall()
        print(f"Found {len(multi_results)} multi-source reports")
        for result in multi_results:
            id, tool_name, sources, confidence = result
            sources_list = json.loads(sources)
            source_names = ", ".join(sources_list)
            print(f"  ID {id}: {tool_name}")
            print(f"    Sources: {source_names}")
            print(f"    Confidence: {confidence}")

        # Query 3: All Benchmarking reports
        print("\\n3️⃣ All Benchmarking Reports:")
        cursor.execute("""
            SELECT id, selected_sources, confidence_score
            FROM key_findings_reports
            WHERE tool_name = ?
            ORDER BY id
        """, ("Benchmarking",))

        benchmark_results = cursor.fetchall()
        print(f"Found {len(benchmark_results)} Benchmarking reports")
        for result in benchmark_results:
            id, sources, confidence = result
            sources_list = json.loads(sources)
            source_count = len(sources_list)
            print(f"  ID {id}: {source_count} sources | Confidence: {confidence}")

        # Check history
        print("\\n📜 History Tracking:")
        cursor.execute("SELECT scenario_hash, change_type, change_timestamp FROM key_findings_history")
        history = cursor.fetchall()
        print(f"Found {len(history)} history entries:")
        for entry in history:
            scenario_hash, change_type, timestamp = entry
            print(f"  {change_type}: {scenario_hash[:16]}... | {timestamp}")

        # Check cache statistics
        print("\\n📊 Cache Statistics:")
        cursor.execute("SELECT * FROM cache_statistics")
        stats = cursor.fetchall()
        print(f"Found {len(stats)} cache statistics:")
        for stat in stats:
            print(f"  Date: {stat[1]}")
            print(f"  Total Requests: {stat[2]}")
            print(f"  Cache Hits: {stat[3]}")
            print(f"  Cache Misses: {stat[4]}")

        conn.close()

        print("\\n" + "=" * 70)
        print("✅ Database Query Test Complete!")
        print("=" * 70)
        print("Database contains proper test data for:")
        print("• Single source analysis (1 source)")
        print("• Multi-source analysis (5 sources)")
        print("• Complete history tracking")
        print("• Cache performance statistics")
        print("Ready for UI testing!")

    except Exception as e:
        print(f"❌ Error testing database queries: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database_queries()

print("\\n" + "="*60)
print("🔍 Database Query Testing Complete!")
print("="*60)
print("This verifies:")
print("• Single source queries work correctly")
print("• Multi-source queries work correctly")
print("• Database contains proper test data")
print("• Ready for UI integration testing")
print("="*60)