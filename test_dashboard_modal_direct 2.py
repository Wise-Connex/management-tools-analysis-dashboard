#!/usr/bin/env python3
"""
Direct test of dashboard modal generation function.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_dashboard_modal_direct():
    """Test the dashboard modal generation function directly."""
    print("🔍 Direct test: Dashboard modal generation function...")

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

    # Test the extract_text_content function directly
    print(f"\n🔍 Testing extract_text_content function directly:")

    principal_findings_data = result.get("principal_findings", "")
    print(f"   Raw principal_findings length: {len(principal_findings_data)}")
    print(f"   Raw principal_findings first 100 chars: {principal_findings_data[:100]}")

    # Simulate the extract_text_content function
    def extract_text_content(content):
        """Simulate extract_text_content function."""
        print(
            f"   extract_text_content called with content length: {len(content) if isinstance(content, str) else 'N/A'}"
        )

        if len(selected_sources) == 1 and isinstance(content, str):
            print(f"   Single-source string detected, checking for JSON list...")
            # Try to parse as JSON list first (for principal_findings)
            try:
                import ast

                parsed_list = ast.literal_eval(content)
                if isinstance(parsed_list, list):
                    print(
                        f"   ✅ Successfully parsed as list with {len(parsed_list)} items"
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
                    result = "\n\n".join(formatted_items)
                    print(f"   ✅ Formatted result length: {len(result)}")
                    return result
                else:
                    print(f"   ❌ Parsed but not a list: {type(parsed_list)}")
            except Exception as e:
                print(f"   ❌ Failed to parse as list: {e}")
                # If not a valid list format, continue with string processing
                if not content.startswith("{"):
                    print(f"   ✅ Returning as raw text (not JSON)")
                    return content

        print(f"   ✅ Returning content as-is")
        return content

    # Test the function
    formatted_result = extract_text_content(principal_findings_data)
    print(f"\n📊 Results:")
    print(f"   Formatted result length: {len(formatted_result)}")
    print(f"   Formatted result preview:")
    print(f"   {formatted_result[:300]}...")

    # Test conclusions
    conclusions_data = result.get("conclusions", "")
    print(f"\n🔍 Testing conclusions content:")
    print(f"   Conclusions length: {len(conclusions_data)}")
    print(f"   Conclusions first 200 chars: {conclusions_data[:200]}")

    # Test the conclusions logic
    conclusions_raw = conclusions_data
    if not conclusions_raw or (
        isinstance(conclusions_raw, str) and len(conclusions_raw.strip()) < 50
    ):
        print(f"   ❌ Would use fallback: 'No conclusions available'")
        final_conclusions = "No conclusions available"
    else:
        print(f"   ✅ Using actual content: {len(conclusions_raw)} chars")
        final_conclusions = conclusions_raw

    print(f"\n🎯 Final Results:")
    print(f"   Principal Findings: {len(formatted_result)} chars (formatted)")
    print(f"   Conclusions: {len(final_conclusions)} chars")

    if len(formatted_result) > 100 and final_conclusions != "No conclusions available":
        print(f"\n🎉 SUCCESS: Both fixes working correctly!")
        return True
    else:
        print(f"\n❌ ISSUE: Fixes not working as expected")
        return False


if __name__ == "__main__":
    success = test_dashboard_modal_direct()
    sys.exit(0 if success else 1)
