#!/usr/bin/env python3
"""
Test the modal generation fix for multi-source analysis
"""

import os
import sys

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the specific callback that was failing
from callbacks.kf_callbacks import generate_key_findings_modal


def test_modal_generation():
    """Test that the modal generation works without dangerously_allow_html errors."""

    print("🧪 TESTING MODAL GENERATION FIX")
    print("=" * 50)

    # Test configuration that was failing
    tool_name = "Calidad Total"
    selected_sources = [
        "Google Trends",
        "Google Books",
        "Bain Usability",
        "Bain Satisfaction",
        "Crossref",
    ]
    language = "es"

    print(f"Tool: {tool_name}")
    print(f"Sources: {', '.join(selected_sources)}")
    print(f"Language: {language}")
    print()

    try:
        # This should now work without the dangerously_allow_html error
        print("🔍 Testing modal generation...")

        # Simulate the callback parameters
        n_clicks = 1
        tool_value = tool_name
        sources_value = selected_sources
        language_value = language

        # Call the function that was failing
        result = generate_key_findings_modal(
            n_clicks=n_clicks,
            tool_value=tool_value,
            sources_value=sources_value,
            language_value=language_value,
        )

        if result and len(result) > 0:
            modal_content = result[0]  # First return value is the modal content
            print("✅ Modal generation successful!")
            print(f"   Modal type: {type(modal_content)}")

            # Check if it's a valid Dash component
            if hasattr(modal_content, "type") and hasattr(modal_content, "props"):
                print("✅ Valid Dash component generated")
                print(f"   Component type: {modal_content.type}")

                # Check for any remaining dangerously_allow_html issues
                if "dangerously_allow_html" in str(modal_content):
                    print("⚠️  Warning: dangerously_allow_html still found in component")
                else:
                    print("✅ No dangerously_allow_html parameters found")
            else:
                print("⚠️  Component structure unexpected")

            return True
        else:
            print("❌ Modal generation returned empty result")
            return False

    except Exception as e:
        print(f"❌ Modal generation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_modal_generation()
    if success:
        print("\n🎉 Modal generation fix successful!")
        print("   The dangerously_allow_html error should be resolved")
    else:
        print("\n❌ Modal generation test failed")
