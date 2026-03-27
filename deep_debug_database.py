#!/usr/bin/env python3
"""
Deep debug script to check database storage and parsing
"""

import os
import sys
import json

# Add database implementation path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "database_implementation"))

try:
    from precomputed_findings_db import get_precomputed_db_manager

    print("✅ Successfully imported database manager")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def deep_debug_database():
    """Deep debug of database content and parsing."""
    print("🔍 Deep Database Debug for Benchmarking Analysis")
    print("=" * 55)

    try:
        # Initialize database manager
        db_manager = get_precomputed_db_manager()

        # Get the existing analysis
        hash_value = "benchmarking_google_trends_es_457d64d712"
        analysis = db_manager.get_combination_by_hash(hash_value)

        if not analysis:
            print("❌ No analysis found")
            return

        print(f"✅ Found analysis ID: {analysis.get('id')}")
        print(f"Tool: {analysis.get('tool_name')}")
        print(f"Language: {analysis.get('language')}")

        # Check all fields in the analysis
        print(f"\n📊 All analysis fields:")
        for key, value in analysis.items():
            if key == "analysis_data":
                print(
                    f"  🔍 {key}: {type(value)} - Length: {len(str(value)) if value else 'None'}"
                )
                if value:
                    # Try to parse as JSON
                    try:
                        parsed = json.loads(value)
                        print(f"    ✅ Successfully parsed as JSON")
                        print(f"    📋 JSON type: {type(parsed)}")
                        if isinstance(parsed, dict):
                            print(f"    📝 JSON keys: {list(parsed.keys())}")
                            for k, v in parsed.items():
                                print(f"      - {k}: {len(str(v))} chars")
                    except json.JSONDecodeError as e:
                        print(f"    ❌ JSON parsing failed: {e}")
                        print(f"    📄 Raw data preview: {str(value)[:200]}...")
            else:
                print(f"  📝 {key}: {type(value)} - {str(value)[:100]}...")

        # Check if there are other records
        print(f"\n🔍 Checking all records in database...")
        with db_manager.get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, tool_name, language, combination_hash, is_active FROM precomputed_findings ORDER BY id"
            )
            all_records = cursor.fetchall()

        print(f"📊 Total records in database: {len(all_records)}")
        for record in all_records:
            print(
                f"  ID {record[0]}: {record[1]} + {record[2]} ({record[3]}) - Active: {record[4]}"
            )

        # Try to store a fresh record to test
        print(f"\n🧪 Testing fresh storage...")
        test_data = {
            "executive_summary": "Test summary",
            "conclusions": "Test conclusions",
        }

        try:
            test_id = db_manager.store_precomputed_analysis(
                combination_hash="test_debug_123",
                tool_name="Test Tool",
                selected_sources=["Test Source"],
                language="en",
                analysis_data=test_data,
            )
            print(f"✅ Test storage successful: ID {test_id}")

            # Retrieve test record
            test_analysis = db_manager.get_combination_by_hash("test_debug_123")
            if test_analysis:
                test_data_parsed = json.loads(test_analysis.get("analysis_data", "{}"))
                print(f"✅ Test retrieval successful: {len(test_data_parsed)} sections")

        except Exception as e:
            print(f"❌ Test storage failed: {e}")

    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    deep_debug_database()
