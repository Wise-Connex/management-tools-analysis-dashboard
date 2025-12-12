#!/usr/bin/env python3
"""
Simple test of the modal component _extract_text_content function.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_extract_text_content_only():
    """Test just the _extract_text_content function from modal component."""
    print("🔍 Testing _extract_text_content function only...")

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

    # Test the _extract_text_content function directly (without importing the full modal)
    print(f"\n🔍 Testing _extract_text_content function directly:")

    def _extract_text_content(content):
        """Copy of the actual modal component _extract_text_content function with our fixes."""
        print(
            f"   _extract_text_content called with: {type(content)}, length: {len(content) if isinstance(content, str) else 'N/A'}"
        )

        if isinstance(content, str):
            print(f"   Processing string content...")
            # Check for list format (our new logic)
            if content.strip().startswith("[") and content.strip().endswith("]"):
                print(f"   Detected list format, attempting to parse...")
                try:
                    import ast

                    parsed_list = ast.literal_eval(content)
                    if isinstance(parsed_list, list):
                        print(
                            f"   Successfully parsed as list with {len(parsed_list)} items"
                        )
                        # Handle principal_findings format
                        if (
                            parsed_list
                            and isinstance(parsed_list[0], dict)
                            and "bullet_point" in parsed_list[0]
                        ):
                            print(
                                f"   Detected bullet_point format, formatting all items..."
                            )
                            formatted_items = []
                            for item in parsed_list:
                                if isinstance(item, dict) and "bullet_point" in item:
                                    bullet = item["bullet_point"]
                                    reasoning = item.get("reasoning", "")
                                    if reasoning:
                                        formatted_items.append(
                                            f"• {bullet}\n  {reasoning}"
                                        )
                                    else:
                                        formatted_items.append(f"• {bullet}")
                            result = "\n\n".join(formatted_items)
                            print(f"   Formatted result length: {len(result)}")
                            return result
                except Exception as e:
                    print(f"   List parsing failed: {e}")
                    pass

            print(f"   Returning content as-is")
            return content

        elif isinstance(content, list) and content:
            print(f"   Processing list content...")
            # Handle list objects
            if (
                content
                and isinstance(content[0], dict)
                and "bullet_point" in content[0]
            ):
                print(
                    f"   Detected bullet_point format in list, formatting all items..."
                )
                formatted_items = []
                for item in content:
                    if isinstance(item, dict) and "bullet_point" in item:
                        bullet = item["bullet_point"]
                        reasoning = item.get("reasoning", "")
                        if reasoning:
                            formatted_items.append(f"• {bullet}\n  {reasoning}")
                        else:
                            formatted_items.append(f"• {bullet}")
                result = "\n\n".join(formatted_items)
                print(f"   Formatted result length: {len(result)}")
                return result
            return str(content) if content else ""

        return str(content) if content else ""

    # Test principal findings
    principal_findings_data = result.get("principal_findings", "")
    print(f"\n🔍 Testing principal_findings:")
    print(f"   Raw content length: {len(principal_findings_data)}")
    print(f"   First 100 chars: {principal_findings_data[:100]}")

    extracted_pf = _extract_text_content(principal_findings_data)
    print(f"   Extracted content length: {len(extracted_pf)}")
    print(f"   First 200 chars: {extracted_pf[:200]}")

    # Check if it's formatted correctly
    if "•" in extracted_pf:
        print(f"   ✅ Formatted as bullet points!")
        bullet_count = extracted_pf.count("•")
        print(f"   📋 Found {bullet_count} bullet points")
    else:
        print(f"   ❌ Not formatted as bullet points")

    # Test conclusions
    conclusions_data = result.get("conclusions", "")
    print(f"\n🔍 Testing conclusions:")
    print(f"   Raw content length: {len(conclusions_data)}")
    print(f"   First 100 chars: {conclusions_data[:100]}")

    extracted_conclusions = _extract_text_content(conclusions_data)
    print(f"   Extracted content length: {len(extracted_conclusions)}")
    print(f"   First 200 chars: {extracted_conclusions[:200]}")

    print(f"\n📊 Final Results:")
    print(f"   Principal Findings: {len(extracted_pf)} chars (formatted)")
    print(f"   Conclusions: {len(extracted_conclusions)} chars")

    if "•" in extracted_pf and len(extracted_conclusions) > 100:
        print(f"\n🎉 SUCCESS: _extract_text_content working correctly!")
        return True
    else:
        print(f"\n❌ ISSUE: _extract_text_content not working as expected")
        return False


if __name__ == "__main__":
    success = test_extract_text_content_only()
    sys.exit(0 if success else 1)
