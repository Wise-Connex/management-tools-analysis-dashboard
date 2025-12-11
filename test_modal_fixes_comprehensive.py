#!/usr/bin/env python3
"""
Comprehensive test for modal formatting fixes.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_modal_fixes():
    """Test the modal formatting fixes comprehensively."""
    print("🧪 Testing comprehensive modal formatting fixes...")

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

    # Test principal findings formatting
    principal_findings_data = result.get("principal_findings", "")
    print(f"\n🔍 Testing principal_findings formatting:")
    print(f"   Raw data type: {type(principal_findings_data)}")
    print(
        f"   Raw data length: {len(principal_findings_data) if isinstance(principal_findings_data, str) else 'N/A'}"
    )

    # Try to parse as list (it's stored as string in database)
    try:
        import ast

        parsed_data = ast.literal_eval(principal_findings_data)
        if isinstance(parsed_data, list):
            print(f"   Parsed as list: {len(parsed_data)} items")
            principal_findings_data = parsed_data
        else:
            print(f"   Parsed but not list: {type(parsed_data)}")
    except Exception as e:
        print(f"   Parse failed: {e}")

    if isinstance(principal_findings_data, list) and principal_findings_data:
        print(f"   First item: {principal_findings_data[0]}")
        print(f"   Last item: {principal_findings_data[-1]}")

        # Simulate the formatting logic
        formatted_items = []
        for item in principal_findings_data:
            if isinstance(item, dict) and "bullet_point" in item:
                bullet = item["bullet_point"]
                reasoning = item.get("reasoning", "")
                if reasoning:
                    formatted_items.append(f"• {bullet}\n  {reasoning}")
                else:
                    formatted_items.append(f"• {bullet}")

        formatted_result = "\n\n".join(formatted_items)
        print(f"   Formatted result length: {len(formatted_result)} chars")
        print(f"   Formatted result preview:")
        print(f"   {formatted_result[:300]}...")

        if len(formatted_items) > 0:
            print(f"✅ Principal findings formatting: SUCCESS")
        else:
            print(f"❌ Principal findings formatting: FAILED")
            return False
    else:
        print(f"❌ Principal findings data invalid or empty")
        return False

    # Test conclusions content
    conclusions_content = result.get("conclusions", "")
    print(f"\n🔍 Testing conclusions content:")
    print(f"   Conclusions type: {type(conclusions_content)}")
    print(
        f"   Conclusions length: {len(conclusions_content) if isinstance(conclusions_content, str) else 'N/A'}"
    )

    if isinstance(conclusions_content, str) and len(conclusions_content) > 100:
        print(f"   Conclusions first 200 chars: {conclusions_content[:200]}")
        print(f"   Conclusions last 200 chars: {conclusions_content[-200:]}")
        print(f"✅ Conclusions content: SUCCESS")
    else:
        print(f"❌ Conclusions content: FAILED")
        return False

    # Test all sections
    sections = [
        "executive_summary",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "strategic_synthesis",
        "conclusions",
    ]

    print(f"\n🔍 Testing all section content:")
    all_good = True
    for section in sections:
        content = result.get(section, "")
        if isinstance(content, str) and len(content) > 100:
            print(f"✅ {section}: {len(content)} chars")
        else:
            print(
                f"❌ {section}: {len(content) if isinstance(content, str) else 'invalid'} chars"
            )
            all_good = False

    if all_good:
        print(f"\n🎉 All formatting fixes ready for implementation!")
        return True
    else:
        print(f"\n⚠️  Some sections have issues")
        return False


if __name__ == "__main__":
    success = test_modal_fixes()
    sys.exit(0 if success else 1)
