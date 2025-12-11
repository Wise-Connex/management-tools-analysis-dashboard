#!/usr/bin/env python3
"""
Debug test to see what's happening in the actual dashboard modal generation.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.modal_component import KeyFindingsModal
import dash
from dash import html


def debug_dashboard_modal():
    """Debug the actual dashboard modal generation process."""
    print("🔍 Debugging actual dashboard modal generation...")

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

    # Create a mock Dash app and language store
    app = dash.Dash(__name__)

    # Create mock language store
    class MockLanguageStore:
        def get(self, key, default="es"):
            return "es"

    language_store = MockLanguageStore()

    # Create the actual KeyFindingsModal instance
    print(f"\n🔍 Creating KeyFindingsModal instance...")
    modal = KeyFindingsModal(app, language_store)

    # Test the _extract_text_content method directly
    print(f"\n🔍 Testing _extract_text_content method directly:")

    # Test principal findings
    principal_findings_data = result.get("principal_findings", "")
    print(f"   Raw principal_findings: {len(principal_findings_data)} chars")
    print(f"   First 100 chars: {principal_findings_data[:100]}")

    extracted_pf = modal._extract_text_content(principal_findings_data)
    print(f"   Extracted principal_findings: {len(extracted_pf)} chars")
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
    print(f"\n   Raw conclusions: {len(conclusions_data)} chars")
    print(f"   First 100 chars: {conclusions_data[:100]}")

    extracted_conclusions = modal._extract_text_content(conclusions_data)
    print(f"   Extracted conclusions: {len(extracted_conclusions)} chars")
    print(f"   First 200 chars: {extracted_conclusions[:200]}")

    # Test the complete modal generation
    print(f"\n🔍 Testing complete modal generation:")

    # Create the report data structure that the modal expects
    report_data = {
        "executive_summary": result.get("executive_summary", ""),
        "principal_findings": result.get("principal_findings", ""),
        "temporal_analysis": result.get("temporal_analysis", ""),
        "seasonal_analysis": result.get("seasonal_analysis", ""),
        "fourier_analysis": result.get("fourier_analysis", ""),
        "strategic_synthesis": result.get("strategic_synthesis", ""),
        "conclusions": result.get("conclusions", ""),
        "pca_analysis": result.get("pca_analysis", ""),
        "heatmap_analysis": result.get("heatmap_analysis", ""),
        "analysis_type": "single_source",  # This is important!
    }

    print(f"   Report data keys: {list(report_data.keys())}")
    print(f"   Analysis type: {report_data.get('analysis_type', 'unknown')}")

    # Test the modal content generation
    try:
        modal_content = modal.generate_modal_content(report_data, language)
        print(f"   Modal content generated successfully!")
        print(f"   Modal content type: {type(modal_content)}")

        # Check if it's a Div component
        if hasattr(modal_content, "children"):
            print(
                f"   Modal has {len(modal_content.children) if hasattr(modal_content.children, '__len__') else 'unknown'} children"
            )

            # Try to extract the actual content
            if hasattr(modal_content, "children") and modal_content.children:
                for i, child in enumerate(modal_content.children):
                    print(f"   Child {i}: {type(child)}")
                    if hasattr(child, "children"):
                        print(
                            f"     Sub-children: {len(child.children) if hasattr(child.children, '__len__') else 'unknown'}"
                        )

    except Exception as e:
        print(f"   ❌ Error generating modal content: {e}")
        import traceback

        traceback.print_exc()

    print(f"\n📊 Final Results:")
    print(f"   Principal findings formatted: {'✅' if '•' in extracted_pf else '❌'}")
    print(
        f"   Conclusions extracted: {'✅' if len(extracted_conclusions) > 100 else '❌'}"
    )

    if "•" in extracted_pf and len(extracted_conclusions) > 100:
        print(f"\n🎉 SUCCESS: Modal component working correctly!")
        return True
    else:
        print(f"\n❌ ISSUE: Modal component not working as expected")
        return False


if __name__ == "__main__":
    success = debug_dashboard_modal()
    sys.exit(0 if success else 1)
