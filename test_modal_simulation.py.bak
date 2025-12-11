#!/usr/bin/env python3
"""
Test to simulate the modal callback logic for single-source analysis.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def simulate_modal_logic():
    """Simulate the modal callback logic to verify our changes work."""
    print("🧪 Simulating modal callback logic...")

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

    # Simulate the report_data structure (this is what gets passed to the modal)
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

    # Simulate the modal logic with our changes
    ai_content = report_data
    modal_sections = []

    print(f"\n🔍 Simulating modal section generation:")

    # 1. Executive Summary Section
    executive_summary = ai_content.get("executive_summary", "")
    if executive_summary:
        print(f"✅ Executive Summary: {len(executive_summary)} chars - WILL DISPLAY")
        modal_sections.append("executive_summary")
    else:
        print(f"❌ Executive Summary: empty - WILL NOT DISPLAY")

    # 2. Principal Findings Section
    principal_findings = ai_content.get("principal_findings", [])
    if principal_findings:
        print(f"✅ Principal Findings: {len(principal_findings)} items - WILL DISPLAY")
        modal_sections.append("principal_findings")
    else:
        print(f"❌ Principal Findings: empty - WILL NOT DISPLAY")

    # 3. Temporal Analysis Section (MODIFIED: now for both single and multi-source)
    temporal_analysis = ai_content.get(
        "temporal_analysis", "No temporal analysis available"
    )
    if temporal_analysis and temporal_analysis != "No temporal analysis available":
        print(f"✅ Temporal Analysis: {len(temporal_analysis)} chars - WILL DISPLAY")
        modal_sections.append("temporal_analysis")
    else:
        print(
            f"❌ Temporal Analysis: {len(temporal_analysis) if isinstance(temporal_analysis, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    # 4. Seasonal Analysis Section (MODIFIED: now for both single and multi-source)
    seasonal_analysis = ai_content.get(
        "seasonal_analysis", "No seasonal analysis available"
    )
    if seasonal_analysis and seasonal_analysis != "No seasonal analysis available":
        print(f"✅ Seasonal Analysis: {len(seasonal_analysis)} chars - WILL DISPLAY")
        modal_sections.append("seasonal_analysis")
    else:
        print(
            f"❌ Seasonal Analysis: {len(seasonal_analysis) if isinstance(seasonal_analysis, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    # 5. Fourier Analysis Section (MODIFIED: now for both single and multi-source)
    fourier_analysis = ai_content.get(
        "fourier_analysis", "No Fourier analysis available"
    )
    if fourier_analysis and fourier_analysis != "No Fourier analysis available":
        print(f"✅ Fourier Analysis: {len(fourier_analysis)} chars - WILL DISPLAY")
        modal_sections.append("fourier_analysis")
    else:
        print(
            f"❌ Fourier Analysis: {len(fourier_analysis) if isinstance(fourier_analysis, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    # 6. Strategic Synthesis Section (NEW: now for both single and multi-source)
    strategic_synthesis = ai_content.get(
        "strategic_synthesis", "No strategic synthesis available"
    )
    if (
        strategic_synthesis
        and strategic_synthesis != "No strategic synthesis available"
    ):
        print(
            f"✅ Strategic Synthesis: {len(strategic_synthesis)} chars - WILL DISPLAY"
        )
        modal_sections.append("strategic_synthesis")
    else:
        print(
            f"❌ Strategic Synthesis: {len(strategic_synthesis) if isinstance(strategic_synthesis, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    # 7. Conclusions Section (with debugging)
    print(f"\n🔍 Conclusions section debugging:")
    print(f"   ai_content keys: {list(ai_content.keys())}")
    conclusions_value = ai_content.get("conclusions")
    print(f"   conclusions value type: {type(conclusions_value)}")
    if isinstance(conclusions_value, str):
        print(f"   conclusions length: {len(conclusions_value)}")
        print(f"   conclusions first 100 chars: {conclusions_value[:100]}")

    conclusions_raw = ai_content.get("conclusions", "No conclusions available")
    print(
        f"   conclusions_raw after get: {type(conclusions_raw)}, length: {len(conclusions_raw) if isinstance(conclusions_raw, str) else 'N/A'}"
    )

    if conclusions_raw and conclusions_raw != "No conclusions available":
        print(f"✅ Conclusions: {len(conclusions_raw)} chars - WILL DISPLAY")
        modal_sections.append("conclusions")
    else:
        print(
            f"❌ Conclusions: {len(conclusions_raw) if isinstance(conclusions_raw, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    print(f"\n📊 Final result:")
    print(f"   Total sections that will display: {len(modal_sections)}")
    print(f"   Sections: {', '.join(modal_sections)}")

    # Expected: 7 sections for single-source
    expected_sections = 7
    if len(modal_sections) == expected_sections:
        print(
            f"🎉 SUCCESS: Single-source analysis will display all {expected_sections} sections!"
        )
        return True
    else:
        print(
            f"⚠️  ISSUE: Expected {expected_sections} sections, got {len(modal_sections)}"
        )
        return False


if __name__ == "__main__":
    success = simulate_modal_logic()
    sys.exit(0 if success else 1)
