#!/usr/bin/env python3
"""
Debug script to understand database content structure for benchmarking analysis
"""

import os
import sys
import json
from pathlib import Path

# Add database implementation path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "database_implementation"))

try:
    from precomputed_findings_db import get_precomputed_db_manager

    print("✅ Successfully imported database manager")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def debug_database_content():
    """Debug the database content for benchmarking analysis."""
    print("🔍 Debugging Database Content for Benchmarking + Google Trends (es)")
    print("=" * 70)

    try:
        # Initialize database manager
        db_manager = get_precomputed_db_manager()
        print("✅ Database manager initialized")

        # Get the existing analysis
        hash_value = "benchmarking_google_trends_es_457d64d712"
        existing_analysis = db_manager.get_combination_by_hash(hash_value)

        if not existing_analysis:
            print("❌ Benchmarking analysis not found in database")
            return

        print("✅ Found existing Benchmarking analysis")
        print(f"Analysis ID: {existing_analysis.get('id', 'N/A')}")
        print(f"Tool: {existing_analysis.get('tool_name', 'N/A')}")
        print(f"Language: {existing_analysis.get('language', 'N/A')}")
        print(f"Sources: {existing_analysis.get('data_sources', 'N/A')}")

        # Debug the analysis_data field
        analysis_data_raw = existing_analysis.get("analysis_data")
        print(f"\n📊 Raw analysis_data type: {type(analysis_data_raw)}")
        print(
            f"📊 Raw analysis_data length: {len(str(analysis_data_raw)) if analysis_data_raw else 'None'}"
        )

        if analysis_data_raw:
            try:
                # Try to parse as JSON
                analysis_data = json.loads(analysis_data_raw)
                print(f"✅ Successfully parsed JSON data")
                print(f"📊 Parsed data type: {type(analysis_data)}")

                if isinstance(analysis_data, dict):
                    print(f"\n📊 All keys in analysis_data:")
                    for key in analysis_data.keys():
                        content = analysis_data.get(key, "")
                        print(f"  📝 {key}: {len(content)} chars")
                        if content:
                            print(f"     Preview: {content[:100]}...")
                        else:
                            print(f"     Content: EMPTY")

                # Check specific required sections
                required_sections = [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "strategic_synthesis",
                    "conclusions",
                ]

                print(f"\n📊 Required sections check:")
                sections_present = 0
                for section in required_sections:
                    content = analysis_data.get(section, "")
                    if content and len(content.strip()) > 10:
                        sections_present += 1
                        print(f"  ✅ {section}: {len(content)} chars")
                    else:
                        print(
                            f"  ❌ {section}: Missing or too short ({len(content)} chars)"
                        )

                print(f"\n🎯 Result: {sections_present}/7 sections present")

                # Save debug info to file
                debug_info = {
                    "hash_value": hash_value,
                    "analysis_id": existing_analysis.get("id"),
                    "analysis_data_keys": list(analysis_data.keys())
                    if isinstance(analysis_data, dict)
                    else str(analysis_data),
                    "sections_present": sections_present,
                    "total_required": 7,
                    "raw_data_length": len(str(analysis_data_raw)),
                    "parsed_data_type": str(type(analysis_data)),
                }

                with open(
                    "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/debug_database_content.json",
                    "w",
                ) as f:
                    json.dump(debug_info, f, indent=2)

                print(f"💾 Debug info saved to debug_database_content.json")

            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON: {e}")
                print(f"Raw data preview: {str(analysis_data_raw)[:200]}...")
        else:
            print("❌ analysis_data is None or empty")

    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_database_content()
