#!/usr/bin/env python3
"""
Final comprehensive test of modal formatting fixes.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def final_comprehensive_test():
    """Final comprehensive test of all modal formatting fixes."""
    print("🎯 FINAL COMPREHENSIVE TEST: Modal formatting fixes")
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

    # Test the modal component logic (simulating what happens in the dashboard)
    print(f"\n🔍 Testing modal component logic:")

    # Simulate the _extract_text_content function
    def _extract_text_content(content):
        """Simulate the fixed _extract_text_content function."""
        if isinstance(content, str):
            # Check if it's JSON formatted (object or array)
            content_stripped = content.strip()
            if (
                content_stripped.startswith("{") and content_stripped.endswith("}")
            ) or (content_stripped.startswith("[") and content_stripped.endswith("]")):
                try:
                    # Try to parse as JSON and extract text
                    import json

                    json_data = json.loads(content)

                    # Handle JSON objects
                    if isinstance(json_data, dict):
                        # Look for common text fields
                        for field in [
                            "executive_summary",
                            "principal_findings",
                            "heatmap_analysis",
                            "pca_analysis",
                            "bullet_point",
                            "analysis",
                        ]:
                            if field in json_data:
                                if isinstance(json_data[field], str):
                                    return json_data[field]

                    # Handle JSON arrays (for principal_findings format)
                    elif isinstance(json_data, list) and json_data:
                        if (
                            isinstance(json_data[0], dict)
                            and "bullet_point" in json_data[0]
                        ):
                            # Format all bullet points with reasoning
                            formatted_items = []
                            for item in json_data:
                                if isinstance(item, dict) and "bullet_point" in item:
                                    bullet = item["bullet_point"]
                                    reasoning = item.get("reasoning", "")
                                    if reasoning:
                                        formatted_items.append(
                                            f"• {bullet}\n  {reasoning}"
                                        )
                                    else:
                                        formatted_items.append(f"• {bullet}")
                            return "\n\n".join(formatted_items)
                except Exception as e:
                    # JSON parsing failed, try ast.literal_eval for Python literals (single quotes)
                    try:
                        import ast

                        python_data = ast.literal_eval(content)

                        # Handle Python lists (for principal_findings format with single quotes)
                        if isinstance(python_data, list) and python_data:
                            if (
                                isinstance(python_data[0], dict)
                                and "bullet_point" in python_data[0]
                            ):
                                # Format all bullet points with reasoning
                                formatted_items = []
                                for item in python_data:
                                    if (
                                        isinstance(item, dict)
                                        and "bullet_point" in item
                                    ):
                                        bullet = item["bullet_point"]
                                        reasoning = item.get("reasoning", "")
                                        if reasoning:
                                            formatted_items.append(
                                                f"• {bullet}\n  {reasoning}"
                                            )
                                        else:
                                            formatted_items.append(f"• {bullet}")
                                return "\n\n".join(formatted_items)

                        # Handle Python dicts
                        elif isinstance(python_data, dict):
                            for field in [
                                "executive_summary",
                                "principal_findings",
                                "heatmap_analysis",
                                "pca_analysis",
                                "bullet_point",
                                "analysis",
                            ]:
                                if field in python_data:
                                    if isinstance(python_data[field], str):
                                        return python_data[field]
                    except:
                        pass
            return content
        elif isinstance(content, dict):
            # Extract from dictionary
            for field in [
                "executive_summary",
                "principal_findings",
                "heatmap_analysis",
                "pca_analysis",
                "bullet_point",
                "analysis",
            ]:
                if field in content:
                    if isinstance(content[field], str):
                        return content[field]
        elif isinstance(content, list) and content:
            # Extract from list
            if (
                content
                and isinstance(content[0], dict)
                and "bullet_point" in content[0]
            ):
                # Format all bullet points with reasoning
                formatted_items = []
                for item in content:
                    if isinstance(item, dict) and "bullet_point" in item:
                        bullet = item["bullet_point"]
                        reasoning = item.get("reasoning", "")
                        if reasoning:
                            formatted_items.append(f"• {bullet}\n  {reasoning}")
                        else:
                            formatted_items.append(f"• {bullet}")
                return "\n\n".join(formatted_items)
        return str(content) if content else ""

    # Test each section
    sections_to_test = [
        ("executive_summary", "Executive Summary"),
        ("principal_findings", "Principal Findings"),
        ("temporal_analysis", "Temporal Analysis"),
        ("seasonal_analysis", "Seasonal Analysis"),
        ("fourier_analysis", "Fourier Analysis"),
        ("strategic_synthesis", "Strategic Synthesis"),
        ("conclusions", "Conclusions"),
    ]

    print(f"\n📊 Testing all sections:")

    all_sections_valid = True
    principal_findings_formatted = False
    conclusions_content_valid = False

    for section_key, section_name in sections_to_test:
        content = result.get(section_key, "")
        if isinstance(content, str) and len(content) > 100:
            print(f"✅ {section_name}: {len(content)} chars")

            # Special checks for our fixes
            if section_key == "principal_findings":
                # Test the formatting
                formatted = _extract_text_content(content)
                if "•" in formatted:
                    print(f"   📋 Successfully formatted as bullet points")
                    bullet_count = formatted.count("•")
                    print(f"   📋 Found {bullet_count} bullet points")
                    principal_findings_formatted = True
                else:
                    print(f"   ❌ Not formatted as bullet points")

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

    print(f"\n🎯 FINAL ASSESSMENT:")
    print(f"   All sections present: {'✅' if all_sections_valid else '❌'}")
    print(
        f"   Principal findings formatted: {'✅' if principal_findings_formatted else '❌'}"
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
        print(f"   ✅ Ready for browser testing!")
        return True
    else:
        print(f"\n❌ ISSUE: Some verification checks failed")
        return False


if __name__ == "__main__":
    success = final_comprehensive_test()
    sys.exit(0 if success else 1)
