#!/usr/bin/env python3
"""
Test the actual KeyFindingsService modal component.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.key_findings_service import KeyFindingsService
import dash
from dash import html


def test_key_findings_service_modal():
    """Test the actual KeyFindingsService modal component."""
    print("🔍 TESTING: KeyFindingsService modal component...")
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

    # Create the exact data structure that gets passed to the service
    print(f"\n🔍 CREATING SERVICE DATA STRUCTURE:")

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
        "analysis_type": "single_source",
    }

    print(f"   Report data keys: {list(report_data.keys())}")
    print(f"   Analysis type: {report_data.get('analysis_type', 'unknown')}")

    # Create a minimal Dash app for testing
    print(f"\n🔍 CREATING DASH APP FOR TESTING:")
    app = dash.Dash(__name__)

    # Create a simple language store
    class SimpleLanguageStore:
        def __init__(self):
            self.id = "language-store"

        def get(self, key, default="es"):
            return "es"

    language_store = SimpleLanguageStore()

    # Create the KeyFindingsService
    print(f"🔍 CREATING KEY FINDINGS SERVICE:")
    service = KeyFindingsService()
    service.set_modal_component(app, language_store)
    print("   ✅ KeyFindingsService created and modal component set")

    # Get the modal component
    modal = service.get_modal_component()
    print(f"   ✅ Modal component retrieved: {type(modal)}")

    # Test the modal component directly
    print(f"\n🔍 TESTING MODAL COMPONENT:")

    # Test principal findings
    principal_findings_raw = report_data.get("principal_findings", "")
    print(f"   📋 PRINCIPAL FINDINGS TEST:")
    print(f"   Input length: {len(principal_findings_raw)}")
    print(f"   Input preview: {repr(principal_findings_raw[:150])}")

    # Call the actual _extract_text_content method from the service's modal
    extracted_pf = modal._extract_text_content(principal_findings_raw)
    print(f"   Output length: {len(extracted_pf)}")
    print(f"   Output preview: {repr(extracted_pf[:200])}")

    # Check if formatting worked
    if "•" in extracted_pf:
        print("   🎉 SUCCESS: Bullet points detected!")
        bullet_count = extracted_pf.count("•")
        print(f"   📊 Found {bullet_count} bullet points")
        print(f"   ✅ Principal findings formatting: WORKING")
    else:
        print("   ❌ FAILURE: No bullet points found")
        print(f"   🔍 Principal findings formatting: NOT WORKING")

    # Test conclusions
    conclusions_raw = report_data.get("conclusions", "")
    print(f"\n   📄 CONCLUSIONS TEST:")
    print(f"   Input length: {len(conclusions_raw)}")
    print(f"   Input preview: {repr(conclusions_raw[:150])}")

    extracted_conclusions = modal._extract_text_content(conclusions_raw)
    print(f"   Output length: {len(extracted_conclusions)}")
    print(f"   Output preview: {repr(extracted_conclusions[:200])}")

    if len(extracted_conclusions) > 2000:
        print("   ✅ SUCCESS: Substantial conclusions content")
        print(f"   ✅ Conclusions content: WORKING")
    else:
        print("   ⚠️  WARNING: Conclusions content shorter than expected")

    print(f"\n🎯 FINAL ASSESSMENT:")
    print("   Backend data: ✅ Available and correct")
    print("   KeyFindingsService: ✅ Created successfully")
    print("   Modal component: ✅ Retrieved successfully")

    # The key test - does it actually format?
    if "•" in extracted_pf:
        print("   🎉 MODAL FORMATTING: WORKING!")
        return True
    else:
        print("   ❌ MODAL FORMATTING: NOT WORKING")
        print("   🔍 Need to investigate why formatting isn't applied")
        return False


if __name__ == "__main__":
    success = test_key_findings_service_modal()
    sys.exit(0 if success else 1)
