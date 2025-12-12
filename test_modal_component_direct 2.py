#!/usr/bin/env python3
"""
Test the modal component directly to debug the issue.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_modal_component_direct():
    """Test the modal component _extract_text_content function directly."""
    print("🔍 Testing modal component _extract_text_content function...")

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

    # Test the modal component _extract_text_content function
    print(f"\n🔍 Testing modal component _extract_text_content:")

    # Create a mock modal component to test the function
    class MockModalComponent:
        def _extract_text_content(self, content):
            """Copy of the actual modal component _extract_text_content function."""
            print(
                f"   _extract_text_content called with: {type(content)}, length: {len(content) if isinstance(content, str) else 'N/A'}"
            )

            if isinstance(content, str):
                print(f"   Processing string content...")
                # Check if it's JSON formatted
                if content.strip().startswith("{") and content.strip().endswith("}"):
                    print(f"   Detected JSON format, attempting to parse...")
                    try:
                        # Try to parse as JSON and extract text
                        import json

                        json_data = json.loads(content)
                        print(f"   Successfully parsed JSON: {type(json_data)}")
                        if isinstance(json_data, dict):
                            # Look for common text fields - prioritize heatmap_analysis for new structure
                            for field in [
                                "executive_summary",
                                "principal_findings",
                                "heatmap_analysis",
                                "pca_analysis",
                                "bullet_point",
                                "analysis",
                            ]:
                                if field in json_data:
                                    print(f"   Found field '{field}' in JSON")
                                    if isinstance(json_data[field], str):
                                        print(f"   Returning string value for {field}")
                                        return json_data[field]
                                    elif (
                                        isinstance(json_data[field], dict)
                                        and field == "analysis"
                                    ):
                                        print(
                                            f"   Converting JSON analysis to narrative"
                                        )
                                        return self._convert_json_to_narrative(
                                            json_data
                                        )
                    except Exception as e:
                        print(f"   JSON parsing failed: {e}")
                        pass

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
                                result = "\n\n".join(formatted_items)
                                print(f"   Formatted result length: {len(result)}")
                                return result
                    except Exception as e:
                        print(f"   List parsing failed: {e}")
                        pass

                print(f"   Returning content as-is")
                return content

            elif isinstance(content, dict):
                print(f"   Processing dict content...")
                # Extract from dictionary - prioritize heatmap_analysis for new structure
                for field in [
                    "executive_summary",
                    "principal_findings",
                    "heatmap_analysis",
                    "pca_analysis",
                    "bullet_point",
                    "analysis",
                ]:
                    if field in content:
                        print(f"   Found field '{field}' in dict")
                        if isinstance(content[field], str):
                            print(f"   Returning string value for {field}")
                            return content[field]
                        elif isinstance(content[field], dict) and field == "analysis":
                            print(f"   Converting JSON analysis to narrative")
                            return self._convert_json_to_narrative(content)

            elif isinstance(content, list) and content:
                print(f"   Processing list content...")
                # Extract from list - handle principal_findings format
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
                else:
                    # Original logic for other list types
                    first_item = content[0]
                    if isinstance(first_item, dict):
                        for field in ["bullet_point", "text", "content"]:
                            if field in first_item and isinstance(
                                first_item[field], str
                            ):
                                print(f"   Found {field} in first item")
                                return first_item[field]
                    elif isinstance(first_item, str):
                        print(f"   Returning first item as string")
                        return first_item

            print(f"   Fallback: converting to string")
            return str(content) if content else ""

        def _convert_json_to_narrative(self, json_data):
            """Mock function for JSON to narrative conversion."""
            return "JSON narrative conversion"

    # Test the function
    mock_component = MockModalComponent()

    # Test principal findings
    principal_findings_data = result.get("principal_findings", "")
    print(f"\n🔍 Testing principal_findings:")
    print(f"   Input type: {type(principal_findings_data)}")
    print(f"   Input length: {len(principal_findings_data)}")

    formatted_pf = mock_component._extract_text_content(principal_findings_data)
    print(f"   Output length: {len(formatted_pf)}")
    print(f"   Output preview: {formatted_pf[:200]}...")

    # Test conclusions
    conclusions_data = result.get("conclusions", "")
    print(f"\n🔍 Testing conclusions:")
    print(f"   Input type: {type(conclusions_data)}")
    print(f"   Input length: {len(conclusions_data)}")

    formatted_conclusions = mock_component._extract_text_content(conclusions_data)
    print(f"   Output length: {len(formatted_conclusions)}")
    print(f"   Output preview: {formatted_conclusions[:200]}...")

    print(f"\n📊 Final Results:")
    print(f"   Principal Findings: {len(formatted_pf)} chars (formatted)")
    print(f"   Conclusions: {len(formatted_conclusions)} chars")

    if len(formatted_pf) > 100 and len(formatted_conclusions) > 100:
        print(f"\n🎉 SUCCESS: Modal component _extract_text_content working correctly!")
        return True
    else:
        print(
            f"\n❌ ISSUE: Modal component _extract_text_content not working as expected"
        )
        return False


if __name__ == "__main__":
    success = test_modal_component_direct()
    sys.exit(0 if success else 1)
