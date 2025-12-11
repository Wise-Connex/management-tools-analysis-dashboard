#!/usr/bin/env python3
"""
Test to simulate actual dashboard modal generation with debugging.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def simulate_dashboard_modal():
    """Simulate the exact dashboard modal generation process."""
    print("🔍 Simulating dashboard modal generation process...")

    # Get database manager
    db_manager = get_precomputed_db_manager()

    # Test parameters (same as dashboard)
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

    # Simulate the exact dashboard process
    print(f"\n🔍 Simulating dashboard process:")

    # 1. Parse AI response (same as dashboard)
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

    print(f"   Available sections: {list(ai_content.keys())}")

    # 2. Extract text content (same as dashboard extract_text_content function)
    def extract_text_content(content):
        """Simulate extract_text_content function."""
        if len(selected_sources) == 1 and isinstance(content, str):
            # Try to parse as JSON list first (for principal_findings)
            try:
                import ast

                parsed_list = ast.literal_eval(content)
                if isinstance(parsed_list, list):
                    print(
                        f"   📋 Parsed principal_findings as list with {len(parsed_list)} items"
                    )
                    formatted_items = []
                    for item in parsed_list:
                        if isinstance(item, dict) and "bullet_point" in item:
                            bullet = item["bullet_point"]
                            reasoning = item.get("reasoning", "")
                            if reasoning:
                                formatted_items.append(f"• {bullet}\n  {reasoning}")
                            else:
                                formatted_items.append(f"• {bullet}")
                    return "\n\n".join(formatted_items)
            except (ValueError, SyntaxError):
                # If not a valid list format, continue with string processing
                if not content.startswith("{"):
                    return content

        # Default: return as-is
        return content

    # Extract content
    executive_summary = extract_text_content(
        ai_content.get("executive_summary", "No summary available")
    )
    principal_findings_raw = extract_text_content(
        ai_content.get("principal_findings", "No findings available")
    )
    temporal_analysis_raw = ai_content.get(
        "temporal_analysis", "No temporal analysis available"
    )
    seasonal_analysis_raw = ai_content.get(
        "seasonal_analysis", "No seasonal analysis available"
    )
    fourier_analysis_raw = ai_content.get(
        "fourier_analysis", "No Fourier analysis available"
    )
    strategic_synthesis_raw = ai_content.get(
        "strategic_synthesis", "No strategic synthesis available"
    )
    conclusions_raw = ai_content.get("conclusions", "No conclusions available")

    print(f"   Executive Summary: {len(executive_summary)} chars")
    print(f"   Principal Findings: {len(principal_findings_raw)} chars")
    print(f"   Temporal Analysis: {len(temporal_analysis_raw)} chars")
    print(f"   Seasonal Analysis: {len(seasonal_analysis_raw)} chars")
    print(f"   Fourier Analysis: {len(fourier_analysis_raw)} chars")
    print(f"   Strategic Synthesis: {len(strategic_synthesis_raw)} chars")
    print(f"   Conclusions: {len(conclusions_raw)} chars")

    # 3. Simulate modal section generation (same as dashboard)
    modal_sections = []

    # Executive Summary
    if executive_summary:
        modal_sections.append("executive_summary")
        print(f"   ✅ Executive Summary added")

    # Principal Findings
    if principal_findings_raw:
        modal_sections.append("principal_findings")
        print(f"   ✅ Principal Findings added")

    # Analysis sections
    analysis_sections = [
        ("temporal_analysis", temporal_analysis_raw, "No temporal analysis available"),
        ("seasonal_analysis", seasonal_analysis_raw, "No seasonal analysis available"),
        ("fourier_analysis", fourier_analysis_raw, "No Fourier analysis available"),
        (
            "strategic_synthesis",
            strategic_synthesis_raw,
            "No strategic synthesis available",
        ),
        ("conclusions", conclusions_raw, "No conclusions available"),
    ]

    for section_name, content, default_msg in analysis_sections:
        if content and content != default_msg:
            modal_sections.append(section_name)
            print(f"   ✅ {section_name.replace('_', ' ').title()} added")
        else:
            print(
                f"   ❌ {section_name.replace('_', ' ').title()} skipped - {content[:50] if isinstance(content, str) else 'invalid'}"
            )

    print(f"\n📊 Final modal sections:")
    print(f"   Total sections: {len(modal_sections)}")
    print(f"   Sections: {', '.join(modal_sections)}")

    expected_sections = 7  # executive_summary, principal_findings + 5 analysis sections
    if len(modal_sections) == expected_sections:
        print(f"\n🎉 SUCCESS: All {expected_sections} sections will display in modal!")
        return True
    else:
        print(
            f"\n⚠️  ISSUE: Expected {expected_sections} sections, got {len(modal_sections)}"
        )
        return False


if __name__ == "__main__":
    success = simulate_dashboard_modal()
    sys.exit(0 if success else 1)
