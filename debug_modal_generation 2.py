#!/usr/bin/env python3
"""
Debug test for modal generation process.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def debug_modal_generation():
    """Debug the modal generation process step by step."""
    print("🔍 Debugging modal generation process...")

    # Get database manager
    db_manager = get_precomputed_db_manager()

    # Test parameters
    selected_tool = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    print(f"🔍 Testing: {selected_tool} + {selected_sources} + {language}")

    # Get the precomputed analysis
    hash_value = db_manager.generate_combination_hash(
        tool_name=selected_tool, selected_sources=selected_sources, language=language
    )

    result = db_manager.get_combination_by_hash(hash_value)
    if not result:
        print("❌ No result found")
        return False

    print("✅ Result found in database")

    # Simulate the ai_content structure
    ai_content = {
        "executive_summary": result.get("executive_summary", ""),
        "principal_findings": result.get("principal_findings", ""),
        "temporal_analysis": result.get("temporal_analysis", ""),
        "seasonal_analysis": result.get("seasonal_analysis", ""),
        "fourier_analysis": result.get("fourier_analysis", ""),
        "strategic_synthesis": result.get("strategic_synthesis", ""),
        "conclusions": result.get("conclusions", ""),
        "pca_analysis": result.get("pca_analysis", ""),
        "heatmap_analysis": result.get("heatmap_analysis", ""),
    }

    print(f"\n🔍 Content analysis:")
    for section, content in ai_content.items():
        if isinstance(content, str):
            print(f"   {section}: {len(content)} chars")
        elif isinstance(content, list):
            print(f"   {section}: {len(content)} items")
        else:
            print(f"   {section}: {type(content)}")

    # Simulate the modal conditions
    print(f"\n🔍 Simulating modal conditions for single-source:")

    sections_to_check = [
        ("temporal_analysis", "No temporal analysis available"),
        ("seasonal_analysis", "No seasonal analysis available"),
        ("fourier_analysis", "No Fourier analysis available"),
        ("strategic_synthesis", "No strategic synthesis available"),
        ("conclusions", "No conclusions available"),
    ]

    for section, default_msg in sections_to_check:
        content = ai_content.get(section, default_msg)
        condition = content and content != default_msg
        print(
            f"   {section}: {len(content) if isinstance(content, str) else 'N/A'} chars - condition: {condition}"
        )

    # Count sections that would display
    display_sections = []
    for section, default_msg in sections_to_check:
        content = ai_content.get(section, default_msg)
        if content and content != default_msg:
            display_sections.append(section)

    print(f"\n📊 Expected modal sections:")
    print(f"   Total sections that should display: {len(display_sections)}")
    print(f"   Sections: {', '.join(display_sections)}")

    if len(display_sections) == 5:
        print(f"\n✅ All 5 analysis sections should display!")
        return True
    else:
        print(f"\n❌ Expected 5 sections, got {len(display_sections)}")
        return False


if __name__ == "__main__":
    success = debug_modal_generation()
    sys.exit(0 if success else 1)
