#!/usr/bin/env python3
"""
Test script to verify single-source modal content generation.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.callbacks.kf_callbacks import register_kf_callbacks
from dashboard_app.key_findings.key_findings_service import KeyFindingsService
from dashboard_app.utils import run_async_in_sync_context
from dashboard_app.fix_source_mapping import map_display_names_to_source_ids


def test_modal_content_generation():
    """Test modal content generation for single-source analysis."""
    print("🧪 Testing modal content generation...")

    # Get database manager
    db_manager = get_precomputed_db_manager()

    # Test parameters
    selected_tool = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    print(f"🔍 Testing: {selected_tool} + {selected_sources} + {language}")

    # Map display names to source IDs
    selected_source_ids = map_display_names_to_source_ids(selected_sources)
    print(f"🔍 Mapped sources: {selected_sources} -> {selected_source_ids}")

    # Get the precomputed analysis
    hash_value = db_manager.generate_combination_hash(
        tool_name=selected_tool, selected_sources=selected_sources, language=language
    )
    print(f"🔍 Generated hash: {hash_value}")

    result = db_manager.get_combination_by_hash(hash_value)
    if not result:
        print("❌ No result found")
        return False

    print("✅ Result found in database")

    # Extract the report data (this is what gets passed to the modal)
    report_data = {
        "executive_summary": result.get("executive_summary", ""),
        "principal_findings": result.get("principal_findings", []),
        "temporal_analysis": result.get("temporal_analysis", ""),
        "seasonal_analysis": result.get("seasonal_analysis", ""),
        "fourier_analysis": result.get("fourier_analysis", ""),
        "strategic_synthesis": result.get("strategic_synthesis", ""),
        "conclusions": result.get("conclusions", ""),
        "pca_analysis": result.get("pca_analysis", ""),
        "heatmap_analysis": result.get("heatmap_analysis", ""),
    }

    print(f"📊 Report data structure:")
    for key, value in report_data.items():
        if isinstance(value, str):
            print(f"   {key}: {len(value)} chars")
        elif isinstance(value, list):
            print(f"   {key}: {len(value)} items")
        else:
            print(f"   {key}: {type(value)}")

    # Test the content extraction logic similar to the modal
    print(f"\n🔍 Testing content extraction:")

    # Simulate what happens in the modal
    ai_content = report_data
    print(f"Available sections: {list(ai_content.keys())}")

    # Test each section
    sections_to_test = [
        "executive_summary",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "strategic_synthesis",
        "conclusions",
    ]

    all_good = True
    for section in sections_to_test:
        content = ai_content.get(section, "No content available")
        if isinstance(content, str) and len(content) > 100:  # Reasonable content length
            print(f"✅ {section}: {len(content)} chars (good)")
        else:
            print(
                f"❌ {section}: {len(content) if isinstance(content, str) else 'invalid'} chars (too short)"
            )
            all_good = False

    # Test principal_findings specifically
    principal_findings = ai_content.get("principal_findings", [])
    if isinstance(principal_findings, list) and len(principal_findings) > 0:
        print(f"✅ principal_findings: {len(principal_findings)} items (good)")
    else:
        print(
            f"❌ principal_findings: {len(principal_findings) if isinstance(principal_findings, list) else 'invalid'} items"
        )
        all_good = False

    if all_good:
        print("\n🎉 All sections have proper content for modal display!")
        return True
    else:
        print("\n⚠️  Some sections are missing or too short")
        return False


if __name__ == "__main__":
    success = test_modal_content_generation()
    sys.exit(0 if success else 1)
