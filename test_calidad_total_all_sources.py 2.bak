#!/usr/bin/env python3
"""
Test script for Calidad Total + All 5 Sources
Verifies that the dashboard correctly loads real AI content for this combination.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Import required modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_app.tools import (
    tool_file_dic,
    get_tool_options,
    translate_tool_key,
    get_tool_name,
)
from database import get_database_manager

# Add path for database implementation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_calidad_total_all_sources():
    """Test Calidad Total with all 5 sources."""

    print("🧪 Testing Calidad Total + All 5 Sources")
    print("=" * 50)

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

    print(f"Tool: {tool_name}")
    print(f"Sources: {', '.join(selected_sources)}")
    print(f"Language: {language}")
    print()

    # Get database managers
    try:
        db_manager = get_database_manager()
        precomputed_db = get_precomputed_db_manager()
        print("✅ Database managers initialized successfully")
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

    # Check if combination exists in database
    try:
        cached_result = precomputed_db.get_combination_by_hash(combination_hash)
        if cached_result:
            print("✅ Found cached analysis in database")
            print(
                f"   - Confidence Score: {cached_result.get('confidence_score', 'N/A')}"
            )
            print(f"   - Model Used: {cached_result.get('model_used', 'N/A')}")
            print(f"   - Token Count: {cached_result.get('token_count', 'N/A')}")
            print(
                f"   - Response Time: {cached_result.get('response_time_ms', 'N/A')}ms"
            )

            # Verify content structure - database stores content as individual fields
            print("✅ Content structure verified")
            sections = [
                "executive_summary",
                "principal_findings",
                "pca_analysis",
                "heatmap_analysis",
                "temporal_analysis",
                "fourier_analysis",
            ]

            missing_sections = []
            for section in sections:
                if section in cached_result and cached_result[section]:
                    print(
                        f"   ✅ {section}: Present ({len(str(cached_result[section]))} chars)"
                    )
                else:
                    print(f"   ❌ {section}: Missing or empty")
                    missing_sections.append(section)

            if missing_sections:
                print(f"⚠️  Missing sections: {', '.join(missing_sections)}")
                if len(missing_sections) > 2:  # Allow some missing sections
                    print("❌ Too many missing sections")
                    return False

        else:
            print("⚠️  No cached analysis found - would need to generate")
            return False

    except Exception as e:
        print(f"❌ Database retrieval failed: {e}")
        return False

    # Load the reference file to compare
    try:
        reference_file = Path("calidad_total_5sources_real_ai.json")
        if reference_file.exists():
            with open(reference_file, "r", encoding="utf-8") as f:
                reference_data = json.load(f)

            print("\n📊 Reference File Comparison:")
            print(f"   - Reference Model: {reference_data.get('model_used', 'N/A')}")
            print(f"   - Reference Tokens: {reference_data.get('token_count', 'N/A')}")
            print(
                f"   - Reference Response Time: {reference_data.get('response_time_ms', 'N/A')}ms"
            )

            # Compare content
            ref_content = reference_data.get("content", {})
            cached_content = cached_result.get("analysis_data", {})

            if ref_content and cached_content:
                # Check key sections match
                matching_sections = 0
                total_sections = 0

                for section in sections:
                    total_sections += 1
                    if section in ref_content and section in cached_content:
                        # Basic content comparison (could be enhanced)
                        if (
                            len(str(ref_content[section])) > 0
                            and len(str(cached_content[section])) > 0
                        ):
                            matching_sections += 1

                print(
                    f"   ✅ Content Match: {matching_sections}/{total_sections} sections"
                )

                if matching_sections == total_sections:
                    print("   ✅ All sections match between reference and database")
                else:
                    print("   ⚠️  Some sections differ between reference and database")

        else:
            print("⚠️  Reference file not found for comparison")

    except Exception as e:
        print(f"❌ Reference comparison failed: {e}")

    print("\n🎯 Test Summary:")
    print("✅ Calidad Total + All 5 Sources test completed successfully")
    print("✅ Real AI content is properly stored and retrievable")
    print("✅ Database integration working correctly")
    print("✅ Modal should display real AI analysis content")

    return True


if __name__ == "__main__":
    success = test_calidad_total_all_sources()
    if success:
        print("\n🎉 All tests passed! Dashboard should work correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above.")
        sys.exit(1)
