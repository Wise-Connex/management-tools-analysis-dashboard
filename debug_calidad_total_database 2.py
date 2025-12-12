#!/usr/bin/env python3
"""
Debug script to check what's actually in the database for Calidad Total + All 5 Sources
"""

import os
import sys
import json

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Add path for database implementation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def debug_calidad_total_database():
    """Debug what's in the database for Calidad Total."""

    print("🔍 Debugging Calidad Total + All 5 Sources Database Content")
    print("=" * 60)

    # Test configuration
    tool_name = "Calidad Total"
    selected_sources = [
        "Google Trends",
        "Bain Usability",
        "Kimi K-Test",
        "Survey Data",
        "Academic Research",
    ]
    language = "es"

    # Get database manager
    try:
        precomputed_db = get_precomputed_db_manager()
        print("✅ Database manager initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    # Generate combination hash
    try:
        combination_hash = precomputed_db.generate_combination_hash(
            tool_name=tool_name, selected_sources=selected_sources, language=language
        )
        print(f"✅ Combination hash generated: {combination_hash}")
    except Exception as e:
        print(f"❌ Hash generation failed: {e}")
        return False

    # Get the raw database result
    try:
        cached_result = precomputed_db.get_combination_by_hash(combination_hash)
        print(f"\n📊 Raw Database Result:")
        print(f"Type: {type(cached_result)}")

        if cached_result:
            print(
                f"Keys: {list(cached_result.keys()) if isinstance(cached_result, dict) else 'Not a dict'}"
            )

            if isinstance(cached_result, dict):
                for key, value in cached_result.items():
                    print(f"\n{key}:")
                    if isinstance(value, dict):
                        print(f"  Type: dict with keys: {list(value.keys())}")
                        if "content" in value:
                            content = value["content"]
                            if isinstance(content, dict):
                                print(f"  Content keys: {list(content.keys())}")
                            else:
                                print(f"  Content type: {type(content)}")
                                print(f"  Content preview: {str(content)[:200]}...")
                        elif "analysis_data" in value:
                            analysis_data = value["analysis_data"]
                            print(f"  Analysis data type: {type(analysis_data)}")
                            if isinstance(analysis_data, dict):
                                print(
                                    f"  Analysis data keys: {list(analysis_data.keys())}"
                                )
                            else:
                                print(
                                    f"  Analysis data preview: {str(analysis_data)[:200]}..."
                                )
                    else:
                        print(f"  Type: {type(value)}")
                        print(f"  Value: {str(value)[:200]}...")
        else:
            print("❌ No result found in database")

    except Exception as e:
        print(f"❌ Database retrieval failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Also check the reference file
    print(f"\n📁 Reference File Check:")
    try:
        import json
        from pathlib import Path

        reference_file = Path("calidad_total_5sources_real_ai.json")
        if reference_file.exists():
            with open(reference_file, "r", encoding="utf-8") as f:
                reference_data = json.load(f)

            print(f"✅ Reference file exists")
            print(f"   - Model: {reference_data.get('model_used', 'N/A')}")
            print(f"   - Tokens: {reference_data.get('token_count', 'N/A')}")
            print(
                f"   - Response Time: {reference_data.get('response_time_ms', 'N/A')}ms"
            )

            content = reference_data.get("content", {})
            if content:
                print(f"   - Content sections: {list(content.keys())}")
            else:
                print("   - No content found in reference file")
        else:
            print("❌ Reference file not found")

    except Exception as e:
        print(f"❌ Reference file check failed: {e}")

    return True


if __name__ == "__main__":
    debug_calidad_total_database()
