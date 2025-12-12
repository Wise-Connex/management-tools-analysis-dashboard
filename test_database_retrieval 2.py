#!/usr/bin/env python3
"""
Test database retrieval for Benchmarking analysis
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def test_database_retrieval():
    """Test that the database returns the stored analysis correctly"""

    print("🔍 TESTING DATABASE RETRIEVAL FOR BENCHMARKING ANALYSIS")
    print("=" * 60)

    # Import the database manager
    from key_findings.database_manager import KeyFindingsDBManager

    # Initialize the Key Findings database manager with local path
    print("🗃️ Initializing Key Findings database manager...")
    local_db_path = os.path.join(os.path.dirname(__file__), 'dashboard_app', 'data', 'key_findings.db')
    kf_db_manager = KeyFindingsDBManager(db_path=local_db_path)

    # Test parameters matching the dashboard query
    tool_name = "Benchmarking"
    selected_sources = [1]  # Google Trends ID
    language = "es"

    # Generate the hash using the same method as the dashboard
    query_hash = kf_db_manager.generate_scenario_hash(
        tool_name=tool_name,
        selected_sources=selected_sources,
        language=language
    )

    print(f"🔑 Generated query hash: {query_hash}")

    # Try to retrieve from database
    print("\n🔍 Retrieving from precomputed findings database...")
    stored_data = kf_db_manager.get_cached_report(scenario_hash=query_hash)

    if stored_data:
        print("✅ Successfully retrieved stored data")
        print(f"📊 Retrieved keys: {list(stored_data.keys())}")

        # Check all 7 sections
        sections = ['executive_summary', 'principal_findings', 'seasonal_analysis',
                   'temporal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']

        print("\n📊 Section analysis:")
        total_sections = 0
        for section in sections:
            content = stored_data.get(section, '')
            length = len(str(content)) if content else 0
            has_content = length > 50
            status = '✅' if has_content else '❌'
            print(f"  {status} {section}: {length} characters")
            if has_content:
                total_sections += 1
                # Show preview
                preview = str(content)[:100].replace('\n', ' ')
                print(f"    Preview: {preview}...")

        print(f"\n📊 Total sections with content: {total_sections}/7")

        if total_sections == 7:
            print("🎉 SUCCESS: All 7 sections found in database!")
            print("📋 The dashboard should now display all sections instantly from database")
            return True
        else:
            print("⚠️ WARNING: Some sections missing from database storage")
            missing_sections = [s for s in sections if not stored_data.get(s) or len(str(stored_data.get(s, ''))) <= 50]
            print(f"🔍 Missing sections: {missing_sections}")
            return False
    else:
        print("❌ Failed to retrieve stored data")
        return False

if __name__ == "__main__":
    result = test_database_retrieval()
    if result:
        print("\n🎉 Database retrieval test PASSED!")
    else:
        print("\n❌ Database retrieval test FAILED!")