#!/usr/bin/env python3
"""
Simple test to verify single-source modal content structure.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_modal_content_structure():
    """Test that single-source content has all sections properly structured for modal display."""
    print("🧪 Testing modal content structure for single-source...")

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
    print(f"🔍 Generated hash: {hash_value}")

    result = db_manager.get_combination_by_hash(hash_value)
    if not result:
        print("❌ No result found")
        return False

    print("✅ Result found in database")

    # Simulate the report_data structure that gets passed to the modal
    report_data = {
        "executive_summary": result.get("executive_summary", ""),
        "principal_findings": result.get("principal_findings", []),
        "temporal_analysis": result.get("temporal_analysis", ""),
        "seasonal_analysis": result.get("seasonal_analysis", ""),
        "fourier_analysis": result.get("fourier_analysis", ""),
        "strategic_synthesis": result.get("strategic_synthesis", ""),
        "conclusions": result.get("conclusions", ""),
        "pca_analysis": result.get("pca_analysis", ""),
        "heatmap_analysis": result.get("heatmap_analysis", ""),
    }

    print(f"\n📊 Content analysis:")

    # Test each section for modal display
    critical_sections = [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "strategic_synthesis",
        "conclusions",
    ]

    all_good = True
    for section in critical_sections:
        content = report_data[section]
        if isinstance(content, str):
            length = len(content)
            if length > 100:  # Reasonable content threshold
                print(f"✅ {section}: {length} chars (ready for modal)")
            else:
                print(f"❌ {section}: {length} chars (too short)")
                all_good = False
        elif isinstance(content, list):
            length = len(content)
            if length > 0:
                print(f"✅ {section}: {length} items (ready for modal)")
            else:
                print(f"❌ {section}: {length} items (empty)")
                all_good = False
        else:
            print(f"⚠️  {section}: {type(content)} (unexpected type)")
            all_good = False

    # Test the conditions that will be used in the modal
    print(f"\n🔍 Testing modal display conditions:")

    # Simulate the modal logic
    for section in critical_sections:
        content = report_data[section]
        if isinstance(content, str):
            condition = content and content != f"No {section} available"
            print(f"   {section} display condition: {condition}")
            if not condition:
                all_good = False
        else:
            condition = bool(content)  # For lists
            print(f"   {section} display condition: {condition}")
            if not condition:
                all_good = False

    # Test conclusions specifically
    conclusions_content = report_data["conclusions"]
    conclusions_condition = (
        conclusions_content and conclusions_content != "No conclusions available"
    )
    print(f"   conclusions final condition: {conclusions_condition}")

    if all_good and conclusions_condition:
        print(f"\n🎉 All sections ready for modal display!")
        print(f"   - Executive Summary: {len(report_data['executive_summary'])} chars")
        print(
            f"   - Principal Findings: {len(report_data['principal_findings'])} items"
        )
        print(f"   - Temporal Analysis: {len(report_data['temporal_analysis'])} chars")
        print(f"   - Seasonal Analysis: {len(report_data['seasonal_analysis'])} chars")
        print(f"   - Fourier Analysis: {len(report_data['fourier_analysis'])} chars")
        print(
            f"   - Strategic Synthesis: {len(report_data['strategic_synthesis'])} chars"
        )
        print(f"   - Conclusions: {len(report_data['conclusions'])} chars")
        return True
    else:
        print(f"\n⚠️  Some sections not ready for modal display")
        return False


if __name__ == "__main__":
    success = test_modal_content_structure()
    sys.exit(0 if success else 1)
