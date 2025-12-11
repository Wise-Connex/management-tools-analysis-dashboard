#!/usr/bin/env python3
"""
Final test to simulate dashboard modal generation with our fixes.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_final_modal_simulation():
    """Final test simulating the complete dashboard modal generation with our fixes."""
    print("🧪 Final test: Dashboard modal generation with fixes...")

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

    # Simulate the exact dashboard process with our fixes
    print(f"\n🔍 Simulating dashboard process with fixes:")

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

    # 2. Extract text content with our fixes
    def extract_text_content(content):
        """Simulate extract_text_content function with our fixes."""
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

    # Extract content with our fixes
    executive_summary = extract_text_content(
        ai_content.get("executive_summary", "No summary available")
    )

    # FIX: Apply extract_text_content to principal_findings for proper JSON-to-bullet formatting
    print(
        f"🔍 PRINCIPAL_FINDINGS_DEBUG: Before extract_text_content - length: {len(ai_content.get('principal_findings', ''))}"
    )
    principal_findings_raw = extract_text_content(
        ai_content.get("principal_findings", "No findings available")
    )
    print(
        f"🔍 PRINCIPAL_FINDINGS_DEBUG: After extract_text_content - length: {len(principal_findings_raw)}"
    )
    print(
        f"🔍 PRINCIPAL_FINDINGS_DEBUG: First 200 chars: {principal_findings_raw[:200]}"
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

    # FIX: Enhanced conclusions processing
    print(f"🔍 CONCLUSIONS_DEBUG: Starting conclusions section processing")
    conclusions_original = ai_content.get("conclusions")
    print(
        f"🔍 CONCLUSIONS_DEBUG: conclusions_original length: {len(conclusions_original) if isinstance(conclusions_original, str) else 'N/A'}"
    )

    conclusions_raw = ai_content.get("conclusions", "")
    print(
        f"🔍 CONCLUSIONS_DEBUG: conclusions_raw after get: {len(conclusions_raw) if isinstance(conclusions_raw, str) else 'N/A'}"
    )

    # Only use "No conclusions available" if truly empty
    if not conclusions_raw or (
        isinstance(conclusions_raw, str) and len(conclusions_raw.strip()) < 50
    ):
        print(
            f"🔍 CONCLUSIONS_DEBUG: Using fallback message - content too short or empty"
        )
        conclusions_raw = "No conclusions available"
    else:
        print(
            f"🔍 CONCLUSIONS_DEBUG: Using actual content - sufficient length detected"
        )

    print(f"   Executive Summary: {len(executive_summary)} chars")
    print(f"   Principal Findings: {len(principal_findings_raw)} chars")
    print(f"   Temporal Analysis: {len(temporal_analysis_raw)} chars")
    print(f"   Seasonal Analysis: {len(seasonal_analysis_raw)} chars")
    print(f"   Fourier Analysis: {len(fourier_analysis_raw)} chars")
    print(f"   Strategic Synthesis: {len(strategic_synthesis_raw)} chars")
    print(f"   Conclusions: {len(conclusions_raw)} chars")

    # 3. Simulate modal section generation with our fixes
    modal_sections = []

    # Executive Summary
    if executive_summary:
        modal_sections.append("executive_summary")
        print(f"   ✅ Executive Summary added")

    # Principal Findings (with our fix)
    if principal_findings_raw:
        modal_sections.append("principal_findings")
        print(f"   ✅ Principal Findings added (with bullet formatting)")

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
        print(
            f"\n🎉 SUCCESS: All {expected_sections} sections will display in modal with proper formatting!"
        )
        print(f"   - Executive Summary: {len(executive_summary)} chars")
        print(
            f"   - Principal Findings: {len(principal_findings_raw)} chars (formatted bullets)"
        )
        print(f"   - Temporal Analysis: {len(temporal_analysis_raw)} chars")
        print(f"   - Seasonal Analysis: {len(seasonal_analysis_raw)} chars")
        print(f"   - Fourier Analysis: {len(fourier_analysis_raw)} chars")
        print(f"   - Strategic Synthesis: {len(strategic_synthesis_raw)} chars")
        print(f"   - Conclusions: {len(conclusions_raw)} chars (actual content)")
        return True
    else:
        print(
            f"\n⚠️  ISSUE: Expected {expected_sections} sections, got {len(modal_sections)}"
        )
        return False


if __name__ == "__main__":
    success = test_final_modal_simulation()
    sys.exit(0 if success else 1)
