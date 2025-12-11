#!/usr/bin/env python3
"""
Final integration test for single-source modal formatting fixes.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def simulate_complete_modal():
    """Simulate the complete modal generation process."""
    print("🧪 Simulating complete modal generation process...")

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

    # Simulate the complete modal data structure
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

    print(f"\n🔍 Simulating extract_text_content() function:")

    # Simulate extract_text_content for each section
    def simulate_extract_text_content(content, section_name):
        """Simulate the extract_text_content function."""
        if len(selected_sources) == 1 and isinstance(content, str):
            # Try to parse as JSON list first (for principal_findings)
            try:
                import ast

                parsed_list = ast.literal_eval(content)
                if isinstance(parsed_list, list):
                    print(
                        f"   {section_name}: Parsed as list with {len(parsed_list)} items"
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
                # If not a valid list format, return as string
                if not content.startswith("{"):
                    print(
                        f"   {section_name}: Raw text content, length: {len(content)}"
                    )
                    return content

        # Default: return as-is
        print(
            f"   {section_name}: Default processing, length: {len(content) if isinstance(content, str) else 'N/A'}"
        )
        return content

    # Process each section
    processed_content = {}
    for section, content in ai_content.items():
        processed_content[section] = simulate_extract_text_content(content, section)

    print(f"\n🔍 Simulating modal section generation:")

    # Simulate modal sections
    modal_sections = []

    # 1. Executive Summary
    executive_summary = processed_content.get("executive_summary", "")
    if executive_summary and len(executive_summary) > 50:
        print(f"✅ Executive Summary: {len(executive_summary)} chars - WILL DISPLAY")
        modal_sections.append("executive_summary")
    else:
        print(
            f"❌ Executive Summary: {len(executive_summary) if isinstance(executive_summary, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    # 2. Principal Findings
    principal_findings = processed_content.get("principal_findings", "")
    if principal_findings and len(principal_findings) > 50:
        print(f"✅ Principal Findings: {len(principal_findings)} chars - WILL DISPLAY")
        modal_sections.append("principal_findings")
    else:
        print(
            f"❌ Principal Findings: {len(principal_findings) if isinstance(principal_findings, str) else 'invalid'} chars - WILL NOT DISPLAY"
        )

    # 3. Other sections
    critical_sections = [
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "strategic_synthesis",
        "conclusions",
    ]

    for section in critical_sections:
        content = processed_content.get(section, "")
        if content and len(content) > 50:
            print(
                f"✅ {section.replace('_', ' ').title()}: {len(content)} chars - WILL DISPLAY"
            )
            modal_sections.append(section)
        else:
            print(
                f"❌ {section.replace('_', ' ').title()}: {len(content) if isinstance(content, str) else 'invalid'} chars - WILL NOT DISPLAY"
            )

    print(f"\n📊 Final modal simulation:")
    print(f"   Total sections that will display: {len(modal_sections)}")
    print(f"   Sections: {', '.join(modal_sections)}")

    # Show preview of formatted content
    print(f"\n📝 Content preview:")
    print(f"   Executive Summary (first 200 chars):")
    print(f"   {processed_content.get('executive_summary', '')[:200]}...")
    print(f"\n   Principal Findings (first 300 chars):")
    print(f"   {processed_content.get('principal_findings', '')[:300]}...")
    print(f"\n   Conclusions (first 200 chars):")
    print(f"   {processed_content.get('conclusions', '')[:200]}...")

    # Expected: 7 sections for single-source
    expected_sections = 7
    if len(modal_sections) == expected_sections:
        print(
            f"\n🎉 SUCCESS: Single-source modal will display all {expected_sections} sections with proper formatting!"
        )
        return True
    else:
        print(
            f"\n⚠️  ISSUE: Expected {expected_sections} sections, got {len(modal_sections)}"
        )
        return False


if __name__ == "__main__":
    success = simulate_complete_modal()
    sys.exit(0 if success else 1)
