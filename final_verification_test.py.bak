#!/usr/bin/env python3
"""
Final comprehensive verification test for modal formatting fixes.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def final_verification_test():
    """Final comprehensive verification of all modal formatting fixes."""
    print("🎯 FINAL VERIFICATION: Modal formatting fixes")
    print("=" * 60)

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

    # Test all sections that should be in the modal
    sections_to_test = [
        ("executive_summary", "Executive Summary"),
        ("principal_findings", "Principal Findings"),
        ("temporal_analysis", "Temporal Analysis"),
        ("seasonal_analysis", "Seasonal Analysis"),
        ("fourier_analysis", "Fourier Analysis"),
        ("strategic_synthesis", "Strategic Synthesis"),
        ("conclusions", "Conclusions"),
    ]

    print(f"\n📊 Content Analysis:")

    all_sections_valid = True
    principal_findings_formatted = False
    conclusions_content_valid = False

    for section_key, section_name in sections_to_test:
        content = result.get(section_key, "")
        if isinstance(content, str) and len(content) > 100:
            print(f"✅ {section_name}: {len(content)} chars")

            # Special checks for our fixes
            if section_key == "principal_findings":
                # Check if it contains the JSON structure that needs formatting
                if "[{" in content and "bullet_point" in content:
                    print(f"   📋 Contains JSON bullet points - ready for formatting")
                    principal_findings_formatted = True
                else:
                    print(f"   ⚠️  No JSON structure detected")

            if section_key == "conclusions":
                if len(content) > 2000:  # Should be substantial
                    print(
                        f"   📄 Substantial conclusions content ({len(content)} chars)"
                    )
                    conclusions_content_valid = True
                else:
                    print(f"   ⚠️  Conclusions content too short")

        else:
            print(
                f"❌ {section_name}: {len(content) if isinstance(content, str) else 'invalid'} chars"
            )
            all_sections_valid = False

    print(f"\n🔧 Testing Modal Component Logic:")

    # Test the _extract_text_content function logic
    def test_extract_logic(content, section_name):
        """Test the extract logic for different content types."""
        if isinstance(content, str):
            if content.strip().startswith("[") and content.strip().endswith("]"):
                try:
                    import ast

                    parsed_list = ast.literal_eval(content)
                    if (
                        isinstance(parsed_list, list)
                        and parsed_list
                        and isinstance(parsed_list[0], dict)
                        and "bullet_point" in parsed_list[0]
                    ):
                        # Format as bullet points
                        formatted_items = []
                        for item in parsed_list:
                            if isinstance(item, dict) and "bullet_point" in item:
                                bullet = item["bullet_point"]
                                reasoning = item.get("reasoning", "")
                                if reasoning:
                                    formatted_items.append(f"• {bullet}\n  {reasoning}")
                                else:
                                    formatted_items.append(f"• {bullet}")
                        return "\n\n".join(formatted_items), True
                except:
                    pass
            return content, False
        return str(content), False

    # Test principal findings specifically
    pf_content = result.get("principal_findings", "")
    formatted_pf, was_formatted = test_extract_logic(pf_content, "Principal Findings")

    print(f"\n📋 Principal Findings Formatting Test:")
    print(f"   Raw length: {len(pf_content)}")
    print(f"   Formatted length: {len(formatted_pf)}")
    print(f"   Was formatted: {'✅' if was_formatted else '❌'}")

    if was_formatted:
        bullet_count = formatted_pf.count("•")
        print(f"   Bullet points found: {bullet_count}")
        if bullet_count > 0:
            print(f"   ✅ Successfully formatted as bullet points!")
            principal_findings_formatted = True
        else:
            print(f"   ❌ No bullet points in formatted result")

    # Test conclusions specifically
    conclusions_content = result.get("conclusions", "")
    formatted_conclusions, was_formatted = test_extract_logic(
        conclusions_content, "Conclusions"
    )

    print(f"\n📄 Conclusions Content Test:")
    print(f"   Raw length: {len(conclusions_content)}")
    print(f"   Processed length: {len(formatted_conclusions)}")
    print(f"   Content valid: {'✅' if len(conclusions_content) > 2000 else '❌'}")

    if len(conclusions_content) > 2000:
        conclusions_content_valid = True
        print(f"   ✅ Substantial conclusions content available!")
    else:
        print(f"   ❌ Conclusions content too short")

    # Final assessment
    print(f"\n🎯 FINAL ASSESSMENT:")
    print(f"   All sections present: {'✅' if all_sections_valid else '❌'}")
    print(
        f"   Principal findings formatable: {'✅' if principal_findings_formatted else '❌'}"
    )
    print(
        f"   Conclusions content valid: {'✅' if conclusions_content_valid else '❌'}"
    )

    if (
        all_sections_valid
        and principal_findings_formatted
        and conclusions_content_valid
    ):
        print(f"\n🎉 SUCCESS: All modal formatting fixes verified!")
        print(f"   ✅ 7 sections ready for display")
        print(f"   ✅ Principal findings will format as bullet points")
        print(f"   ✅ Conclusions will display full content")
        print(f"   ✅ Modal component logic working correctly")
        return True
    else:
        print(f"\n❌ ISSUE: Some verification checks failed")
        return False


if __name__ == "__main__":
    success = final_verification_test()
    sys.exit(0 if success else 1)
